from typing import List, Union, Optional
from datalogue.errors import DtlError, _property_not_found
from datalogue.models.transformations.commons import Transformation
from datalogue.dtl_utils import _parse_list
from abc import ABC, abstractmethod
from uuid import UUID

class RecognizeEntities(Transformation):
    """
    RecognizeEntities: Runs all data nodes through the entity recognition service using NER model and passes the classification results to the next stage. Since entity recognition process goes through the value of the node and analyzes individual tokens, one node may have several classification tags attached to it.
    """

    type_str = "RecognizeEntities"

    def __init__(self, model_id: UUID, fieldsToTarget: Optional[List[List[str]]] = None):
        """
        Builds an entity recognition transformation

        :param include_classes: augments resulting ADGs with xyz_#DTL_class nodes containing ontology class for corresponding xyz nodes.
        :param include_scores:  augments resulting ADGs with xyz_#DTL_score nodes containing classification score for corresponding xyz nodes.
        """
        Transformation.__init__(self, RecognizeEntities.type_str)
        self.model_id = model_id
        self.fieldsToTarget = fieldsToTarget

    def __eq__(self, other: 'RecognizeEntities'):
        if isinstance(self, other.__class__):
            return self._as_payload() == other._as_payload()
        return False

    def __repr__(self):
        return f"RecognizeEntities(model_id: {self.model_id}, fieldsToTarget = {self.fieldsToTarget})"

    def _as_payload(self) -> dict:
        base = self._base_payload()
        base['modelId'] = str(self.model_id)
        if self.fieldsToTarget is not None:
            base['fieldsToTarget'] = self.fieldsToTarget
        return base

    @staticmethod
    def _from_payload(json: dict) -> Union[DtlError, 'RecognizeEntities']:
        if json.get(Transformation.type_field) != RecognizeEntities.type_str:
            return DtlError(f"Type of the transformation is not RecognizeEntities! Payload: {str(json)}")

        model_id = UUID(json.get("modelId"))
        fieldsToTarget = json.get("fieldsToTarget")
        return RecognizeEntities(model_id, fieldsToTarget)