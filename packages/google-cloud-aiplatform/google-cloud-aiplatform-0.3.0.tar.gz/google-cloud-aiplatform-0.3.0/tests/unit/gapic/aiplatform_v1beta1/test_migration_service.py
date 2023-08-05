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

import os
import mock

import grpc
from grpc.experimental import aio
import math
import pytest
from proto.marshal.rules.dates import DurationRule, TimestampRule

from google import auth
from google.api_core import client_options
from google.api_core import exceptions
from google.api_core import future
from google.api_core import gapic_v1
from google.api_core import grpc_helpers
from google.api_core import grpc_helpers_async
from google.api_core import operation_async  # type: ignore
from google.api_core import operations_v1
from google.auth import credentials
from google.auth.exceptions import MutualTLSChannelError
from google.cloud.aiplatform_v1beta1.services.migration_service import (
    MigrationServiceAsyncClient,
)
from google.cloud.aiplatform_v1beta1.services.migration_service import (
    MigrationServiceClient,
)
from google.cloud.aiplatform_v1beta1.services.migration_service import pagers
from google.cloud.aiplatform_v1beta1.services.migration_service import transports
from google.cloud.aiplatform_v1beta1.types import migratable_resource
from google.cloud.aiplatform_v1beta1.types import migration_service
from google.longrunning import operations_pb2
from google.oauth2 import service_account


def client_cert_source_callback():
    return b"cert bytes", b"key bytes"


# If default endpoint is localhost, then default mtls endpoint will be the same.
# This method modifies the default endpoint so the client can produce a different
# mtls endpoint for endpoint testing purposes.
def modify_default_endpoint(client):
    return (
        "foo.googleapis.com"
        if ("localhost" in client.DEFAULT_ENDPOINT)
        else client.DEFAULT_ENDPOINT
    )


def test__get_default_mtls_endpoint():
    api_endpoint = "example.googleapis.com"
    api_mtls_endpoint = "example.mtls.googleapis.com"
    sandbox_endpoint = "example.sandbox.googleapis.com"
    sandbox_mtls_endpoint = "example.mtls.sandbox.googleapis.com"
    non_googleapi = "api.example.com"

    assert MigrationServiceClient._get_default_mtls_endpoint(None) is None
    assert (
        MigrationServiceClient._get_default_mtls_endpoint(api_endpoint)
        == api_mtls_endpoint
    )
    assert (
        MigrationServiceClient._get_default_mtls_endpoint(api_mtls_endpoint)
        == api_mtls_endpoint
    )
    assert (
        MigrationServiceClient._get_default_mtls_endpoint(sandbox_endpoint)
        == sandbox_mtls_endpoint
    )
    assert (
        MigrationServiceClient._get_default_mtls_endpoint(sandbox_mtls_endpoint)
        == sandbox_mtls_endpoint
    )
    assert (
        MigrationServiceClient._get_default_mtls_endpoint(non_googleapi)
        == non_googleapi
    )


@pytest.mark.parametrize(
    "client_class", [MigrationServiceClient, MigrationServiceAsyncClient]
)
def test_migration_service_client_from_service_account_file(client_class):
    creds = credentials.AnonymousCredentials()
    with mock.patch.object(
        service_account.Credentials, "from_service_account_file"
    ) as factory:
        factory.return_value = creds
        client = client_class.from_service_account_file("dummy/file/path.json")
        assert client.transport._credentials == creds

        client = client_class.from_service_account_json("dummy/file/path.json")
        assert client.transport._credentials == creds

        assert client.transport._host == "aiplatform.googleapis.com:443"


