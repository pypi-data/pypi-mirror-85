"""
Implementation of the `Dataset` class.
"""
import pyrfc3339  # type: ignore

from datetime import datetime
from enum import Enum
from tusclient import client as tus_client  # type: ignore
from typing import Dict, Optional, Any, Iterator, Tuple, List, IO, Union

from .core import Connection
from .process import Process
from .user import User
from .type import ApiType, ApiQuery, ApiQueryOrder


class DatasetSource(Enum):
    GIT = "git"
    UPLOAD = "upload"
    LOCAL = "local"
    DOWNLOAD = "download"

    def __str__(self):
        return str(self.value)


class DatasetStatus(Enum):
    CREATED = "created"
    TRANSFERRED = "transferred"
    UNPACKED = "unpacked"
    VALIDATED = "validated"
    ARCHIVED = "archived"
    ERROR = "error"

    def __str__(self):
        return str(self.value)


class Dataset(ApiType['Dataset']):
    """The Dataset class contains information about datasets.

    ...
    Attributes:
    -----------
    identifier: str
        A unique identifier of the user (i.e. the username).
    name: str
        The full name of the user.
    status: str
        The current status of the user. Can be 'active' or 'archived'.
    """
    # TODO tutorial assumes we can pass directly the keyword i.e. id=ID
    def __init__(self, input: Dict[str, Any]) -> None:
        if "id" not in input:
            raise ValueError("Invalid input dictionary: It must contain an 'id' key.")

        # TODO Fix it robustly -> conceptually
        if input.get('user',None):
            if input['user']+"/" in input['id']:
                input['id'] = input['id'].split("/")[-1]

        super().__init__(input)

    @classmethod
    def create(
            cls,
            id: str,
            source: Optional[Union[str,DatasetSource]] = None,
            source_address: Optional[str] = None,
            name: Optional[str] = None,
            access_key: Optional[str] = None,
            description: Optional[str] = None) -> 'Dataset':
        init_dict: Dict[str, Any] = {"id": id}
        if source is not None:
            init_dict["source"] = str(source)
        if source_address is not None:
            init_dict["source-address"] = source_address
        if name is not None:
            init_dict["name"] = name
        if description is not None:
            init_dict["description"] = description
        # TODO Do not transfer access keys over plain connection
        if access_key is not None:
            init_dict["access-key"] = access_key
        return Dataset(init_dict)

    @classmethod
    def create_ref(cls, id: str) -> 'Dataset':
        return Dataset({"id": id})

    @property
    def id(self) -> str:
        return self._dict["id"]

    @property
    def user(self) -> Optional[User]:
        value = self._dict.get("user")
        return User({"id": value}) if value is not None else None

    # TODO BIG: should instances hold object e.g. user object or a user string and create user objects when queried
    # TODO NOT caught by the mipy
    @user.setter
    def user(self, value: Optional[str]):
        if value is not None:
            self._dict["user"] = value
        else:
            self._dict.pop("user")

    @property
    def name(self) -> Optional[str]:
        value = self._updates.get("name") or self._dict.get("name")
        return str(value) if value is not None else None

    @name.setter
    def name(self, value: Optional[str] = None) -> None:
        if value is not None:
            self._updates["name"] = value
        else:
            self._updates.pop("name")

    @property
    def description(self) -> Optional[str]:
        value = self._updates.get("description") or self._dict.get("description")
        return str(value) if value is not None else None

    @description.setter
    def description(self, value: Optional[str] = None) -> None:
        if value is not None:
            self._updates["description"] = value
        else:
            self._updates.pop("description")

    @property
    def schema_in(self) -> Optional[str]:
        value = self._dict.get("schema-in")
        return str(value) if value is not None else None

    @property
    def schema_out(self) -> Optional[str]:
        value = self._dict.get("schema-out")
        return str(value) if value is not None else None

    @property
    def source(self) -> Optional[DatasetSource]:
        value = self._dict.get("source")
        return DatasetSource(value) if value is not None else None

    @property
    def source_address(self) -> Optional[str]:
        value = self._dict.get("source-address")
        return str(value) if value is not None else None

    @property
    def creation_time(self) -> Optional[datetime]:
        value = self._dict.get("creation-time")
        return pyrfc3339.parse(value) if value is not None else None

    @property
    def status(self) -> Optional[DatasetStatus]:
        value = self._updates.get("status") or self._dict.get("status")
        return DatasetStatus(value) if value is not None else None

    @status.setter
    def status(self, value: Optional[DatasetStatus] = None) -> None:
        if value is not None:
            self._updates["status"] = value.value
        else:
            self._updates.pop("status")

    @property
    def status_message(self) -> Optional[str]:
        value = self._dict.get("status-message")
        return str(value) if value is not None else None

    @property
    def process(self) -> Optional[Process]:
        value = self._dict.get("process")
        return Process({"id": value}) if value is not None else None

    def __iter__(self) -> Iterator[Tuple[str, Any]]:
        for (k, v) in self._dict.items():
            yield (k, v)

    def post(self, connection: Connection) -> 'Dataset':
        url = connection.url("datasets")
        return self._post(connection, url)

    def patch(self, connection: Connection) -> 'Dataset':
        if not self.user:
            self.user = connection.user_id
        url = connection.url("datasets/{}/{}".format(self.user.id, self.id))
        return self._patch(connection, url)

    def get(self, connection: Connection) -> 'Dataset':
        if not self.user:
            self.user = connection.user_id
        url = connection.url("datasets/{}/{}".format(self.user.id, self.id))
        return self._get(connection, url)

    def upload(self, connection: Connection, data: IO, file_name: Optional[str] = None) -> None:
        if not self.user:
            self.user = connection.user_id
        url = connection.url("datasets/{}/{}/upload".format(self.user.id, self.id))
        metadata = {"filename": file_name} if file_name is not None else None

        # Initialize the client for the TUS upload protocol. Apply the authentication header.
        client = tus_client.TusClient(url)
        connection.auth(client)

        uploader = client.uploader(file_stream=data, chunk_size=201800, metadata=metadata)
        uploader.upload()

    def get_dataset(self, connection: Connection) -> bytes:
        # TODO FIX ID
        if not self.user:
            self.user = connection.user_id
        if self.user.id in self.id:
            id = self.id.split("/")[-1]
        else:
            id = self.id

        url = connection.url("datasets/{}/{}/data.tar".format(self.user.id, id))
        return self._download(connection, url)


