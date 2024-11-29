from datetime import datetime
from pydantic import BaseModel, Field, HttpUrl


class Viewer(BaseModel):
    muted: bool
    blocked_by: bool = Field(alias="blockedBy")


class Author(BaseModel):
    did: str
    handle: str
    display_name: str | None = Field(alias="displayName")
    avatar: HttpUrl
    viewer: Viewer
    labels: list
    created_at: datetime = Field(alias="createdAt")


class AspectRatio(BaseModel):
    height: int
    width: int


class BlobRef(BaseModel):
    link: str = Field(alias="$link")


class Blob(BaseModel):
    type: str = Field(alias="$type")
    ref: BlobRef
    mime_type: str = Field(alias="mimeType")
    size: int


class Image(BaseModel):
    type: str = Field(alias="$type")
    ref: BlobRef


class EmbedImage(BaseModel):
    image: Image | None = None
    thumb: str | None = None
    alt: str
    aspect_ratio: AspectRatio = Field(alias="aspectRatio")


class Embed(BaseModel):
    type: str = Field(alias="$type")
    images: list[EmbedImage] | None = None


class Record(BaseModel):
    type: str = Field(alias="$type")
    created_at: datetime = Field(alias="createdAt")
    embed: Embed
    langs: list[str]
    text: str
    images: list[EmbedImage] | None = None


class ImageView(BaseModel):
    thumb: str
    fullsize: str
    alt: str
    aspect_ratio: AspectRatio = Field(alias="aspectRatio")


class PostViewer(BaseModel):
    thread_muted: bool = Field(alias="threadMuted")
    embedding_disabled: bool = Field(alias="embeddingDisabled")


class PostItem(BaseModel):
    uri: str
    cid: str
    author: Author
    record: Record
    embed: Embed
    reply_count: int = Field(alias="replyCount")
    repost_count: int = Field(alias="repostCount")
    like_count: int = Field(alias="likeCount")
    quote_count: int = Field(alias="quoteCount")
    indexed_at: datetime = Field(alias="indexedAt")
    viewer: PostViewer
    labels: list

    class Config:
        populate_by_name = True
        extra = "allow"


class Feed(BaseModel):
    items: list[PostItem]
    cursor: str | None = None
