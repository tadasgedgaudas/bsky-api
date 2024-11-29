import pytest
from bsky_api.modules.login import Login
from bsky_api.modules.user import User


@pytest.mark.asyncio
async def test_get_followers(logged_in_client: Login) -> None:
    login = await anext(logged_in_client)

    user_did = "did:plc:hv5mkduryfgajlvmbo3ruole"

    user = User(login)
    followers_response = await user.followers(user_did)

    assert followers_response.cursor is not None
    assert len(followers_response.users) > 0
