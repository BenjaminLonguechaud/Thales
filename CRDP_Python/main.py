#!/usr/bin/env python3
"""
CRDP Data Protection Application
A user-friendly GUI for protecting and revealing sensitive data using CipherTrust CRDP.
"""

import tkinter as tk
from tkinter import ttk, scrolledtext
import json
from datetime import datetime

from logger import logger
from config_manager import ConfigManager
from CRDP_client import CRDPClient
import styles

class CRDPApplication:
    """Main GUI application for CRDP data protection."""

    def __init__(self, root, config: ConfigManager):
        """Initialize the application.

        Args:
            root: Tkinter root window
            config: ConfigManager instance
        """
        self.root = root
        self.config = config

        # Get UI dimensions from config
        window_width = config.get("ui.window_width", styles.WINDOW_WIDTH)
        window_height = config.get("ui.window_height", styles.WINDOW_HEIGHT)

        self.root.title(styles.APP_TITLE)
        self.root.geometry(f"{window_width}x{window_height}")
        self.root.minsize(600, 500)  # Ensure window is large enough to show status bar
        self.root.configure(bg=styles.WINDOW_BG)

        # Initialize CRDP client with configuration
        self.crdp_client = CRDPClient(config)

        # Default policies (will be updated from API)
        self.available_policies = self.crdp_client.load_policies()

        # Set up the GUI
        self._setup_ui()

    def _setup_ui(self):
        """Set up the user interface."""
        # Title
        title_frame = ttk.Frame(self.root)
        title_frame.pack(fill=tk.X, padx=styles.TITLE_FRAME_PADDING_X, pady=styles.TITLE_FRAME_PADDING_Y)

        title_label = ttk.Label(title_frame, text=styles.APP_TITLE,
                               font=styles.FONT_TITLE)
        title_label.pack()

        subtitle = ttk.Label(title_frame, text=styles.APP_SUBTITLE,
                            font=styles.FONT_SUBTITLE, foreground=styles.TEXT_SECONDARY_FG)
        subtitle.pack()

        # Create status bar FIRST (before notebook) so it stays at the bottom
        self._create_status_bar()

        # Create notebook (tabs) - will expand to fill remaining space above status bar
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=styles.NOTEBOOK_PADX, pady=styles.NOTEBOOK_PADY)

        # Create tabs
        self._create_protect_tab()
        self._create_reveal_tab()
        self._create_performance_tab()
        self._create_status_tab()

    def _create_protect_tab(self):
        """Create the data protection tab."""
        protect_frame = ttk.Frame(self.notebook, padding=styles.FRAME_PADDING)
        self.notebook.add(protect_frame, text=styles.TAB_PROTECT)

        # Input fields
        ttk.Label(protect_frame, text=styles.LABEL_DATA_TO_PROTECT, font=styles.FONT_LABEL_BOLD).grid(
            row=0, column=0, columnspan=2, sticky=styles.STICKY_W, pady=styles.PADY_LABEL)

        self.protect_data_text = scrolledtext.ScrolledText(
            protect_frame, height=styles.TEXT_HEIGHT_SMALL, width=styles.TEXT_WIDTH_NORMAL, wrap=tk.WORD, font=styles.FONT_MONOSPACE)
        self.protect_data_text.grid(row=1, column=0, columnspan=2, sticky=styles.STICKY_NSEW, pady=styles.PADY_SECTION)
        protect_frame.rowconfigure(1, weight=1)

        # Policy selection
        ttk.Label(protect_frame, text=styles.LABEL_PROTECTION_POLICY, font=styles.FONT_LABEL).grid(
            row=2, column=0, sticky=styles.STICKY_W, pady=styles.PADY_LABEL)
        self.protect_policy_var = tk.StringVar()
        self.protect_policy_combo = ttk.Combobox(
            protect_frame, textvariable=self.protect_policy_var, state='readonly', width=37)
        self.protect_policy_combo['values'] = self.available_policies
        if self.available_policies:
            self.protect_policy_combo.set(self.available_policies[0])
        self.protect_policy_combo.grid(row=2, column=1, sticky=styles.STICKY_EW, pady=styles.PADY_WIDGET)

        # Protect button
        protect_button = ttk.Button(
            protect_frame, text=styles.BUTTON_PROTECT_DATA, command=self._on_protect_click)
        protect_button.grid(row=3, column=0, columnspan=2, sticky=styles.STICKY_EW, pady=styles.PADY_BUTTON)

        # Result frame
        ttk.Label(protect_frame, text=styles.LABEL_PROTECTED_DATA, font=styles.FONT_LABEL_BOLD).grid(
            row=4, column=0, columnspan=2, sticky=styles.STICKY_W, pady=styles.PADY_LABEL)

        self.protect_result_text = scrolledtext.ScrolledText(
            protect_frame, height=styles.TEXT_HEIGHT_SMALL, width=styles.TEXT_WIDTH_NORMAL, wrap=tk.WORD, font=styles.FONT_MONOSPACE,
            state=tk.DISABLED, bg=styles.TEXT_DISABLED_BG)
        self.protect_result_text.grid(row=5, column=0, columnspan=2, sticky=styles.STICKY_NSEW, pady=styles.PADY_WIDGET)

        # Copy button
        copy_button = ttk.Button(
            protect_frame, text=styles.BUTTON_COPY_PROTECTED, command=self._copy_protected_data)
        copy_button.grid(row=6, column=0, columnspan=2, sticky=styles.STICKY_EW)

        protect_frame.columnconfigure(1, weight=1)
        protect_frame.rowconfigure(5, weight=1)

    def _create_reveal_tab(self):
        """Create the data revelation tab."""
        reveal_frame = ttk.Frame(self.notebook, padding=styles.FRAME_PADDING)
        self.notebook.add(reveal_frame, text=styles.TAB_REVEAL)

        # Input fields
        ttk.Label(reveal_frame, text=styles.LABEL_PROTECTED_DATA, font=styles.FONT_LABEL_BOLD).grid(
            row=0, column=0, columnspan=2, sticky=styles.STICKY_W, pady=styles.PADY_LABEL)

        self.reveal_data_text = scrolledtext.ScrolledText(
            reveal_frame, height=styles.TEXT_HEIGHT_SMALL, width=styles.TEXT_WIDTH_NORMAL, wrap=tk.WORD, font=styles.FONT_MONOSPACE)
        self.reveal_data_text.grid(row=1, column=0, columnspan=2, sticky=styles.STICKY_NSEW, pady=styles.PADY_SECTION)
        reveal_frame.rowconfigure(1, weight=1)

        # Protection Policy field
        ttk.Label(reveal_frame, text=styles.LABEL_PROTECTION_POLICY, font=styles.FONT_LABEL).grid(
            row=2, column=0, sticky=styles.STICKY_W, pady=styles.PADY_LABEL)
        self.reveal_policy_var = tk.StringVar()
        self.reveal_policy_combo = ttk.Combobox(
            reveal_frame, textvariable=self.reveal_policy_var, state='readonly', width=37)
        self.reveal_policy_combo['values'] = self.available_policies
        if self.available_policies:
            self.reveal_policy_combo.set(self.available_policies[0])
        self.reveal_policy_combo.grid(row=2, column=1, sticky=styles.STICKY_EW, pady=styles.PADY_WIDGET)

        # Username field (mandatory)
        ttk.Label(reveal_frame, text=styles.LABEL_USERNAME, font=styles.FONT_LABEL).grid(
            row=3, column=0, sticky=styles.STICKY_W, pady=styles.PADY_LABEL)
        self.reveal_username = ttk.Entry(reveal_frame, width=styles.ENTRY_WIDTH)
        self.reveal_username.grid(row=3, column=1, sticky=styles.STICKY_EW, pady=styles.PADY_WIDGET)
        ttk.Label(reveal_frame, text=styles.LABEL_USERNAME_HELP,
                 font=styles.FONT_LABEL, foreground=styles.TEXT_SECONDARY_FG).grid(row=4, column=0, columnspan=2, sticky=styles.STICKY_W)

        # Reveal button
        reveal_button = ttk.Button(
            reveal_frame, text=styles.BUTTON_REVEAL_DATA, command=self._on_reveal_click)
        reveal_button.grid(row=5, column=0, columnspan=2, sticky=styles.STICKY_EW, pady=styles.PADY_BUTTON)

        # Result frame
        ttk.Label(reveal_frame, text=styles.LABEL_REVEALED_DATA, font=styles.FONT_LABEL_BOLD).grid(
            row=6, column=0, columnspan=2, sticky=styles.STICKY_W, pady=styles.PADY_LABEL)

        self.reveal_result_text = scrolledtext.ScrolledText(
            reveal_frame, height=styles.TEXT_HEIGHT_SMALL, width=styles.TEXT_WIDTH_NORMAL, wrap=tk.WORD, font=styles.FONT_MONOSPACE,
            state=tk.DISABLED, bg=styles.TEXT_DISABLED_BG)
        self.reveal_result_text.grid(row=7, column=0, columnspan=2, sticky=styles.STICKY_NSEW, pady=styles.PADY_WIDGET)

        # Copy button
        copy_button = ttk.Button(
            reveal_frame, text=styles.BUTTON_COPY_REVEALED, command=self._copy_revealed_data)
        copy_button.grid(row=8, column=0, columnspan=2, sticky=styles.STICKY_EW)

        reveal_frame.columnconfigure(1, weight=1)
        reveal_frame.rowconfigure(7, weight=1)

    def _create_performance_tab(self):
        """Create the performance metrics and liveness tab."""
        perf_frame = ttk.Frame(self.notebook, padding=styles.FRAME_PADDING)
        self.notebook.add(perf_frame, text=styles.TAB_PERFORMANCE)

        # Metrics section
        ttk.Label(perf_frame, text=styles.LABEL_PERFORMANCE_METRICS, font=styles.FONT_LABEL_BOLD).pack(
            anchor=styles.STICKY_W, pady=styles.PACK_PADDING_SMALL)

        metrics_button = ttk.Button(
            perf_frame, text=styles.BUTTON_FETCH_METRICS, command=self._on_metrics_click)
        metrics_button.pack(anchor=styles.STICKY_W, pady=styles.PACK_PADDING_MEDIUM)

        self.metrics_text = scrolledtext.ScrolledText(
            perf_frame, height=styles.TEXT_HEIGHT_SMALL, width=styles.TEXT_WIDTH_WIDE, wrap=tk.WORD, font=styles.FONT_MONOSPACE,
            state=tk.DISABLED, bg=styles.TEXT_DISABLED_BG)
        self.metrics_text.pack(fill=tk.BOTH, expand=True, pady=styles.PACK_PADDING_LARGE)

        # Separator
        ttk.Separator(perf_frame, orient=styles.SEPARATOR_ORIENTATION).pack(fill=tk.X, pady=styles.SEPARATOR_PADDING_Y)

        # Liveness section
        ttk.Label(perf_frame, text=styles.LABEL_LIVENESS_STATUS, font=styles.FONT_LABEL_BOLD).pack(
            anchor=styles.STICKY_W, pady=styles.PACK_PADDING_SMALL)

        liveness_button = ttk.Button(
            perf_frame, text=styles.BUTTON_CHECK_LIVENESS, command=self._on_liveness_click)
        liveness_button.pack(anchor=styles.STICKY_W, pady=styles.PACK_PADDING_MEDIUM)

        self.liveness_text = scrolledtext.ScrolledText(
            perf_frame, height=styles.TEXT_HEIGHT_SMALL, width=styles.TEXT_WIDTH_WIDE, wrap=tk.WORD, font=styles.FONT_MONOSPACE,
            state=tk.DISABLED, bg=styles.TEXT_DISABLED_BG)
        self.liveness_text.pack(fill=tk.BOTH, expand=True)

    def _create_status_tab(self):
        """Create the status/logs tab."""
        status_frame = ttk.Frame(self.notebook, padding=styles.FRAME_PADDING)
        self.notebook.add(status_frame, text=styles.TAB_STATUS)

        # Info section
        ttk.Label(status_frame, text=styles.LABEL_CONNECTION_STATUS, font=styles.FONT_LABEL_BOLD).pack(
            anchor=styles.STICKY_W, pady=styles.PACK_PADDING_SMALL)

        self.status_text = tk.Text(status_frame, height=styles.TEXT_HEIGHT_LARGE, width=styles.TEXT_WIDTH_WIDE, font=styles.FONT_MONOSPACE,
                                  state=tk.DISABLED, bg=styles.TEXT_DISABLED_BG)
        self.status_text.pack(fill=tk.BOTH, expand=True, pady=styles.PACK_PADDING_MEDIUM)

        # Refresh button
        refresh_button = ttk.Button(
            status_frame, text=styles.BUTTON_REFRESH_STATUS, command=self._update_status)
        refresh_button.pack(anchor=tk.E)

        # Initial status update
        self._update_status()

    def _create_status_bar(self):
        """Create the status bar at the bottom of the main window."""
        # Status bar frame - packed at the bottom to stay always visible
        status_bar_frame = tk.Frame(self.root, bg=styles.STATUS_BAR_BG)
        status_bar_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=styles.STATUS_BAR_PADX, pady=styles.STATUS_BAR_PADY)

        # Status label
        self.status_bar_label = tk.Label(
            status_bar_frame, text="Ready", bg=styles.STATUS_BAR_BG, fg=styles.STATUS_BAR_FG,
            font=styles.STATUS_BAR_FONT, anchor=tk.W, justify=tk.LEFT, height=1)
        self.status_bar_label.pack(side=tk.LEFT, fill=tk.X, expand=True)

    def _update_status_bar(self, message: str, color: str = None):
        """Update the status bar with a message.

        Args:
            message: Status message to display
            color: Color for the message (uses default if None, green for success, red for error)
        """
        self.status_bar_label.config(text=message)
        if color:
            self.status_bar_label.config(fg=color)
        else:
            self.status_bar_label.config(fg=styles.STATUS_BAR_FG)
        self.root.update_idletasks()

    def _on_protect_click(self):
        """Handle protect button click."""
        data = self.protect_data_text.get("1.0", tk.END).strip()
        policy = self.protect_policy_var.get()

        if not data:
            self._update_status_bar("Please enter data to protect", styles.STATUS_BAR_ERROR_FG)
            return

        if not policy:
            self._update_status_bar("Please select a protection policy", styles.STATUS_BAR_ERROR_FG)
            return

        try:
            self._update_status_message(f"Protecting data with policy: {policy}")
            result = self.crdp_client.protect(data, policy)

            # Display result
            self.protect_result_text.config(state=tk.NORMAL)
            self.protect_result_text.delete("1.0", tk.END)

            if result:
                result_str = result.get("protected_data", "")
                self.protect_result_text.insert(tk.END, result_str)

            self.protect_result_text.config(state=tk.DISABLED)
            self._update_status_bar("Data protected successfully!", styles.STATUS_BAR_SUCCESS_FG)
            self._update_status_message("Data protection completed successfully")

        except Exception as e:
            logger.error(f"Protection failed: {str(e)}")
            self._update_status_bar(f"Protection failed: {str(e)}", styles.STATUS_BAR_ERROR_FG)
            self._update_status_message(f"Error: {str(e)}")

    def _on_reveal_click(self):
        """Handle reveal button click."""
        protected_data = self.reveal_data_text.get("1.0", tk.END).strip()
        policy = self.reveal_policy_var.get()
        username = self.reveal_username.get().strip()

        if not protected_data:
            self._update_status_bar("Please enter protected data to reveal", styles.STATUS_BAR_ERROR_FG)
            return

        if not policy:
            self._update_status_bar("Please select a protection policy", styles.STATUS_BAR_ERROR_FG)
            return

        if not username:
            self._update_status_bar("Username is required to reveal data", styles.STATUS_BAR_ERROR_FG)
            return

        try:
            self._update_status_message(f"Revealing data for user: {username}")
            result = self.crdp_client.reveal(protected_data, policy, username)

            # Display result
            self.reveal_result_text.config(state=tk.NORMAL)
            self.reveal_result_text.delete("1.0", tk.END)

            if result:
                self.reveal_result_text.insert(tk.END, result)

            self.reveal_result_text.config(state=tk.DISABLED)
            self._update_status_bar("Data revealed successfully!", styles.STATUS_BAR_SUCCESS_FG)
            self._update_status_message("Data revelation completed successfully")

        except Exception as e:
            logger.error(f"Reveal failed: {str(e)}")
            self._update_status_bar(f"Reveal failed: {str(e)}", styles.STATUS_BAR_ERROR_FG)
            self._update_status_message(f"Error: {str(e)}")

    def _copy_protected_data(self):
        """Copy protected data to clipboard."""
        self._copy_to_clipboard(self.protect_result_text)

    def _copy_revealed_data(self):
        """Copy revealed data to clipboard."""
        self._copy_to_clipboard(self.reveal_result_text)

    def _copy_to_clipboard(self, text_widget):
        """Copy text widget content to clipboard."""
        content = text_widget.get("1.0", tk.END).strip()
        if not content:
            self._update_status_bar("Nothing to copy", styles.STATUS_BAR_ERROR_FG)
            return

        self.root.clipboard_clear()
        self.root.clipboard_append(content)
        self._update_status_bar("✓ Data copied to clipboard!", styles.STATUS_BAR_SUCCESS_FG)

    def _on_metrics_click(self):
        """Handle metrics button click."""
        try:
            self._update_status_message("Fetching performance metrics...")
            result = self.crdp_client.metrics()

            # Display result
            self.metrics_text.config(state=tk.NORMAL)
            self.metrics_text.delete("1.0", tk.END)

            if result:
                self.metrics_text.insert(tk.END, result)

            self.metrics_text.config(state=tk.DISABLED)
            self._update_status_bar("Metrics retrieved successfully!", styles.STATUS_BAR_SUCCESS_FG)
            self._update_status_message("Performance metrics retrieved successfully")

        except Exception as e:
            logger.error(f"Metrics retrieval failed: {str(e)}")
            self._update_status_bar(f"Failed to retrieve metrics: {str(e)}", styles.STATUS_BAR_ERROR_FG)
            self._update_status_message(f"Error retrieving metrics: {str(e)}")

    def _on_liveness_click(self):
        """Handle liveness button click."""
        try:
            self._update_status_message("Checking liveness status...")
            result = self.crdp_client.liveness()

            # Display result
            self.liveness_text.config(state=tk.NORMAL)
            self.liveness_text.delete("1.0", tk.END)

            if result:
                result_str = json.dumps(result, indent=2)
                self.liveness_text.insert(tk.END, result_str)

            self.liveness_text.config(state=tk.DISABLED)
            self._update_status_bar("Liveness check completed successfully!", styles.STATUS_BAR_SUCCESS_FG)
            self._update_status_message("Liveness check completed successfully")

        except Exception as e:
            logger.error(f"Liveness check failed: {str(e)}")
            self._update_status_bar(f"Failed to check liveness: {str(e)}", styles.STATUS_BAR_ERROR_FG)
            self._update_status_message(f"Error checking liveness: {str(e)}")

    def _update_status(self):
        """Update status information."""
        crdp_url = self.config.get("crdp.url", "Not configured")

        # Check health status
        health_status = "Unknown"
        health_details = ""
        try:
            health_result = self.crdp_client.healthz().get("status", "Unknown")
            health_status = "Healthy"
            if health_result:
                health_details = f"\n  Details: {json.dumps(health_result, indent=4)}"
        except Exception as e:
            health_status = "Unhealthy"
            health_details = f"\n  Error: {str(e)}"

        status_info = f"""
=== CRDP Data Protection Status ===

CRDP Service Configuration:
  URL: {crdp_url}
  Timeout: {self.config.get("crdp.timeout", "N/A")} seconds
  SSL Verify: {self.config.get("crdp.ssl_verify", False)}

Health Status:
  {health_status}{health_details}

Available Policies:
  {', '.join(self.available_policies) if self.available_policies else "No policies loaded"}

Status:
  Application ready
  Ready to protect and reveal data using CRDP service
"""

        status_info += f"""
Application Features:
  • Protect Data: Encrypt sensitive information using CRDP policies
  • Reveal Data: Decrypt protected data with masking options
  • Clear Text: Display full decrypted data
  • Masked View: Display only last 4 characters for security
  • Performance Metrics: View service performance metrics
  • Liveness Check: Verify service liveness status

Usage:
  1. Go to 'Protect Data' tab to encrypt data
  2. Enter data and select policy
  3. Click 'Protect Data' to encrypt
  4. Go to 'Reveal Data' tab to decrypt
  5. Paste encrypted data and click 'Reveal Data'
  6. Go to 'Performance & Liveness' tab to view metrics and health

Configuration:
  - Edit config.json to change CRDP service URL
  - Restart application after modifying configuration
"""

        self.status_text.config(state=tk.NORMAL)
        self.status_text.delete("1.0", tk.END)
        self.status_text.insert(tk.END, status_info)
        self.status_text.config(state=tk.DISABLED)

    def _update_status_message(self, message: str):
        """Update status with a new message."""
        self.status_text.config(state=tk.NORMAL)
        current_text = self.status_text.get("1.0", tk.END)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        new_message = f"\n[{timestamp}] {message}"
        self.status_text.insert(tk.END, new_message)
        self.status_text.see(tk.END)
        self.status_text.config(state=tk.DISABLED)


def main():
    """Main entry point."""
    # Load configuration
    config = ConfigManager()

    root = tk.Tk()
    app = CRDPApplication(root, config)
    root.mainloop()


if __name__ == "__main__":
    main()
