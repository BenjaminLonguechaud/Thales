package com.thales.cts.samples;
import java.awt.event.FocusEvent;
import java.awt.event.FocusListener;
import javax.swing.JTextField;
public class MyTextField extends JTextField {
	/**
	 * Generated to prevent warning "The serializable class MyTextField
	 * does not declare a static final serialVersionUID"
	 */
	private static final long serialVersionUID = 1L;
	String _originalText;
	public MyTextField(String text) {
		super(text);
		_originalText = new String(text);
		addFocusListener(new FocusListener() {
			@Override
			public void focusLost(FocusEvent arg0) {
				if (getText().trim().equals(""))
					setText(_originalText);
			}
			@Override
			public void focusGained(FocusEvent arg0) {
				if (getText().trim().equals(text))
					setText("");
				else
					// Do Nothing...
					setText(getText());
			}
		});
	}
}
