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

from msrest.serialization import Model


class EndpointSettingsDTO(Model):
    """Endpoint settings.

    :param active_learning: Active Learning settings of the endpoint.
    :type active_learning:
     ~azure.cognitiveservices.knowledge.qnamaker.models.EndpointSettingsDTOActiveLearning
    """

    _attribute_map = {
        'active_learning': {'key': 'activeLearning', 'type': 'EndpointSettingsDTOActiveLearning'},
    }

    def __init__(self, **kwargs):
        super(EndpointSettingsDTO, self).__init__(**kwargs)
        self.active_learning = kwargs.get('active_learning', None)
