from typing import AsyncGenerator
import pytest

from src.modules.login import Login
from tests.settings import settings


@pytest.fixture
async def logged_in_client() -> AsyncGenerator[Login, None]:
    login = Login(
        username=settings.bsky_username,
        password=settings.bsky_password,
        user_agent=settings.user_agent,
    )
    await login.login()
    yield login
