#
# This file is part of the Ingram Micro CloudBlue Connect Processors Toolkit.
#
# Copyright (c) 2023 Ingram Micro. All Rights Reserved.
#
from copy import deepcopy
from datetime import datetime
from typing import Any, Dict, List, Optional, TypeVar, Union

from rndi.connect_business_objects.exceptions import MissingParameterError
from rndi.connect_business_objects.helpers import find_by_id, make_param, merge

THasConfiguration = TypeVar('THasConfiguration', bound='HasConfiguration')
THasConnection = TypeVar('THasConnection', bound='HasConnection')
THasContract = TypeVar('THasContract', bound='HasContract')
THasEvents = TypeVar('THasEvents', bound='HasEvents')
THasMarketplace = TypeVar('THasMarketplace', bound='HasMarketplace')
THasParameters = TypeVar('THasParameters', bound='HasParameters')
THasProduct = TypeVar('THasProduct', bound='HasProduct')
THasReadWriteOperations = TypeVar('THasReadWriteOperations', bound='HasReadWriteOperations')


class HasConfiguration:
    _data: dict

    def configuration_params(self) -> List[dict]:
        return self._data.get('configuration', {}).get('params', [])

    def configuration_param(
            self,
            param_id: str,
            key: Optional[str] = None,
            default: Optional[Any] = None,
    ) -> Optional[Any]:
        parameter = find_by_id(self.configuration_params(), param_id)
        if parameter is None:
            raise MissingParameterError(f'Missing parameter {param_id}', param_id)

        return parameter if key is None else parameter.get(key, default)

    def with_configuration_params(self, params: List[dict]) -> THasConfiguration:
        for param in params:
            self.with_configuration_param(**param)
        return self

    def with_configuration_param(
            self,
            param_id: str,
            value: Optional[Union[str, dict, list]] = None,
            value_error: Optional[str] = None,
            value_type: Optional[str] = None,
            title: Optional[str] = None,
            description: Optional[str] = None,
    ) -> THasConfiguration:
        if 'configuration' not in self._data:
            self._data.update({'configuration': {}})

        if 'params' not in self._data.get('configuration', {}):
            self._data.get('configuration', {}).update({'params': []})

        try:
            param = self.configuration_param(param_id)
        except MissingParameterError:
            param = {'id': param_id}
            self._data.get('configuration', {}).get('params', []).append(param)

        members = make_param(param_id, value, value_error, value_type, title, description)
        param.update({k: v for k, v in members.items() if v is not None})
        return self


class HasConnection:
    _data: dict

    def connection(self, key: Optional[str] = None, default: Optional[Any] = None) -> Optional[Any]:
        connection = self._data.get('connection')
        if connection is None:
            return None

        return connection if key is None else connection.get(key, default)

    def with_connection(
            self,
            connection_id: str,
            connection_type: str,
            provider: Optional[dict] = None,
            vendor: Optional[dict] = None,
            hub: Optional[dict] = None,
    ) -> THasConnection:
        self._data.update({'connection': merge(self._data.get('connection', {}), {
            'id': connection_id,
            'type': connection_type,
        })})
        if provider is not None:
            self.with_connection_provider(provider_id=provider.get('id'), provider_name=provider.get('name'))
        if vendor is not None:
            self.with_connection_vendor(vendor_id=vendor.get('id'), vendor_name=vendor.get('name'))
        if hub is not None:
            self.with_connection_hub(hub_id=hub.get('id'), hub_name=hub.get('name'))
        return self

    def connection_provider(self, key: Optional[str] = None, default: Optional[Any] = None) -> Optional[Any]:
        provider = self.connection('provider')
        if provider is None:
            return None

        return provider if key is None else provider.get(key, default)

    def with_connection_provider(self, provider_id: str, provider_name: Optional[str] = None) -> THasConnection:
        self._data.update({'connection': merge(self._data.get('connection', {}), {'provider': {
            'id': provider_id,
            'name': provider_name,
        }})})
        return self

    def connection_vendor(self, key: Optional[str] = None, default: Optional[Any] = None) -> Optional[Any]:
        vendor = self.connection('vendor')
        if vendor is None:
            return None

        return vendor if key is None else vendor.get(key, default)

    def with_connection_vendor(self, vendor_id: str, vendor_name: Optional[str] = None) -> THasConnection:
        self._data.update({'connection': merge(self._data.get('connection', {}), {'vendor': {
            'id': vendor_id,
            'name': vendor_name,
        }})})
        return self

    def connection_hub(self, key: Optional[str] = None, default: Optional[Any] = None) -> Optional[Any]:
        hub = self.connection('hub')
        if hub is None:
            return None

        return hub if key is None else hub.get(key, default)

    def with_connection_hub(self, hub_id: str, hub_name: Optional[str] = None) -> THasConnection:
        self._data.update({'connection': merge(self._data.get('connection', {}), {'hub': {
            'id': hub_id,
            'name': hub_name,
        }})})
        return self


