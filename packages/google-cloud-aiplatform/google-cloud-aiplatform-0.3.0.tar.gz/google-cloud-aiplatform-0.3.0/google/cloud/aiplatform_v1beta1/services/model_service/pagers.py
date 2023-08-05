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

from typing import Any, AsyncIterable, Awaitable, Callable, Iterable, Sequence, Tuple

from google.cloud.aiplatform_v1beta1.types import model
from google.cloud.aiplatform_v1beta1.types import model_evaluation
from google.cloud.aiplatform_v1beta1.types import model_evaluation_slice
from google.cloud.aiplatform_v1beta1.types import model_service


class ListModelsPager:
    """A pager for iterating through ``list_models`` requests.

    This class thinly wraps an initial
    :class:`~.model_service.ListModelsResponse` object, and
    provides an ``__iter__`` method to iterate through its
    ``models`` field.

    If there are more pages, the ``__iter__`` method will make additional
    ``ListModels`` requests and continue to iterate
    through the ``models`` field on the
    corresponding responses.

    All the usual :class:`~.model_service.ListModelsResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., model_service.ListModelsResponse],
        request: model_service.ListModelsRequest,
        response: model_service.ListModelsResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiate the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (:class:`~.model_service.ListModelsRequest`):
                The initial request object.
            response (:class:`~.model_service.ListModelsResponse`):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = model_service.ListModelsRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    def pages(self) -> Iterable[model_service.ListModelsResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = self._method(self._request, metadata=self._metadata)
            yield self._response

    def __iter__(self) -> Iterable[model.Model]:
        for page in self.pages:
            yield from page.models

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListModelsAsyncPager:
    """A pager for iterating through ``list_models`` requests.

    This class thinly wraps an initial
    :class:`~.model_service.ListModelsResponse` object, and
    provides an ``__aiter__`` method to iterate through its
    ``models`` field.

    If there are more pages, the ``__aiter__`` method will make additional
    ``ListModels`` requests and continue to iterate
    through the ``models`` field on the
    corresponding responses.

    All the usual :class:`~.model_service.ListModelsResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., Awaitable[model_service.ListModelsResponse]],
        request: model_service.ListModelsRequest,
        response: model_service.ListModelsResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiate the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (:class:`~.model_service.ListModelsRequest`):
                The initial request object.
            response (:class:`~.model_service.ListModelsResponse`):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = model_service.ListModelsRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    async def pages(self) -> AsyncIterable[model_service.ListModelsResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = await self._method(self._request, metadata=self._metadata)
            yield self._response

    def __aiter__(self) -> AsyncIterable[model.Model]:
        async def async_generator():
            async for page in self.pages:
                for response in page.models:
                    yield response

        return async_generator()

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListModelEvaluationsPager:
    """A pager for iterating through ``list_model_evaluations`` requests.

    This class thinly wraps an initial
    :class:`~.model_service.ListModelEvaluationsResponse` object, and
    provides an ``__iter__`` method to iterate through its
    ``model_evaluations`` field.

    If there are more pages, the ``__iter__`` method will make additional
    ``ListModelEvaluations`` requests and continue to iterate
    through the ``model_evaluations`` field on the
    corresponding responses.

    All the usual :class:`~.model_service.ListModelEvaluationsResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., model_service.ListModelEvaluationsResponse],
        request: model_service.ListModelEvaluationsRequest,
        response: model_service.ListModelEvaluationsResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiate the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (:class:`~.model_service.ListModelEvaluationsRequest`):
                The initial request object.
            response (:class:`~.model_service.ListModelEvaluationsResponse`):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = model_service.ListModelEvaluationsRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    def pages(self) -> Iterable[model_service.ListModelEvaluationsResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = self._method(self._request, metadata=self._metadata)
            yield self._response

    def __iter__(self) -> Iterable[model_evaluation.ModelEvaluation]:
        for page in self.pages:
            yield from page.model_evaluations

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListModelEvaluationsAsyncPager:
    """A pager for iterating through ``list_model_evaluations`` requests.

    This class thinly wraps an initial
    :class:`~.model_service.ListModelEvaluationsResponse` object, and
    provides an ``__aiter__`` method to iterate through its
    ``model_evaluations`` field.

    If there are more pages, the ``__aiter__`` method will make additional
    ``ListModelEvaluations`` requests and continue to iterate
    through the ``model_evaluations`` field on the
    corresponding responses.

    All the usual :class:`~.model_service.ListModelEvaluationsResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., Awaitable[model_service.ListModelEvaluationsResponse]],
        request: model_service.ListModelEvaluationsRequest,
        response: model_service.ListModelEvaluationsResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiate the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (:class:`~.model_service.ListModelEvaluationsRequest`):
                The initial request object.
            response (:class:`~.model_service.ListModelEvaluationsResponse`):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = model_service.ListModelEvaluationsRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    async def pages(self) -> AsyncIterable[model_service.ListModelEvaluationsResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = await self._method(self._request, metadata=self._metadata)
            yield self._response

    def __aiter__(self) -> AsyncIterable[model_evaluation.ModelEvaluation]:
        async def async_generator():
            async for page in self.pages:
                for response in page.model_evaluations:
                    yield response

        return async_generator()

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListModelEvaluationSlicesPager:
    """A pager for iterating through ``list_model_evaluation_slices`` requests.

    This class thinly wraps an initial
    :class:`~.model_service.ListModelEvaluationSlicesResponse` object, and
    provides an ``__iter__`` method to iterate through its
    ``model_evaluation_slices`` field.

    If there are more pages, the ``__iter__`` method will make additional
    ``ListModelEvaluationSlices`` requests and continue to iterate
    through the ``model_evaluation_slices`` field on the
    corresponding responses.

    All the usual :class:`~.model_service.ListModelEvaluationSlicesResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., model_service.ListModelEvaluationSlicesResponse],
        request: model_service.ListModelEvaluationSlicesRequest,
        response: model_service.ListModelEvaluationSlicesResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiate the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (:class:`~.model_service.ListModelEvaluationSlicesRequest`):
                The initial request object.
            response (:class:`~.model_service.ListModelEvaluationSlicesResponse`):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = model_service.ListModelEvaluationSlicesRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    def pages(self) -> Iterable[model_service.ListModelEvaluationSlicesResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = self._method(self._request, metadata=self._metadata)
            yield self._response

    def __iter__(self) -> Iterable[model_evaluation_slice.ModelEvaluationSlice]:
        for page in self.pages:
            yield from page.model_evaluation_slices

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListModelEvaluationSlicesAsyncPager:
    """A pager for iterating through ``list_model_evaluation_slices`` requests.

    This class thinly wraps an initial
    :class:`~.model_service.ListModelEvaluationSlicesResponse` object, and
    provides an ``__aiter__`` method to iterate through its
    ``model_evaluation_slices`` field.

    If there are more pages, the ``__aiter__`` method will make additional
    ``ListModelEvaluationSlices`` requests and continue to iterate
    through the ``model_evaluation_slices`` field on the
    corresponding responses.

    All the usual :class:`~.model_service.ListModelEvaluationSlicesResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[
            ..., Awaitable[model_service.ListModelEvaluationSlicesResponse]
        ],
        request: model_service.ListModelEvaluationSlicesRequest,
        response: model_service.ListModelEvaluationSlicesResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiate the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (:class:`~.model_service.ListModelEvaluationSlicesRequest`):
                The initial request object.
            response (:class:`~.model_service.ListModelEvaluationSlicesResponse`):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = model_service.ListModelEvaluationSlicesRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    async def pages(
        self,
    ) -> AsyncIterable[model_service.ListModelEvaluationSlicesResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = await self._method(self._request, metadata=self._metadata)
            yield self._response

    def __aiter__(self) -> AsyncIterable[model_evaluation_slice.ModelEvaluationSlice]:
        async def async_generator():
            async for page in self.pages:
                for response in page.model_evaluation_slices:
                    yield response

        return async_generator()

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)
