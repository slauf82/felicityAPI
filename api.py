from __future__ import annotations

import base64
import ssl
from datetime import datetime

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


class FelicityAPI:
    def __init__(self, session, username, password):
        self._session = session
        self._username = username
        self._password = password
        self._token = None
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

    async def login(self):
        url = f"{BASE_URL}{API_LOGIN}"

        payload = {
            "userName": self._username,
            "password": self._encrypt_password(self._password),
            "source": "WEB",
            "lang": "de_DE",
        }

        headers = {
            "Content-Type": "application/json",
            "Origin": "https://shine.felicitysolar.com",
            "Referer": "https://shine.felicitysolar.com/",
        }

        async with self._session.post(
            url,
            json=payload,
            headers=headers,
            ssl=self._ssl,
            timeout=aiohttp.ClientTimeout(total=15),
        ) as resp:
            data = await resp.json(content_type=None)

            if data.get("code") != 200:
                raise Exception(f"Login failed: {data}")

            token = data.get("data", {}).get("token")

            if token and not token.startswith("Bearer_"):
                token = f"Bearer_{token}"

            self._token = token

    async def ensure_login(self):
        if not self._token:
            await self.login()

    def _headers(self):
        return {
            "Authorization": self._token,
            "Content-Type": "application/json",
            "lang": "de_DE",
            "source": "WEB",
        }

    async def list_device_all_type(self):
        await self.ensure_login()

        url = f"{BASE_URL}{API_DEVICE_LIST}"

        async with self._session.get(
            url,
            headers=self._headers(),
            ssl=self._ssl,
            timeout=aiohttp.ClientTimeout(total=15),
        ) as resp:
            return await resp.json(content_type=None)

    async def get_device_snapshot(self, device_sn: str):
        await self.ensure_login()

        url = f"{BASE_URL}{API_DEVICE_SNAPSHOT}"

        payload = {
            "deviceSn": str(device_sn),
            "dateStr": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }

        async with self._session.post(
            url,
            json=payload,
            headers=self._headers(),
            ssl=self._ssl,
            timeout=aiohttp.ClientTimeout(total=15),
        ) as resp:
            return await resp.json(content_type=None)

    async def get_device_basic(self, device_sn: str):
        await self.ensure_login()

        url = f"{BASE_URL}{API_DEVICE_BASIC}/{device_sn}"

        async with self._session.get(
            url,
            headers=self._headers(),
            ssl=self._ssl,
            timeout=aiohttp.ClientTimeout(total=15),
        ) as resp:
            return await resp.json(content_type=None)

    async def get_device_list(self):
        return await self.list_device_all_type()

    async def get_snapshot(self, device_sn: str):
        return await self.get_device_snapshot(device_sn)