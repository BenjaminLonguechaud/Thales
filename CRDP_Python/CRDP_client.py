import requests
from typing import Optional, Dict, Any
from urllib.parse import urljoin
from logger import logger
from config_manager import ConfigManager

class CRDPClient:
    """Client for interacting with CRDP API endpoints."""

    def __init__(self, config: ConfigManager):
        """Initialize CRDP client.

        Args:
            config: ConfigManager instance
        """
        self.config = config
        self.crdp_url = config.get("crdp.url", "http://localhost:32085").rstrip('/')
        self.timeout = config.get("crdp.timeout", 10)
        self.ssl_verify = config.get("crdp.ssl_verify", False)
        self.ciphertrust_url = config.get("ciphertrust.url", "http://localhost")
        self.username = config.get("ciphertrust.username", "admin")
        self.password = config.get("ciphertrust.password", "password")

        self.session = requests.Session()
        self.session.verify = self.ssl_verify
        self.session.headers.update({'Content-Type': 'application/json'})

    def load_policies(self):
        """
        Fetches the list of protection policies from the API.

        Returns:
            list: A list of protection policies if successful
        """

        # Authenticate to get the JWT token
        token_url = urljoin(self.ciphertrust_url, '/api/v1/auth/tokens')
        policies_url = urljoin(self.ciphertrust_url, '/api/v1/data-protection/protection-policies')

        auth_payload = {
            "name": self.username,
            "password": self.password
        }

        try:
            auth_response = requests.post(token_url, json=auth_payload, verify=False)
            auth_response.raise_for_status()
            jwt_token = auth_response.json().get("jwt")

            headers = {
                "Authorization": f"Bearer {jwt_token}",
            }

            logger.info(f"Loading protection policies")
            policies_response = self.session.get(policies_url, headers=headers, timeout=self.timeout)
            policies_response.raise_for_status()
            result = [resource["name"] for resource in policies_response.json().get("resources", [])]
            # Remove duplicates by converting to a set, then back to a list
            unique_names = list(set(result))
            return unique_names

        except requests.exceptions.RequestException as e:
            logger.error(f"API Error while loading policies: {str(e)}")
            raise Exception(f"Failed to load protection policies: {str(e)}")

    def protect(self, data: str, protection_policy_name: str) -> Optional[Dict[str, Any]]:
        """Protect data using CRDP.

        Args:
            data: Raw data to protect
            protection_policy_name: Name of the protection policy to apply

        Returns:
            Protected data response or None on failure
        """
        try:
            url = urljoin(self.crdp_url, '/v1/protect')
            payload = {
                "protection_policy_name": protection_policy_name,
                "data": data
            }

            logger.info(f"Calling protect API with policy: {protection_policy_name}")
            response = self.session.post(url, json=payload, timeout=self.timeout)
            response.raise_for_status()

            result = response.json()
            logger.info("Data protected successfully")
            return result

        except requests.exceptions.RequestException as e:
            logger.error(f"API Error during protect: {str(e)}")
            raise Exception(f"Failed to protect data: {str(e)}")

    def unprotect(self, protected_data: str, protection_policy_name: str, username: str, external_version: str = "1001002") -> Optional[Dict[str, Any]]:
        """Reveal/unprotect data using CRDP.

        Args:
            protected_data: Protected data to reveal
            protection_policy_name: Name of the protection policy used
            username: Username for audit logging
            external_version: External version (defaults to "1001002")

        Returns:
            Revealed data response or None on failure
        """
        try:
            url = urljoin(self.crdp_url, '/v1/reveal')
            payload = {
                "protected_data": protected_data,
                "protection_policy_name": protection_policy_name,
                "username": username,
                "external_version": external_version
            }

            logger.info(f"Calling reveal API with policy: {protection_policy_name}")
            response = self.session.post(url, json=payload, timeout=self.timeout)
            response.raise_for_status()

            result = response.json()
            logger.info("Data revealed successfully")
            return result

        except requests.exceptions.RequestException as e:
            logger.error(f"API Error during reveal: {str(e)}")
            raise Exception(f"Failed to reveal data: {str(e)}")
