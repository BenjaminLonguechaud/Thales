# Vaultless Tokenization

Example application that levreage the Tokenization REST API to tokenize/detokenize an input Credit Card.

# About CTE for Kubernetes

Product Description:

[https://cpl.thalesgroup.com/encryption/tokenization](https://cpl.thalesgroup.com/encryption/tokenization)

More information can be found through Thales online documentation portal at:

[https://thalesdocs.com/ctp/con/ct-vl/latest/](https://thalesdocs.com/ctp/con/ct-vl/latest/)

# Quick installation guide
> **_NOTE:_**  Refer to the online docs for a detailed installation and configuration guide.

Install the virtual Tokenization Server using the OVA file which can be foudn on the Thales Support Portal.

Download this source code and make sure to change the *ct_url* variable in the var.cs file to match your Tokenization server IP address.
Make sure to also change the variables *tokengroupCC* and *tokentemplateCC* to match your Tokenization Group and Tokenization Template.
Open the project file CT-VL.csproj with Visual Studio, compile the project and lauch the application.
