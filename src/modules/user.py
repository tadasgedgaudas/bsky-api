from src.models.user import FollowRecord, UserItem, Users
from src.modules.login import Login
from src.response import check_response


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

    async def followers(self, did: str, limit: int = 30) -> list[UserItem]:
        url_path: str = "/xrpc/app.bsky.graph.getFollowers"
        params: dict[str, str] = {"actor": did, "limit": limit}

        url = f"{self.login.session.service_endpoint}{url_path}"

        response = await self.login.async_session.get(url, params=params)

        check_response(response)

        return Users(
            users=[UserItem(**user) for user in response.json()["followers"]],
            cursor=response.json().get("cursor"),
        )