def test_migration_service_client_get_transport_class():
    transport = MigrationServiceClient.get_transport_class()
    assert transport == transports.MigrationServiceGrpcTransport

    transport = MigrationServiceClient.get_transport_class("grpc")
    assert transport == transports.MigrationServiceGrpcTransport


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name",
    [
        (MigrationServiceClient, transports.MigrationServiceGrpcTransport, "grpc"),
        (
            MigrationServiceAsyncClient,
            transports.MigrationServiceGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
    ],
)
@mock.patch.object(
    MigrationServiceClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(MigrationServiceClient),
)
@mock.patch.object(
    MigrationServiceAsyncClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(MigrationServiceAsyncClient),
)
def test_migration_service_client_client_options(
    client_class, transport_class, transport_name
):
    # Check that if channel is provided we won't create a new one.
    with mock.patch.object(MigrationServiceClient, "get_transport_class") as gtc:
        transport = transport_class(credentials=credentials.AnonymousCredentials())
        client = client_class(transport=transport)
        gtc.assert_not_called()

    # Check that if channel is provided via str we will create a new one.
    with mock.patch.object(MigrationServiceClient, "get_transport_class") as gtc:
        client = client_class(transport=transport_name)
        gtc.assert_called()

    # Check the case api_endpoint is provided.
    options = client_options.ClientOptions(api_endpoint="squid.clam.whelk")
    with mock.patch.object(transport_class, "__init__") as patched:
        patched.return_value = None
        client = client_class(client_options=options)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file=None,
            host="squid.clam.whelk",
            scopes=None,
            ssl_channel_credentials=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
        )

    # Check the case api_endpoint is not provided and GOOGLE_API_USE_MTLS_ENDPOINT is
    # "never".
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "never"}):
        with mock.patch.object(transport_class, "__init__") as patched:
            patched.return_value = None
            client = client_class()
            patched.assert_called_once_with(
                credentials=None,
                credentials_file=None,
                host=client.DEFAULT_ENDPOINT,
                scopes=None,
                ssl_channel_credentials=None,
                quota_project_id=None,
                client_info=transports.base.DEFAULT_CLIENT_INFO,
            )

    # Check the case api_endpoint is not provided and GOOGLE_API_USE_MTLS_ENDPOINT is
    # "always".
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "always"}):
        with mock.patch.object(transport_class, "__init__") as patched:
            patched.return_value = None
            client = client_class()
            patched.assert_called_once_with(
                credentials=None,
                credentials_file=None,
                host=client.DEFAULT_MTLS_ENDPOINT,
                scopes=None,
                ssl_channel_credentials=None,
                quota_project_id=None,
                client_info=transports.base.DEFAULT_CLIENT_INFO,
            )

    # Check the case api_endpoint is not provided and GOOGLE_API_USE_MTLS_ENDPOINT has
    # unsupported value.
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "Unsupported"}):
        with pytest.raises(MutualTLSChannelError):
            client = client_class()

    # Check the case GOOGLE_API_USE_CLIENT_CERTIFICATE has unsupported value.
    with mock.patch.dict(
        os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "Unsupported"}
    ):
        with pytest.raises(ValueError):
            client = client_class()

    # Check the case quota_project_id is provided
    options = client_options.ClientOptions(quota_project_id="octopus")
    with mock.patch.object(transport_class, "__init__") as patched:
        patched.return_value = None
        client = client_class(client_options=options)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file=None,
            host=client.DEFAULT_ENDPOINT,
            scopes=None,
            ssl_channel_credentials=None,
            quota_project_id="octopus",
            client_info=transports.base.DEFAULT_CLIENT_INFO,
        )


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name,use_client_cert_env",
    [
        (
            MigrationServiceClient,
            transports.MigrationServiceGrpcTransport,
            "grpc",
            "true",
        ),
        (
            MigrationServiceAsyncClient,
            transports.MigrationServiceGrpcAsyncIOTransport,
            "grpc_asyncio",
            "true",
        ),
        (
            MigrationServiceClient,
            transports.MigrationServiceGrpcTransport,
            "grpc",
            "false",
        ),
        (
            MigrationServiceAsyncClient,
            transports.MigrationServiceGrpcAsyncIOTransport,
            "grpc_asyncio",
            "false",
        ),
    ],
)
@mock.patch.object(
    MigrationServiceClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(MigrationServiceClient),
)
@mock.patch.object(
    MigrationServiceAsyncClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(MigrationServiceAsyncClient),
)
@mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "auto"})
def test_migration_service_client_mtls_env_auto(
    client_class, transport_class, transport_name, use_client_cert_env
):
    # This tests the endpoint autoswitch behavior. Endpoint is autoswitched to the default
    # mtls endpoint, if GOOGLE_API_USE_CLIENT_CERTIFICATE is "true" and client cert exists.

    # Check the case client_cert_source is provided. Whether client cert is used depends on
    # GOOGLE_API_USE_CLIENT_CERTIFICATE value.
    with mock.patch.dict(
        os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": use_client_cert_env}
    ):
        options = client_options.ClientOptions(
            client_cert_source=client_cert_source_callback
        )
        with mock.patch.object(transport_class, "__init__") as patched:
            ssl_channel_creds = mock.Mock()
            with mock.patch(
                "grpc.ssl_channel_credentials", return_value=ssl_channel_creds
            ):
                patched.return_value = None
                client = client_class(client_options=options)

                if use_client_cert_env == "false":
                    expected_ssl_channel_creds = None
                    expected_host = client.DEFAULT_ENDPOINT
                else:
                    expected_ssl_channel_creds = ssl_channel_creds
                    expected_host = client.DEFAULT_MTLS_ENDPOINT

                patched.assert_called_once_with(
                    credentials=None,
                    credentials_file=None,
                    host=expected_host,
                    scopes=None,
                    ssl_channel_credentials=expected_ssl_channel_creds,
                    quota_project_id=None,
                    client_info=transports.base.DEFAULT_CLIENT_INFO,
                )

    # Check the case ADC client cert is provided. Whether client cert is used depends on
    # GOOGLE_API_USE_CLIENT_CERTIFICATE value.
    with mock.patch.dict(
        os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": use_client_cert_env}
    ):
        with mock.patch.object(transport_class, "__init__") as patched:
            with mock.patch(
                "google.auth.transport.grpc.SslCredentials.__init__", return_value=None
            ):
                with mock.patch(
                    "google.auth.transport.grpc.SslCredentials.is_mtls",
                    new_callable=mock.PropertyMock,
                ) as is_mtls_mock:
                    with mock.patch(
                        "google.auth.transport.grpc.SslCredentials.ssl_credentials",
                        new_callable=mock.PropertyMock,
                    ) as ssl_credentials_mock:
                        if use_client_cert_env == "false":
                            is_mtls_mock.return_value = False
                            ssl_credentials_mock.return_value = None
                            expected_host = client.DEFAULT_ENDPOINT
                            expected_ssl_channel_creds = None
                        else:
                            is_mtls_mock.return_value = True
                            ssl_credentials_mock.return_value = mock.Mock()
                            expected_host = client.DEFAULT_MTLS_ENDPOINT
                            expected_ssl_channel_creds = (
                                ssl_credentials_mock.return_value
                            )

                        patched.return_value = None
                        client = client_class()
                        patched.assert_called_once_with(
                            credentials=None,
                            credentials_file=None,
                            host=expected_host,
                            scopes=None,
                            ssl_channel_credentials=expected_ssl_channel_creds,
                            quota_project_id=None,
                            client_info=transports.base.DEFAULT_CLIENT_INFO,
                        )

    # Check the case client_cert_source and ADC client cert are not provided.
    with mock.patch.dict(
        os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": use_client_cert_env}
    ):
        with mock.patch.object(transport_class, "__init__") as patched:
            with mock.patch(
                "google.auth.transport.grpc.SslCredentials.__init__", return_value=None
            ):
                with mock.patch(
                    "google.auth.transport.grpc.SslCredentials.is_mtls",
                    new_callable=mock.PropertyMock,
                ) as is_mtls_mock:
                    is_mtls_mock.return_value = False
                    patched.return_value = None
                    client = client_class()
                    patched.assert_called_once_with(
                        credentials=None,
                        credentials_file=None,
                        host=client.DEFAULT_ENDPOINT,
                        scopes=None,
                        ssl_channel_credentials=None,
                        quota_project_id=None,
                        client_info=transports.base.DEFAULT_CLIENT_INFO,
                    )


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name",
    [
        (MigrationServiceClient, transports.MigrationServiceGrpcTransport, "grpc"),
        (
            MigrationServiceAsyncClient,
            transports.MigrationServiceGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
    ],
)
def test_migration_service_client_client_options_scopes(
    client_class, transport_class, transport_name
):
    # Check the case scopes are provided.
    options = client_options.ClientOptions(scopes=["1", "2"],)
    with mock.patch.object(transport_class, "__init__") as patched:
        patched.return_value = None
        client = client_class(client_options=options)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file=None,
            host=client.DEFAULT_ENDPOINT,
            scopes=["1", "2"],
            ssl_channel_credentials=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
        )


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name",
    [
        (MigrationServiceClient, transports.MigrationServiceGrpcTransport, "grpc"),
        (
            MigrationServiceAsyncClient,
            transports.MigrationServiceGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
    ],
)
def test_migration_service_client_client_options_credentials_file(
    client_class, transport_class, transport_name
):
    # Check the case credentials file is provided.
    options = client_options.ClientOptions(credentials_file="credentials.json")
    with mock.patch.object(transport_class, "__init__") as patched:
        patched.return_value = None
        client = client_class(client_options=options)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file="credentials.json",
            host=client.DEFAULT_ENDPOINT,
            scopes=None,
            ssl_channel_credentials=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
        )


