package com.thales.cts.samples;
import javax.swing.*;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
public class TokenizationExample extends JFrame {
    /**
     * Generated to prevent warning "The serializable class GUI
     * does not declare a static final serialVersionUID"
     */
    private static final long serialVersionUID = 1L;
    private JLabel _token;
    private JLabel _clearValuePayable;
    private JLabel _clearValueSupport;
    private TokenServer _tokenServer;
    private JTextField _tokenFieldPayable;
    private JTextField _tokenFieldSupport;
    public TokenizationExample() {
        setTitle("Thales Tokenization Server");
        setIconImage(Toolkit.getDefaultToolkit().getImage(getClass().getResource("/thales.png")));
        _tokenServer = new TokenServer();
        _clearValuePayable = new JLabel();
        _clearValueSupport = new JLabel();
        _token = new JLabel();
        _tokenFieldPayable = new JTextField();
        _tokenFieldSupport = new JTextField();
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        // Create tab pane to separate the 3 accounts
        JTabbedPane tabbedPane = new JTabbedPane();
        // Add the "Application" tab
        tabbedPane.addTab("Application", createAppPanel());
        tabbedPane.addTab("Payable", createPayablePanel());
        tabbedPane.addTab("Support", createSupportPanel());
        // Add the tabbedPane to the frame
        getContentPane().add(tabbedPane);
        setSize(510, 305);
        setLocationRelativeTo(null);
    }
    /**
     * Popup configuration windows
     * - Tokenization server URL
     * - Tokenization Group
     * - Tokenization Template
     * @return the button allowing the user to open the configuration popup.
     */
    private JButton createconfigButton() {
        // Popup which open when the Configuration button is pressed.
        JFrame frame = new JFrame("Configuration");
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        frame.setSize(300, 200);
        
    	// Create the Configuration button
        JButton configButton = new JButton("Configuration");
        // Add action listener to the button
        configButton.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                // Create the message to display in the popup
                String message = "Tokenization server: " + Var.ct_url + "\n" + 
                "Token Group: " + Var.tokengroupCC + "\n" + 
                "Token Template: " + Var.tokentemplateCC;
                
                // Show the popup
                JOptionPane.showMessageDialog(frame, message, "Configuration", JOptionPane.INFORMATION_MESSAGE);
            }
        });
        return configButton;
    }
    
    /**
     * Create the "Application" tab.
     * Includes a first line of two text filed to allow the user
     * to enter its credentials. The second line has a text field which
     * requires a SSN format (XXX-XX-XXXX ) and a Tokenization button.
     * The result of the Tokenization operation is displayed to the right
     * of the button.
     * 
     * @return The application account panel
     */
    private JPanel createAppPanel() {
    	JPanel appPanel = new JPanel(new BorderLayout());
    	
    	// Create a panel for top space
        JPanel topSpacePanel = new JPanel();
        topSpacePanel.setPreferredSize(new Dimension(0, 20));
        appPanel.add(topSpacePanel, BorderLayout.NORTH);

        JPanel topPanel = new JPanel(new FlowLayout(FlowLayout.LEFT));
        topPanel.add(createconfigButton());
        appPanel.add(topPanel, BorderLayout.NORTH);

        // Create the middle panel with text fields and buttons
        JPanel appLayout = new JPanel(new GridLayout(2, 3, 5, 70));

        // First line
        MyTextField login = new MyTextField("Login");        
        JPasswordField password = new JPasswordField("Password");
        password.setText("");

        appLayout.add(login);
        appLayout.add(password);
        appLayout.add(new JLabel(""));

        // Second line
        MyTextField ssn = new MyTextField("SSN");
        JButton tokenizeButton = new JButton("Tokenize");
        tokenizeButton.addActionListener(new ActionListener() {
			@Override
			public void actionPerformed(ActionEvent e) {
				String result = _tokenServer.Tokenize(Var.ct_url, login.getText(), new String(password.getPassword()), ssn.getText());
				_token.setText(result);
				_tokenFieldPayable.setText(result);
				_tokenFieldSupport.setText(result);
			}
		});
        
        
        appLayout.add(ssn);
        appLayout.add(tokenizeButton);
        // Empty cell to fill the grid layout
        appLayout.add(_token);

        // Add the middle panel to the center of the appPanel
        appPanel.add(appLayout, BorderLayout.CENTER);

        // Create a panel for bottom space
        JPanel bottomSpacePanel = new JPanel();
        bottomSpacePanel.setPreferredSize(new Dimension(0, 50));
        appPanel.add(bottomSpacePanel, BorderLayout.SOUTH);
	    
	    return appPanel;
    }
    
    /**
     * Create the "Payable" tab.
     * Includes a first line of two text filed to allow the user
     * to enter its credentials. The second line has a text field which
     * was automatically filled by the Tokenization operation and a Detokenization
     * button. The result of the Detokenization operation is displayed
     * to the right of the button.
     * Being the Payable account, the user reads data in clear.
     * 
     * @return The payable account panel
     */
    private JPanel createPayablePanel() {
	    JPanel payablePanel = new JPanel(new BorderLayout());
	    
	    // Create a panel for top space
        JPanel topSpacePanel = new JPanel();
        topSpacePanel.setPreferredSize(new Dimension(0, 20));
        payablePanel.add(topSpacePanel, BorderLayout.NORTH);

        // Create the middle panel with text fields and buttons
        JPanel payableLayout = new JPanel(new GridLayout(2, 3, 5, 90));

        // First line
        JTextField login = new JTextField(10);
        JPasswordField password = new JPasswordField(10);
        password.setText("");
        
        payableLayout.add(login);
        payableLayout.add(password);
        payableLayout.add(new JLabel(""));

        // Second line
        JButton detokenizeButton = new JButton("Detokenize");
        detokenizeButton.addActionListener(new ActionListener() {
			@Override
			public void actionPerformed(ActionEvent e) {
				_clearValuePayable.setText(_tokenServer.Detokenize(Var.ct_url, login.getText(), new String(password.getPassword()), _tokenFieldPayable.getText()));
			}
		});
        
        payableLayout.add(_tokenFieldPayable);
        payableLayout.add(detokenizeButton);
        payableLayout.add(_clearValuePayable);

        // Add the middle panel to the center of the appPanel
        payablePanel.add(payableLayout, BorderLayout.CENTER);

        // Create a panel for bottom space
        JPanel bottomSpacePanel = new JPanel();
        bottomSpacePanel.setPreferredSize(new Dimension(0, 50));
        payablePanel.add(bottomSpacePanel, BorderLayout.SOUTH);
	    
	    return payablePanel;
    }
    
    /**
     * Create the "Support" tab.
     * Includes a first line of two text filed to allow the user
     * to enter its credentials. The second line has a text field which
     * was automatically filled by the Tokenization operation and a Detokenization
     * button. The result of the Detokenization operation is displayed
     * to the right of the button.
     * Being the Support account, the user only reads the last 4 digits.
     * The beginning is masked
     * 
     * @return The support account panel
     */
    private JPanel createSupportPanel() {
    	JPanel supportPanel = new JPanel(new BorderLayout());
	    
	    // Create a panel for top space
        JPanel topSpacePanel = new JPanel();
        topSpacePanel.setPreferredSize(new Dimension(0, 20));
        supportPanel.add(topSpacePanel, BorderLayout.NORTH);

        // Create the middle panel with text fields and buttons
        JPanel supportLayout = new JPanel(new GridLayout(2, 3, 5, 90));

        // First line
        JTextField login = new JTextField(10);
        JPasswordField password = new JPasswordField(10);
        supportLayout.add(login);
        supportLayout.add(password);
        supportLayout.add(new JLabel(""));

        // Second line
        JButton detokenizeButton = new JButton("Detokenize");
        detokenizeButton.addActionListener(new ActionListener() {
			@Override
			public void actionPerformed(ActionEvent e) {
				_clearValueSupport.setText(_tokenServer.Detokenize(Var.ct_url, login.getText(), new String(password.getPassword()), _tokenFieldSupport.getText()));
			}
		});
        
        supportLayout.add(_tokenFieldSupport);
        supportLayout.add(detokenizeButton);
        supportLayout.add(_clearValueSupport);

        // Add the middle panel to the center of the appPanel
        supportPanel.add(supportLayout, BorderLayout.CENTER);

        // Create a panel for bottom space
        JPanel bottomSpacePanel = new JPanel();
        bottomSpacePanel.setPreferredSize(new Dimension(0, 50));
        supportPanel.add(bottomSpacePanel, BorderLayout.SOUTH);
	    
	    return supportPanel;
    }

    public static void main(String[] args) {
        // Create and show the application
        SwingUtilities.invokeLater(() -> {
            new TokenizationExample().setVisible(true);
        });
    }
}