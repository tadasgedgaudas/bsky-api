from bsky_api.helpers import get_record_key
from bsky_api.models.post import Feed, PostItem
from bsky_api.models.user import FollowRecord, UnfollowRecord, UserItem, Users
from bsky_api.modules.login import Login
from bsky_api.response import check_response


class User:
    def __init__(self, login: Login) -> None:
        self.login = login

    async def get_by_did(self, did: str) -> UserItem:
        url_path: str = "/xrpc/app.bsky.actor.getProfile"
        params: dict[str, str] = {"actor": did}

        url = f"{self.login.session.service_endpoint}{url_path}"

        response = await self.login.async_session.get(url, params=params)

        check_response(response)

        return UserItem(**response.json())

    async def follow(self, did: str) -> FollowRecord:
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

        check_response(response)

        return FollowRecord(**response.json())

    async def unfollow(self, did: str, record_key: str | None = None) -> UnfollowRecord:
        if not record_key:
            follow_record = await self.follow(did)
            record_key = get_record_key(follow_record.uri)

        url_path: str = "/xrpc/com.atproto.repo.deleteRecord"

        url = f"{self.login.session.service_endpoint}{url_path}"

        payload = {
            "collection": "app.bsky.graph.follow",
            "repo": self.login.session.controller_did,
            "rkey": record_key,
        }

        response = await self.login.async_session.post(url, json=payload)

        check_response(response)

        return UnfollowRecord(**response.json())

    async def followers(
        self, did: str, limit: int = 30, cursor: str | None = None
    ) -> Users:
        url_path: str = "/xrpc/app.bsky.graph.getFollowers"
        params: dict[str, str] = {"actor": did, "limit": limit}

        if cursor:
            params["cursor"] = cursor

        url = f"{self.login.session.service_endpoint}{url_path}"

        response = await self.login.async_session.get(url, params=params)

        check_response(response)

        return Users(
            users=[UserItem(**user) for user in response.json()["followers"]],
            cursor=response.json().get("cursor"),
        )

    async def following(
        self, did: str, limit: int = 30, cursor: str | None = None
    ) -> Users:
        url_path: str = "/xrpc/app.bsky.graph.getFollows"
        params: dict[str, str] = {"actor": did, "limit": limit}

        if cursor:
            params["cursor"] = cursor

        url = f"{self.login.session.service_endpoint}{url_path}"

        response = await self.login.async_session.get(url, params=params)

        check_response(response)

        return Users(
            users=[UserItem(**user) for user in response.json()["follows"]],
            cursor=response.json().get("cursor"),
        )

    async def feed(self, did: str, limit: int = 30, cursor: str | None = None) -> Feed:
        url_path: str = "/xrpc/app.bsky.feed.getAuthorFeed"
        params: dict[str, str] = {
            "actor": did,
            "limit": limit,
            "filter": "posts_and_author_threads",
            "includePins": True,
        }

        if cursor:
            params["cursor"] = cursor

        url = f"{self.login.session.service_endpoint}{url_path}"

        response = await self.login.async_session.get(url, params=params)

        check_response(response)

        return Feed(
            items=[PostItem(**item["post"]) for item in response.json()["feed"]],
            cursor=response.json().get("cursor"),
        )
