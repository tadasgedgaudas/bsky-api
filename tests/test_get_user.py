import datetime
from pydantic_core import Url
import pytest
from typing import AsyncGenerator
from src.models.user import Associated, PinnedPost, UserItem, Viewer
from src.modules.login import Login
from src.modules.user import User
from tests.settings import settings


USER_INFO = UserItem(
    did="did:plc:hv5mkduryfgajlvmbo3ruole",
    handle="markoraassina.bsky.social",
    display_name="Marko (NERD PLUSHIE OUT NOW!)",
    avatar=Url(
        "https://cdn.bsky.app/img/avatar/plain/did:plc:hv5mkduryfgajlvmbo3ruole/bafkreicbte7xmirpbknccnb6l5ho3rzayi2o6oxgc46klgejvk7h5ql6ua@jpeg"
    ),
    banner=Url(
        "https://cdn.bsky.app/img/banner/plain/did:plc:hv5mkduryfgajlvmbo3ruole/bafkreiheo6rxpgzu2luflz76z7orzhp7i3fq7hzgwaw4djwyfsz4umvnii@jpeg"
    ),
    description="Official page of Marko Raassina, Finnish comic creator of Nerd and Jock! Get NERD PLUSHIE from link below\nhttps://www.makeship.com/products/nerd-plushie\nhttps://www.patreon.com/Markocomics\n",
    associated=Associated(lists=0, feedgens=0, starter_packs=0, labeler=False),
    viewer=Viewer(muted=False, blocked_by=False),
    labels=[],
    created_at=datetime.datetime(2024, 10, 22, 17, 19, 42, 845000),
    indexed_at=datetime.datetime(2024, 11, 11, 20, 13, 40, 937000),
    followers_count=84674,
    follows_count=15,
    posts_count=232,
    pinned_post=PinnedPost(
        cid="bafyreiaeqvlv2niwbprszw5yjjpee2t4ylng3y2epbooisit6n7n2peare",
        uri="at://did:plc:hv5mkduryfgajlvmbo3ruole/app.bsky.feed.post/3laotejpuwc2g",
    ),
)


@pytest.fixture
async def logged_in_client() -> AsyncGenerator[Login, None]:
    login = Login(
        username=settings.bsky_username,
        password=settings.bsky_password,
        user_agent=settings.user_agent,
    )
    await login.login()
    yield login


@pytest.mark.asyncio
async def test_get_user(logged_in_client: Login) -> None:
    login = await anext(logged_in_client)

    user_did = "did:plc:hv5mkduryfgajlvmbo3ruole"

    user = User(login)
    user_info = await user.get_by_did(user_did)

    assert user_info.did == USER_INFO.did
    assert user_info.handle == USER_INFO.handle
    assert user_info.display_name == USER_INFO.display_name
    assert user_info.followers_count >= USER_INFO.followers_count
