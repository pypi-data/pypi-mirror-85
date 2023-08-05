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

from .update_questions_dto import UpdateQuestionsDTO


class UpdateQnaDTOQuestions(UpdateQuestionsDTO):
    """List of questions associated with the answer.

    :param add: List of questions to be added
    :type add: list[str]
    :param delete: List of questions to be deleted.
    :type delete: list[str]
    """

    _attribute_map = {
        'add': {'key': 'add', 'type': '[str]'},
        'delete': {'key': 'delete', 'type': '[str]'},
    }

    def __init__(self, **kwargs):
        super(UpdateQnaDTOQuestions, self).__init__(**kwargs)
