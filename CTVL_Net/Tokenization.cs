using RestSharp;
using RestSharp.Authenticators;
using System.Net;
using System.Text.Json.Nodes;

/// <summary>
/// Application demonstrates Thales Vaultless Tokenization CT-VL
/// </summary>
/// <remarks>
/// The application has 3 tabs
/// 1. The first tab represents the application which receives the
/// clear data that the user has to enter in the text box and tokenizes it.
/// 2. The second tab represents the administrator who reads the data
/// with a mask (clear first 4 character and 4 last)
/// 3. The last tab represents the support employee who reads the data
/// with a mask (only clear last characters)
/// </remarks>
namespace CT_VL
{ 
    public partial class TokenizationApplication : Form
    {
        // Client used for application which receives the clear data and tokenize it.
        private RestClientOptions _appClient;
        // Client used for Admin who read the data with a mask (clear first 4 character and 4 last)
        private RestClientOptions _payableClient;
        // Client used for support who read the data with a mask (only clear last characters)
        private RestClientOptions _supportClient;
        
        /// <summary>
        /// Return token from tokenize operation 
        /// </summary>
        /// <returns>
        /// The token from tokenize operation 
        /// </returns>
        /// <param name="entryNode">
        /// [
	    ///   {
	    ///	    "token": "CC-1654N0.I~{0?JRJ4569",
	    ///	    "status": "Succeed"
	    ///   }
        /// ]
        /// </param>
        private String giveTokenFromJSON(String? entryNode)
        {
            if(String.IsNullOrEmpty(entryNode))
                return "";
            else
            {
                JsonNode ctvlNode = JsonNode.Parse(entryNode)!;
                JsonNode tokenNode = ctvlNode!["token"]!;
                return tokenNode.ToString();
            }
        }
        /// <summary>
        /// Return data from detokenize operation 
        /// </summary>
        /// <returns>
        /// The data from detokenize operation 
        /// </returns>
        /// <param name="entryNode">
        /// [
	    ///   {
	    ///     "data": "XXXXXXXXXXXXXXX4569",
	    ///     "status": "Succeed"
	    ///   }
        /// ]
        /// </param>
        private String giveDataFromJSON(String? entryNode)
        {
            if(String.IsNullOrEmpty(entryNode))
                return "";
            else
            {
                JsonNode ctvlNode = JsonNode.Parse(entryNode)!;
                JsonNode tokenNode = ctvlNode!["data"]!;
                return tokenNode.ToString();
            }
        }

        /// <summary>
        /// Initialize the application and create the payable and custoemr support clients.
        /// </summary>
        public TokenizationApplication()
        {
            InitializeComponent();

            ServicePointManager.SecurityProtocol = SecurityProtocolType.Tls12;

            _appClient = new RestClientOptions(AdminVariables.ct_url);
            _payableClient = new RestClientOptions(AdminVariables.ct_url);
            _supportClient = new RestClientOptions(AdminVariables.ct_url);
        }

        private void configButton_Click(object sender, EventArgs e)
        {
            String message = "Token Server: " + AdminVariables.ct_url.ToString() + Environment.NewLine
            + "Token Group: " + AdminVariables.tokengroupCC.ToString() + Environment.NewLine
            + "Token Template: " + AdminVariables.tokentemplateCC.ToString();
            MessageBox.Show(message);
        }

