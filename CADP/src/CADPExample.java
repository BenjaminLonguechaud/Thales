package CADP_Java.Demo;

import com.centralmanagement.CipherTextData;

import java.awt.GridLayout;

import javax.swing.JFrame;
import javax.swing.JPanel;
import javax.swing.JTextField;
import javax.swing.SwingUtilities;

import com.centralmanagement.CentralManagementProvider;
import com.centralmanagement.RegisterClientParameters;
import com.centralmanagement.policy.CryptoManager;

/**
 * Hello world!
 */
public class CADPExample extends JFrame {

	private CipherTextData _cipherTextDataObject;
	private String _protectionPolicy = "CADP_Protection";

    public static void main(String[] args) {

		// Create and show the application
        SwingUtilities.invokeLater(() -> {
            new CADPExample().setVisible(true);
        });
    }

    public CADPExample() {
        setTitle("Thales CADP with centralized connectors management");
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        setSize(510, 305);
        setLocationRelativeTo(null);

        JPanel panel = new JPanel(new GridLayout(4, 1, 5, 5));

		try {
			String keyManagerHost = System.getenv("CIPHERTRUST_IP");
			String registrationToken = System.getenv("REG_TOKEN");
			if (keyManagerHost == null || registrationToken == null) {
				throw new Exception("Please set the environment variables CIPHERTRUST_IP and REG_TOKEN");
			}

			// Creates RegisterClientParameters object - key manager default web port 443 is used
			RegisterClientParameters registerClientParams = new RegisterClientParameters.Builder(keyManagerHost,
					registrationToken.toCharArray()).build();

			System.out.println("App registered on Host " + registerClientParams.getKeyManagerHost() + " registered with token " + 
					new String(registerClientParams.getRegistrationToken()));

			// Creates CentralManagementProvider object
			CentralManagementProvider centralManagementProvider = new CentralManagementProvider(registerClientParams);

			// Register the Client
			centralManagementProvider.addProvider();
			System.out.println("CADP client registered successfully.");

			String clearText = "This is clear text";
			String encryptedText = Protect(clearText);
			String revealedTextRestrictedUser = Reveal(encryptedText, "restrictedUser");
			String revealedTextAuthorizedUser = Reveal(encryptedText, "authorizedUser");

			JTextField text1 = new JTextField("Clear text: \t\t\t" + clearText);
			panel.add(text1);
			JTextField text2 = new JTextField("Encrypted text: \t\t\t" + encryptedText);
			panel.add(text2);
			JTextField text3 = new JTextField("Revealed text for authorized user: \t" + revealedTextAuthorizedUser);
			panel.add(text3);
			JTextField text4 = new JTextField("Revealed text for restricted user: \t" + revealedTextRestrictedUser);
			panel.add(text4);
			getContentPane().add(panel);


		} catch (Exception e) {
			e.printStackTrace();
		}
    }

    public String Protect(String clearText) {
		String encryptedText = "";
		try {
			// protectionPolicy: Internal Protection Policy
			_cipherTextDataObject = CryptoManager.protect(clearText.getBytes(), _protectionPolicy);

			encryptedText = new String(_cipherTextDataObject.getCipherText());
			System.out.println("Protected Data: " + encryptedText);

		} catch (Exception e) {
			e.printStackTrace();
		}
		return encryptedText;
	}

    public String Reveal(String encryptedText, String user) {
		String clearText = "";
		try {
			// protectionPolicy: Internal Protection Policy
			// _cipherTextDataObject: Object of CipherTextData which holds the response of protect API.
			// userName: Name of the user for whom data will be revealed. The reveal format depends on the access policy.
			clearText = new String(CryptoManager.reveal(_cipherTextDataObject, _protectionPolicy, user));

			System.out.println("Clear Data: " + clearText);

        } catch (Exception e) {
            e.printStackTrace();
        }
        return clearText;
    }
}
