from datetime import datetime
from pydantic import BaseModel, Field, HttpUrl


class PinnedPost(BaseModel):
    cid: str
    uri: str


class Associated(BaseModel):
    lists: int | None = None
    feedgens: int | None = None
    starter_packs: int | None = Field(default=0, alias="starterPacks")
    labeler: bool | None = None


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
    associated: Associated | None = None
    viewer: Viewer
    labels: list = []
    created_at: datetime = Field(alias="createdAt")
    indexed_at: datetime = Field(alias="indexedAt")
    followers_count: int | None = Field(default=None, alias="followersCount")
    follows_count: int | None = Field(default=None, alias="followsCount")
    posts_count: int | None = Field(default=None, alias="postsCount")
    pinned_post: PinnedPost | None = Field(default=None, alias="pinnedPost")

    class Config:
        populate_by_name = True
        extra = "allow"


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


class UnfollowRecord(BaseModel):
    cid: str
    rev: str

    class Config:
        extra = "allow"


class Users(BaseModel):
    users: list[UserItem]
    cursor: str | None = None
