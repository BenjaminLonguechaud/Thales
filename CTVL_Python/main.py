import tkinter as tk
from PIL import Image, ImageTk
from tkinter import ttk, messagebox, Menu
import requests
import json
import urllib3
import os

# Suppress only the single InsecureRequestWarning from urllib3 needed for unverified HTTPS requests.
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

CIPHERTRUST_IP = os.environ.get("CIPHERTRUST_IP")

# Configuration Variables
class AdminVariables:
    ct_url = CIPHERTRUST_IP
# For tokenadmin
    tokengroupCC = "tokenization_group"  
    tokentemplateCC = "token_template"

# For support user
    tokengroupSupport = "tokenization_group_0-4"  
    tokentemplateSupport = "token_template_0-4"


# Helper Functions
def give_token_from_json(entry_node):
    if not entry_node:
        return ""
    try:
        ctvl_node = json.loads(entry_node)
        return ctvl_node["token"]
    except (json.JSONDecodeError, KeyError) as e:
        print(f"Error in give_token_from_json: {e}")
        return ""


def give_data_from_json(entry_node):
    if not entry_node:
        return ""
    try:
        ctvl_node = json.loads(entry_node)
        print(f"Parsed JSON: {ctvl_node}")
        return ctvl_node.get("data", "")
    except (json.JSONDecodeError, KeyError) as e:
        print(f"Error in give_data_from_json: {e}")
        return ""


