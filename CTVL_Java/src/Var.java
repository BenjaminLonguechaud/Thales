package com.thales.cts.samples;
/**
 * Set of configuration variables from the Thales Tokenization Server.
 */
public class Var {
    /**
     * CT-VL IP address
     */
    public static String ct_url = System.getenv("TOKEN_SERVER_IP");
    /**
     * Tokenization group with associated token key
     */
    public static String tokengroupCC = "tokenization_group";
    /**
     * Tokenization template used to supply parameters to the
     * tokenization/detokenization operation.
     * Format: FPE
     * Character Set: All digits
     * Keep left: 0
     * Keep right: 0
     * Allow small input set to true.
     */
    public static String tokentemplateCC = "token_template_0-4";
}
