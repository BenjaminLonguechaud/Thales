"""
PostgreSQL Database GUI Application
A tkinter-based GUI for interacting with PostgreSQL database.
Features: Add/List/Remove entries in a tab, and a logs tab for monitoring operations.
"""

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from tkinter import scrolledtext
import threading
import logging
from datetime import datetime
from typing import List, Dict, Any
import json

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

    def __init__(self, root):
        """Initialize the GUI application."""
        self.root = root
        self.root.title("PostgreSQL Database Manager")
        self.root.geometry("900x700")
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.db = None
        self.current_table = "users"
        self.table_schema = None

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

        self.table_var = tk.StringVar(value="users")
        self.table_combo = ttk.Combobox(
            top_frame, textvariable=self.table_var,
            values=["users", "products", "orders", "custom"],
            width=15, state="readonly"
        )
        self.table_combo.pack(side=tk.LEFT, padx=5)
        self.table_combo.bind("<<ComboboxSelected>>", self.on_table_change)

        # Buttons
        ttk.Button(top_frame, text="Refresh", command=self.load_table_data).pack(side=tk.LEFT, padx=5)
        ttk.Button(top_frame, text="Create Table", command=self.create_table_dialog).pack(side=tk.LEFT, padx=5)
        ttk.Button(top_frame, text="Drop Table", command=self.drop_table_dialog).pack(side=tk.LEFT, padx=5)

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

    def create_form_fields(self, parent):
        """Create dynamic form fields."""
        # Frame to hold form fields
        self.form_container = ttk.Frame(parent)
        self.form_container.pack(fill=tk.BOTH, expand=True)

        # Add default fields
        self.add_form_field("name", "Name", "text")
        self.add_form_field("email", "Email", "text")

        # Buttons frame
        button_frame = ttk.Frame(parent)
        button_frame.pack(fill=tk.X, pady=10)

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
            columns=("id", "name", "email"),
            height=15,
            yscrollcommand=vsb.set,
            xscrollcommand=hsb.set
        )

        vsb.config(command=self.tree.yview)
        hsb.config(command=self.tree.xview)

        # Define columns
        self.tree.column("#0", width=0, stretch=tk.NO)
        self.tree.column("id", anchor=tk.W, width=50)
        self.tree.column("name", anchor=tk.W, width=150)
        self.tree.column("email", anchor=tk.W, width=200)

        # Create headings
        self.tree.heading("#0", text="")
        self.tree.heading("id", text="ID")
        self.tree.heading("name", text="Name")
        self.tree.heading("email", text="Email")

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
                self.load_table_data()
            except Exception as e:
                self.update_status("Connection Failed", "red")
                logger.error(f"✗ Failed to connect: {str(e)}")
                messagebox.showerror("Connection Error", f"Could not connect to database:\n{str(e)}")

        thread = threading.Thread(target=connect, daemon=True)
        thread.start()

    def update_status(self, status: str, color: str):
        """Update the connection status label."""
        self.root.after(0, lambda: self.status_label.config(text=status, foreground=color))

    def load_table_data(self):
        """Load data from the selected table."""
        if not self.db:
            messagebox.showwarning("Warning", "Not connected to database")
            return

        table_name = self.table_var.get()

        def load():
            try:
                # Get table info
                columns = self.db.get_table_info(table_name)
                if not columns:
                    logger.warning(f"Table '{table_name}' does not exist")
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

        thread = threading.Thread(target=load, daemon=True)
        thread.start()

    def on_table_change(self, event=None):
        """Handle table selection change."""
        self.load_table_data()

    def add_record(self):
        """Add a new record to the table."""
        if not self.db:
            messagebox.showwarning("Warning", "Not connected to database")
            return

        # Collect form data
        record = {}
        for field_name, widget in self.form_fields.items():
            value = widget.get()
            if value:
                record[field_name] = value

        if not record:
            messagebox.showwarning("Warning", "Please fill in at least one field")
            return

        table_name = self.table_var.get()

        def insert():
            try:
                success = self.db.insert_record(table_name, record)
                if success:
                    logger.info(f"✓ Inserted record into '{table_name}': {record}")
                    self.root.after(0, lambda: messagebox.showinfo("Success", "Record added successfully"))
                    self.root.after(0, self.load_table_data)
                    self.root.after(0, self.clear_form)
                else:
                    logger.error(f"✗ Failed to insert record into '{table_name}'")
                    self.root.after(0, lambda: messagebox.showerror("Error", "Failed to insert record"))
            except Exception as e:
                logger.error(f"Error inserting record: {str(e)}")
                self.root.after(0, lambda: messagebox.showerror("Error", f"Error: {str(e)}"))

        thread = threading.Thread(target=insert, daemon=True)
        thread.start()

    def delete_selected_record(self):
        """Delete the selected record from the table."""
        if not self.db:
            messagebox.showwarning("Warning", "Not connected to database")
            return

        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a record to delete")
            return

        if messagebox.askyesno("Confirm", "Delete the selected record(s)?"):
            table_name = self.table_var.get()

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
                    self.root.after(0, self.load_table_data)
                    self.root.after(0, lambda: messagebox.showinfo("Success", f"Deleted {deleted_count} record(s)"))
                except Exception as e:
                    logger.error(f"Error deleting record: {str(e)}")
                    self.root.after(0, lambda: messagebox.showerror("Error", f"Error: {str(e)}"))

            thread = threading.Thread(target=delete, daemon=True)
            thread.start()

    def on_tree_double_click(self, event):
        """Handle double-click on tree item to edit."""
        item = self.tree.selection()
        if item:
            messagebox.showinfo("Info", "Edit feature coming soon")

    def clear_form(self):
        """Clear all form fields."""
        for widget in self.form_fields.values():
            widget.delete(0, tk.END)

    def create_table_dialog(self):
        """Show dialog to create a new table."""
        dialog = tk.Toplevel(self.root)
        dialog.title("Create Table")
        dialog.geometry("400x300")

        ttk.Label(dialog, text="Table Name:", font=("Arial", 10, "bold")).pack(pady=5)
        table_name_entry = ttk.Entry(dialog, width=30)
        table_name_entry.pack(pady=5)

        ttk.Label(dialog, text="Columns (JSON format):", font=("Arial", 10, "bold")).pack(pady=5)
        columns_text = tk.Text(dialog, height=10, width=45)
        columns_text.pack(pady=5)
        columns_text.insert("1.0", '{\n  "id": "SERIAL PRIMARY KEY",\n  "name": "VARCHAR(255)",\n  "email": "VARCHAR(255)"\n}')

        def create():
            try:
                table_name = table_name_entry.get().strip()
                if not table_name:
                    messagebox.showwarning("Warning", "Please enter a table name")
                    return

                columns_json = columns_text.get("1.0", tk.END)
                schema = json.loads(columns_json)

                if self.db.create_table(table_name, schema):
                    logger.info(f"✓ Created table '{table_name}'")
                    messagebox.showinfo("Success", f"Table '{table_name}' created successfully")
                    dialog.destroy()
                    self.load_table_data()
            except json.JSONDecodeError:
                messagebox.showerror("Error", "Invalid JSON format")
            except Exception as e:
                logger.error(f"Error creating table: {str(e)}")
                messagebox.showerror("Error", f"Error: {str(e)}")

        ttk.Button(dialog, text="Create", command=create).pack(pady=10)

    def drop_table_dialog(self):
        """Show dialog to drop a table."""
        table_name = self.table_var.get()
        if messagebox.askyesno("Confirm", f"Drop table '{table_name}'? This cannot be undone."):
            if self.db.drop_table(table_name):
                logger.info(f"✓ Dropped table '{table_name}'")
                messagebox.showinfo("Success", f"Table '{table_name}' dropped successfully")
                self.load_table_data()

    def export_json(self):
        """Export current table data as JSON."""
        if not self.db:
            messagebox.showwarning("Warning", "Not connected to database")
            return

        table_name = self.table_var.get()

        def export():
            try:
                records = self.db.select_all(table_name)
                json_data = json.dumps(records, indent=2, default=str)

                # Show in new window
                export_window = tk.Toplevel(self.root)
                export_window.title(f"Export: {table_name}")
                export_window.geometry("600x400")

                text_widget = scrolledtext.ScrolledText(export_window, wrap=tk.WORD)
                text_widget.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
                text_widget.insert("1.0", json_data)
                text_widget.configure(state=tk.DISABLED)

                logger.info(f"✓ Exported {len(records)} records from '{table_name}' to JSON")
            except Exception as e:
                logger.error(f"Error exporting data: {str(e)}")
                self.root.after(0, lambda: messagebox.showerror("Error", f"Error: {str(e)}"))

        thread = threading.Thread(target=export, daemon=True)
        thread.start()

    def clear_logs(self):
        """Clear the logs text widget."""
        self.log_text.configure(state=tk.NORMAL)
        self.log_text.delete("1.0", tk.END)
        self.log_text.configure(state=tk.DISABLED)

    def save_logs(self):
        """Save logs to a file."""
        from tkinter import filedialog
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
                messagebox.showinfo("Success", "Logs saved successfully")
            except Exception as e:
                logger.error(f"Error saving logs: {str(e)}")
                messagebox.showerror("Error", f"Error saving logs: {str(e)}")

    def on_closing(self):
        """Handle application closing."""
        if self.db:
            self.db.close_all_connections()
            logger.info("Database connections closed")
        self.root.destroy()


def main():
    """Main entry point."""
    root = tk.Tk()
    app = PostgreSQLGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
