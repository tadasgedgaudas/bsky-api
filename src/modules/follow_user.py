from typing import Any

from pydantic import BaseModel, Field
from src.modules.login import Login

from curl_cffi.requests.exceptions import HTTPError


class Commit(BaseModel):
    cid: str
    rev: str


class FollowRecord(BaseModel):
    uri: str
    cid: str
    commit: Commit
    validation_status: str = Field(alias="validationStatus")

    class Config:
        populate_by_name = True
        extra = "allow"


class Follow:
    def __init__(self, login: Login):
        self.login = login

    async def user(self, did: str) -> dict[str, Any]:
        url_path: str = "/xrpc/com.atproto.repo.createRecord"

        url = f"{self.login.session.service_endpoint}{url_path}"

        payload = {
            "collection": "app.bsky.graph.follow",
            "repo": self.login.session.controller_did,
            "record": {
                "subject": did,
                "createdAt": "2024-11-20T20:15:04.549Z",
                "$type": "app.bsky.graph.follow",
            },
        }

        response = await self.login.async_session.post(url, json=payload)

        if response.status_code not in (200, 204):
            # TODO: add handling to refresh jwt
            raise HTTPError(
                f"Failed to get user: {response.status_code} -- {response.text}"
            )

        return FollowRecord(**response.json())
