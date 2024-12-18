import pytest
from bsky_api.models.user import Commit, FollowRecord
from bsky_api.modules.login import Login
from bsky_api.modules.user import User

FOLLOW_RECORD = FollowRecord(
    uri="at://did:plc:wpixnhsqu4p5ix23recmsda7/app.bsky.graph.follow/3lbfsmppgrg2p",
    cid="bafyreignifhnxgilh7ih4oeatowljttyu6qqho5kd7tmoe27fcdcvdzcpq",
    commit=Commit(
        cid="bafyreihwyeap7n6rcms2ojuoopgpmzt5gfdecrzcd3bgmin5vbg33wzx5a",
        rev="3lbfsmppjp62p",
    ),
    validation_status="valid",
)


@pytest.mark.asyncio
async def test_follow_user(logged_in_client: Login) -> None:
    login = await anext(logged_in_client)

    user_did = "did:plc:hv5mkduryfgajlvmbo3ruole"

    user = User(login)
    follow_response = await user.follow(user_did)

    assert follow_response.validation_status == "valid"