def test_migration_service_client_client_options_from_dict():
    with mock.patch(
        "google.cloud.aiplatform_v1beta1.services.migration_service.transports.MigrationServiceGrpcTransport.__init__"
    ) as grpc_transport:
        grpc_transport.return_value = None
        client = MigrationServiceClient(
            client_options={"api_endpoint": "squid.clam.whelk"}
        )
        grpc_transport.assert_called_once_with(
            credentials=None,
            credentials_file=None,
            host="squid.clam.whelk",
            scopes=None,
            ssl_channel_credentials=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
        )


def test_search_migratable_resources(
    transport: str = "grpc",
    request_type=migration_service.SearchMigratableResourcesRequest,
):
    client = MigrationServiceClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.search_migratable_resources), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = migration_service.SearchMigratableResourcesResponse(
            next_page_token="next_page_token_value",
        )

        response = client.search_migratable_resources(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == migration_service.SearchMigratableResourcesRequest()

    # Establish that the response is the type that we expect.

    assert isinstance(response, pagers.SearchMigratableResourcesPager)

    assert response.next_page_token == "next_page_token_value"


def test_search_migratable_resources_from_dict():
    test_search_migratable_resources(request_type=dict)


@pytest.mark.asyncio
async def test_search_migratable_resources_async(
    transport: str = "grpc_asyncio",
    request_type=migration_service.SearchMigratableResourcesRequest,
):
    client = MigrationServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.search_migratable_resources), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            migration_service.SearchMigratableResourcesResponse(
                next_page_token="next_page_token_value",
            )
        )

        response = await client.search_migratable_resources(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == migration_service.SearchMigratableResourcesRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.SearchMigratableResourcesAsyncPager)

    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_search_migratable_resources_async_from_dict():
    await test_search_migratable_resources_async(request_type=dict)


