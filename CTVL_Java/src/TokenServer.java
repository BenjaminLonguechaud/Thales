
package com.thales.cts.samples;

import java.util.Base64;

import org.json.JSONObject;

import javax.net.ssl.HostnameVerifier;
import javax.net.ssl.HttpsURLConnection;
import javax.net.ssl.SSLSession;
import javax.net.ssl.SSLContext;
import javax.net.ssl.TrustManager;
import javax.net.ssl.X509TrustManager;

import java.security.KeyManagementException;
import java.security.NoSuchAlgorithmException;
import java.security.cert.X509Certificate;

import java.io.BufferedReader;
import java.io.DataOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.net.MalformedURLException;
import java.net.URI;

public class TokenServer {
	private String _token;
	private String _clearValue;
	
	/**
	 * Tokenization operation which first verifies that the input is an SSN format
	 * (XXX-XX-XXXX)
	 * @param https_url URL of the Thales Tokenization server.
	 * @param login User login
	 * @param password User password
	 * @param data String to be tokenized
	 * @return The Tokenized data 
	 */
	public String Tokenize(String https_url, String login, String password, String data) {
        try {
        	// Tokenization request
        	String credential = Base64.getEncoder().encodeToString((login + ":" + password).getBytes());

        	removeCertificateValidation();
        	
        	if(!pingHost(https_url, 1000))
        		return "";
        	
        	var url = URI.create(https_url + "/vts/rest/v2.0/tokenize").toURL();
            
            HttpsURLConnection connection = (HttpsURLConnection) url.openConnection();
            connection.setRequestProperty("Content-Type", "application/json");
            connection.setRequestProperty("Authorization", "Basic " + credential);

            String inputData = "{\"data\":\"" + data + "\",\"tokengroup\":\"" + Var.tokengroupCC + "\",\"tokentemplate\":\"" + Var.tokentemplateCC + "\"}";
            connection.setRequestProperty("Content-length", String.valueOf(inputData.length()));
            connection.setRequestMethod("POST");
            connection.setDoOutput(true);
            connection.setDoInput(true);
            DataOutputStream output = new DataOutputStream(connection.getOutputStream());
            output.writeBytes(inputData);
            output.close();
            String outputData = readStream(connection.getInputStream());
            
            JSONObject jo = new JSONObject(outputData);
            _token = jo.getString("token");
            
            connection.disconnect();
            System.out.println("Tokenize server: " + https_url);
            System.out.println("Tokenize request: " + inputData);
            System.out.println("Tokenize response: " + outputData);
            
        } catch (MalformedURLException e) {
            e.printStackTrace();
        } catch (IOException e) {
            e.printStackTrace();
        }
        return _token;
	}
	
	/**
	 * Detokenization operation.
	 * @param https_url URL of the Thales Tokenization server.
	 * @param login User login (admin or support)
	 * @param password User password
	 * @param data String to be detokenized
	 * @return The Detokenized data 
	 */
	public String Detokenize(String https_url, String login, String password, String data) {
        try {
        	String credential = Base64.getEncoder().encodeToString((login + ":" + password).getBytes());
        	
        	removeCertificateValidation();
        	
        	if(!pingHost(https_url, 1000))
        		return "";
        	
        	var url = URI.create(https_url + "/vts/rest/v2.0/detokenize").toURL();
        	
        	HttpsURLConnection connection = (HttpsURLConnection) url.openConnection();
        	
        	String jStr = "{\"token\":\"" + _token + "\",\"tokengroup\" :\"" + Var.tokengroupCC + "\",\"tokentemplate\":\"" + Var.tokentemplateCC + "\"}";
            System.out.println("Token : " + jStr);
            connection.setRequestProperty("Content-length", String.valueOf(jStr.length()));
            connection.setRequestProperty("Content-Type", "application/json");
            connection.setRequestProperty("Authorization", "Basic " + credential);
            connection.setDoOutput(true);
            connection.setDoInput(true);
            connection.setRequestMethod("POST");
            DataOutputStream output = new DataOutputStream(connection.getOutputStream());
            output.writeBytes(jStr);
            output.close();
            String outputData = readStream(connection.getInputStream());
            
            JSONObject jo = new JSONObject(outputData);
            _clearValue = jo.getString("data");
            
            connection.disconnect();
            System.out.println("Detokenize server: " + https_url);
            System.out.println("Detokenize request: " + jStr);
            System.out.println("Detokenize response: " + outputData);

        } catch (MalformedURLException e) {
            e.printStackTrace();
        } catch (IOException e) {
            e.printStackTrace();
        }
        return _clearValue;
	}

	/**
	 * Prevents the verification and validation of SSL certificate.
	 */
	public void removeCertificateValidation() {
		// Create a trust manager that does not validate certificate chains
        TrustManager[] trustAllCerts = new TrustManager[] {new X509TrustManager() {
                public java.security.cert.X509Certificate[] getAcceptedIssuers() {
                    return null;
                }
                public void checkClientTrusted(X509Certificate[] certs, String authType) {
                }
                public void checkServerTrusted(X509Certificate[] certs, String authType) {
                }
            }
        };
 
        // Install the all-trusting trust manager
		try {
			SSLContext sc = SSLContext.getInstance("SSL");
			sc.init(null, trustAllCerts, new java.security.SecureRandom());
			
	        HttpsURLConnection.setDefaultSSLSocketFactory(sc.getSocketFactory());
	    	
	    	// Create all-trusting host name verifier
	        HostnameVerifier allHostsValid = new HostnameVerifier() {
	            public boolean verify(String hostname, SSLSession session) {
	                return true;
	            }
	        };
	    	// Install the all-trusting host verifier
	        HttpsURLConnection.setDefaultHostnameVerifier(allHostsValid);
		}
		catch (NoSuchAlgorithmException e) {
			e.printStackTrace();
		}
        catch (KeyManagementException e) {
			e.printStackTrace();
		}
	}
	
	/**
	 * 
	 * @param hostname URL to check reachability
	 * @param timeout Connection timeout
	 * @return True if hostname is reachable, false otherwize.
	 */
	public boolean pingHost(String hostname, int timeout) {
	    boolean result = false;
		try {
			var url = URI.create(hostname).toURL();
	    	HttpsURLConnection connection = (HttpsURLConnection) url.openConnection();
	        connection.setConnectTimeout(timeout);
	        connection.setReadTimeout(timeout);
	        connection.setRequestMethod("HEAD");
	        int responseCode = connection.getResponseCode();
	        if (responseCode != 200)
            	System.out.println("Hostname is not reachable - Error " + responseCode);
	        else
	        	result = true;
	        connection.disconnect();
	    } catch (IOException exception) {
	        return result;
	    }
		return result;
	}
	
	/**
	 * After the connection was opened with getInputStream, the function
	 * creates a BufferedReader on the input stream and reads from it. 
	 * @param stream input stream from the connection.
	 * @return The string read from the InputStream.
	 */
	private String readStream(InputStream stream) {
		BufferedReader rd = new BufferedReader(new InputStreamReader(stream));
        String line = "";
        String strResponse = "";
        
        try {
			while ((line = rd.readLine()) != null) {
				strResponse = strResponse + line;
			}
		} catch (IOException e) {
			e.printStackTrace();
		}
        return strResponse;
	}
	
}
