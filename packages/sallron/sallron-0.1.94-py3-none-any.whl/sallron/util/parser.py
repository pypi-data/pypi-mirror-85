#!/usr/bin/env python
"""Core module for parsing related operations"""

import re

PUNCTUATION = '!"#$%&\'()*+,./:;<=>?@[\\]^_`{|}~'

def remove_punctuation(obj):
    """
    Utility funciton to remove all punctuation from a obj

    e.g.:
    obj = {
        "sampling_level": [
            "field.vision": 23,
            "field.name": "Leo_di_Caprio"
        ]
    }

    => {
        "sampling_level": [
            "fieldvision": 23,
            "fieldname": "Leo_di_Caprio"
        ]
    }

    Args:
        obj (dict): Dict object containing the query for GA

    Returns:
        function: Recursive function to modify the object
    """

    def func(string): return ''.join(
        list(filter(
            lambda char: char not in PUNCTUATION,
            string
        ))
    )

    return modify_object(obj, func)

def camelify(obj):
    """
    Utility function to modify a string removing the underscores

    e.g.:
    obj = {
        "sampling_level": [
            "field_vision": 23,
            "field_name": "Leo_di_Caprio"
        ]
    }

    => {
        "samplingLevel": [
            "fieldVision": 23,
            "fieldName": "LeoDiCaprio"
        ]
    }

    Args:
        obj (dict): Dict object containing the query for GA

    Returns:
        function: Recursive function to modify the object
    """

    def func(string): return re.sub(
        r'_(\w)', lambda match: match.group(1).upper(), string)

    return modify_object(obj, func)

def decamelify(obj):
    """
    Opposite of camelify
    """

    def func(string): return re.sub(
        '([a-z0-9])([A-Z])', r'\1_\2', string).lower()

    return modify_object(obj, func)


def modify_object(obj, func):
    """
    Recursive function to go through indented objects and modify it

    Args:
        obj (dict, list, bool, str): Value of key-value pair of query object from GA
        func (function): Input function to modify obj

    Returns:
        obj: Modified object
    """

    if isinstance(obj, dict):

        temp_obj = {}
        for key in obj:
            temp_obj[func(key)] = modify_object(obj[key], func)

        return temp_obj

    if isinstance(obj, list):

        temp_obj = []
        for key in obj:
            temp_obj.append(modify_object(key, func))

        return temp_obj

    if isinstance(obj, bool):
        return obj

    if isinstance(obj, str) and not obj.isupper():
        return func(obj)

    return obj