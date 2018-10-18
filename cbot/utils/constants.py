# -*- coding: utf-8 -*-

"""
CBot Constants
"""

'''
每个句子最大长度
'''
STATEMENT_TEXT_MAX_LENGTH = 400

# 标签的最大长度
TAG_NAME_MAX_LENGTH = 50

DEFAULT_STORAGE_ADAPTER = 'cbot.adapters.storageadapters.SQLStorageAdapter'
DEFAULT_NO_KNOWLEDGE_ADAPTER = 'cbot.adapters.noknowledgeadapters.NoKnowledgeAdapter'
DEFAULT_CORE_ADAPTER = 'cbot.adapters.coreadapters.BestMatch'
DEFAULT_INPUT_ADAPTER = 'cbot.adapters.inputadapters.VariableInputTypeAdapter'
DEFAULT_OUTPUT_ADAPTER = 'cbot.adapters.outputadapters.OutputAdapter'
DEFAULT_TRAINER = 'cbot.main.trainers.ListTrainer'


IS_STUDY=True
