import hashlib
import hmac
import json
import os
import time

import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class VyaparAPIService:
    """
    A service class to interact with the Vyapar API for fetching summary and detailed
    data related to items, parties, and transactions.

    The class handles authentication using HMAC signatures, prepares appropriate headers,
    and manages request sending and response parsing.
    """

    def __init__(self, user_id):
        """
        Initializes the VyaparAPIService by loading base URL, API key, vendor,
        and user_id from environment variables or constructor arguments.
        """
        self.BASE_URL = "https://staging.vyaparapp.in/api/ns/public/"
        self.api_key = os.getenv("VYAPAR_API_KEY")
        self.vendor = os.getenv("VYAPAR_VENDOR")
        self.user_id = user_id

        if not self.api_key or not self.vendor:
            raise ValueError("API Key or Vendor is missing. Check your .env file.")

    def signature_code(self,api_key, payload_str):
        """
        Generate HMAC SHA256 signature required for API authentication.

        Args:
            api_key (str): The secret API key.
            payload_str (str): The payload string to be signed.

        Returns:
            str: The generated HMAC signature.
        """
        signature = hmac.new(
            api_key.encode("utf-8"),
            payload_str.encode("utf-8"),
            hashlib.sha256,
        ).hexdigest()
        return signature

    def _add_auth_headers(self, payload):
        """
        Create headers including vendor, timestamp, and HMAC signature.

        Args:
            payload (dict): The JSON payload of the request.

        Returns:
            dict: A dictionary of HTTP headers.
        """
        timestamp = str(int(time.time() * 1000))
        req_body = json.dumps(payload, separators=(",", ":"))
        payload_str = req_body + self.vendor + timestamp
        signature = self.signature_code(self.api_key, payload_str)

        headers = {
            "x-vendor": self.vendor,
            "x-api-version": "1",
            "Content-Type": "application/json",
            "x-timestamp": timestamp,
            "x-auth-signature": signature,
        }
        return headers

    def _post(self, endpoint, payload):
        """
        Send a POST request to the Vyapar API and return structured response.

        Args:
            endpoint (str): The API endpoint (e.g., 'items-summary').
            payload (dict): The request body.

        Returns:
            dict: Response data with status and message.
        """
        url = self.BASE_URL + endpoint
        headers = self._add_auth_headers(payload)

        try:
            response = requests.post(url, json=payload, headers=headers, timeout=10)
            response.raise_for_status()
            data = response.json()

            if response.status_code in (200, 201) and data.get("statusCode") == 200:
                return {
                    "status": "success",
                    "data": data.get("data"),
                    "message": data.get("message", "Success"),
                }
            else:
                return {
                    "status": "failed",
                    "data": data.get("data"),
                    "message": f"API returned error: {data.get('message', 'No error message')}",
                    "api_status": data.get("status"),
                    "statusCode": data.get("statusCode"),
                }

        except requests.exceptions.Timeout:
            return {
                "status": "failed",
                "data": None,
                "message": "Request timed out while calling Vyapar API",
            }
        except requests.exceptions.ConnectionError:
            return {
                "status": "failed",
                "data": None,
                "message": "Failed to connect to Vyapar API",
            }
        except requests.exceptions.RequestException as e:
            return {
                "status": "failed",
                "data": None,
                "message": f"HTTP Request error: {str(e)}",
            }

    def item_summary(self, limit=10):
        """
        Fetch item summary data.

        Args:
            limit (int): Number of items to fetch (default: 10).

        Returns:
            dict: API response with summary of items.
        """
        payload = {"user_data_identifier_id": self.user_id, "limit": limit}
        return self._post("items-summary", payload)

    def item_detailed(self, item_ids):
        """
        Fetch detailed item data.

        Args:
            item_ids (list): List of item IDs to fetch.

        Returns:
            dict: API response with detailed item data.
        """
        payload = {"user_data_identifier_id": self.user_id, "item_ids": item_ids}
        return self._post("items-detailed", payload)

    def party_summary(self, limit=10):
        """
        Fetch party summary data.

        Args:
            limit (int): Number of parties to fetch (default: 10).

        Returns:
            dict: API response with summary of parties.
        """
        payload = {"user_data_identifier_id": self.user_id, "limit": limit}
        return self._post("parties-summary", payload)

    def party_detailed(self, party_ids):
        """
        Fetch detailed party data.

        Args:
            party_ids (list): List of party IDs to fetch.

        Returns:
            dict: API response with detailed party data.
        """
        payload = {"user_data_identifier_id": self.user_id, "party_ids": party_ids}
        return self._post("parties-detailed", payload)

    def transaction_summary(self, limit=10):
        """
        Fetch transaction summary data.

        Args:
            limit (int): Number of transactions to fetch (default: 10).

        Returns:
            dict: API response with summary of transactions.
        """
        payload = {"user_data_identifier_id": self.user_id, "limit": limit}
        return self._post("transactions-summary", payload)

    def transaction_detailed(self, transaction_ids):
        """
        Fetch detailed transaction data.

        Args:
            transaction_ids (list): List of transaction IDs to fetch.

        Returns:
            dict: API response with detailed transaction data.
        """
        payload = {
            "user_data_identifier_id": self.user_id,
            "transaction_ids": transaction_ids,
        }
        return self._post("transactions-detailed", payload)