        private void loginButton_Click(object sender, EventArgs e)
        {
            int tabNumber = tabControl.SelectedIndex;
            if(String.IsNullOrEmpty(accountsIDs[tabNumber].Text) || String.IsNullOrEmpty(accountsPasswords[tabNumber].Text))
                return;

            // Ignore SSL Certificate verification error
            _appClient.RemoteCertificateValidationCallback = (sender, certificate, chain, sslPolicyErrors) => true;
            _payableClient.RemoteCertificateValidationCallback = (sender, certificate, chain, sslPolicyErrors) => true;
            _supportClient.RemoteCertificateValidationCallback = (sender, certificate, chain, sslPolicyErrors) => true;

            // User authentication
            var accountID = accountsIDs[tabNumber].Text;
            var accountPassword = accountsPasswords[tabNumber].Text;
            var request = new RestRequest("api/api-token-auth/", Method.Post);
            request.RequestFormat = DataFormat.Json;
            request.AddBody(new { username = accountID, password = accountPassword });
            RestClientOptions authClientOptions = new RestClientOptions(AdminVariables.ct_url);
            authClientOptions.RemoteCertificateValidationCallback = (sender, certificate, chain, sslPolicyErrors) => true;
            var authClient = new RestClient(authClientOptions);
            
            // Excecute the request synchronously
            var response = authClient.Execute(request);

            // Check is authentication was successful
            if (!response.IsSuccessful)
                return;

            // Enable Application tab after login
            if(tabNumber == 0)
            {
                _appClient.Authenticator = new HttpBasicAuthenticator(accountID, accountPassword);
                inputTextBox.ReadOnly = false;
                inputTextBox.BackColor = Color.Empty;
                tokenizeButton.Enabled = true;
            }
            // Enable Payable Account tab after login
            else if(tabNumber == 1)
            {
                _payableClient.Authenticator = new HttpBasicAuthenticator(accountID, accountPassword);  
                detokenizeButtonPayable.Enabled = true;
            }
            // Enable Support Account tab after login
            else
            {
                _supportClient.Authenticator = new HttpBasicAuthenticator(accountID, accountPassword);
                detokenizeButtonSupport.Enabled = true;
            }

            tokenizedText[tabNumber].Text = tokenizedText[0].Text;
        }

        /// <summary>
        /// Tokenize the data which was entered in the text box
        /// </summary>
        private void tokenizeButton_Click(object sender, EventArgs e)
        {
            if(inputTextBox.Text.ToString() == "")
                return;

            var request = new RestRequest("vts/rest/v2.0/tokenize", Method.Post);
            request.RequestFormat = DataFormat.Json;
            request.AddBody(new { tokengroup = AdminVariables.tokengroupCC, tokentemplate = AdminVariables.tokentemplateCC,
            data = inputTextBox.Text.ToString() });
            
            var client = new RestClient(_appClient);
            var response = client.Execute(request);
            var content = response.Content ?? String.Empty;

            try
            {
                if (response is not null && response.IsSuccessful && !content.Contains("error"))
                {
                    tokenizedText[0].Text = giveTokenFromJSON(response.Content);
                }
                else
                {
                    throw new Exception();
                }
            }
            catch (Exception exept)
            {
                throw new Exception(exept.ToString());
            }
        }

        /// <summary>
        /// Detokanize the data which was previously tokanized.
        /// If the button was clicked from the Payable tab, the detokanization operation uses the Payable client.
        /// If the button was clicked from the Support tab, the detokanization operation uses the Customer support client.
        /// </summary>
        private void detokenizeButton_Click(object sender, EventArgs e)
        {
            if(String.IsNullOrEmpty(tokenizedText[0].Text))
                return;

            var request = new RestRequest("vts/rest/v2.0/detokenize", Method.Post);
            request.RequestFormat = DataFormat.Json;
            request.AddBody(new { tokengroup = AdminVariables.tokengroupCC, tokentemplate = AdminVariables.tokentemplateCC,
            token = tokenizedText[0].Text });
            
            RestClientOptions options;
            Label text;
            // If the function has been triggered from the admin tab, use the admin client
            // Use the support client overwise.
            if(tabControl.SelectedIndex == 1)
            {
                options = _payableClient;
                text = detokenizedTextPayable;
            }
            else
            {
                options = _supportClient;
                text = detokenizedTextSupport;
            }

            RestClient client = new RestClient(options);
            var response = client.Execute(request);
            try
            {
                if (response.IsSuccessful)
                {
                    text.Text = giveDataFromJSON(response.Content);
                }
            }
            catch (Exception exept)
            {
                throw new Exception(exept.ToString());
            }
        }
    }
}