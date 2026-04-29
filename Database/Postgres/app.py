"""
PostgreSQL Database GUI Application
A tkinter-based GUI for interacting with PostgreSQL database.
Features: Add/List/Remove entries in a tab, and a logs tab for monitoring operations.
"""

import tkinter as tk
from tkinter import ttk, filedialog
from tkinter import scrolledtext
import threading
import logging
import json
import re
from tkinter import messagebox

from CRDP.CRDP_client import CRDPClient
from CRDP.config_manager import ConfigManager
from config import DB_CONFIG
from postgresql import PostgreSQLDatabase

# Configure logging to capture database operations
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class LogHandler(logging.Handler):
    """Custom logging handler to capture logs in the GUI."""

    def __init__(self, text_widget):
        super().__init__()
        self.text_widget = text_widget

    def emit(self, record):
        """Emit a log record to the text widget."""
        try:
            msg = self.format(record)
            self.text_widget.configure(state=tk.NORMAL)
            self.text_widget.insert(tk.END, msg + '\n')
            self.text_widget.see(tk.END)
            self.text_widget.configure(state=tk.DISABLED)
        except Exception:
            self.handleError(record)


class PostgreSQLGUI:
    """Main GUI application for PostgreSQL database operations."""

    def __init__(self, root, config: ConfigManager):
        """Initialize the GUI application."""
        self.root = root
        self.root.title("PostgreSQL Database Manager")
        self.root.geometry("900x750")
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.db = None
        self.current_table = "users"
        self.table_schema = None
        self.next_table_number = 1  # Track next UsersX number
        self.status_message = ""  # Store status message

        # Initialize CRDP client with configuration
        self.crdp_client = CRDPClient(config)
        # Default policies (will be updated from API)
        self.policy = config.get("crdp.protection_policy", "CRDP_Protection")
        self.reveal_username = config.get("crdp.reveal_username", "authorizedUser")

        # Create the UI
        self.create_widgets()

        # Try to connect to database
        self.connect_database()

    def create_widgets(self):
        """Create the main UI widgets."""
        # Create a notebook (tabbed interface)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Create tabs
        self.create_data_tab()
        self.create_logs_tab()

    def create_data_tab(self):
        """Create the data management tab."""
        self.data_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.data_frame, text="Data Management")

        # Top frame for table selection and controls
        top_frame = ttk.Frame(self.data_frame)
        top_frame.pack(fill=tk.X, padx=10, pady=10)

        ttk.Label(top_frame, text="Table:", font=("Arial", 10, "bold")).pack(side=tk.LEFT)

        self.table_var = tk.StringVar()
        self.table_combo = ttk.Combobox(
            top_frame, textvariable=self.table_var,
            values=[], width=15, state="readonly"
        )
        self.table_combo.pack(side=tk.LEFT, padx=5)
        self.table_combo.bind("<<ComboboxSelected>>", self.on_table_change)

        # Buttons
        ttk.Button(top_frame, text="Refresh", command=self.load_table_data).pack(side=tk.LEFT, padx=5)
        ttk.Button(top_frame, text="Create Table", command=self.create_new_users_table).pack(side=tk.LEFT, padx=5)
        ttk.Button(top_frame, text="Drop Table", command=self.drop_current_table).pack(side=tk.LEFT, padx=5)

        # Connection status
        self.status_label = ttk.Label(top_frame, text="Disconnected", foreground="red")
        self.status_label.pack(side=tk.RIGHT, padx=5)

        # Paned window for left (form) and right (table) sections
        paned = ttk.PanedWindow(self.data_frame, orient=tk.HORIZONTAL)
        paned.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # Left frame - Form for adding records
        left_frame = ttk.LabelFrame(paned, text="Add/Edit Record", padding=10)
        paned.add(left_frame, weight=1)

        self.form_fields = {}
        self.create_form_fields(left_frame)

        # Right frame - Table view
        right_frame = ttk.LabelFrame(paned, text="Records", padding=10)
        paned.add(right_frame, weight=1)

        self.create_table_view(right_frame)

        # Status message bar at the bottom
        status_bar_frame = ttk.Frame(self.data_frame)
        status_bar_frame.pack(fill=tk.X, padx=10, pady=5)

        self.status_message_label = ttk.Label(
            status_bar_frame,
            text="",
            foreground="blue",
            font=("Arial", 9),
            wraplength=700
        )
        self.status_message_label.pack(side=tk.LEFT, fill=tk.X, expand=True)

    def create_form_fields(self, parent):
        """Create dynamic form fields."""
        # Frame to hold form fields
        self.form_container = ttk.Frame(parent)
        self.form_container.pack(fill=tk.BOTH, expand=True)

        # Add default fields: Name, Email, SSN
        self.add_form_field("name", "Name", "text")
        self.add_form_field("email", "Email", "text")
        self.add_form_field("ssn", "SSN", "text")

        # Buttons frame
        button_frame = ttk.Frame(parent)
        button_frame.pack(fill=tk.X, pady=10)

        ttk.Button(button_frame, text="Protect and Add Record",
           command=lambda: self.add_record(protect=True)).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Add Record", command=self.add_record).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Clear Form", command=self.clear_form).pack(side=tk.LEFT, padx=5)

    def add_form_field(self, field_name: str, label: str, field_type: str = "text"):
        """Add a form field dynamically."""
        frame = ttk.Frame(self.form_container)
        frame.pack(fill=tk.X, pady=5)

        ttk.Label(frame, text=f"{label}:", width=15).pack(side=tk.LEFT)

        if field_type == "text":
            entry = ttk.Entry(frame, width=30)
            entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
            self.form_fields[field_name] = entry
        elif field_type == "number":
            entry = ttk.Entry(frame, width=30)
            entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
            self.form_fields[field_name] = entry
        elif field_type == "textarea":
            entry = tk.Text(frame, height=3, width=30)
            entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
            self.form_fields[field_name] = entry

    def create_table_view(self, parent):
        """Create the table view for displaying records."""
        # Frame for buttons
        button_frame = ttk.Frame(parent)
        button_frame.pack(fill=tk.X, pady=5)

        ttk.Button(button_frame, text="Delete Selected", command=self.delete_selected_record).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Export JSON", command=self.export_json).pack(side=tk.LEFT, padx=5)

        # Create treeview with scrollbars
        tree_frame = ttk.Frame(parent)
        tree_frame.pack(fill=tk.BOTH, expand=True)

        # Scrollbars
        vsb = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL)
        hsb = ttk.Scrollbar(tree_frame, orient=tk.HORIZONTAL)

        # Treeview
        self.tree = ttk.Treeview(
            tree_frame,
            columns=("id", "name", "email", "ssn"),
            height=15,
            yscrollcommand=vsb.set,
            xscrollcommand=hsb.set
        )

        vsb.config(command=self.tree.yview)
        hsb.config(command=self.tree.xview)

        # Define columns
        self.tree.column("#0", width=0, stretch=tk.NO)
        self.tree.column("id", anchor=tk.W, width=50)
        self.tree.column("name", anchor=tk.W, width=120)
        self.tree.column("email", anchor=tk.W, width=150)
        self.tree.column("ssn", anchor=tk.W, width=120)

        # Create headings
        self.tree.heading("#0", text="")
        self.tree.heading("id", text="ID")
        self.tree.heading("name", text="Name")
        self.tree.heading("email", text="Email")
        self.tree.heading("ssn", text="SSN")

        # Grid layout
        self.tree.grid(row=0, column=0, sticky='nsew')
        vsb.grid(row=0, column=1, sticky='ns')
        hsb.grid(row=1, column=0, sticky='ew')
        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)

        # Bind double-click to edit
        self.tree.bind("<Double-1>", self.on_tree_double_click)

    def create_logs_tab(self):
        """Create the logs tab."""
        self.logs_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.logs_frame, text="Logs")

        # Toolbar
        toolbar = ttk.Frame(self.logs_frame)
        toolbar.pack(fill=tk.X, padx=10, pady=5)

        ttk.Button(toolbar, text="Clear Logs", command=self.clear_logs).pack(side=tk.LEFT, padx=5)
        ttk.Button(toolbar, text="Save Logs", command=self.save_logs).pack(side=tk.LEFT, padx=5)

        # Log text widget
        self.log_text = scrolledtext.ScrolledText(
            self.logs_frame,
            wrap=tk.WORD,
            height=30,
            width=100,
            bg="black",
            fg="lime",
            font=("Courier", 9)
        )
        self.log_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.log_text.configure(state=tk.DISABLED)

        # Add custom log handler
        self.log_handler = LogHandler(self.log_text)
        self.log_handler.setFormatter(
            logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        )
        logger.addHandler(self.log_handler)

        # Log initial message
        logger.info("Application started")

    def connect_database(self):
        """Connect to the database in a separate thread."""
        def connect():
            try:
                self.db = PostgreSQLDatabase(**DB_CONFIG)
                self.update_status("Connected", "green")
                logger.info(f"✓ Successfully connected to PostgreSQL at {DB_CONFIG['host']}:{DB_CONFIG['port']}")
                self.root.after(0, self.refresh_available_tables)
            except Exception as e:
                self.update_status("Connection Failed", "red")
                logger.error(f"✗ Failed to connect: {str(e)}")
                self.show_status_message(f"Connection Error: {str(e)}")

        thread = threading.Thread(target=connect, daemon=True)
        thread.start()

    def update_status(self, status: str, color: str):
        """Update the connection status label."""
        self.root.after(0, lambda: self.status_label.config(text=status, foreground=color))

    def show_status_message(self, message: str, duration=5000):
        """Show a status message at the bottom of the window."""
        self.status_message = message
        self.root.after(0, lambda: self.status_message_label.config(text=message))
        # Auto-clear message after duration (in milliseconds)
        if duration > 0:
            self.root.after(duration, lambda: self.root.after(0, lambda: self.status_message_label.config(text="")))

    def refresh_available_tables(self, select_latest=False, select_first=False):
        """Refresh the list of available UsersX tables in the dropdown."""
        if not self.db:
            return

        def refresh():
            try:
                # Get list of all tables
                tables = self.db.get_all_tables()

                # Filter for UsersX pattern tables (case-insensitive, matches Users1, Users2, etc.)
                users_tables = [t for t in tables if re.match(r'^Users\d+$', t, re.IGNORECASE)]

                # Sort by number
                def extract_number(table_name):
                    match = re.search(r'\d+', table_name)
                    return int(match.group()) if match else 0

                users_tables.sort(key=extract_number)

                # Update dropdown
                if users_tables:
                    self.root.after(0, lambda: self.table_combo.configure(values=users_tables))
                    # Select table based on parameters
                    if select_latest:
                        # After table creation - select the newly created table (last one)
                        self.root.after(0, lambda: self.table_combo.set(users_tables[-1]))
                        self.root.after(0, self.load_table_data)
                    elif select_first:
                        # After table deletion - select the first available table
                        self.root.after(0, lambda: self.table_combo.set(users_tables[0]))
                        self.root.after(0, self.load_table_data)
                    elif not self.table_var.get():
                        # On initial connection - select first table if none selected
                        self.root.after(0, lambda: self.table_combo.set(users_tables[0]))
                        self.root.after(0, self.load_table_data)
                    # Calculate next table number
                    self.next_table_number = extract_number(users_tables[-1]) + 1
                else:
                    self.root.after(0, lambda: self.table_combo.configure(values=[]))
                    self.root.after(0, lambda: self.table_var.set(""))
                    self.next_table_number = 1

            except Exception as e:
                logger.error(f"Error refreshing tables: {str(e)}")

        thread = threading.Thread(target=refresh, daemon=True)
        thread.start()

    def load_table_data(self):
        """Load data from the selected table."""
        if not self.db:
            self.show_status_message("Not connected to database")
            return

        table_name = self.table_var.get()
        if not table_name:
            return

        def load():
            try:
                # Get table info
                columns = self.db.get_table_info(table_name)
                if not columns:
                    logger.warning(f"Table '{table_name}' does not exist")
                    self.root.after(0, lambda: self.show_status_message(f"Table '{table_name}' not found"))
                    return

                # Clear existing tree items
                for item in self.tree.get_children():
                    self.tree.delete(item)

                # Update tree columns based on table schema
                column_names = [col['column_name'] for col in columns]
                self.tree.configure(columns=column_names)

                # Configure columns
                self.tree.column("#0", width=0, stretch=tk.NO)
                for col in column_names:
                    self.tree.column(col, anchor=tk.W, width=100)
                    self.tree.heading(col, text=col)

                # Fetch records
                records = self.db.select_all(table_name)
                for record in records:
                    values = [record.get(col, "") for col in column_names]
                    self.tree.insert("", tk.END, values=values)

                logger.info(f"Loaded {len(records)} records from table '{table_name}'")
            except Exception as e:
                logger.error(f"Error loading table data: {str(e)}")
                self.root.after(0, lambda: self.show_status_message(f"Error loading table data: {str(e)}"))

        thread = threading.Thread(target=load, daemon=True)
        thread.start()

    def on_table_change(self, event=None):
        """Handle table selection change."""
        self.load_table_data()

    def add_record(self, protect=False):
        # Collect form data
        record = {}
        for field_name, widget in self.form_fields.items():
            value = widget.get()
            if value:
                record[field_name] = value

        if not record:
            self.show_status_message("Please fill in at least one field")
            return

        """Protect the SSN field"""
        if protect:
            ssn_value = self.form_fields.get("ssn").get()
            if ssn_value:
                # Call CRDP protect API
                try:
                    protected_data = self.crdp_client.protect(ssn_value, self.policy)
                    if protected_data and "protected_data" in protected_data:
                        record["ssn"] = protected_data["protected_data"]
                        logger.info(f"SSN protected using CRDP: {record["ssn"]}")
                    else:
                        logger.error("Failed to protect SSN: No protected data returned")
                except Exception as e:
                    logger.error(f"Error protecting SSN: {str(e)}")
                    self.show_status_message(f"Error protecting SSN: {str(e)}")

        """Add a new record to the table."""
        if not self.db:
            self.show_status_message("Not connected to database")
            return

        table_name = self.table_var.get()
        if not table_name:
            self.show_status_message("No table selected")
            return

        def insert():
            try:
                success = self.db.insert_record(table_name, record)
                if success:
                    logger.info(f"✓ Inserted record into '{table_name}': {record}")
                    self.root.after(0, lambda: self.show_status_message(f"Record added to {table_name} successfully"))
                    self.root.after(0, self.load_table_data)
                    self.root.after(0, self.clear_form)
                else:
                    logger.error(f"✗ Failed to insert record into '{table_name}'")
                    self.root.after(0, lambda: self.show_status_message(f"Failed to insert record into {table_name}"))
            except Exception as e:
                logger.error(f"Error inserting record: {str(e)}")
                self.root.after(0, lambda: self.show_status_message(f"Error: {str(e)}"))

        thread = threading.Thread(target=insert, daemon=True)
        thread.start()

    def delete_selected_record(self):
        """Delete the selected record from the table."""
        if not self.db:
            self.show_status_message("Not connected to database")
            return

        selected = self.tree.selection()
        if not selected:
            self.show_status_message("Please select a record to delete")
            return

        table_name = self.table_var.get()
        if not table_name:
            self.show_status_message("No table selected")
            return

        def delete():
            try:
                deleted_count = 0
                for item in selected:
                    values = self.tree.item(item, "values")
                    if values:
                        # Assume first column is ID
                        record_id = values[0]
                        deleted = self.db.delete_records(table_name, "id = %s", (record_id,))
                        deleted_count += deleted

                logger.info(f"✓ Deleted {deleted_count} record(s) from '{table_name}'")
                self.root.after(0, lambda: self.show_status_message(f"Deleted {deleted_count} record(s) from {table_name}"))
                self.root.after(0, self.load_table_data)
            except Exception as e:
                logger.error(f"Error deleting record: {str(e)}")
                self.root.after(0, lambda: self.show_status_message(f"Error: {str(e)}"))

        thread = threading.Thread(target=delete, daemon=True)
        thread.start()

    def on_tree_double_click(self, event):
        # Get selected item
        selected_item = self.tree.selection()
        if selected_item:
            item_id = selected_item[0]
            values = self.tree.item(item_id, "values")

            protect_ssn_value = values[3]
            try:
                revealed_ssn = self.crdp_client.reveal(protect_ssn_value, self.policy, self.reveal_username)
                if revealed_ssn:
                    messagebox.showinfo("Revealed SSN", f"Name: {values[1]}\nEmail: {values[2]}\nSSN: {revealed_ssn}")
                else:
                    logger.error("Failed to reveal SSN: No revealed data returned")
            except Exception as e:
                logger.error(f"Error revealing SSN: {str(e)}")
                self.show_status_message(f"Error revealing SSN: {str(e)}")

    def clear_form(self):
        """Clear all form fields."""
        for widget in self.form_fields.values():
            widget.delete(0, tk.END)

    def create_new_users_table(self):
        """Create a new UsersX table with the fixed schema (Name, Email, SSN)."""
        if not self.db:
            self.show_status_message("Not connected to database")
            return

        # Use the next available table number
        table_name = f"Users{self.next_table_number}"

        # Define the fixed schema
        schema = {
            "id": "SERIAL PRIMARY KEY",
            "name": "VARCHAR(255)",
            "email": "VARCHAR(255)",
            "ssn": "VARCHAR(255)"
        }

        def create():
            try:
                if self.db.create_table(table_name, schema):
                    logger.info(f"✓ Created table '{table_name}' with columns: Name, Email, SSN")
                    self.show_status_message(f"Table {table_name} created with columns: Name, Email, SSN")
                    self.next_table_number += 1
                    self.root.after(0, lambda: self.refresh_available_tables(select_latest=True))
                else:
                    logger.error(f"Failed to create table '{table_name}'")
                    self.show_status_message(f"Failed to create table {table_name}")
            except Exception as e:
                logger.error(f"Error creating table: {str(e)}")
                self.show_status_message(f"Error creating table: {str(e)}")

        thread = threading.Thread(target=create, daemon=True)
        thread.start()

    def drop_current_table(self):
        """Drop the currently selected table."""
        if not self.db:
            self.show_status_message("Not connected to database")
            return

        table_name = self.table_var.get()
        if not table_name:
            self.show_status_message("No table selected")
            return

        def drop():
            try:
                if self.db.drop_table(table_name):
                    logger.info(f"✓ Dropped table '{table_name}'")
                    self.show_status_message(f"Table {table_name} dropped successfully")
                    self.root.after(0, lambda: self.refresh_available_tables(select_first=True))
                else:
                    logger.error(f"Failed to drop table '{table_name}'")
                    self.show_status_message(f"Failed to drop table {table_name}")
            except Exception as e:
                logger.error(f"Error dropping table: {str(e)}")
                self.show_status_message(f"Error dropping table: {str(e)}")

        thread = threading.Thread(target=drop, daemon=True)
        thread.start()

    def export_json(self):
        """Export current table data as JSON."""
        if not self.db:
            self.show_status_message("Not connected to database")
            return

        table_name = self.table_var.get()
        if not table_name:
            self.show_status_message("No table selected")
            return

        def export():
            try:
                records = self.db.select_all(table_name)
                json_data = json.dumps(records, indent=2, default=str)

                # Save to file dialog
                file_path = filedialog.asksaveasfilename(
                    defaultextension=".json",
                    filetypes=[("JSON files", "*.json"), ("Text files", "*.txt")]
                )

                if file_path:
                    with open(file_path, 'w') as f:
                        f.write(json_data)
                    logger.info(f"✓ Exported {len(records)} records from '{table_name}' to {file_path}")
                    self.root.after(0, lambda: self.show_status_message(f"Exported {len(records)} records from {table_name} to JSON file"))
                else:
                    self.root.after(0, lambda: self.show_status_message("Export cancelled"))
            except Exception as e:
                logger.error(f"Error exporting data: {str(e)}")
                self.root.after(0, lambda: self.show_status_message(f"Error exporting data: {str(e)}"))

        thread = threading.Thread(target=export, daemon=True)
        thread.start()

    def clear_logs(self):
        """Clear the logs text widget."""
        self.log_text.configure(state=tk.NORMAL)
        self.log_text.delete("1.0", tk.END)
        self.log_text.configure(state=tk.DISABLED)

    def save_logs(self):
        """Save logs to a file."""
        file_path = filedialog.asksaveasfilename(
            defaultextension=".log",
            filetypes=[("Log files", "*.log"), ("Text files", "*.txt")]
        )

        if file_path:
            try:
                self.log_text.configure(state=tk.NORMAL)
                logs = self.log_text.get("1.0", tk.END)
                self.log_text.configure(state=tk.DISABLED)

                with open(file_path, 'w') as f:
                    f.write(logs)

                logger.info(f"✓ Logs saved to '{file_path}'")
                self.show_status_message(f"Logs saved to file successfully")
            except Exception as e:
                logger.error(f"Error saving logs: {str(e)}")
                self.show_status_message(f"Error saving logs: {str(e)}")

    def on_closing(self):
        """Handle application closing."""
        if self.db:
            self.db.close_all_connections()
            logger.info("Database connections closed")
        self.root.destroy()


def main():
    """Main entry point."""
    # Load configuration
    config = ConfigManager()

    root = tk.Tk()
    app = PostgreSQLGUI(root, config)
    root.mainloop()


if __name__ == "__main__":
    main()
