using RestSharp;
using RestSharp.Authenticators;
using System.Security.Cryptography.X509Certificates;
using System.Net.Security;
using System.Net;

namespace CT_VL
{
    partial class TokenizationApplication
    {
        /// <summary>
        ///  Required designer variable.
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        ///  Clean up any resources being used.
        /// </summary>
        /// <param name="disposing">true if managed resources should be disposed; otherwise, false.</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Windows Form Designer generated code

        /// <summary>
        ///  Required method for Designer support - do not modify
        ///  the contents of this method with the code editor.
        /// </summary>
        private void InitializeComponent()
        {
            this.parameters = new System.Windows.Forms.Button();
            this.inputTextBox = new System.Windows.Forms.TextBox();
            this.tokenizeButton = new System.Windows.Forms.Button();
            this.detokenizeButtonPayable = new System.Windows.Forms.Button();
            this.detokenizeButtonSupport = new System.Windows.Forms.Button();
            this.tokenizedText = new List<System.Windows.Forms.Label>();
            this.detokenizedTextPayable = new System.Windows.Forms.Label();
            this.detokenizedTextSupport = new System.Windows.Forms.Label();
            this.tabControl = new System.Windows.Forms.TabControl();
            this.applicationPage = new System.Windows.Forms.TabPage("Application");
            this.payablePage = new System.Windows.Forms.TabPage("Payable");            
            this.supportPage = new System.Windows.Forms.TabPage("Support");
            this.thalesLogo = new List<System.Windows.Forms.PictureBox>();
            this.accountsIDs = new List<System.Windows.Forms.TextBox>();
            this.accountsPasswords = new List<System.Windows.Forms.TextBox>();
            this.loginButtons = new List<System.Windows.Forms.Button>();
            this.SuspendLayout();

            // Configuration menu displaying information written in var.cs
            this.parameters.Text = "Configuration";
            this.parameters.Location = new System.Drawing.Point(2, 2);
            this.parameters.Size = new System.Drawing.Size(80, 20);
            this.parameters.Click += new System.EventHandler(this.configButton_Click);

            for(int i = 0; i < 3; i++)
            {
                System.Windows.Forms.TextBox account = new System.Windows.Forms.TextBox();
                account.Location = new System.Drawing.Point(50, 50);
                account.Size = new System.Drawing.Size(100, 35);
                account.ScrollBars = System.Windows.Forms.ScrollBars.Vertical;
                account.PlaceholderText = "Account ID";
                this.accountsIDs.Add(account);
            
                System.Windows.Forms.TextBox password = new System.Windows.Forms.TextBox();
                password.Location = new System.Drawing.Point(170, 50);
                password.Size = new System.Drawing.Size(100, 35);
                password.ScrollBars = System.Windows.Forms.ScrollBars.Vertical;
                password.PlaceholderText = "Password";
                password.PasswordChar = '*';
                this.accountsPasswords.Add(password);

                System.Windows.Forms.Button loginButton = new System.Windows.Forms.Button();
                loginButton.Location = new System.Drawing.Point(300, 50);
                loginButton.Name = "loginButton";
                loginButton.Size = new System.Drawing.Size(50, 20);
                loginButton.TabIndex = 0;
                loginButton.Text = "Login";
                loginButton.UseVisualStyleBackColor = true;
                loginButton.Click += new System.EventHandler(this.loginButton_Click);

                this.loginButtons.Add(loginButton);
            }

            this.inputTextBox.Location = new System.Drawing.Point(50, 100);
            this.inputTextBox.Size = new System.Drawing.Size(100, 35);
            this.inputTextBox.ScrollBars = System.Windows.Forms.ScrollBars.Vertical;
            this.inputTextBox.ReadOnly = true;
            this.inputTextBox.BackColor = Color.Gray;
 
            this.tokenizeButton.Location = new System.Drawing.Point(170, 100);
            this.tokenizeButton.Name = "tokenizeButton";
            this.tokenizeButton.Size = new System.Drawing.Size(70, 20);
            this.tokenizeButton.TabIndex = 0;
            this.tokenizeButton.Text = "Tokenize";
            this.tokenizeButton.Enabled = false;
            this.tokenizeButton.UseVisualStyleBackColor = true;
            this.tokenizeButton.Click += new System.EventHandler(this.tokenizeButton_Click);

            this.detokenizeButtonPayable.Location = new System.Drawing.Point(50, 120);
            this.detokenizeButtonPayable.Name = "detokenizeButtonPayable";
            this.detokenizeButtonPayable.Size = new System.Drawing.Size(105, 35);
            this.detokenizeButtonPayable.TabIndex = 1;
            this.detokenizeButtonPayable.Text = "Detokenize";
            this.detokenizeButtonPayable.Enabled = false;
            this.detokenizeButtonPayable.UseVisualStyleBackColor = true;
            this.detokenizeButtonPayable.Click += new System.EventHandler(this.detokenizeButton_Click);
 
            this.detokenizeButtonSupport.Location = new System.Drawing.Point(50, 120);
            this.detokenizeButtonSupport.Name = "detokenizeButtonSupport";
            this.detokenizeButtonSupport.Size = new System.Drawing.Size(105, 35);
            this.detokenizeButtonSupport.TabIndex = 1;
            this.detokenizeButtonSupport.Text = "Detokenize";
            this.detokenizeButtonSupport.Enabled = false;
            this.detokenizeButtonSupport.UseVisualStyleBackColor = true;
            this.detokenizeButtonSupport.Click += new System.EventHandler(this.detokenizeButton_Click);

            this.detokenizedTextPayable.Location = new System.Drawing.Point(200, 130);
            this.detokenizedTextPayable.Size = new System.Drawing.Size(105, 100);
            this.detokenizedTextPayable.AutoSize = true;
            this.detokenizedTextPayable.TabIndex = 1;

            this.detokenizedTextSupport.Location = new System.Drawing.Point(200, 130);
            this.detokenizedTextSupport.Size = new System.Drawing.Size(105, 100);
            this.detokenizedTextSupport.AutoSize = true;
            this.detokenizedTextSupport.TabIndex = 1;

            for(int i = 0; i < 3; i++)
            {
                System.Windows.Forms.Label label = new System.Windows.Forms.Label();
                if(i == 0)
                    label.Location = new System.Drawing.Point(50, 140);
                else
                    label.Location = new System.Drawing.Point(50, 100);
                label.Size = new System.Drawing.Size(105, 100);
                label.AutoSize = true;
                label.TabIndex = 1;
                this.tokenizedText.Add(label);

                System.Windows.Forms.PictureBox logo = new System.Windows.Forms.PictureBox();
                logo.Location = new System.Drawing.Point(270, 200);
                logo.Size = new System.Drawing.Size(150, 50);
                logo.Image = Image.FromFile("resources/ThalesLogo.png");
                thalesLogo.Add(logo);
            }

            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 13F);
            this.components = new System.ComponentModel.Container();
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(400, 250);
            this.tabControl.Size = new System.Drawing.Size(400, 250);
            this.Controls.Add(this.tabControl);
            this.tabControl.Controls.Add(applicationPage);
            this.tabControl.Controls.Add(payablePage);
            this.tabControl.Controls.Add(supportPage);

