import random
from typing import Any
from curl_cffi.requests import AsyncSession
from curl_cffi.requests.exceptions import HTTPError
from pydantic import BaseModel


class LoginSession(BaseModel):
    accessJwt: str
    refreshJwt: str
    handle: str
    did: str
    controller_did: str
    service_endpoint: str


class Login:
    def __init__(
        self,
        username: str,
        password: str,
        user_agent: str | None = None,
        headers: dict[str, str] | None = None,
    ) -> None:
        headers = headers or {}
        self.username = username
        self.password = password

        self.async_session = AsyncSession()
        self.session: LoginSession | None = None

        USER_AGENTS = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.3",
            "Mozilla/5.0 (Linux; Android 13; S110 Build/TP1A.220624.014) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.6668.71 Mobile Safari/537.36 OPX/2.5",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 17_5_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.5 Mobile/15E148 Safari/604.1",
        ]

        DEFAULT_HEADERS = {
            "accept": "*/*",
            "accept-language": "en-US,en;q=0.9",
            "content-type": "application/json",
            "priority": "u=1, i",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "cross-site",
            "Referer": "https://bsky.app/",
            "Referrer-Policy": "origin-when-cross-origin",
        }

        if not user_agent:
            user_agent = random.choice(USER_AGENTS)

        if not headers:
            headers = DEFAULT_HEADERS

        self.user_agent = user_agent
        self.headers = headers
        self.url = "https://bsky.social/xrpc/com.atproto.server.createSession"

    def _parse_response(self, response: dict[str, Any]) -> LoginSession:
        return LoginSession(
            accessJwt=response["accessJwt"],
            refreshJwt=response["refreshJwt"],
            handle=response["handle"],
            did=response["did"],
            controller_did=response["didDoc"]["verificationMethod"][0]["controller"],
            service_endpoint=response["didDoc"]["service"][0]["serviceEndpoint"],
        )

    async def login(self) -> None:
        headers = self.headers
        headers["user-agent"] = self.user_agent
        self.async_session.headers = headers

        payload = {
            "identifier": self.username,
            "password": self.password,
            "authFactorToken": "",
        }
        response = await self.async_session.post(self.url, json=payload)
        if response.status_code != 200:
            raise HTTPError(
                f"Failed to login: {response.status_code} -- {response.text}"
            )

        self.session = self._parse_response(response.json())
        self.async_session.headers["Authorization"] = f"Bearer {self.session.accessJwt}"

    async def refresh_jwt(self) -> None:
        self.session.refreshJwt = "refreshed"
