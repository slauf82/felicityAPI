from __future__ import annotations

import base64
import ssl
from datetime import datetime
from typing import Any

import aiohttp
from Cryptodome.PublicKey import RSA
from Cryptodome.Cipher import PKCS1_v1_5

from .const import (
    API_LOGIN,
    API_DEVICE_LIST,
    API_DEVICE_SNAPSHOT,
    API_DEVICE_BASIC,
    API_DEVICE_ENERGY_FLOW,
    API_DEVICE_WARNINGS,
    API_DEVICE_WARNINGS_FALLBACK,
)

PUBLIC_KEY = "MFwwDQYJKoZIhvcNAQEBBQADSwAwSAJBAK0GDivaRzIKeTmQnAxAYh2LChuHWDp0yHZ0zIvm+Eoi7J+rx7phqR7EtkBDO3HWqAXVkNDeeQaU32P5w1Q4FVUCAwEAAQ=="
PUBLIC_KEY_FALLBACK = "MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAnAJE68pjWZmtSg6ZJs9FZugJXC6bBSluTW6mJttOLOaljrdErVnM5DNN+YFzpB9pAysTErjY1bnSVuEwQSwptnqUji7Ch2qMj2n+0eCp8p6vtSh7/tFr2ul8nDRtkoswLANAIwtUk/G85ipMpmY1W642LImnEJmGkkddlbjbjxJTZWR5hc/d9cPWb+AR77LxFFrMik3c+44v1kQlIPFP6EjIbOvt/Lv7fHWD9JI/YzN4y1gK7C/VQdNGuikQyNg+5W3rg9ecYf9I5uLAQwY/hxeI3lbNsErebqKe2EbJ8AwcNIC0lDBz53Sq0ML89QapEuy3fB+upuctxLULVDCbNwIDAQAB"
API_LOGIN_FALLBACK = "/userlogin"

BASE_URL = "https://shine-api.felicitysolar.com"


class FelicityApiError(Exception):
    pass


class FelicityAuthError(FelicityApiError):
    pass


