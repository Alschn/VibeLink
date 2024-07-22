import dataclasses
import enum
from typing import Any


class YoutubeParts(enum.StrEnum):
    SNIPPET = 'snippet'
    CONTENT_DETAILS = 'contentDetails'
    FILE_DETAILS = 'fileDetails'
    PLAYER = 'player'
    PROCESSING_DETAILS = 'processingDetails'
    RECORDING_DETAILS = 'recordingDetails'
    STATISTICS = 'statistics'
    STATUS = 'status'
    SUGGESTIONS = 'suggestions'
    TOPIC_DETAILS = 'topicDetails'
    VIDEO_ID = 'id'


@dataclasses.dataclass
class YoutubePageInfo:
    totalResults: int
    resultsPerPage: int


@dataclasses.dataclass
class YoutubeVideoStatistics:
    viewCount: int
    likeCount: int | None = None
    commentCount: int | None = None


@dataclasses.dataclass
class YoutubeVideoSnippet:
    publishedAt: str
    channelId: str
    title: str
    description: str
    thumbnails: dict[str, Any]
    channelTitle: str
    categoryId: str
    defaultLanguage: str = dataclasses.field(default_factory=str)
    defaultAudioLanguage: str = dataclasses.field(default_factory=str)
    tags: list[str] = dataclasses.field(default_factory=list)


@dataclasses.dataclass
class YoutubeVideo:
    kind: str
    etag: str
    id: str
    snippet: YoutubeVideoSnippet
    statistics: YoutubeVideoStatistics


@dataclasses.dataclass
class YoutubeVideoList:
    kind: str
    etag: str
    items: list[YoutubeVideo]
    pageInfo: YoutubePageInfo
