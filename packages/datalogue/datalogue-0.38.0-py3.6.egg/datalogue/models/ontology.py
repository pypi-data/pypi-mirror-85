from typing import Dict, List, Optional, Union
from uuid import UUID
import itertools

from datalogue.errors import _enum_parse_error, DtlError
from datalogue.models.permission import OntologyPermission
from datalogue.models.scope_level import Scope
from datalogue.dtl_utils import _parse_list, SerializableStringEnum


class TrainingDataColumn:
    def __init__(self,
                 datastore_name: str,
                 path: List[str] = [],
                 count: int = 0):

        if count is not 0 and not isinstance(count, int):
            raise DtlError("count should be an integer in TrainingDataColumn")

        self.datastore_name = datastore_name
        self.path = path
        self.count = count

    def __eq__(self, other: 'TrainingDataColumn'):
        if isinstance(self, other.__class__):
            return (self.datastore_name == other.datastore_name and
                    self.path == other.path and
                    self.count == other.count)
        return False

    @staticmethod
    def _as_payload(training_data_column: 'TrainingDataColumn') -> Union[DtlError, dict]:
        payload = {
            "datastore_name": str(training_data_column.datastore_name),
            "path": list(map(lambda n: str(n), training_data_column.path)),
            "count": training_data_column.count
        }

        return payload

    @staticmethod
    def _from_payload(payload: dict) -> Union[DtlError, 'TrainingDataColumn']:
        datastore_name = payload.get("datastore_name")
        path = payload.get("path")
        count = payload.get("count")
        
        if datastore_name is None:
            return DtlError("'datastore_name' not defined in TrainingDataColumn")
        
        if path is None:
            path = []

        return TrainingDataColumn(datastore_name, path, count)


class OntologyNode:
    def __init__(self,
                 name: str,
                 description: Optional[str] = None,
                 children: List['OntologyNode'] = [],
                 id: Optional[UUID] = None,
                 total_training_count: int = 0,
                 training_data_columns: List[TrainingDataColumn] = []):

        if not isinstance(name, str):
            raise DtlError("name should be string in OntologyNode")

        if description is not None and not isinstance(description, str):
            raise DtlError("description should be string in OntologyNode")

        if not isinstance(children, List):
            raise DtlError("children should be list in OntologyNode")

        if id is not None and not isinstance(id, UUID):
            raise DtlError("id should be uuid in OntologyNode")

        if total_training_count is not 0 and not isinstance(total_training_count, int):
            raise DtlError("total_training_count should be an integer in OntologyNode")

        self.name = name
        self.description = description
        self.children = children
        self.id = id
        self.total_training_count = total_training_count
        self.training_data_columns = training_data_columns

    def __eq__(self, other: 'OntologyNode'):
        if isinstance(self, other.__class__):
            return (self.name == other.name and
                    self.description == other.description and
                    self.children == other.children and
                    self.id == other.id and 
                    self.total_training_count == other.total_training_count and 
                    self.training_data_columns == other.training_data_columns)
        return False


    def __repr__(self):
        return f'{self.__class__.__name__}(id: {self.id}, name: {self.name!r})'

    @staticmethod
    def as_payload(ontology_node: 'OntologyNode') -> Union[DtlError, dict]:
        payload = {
            "name": ontology_node.name,
            "children": list(map(lambda n: OntologyNode.as_payload(n), ontology_node.children)),
            "training_data_columns": list(map(lambda n: TrainingDataColumn._as_payload(n), ontology_node.training_data_columns)),
            "total_training_count": ontology_node.total_training_count
        }

        if ontology_node.id is not None:
            payload["node_id"] = str(ontology_node.id)

        if ontology_node.description is not None:
            payload["description"] = ontology_node.description

        return payload

    @staticmethod
    def from_payload(payload: dict) -> Union[DtlError, 'OntologyNode']:
        id = UUID(payload.get("id"))
        name = payload.get("name")
        description = payload.get("description")
        children = payload.get("children")
        total_training_count = payload.get("total_training_count")
        training_data_columns = payload.get("training_data_columns")

        if children is None:
            children = []
        else:
            children = _parse_list(OntologyNode.from_payload)(children)
        
        if training_data_columns is None:
            training_data_columns = []
        else:
            training_data_columns = _parse_list(OntologyNode.from_payload)(training_data_columns)
        
        if total_training_count is None:
            total_training_count = 0
        return OntologyNode(name, description, children, id, total_training_count, training_data_columns)


