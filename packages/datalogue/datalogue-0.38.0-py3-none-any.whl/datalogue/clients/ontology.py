from typing import Optional, Union, List, Callable
from datalogue.clients.http import _HttpClient, HttpMethod, MultiPartData, MultiPartFile
from datalogue.models.ontology import Ontology, OntologyNode, TrainingDataColumn
from datalogue.models.scope_level import Scope
from datalogue.models.permission import OntologyPermission
from datalogue.dtl_utils import _parse_list, _parse_uuid
from datalogue.errors import DtlError
from uuid import UUID
import itertools


class _OntologyClient:
    """
    Client to interact with the ontology
    """

    def __init__(self, http_client: _HttpClient):
        self.http_client = http_client
        self.service_uri = "/yggy"

    def create(self, ontology: Ontology) -> Union[DtlError, Ontology]:
        """
        Create :class:`Ontology` object given ontology object
        :return: :class:`Ontology` object, else returns :class:`DtlError`
        """
        res = self.http_client.make_authed_request(self.service_uri + '/ontology/import', HttpMethod.POST, body=Ontology._as_payload(ontology))

        if isinstance(res, DtlError):
            return res
            
        return Ontology._from_payload(res)
    
    def get(self, ontology_id: UUID) -> Union[DtlError, Ontology]:
        """
        Get :class:`Ontology` object given ontology_id
        :return: :class:`Ontology` object, else returns :class:`DtlError`
        """
        res = self.http_client.make_authed_request(self.service_uri + f'/ontology/{str(ontology_id)}', HttpMethod.GET)

        if isinstance(res, DtlError):
            return res
        
        ontology = Ontology._from_payload(res)
        updated_tree = []

        updated_tree = list(map(lambda c: self.__iterate_over_tree(c, self.__update_training_data_info), ontology.tree))        
        return Ontology(ontology.name, ontology.description, updated_tree, ontology.id)

    """
    Upload a csv data dictionary as a data model, with optional source & destinations mappings at the class level. 
    Classes may be duplicated to demonstrate multiple source or destination mappings
    Supported csv header: 
    class,description,source,source_field,destination,destination_field
    """
    def import_model(self, ontology_id: Union[str, UUID], path: str) -> Union[DtlError, Ontology]:
        """
        :param ontology_id: id of the data model to be populated via the uploaded dictionary
        :param path: local path to the data dictionary csv
        :return: The updated Ontology if successful, else returns :class:`DtlError`
        """
        ontology_id = _parse_uuid(ontology_id)
        with open(path, 'rb') as f:
            files = [MultiPartFile("ontology", f)]

            data = [
                MultiPartData("params", "{}"),
            ]

            res = self.http_client.post_multipart_data(
                self.service_uri + "/ontology/" + str(ontology_id) + "/import",
                files, data
            )

            return Ontology._from_payload(res)


    def update(self, ontology_id: UUID, updated_ontology: Ontology) -> Union[DtlError, Ontology]:
        """
        Update :class:`Ontology` method that will replace the existing ontology.
        The structure of this ontology will replace the existing structure. Please make sure you include a full
        ontological structure and not just the changes/modifications
        :param ontology_id: UUID is the id of the ontology that you want to replace/modify/update.
        :param updated_ontology: Ontology object that will replace the existing ontology.
        :return: The updated Ontology if successful, else returns :class:`DtlError`
        """
        res = self.http_client.make_authed_request(self.service_uri + f'/ontology/{str(ontology_id)}', HttpMethod.PUT, body=Ontology._as_payload(updated_ontology))

        if isinstance(res, DtlError):
            return res

        return Ontology._from_payload(res)

    def delete(self, ontology_id: UUID) -> Union[DtlError, bool]:
        """
        Delete :class:`Ontology` based on the given ontology_id
        :return: True if successful, else returns :class:`DtlError`
        """
        res = self.http_client.make_authed_request(self.service_uri + f'/ontology/{str(ontology_id)}', HttpMethod.DELETE)
        if isinstance(res, DtlError):
            return res
        else:
            return True

    def get_class(self, class_id: UUID) -> Union[DtlError, OntologyNode]:
        """
        Retrieve an ontological class locally/ a class is represented as an OntologyNode object

        :param class_id: id of the ontological class to retrieve
        :return: the OntologyNode object corresponding to the id
        """
        res = self.http_client.make_authed_request(f"/yggy/entity/{class_id}", HttpMethod.GET)
        if isinstance(res, DtlError):
            return res

        ontology_node = OntologyNode.from_payload(res)

        ontology_with_numbers = self.__update_training_data_info(ontology_node)
        return ontology_with_numbers

    def share(self, ontology_id: UUID, target_id: UUID, target_type: Scope, permission: OntologyPermission) -> Union[DtlError, bool]:
        """
        Share the given ontology with an specific user or group with the desired permission (Write or Read)

        :param ontology_id: UUID is the id of the ontology that you want to share
        :param target_id: UUID is the id of the User the Group or Organization you want to share with (depending on the target_type param)
        :param target_type: Scope (`Group`, `User` or `Organization`) with whom you want to share the ontology. It can be a User, Group or Organization.
        :param permission: OntologyPermission (`Write` or `Read`) the permission you want to grant
        :return: True if successful, else returns :class:`DtlError`
        """

        body = Ontology._create_body_for_sharing(target_id, target_type, permission)
        if isinstance(body, DtlError):
            return body

        res = self.http_client.make_authed_request(self.service_uri + f'/ontology/{str(ontology_id)}/share', HttpMethod.POST, body)
        if isinstance(res, DtlError):
            return res
        else:
            return True

    def unshare(self, ontology_id: UUID, target_id: UUID, target_type: Scope) -> Union[DtlError, bool]:
        """
        Unshare the given ontology from an specific user or group. That User/Group won't be able to access that ontology
        any more.

        :param ontology_id: UUID is the id of the ontology that you want to unshare
        :param target_id: UUID is the id of the User, the Group or Organization you want to unshare from (depending on the target_type param)
        :param target_type: Scope (`Group`, `User` or `Organization`) with whom you want to unshare the ontology. It can be a User, Group or Organization.
        :return: True if successful, else returns :class:`DtlError`
        """
        body = Ontology._create_body_for_unsharing(target_id, target_type, 'None')

        if isinstance(body, DtlError):
            return body

        res = self.http_client.make_authed_request(self.service_uri + f'/ontology/{str(ontology_id)}/share',
                                                   HttpMethod.POST, body)
        if isinstance(res, DtlError):
            return res
        else:
            return True

    def list(self, page: int = 1, item_per_page: int = 25) -> Union[DtlError, List[Ontology]]:
        """
        List the ontologies

        :param page: page to be retrieved
        :param item_per_page: number of ontologies to be put in a page
        :return: Returns a List of all the available Ontologies or an error message as a string

        """
        res = self.http_client.make_authed_request(
            self.service_uri + f'/ontologies?page={page}&size={item_per_page}', HttpMethod.GET)

        if isinstance(res, DtlError):
            return res

        return _parse_list(Ontology._from_payload)(res)

    def overwrite(self, ontology_id: UUID, ontology: Ontology) -> Union[DtlError, Ontology]:
        """
        It overwrites all ontology and node information for the given ontology id including training data if there is an ontology for the given id. 
        Otherwise, it creates brand new ontology with the given ontology id
        :return: :class:`Ontology` object, else returns :class:`DtlError`
        """
        res = self.http_client.make_authed_request(self.service_uri + f'/ontology/{ontology_id}/import', HttpMethod.PUT, body=Ontology._as_payload(ontology))

        if isinstance(res, DtlError):
            return res
            
        return Ontology._from_payload(res)

    ####### Internal functions
    def __iterate_over_tree(self, current_node: OntologyNode, f: Callable[[OntologyNode], OntologyNode]) -> OntologyNode:
        if not current_node.children:
            updated_node = f(current_node)
            return updated_node
        else:
            updated_children = list(map(lambda c: self.__iterate_over_tree(c, f), current_node.children))
            updated_node = f(current_node)
            updated_node.children = updated_children
            return updated_node

    def __update_training_data_info(self, node: OntologyNode) -> OntologyNode:
        if len(node.children) > 0:
            return node
        else:
            dataset_ids = self.__get_node_dataset_ids(node.id)
            training_data_columns = []
            total_count = 0
            if len(dataset_ids) > 0:
                training_data_columns = self.__get_training_data_statistics(node.id, dataset_ids)
                for training_data_column in training_data_columns:
                    total_count += training_data_column.count
        
            updated_node = OntologyNode(
                node.name, 
                node.description, 
                [],
                node.id, 
                total_count, 
                training_data_columns)
            
            return updated_node

    def __get_training_data_statistics(self, node_id: UUID, dataset_ids: List[str]) -> Union[DtlError, List[TrainingDataColumn]]:
        res = self.http_client.make_authed_request("/themis/get-datasets", HttpMethod.POST, body=dataset_ids)
        if isinstance(res, DtlError):
            return res
        else:
            training_data_columns = []
            for r in res:
                path_response = self.__get_node_path(node_id, r.get("id"))
                if isinstance(path_response, DtlError):
                    return res
                else:
                    statistics = r.get("statistics")
                    if path_response != [] and statistics is not None and statistics.get("totalEntries") is not None:
                        training_data_columns.append({"count": statistics.get(
                            "totalEntries"), "path": path_response, "datastore_name": r.get("title")}) # TODO datastore_id should be updated

            return _parse_list(TrainingDataColumn._from_payload)(training_data_columns)

    def __get_node_dataset_ids(self, node_id: UUID) -> List[str]:
        entity_res = self.http_client.make_authed_request(f"/yggy/entity/{node_id}", HttpMethod.GET)
        training_data_list = entity_res.get("trainingDataInfo")
        if training_data_list is None:
            training_data_list = []

        dataset_ids = []
        for trainingData in training_data_list:
            dataset_ids.append(trainingData["datasetId"])

        return dataset_ids

    def __get_node_path(self, node_id: UUID, dataset_id: str) -> List[str]:
        entity_res = self.http_client.make_authed_request(f"/yggy/entity/{node_id}", HttpMethod.GET)
        training_data_list = entity_res.get("trainingDataInfo")
        if training_data_list is None:
            training_data_list = []

        path = []
        for trainingData in training_data_list:
            if dataset_id == trainingData.get("datasetId"):
                path = trainingData.get("nodePath")

        return path
