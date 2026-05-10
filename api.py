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
)

PUBLIC_KEY = "MFwwDQYJKoZIhvcNAQEBBQADSwAwSAJBAK0GDivaRzIKeTmQnAxAYh2LChuHWDp0yHZ0zIvm+Eoi7J+rx7phqR7EtkBDO3HWqAXVkNDeeQaU32P5w1Q4FVUCAwEAAQ=="

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

    def _encrypt_password(self, password: str) -> str:
        key = RSA.import_key(base64.b64decode(PUBLIC_KEY))
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

    async def login(self) -> None:
        payload = {
            "userName": self._username,
            "password": self._encrypt_password(self._password),
            "source": "WEB",
            "lang": "de_DE",
        }

        data = await self._request(
            "POST",
            API_LOGIN,
            json_payload=payload,
            auth=False,
        )

        if data.get("code") != 200:
            raise FelicityAuthError(f"Login failed: {data}")

        token = data.get("data", {}).get("token")

        if not token:
            raise FelicityAuthError(f"Login failed: no token received: {data}")

        if not token.startswith("Bearer_"):
            token = f"Bearer_{token}"

        self._token = token

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

    async def get_device_list(self) -> dict[str, Any]:
        return await self.list_device_all_type()

    async def get_snapshot(self, device_sn: str) -> dict[str, Any]:
        return await self.get_device_snapshot(device_sn)
