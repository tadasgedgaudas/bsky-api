import pytest

from src.modules.login import Login
from tests.settings import settings


@pytest.mark.asyncio
async def test_login() -> None:
    login = Login(
        username=settings.bsky_username,
        password=settings.bsky_password,
        user_agent=settings.user_agent,
    )
    await login.login()

    login_session = login.session
    assert login_session is not None

    assert login_session.accessJwt is not None
    assert login_session.refreshJwt is not None
    assert login_session.service_endpoint is not None

    assert login_session.handle == settings.bsky_username
    assert login_session.did.startswith("did:plc:")
    assert login_session.controller_did.startswith("did:plc:")
