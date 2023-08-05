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

import proto  # type: ignore


from google.cloud.aiplatform_v1beta1.types import explanation
from google.protobuf import struct_pb2 as struct  # type: ignore


__protobuf__ = proto.module(
    package="google.cloud.aiplatform.v1beta1",
    manifest={
        "PredictRequest",
        "PredictResponse",
        "ExplainRequest",
        "ExplainResponse",
    },
)


class PredictRequest(proto.Message):
    r"""Request message for
    ``PredictionService.Predict``.

    Attributes:
        endpoint (str):
            Required. The name of the Endpoint requested to serve the
            prediction. Format:
            ``projects/{project}/locations/{location}/endpoints/{endpoint}``
        instances (Sequence[~.struct.Value]):
            Required. The instances that are the input to the prediction
            call. A DeployedModel may have an upper limit on the number
            of instances it supports per request, and when it is
            exceeded the prediction call errors in case of AutoML
            Models, or, in case of customer created Models, the
            behaviour is as documented by that Model. The schema of any
            single instance may be specified via Endpoint's
            DeployedModels'
            [Model's][google.cloud.aiplatform.v1beta1.DeployedModel.model]
            [PredictSchemata's][google.cloud.aiplatform.v1beta1.Model.predict_schemata]
            ``instance_schema_uri``.
        parameters (~.struct.Value):
            The parameters that govern the prediction. The schema of the
            parameters may be specified via Endpoint's DeployedModels'
            [Model's
            ][google.cloud.aiplatform.v1beta1.DeployedModel.model]
            [PredictSchemata's][google.cloud.aiplatform.v1beta1.Model.predict_schemata]
            ``parameters_schema_uri``.
    """

    endpoint = proto.Field(proto.STRING, number=1)

    instances = proto.RepeatedField(proto.MESSAGE, number=2, message=struct.Value,)

    parameters = proto.Field(proto.MESSAGE, number=3, message=struct.Value,)


class PredictResponse(proto.Message):
    r"""Response message for
    ``PredictionService.Predict``.

    Attributes:
        predictions (Sequence[~.struct.Value]):
            The predictions that are the output of the predictions call.
            The schema of any single prediction may be specified via
            Endpoint's DeployedModels' [Model's
            ][google.cloud.aiplatform.v1beta1.DeployedModel.model]
            [PredictSchemata's][google.cloud.aiplatform.v1beta1.Model.predict_schemata]
            ``prediction_schema_uri``.
        deployed_model_id (str):
            ID of the Endpoint's DeployedModel that
            served this prediction.
    """

    predictions = proto.RepeatedField(proto.MESSAGE, number=1, message=struct.Value,)

    deployed_model_id = proto.Field(proto.STRING, number=2)


class ExplainRequest(proto.Message):
    r"""Request message for
    ``PredictionService.Explain``.

    Attributes:
        endpoint (str):
            Required. The name of the Endpoint requested to serve the
            explanation. Format:
            ``projects/{project}/locations/{location}/endpoints/{endpoint}``
        instances (Sequence[~.struct.Value]):
            Required. The instances that are the input to the
            explanation call. A DeployedModel may have an upper limit on
            the number of instances it supports per request, and when it
            is exceeded the explanation call errors in case of AutoML
            Models, or, in case of customer created Models, the
            behaviour is as documented by that Model. The schema of any
            single instance may be specified via Endpoint's
            DeployedModels'
            [Model's][google.cloud.aiplatform.v1beta1.DeployedModel.model]
            [PredictSchemata's][google.cloud.aiplatform.v1beta1.Model.predict_schemata]
            ``instance_schema_uri``.
        parameters (~.struct.Value):
            The parameters that govern the prediction. The schema of the
            parameters may be specified via Endpoint's DeployedModels'
            [Model's
            ][google.cloud.aiplatform.v1beta1.DeployedModel.model]
            [PredictSchemata's][google.cloud.aiplatform.v1beta1.Model.predict_schemata]
            ``parameters_schema_uri``.
        deployed_model_id (str):
            If specified, this ExplainRequest will be served by the
            chosen DeployedModel, overriding
            ``Endpoint.traffic_split``.
    """

    endpoint = proto.Field(proto.STRING, number=1)

    instances = proto.RepeatedField(proto.MESSAGE, number=2, message=struct.Value,)

    parameters = proto.Field(proto.MESSAGE, number=4, message=struct.Value,)

    deployed_model_id = proto.Field(proto.STRING, number=3)


class ExplainResponse(proto.Message):
    r"""Response message for
    ``PredictionService.Explain``.

    Attributes:
        explanations (Sequence[~.explanation.Explanation]):
            The explanations of the Model's
            ``PredictResponse.predictions``.

            It has the same number of elements as
            ``instances``
            to be explained.
        deployed_model_id (str):
            ID of the Endpoint's DeployedModel that
            served this explanation.
        predictions (Sequence[~.struct.Value]):
            The predictions that are the output of the predictions call.
            Same as
            ``PredictResponse.predictions``.
    """

    explanations = proto.RepeatedField(
        proto.MESSAGE, number=1, message=explanation.Explanation,
    )

    deployed_model_id = proto.Field(proto.STRING, number=2)

    predictions = proto.RepeatedField(proto.MESSAGE, number=3, message=struct.Value,)


__all__ = tuple(sorted(__protobuf__.manifest))
