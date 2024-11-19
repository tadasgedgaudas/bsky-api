import random
from curl_cffi.requests import AsyncSession

class Login:
    def __init__(self, username: str, password: str, user_agent: str | None = None, headers: dict[str, str] | None = None) -> None:
        headers = headers or {}
        self.username = username
        self.password = password

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
            "Referrer-Policy": "origin-when-cross-origin"
        }

        if not user_agent:
            user_agent = random.choice(USER_AGENTS)
        if not headers:
            headers = DEFAULT_HEADERS
    
        self.user_agent = user_agent
        self.headers = headers
        self.url = "https://bsky.social/xrpc/com.atproto.server.createSession"

    async def login(self):
        headers = self.headers
        headers["user-agent"] = self.user_agent
        session = AsyncSession(headers=headers)

        payload = {
            "identifier": self.username,
            "password": self.password,
            "authFactorToken": "",
        }
        response = await session.post(self.url, json=payload)
        response.raise_for_status()
        return response.json()  # TODO: return session object pydantic model

