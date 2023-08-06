from typing import Any, Dict, List, Optional, cast

import attr

from ..models.aa_sequence_bulk_create import AaSequenceBulkCreate
from ..types import UNSET


@attr.s(auto_attribs=True)
class AaSequencesBulkCreate:
    """  """

    dna_sequences: Optional[List[AaSequenceBulkCreate]] = cast(None, UNSET)

    def to_dict(self) -> Dict[str, Any]:
        if self.dna_sequences is None:
            dna_sequences = None
        elif self.dna_sequences is UNSET:
            dna_sequences = UNSET
        else:
            dna_sequences = []
            for dna_sequences_item_data in self.dna_sequences:
                dna_sequences_item = dna_sequences_item_data.to_dict()

                dna_sequences.append(dna_sequences_item)

        properties: Dict[str, Any] = dict()

        if dna_sequences is not UNSET:
            properties["dnaSequences"] = dna_sequences
        return properties

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "AaSequencesBulkCreate":
        dna_sequences = []
        for dna_sequences_item_data in d.get("dnaSequences") or []:
            dna_sequences_item = AaSequenceBulkCreate.from_dict(dna_sequences_item_data)

            dna_sequences.append(dna_sequences_item)

        return AaSequencesBulkCreate(
            dna_sequences=dna_sequences,
        )
