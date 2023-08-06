import datetime
from typing import Any, Dict, List

import attr
from dateutil.parser import isoparse

from ..models.container_content import ContainerContent


@attr.s(auto_attribs=True)
class ContainerBase:
    """  """

    id: str
    contents: List[ContainerContent]
    created_at: datetime.datetime
    modified_at: datetime.datetime
    web_url: str

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        contents = []
        for contents_item_data in self.contents:
            contents_item = contents_item_data.to_dict()

            contents.append(contents_item)

        created_at = self.created_at.isoformat()

        modified_at = self.modified_at.isoformat()

        web_url = self.web_url

        properties: Dict[str, Any] = dict()

        properties["id"] = id
        properties["contents"] = contents
        properties["createdAt"] = created_at
        properties["modifiedAt"] = modified_at
        properties["webURL"] = web_url
        return properties

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "ContainerBase":
        id = d["id"]

        contents = []
        for contents_item_data in d["contents"]:
            contents_item = ContainerContent.from_dict(contents_item_data)

            contents.append(contents_item)

        created_at = isoparse(d["createdAt"])

        modified_at = isoparse(d["modifiedAt"])

        web_url = d["webURL"]

        return ContainerBase(
            id=id,
            contents=contents,
            created_at=created_at,
            modified_at=modified_at,
            web_url=web_url,
        )