class TokenizationApplication(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Tokenization with CT-VL")
        self.geometry("600x400")
        self.session = requests.Session()
        self.auth_token = None

        # Menu
        menu = Menu(self)
        self.config(menu=menu)
        settings_menu = Menu(menu, tearoff=0)
        menu.add_cascade(label="Settings", menu=settings_menu)
        settings_menu.add_command(label="Set CT-VL URL", command=self.set_url)

        # Tabs
        self.tab_control = ttk.Notebook(self)
        self.application_tab = ttk.Frame(self.tab_control)
        self.payable_tab = ttk.Frame(self.tab_control)
        self.support_tab = ttk.Frame(self.tab_control)

        self.tab_control.add(self.application_tab, text='Application')
        self.tab_control.add(self.payable_tab, text='Payable')
        self.tab_control.add(self.support_tab, text='Support')
        self.tab_control.pack(expand=1, fill='both')

        self.create_application_tab()
        self.create_payable_tab()
        self.create_support_tab()

        self.add_logo(self.application_tab)
        self.add_logo(self.payable_tab)
        self.add_logo(self.support_tab)

    def set_url(self):
        url_window = tk.Toplevel(self)
        url_window.title("Set CT-VL URL")
        url_label = tk.Label(url_window, text="CT-VL URL:")
        url_label.grid(row=0, column=0, padx=10, pady=10)
        self.url_entry = tk.Entry(url_window, width=50)
        self.url_entry.grid(row=0, column=1, padx=10, pady=10)
        self.url_entry.insert(0, AdminVariables.ct_url)
        save_button = tk.Button(url_window, text="Save", command=self.save_url)
        save_button.grid(row=1, column=0, columnspan=2, pady=10)

    def save_url(self):
        AdminVariables.ct_url = self.url_entry.get()
        messagebox.showinfo("URL Saved", f"CT-VL URL set to: {AdminVariables.ct_url}")

    def create_application_tab(self):
        row_counter = 0

        tk.Label(self.application_tab, text="Username:").grid(row=row_counter, column=0, padx=10, pady=5, sticky='e')
        self.accountID_app = tk.Entry(self.application_tab)
        self.accountID_app.grid(row=row_counter, column=1, padx=10, pady=5, sticky='w')

        row_counter += 1
        tk.Label(self.application_tab, text="Password:").grid(row=row_counter, column=0, padx=10, pady=5, sticky='e')
        self.password_app = tk.Entry(self.application_tab, show='*')
        self.password_app.grid(row=row_counter, column=1, padx=10, pady=5, sticky='w')

        row_counter += 1
        self.loginButton_app = tk.Button(self.application_tab, text="Login", command=lambda: self.login(0))
        self.loginButton_app.grid(row=row_counter, column=1, padx=10, pady=5, sticky='w')

        row_counter += 1
        tk.Label(self.application_tab, text="Credit Card Number:").grid(row=row_counter, column=0, padx=10, pady=5,
                                                                        sticky='e')
        self.inputTextBox = tk.Entry(self.application_tab)
        self.inputTextBox.grid(row=row_counter, column=1, padx=10, pady=5, sticky='w')

        row_counter += 1
        self.tokenizeButton = tk.Button(self.application_tab, text="Tokenize", command=self.tokenize)
        self.tokenizeButton.grid(row=row_counter, column=1, padx=10, pady=5, sticky='w')
        self.tokenizeButton.config(state=tk.DISABLED)

        row_counter += 1
        self.resultLabel_app = tk.Label(self.application_tab, text="Result: ", anchor='w')
        self.resultLabel_app.grid(row=row_counter, column=0, columnspan=2, pady=10, sticky=tk.W)

    def create_payable_tab(self):
        row_counter = 0

        tk.Label(self.payable_tab, text="Username:").grid(row=row_counter, column=0, padx=10, pady=5, sticky='e')
        self.accountID_payable = tk.Entry(self.payable_tab)
        self.accountID_payable.grid(row=row_counter, column=1, padx=10, pady=5, sticky='w')

        row_counter += 1
        tk.Label(self.payable_tab, text="Password:").grid(row=row_counter, column=0, padx=10, pady=5, sticky='e')
        self.password_payable = tk.Entry(self.payable_tab, show='*')
        self.password_payable.grid(row=row_counter, column=1, padx=10, pady=5, sticky='w')

        row_counter += 1
        self.loginButton_payable = tk.Button(self.payable_tab, text="Login", command=lambda: self.login(1))
        self.loginButton_payable.grid(row=row_counter, column=1, padx=10, pady=5, sticky='w')

        row_counter += 1
        tk.Label(self.payable_tab, text="Tokenized Data:").grid(row=row_counter, column=0, padx=10, pady=5, sticky='e')
        self.tokenizedData_payable = tk.Entry(self.payable_tab)
        self.tokenizedData_payable.grid(row=row_counter, column=1, padx=10, pady=5, sticky='w')

        row_counter += 1
        self.detokenizeButtonPayable = tk.Button(self.payable_tab, text="Detokenize",
                                                 command=lambda: self.detokenize(1))
        self.detokenizeButtonPayable.grid(row=row_counter, column=1, padx=10, pady=5, sticky='w')
        self.detokenizeButtonPayable.config(state=tk.DISABLED)

        row_counter += 1
        self.detokenizedTextPayable = tk.Label(self.payable_tab, text="")
        self.detokenizedTextPayable.grid(row=row_counter, column=0, columnspan=2, pady=10)

        row_counter += 1
        self.resultLabel_payable = tk.Label(self.payable_tab, text="Result: ", anchor='w')
        self.resultLabel_payable.grid(row=row_counter, column=0, columnspan=2, pady=10, sticky=tk.W)

    def create_support_tab(self):
        row_counter = 0

        tk.Label(self.support_tab, text="Username:").grid(row=row_counter, column=0, padx=10, pady=5, sticky='e')
        self.accountID_support = tk.Entry(self.support_tab)
        self.accountID_support.grid(row=row_counter, column=1, padx=10, pady=5, sticky='w')

        row_counter += 1
        tk.Label(self.support_tab, text="Password:").grid(row=row_counter, column=0, padx=10, pady=5, sticky='e')
        self.password_support = tk.Entry(self.support_tab, show='*')
        self.password_support.grid(row=row_counter, column=1, padx=10, pady=5, sticky='w')

        row_counter += 1
        self.loginButton_support = tk.Button(self.support_tab, text="Login", command=lambda: self.login(2))
        self.loginButton_support.grid(row=row_counter, column=1, padx=10, pady=5, sticky='w')

        row_counter += 1
        tk.Label(self.support_tab, text="Tokenized Data:").grid(row=row_counter, column=0, padx=10, pady=5, sticky='e')
        self.tokenizedData_support = tk.Entry(self.support_tab)
        self.tokenizedData_support.grid(row=row_counter, column=1, padx=10, pady=5, sticky='w')

        row_counter += 1
        self.detokenizeButtonSupport = tk.Button(self.support_tab, text="Detokenize",
                                                 command=lambda: self.detokenize(2))
        self.detokenizeButtonSupport.grid(row=row_counter, column=1, padx=10, pady=5, sticky='w')
        self.detokenizeButtonSupport.config(state=tk.DISABLED)

        row_counter += 1
        self.detokenizedTextSupport = tk.Label(self.support_tab, text="")
        self.detokenizedTextSupport.grid(row=row_counter, column=0, columnspan=2, pady=10)

        row_counter += 1
        self.resultLabel_support = tk.Label(self.support_tab, text="Result: ", anchor='w')
        self.resultLabel_support.grid(row=row_counter, column=0, columnspan=2, pady=10, sticky=tk.W)

    def add_logo(self, tab):
        try:
            image = Image.open("Thaleslogo.jpg")
            image = image.resize((200, 100), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(image)
            logo_label = tk.Label(tab, image=photo)
            logo_label.image = photo  # Keep a reference to the image
            logo_label.place(relx=1.0, rely=1.0, anchor='se')
        except Exception as e:
            print(f"Error loading logo: {e}")

    def login(self, tab_number):
        if tab_number == 0:
            account_id = self.accountID_app.get()
            account_password = self.password_app.get()
        elif tab_number == 1:
            account_id = self.accountID_payable.get()
            account_password = self.password_payable.get()
        else:
            account_id = self.accountID_support.get()
            account_password = self.password_support.get()

        if not account_id or not account_password:
            messagebox.showerror("Error", "Please enter both username and password.")
            return

        url = f"{AdminVariables.ct_url}/api/api-token-auth/"
        payload = {
            "username": account_id,
            "password": account_password
        }
        headers = {
            "Content-Type": "application/json"
        }

        response = self.session.post(url, json=payload, headers=headers, verify=False)

        if response.status_code == 200:
            self.auth_token = response.json().get("token")
            print("Login successful")
            print(response.json())
            if tab_number == 0:
                self.tokenizeButton.config(state=tk.NORMAL)
                self.resultLabel_app.config(text="Login successful")
            elif tab_number == 1:
                self.detokenizeButtonPayable.config(state=tk.NORMAL)
                self.resultLabel_payable.config(text="Login successful")
            else:
                self.detokenizeButtonSupport.config(state=tk.NORMAL)
                self.resultLabel_support.config(text="Login successful")
        else:
            messagebox.showerror("Error", f"Login failed: {response.text}")

    def tokenize(self):
        data = self.inputTextBox.get()
        if not data:
            return

        url = f"{AdminVariables.ct_url}/vts/rest/v2.0/tokenize"
        payload = {
            "tokengroup": AdminVariables.tokengroupCC,
            "tokentemplate": AdminVariables.tokentemplateCC,
            "data": data
        }
        headers = {
            "Authorization": f"Bearer {self.auth_token}"
        }

        response = self.session.post(url, json=payload, headers=headers, verify=False)

        if response.status_code == 200:
            token = give_token_from_json(response.text)
            print(f"Tokenized Data: {token}")
            self.resultLabel_app.config(text=f"Result: {token}")
            self.tokenizedData_payable.delete(0, tk.END)
            self.tokenizedData_payable.insert(0, token)
            self.tokenizedData_support.delete(0, tk.END)
            self.tokenizedData_support.insert(0, token)
        else:
            messagebox.showerror("Error", f"Tokenization failed: {response.text}")

    def tokenize_support(self):
        data = self.inputTextBox.get()
        if not data:
            return

        url = f"{AdminVariables.ct_url}/vts/rest/v2.0/tokenize"
        payload = {
            "tokengroup": AdminVariables.tokengroupSupport,
            "tokentemplate": AdminVariables.tokentemplateSupport,
            "data": data
        }
        headers = {
            "Authorization": f"Bearer {self.auth_token}"
        }

        response = self.session.post(url, json=payload, headers=headers, verify=False)

        if response.status_code == 200:
            token = give_token_from_json(response.text)
            print(f"Tokenized Data: {token}")
            self.resultLabel_app.config(text=f"Result: {token}")
            self.tokenizedData_payable.delete(0, tk.END)
            self.tokenizedData_payable.insert(0, token)
            self.tokenizedData_support.delete(0, tk.END)
            self.tokenizedData_support.insert(0, token)
        else:
            messagebox.showerror("Error", f"Tokenization failed: {response.text}")

    def detokenize(self, tab_number):
        if tab_number == 1:
            token = self.tokenizedData_payable.get()
        else:
            token = self.tokenizedData_support.get()

        if not token:
            return

        url = f"{AdminVariables.ct_url}/vts/rest/v2.0/detokenize"
        payload = {
            "tokengroup": AdminVariables.tokengroupCC,
            "tokentemplate": AdminVariables.tokentemplateCC,
            "token": token
        }
        headers = {
            "Authorization": f"Bearer {self.auth_token}"
        }

        response = self.session.post(url, json=payload, headers=headers, verify=False)

        if response.status_code == 200:
            detokenized_data = give_data_from_json(response.text)
            if tab_number == 1:
                self.detokenizedTextPayable.config(text=detokenized_data)
                self.resultLabel_payable.config(text=f"Result: {detokenized_data}")
            else:
                masked_data = "CC-" + "X" * (len(detokenized_data) - 4) + detokenized_data[-4:]
                self.detokenizedTextSupport.config(text=masked_data)
                self.resultLabel_support.config(text=f"Result: {masked_data}")
        else:
            messagebox.showerror("Error", f"Detokenization failed: {response.text}")

    def detokenize_support(self):
        token = self.tokenizedData_support.get()
        if not token:
            return

        url = f"{AdminVariables.ct_url}/vts/rest/v2.0/detokenize"
        payload = {
            "tokengroup": AdminVariables.tokengroupSupport,
            "tokentemplate": AdminVariables.tokentemplateSupport,
            "token": token
        }
        headers = {
            "Authorization": f"Bearer {self.auth_token}"
        }

        response = self.session.post(url, json=payload, headers=headers, verify=False)

        if response.status_code == 200:
            detokenized_data = give_data_from_json(response.text)
            masked_data = "CC-" + "X" * (len(detokenized_data) - 4) + detokenized_data[-4:]
            self.detokenizedTextSupport.config(text=masked_data)
            self.resultLabel_support.config(text=f"Result: {masked_data}")
        else:
            messagebox.showerror("Error", f"Detokenization failed: {response.text}")


if __name__ == "__main__":
    app = TokenizationApplication()
    app.mainloop()