            this.applicationPage.Controls.Add(this.parameters);
            this.applicationPage.Controls.Add(this.inputTextBox);
            this.applicationPage.Controls.Add(this.tokenizeButton);  
            for(int i = 0; i < 3; i++)
            {
                this.tabControl.Controls[i].Controls.Add(this.accountsIDs[i]);
                this.tabControl.Controls[i].Controls.Add(this.accountsPasswords[i]);
                this.tabControl.Controls[i].Controls.Add(this.loginButtons[i]);

                this.tabControl.Controls[i].Controls.Add(this.thalesLogo[i]);
                this.tabControl.Controls[i].Controls.Add(this.tokenizedText[i]);
            }
            this.payablePage.Controls.Add(this.detokenizeButtonPayable);
            this.payablePage.Controls.Add(this.detokenizedTextPayable);
            this.supportPage.Controls.Add(this.detokenizeButtonSupport);
            this.supportPage.Controls.Add(this.detokenizedTextSupport);

            this.Text = "Tokenization with CT-VL";

            this.ResumeLayout(false);
        }

        #endregion

        /// <summary>
        /// Pop-up window to display tokenization server parameters
        /// </summary>
        private System.Windows.Forms.Button parameters;

        /// <summary>
        /// List of the 3 login IDs.
        /// </summary>
        private List<System.Windows.Forms.TextBox> accountsIDs;
        /// <summary>
        /// List of the 3 login passwords.
        /// </summary>
        private List<System.Windows.Forms.TextBox> accountsPasswords;
        /// <summary>
        /// Text to display when login is successful.
        /// </summary>
        private List<System.Windows.Forms.Button> loginButtons;
        /// <summary>
        /// Control all account tabs.
        /// </summary>
        private System.Windows.Forms.TabControl tabControl;
        /// <summary>
        ///  Entry for the user to set the CC number to be tokenized.
        /// </summary>
        private System.Windows.Forms.TextBox inputTextBox;
        /// <summary>
        /// Button to launch the tokenization of the information set in inputTextBox.
        /// </summary>
        private System.Windows.Forms.Button tokenizeButton;
        /// <summary>
        /// Display the tokenized text, result of the process launched by tokenizeButton.
        /// </summary>
        private List<System.Windows.Forms.Label> tokenizedText;
        /// <summary>
        /// Launch the detokenization process of tokenizedText as the Payable account.
        /// </summary>
        private System.Windows.Forms.Button detokenizeButtonPayable;
        /// <summary>
        /// Launch the detokenization process of tokenizedText as the Support account.
        /// </summary>
        private System.Windows.Forms.Button detokenizeButtonSupport;
        /// <summary>
        /// Display the detokenized text, result of the process launched by tokenizeButton with
        /// Data Masking set for the payable account.
        /// </summary>
        private System.Windows.Forms.Label detokenizedTextPayable;
        /// <summary>
        /// Display the detokenized text, result of the process launched by tokenizeButton with
        /// Data Masking set for the support account.
        /// </summary>
        private System.Windows.Forms.Label detokenizedTextSupport;
        /// <summary>
        /// First tab: The application set the CC number to be tokenized.
        /// </summary>
        private System.Windows.Forms.TabPage applicationPage;
        /// <summary>
        /// Second tab: The payable user can login and detokenized the data.
        /// </summary>
        private System.Windows.Forms.TabPage payablePage;
        /// <summary>
        /// Third tab: The support user can login and detokenized the data.
        /// </summary>
        private System.Windows.Forms.TabPage supportPage;
        /// <summary>
        /// Thales logo to be displayed on all tabs.
        /// </summary>
        private List<System.Windows.Forms.PictureBox> thalesLogo;
    }
}