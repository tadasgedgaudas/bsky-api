import pytest
from bsky_api.modules.login import Login
from bsky_api.modules.user import User


@pytest.mark.asyncio
async def test_unfollow_user(logged_in_client: Login) -> None:
    login = await anext(logged_in_client)

    user_did = "did:plc:hv5mkduryfgajlvmbo3ruole"

    user = User(login)
    unfollow_response = await user.unfollow(user_did)

    assert unfollow_response.cid is not None
    assert unfollow_response.rev is not None
