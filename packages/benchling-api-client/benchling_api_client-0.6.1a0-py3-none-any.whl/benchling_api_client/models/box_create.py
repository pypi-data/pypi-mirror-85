from typing import Any, Dict, Optional, cast

import attr

from ..models.schema_summary import SchemaSummary
from ..types import UNSET


@attr.s(auto_attribs=True)
class BoxCreate:
    """  """

    barcode: Optional[str] = cast(None, UNSET)
    fields: Optional[Dict[Any, Any]] = cast(None, UNSET)
    name: Optional[str] = cast(None, UNSET)
    parent_storage_id: Optional[str] = cast(None, UNSET)
    project_id: Optional[str] = cast(None, UNSET)
    schema: Optional[SchemaSummary] = cast(None, UNSET)

    def to_dict(self) -> Dict[str, Any]:
        barcode = self.barcode
        if self.fields is UNSET:
            fields = UNSET
        else:
            fields = self.fields if self.fields else None

        name = self.name
        parent_storage_id = self.parent_storage_id
        project_id = self.project_id
        if self.schema is UNSET:
            schema = UNSET
        else:
            schema = self.schema.to_dict() if self.schema else None

        properties: Dict[str, Any] = dict()

        if barcode is not UNSET:
            properties["barcode"] = barcode
        if fields is not UNSET:
            properties["fields"] = fields
        if name is not UNSET:
            properties["name"] = name
        if parent_storage_id is not UNSET:
            properties["parentStorageId"] = parent_storage_id
        if project_id is not UNSET:
            properties["projectId"] = project_id
        if schema is not UNSET:
            properties["schema"] = schema
        return properties

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "BoxCreate":
        barcode = d.get("barcode")

        fields = None
        if d.get("fields") is not None:
            fields = d.get("fields")

        name = d.get("name")

        parent_storage_id = d.get("parentStorageId")

        project_id = d.get("projectId")

        schema = None
        if d.get("schema") is not None:
            schema = SchemaSummary.from_dict(cast(Dict[str, Any], d.get("schema")))

        return BoxCreate(
            barcode=barcode,
            fields=fields,
            name=name,
            parent_storage_id=parent_storage_id,
            project_id=project_id,
            schema=schema,
        )