class HasContract:
    _data: dict

    def contract(self, key: Optional[str] = None, default: Optional[Any] = None) -> Optional[Any]:
        contract = self._data.get('contract')
        if contract is None:
            return None

        return contract if key is None else contract.get(key, default)

    def with_contract(self, contract_id: str, contract_name: Optional[str] = None) -> THasContract:
        self._data.update({'contract': merge(self._data.get('contract', {}), {
            'id': contract_id,
            'name': contract_name,
        })})
        return self


class HasEvents:
    _data: dict

    def events(self, key: Optional[str] = None, default: Optional[Any] = None) -> Optional[Any]:
        events = self._data.get('events')
        if events is None:
            return None

        return events if key is None else events.get(key, default)

    def with_events(self, created: datetime, updated: datetime) -> THasEvents:
        self._data.update({'events': merge(self._data.get('events', {}), {
            'created': {'at': created.isoformat()},
            'updated': {'at': updated.isoformat()},
        })})
        return self


class HasMarketplace:
    _data: dict

    def marketplace(self, key: Optional[str] = None, default: Optional[Any] = None) -> Optional[Any]:
        marketplace = self._data.get('marketplace')
        if marketplace is None:
            return None

        return marketplace if key is None else marketplace.get(key, default)

    def with_marketplace(self, marketplace_id: str, marketplace_name: Optional[str] = None) -> THasMarketplace:
        self._data.update({'marketplace': merge(self._data.get('marketplace', {}), {
            'id': marketplace_id,
            'name': marketplace_name,
        })})
        return self


class HasParameters:
    _data: dict

    def params(self) -> List[Dict[Any, Any]]:
        return self._data.get('params', [])

    def param(self, param_id: str, key: Optional[str] = None, default: Optional[Any] = None) -> Optional[Any]:
        parameter = find_by_id(self.params(), param_id)
        if parameter is None:
            raise MissingParameterError(f'Missing parameter {param_id}', param_id)

        return parameter if key is None else parameter.get(key, default)

    def with_params(self, params: List[dict]) -> THasParameters:
        for param in params:
            self.with_param(**param)
        return self

    def with_param(
            self,
            param_id: str,
            value: Optional[Union[str, dict, list]] = None,
            value_error: Optional[str] = None,
            value_type: str = 'text',
            create: bool = True,
    ) -> THasParameters:
        try:
            param = self.param(param_id)
        except MissingParameterError:
            if create is False:
                raise
            param = {'id': param_id}
            self._data.update({'params': self.params() + [param]})

        members = make_param(param_id, value, value_error, value_type)
        param.update({k: v for k, v in members.items() if v is not None})
        return self


class HasProduct:
    _data: dict

    def product(self, key: Optional[str] = None, default: Optional[Any] = None) -> Optional[Any]:
        product = self._data.get('product')
        if product is None:
            return None

        return product if key is None else product.get(key, default)

    def with_product(self, product_id: str, product_status: str = 'published') -> THasProduct:
        self._data.update({'product': merge(self._data.get('product', {}), {
            'id': product_id,
            'status': product_status,
        })})
        return self


class HasReadWriteOperations:
    _data: dict

    def with_member(self, key: str, value: Any):
        self._data.update({key: value})
        return self

    def without_member(self, key: str) -> THasReadWriteOperations:
        self._data.pop(key, None)
        return self

    def get(self, key: Optional[str] = None, default: Optional[Any] = None) -> Optional[Any]:
        return self._data.get(key, default)

    def raw(self, deep_copy: bool = False) -> dict:
        return deepcopy(self._data) if deep_copy else self._data