class Ontology:
    def __init__(self,
                 name: str,
                 description: Optional[str] = None,
                 tree: List[OntologyNode] = [],
                 id: Optional[UUID] = None):

        if not isinstance(name, str):
            raise DtlError("name should be string in Ontology")

        if description is not None and not isinstance(description, str):
            raise DtlError("description should be string in Ontology")

        if not isinstance(tree, List):
            raise DtlError("tree should be list in Ontology")

        if id is not None and not isinstance(id, UUID):
            raise DtlError("id should be uuid in Ontology")

        self.name = name
        self.description = description
        self.tree = tree
        self.id = id



    def __eq__(self, other: 'Ontology'):
        if isinstance(self, other.__class__):
            return (self.name == other.name and
                    self.description == other.description and
                    self.tree == other.tree and
                    self.id == other.id)
        return False

    def __repr__(self):
        def print_nodes(tree, output=[], level=0):
            for n in tree:
                padding = '   ' * level
                if level == 0:
                    output.append(padding + n.name)
                else:
                    output.append(padding + '|___' + n.name)
                for c in n.children:
                    print_nodes([c], output, level=level+1)
            return output

        first_line = f'Ontology(id: {self.id}, name: {self.name!r}, description: {self.description!r})' + '\n'
        return '\n'.join(print_nodes(self.tree, [first_line]))

    def leaves(self) -> List[OntologyNode]:
        def iterate(node: OntologyNode) -> List[OntologyNode]:
            if not node.children:
                return [ node ]
            else:
                return list(itertools.chain(*map(lambda n: iterate(n), node.children)))

        return list(itertools.chain(*map(lambda n: iterate(n), self.tree)))

    @staticmethod
    def _as_payload(ontology: 'Ontology') -> Union[DtlError, dict]:
        payload = {
            "name": ontology.name,
            "children": list(map(lambda n: OntologyNode.as_payload(n), ontology.tree))
        }

        if ontology.description is not None:
            payload["description"] = ontology.description

        return payload

    @staticmethod
    def _from_payload(payload: dict) -> Union[DtlError, 'Ontology']:
        id = UUID(payload.get("id"))
        name = payload.get("name")
        description = payload.get("description")
        tree = payload.get("tree")
        if tree is None:
            tree = []
        else:
            tree = _parse_list(OntologyNode.from_payload)(payload["tree"])
        return Ontology(name, description, tree, id=id)

    @staticmethod
    def _create_body_for_sharing(target_id: UUID, target_type: Scope, permission: OntologyPermission) -> Dict:

        if not isinstance(target_type, Scope):
             return DtlError(f"'{target_type}' should be a type of '{Scope.__name__}' and must be in: {list(map(str, Scope))}")

        if not isinstance(permission, OntologyPermission):
            return DtlError(f"'{permission}' should be a type of '{OntologyPermission.__name__}' and must be in: {list(map(str, OntologyPermission))}")

        body = {}

        body["organizations"] = None
        body["groups"] = None
        body["users"] = None

        if target_type == Scope.User:
            body["users"] = {str(target_id): permission.value}
        elif target_type == Scope.Group:
            body["groups"] = {str(target_id): permission.value}
        elif target_type == Scope.Organization:
            body["organizations"] = {str(target_id): permission.value}
        return body


    @staticmethod
    def _create_body_for_unsharing(target_id: UUID, target_type: Scope, permission: str) -> Dict:

        if not isinstance(target_type, Scope):
             return DtlError(f"'{target_type}' should be a type of '{Scope.__name__}' and must be in: {list(map(str, Scope))}")

        body = {}

        body["organizations"] = None
        body["groups"] = None
        body["users"] = None

        if target_type == Scope.User:
            body["users"] = {str(target_id): permission}
        elif target_type == Scope.Group:
            body["groups"] = {str(target_id): permission}
        elif target_type == Scope.Organization:
            body["organizations"] = {str(target_id): permission}
        return body


class DataRef:
    def __init__(self, node_id: Union[str, UUID], path_list: List[List[str]]):
        self.node_id = node_id
        self.path_list = path_list
