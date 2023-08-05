# coding=utf-8
# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
#
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.service_client import SDKClient
from msrest import Configuration, Serializer, Deserializer
from .version import VERSION
from .operations.endpoint_settings_operations import EndpointSettingsOperations
from .operations.endpoint_keys_operations import EndpointKeysOperations
from .operations.alterations_operations import AlterationsOperations
from .operations.knowledgebase_operations import KnowledgebaseOperations
from .operations.operations import Operations
from . import models


class QnAMakerClientConfiguration(Configuration):
    """Configuration for QnAMakerClient
    Note that all parameters used to create this instance are saved as instance
    attributes.

    :param endpoint: Supported Cognitive Services endpoint (e.g., https://<
     qnamaker-resource-name >.api.cognitiveservices.azure.com).
    :type endpoint: str
    :param credentials: Subscription credentials which uniquely identify
     client subscription.
    :type credentials: None
    """

    def __init__(
            self, endpoint, credentials):

        if endpoint is None:
            raise ValueError("Parameter 'endpoint' must not be None.")
        if credentials is None:
            raise ValueError("Parameter 'credentials' must not be None.")
        base_url = '{Endpoint}/qnamaker/v5.0-preview.1'

        super(QnAMakerClientConfiguration, self).__init__(base_url)

        self.add_user_agent('azure-cognitiveservices-knowledge-qnamaker/{}'.format(VERSION))

        self.endpoint = endpoint
        self.credentials = credentials


class QnAMakerClient(SDKClient):
    """An API for QnAMaker Service

    :ivar config: Configuration for client.
    :vartype config: QnAMakerClientConfiguration

    :ivar endpoint_settings: EndpointSettings operations
    :vartype endpoint_settings: azure.cognitiveservices.knowledge.qnamaker.operations.EndpointSettingsOperations
    :ivar endpoint_keys: EndpointKeys operations
    :vartype endpoint_keys: azure.cognitiveservices.knowledge.qnamaker.operations.EndpointKeysOperations
    :ivar alterations: Alterations operations
    :vartype alterations: azure.cognitiveservices.knowledge.qnamaker.operations.AlterationsOperations
    :ivar knowledgebase: Knowledgebase operations
    :vartype knowledgebase: azure.cognitiveservices.knowledge.qnamaker.operations.KnowledgebaseOperations
    :ivar operations: Operations operations
    :vartype operations: azure.cognitiveservices.knowledge.qnamaker.operations.Operations

    :param endpoint: Supported Cognitive Services endpoint (e.g., https://<
     qnamaker-resource-name >.api.cognitiveservices.azure.com).
    :type endpoint: str
    :param credentials: Subscription credentials which uniquely identify
     client subscription.
    :type credentials: None
    """

    def __init__(
            self, endpoint, credentials):

        self.config = QnAMakerClientConfiguration(endpoint, credentials)
        super(QnAMakerClient, self).__init__(self.config.credentials, self.config)

        client_models = {k: v for k, v in models.__dict__.items() if isinstance(v, type)}
        self.api_version = 'v5.0-preview.1'
        self._serialize = Serializer(client_models)
        self._deserialize = Deserializer(client_models)

        self.endpoint_settings = EndpointSettingsOperations(
            self._client, self.config, self._serialize, self._deserialize)
        self.endpoint_keys = EndpointKeysOperations(
            self._client, self.config, self._serialize, self._deserialize)
        self.alterations = AlterationsOperations(
            self._client, self.config, self._serialize, self._deserialize)
        self.knowledgebase = KnowledgebaseOperations(
            self._client, self.config, self._serialize, self._deserialize)
        self.operations = Operations(
            self._client, self.config, self._serialize, self._deserialize)