class DatasetQuery(ApiQuery['Dataset', 'DatasetQuery']):

    VALID_SORTING_FIELDS = ["id", "user", "source", "source-address", "creation-time", "status"]

    def __init__(self, id: Optional[List[str]] = None, user: Optional[Union[str,User]] = None,
                 status: Optional[Union[str,DatasetStatus]] = None, source: Optional[Union[str,DatasetSource]] = None,
                 source_address: Optional[str] = None,
                 schema_in: Optional[str] = None, schema_out: Optional[str] = None,                 
                 order_by: Optional[str] = None, order: Optional[Union[str,ApiQueryOrder]] = None,
                 limit: Optional[int] = None, cursor: Optional[str] = None) -> None:
        super().__init__(order_by, order, limit, cursor)
        self.T = Dataset

        if id is not None:
            self._query["id"] = id
        if user is not None:
            self._query["user"] = str(user)
        if status is not None:
            self._query["status"] = str(status)
        if source is not None:
            self._query["source"] = str(source)
        if source_address is not None:
            self._query["source-address"] = source_address
        if schema_in is not None:
            self._query["schema-in"] = schema_in
        if schema_out is not None:
            self._query["schema-out"] = schema_out

    def run(self, connection: Connection) -> Tuple[List[Dataset], Optional['DatasetQuery']]:
        url = connection.url("datasets")
        return self._run(connection, url)
