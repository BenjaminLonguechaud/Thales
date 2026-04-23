#!/usr/bin/env python3
"""
CRDP Data Protection Application
A user-friendly GUI for protecting and revealing sensitive data using CipherTrust CRDP.
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import json
from datetime import datetime

from logger import logger
from config_manager import ConfigManager
from CRDP_client import CRDPClient

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
        window_width = config.get("ui.window_width", 800)
        window_height = config.get("ui.window_height", 700)

        self.root.title("CRDP Data Protection Manager")
        self.root.geometry(f"{window_width}x{window_height}")
        self.root.configure(bg='#f0f0f0')

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
        title_frame.pack(fill=tk.X, padx=20, pady=10)

        title_label = ttk.Label(title_frame, text="CRDP Data Protection Manager",
                               font=('Arial', 16, 'bold'))
        title_label.pack()

        subtitle = ttk.Label(title_frame, text="Secure data encryption and tokenization",
                            font=('Arial', 10), foreground='gray')
        subtitle.pack()

        # Create notebook (tabs)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Create tabs
        self._create_protect_tab()
        self._create_reveal_tab()
        self._create_status_tab()

    def _create_protect_tab(self):
        """Create the data protection tab."""
        protect_frame = ttk.Frame(self.notebook, padding=15)
        self.notebook.add(protect_frame, text="Protect Data")

        # Input fields
        ttk.Label(protect_frame, text="Data to Protect:", font=('Arial', 10, 'bold')).grid(
            row=0, column=0, columnspan=2, sticky=tk.W, pady=(0, 5))

        self.protect_data_text = scrolledtext.ScrolledText(
            protect_frame, height=6, width=60, wrap=tk.WORD, font=('Courier', 9))
        self.protect_data_text.grid(row=1, column=0, columnspan=2, sticky=tk.NSEW, pady=(0, 15))
        protect_frame.rowconfigure(1, weight=1)

        # Policy selection
        ttk.Label(protect_frame, text="Protection Policy:", font=('Arial', 9)).grid(
            row=2, column=0, sticky=tk.W, pady=(0, 5))
        self.protect_policy_var = tk.StringVar()
        self.protect_policy_combo = ttk.Combobox(
            protect_frame, textvariable=self.protect_policy_var, state='readonly', width=37)
        self.protect_policy_combo['values'] = self.available_policies
        if self.available_policies:
            self.protect_policy_combo.set(self.available_policies[0])
        self.protect_policy_combo.grid(row=2, column=1, sticky=tk.EW, pady=(0, 20))

        # Protect button
        protect_button = ttk.Button(
            protect_frame, text="Protect Data", command=self._on_protect_click)
        protect_button.grid(row=3, column=0, columnspan=2, sticky=tk.EW, pady=(0, 15))

        # Result frame
        ttk.Label(protect_frame, text="Protected Data (Cipher):", font=('Arial', 10, 'bold')).grid(
            row=4, column=0, columnspan=2, sticky=tk.W, pady=(0, 5))

        self.protect_result_text = scrolledtext.ScrolledText(
            protect_frame, height=6, width=60, wrap=tk.WORD, font=('Courier', 9),
            state=tk.DISABLED, bg='#f5f5f5')
        self.protect_result_text.grid(row=5, column=0, columnspan=2, sticky=tk.NSEW, pady=(0, 10))

        # Copy button
        copy_button = ttk.Button(
            protect_frame, text="Copy Protected Data", command=self._copy_protected_data)
        copy_button.grid(row=6, column=0, columnspan=2, sticky=tk.EW)

        protect_frame.columnconfigure(1, weight=1)
        protect_frame.rowconfigure(5, weight=1)

    def _create_reveal_tab(self):
        """Create the data revelation tab."""
        reveal_frame = ttk.Frame(self.notebook, padding=15)
        self.notebook.add(reveal_frame, text="Reveal Data")

        # Input fields
        ttk.Label(reveal_frame, text="Protected Data (Cipher):", font=('Arial', 10, 'bold')).grid(
            row=0, column=0, columnspan=2, sticky=tk.W, pady=(0, 5))

        self.reveal_data_text = scrolledtext.ScrolledText(
            reveal_frame, height=6, width=60, wrap=tk.WORD, font=('Courier', 9))
        self.reveal_data_text.grid(row=1, column=0, columnspan=2, sticky=tk.NSEW, pady=(0, 15))
        reveal_frame.rowconfigure(1, weight=1)

        # Protection Policy field
        ttk.Label(reveal_frame, text="Protection Policy:", font=('Arial', 9)).grid(
            row=2, column=0, sticky=tk.W, pady=(0, 5))
        self.reveal_policy_var = tk.StringVar()
        self.reveal_policy_combo = ttk.Combobox(
            reveal_frame, textvariable=self.reveal_policy_var, state='readonly', width=37)
        self.reveal_policy_combo['values'] = self.available_policies
        if self.available_policies:
            self.reveal_policy_combo.set(self.available_policies[0])
        self.reveal_policy_combo.grid(row=2, column=1, sticky=tk.EW, pady=(0, 15))

        # Username field (mandatory)
        ttk.Label(reveal_frame, text="Username (required):", font=('Arial', 9)).grid(
            row=3, column=0, sticky=tk.W, pady=(0, 5))
        self.reveal_username = ttk.Entry(reveal_frame, width=40)
        self.reveal_username.grid(row=3, column=1, sticky=tk.EW, pady=(0, 15))
        ttk.Label(reveal_frame, text="CipherTrust will determine how data is revealed based on this username",
                 font=('Arial', 8), foreground='gray').grid(row=4, column=0, columnspan=2, sticky=tk.W)

        # Reveal button
        reveal_button = ttk.Button(
            reveal_frame, text="Reveal Data", command=self._on_reveal_click)
        reveal_button.grid(row=5, column=0, columnspan=2, sticky=tk.EW, pady=(0, 15))

        # Result frame
        ttk.Label(reveal_frame, text="Revealed Data:", font=('Arial', 10, 'bold')).grid(
            row=6, column=0, columnspan=2, sticky=tk.W, pady=(0, 5))

        self.reveal_result_text = scrolledtext.ScrolledText(
            reveal_frame, height=6, width=60, wrap=tk.WORD, font=('Courier', 9),
            state=tk.DISABLED, bg='#f5f5f5')
        self.reveal_result_text.grid(row=7, column=0, columnspan=2, sticky=tk.NSEW, pady=(0, 10))

        # Copy button
        copy_button = ttk.Button(
            reveal_frame, text="Copy Revealed Data", command=self._copy_revealed_data)
        copy_button.grid(row=8, column=0, columnspan=2, sticky=tk.EW)

        reveal_frame.columnconfigure(1, weight=1)
        reveal_frame.rowconfigure(7, weight=1)

    def _create_status_tab(self):
        """Create the status/logs tab."""
        status_frame = ttk.Frame(self.notebook, padding=15)
        self.notebook.add(status_frame, text="Status & Info")

        # Info section
        ttk.Label(status_frame, text="Connection Status:", font=('Arial', 10, 'bold')).pack(
            anchor=tk.W, pady=(0, 5))

        self.status_text = tk.Text(status_frame, height=25, width=80, font=('Courier', 9),
                                  state=tk.DISABLED, bg='#f5f5f5')
        self.status_text.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

        # Refresh button
        refresh_button = ttk.Button(
            status_frame, text="Refresh Status", command=self._update_status)
        refresh_button.pack(anchor=tk.E)

        # Initial status update
        self._update_status()

    def _on_protect_click(self):
        """Handle protect button click."""
        data = self.protect_data_text.get("1.0", tk.END).strip()
        policy = self.protect_policy_var.get()

        if not data:
            messagebox.showwarning("Validation", "Please enter data to protect")
            return

        if not policy:
            messagebox.showwarning("Validation", "Please select a protection policy")
            return

        try:
            self._update_status_message(f"Protecting data with policy: {policy}")
            result = self.crdp_client.protect(data, policy)

            # Display result
            self.protect_result_text.config(state=tk.NORMAL)
            self.protect_result_text.delete("1.0", tk.END)

            if result:
                result_str = json.dumps(result, indent=2)
                self.protect_result_text.insert(tk.END, result_str)

            self.protect_result_text.config(state=tk.DISABLED)
            messagebox.showinfo("Success", "Data protected successfully!")
            self._update_status_message("Data protection completed successfully")

        except Exception as e:
            logger.error(f"Protection failed: {str(e)}")
            messagebox.showerror("Error", f"Failed to protect data:\n{str(e)}")
            self._update_status_message(f"Error: {str(e)}")

    def _on_reveal_click(self):
        """Handle reveal button click."""
        protected_data = self.reveal_data_text.get("1.0", tk.END).strip()
        policy = self.reveal_policy_var.get()
        username = self.reveal_username.get().strip()

        if not protected_data:
            messagebox.showwarning("Validation", "Please enter protected data to reveal")
            return

        if not policy:
            messagebox.showwarning("Validation", "Please select a protection policy")
            return

        if not username:
            messagebox.showwarning("Validation", "Username is required to reveal data")
            return

        try:
            self._update_status_message(f"Revealing data for user: {username}")
            result = self.crdp_client.unprotect(protected_data, policy, username)

            # Display result
            self.reveal_result_text.config(state=tk.NORMAL)
            self.reveal_result_text.delete("1.0", tk.END)

            if result:
                result_str = json.dumps(result, indent=2)
                self.reveal_result_text.insert(tk.END, result_str)

            self.reveal_result_text.config(state=tk.DISABLED)
            messagebox.showinfo("Success", "Data revealed successfully!")
            self._update_status_message("Data revelation completed successfully")

        except Exception as e:
            logger.error(f"Reveal failed: {str(e)}")
            messagebox.showerror("Error", f"Failed to reveal data:\n{str(e)}")
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
            messagebox.showwarning("Warning", "Nothing to copy")
            return

        self.root.clipboard_clear()
        self.root.clipboard_append(content)
        messagebox.showinfo("Success", "Data copied to clipboard!")

    def _update_status(self):
        """Update status information."""
        crdp_url = self.config.get("crdp.url", "Not configured")

        status_info = f"""
=== CRDP Data Protection Manager Status ===

CRDP Service Configuration:
  URL: {crdp_url}
  Timeout: {self.config.get("crdp.timeout", "N/A")} seconds
  SSL Verify: {self.config.get("crdp.ssl_verify", False)}

Available Policies:
  {', '.join(self.available_policies)}

Status:
  ✓ Application ready
  Ready to protect and reveal data using CRDP service
"""

        status_info += f"""
Application Features:
  • Protect Data: Encrypt sensitive information using CRDP policies
  • Reveal Data: Decrypt protected data with masking options
  • Clear Text: Display full decrypted data
  • Masked View: Display only last 4 characters for security

Usage:
  1. Go to 'Protect Data' tab to encrypt data
  2. Enter data, optional username, and select policy
  3. Click 'Protect Data' to encrypt
  4. Go to 'Reveal Data' tab to decrypt
  5. Paste encrypted data and click 'Reveal Data'
  6. Choose display format (clear or masked)

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