class FelicityAPI:
    def __init__(self, session, username: str, password: str):
        self._session = session
        self._username = username
        self._password = password
        self._token: str | None = None
        self._ssl = self._create_ssl_context()

    def _create_ssl_context(self):
        context = ssl.create_default_context()
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE
        return context

    def _encrypt_password(self, password: str, public_key: str = PUBLIC_KEY) -> str:
        key = RSA.import_key(base64.b64decode(public_key))
        cipher = PKCS1_v1_5.new(key)
        return base64.b64encode(cipher.encrypt(password.encode())).decode()

    def _auth_headers(self) -> dict[str, str]:
        return {
            "Authorization": self._token or "",
            "Content-Type": "application/json",
            "lang": "de_DE",
            "source": "WEB",
        }

    def _login_headers(self) -> dict[str, str]:
        return {
            "Content-Type": "application/json",
            "Origin": "https://shine.felicitysolar.com",
            "Referer": "https://shine.felicitysolar.com/",
        }

    async def _request(
        self,
        method: str,
        endpoint: str,
        *,
        json_payload: dict[str, Any] | None = None,
        auth: bool = True,
        retry_auth: bool = True,
    ) -> dict[str, Any]:
        if auth:
            await self.ensure_login()

        url = f"{BASE_URL}{endpoint}"

        headers = self._auth_headers() if auth else self._login_headers()

        try:
            async with self._session.request(
                method,
                url,
                json=json_payload,
                headers=headers,
                ssl=self._ssl,
                timeout=aiohttp.ClientTimeout(total=15),
            ) as resp:
                data = await resp.json(content_type=None)

        except Exception as err:
            raise FelicityApiError(f"Request failed: {method} {endpoint}: {err}") from err

        if not isinstance(data, dict):
            raise FelicityApiError(f"Invalid response from {endpoint}: {data}")

        code = data.get("code")

        if auth and retry_auth and code in (401, 403, 998):
            self._token = None
            await self.ensure_login()
            return await self._request(
                method,
                endpoint,
                json_payload=json_payload,
                auth=auth,
                retry_auth=False,
            )

        return data

    def _build_login_payload(
        self,
        encrypted_password: str,
        payload_style: str,
    ) -> dict[str, Any]:
        """Build login payload variants used by different Felicity cloud versions."""
        username_field = "account" if payload_style.endswith("_account") else "userName"

        if payload_style.startswith("modern"):
            return {
                username_field: self._username,
                "password": encrypted_password,
                "version": "1.0",
            }

        return {
            username_field: self._username,
            "password": encrypted_password,
            "source": "WEB",
            "lang": "de_DE",
        }

    async def _login_once(
        self,
        endpoint: str,
        public_key: str,
        payload_style: str,
    ) -> str:
        encrypted_password = self._encrypt_password(self._password, public_key)
        payload = self._build_login_payload(encrypted_password, payload_style)

        data = await self._request(
            "POST",
            endpoint,
            json_payload=payload,
            auth=False,
        )

        if data.get("code") != 200:
            raise FelicityAuthError(f"Login failed via {endpoint}: {data}")

        token = data.get("data", {}).get("token")

        if not token:
            raise FelicityAuthError(f"Login failed via {endpoint}: no token received: {data}")

        if not token.startswith("Bearer_"):
            token = f"Bearer_{token}"

        return token

    async def login(self) -> None:
        endpoints = [API_LOGIN, API_LOGIN_FALLBACK]
        public_keys = [PUBLIC_KEY, PUBLIC_KEY_FALLBACK]
        payload_styles = [
            "legacy_userName",
            "modern_userName",
            "legacy_account",
            "modern_account",
        ]

        # Keep the known working v1.2.0 path first, then try all fallback variants.
        attempts: list[tuple[str, str, str]] = [(API_LOGIN, PUBLIC_KEY, "legacy_userName")]

        for endpoint in endpoints:
            for public_key in public_keys:
                for payload_style in payload_styles:
                    attempt = (endpoint, public_key, payload_style)
                    if attempt not in attempts:
                        attempts.append(attempt)

        errors: list[str] = []

        for endpoint, public_key, payload_style in attempts:
            try:
                self._token = await self._login_once(endpoint, public_key, payload_style)
                return
            except Exception as err:
                errors.append(f"{endpoint}/{payload_style}: {err}")

        raise FelicityAuthError("Login failed for all supported Felicity login variants: " + " | ".join(errors))

    async def ensure_login(self) -> None:
        if not self._token:
            await self.login()

    async def list_device_all_type(self) -> dict[str, Any]:
        return await self._request(
            "GET",
            API_DEVICE_LIST,
        )

    async def get_device_snapshot(self, device_sn: str) -> dict[str, Any]:
        payload = {
            "deviceSn": str(device_sn),
            "dateStr": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }

        return await self._request(
            "POST",
            API_DEVICE_SNAPSHOT,
            json_payload=payload,
        )

    async def get_device_basic(self, device_sn: str) -> dict[str, Any]:
        return await self._request(
            "GET",
            f"{API_DEVICE_BASIC}/{device_sn}",
        )

    async def get_energy_flow(self, device_sn: str) -> dict[str, Any]:
        return await self._request(
            "GET",
            f"{API_DEVICE_ENERGY_FLOW}?deviceSN={device_sn}",
        )


    async def get_warnings(self) -> dict[str, Any]:
        """Fetch device warnings using the historic Felicity typo and the corrected endpoint.

        Felicity currently exposes the warning endpoint with the misspelled
        ``warring`` path. If the cloud API is corrected to ``warnings`` later,
        this fallback keeps warning sensors populated instead of silently
        becoming empty.
        """
        errors: list[str] = []

        for endpoint in (API_DEVICE_WARNINGS, API_DEVICE_WARNINGS_FALLBACK):
            try:
                data = await self._request("GET", endpoint)
            except Exception as err:
                errors.append(f"{endpoint}: {err}")
                continue

            if not isinstance(data, dict):
                errors.append(f"{endpoint}: invalid response {data}")
                continue

            # Treat normal Felicity success as final. A not-found / unsupported
            # response on the old typo endpoint falls through to the corrected
            # spelling.
            if data.get("code") in (None, 200):
                return data

            errors.append(f"{endpoint}: {data}")

        raise FelicityApiError("Warnings endpoint failed for all supported spellings: " + " | ".join(errors))

    async def get_device_list(self) -> dict[str, Any]:
        return await self.list_device_all_type()

    async def get_snapshot(self, device_sn: str) -> dict[str, Any]:
        return await self.get_device_snapshot(device_sn)
