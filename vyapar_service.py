# vyapar_service.py

import hashlib
import hmac
import json
import time

import requests


class VyaparAPIService:
    def __init__(self):
        self.BASE_URL = "https://staging.vyaparapp.in/api/ns/public/"
        self.HEADERS = {
            "x-vendor": "RUPYZ",
            "x-api-version": "1",
            "Content-Type": "application/json",
        }

    def _add_auth_headers(self, payload):
        api_key = "VYAPAR_STAGING_224abc40-de2d-441d-afec-754e4edd3ce1"
        vendor = "RUPYZ"
        timestamp = str(int(time.time() * 1000))
        req_body = json.dumps(payload, separators=(",", ":"))

        payload = req_body + vendor + timestamp

        signature = hmac.new(
            api_key.encode("utf-8"), payload.encode("utf-8"), hashlib.sha256
        ).hexdigest()

        headers = self.HEADERS.copy()
        headers["x-timestamp"] = timestamp
        headers["x-auth-signature"] = signature
        return headers

    def _post(self, endpoint, payload):
        url = self.BASE_URL + endpoint
        headers = self._add_auth_headers(payload)
        response = requests.post(url, json=payload, headers=headers)
        return response.json()

    def item_summary(self, user_id, limit=10):
        payload = {"user_data_identifier_id": user_id, "limit": limit}
        return self._post("items-summary", payload)

    def item_detailed(self, user_id, item_ids):
        payload = {"user_data_identifier_id": user_id, "item_ids": item_ids}
        return self._post("items-detailed", payload)

    def party_summary(self, user_id, limit=10):
        payload = {"user_data_identifier_id": user_id, "limit": limit}
        return self._post("parties-summary", payload)

    def party_detailed(self, user_id, party_ids):
        payload = {"user_data_identifier_id": user_id, "party_ids": party_ids}
        return self._post("parties-detailed", payload)

    def transaction_summary(self, user_id, limit=10):
        payload = {"user_data_identifier_id": user_id, "limit": limit}
        return self._post("transactions-summary", payload)

    def transaction_detailed(self, user_id, transaction_ids):
        payload = {
            "user_data_identifier_id": user_id,
            "transaction_ids": transaction_ids,
        }
        return self._post("transactions-detailed", payload)
