#
# This file is part of the Ingram Micro CloudBlue Connect Processors Toolkit.
#
# Copyright (c) 2022 Ingram Micro. All Rights Reserved.
#
from copy import deepcopy
from typing import List, Optional, Union

from faker import Faker


def find_by_id(elements: List[dict], element_id: str, default: Optional[dict] = None) -> Optional[dict]:
    """
    Searches for a parameter/item with the given ``id`` within the ``list``.

    :param elements: The list of parameters/items to search.
    :param element_id: The id of the parameter/item to find.
    :param default: Default value to return if item is not found.
    :return: The parameter/list, or ``default`` if it was not found.
    """
    try:
        return next(filter(lambda element: element['id'] == element_id, elements))
    except StopIteration:
        return default


def merge(base: dict, override: dict) -> dict:
    """
    Merge two dictionaries (override into base) recursively.

    :param base: The base dictionary.
    :param override: Override dictionary to be merged into base.
    :return dict: The new dictionary.
    """
    new_base = deepcopy(base)
    for key, value in override.items():
        if key in new_base:
            if isinstance(new_base[key], dict) and isinstance(value, dict):
                new_base[key] = merge(new_base[key], value)
            elif isinstance(new_base[key], list) and isinstance(value, list):
                new_base[key].extend(value)
            else:
                new_base[key] = value
        else:
            new_base[key] = value

    return new_base


def make_tier(tier_type: str = 'customer', locale: List[str] = None) -> dict:
    faker = Faker(['en_US'] if locale is None else locale)
    return {
        "name": faker.company(),
        "type": tier_type,
        "external_id": f"{faker.pyint(1000000, 9999999)}",
        "external_uid": f"{faker.uuid4()}",
        "contact_info": {
            "address_line1": f"{faker.pyint(100, 999)}, {faker.street_name()}",
            "address_line2": faker.secondary_address(),
            "city": faker.city(),
            "state": faker.state(),
            "postal_code": faker.zipcode(),
            "country": faker.country_code(),
            "contact": {
                "first_name": faker.first_name(),
                "last_name": faker.last_name(),
                "email": faker.company_email(),
                "phone_number": {
                    "country_code": f"+{faker.pyint(1, 99)}",
                    "area_code": f"{faker.pyint(1, 99)}",
                    "phone_number": f"{faker.pyint(1, 999999)}",
                    "extension": f"{faker.pyint(1, 100)}",
                },
            },
        },
    }


def make_param(
        param_id: str,
        value: Optional[Union[str, dict]] = None,
        value_error: Optional[str] = None,
        value_type: Optional[str] = None,
        title: Optional[str] = None,
        description: Optional[str] = None,
        scope: Optional[str] = None,
        phase: Optional[str] = None,
) -> dict:
    return {
        'id': param_id,
        'structured_value' if type(value) in [object, dict, list] else 'value': value,
        'value_error': value_error,
        'title': f'Parameter {param_id} title.' if title is None else title,
        'description': f'Parameter {param_id} description.' if description is None else description,
        'type': 'text' if value_type is None else value_type,
        'scope': scope,
        'phase': phase,
    }


def request_model(request: dict) -> str:
    """
    Returns the request model depending on the request type.

    :param request: dict
    :return: str
    """

    def match_request_type(model: dict) -> bool:
        return model.get('object') in request or request.get('type') in model.get('types')

    try:
        return next(filter(match_request_type, [
            {
                'request': 'asset',
                'object': 'asset',
                'types': ['adjustment', 'purchase', 'change', 'suspend', 'resume', 'cancel'],
            },
            {
                'request': 'tier-config',
                'object': 'configuration',
                'types': ['setup'],
            },
        ])).get('request')
    except StopIteration:
        return 'undefined'
