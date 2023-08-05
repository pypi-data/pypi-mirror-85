# -*- coding: utf-8 -*-

# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import warnings
from typing import Callable, Dict, Optional, Sequence, Tuple

from google.api_core import grpc_helpers  # type: ignore
from google.api_core import operations_v1  # type: ignore
from google.api_core import gapic_v1  # type: ignore
from google import auth  # type: ignore
from google.auth import credentials  # type: ignore
from google.auth.transport.grpc import SslCredentials  # type: ignore

import grpc  # type: ignore

from google.cloud.aiplatform_v1beta1.types import annotation_spec
from google.cloud.aiplatform_v1beta1.types import dataset
from google.cloud.aiplatform_v1beta1.types import dataset as gca_dataset
from google.cloud.aiplatform_v1beta1.types import dataset_service
from google.longrunning import operations_pb2 as operations  # type: ignore

from .base import DatasetServiceTransport, DEFAULT_CLIENT_INFO


class DatasetServiceGrpcTransport(DatasetServiceTransport):
    """gRPC backend transport for DatasetService.

    This class defines the same methods as the primary client, so the
    primary client can load the underlying transport implementation
    and call it.

    It sends protocol buffers over the wire using gRPC (which is built on
    top of HTTP/2); the ``grpcio`` package must be installed.
    """

    _stubs: Dict[str, Callable]

    def __init__(
        self,
        *,
        host: str = "aiplatform.googleapis.com",
        credentials: credentials.Credentials = None,
        credentials_file: str = None,
        scopes: Sequence[str] = None,
        channel: grpc.Channel = None,
        api_mtls_endpoint: str = None,
        client_cert_source: Callable[[], Tuple[bytes, bytes]] = None,
        ssl_channel_credentials: grpc.ChannelCredentials = None,
        quota_project_id: Optional[str] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
    ) -> None:
        """Instantiate the transport.

        Args:
            host (Optional[str]): The hostname to connect to.
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
                This argument is ignored if ``channel`` is provided.
            credentials_file (Optional[str]): A file with credentials that can
                be loaded with :func:`google.auth.load_credentials_from_file`.
                This argument is ignored if ``channel`` is provided.
            scopes (Optional(Sequence[str])): A list of scopes. This argument is
                ignored if ``channel`` is provided.
            channel (Optional[grpc.Channel]): A ``Channel`` instance through
                which to make calls.
            api_mtls_endpoint (Optional[str]): Deprecated. The mutual TLS endpoint.
                If provided, it overrides the ``host`` argument and tries to create
                a mutual TLS channel with client SSL credentials from
                ``client_cert_source`` or applicatin default SSL credentials.
            client_cert_source (Optional[Callable[[], Tuple[bytes, bytes]]]):
                Deprecated. A callback to provide client SSL certificate bytes and
                private key bytes, both in PEM format. It is ignored if
                ``api_mtls_endpoint`` is None.
            ssl_channel_credentials (grpc.ChannelCredentials): SSL credentials
                for grpc channel. It is ignored if ``channel`` is provided.
            quota_project_id (Optional[str]): An optional project to use for billing
                and quota.
            client_info (google.api_core.gapic_v1.client_info.ClientInfo):
                The client info used to send a user-agent string along with
                API requests. If ``None``, then default info will be used.
                Generally, you only need to set this if you're developing
                your own client library.

        Raises:
          google.auth.exceptions.MutualTLSChannelError: If mutual TLS transport
              creation failed for any reason.
          google.api_core.exceptions.DuplicateCredentialArgs: If both ``credentials``
              and ``credentials_file`` are passed.
        """
        self._ssl_channel_credentials = ssl_channel_credentials

        if channel:
            # Sanity check: Ensure that channel and credentials are not both
            # provided.
            credentials = False

            # If a channel was explicitly provided, set it.
            self._grpc_channel = channel
            self._ssl_channel_credentials = None
        elif api_mtls_endpoint:
            warnings.warn(
                "api_mtls_endpoint and client_cert_source are deprecated",
                DeprecationWarning,
            )

            host = (
                api_mtls_endpoint
                if ":" in api_mtls_endpoint
                else api_mtls_endpoint + ":443"
            )

            if credentials is None:
                credentials, _ = auth.default(
                    scopes=self.AUTH_SCOPES, quota_project_id=quota_project_id
                )

            # Create SSL credentials with client_cert_source or application
            # default SSL credentials.
            if client_cert_source:
                cert, key = client_cert_source()
                ssl_credentials = grpc.ssl_channel_credentials(
                    certificate_chain=cert, private_key=key
                )
            else:
                ssl_credentials = SslCredentials().ssl_credentials

            # create a new channel. The provided one is ignored.
            self._grpc_channel = type(self).create_channel(
                host,
                credentials=credentials,
                credentials_file=credentials_file,
                ssl_credentials=ssl_credentials,
                scopes=scopes or self.AUTH_SCOPES,
                quota_project_id=quota_project_id,
            )
            self._ssl_channel_credentials = ssl_credentials
        else:
            host = host if ":" in host else host + ":443"

            if credentials is None:
                credentials, _ = auth.default(
                    scopes=self.AUTH_SCOPES, quota_project_id=quota_project_id
                )

            # create a new channel. The provided one is ignored.
            self._grpc_channel = type(self).create_channel(
                host,
                credentials=credentials,
                credentials_file=credentials_file,
                ssl_credentials=ssl_channel_credentials,
                scopes=scopes or self.AUTH_SCOPES,
                quota_project_id=quota_project_id,
            )

        self._stubs = {}  # type: Dict[str, Callable]

        # Run the base constructor.
        super().__init__(
            host=host,
            credentials=credentials,
            credentials_file=credentials_file,
            scopes=scopes or self.AUTH_SCOPES,
            quota_project_id=quota_project_id,
            client_info=client_info,
        )

    @classmethod
    def create_channel(
        cls,
        host: str = "aiplatform.googleapis.com",
        credentials: credentials.Credentials = None,
        credentials_file: str = None,
        scopes: Optional[Sequence[str]] = None,
        quota_project_id: Optional[str] = None,
        **kwargs,
    ) -> grpc.Channel:
        """Create and return a gRPC channel object.
        Args:
            address (Optionsl[str]): The host for the channel to use.
            credentials (Optional[~.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify this application to the service. If
                none are specified, the client will attempt to ascertain
                the credentials from the environment.
            credentials_file (Optional[str]): A file with credentials that can
                be loaded with :func:`google.auth.load_credentials_from_file`.
                This argument is mutually exclusive with credentials.
            scopes (Optional[Sequence[str]]): A optional list of scopes needed for this
                service. These are only used when credentials are not specified and
                are passed to :func:`google.auth.default`.
            quota_project_id (Optional[str]): An optional project to use for billing
                and quota.
            kwargs (Optional[dict]): Keyword arguments, which are passed to the
                channel creation.
        Returns:
            grpc.Channel: A gRPC channel object.

        Raises:
            google.api_core.exceptions.DuplicateCredentialArgs: If both ``credentials``
              and ``credentials_file`` are passed.
        """
        scopes = scopes or cls.AUTH_SCOPES
        return grpc_helpers.create_channel(
            host,
            credentials=credentials,
            credentials_file=credentials_file,
            scopes=scopes,
            quota_project_id=quota_project_id,
            **kwargs,
        )

    @property
    def grpc_channel(self) -> grpc.Channel:
        """Return the channel designed to connect to this service.
        """
        return self._grpc_channel

    @property
    def operations_client(self) -> operations_v1.OperationsClient:
        """Create the client designed to process long-running operations.

        This property caches on the instance; repeated calls return the same
        client.
        """
        # Sanity check: Only create a new client if we do not already have one.
        if "operations_client" not in self.__dict__:
            self.__dict__["operations_client"] = operations_v1.OperationsClient(
                self.grpc_channel
            )

        # Return the client from cache.
        return self.__dict__["operations_client"]

    @property
    def create_dataset(
        self,
    ) -> Callable[[dataset_service.CreateDatasetRequest], operations.Operation]:
        r"""Return a callable for the create dataset method over gRPC.

        Creates a Dataset.

        Returns:
            Callable[[~.CreateDatasetRequest],
                    ~.Operation]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "create_dataset" not in self._stubs:
            self._stubs["create_dataset"] = self.grpc_channel.unary_unary(
                "/google.cloud.aiplatform.v1beta1.DatasetService/CreateDataset",
                request_serializer=dataset_service.CreateDatasetRequest.serialize,
                response_deserializer=operations.Operation.FromString,
            )
        return self._stubs["create_dataset"]

    @property
    def get_dataset(
        self,
    ) -> Callable[[dataset_service.GetDatasetRequest], dataset.Dataset]:
        r"""Return a callable for the get dataset method over gRPC.

        Gets a Dataset.

        Returns:
            Callable[[~.GetDatasetRequest],
                    ~.Dataset]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_dataset" not in self._stubs:
            self._stubs["get_dataset"] = self.grpc_channel.unary_unary(
                "/google.cloud.aiplatform.v1beta1.DatasetService/GetDataset",
                request_serializer=dataset_service.GetDatasetRequest.serialize,
                response_deserializer=dataset.Dataset.deserialize,
            )
        return self._stubs["get_dataset"]

    @property
    def update_dataset(
        self,
    ) -> Callable[[dataset_service.UpdateDatasetRequest], gca_dataset.Dataset]:
        r"""Return a callable for the update dataset method over gRPC.

        Updates a Dataset.

        Returns:
            Callable[[~.UpdateDatasetRequest],
                    ~.Dataset]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "update_dataset" not in self._stubs:
            self._stubs["update_dataset"] = self.grpc_channel.unary_unary(
                "/google.cloud.aiplatform.v1beta1.DatasetService/UpdateDataset",
                request_serializer=dataset_service.UpdateDatasetRequest.serialize,
                response_deserializer=gca_dataset.Dataset.deserialize,
            )
        return self._stubs["update_dataset"]

    @property
    def list_datasets(
        self,
    ) -> Callable[
        [dataset_service.ListDatasetsRequest], dataset_service.ListDatasetsResponse
    ]:
        r"""Return a callable for the list datasets method over gRPC.

        Lists Datasets in a Location.

        Returns:
            Callable[[~.ListDatasetsRequest],
                    ~.ListDatasetsResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_datasets" not in self._stubs:
            self._stubs["list_datasets"] = self.grpc_channel.unary_unary(
                "/google.cloud.aiplatform.v1beta1.DatasetService/ListDatasets",
                request_serializer=dataset_service.ListDatasetsRequest.serialize,
                response_deserializer=dataset_service.ListDatasetsResponse.deserialize,
            )
        return self._stubs["list_datasets"]

    @property
    def delete_dataset(
        self,
    ) -> Callable[[dataset_service.DeleteDatasetRequest], operations.Operation]:
        r"""Return a callable for the delete dataset method over gRPC.

        Deletes a Dataset.

        Returns:
            Callable[[~.DeleteDatasetRequest],
                    ~.Operation]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "delete_dataset" not in self._stubs:
            self._stubs["delete_dataset"] = self.grpc_channel.unary_unary(
                "/google.cloud.aiplatform.v1beta1.DatasetService/DeleteDataset",
                request_serializer=dataset_service.DeleteDatasetRequest.serialize,
                response_deserializer=operations.Operation.FromString,
            )
        return self._stubs["delete_dataset"]

    @property
    def import_data(
        self,
    ) -> Callable[[dataset_service.ImportDataRequest], operations.Operation]:
        r"""Return a callable for the import data method over gRPC.

        Imports data into a Dataset.

        Returns:
            Callable[[~.ImportDataRequest],
                    ~.Operation]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "import_data" not in self._stubs:
            self._stubs["import_data"] = self.grpc_channel.unary_unary(
                "/google.cloud.aiplatform.v1beta1.DatasetService/ImportData",
                request_serializer=dataset_service.ImportDataRequest.serialize,
                response_deserializer=operations.Operation.FromString,
            )
        return self._stubs["import_data"]

    @property
    def export_data(
        self,
    ) -> Callable[[dataset_service.ExportDataRequest], operations.Operation]:
        r"""Return a callable for the export data method over gRPC.

        Exports data from a Dataset.

        Returns:
            Callable[[~.ExportDataRequest],
                    ~.Operation]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "export_data" not in self._stubs:
            self._stubs["export_data"] = self.grpc_channel.unary_unary(
                "/google.cloud.aiplatform.v1beta1.DatasetService/ExportData",
                request_serializer=dataset_service.ExportDataRequest.serialize,
                response_deserializer=operations.Operation.FromString,
            )
        return self._stubs["export_data"]

    @property
    def list_data_items(
        self,
    ) -> Callable[
        [dataset_service.ListDataItemsRequest], dataset_service.ListDataItemsResponse
    ]:
        r"""Return a callable for the list data items method over gRPC.

        Lists DataItems in a Dataset.

        Returns:
            Callable[[~.ListDataItemsRequest],
                    ~.ListDataItemsResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_data_items" not in self._stubs:
            self._stubs["list_data_items"] = self.grpc_channel.unary_unary(
                "/google.cloud.aiplatform.v1beta1.DatasetService/ListDataItems",
                request_serializer=dataset_service.ListDataItemsRequest.serialize,
                response_deserializer=dataset_service.ListDataItemsResponse.deserialize,
            )
        return self._stubs["list_data_items"]

    @property
    def get_annotation_spec(
        self,
    ) -> Callable[
        [dataset_service.GetAnnotationSpecRequest], annotation_spec.AnnotationSpec
    ]:
        r"""Return a callable for the get annotation spec method over gRPC.

        Gets an AnnotationSpec.

        Returns:
            Callable[[~.GetAnnotationSpecRequest],
                    ~.AnnotationSpec]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_annotation_spec" not in self._stubs:
            self._stubs["get_annotation_spec"] = self.grpc_channel.unary_unary(
                "/google.cloud.aiplatform.v1beta1.DatasetService/GetAnnotationSpec",
                request_serializer=dataset_service.GetAnnotationSpecRequest.serialize,
                response_deserializer=annotation_spec.AnnotationSpec.deserialize,
            )
        return self._stubs["get_annotation_spec"]

    @property
    def list_annotations(
        self,
    ) -> Callable[
        [dataset_service.ListAnnotationsRequest],
        dataset_service.ListAnnotationsResponse,
    ]:
        r"""Return a callable for the list annotations method over gRPC.

        Lists Annotations belongs to a dataitem

        Returns:
            Callable[[~.ListAnnotationsRequest],
                    ~.ListAnnotationsResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_annotations" not in self._stubs:
            self._stubs["list_annotations"] = self.grpc_channel.unary_unary(
                "/google.cloud.aiplatform.v1beta1.DatasetService/ListAnnotations",
                request_serializer=dataset_service.ListAnnotationsRequest.serialize,
                response_deserializer=dataset_service.ListAnnotationsResponse.deserialize,
            )
        return self._stubs["list_annotations"]


__all__ = ("DatasetServiceGrpcTransport",)