def test_search_migratable_resources_field_headers():
    client = MigrationServiceClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = migration_service.SearchMigratableResourcesRequest()
    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.search_migratable_resources), "__call__"
    ) as call:
        call.return_value = migration_service.SearchMigratableResourcesResponse()

        client.search_migratable_resources(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_search_migratable_resources_field_headers_async():
    client = MigrationServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = migration_service.SearchMigratableResourcesRequest()
    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.search_migratable_resources), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            migration_service.SearchMigratableResourcesResponse()
        )

        await client.search_migratable_resources(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


def test_search_migratable_resources_flattened():
    client = MigrationServiceClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.search_migratable_resources), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = migration_service.SearchMigratableResourcesResponse()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.search_migratable_resources(parent="parent_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].parent == "parent_value"


def test_search_migratable_resources_flattened_error():
    client = MigrationServiceClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.search_migratable_resources(
            migration_service.SearchMigratableResourcesRequest(), parent="parent_value",
        )


@pytest.mark.asyncio
async def test_search_migratable_resources_flattened_async():
    client = MigrationServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.search_migratable_resources), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = migration_service.SearchMigratableResourcesResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            migration_service.SearchMigratableResourcesResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.search_migratable_resources(parent="parent_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].parent == "parent_value"


@pytest.mark.asyncio
async def test_search_migratable_resources_flattened_error_async():
    client = MigrationServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.search_migratable_resources(
            migration_service.SearchMigratableResourcesRequest(), parent="parent_value",
        )


def test_search_migratable_resources_pager():
    client = MigrationServiceClient(credentials=credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.search_migratable_resources), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            migration_service.SearchMigratableResourcesResponse(
                migratable_resources=[
                    migratable_resource.MigratableResource(),
                    migratable_resource.MigratableResource(),
                    migratable_resource.MigratableResource(),
                ],
                next_page_token="abc",
            ),
            migration_service.SearchMigratableResourcesResponse(
                migratable_resources=[], next_page_token="def",
            ),
            migration_service.SearchMigratableResourcesResponse(
                migratable_resources=[migratable_resource.MigratableResource(),],
                next_page_token="ghi",
            ),
            migration_service.SearchMigratableResourcesResponse(
                migratable_resources=[
                    migratable_resource.MigratableResource(),
                    migratable_resource.MigratableResource(),
                ],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", ""),)),
        )
        pager = client.search_migratable_resources(request={})

        assert pager._metadata == metadata

        results = [i for i in pager]
        assert len(results) == 6
        assert all(
            isinstance(i, migratable_resource.MigratableResource) for i in results
        )


def test_search_migratable_resources_pages():
    client = MigrationServiceClient(credentials=credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.search_migratable_resources), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            migration_service.SearchMigratableResourcesResponse(
                migratable_resources=[
                    migratable_resource.MigratableResource(),
                    migratable_resource.MigratableResource(),
                    migratable_resource.MigratableResource(),
                ],
                next_page_token="abc",
            ),
            migration_service.SearchMigratableResourcesResponse(
                migratable_resources=[], next_page_token="def",
            ),
            migration_service.SearchMigratableResourcesResponse(
                migratable_resources=[migratable_resource.MigratableResource(),],
                next_page_token="ghi",
            ),
            migration_service.SearchMigratableResourcesResponse(
                migratable_resources=[
                    migratable_resource.MigratableResource(),
                    migratable_resource.MigratableResource(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.search_migratable_resources(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_search_migratable_resources_async_pager():
    client = MigrationServiceAsyncClient(credentials=credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.search_migratable_resources),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            migration_service.SearchMigratableResourcesResponse(
                migratable_resources=[
                    migratable_resource.MigratableResource(),
                    migratable_resource.MigratableResource(),
                    migratable_resource.MigratableResource(),
                ],
                next_page_token="abc",
            ),
            migration_service.SearchMigratableResourcesResponse(
                migratable_resources=[], next_page_token="def",
            ),
            migration_service.SearchMigratableResourcesResponse(
                migratable_resources=[migratable_resource.MigratableResource(),],
                next_page_token="ghi",
            ),
            migration_service.SearchMigratableResourcesResponse(
                migratable_resources=[
                    migratable_resource.MigratableResource(),
                    migratable_resource.MigratableResource(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.search_migratable_resources(request={},)
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:
            responses.append(response)

        assert len(responses) == 6
        assert all(
            isinstance(i, migratable_resource.MigratableResource) for i in responses
        )


@pytest.mark.asyncio
async def test_search_migratable_resources_async_pages():
    client = MigrationServiceAsyncClient(credentials=credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.search_migratable_resources),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            migration_service.SearchMigratableResourcesResponse(
                migratable_resources=[
                    migratable_resource.MigratableResource(),
                    migratable_resource.MigratableResource(),
                    migratable_resource.MigratableResource(),
                ],
                next_page_token="abc",
            ),
            migration_service.SearchMigratableResourcesResponse(
                migratable_resources=[], next_page_token="def",
            ),
            migration_service.SearchMigratableResourcesResponse(
                migratable_resources=[migratable_resource.MigratableResource(),],
                next_page_token="ghi",
            ),
            migration_service.SearchMigratableResourcesResponse(
                migratable_resources=[
                    migratable_resource.MigratableResource(),
                    migratable_resource.MigratableResource(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        async for page_ in (await client.search_migratable_resources(request={})).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


def test_batch_migrate_resources(
    transport: str = "grpc", request_type=migration_service.BatchMigrateResourcesRequest
):
    client = MigrationServiceClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.batch_migrate_resources), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")

        response = client.batch_migrate_resources(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == migration_service.BatchMigrateResourcesRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_batch_migrate_resources_from_dict():
    test_batch_migrate_resources(request_type=dict)


@pytest.mark.asyncio
async def test_batch_migrate_resources_async(
    transport: str = "grpc_asyncio",
    request_type=migration_service.BatchMigrateResourcesRequest,
):
    client = MigrationServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.batch_migrate_resources), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )

        response = await client.batch_migrate_resources(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == migration_service.BatchMigrateResourcesRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_batch_migrate_resources_async_from_dict():
    await test_batch_migrate_resources_async(request_type=dict)


def test_batch_migrate_resources_field_headers():
    client = MigrationServiceClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = migration_service.BatchMigrateResourcesRequest()
    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.batch_migrate_resources), "__call__"
    ) as call:
        call.return_value = operations_pb2.Operation(name="operations/op")

        client.batch_migrate_resources(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_batch_migrate_resources_field_headers_async():
    client = MigrationServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = migration_service.BatchMigrateResourcesRequest()
    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.batch_migrate_resources), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )

        await client.batch_migrate_resources(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


def test_batch_migrate_resources_flattened():
    client = MigrationServiceClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.batch_migrate_resources), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.batch_migrate_resources(
            parent="parent_value",
            migrate_resource_requests=[
                migration_service.MigrateResourceRequest(
                    migrate_ml_engine_model_version_config=migration_service.MigrateResourceRequest.MigrateMlEngineModelVersionConfig(
                        endpoint="endpoint_value"
                    )
                )
            ],
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].parent == "parent_value"

        assert args[0].migrate_resource_requests == [
            migration_service.MigrateResourceRequest(
                migrate_ml_engine_model_version_config=migration_service.MigrateResourceRequest.MigrateMlEngineModelVersionConfig(
                    endpoint="endpoint_value"
                )
            )
        ]


def test_batch_migrate_resources_flattened_error():
    client = MigrationServiceClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.batch_migrate_resources(
            migration_service.BatchMigrateResourcesRequest(),
            parent="parent_value",
            migrate_resource_requests=[
                migration_service.MigrateResourceRequest(
                    migrate_ml_engine_model_version_config=migration_service.MigrateResourceRequest.MigrateMlEngineModelVersionConfig(
                        endpoint="endpoint_value"
                    )
                )
            ],
        )


@pytest.mark.asyncio
async def test_batch_migrate_resources_flattened_async():
    client = MigrationServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.batch_migrate_resources), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.batch_migrate_resources(
            parent="parent_value",
            migrate_resource_requests=[
                migration_service.MigrateResourceRequest(
                    migrate_ml_engine_model_version_config=migration_service.MigrateResourceRequest.MigrateMlEngineModelVersionConfig(
                        endpoint="endpoint_value"
                    )
                )
            ],
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].parent == "parent_value"

        assert args[0].migrate_resource_requests == [
            migration_service.MigrateResourceRequest(
                migrate_ml_engine_model_version_config=migration_service.MigrateResourceRequest.MigrateMlEngineModelVersionConfig(
                    endpoint="endpoint_value"
                )
            )
        ]


@pytest.mark.asyncio
async def test_batch_migrate_resources_flattened_error_async():
    client = MigrationServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.batch_migrate_resources(
            migration_service.BatchMigrateResourcesRequest(),
            parent="parent_value",
            migrate_resource_requests=[
                migration_service.MigrateResourceRequest(
                    migrate_ml_engine_model_version_config=migration_service.MigrateResourceRequest.MigrateMlEngineModelVersionConfig(
                        endpoint="endpoint_value"
                    )
                )
            ],
        )


def test_credentials_transport_error():
    # It is an error to provide credentials and a transport instance.
    transport = transports.MigrationServiceGrpcTransport(
        credentials=credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = MigrationServiceClient(
            credentials=credentials.AnonymousCredentials(), transport=transport,
        )

    # It is an error to provide a credentials file and a transport instance.
    transport = transports.MigrationServiceGrpcTransport(
        credentials=credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = MigrationServiceClient(
            client_options={"credentials_file": "credentials.json"},
            transport=transport,
        )

    # It is an error to provide scopes and a transport instance.
    transport = transports.MigrationServiceGrpcTransport(
        credentials=credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = MigrationServiceClient(
            client_options={"scopes": ["1", "2"]}, transport=transport,
        )


def test_transport_instance():
    # A client may be instantiated with a custom transport instance.
    transport = transports.MigrationServiceGrpcTransport(
        credentials=credentials.AnonymousCredentials(),
    )
    client = MigrationServiceClient(transport=transport)
    assert client.transport is transport


def test_transport_get_channel():
    # A client may be instantiated with a custom transport instance.
    transport = transports.MigrationServiceGrpcTransport(
        credentials=credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel

    transport = transports.MigrationServiceGrpcAsyncIOTransport(
        credentials=credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.MigrationServiceGrpcTransport,
        transports.MigrationServiceGrpcAsyncIOTransport,
    ],
)
def test_transport_adc(transport_class):
    # Test default credentials are used if not provided.
    with mock.patch.object(auth, "default") as adc:
        adc.return_value = (credentials.AnonymousCredentials(), None)
        transport_class()
        adc.assert_called_once()


def test_transport_grpc_default():
    # A client should use the gRPC transport by default.
    client = MigrationServiceClient(credentials=credentials.AnonymousCredentials(),)
    assert isinstance(client.transport, transports.MigrationServiceGrpcTransport,)


def test_migration_service_base_transport_error():
    # Passing both a credentials object and credentials_file should raise an error
    with pytest.raises(exceptions.DuplicateCredentialArgs):
        transport = transports.MigrationServiceTransport(
            credentials=credentials.AnonymousCredentials(),
            credentials_file="credentials.json",
        )


def test_migration_service_base_transport():
    # Instantiate the base transport.
    with mock.patch(
        "google.cloud.aiplatform_v1beta1.services.migration_service.transports.MigrationServiceTransport.__init__"
    ) as Transport:
        Transport.return_value = None
        transport = transports.MigrationServiceTransport(
            credentials=credentials.AnonymousCredentials(),
        )

    # Every method on the transport should just blindly
    # raise NotImplementedError.
    methods = (
        "search_migratable_resources",
        "batch_migrate_resources",
    )
    for method in methods:
        with pytest.raises(NotImplementedError):
            getattr(transport, method)(request=object())

    # Additionally, the LRO client (a property) should
    # also raise NotImplementedError
    with pytest.raises(NotImplementedError):
        transport.operations_client


def test_migration_service_base_transport_with_credentials_file():
    # Instantiate the base transport with a credentials file
    with mock.patch.object(
        auth, "load_credentials_from_file"
    ) as load_creds, mock.patch(
        "google.cloud.aiplatform_v1beta1.services.migration_service.transports.MigrationServiceTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        load_creds.return_value = (credentials.AnonymousCredentials(), None)
        transport = transports.MigrationServiceTransport(
            credentials_file="credentials.json", quota_project_id="octopus",
        )
        load_creds.assert_called_once_with(
            "credentials.json",
            scopes=("https://www.googleapis.com/auth/cloud-platform",),
            quota_project_id="octopus",
        )


def test_migration_service_base_transport_with_adc():
    # Test the default credentials are used if credentials and credentials_file are None.
    with mock.patch.object(auth, "default") as adc, mock.patch(
        "google.cloud.aiplatform_v1beta1.services.migration_service.transports.MigrationServiceTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        adc.return_value = (credentials.AnonymousCredentials(), None)
        transport = transports.MigrationServiceTransport()
        adc.assert_called_once()


def test_migration_service_auth_adc():
    # If no credentials are provided, we should use ADC credentials.
    with mock.patch.object(auth, "default") as adc:
        adc.return_value = (credentials.AnonymousCredentials(), None)
        MigrationServiceClient()
        adc.assert_called_once_with(
            scopes=("https://www.googleapis.com/auth/cloud-platform",),
            quota_project_id=None,
        )


def test_migration_service_transport_auth_adc():
    # If credentials and host are not provided, the transport class should use
    # ADC credentials.
    with mock.patch.object(auth, "default") as adc:
        adc.return_value = (credentials.AnonymousCredentials(), None)
        transports.MigrationServiceGrpcTransport(
            host="squid.clam.whelk", quota_project_id="octopus"
        )
        adc.assert_called_once_with(
            scopes=("https://www.googleapis.com/auth/cloud-platform",),
            quota_project_id="octopus",
        )


def test_migration_service_host_no_port():
    client = MigrationServiceClient(
        credentials=credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="aiplatform.googleapis.com"
        ),
    )
    assert client.transport._host == "aiplatform.googleapis.com:443"


def test_migration_service_host_with_port():
    client = MigrationServiceClient(
        credentials=credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="aiplatform.googleapis.com:8000"
        ),
    )
    assert client.transport._host == "aiplatform.googleapis.com:8000"


def test_migration_service_grpc_transport_channel():
    channel = grpc.insecure_channel("http://localhost/")

    # Check that channel is used if provided.
    transport = transports.MigrationServiceGrpcTransport(
        host="squid.clam.whelk", channel=channel,
    )
    assert transport.grpc_channel == channel
    assert transport._host == "squid.clam.whelk:443"
    assert transport._ssl_channel_credentials == None


def test_migration_service_grpc_asyncio_transport_channel():
    channel = aio.insecure_channel("http://localhost/")

    # Check that channel is used if provided.
    transport = transports.MigrationServiceGrpcAsyncIOTransport(
        host="squid.clam.whelk", channel=channel,
    )
    assert transport.grpc_channel == channel
    assert transport._host == "squid.clam.whelk:443"
    assert transport._ssl_channel_credentials == None


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.MigrationServiceGrpcTransport,
        transports.MigrationServiceGrpcAsyncIOTransport,
    ],
)
def test_migration_service_transport_channel_mtls_with_client_cert_source(
    transport_class,
):
    with mock.patch(
        "grpc.ssl_channel_credentials", autospec=True
    ) as grpc_ssl_channel_cred:
        with mock.patch.object(
            transport_class, "create_channel", autospec=True
        ) as grpc_create_channel:
            mock_ssl_cred = mock.Mock()
            grpc_ssl_channel_cred.return_value = mock_ssl_cred

            mock_grpc_channel = mock.Mock()
            grpc_create_channel.return_value = mock_grpc_channel

            cred = credentials.AnonymousCredentials()
            with pytest.warns(DeprecationWarning):
                with mock.patch.object(auth, "default") as adc:
                    adc.return_value = (cred, None)
                    transport = transport_class(
                        host="squid.clam.whelk",
                        api_mtls_endpoint="mtls.squid.clam.whelk",
                        client_cert_source=client_cert_source_callback,
                    )
                    adc.assert_called_once()

            grpc_ssl_channel_cred.assert_called_once_with(
                certificate_chain=b"cert bytes", private_key=b"key bytes"
            )
            grpc_create_channel.assert_called_once_with(
                "mtls.squid.clam.whelk:443",
                credentials=cred,
                credentials_file=None,
                scopes=("https://www.googleapis.com/auth/cloud-platform",),
                ssl_credentials=mock_ssl_cred,
                quota_project_id=None,
            )
            assert transport.grpc_channel == mock_grpc_channel
            assert transport._ssl_channel_credentials == mock_ssl_cred


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.MigrationServiceGrpcTransport,
        transports.MigrationServiceGrpcAsyncIOTransport,
    ],
)
def test_migration_service_transport_channel_mtls_with_adc(transport_class):
    mock_ssl_cred = mock.Mock()
    with mock.patch.multiple(
        "google.auth.transport.grpc.SslCredentials",
        __init__=mock.Mock(return_value=None),
        ssl_credentials=mock.PropertyMock(return_value=mock_ssl_cred),
    ):
        with mock.patch.object(
            transport_class, "create_channel", autospec=True
        ) as grpc_create_channel:
            mock_grpc_channel = mock.Mock()
            grpc_create_channel.return_value = mock_grpc_channel
            mock_cred = mock.Mock()

            with pytest.warns(DeprecationWarning):
                transport = transport_class(
                    host="squid.clam.whelk",
                    credentials=mock_cred,
                    api_mtls_endpoint="mtls.squid.clam.whelk",
                    client_cert_source=None,
                )

            grpc_create_channel.assert_called_once_with(
                "mtls.squid.clam.whelk:443",
                credentials=mock_cred,
                credentials_file=None,
                scopes=("https://www.googleapis.com/auth/cloud-platform",),
                ssl_credentials=mock_ssl_cred,
                quota_project_id=None,
            )
            assert transport.grpc_channel == mock_grpc_channel


def test_migration_service_grpc_lro_client():
    client = MigrationServiceClient(
        credentials=credentials.AnonymousCredentials(), transport="grpc",
    )
    transport = client.transport

    # Ensure that we have a api-core operations client.
    assert isinstance(transport.operations_client, operations_v1.OperationsClient,)

    # Ensure that subsequent calls to the property send the exact same object.
    assert transport.operations_client is transport.operations_client


def test_migration_service_grpc_lro_async_client():
    client = MigrationServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport="grpc_asyncio",
    )
    transport = client.transport

    # Ensure that we have a api-core operations client.
    assert isinstance(transport.operations_client, operations_v1.OperationsAsyncClient,)

    # Ensure that subsequent calls to the property send the exact same object.
    assert transport.operations_client is transport.operations_client


def test_annotated_dataset_path():
    project = "squid"
    dataset = "clam"
    annotated_dataset = "whelk"

    expected = "projects/{project}/datasets/{dataset}/annotatedDatasets/{annotated_dataset}".format(
        project=project, dataset=dataset, annotated_dataset=annotated_dataset,
    )
    actual = MigrationServiceClient.annotated_dataset_path(
        project, dataset, annotated_dataset
    )
    assert expected == actual


def test_parse_annotated_dataset_path():
    expected = {
        "project": "octopus",
        "dataset": "oyster",
        "annotated_dataset": "nudibranch",
    }
    path = MigrationServiceClient.annotated_dataset_path(**expected)

    # Check that the path construction is reversible.
    actual = MigrationServiceClient.parse_annotated_dataset_path(path)
    assert expected == actual


def test_dataset_path():
    project = "cuttlefish"
    location = "mussel"
    dataset = "winkle"

    expected = "projects/{project}/locations/{location}/datasets/{dataset}".format(
        project=project, location=location, dataset=dataset,
    )
    actual = MigrationServiceClient.dataset_path(project, location, dataset)
    assert expected == actual


def test_parse_dataset_path():
    expected = {
        "project": "nautilus",
        "location": "scallop",
        "dataset": "abalone",
    }
    path = MigrationServiceClient.dataset_path(**expected)

    # Check that the path construction is reversible.
    actual = MigrationServiceClient.parse_dataset_path(path)
    assert expected == actual


def test_dataset_path():
    project = "squid"
    dataset = "clam"

    expected = "projects/{project}/datasets/{dataset}".format(
        project=project, dataset=dataset,
    )
    actual = MigrationServiceClient.dataset_path(project, dataset)
    assert expected == actual


def test_parse_dataset_path():
    expected = {
        "project": "whelk",
        "dataset": "octopus",
    }
    path = MigrationServiceClient.dataset_path(**expected)

    # Check that the path construction is reversible.
    actual = MigrationServiceClient.parse_dataset_path(path)
    assert expected == actual


def test_dataset_path():
    project = "oyster"
    location = "nudibranch"
    dataset = "cuttlefish"

    expected = "projects/{project}/locations/{location}/datasets/{dataset}".format(
        project=project, location=location, dataset=dataset,
    )
    actual = MigrationServiceClient.dataset_path(project, location, dataset)
    assert expected == actual


def test_parse_dataset_path():
    expected = {
        "project": "mussel",
        "location": "winkle",
        "dataset": "nautilus",
    }
    path = MigrationServiceClient.dataset_path(**expected)

    # Check that the path construction is reversible.
    actual = MigrationServiceClient.parse_dataset_path(path)
    assert expected == actual


def test_model_path():
    project = "scallop"
    location = "abalone"
    model = "squid"

    expected = "projects/{project}/locations/{location}/models/{model}".format(
        project=project, location=location, model=model,
    )
    actual = MigrationServiceClient.model_path(project, location, model)
    assert expected == actual


def test_parse_model_path():
    expected = {
        "project": "clam",
        "location": "whelk",
        "model": "octopus",
    }
    path = MigrationServiceClient.model_path(**expected)

    # Check that the path construction is reversible.
    actual = MigrationServiceClient.parse_model_path(path)
    assert expected == actual


def test_model_path():
    project = "oyster"
    location = "nudibranch"
    model = "cuttlefish"

    expected = "projects/{project}/locations/{location}/models/{model}".format(
        project=project, location=location, model=model,
    )
    actual = MigrationServiceClient.model_path(project, location, model)
    assert expected == actual


def test_parse_model_path():
    expected = {
        "project": "mussel",
        "location": "winkle",
        "model": "nautilus",
    }
    path = MigrationServiceClient.model_path(**expected)

    # Check that the path construction is reversible.
    actual = MigrationServiceClient.parse_model_path(path)
    assert expected == actual


def test_version_path():
    project = "scallop"
    model = "abalone"
    version = "squid"

    expected = "projects/{project}/models/{model}/versions/{version}".format(
        project=project, model=model, version=version,
    )
    actual = MigrationServiceClient.version_path(project, model, version)
    assert expected == actual


def test_parse_version_path():
    expected = {
        "project": "clam",
        "model": "whelk",
        "version": "octopus",
    }
    path = MigrationServiceClient.version_path(**expected)

    # Check that the path construction is reversible.
    actual = MigrationServiceClient.parse_version_path(path)
    assert expected == actual


def test_common_billing_account_path():
    billing_account = "oyster"

    expected = "billingAccounts/{billing_account}".format(
        billing_account=billing_account,
    )
    actual = MigrationServiceClient.common_billing_account_path(billing_account)
    assert expected == actual


def test_parse_common_billing_account_path():
    expected = {
        "billing_account": "nudibranch",
    }
    path = MigrationServiceClient.common_billing_account_path(**expected)

    # Check that the path construction is reversible.
    actual = MigrationServiceClient.parse_common_billing_account_path(path)
    assert expected == actual


def test_common_folder_path():
    folder = "cuttlefish"

    expected = "folders/{folder}".format(folder=folder,)
    actual = MigrationServiceClient.common_folder_path(folder)
    assert expected == actual


def test_parse_common_folder_path():
    expected = {
        "folder": "mussel",
    }
    path = MigrationServiceClient.common_folder_path(**expected)

    # Check that the path construction is reversible.
    actual = MigrationServiceClient.parse_common_folder_path(path)
    assert expected == actual


def test_common_organization_path():
    organization = "winkle"

    expected = "organizations/{organization}".format(organization=organization,)
    actual = MigrationServiceClient.common_organization_path(organization)
    assert expected == actual


def test_parse_common_organization_path():
    expected = {
        "organization": "nautilus",
    }
    path = MigrationServiceClient.common_organization_path(**expected)

    # Check that the path construction is reversible.
    actual = MigrationServiceClient.parse_common_organization_path(path)
    assert expected == actual


def test_common_project_path():
    project = "scallop"

    expected = "projects/{project}".format(project=project,)
    actual = MigrationServiceClient.common_project_path(project)
    assert expected == actual


def test_parse_common_project_path():
    expected = {
        "project": "abalone",
    }
    path = MigrationServiceClient.common_project_path(**expected)

    # Check that the path construction is reversible.
    actual = MigrationServiceClient.parse_common_project_path(path)
    assert expected == actual


def test_common_location_path():
    project = "squid"
    location = "clam"

    expected = "projects/{project}/locations/{location}".format(
        project=project, location=location,
    )
    actual = MigrationServiceClient.common_location_path(project, location)
    assert expected == actual


def test_parse_common_location_path():
    expected = {
        "project": "whelk",
        "location": "octopus",
    }
    path = MigrationServiceClient.common_location_path(**expected)

    # Check that the path construction is reversible.
    actual = MigrationServiceClient.parse_common_location_path(path)
    assert expected == actual


def test_client_withDEFAULT_CLIENT_INFO():
    client_info = gapic_v1.client_info.ClientInfo()

    with mock.patch.object(
        transports.MigrationServiceTransport, "_prep_wrapped_messages"
    ) as prep:
        client = MigrationServiceClient(
            credentials=credentials.AnonymousCredentials(), client_info=client_info,
        )
        prep.assert_called_once_with(client_info)

    with mock.patch.object(
        transports.MigrationServiceTransport, "_prep_wrapped_messages"
    ) as prep:
        transport_class = MigrationServiceClient.get_transport_class()
        transport = transport_class(
            credentials=credentials.AnonymousCredentials(), client_info=client_info,
        )
        prep.assert_called_once_with(client_info)
