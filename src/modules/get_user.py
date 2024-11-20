from datetime import datetime
from typing import Any
from curl_cffi.requests.exceptions import HTTPError
from pydantic import BaseModel, Field, HttpUrl

from src.modules.login import Login


class PinnedPost(BaseModel):
    cid: str
    uri: str


class Associated(BaseModel):
    lists: int
    feedgens: int
    starter_packs: int = Field(default=0, alias="starterPacks")
    labeler: bool


class Viewer(BaseModel):
    muted: bool
    blocked_by: bool = Field(default=False, alias="blockedBy")


class UserItem(BaseModel):
    did: str
    handle: str
    display_name: str | None = Field(default=None, alias="displayName")
    avatar: HttpUrl | None = None
    banner: HttpUrl | None = None
    description: str | None = None
    associated: Associated
    viewer: Viewer
    labels: list = []
    created_at: datetime = Field(alias="createdAt")
    indexed_at: datetime = Field(alias="indexedAt")
    followers_count: int = Field(alias="followersCount")
    follows_count: int = Field(alias="followsCount")
    posts_count: int = Field(alias="postsCount")
    pinned_post: PinnedPost | None = Field(default=None, alias="pinnedPost")

    class Config:
        populate_by_name = True
        extra = "allow"


class User:
    def __init__(self, login: Login):
        self.login = login

    async def get_by_did(self, did: str) -> UserItem:
        url_path: str = "/xrpc/app.bsky.actor.getProfile"
        params: dict[str, str] = {"actor": did}

        url = f"{self.login.session.service_endpoint}{url_path}"

        response = await self.login.async_session.get(url, params=params)

        if response.status_code not in (200, 204):
            # TODO: add handling to refresh jwt
            raise HTTPError(
                f"Failed to get user: {response.status_code} -- {response.text}"
            )

        return UserItem(**response.json())
