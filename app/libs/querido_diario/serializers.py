from dataclasses import dataclass
from enum import Enum
from typing import List, Optional

from ..json_serializeble import JSONSerializeble


@dataclass
class Gazette(JSONSerializeble):
    territory_id: str
    date: str
    url: str
    territory_name: str
    state_code: str
    excerpt: str
    subthemes: List[str]
    entities: List[str]
    txt_url: str
    is_extra_edition: Optional[bool] = None
    edition: Optional[str] = None
    scraped_at: Optional[str] = None

    def json(self):
        return {
            "territory_id": self.territory_id,
            "date": self.date,
            "url": self.url,
            "territory_name": self.territory_name,
            "state_code": self.state_code,
            "excerpt": self.excerpt,
            "edition": self.edition,
            "subthemes": self.subthemes,
            "entities": self.entities,
            "is_extra_edition": self.is_extra_edition,
            "txt_url": self.txt_url,
            "scraped_at": self.scraped_at,
        }


@dataclass
class GazettesResult(JSONSerializeble):
    total_gazettes: int
    gazettes: List[Gazette]

    def json(self):
        return {
            "total_excerpts": self.total_gazettes,
            "excerpts": [gazette.json() for gazette in self.gazettes],
        }

    @classmethod
    def from_json(cls, data: dict):
        return GazettesResult(
            total_gazettes=data["total_excerpts"],
            gazettes=[Gazette(**gazette) for gazette in data["excerpts"]],
        )


class SortByEnum(Enum):
    relevance = "relevance"
    descending_date = "descending_date"
    ascending_date = "ascending_date"


@dataclass
class GazetteFilters:
    entities: Optional[List[str]] = None
    subthemes: Optional[List[str]] = None
    territory_ids: Optional[List[str]] = None
    scraped_since: Optional[str] = None
    scraped_until: Optional[str] = None
    published_since: Optional[str] = None
    published_until: Optional[str] = None
    querystring: Optional[str] = None
    offset: Optional[int] = None
    size: Optional[int] = None
    pre_tags: Optional[str] = None
    post_tags: Optional[str] = None
    sort_by: Optional[str] = None

    def json(self):
        return {
            "entities": self.entities,
            "subthemes": self.subthemes,
            "territory_ids": self.territory_ids,
            "scraped_since": self.scraped_since,
            "scraped_until": self.scraped_until,
            "published_since": self.published_since,
            "published_until": self.published_until,
            "querystring": self.querystring,
            "offset": self.offset,
            "size": self.size,
            "pre_tags": self.pre_tags,
            "post_tags": self.post_tags,
            "sort_by": self.sort_by,
        }
