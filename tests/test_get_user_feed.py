import pytest
from bsky_api.modules.login import Login
from bsky_api.modules.user import User


@pytest.mark.asyncio
async def test_get_user_feed(logged_in_client: Login) -> None:
    login = await anext(logged_in_client)

    user_did = "did:plc:hv5mkduryfgajlvmbo3ruole"

    items_count = 30
    user = User(login)
    feed = await user.feed(user_did, limit=items_count)

    assert feed.cursor is not None
    assert len(feed.items) == items_count
