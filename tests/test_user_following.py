import pytest
from src.modules.login import Login
from src.modules.user import User


@pytest.mark.asyncio
async def test_get_following(logged_in_client: Login) -> None:
    login = await anext(logged_in_client)

    user_did = "did:plc:wv5f5hbz27vg4jgcxifp23uo"

    user = User(login)
    following_response = await user.following(user_did)

    assert following_response.cursor is not None
    assert len(following_response.users) > 0
