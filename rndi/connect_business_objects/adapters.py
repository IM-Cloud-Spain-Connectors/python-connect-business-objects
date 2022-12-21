#
# This file is part of the Ingram Micro CloudBlue Connect Processors Toolkit.
#
# Copyright (c) 2022 Ingram Micro. All Rights Reserved.
#
from __future__ import annotations

from copy import deepcopy
from datetime import datetime
from typing import Any, Dict, List, Optional, Union

from rndi.connect_business_objects.contracts import AssetSource, RequestSource, TierConfigurationSource
from rndi.connect_business_objects.helpers import find_by_id, make_param, make_tier, merge, request_model
from rndi.connect_business_objects.exceptions import MissingItemError, MissingParameterError


class Request(RequestSource):
    def __init__(self, request: Optional[dict] = None):
        request = {} if request is None else request

        if not isinstance(request, dict):
            raise ValueError('Request must be a dictionary.')

        self._request = request

    def __repr__(self) -> str:
        return '{class_name}(request={request})'.format(
            class_name=self.__class__.__name__,
            request=self._request,
        )

    def __str__(self) -> str:
        return str(self._request)

    def raw(self, deep_copy: bool = False) -> dict:
        return deepcopy(self._request) if deep_copy else self._request

    def request_model(self) -> str:
        return request_model(self.raw())

    def is_tier_config_request(self) -> bool:
        return 'tier-config' == self.request_model()

    def is_asset_request(self) -> bool:
        return 'asset' == self.request_model()

    def without(self, key: str) -> Request:
        self._request.pop(key, None)
        return self

    def get(self, key: Optional[str] = None, default: Optional[Any] = None) -> Optional[Any]:
        return self._request.get(key, default)

    def id(self) -> Optional[str]:
        return self._request.get('id')

    def with_id(self, request_id: str) -> Request:
        self._request.update({'id': request_id})
        return self

    def type(self) -> Optional[str]:
        return self._request.get('type')

    def with_type(self, request_type: str) -> Request:
        self._request.update({'type': request_type})
        return self

    def status(self) -> Optional[str]:
        return self._request.get('status')

    def with_status(self, request_status) -> Request:
        self._request.update({'status': request_status})
        return self

    def created(self) -> Optional[datetime]:
        created = self._request.get('created')
        if created is not None:
            return datetime.fromisoformat(created)

        return created

    def with_created(self, created: datetime) -> Request:
        self._request.update({'created': created.isoformat()})
        return self

    def updated(self) -> Optional[datetime]:
        updated = self._request.get('updated')
        if updated is not None:
            return datetime.fromisoformat(updated)

        return updated

    def with_updated(self, updated: datetime) -> Request:
        self._request.update({'updated': updated.isoformat()})
        return self

    def marketplace(self, key: Optional[str] = None, default: Optional[Any] = None) -> Optional[Any]:
        marketplace = self._request.get('marketplace')
        if marketplace is None:
            return None

        return marketplace if key is None else marketplace.get(key, default)

    def with_marketplace(self, marketplace_id: str, marketplace_name: Optional[str] = None) -> Request:
        self._request.update({'marketplace': merge(self._request.get('marketplace', {}), {
            'id': marketplace_id,
            'name': marketplace_name,
        })})
        return self

    def note(self) -> Optional[str]:
        return self._request.get('note')

    def with_note(self, note: str) -> Request:
        self._request.update({'note': note})
        return self

    def reason(self) -> Optional[str]:
        return self._request.get('reason')

    def with_reason(self, reason: str) -> Request:
        self._request.update({'reason': reason})
        return self

    def assignee(self, key: Optional[str] = None, default: Optional[Any] = None) -> Optional[Any]:
        assignee = self._request.get('assignee')
        if assignee is None:
            return None

        return assignee if key is None else assignee.get(key, default)

    def with_assignee(self, assignee_id: str, assignee_name: str, assignee_email: str) -> Request:
        self._request.update({'assignee': merge(self._request.get('assignee', {}), {
            'id': assignee_id,
            'name': assignee_name,
            'email': assignee_email,
        })})
        return self

    def params(self) -> List[Dict[Any, Any]]:
        return self._request.get('params', [])

    def param(self, param_id: str, key: Optional[str] = None, default: Optional[Any] = None) -> Optional[Any]:
        parameter = find_by_id(self.params(), param_id)
        if parameter is None:
            raise MissingParameterError(f'Missing parameter {param_id}', param_id)

        return parameter if key is None else parameter.get(key, default)

    def with_params(self, params: List[dict]) -> Request:
        for param in params:
            self.with_param(**param)
        return self

    def with_param(
            self,
            param_id: str,
            value: Optional[Union[str, dict, list]] = None,
            value_error: Optional[str] = None,
            value_type: str = 'text',
    ) -> Request:
        try:
            param = self.param(param_id)
        except MissingParameterError:
            param = {'id': param_id}
            self._request.update({'params': self.params() + [param]})

        members = make_param(param_id, value, value_error, value_type)
        param.update({k: v for k, v in members.items() if v is not None})
        return self

    def asset(self) -> Asset:
        return Asset(self._request.get('asset', {}))

    def with_asset(self, asset: Union[dict, Asset]) -> Request:
        asset = asset if isinstance(asset, dict) else asset.raw()
        self._request.update({'asset': asset})
        return self

    def tier_configuration(self) -> TierConfiguration:
        return TierConfiguration(self._request.get('configuration', {}))

    def with_tier_configuration(self, configuration: Union[dict, TierConfiguration]) -> Request:
        configuration = configuration if isinstance(configuration, dict) else configuration.raw()
        self._request.update({'configuration': configuration})
        return self

    def events(self, key: Optional[str] = None, default: Optional[Any] = None) -> Optional[Any]:
        events = self._request.get('events')
        if events is None:
            return None

        return events if key is None else events.get(key, default)

    def contract(self, key: Optional[str] = None, default: Optional[Any] = None) -> Optional[Any]:
        contract = self._request.get('contract')
        if contract is None:
            return None

        return contract if key is None else contract.get(key, default)


class Asset(AssetSource):
    def __init__(self, asset: Optional[dict] = None):
        if asset is None:
            asset = {}

        if not isinstance(asset, dict):
            raise ValueError('Asset must be a dictionary.')

        self._asset = asset

    def __repr__(self) -> str:
        return '{class_name}(asset={asset})'.format(
            class_name=self.__class__.__name__,
            asset=self._asset,
        )

    def __str__(self) -> str:
        return str(self._asset)

    def raw(self, deep_copy: bool = False) -> dict:
        return deepcopy(self._asset) if deep_copy else self._asset

    def without(self, key: str) -> Asset:
        self._asset.pop(key, None)
        return self

    def id(self) -> Optional[str]:
        return self._asset.get('id')

    def with_id(self, asset_id: str) -> Asset:
        self._asset.update({'id': asset_id})
        return self

    def external_id(self) -> Optional[str]:
        return self._asset.get('external_id')

    def with_external_id(self, asset_external_id: str) -> Asset:
        self._asset.update({'external_id': asset_external_id})
        return self

    def external_uid(self) -> Optional[str]:
        return self._asset.get('external_uid')

    def with_external_uid(self, asset_external_uid: str) -> Asset:
        self._asset.update({'external_uid': asset_external_uid})
        return self

    def status(self) -> Optional[str]:
        return self._asset.get('status')

    def with_status(self, asset_status: str) -> Asset:
        self._asset.update({'status': asset_status})
        return self

    def product(self, key: Optional[str] = None, default: Optional[Any] = None) -> Optional[Any]:
        product = self._asset.get('product')
        if product is None:
            return None

        return product if key is None else product.get(key, default)

    def with_product(self, product_id: str, product_status: str = 'published') -> Asset:
        self._asset.update({'product': merge(self._asset.get('product', {}), {
            'id': product_id,
            'status': product_status,
        })})
        return self

    def marketplace(self, key: Optional[str] = None, default: Optional[Any] = None) -> Optional[Any]:
        marketplace = self._asset.get('marketplace')
        if marketplace is None:
            return None

        return marketplace if key is None else marketplace.get(key, default)

    def with_marketplace(self, marketplace_id: str, marketplace_name: Optional[str] = None) -> Asset:
        self._asset.update({'marketplace': merge(self._asset.get('marketplace', {}), {
            'id': marketplace_id,
            'name': marketplace_name,
        })})
        return self

    def connection(self, key: Optional[str] = None, default: Optional[Any] = None) -> Optional[Any]:
        connection = self._asset.get('connection')
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
    ) -> Asset:
        self._asset.update({'connection': merge(self._asset.get('connection', {}), {
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

    def with_connection_provider(self, provider_id: str, provider_name: Optional[str] = None) -> Asset:
        self._asset.update({'connection': merge(self._asset.get('connection', {}), {'provider': {
            'id': provider_id,
            'name': provider_name,
        }})})
        return self

    def connection_vendor(self, key: Optional[str] = None, default: Optional[Any] = None) -> Optional[Any]:
        vendor = self.connection('vendor')
        if vendor is None:
            return None

        return vendor if key is None else vendor.get(key, default)

    def with_connection_vendor(self, vendor_id: str, vendor_name: Optional[str] = None) -> Asset:
        self._asset.update({'connection': merge(self._asset.get('connection', {}), {'vendor': {
            'id': vendor_id,
            'name': vendor_name,
        }})})
        return self

    def connection_hub(self, key: Optional[str] = None, default: Optional[Any] = None) -> Optional[Any]:
        hub = self.connection('hub')
        if hub is None:
            return None

        return hub if key is None else hub.get(key, default)

    def with_connection_hub(self, hub_id: str, hub_name: Optional[str] = None) -> Asset:
        self._asset.update({'connection': merge(self._asset.get('connection', {}), {'hub': {
            'id': hub_id,
            'name': hub_name,
        }})})
        return self

    def tier(self, tier_name: str, key: Optional[str] = None, default: Optional[Any] = None) -> Optional[Any]:
        tier = self._asset.get('tiers', {}).get(tier_name)
        if tier is None:
            return None

        return tier if key is None else tier.get(key, default)

    def with_tier(self, tier_name: str, tier: Union[str, dict]) -> Asset:
        if 'tiers' not in self._asset:
            self._asset.update({'tiers': {}})

        if tier_name not in self._asset.get('tiers', {}):
            self._asset.get('tiers', {}).update({tier_name: {}})

        if isinstance(tier, str):
            self._asset.get('tiers', {}).get(tier_name, {}).clear()
            tier = make_tier(tier_name) if tier == 'random' else {'id': tier}

        self._asset.get('tiers', {}).get(tier_name).update(
            merge(self._asset.get('tiers', {}).get(tier_name), tier),
        )
        return self

    def tier_customer(self, key: Optional[str] = None, default: Optional[Any] = None) -> Optional[Any]:
        return self.tier('customer', key, default)

    def with_tier_customer(self, customer: Union[str, dict]) -> Asset:
        return self.with_tier('customer', customer)

    def tier_tier1(self, key: Optional[str] = None, default: Optional[Any] = None) -> Optional[Any]:
        return self.tier('tier1', key, default)

    def with_tier_tier1(self, tier1: Union[str, dict]) -> Asset:
        return self.with_tier('tier1', tier1)

    def tier_tier2(self, key: Optional[str] = None, default: Optional[Any] = None) -> Optional[Any]:
        return self.tier('tier2', key, default)

    def with_tier_tier2(self, tier2: Union[str, dict]) -> Asset:
        return self.with_tier('tier2', tier2)

    def params(self) -> List[Dict[Any, Any]]:
        return self._asset.get('params', [])

    def param(self, param_id: str, key: Optional[str] = None, default: Optional[Any] = None) -> Optional[Any]:
        parameter = find_by_id(self.params(), param_id)
        if parameter is None:
            raise MissingParameterError(f'Missing parameter {param_id}', param_id)

        return parameter if key is None else parameter.get(key, default)

    def with_params(self, params: List[dict]) -> Asset:
        for param in params:
            self.with_param(**param)
        return self

    def with_param(
            self,
            param_id: str,
            value: Optional[Union[str, dict, list]] = None,
            value_error: Optional[str] = None,
            value_type: Optional[str] = None,
            title: Optional[str] = None,
            description: Optional[str] = None,
    ) -> Asset:
        try:
            param = self.param(param_id)
        except MissingParameterError:
            param = {'id': param_id}
            self._asset.update({'params': self.params() + [param]})

        members = make_param(param_id, value, value_error, value_type, title, description)
        param.update({k: v for k, v in members.items() if v is not None})
        return self

    def items(self) -> List[Dict[Any, Any]]:
        return self._asset.get('items', [])

    def item(self, item_id: str, key: Optional[str] = None, default: Optional[Any] = None) -> Optional[Any]:
        item = find_by_id(self.items(), item_id)
        if item is None:
            raise MissingItemError(f'Missing item {item_id}', item_id)

        return item if key is None else item.get(key, default)

    def with_items(self, items: List[dict]):
        for item in items:
            self.with_item(**item)
        return self

    def with_item(
            self,
            item_id: str,
            item_mpn: str,
            quantity: str = '1',
            old_quantity: Optional[str] = None,
            item_type: Optional[str] = None,
            period: Optional[str] = None,
            unit: Optional[str] = None,
            display_name: Optional[str] = None,
            global_id: Optional[str] = None,
            params: Optional[List[dict]] = None,
    ) -> Asset:
        try:
            item = self.item(item_id)
        except MissingItemError:
            item = {'id': item_id}
            self._asset.update({'items': self.items() + [item]})

        members = {
            'global_id': global_id,
            'display_name': display_name,
            'mpn': item_mpn,
            'quantity': quantity,
            'old_quantity': old_quantity,
            'params': [],
            'item_type': item_type,
            'period': period,
            'type': unit,
        }

        item.update({k: v for k, v in members.items() if v is not None})
        self.with_item_params(item_id, [] if params is None else params)
        return self

    def item_params(self, item_id: str) -> List[Dict[Any, Any]]:
        return self.item(item_id, 'params', [])

    def item_param(
            self,
            item_id: str,
            param_id: str,
            key: Optional[str] = None,
            default: Optional[Any] = None,
    ) -> Optional[Any]:
        param = find_by_id(self.item(item_id, 'params', []), param_id)
        if param is None:
            raise MissingItemError(f'Missing item {param_id} in item {item_id}', item_id)

        return param if key is None else param.get(key, default)

    def with_item_params(self, item_id: str, params: List[dict]) -> Asset:
        for param in params:
            self.with_item_param(**{'item_id': item_id, **param})
        return self

    def with_item_param(
            self,
            item_id: str,
            param_id: str,
            value: Optional[Union[str, dict, list]] = None,
            value_type: Optional[str] = None,
            title: Optional[str] = None,
            description: Optional[str] = None,
            scope: Optional[str] = None,
            phase: Optional[str] = None,
    ) -> Asset:
        item = self.item(item_id)
        param = find_by_id(item.get('params', []), param_id)
        if param is None:
            param = {'id': param_id}
            item.get('params', []).append(param)

        members = make_param(
            param_id,
            value,
            None,
            value_type,
            title,
            description,
            'item' if scope is None else scope,
            'configuration' if phase is None else phase,
        )
        param.update({k: v for k, v in members.items() if v is not None})
        return self

    def configuration_params(self) -> List[Dict[Any, Any]]:
        return self._asset.get('configuration', {}).get('params', [])

    def configuration_param(
            self,
            param_id: str,
            key: Optional[str] = None,
            default: Optional[Any] = None,
    ) -> Optional[Any]:
        param = find_by_id(self.configuration_params(), param_id)
        if param is None:
            raise MissingParameterError(f'Missing configuration parameter {param_id}', param_id)

        return param if key is None else param.get(key, default)

    def with_configuration_params(self, params: List[dict]) -> Asset:
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
    ) -> Asset:
        if 'configuration' not in self._asset:
            self._asset.update({'configuration': {}})

        if 'params' not in self._asset.get('configuration', {}):
            self._asset.get('configuration', {}).update({'params': []})

        try:
            param = self.configuration_param(param_id)
        except MissingParameterError:
            param = {'id': param_id}
            self._asset.get('configuration', {}).get('params', []).append(param)

        members = make_param(param_id, value, value_error, value_type, title, description)
        param.update({k: v for k, v in members.items() if v is not None})
        return self

    def contract(self, key: Optional[str] = None, default: Optional[Any] = None) -> Optional[Any]:
        contract = self._asset.get('contract')
        if contract is None:
            return None

        return contract if key is None else contract.get(key, default)


class TierConfiguration(TierConfigurationSource):
    def __init__(self, tier_config: Optional[dict] = None):
        if tier_config is None:
            tier_config = {}

        if not isinstance(tier_config, dict):
            raise ValueError('Tier Configuration must be a dictionary.')

        self._tier_config = tier_config

    def __repr__(self) -> str:
        return '{class_name}(tier_config={tier_config})'.format(
            class_name=self.__class__.__name__,
            tier_config=self._tier_config,
        )

    def __str__(self) -> str:
        return str(self._tier_config)

    def raw(self, deep_copy: bool = False) -> dict:
        return deepcopy(self._tier_config) if deep_copy else self._tier_config

    def without(self, key: str) -> TierConfiguration:
        self._tier_config.pop(key, None)
        return self

    def id(self) -> Optional[str]:
        return self._tier_config.get('id')

    def with_id(self, tier_configuration_id: str) -> TierConfiguration:
        self._tier_config.update({'id': tier_configuration_id})
        return self

    def status(self) -> Optional[str]:
        return self._tier_config.get('status')

    def with_status(self, tier_configuration_status: str) -> TierConfiguration:
        self._tier_config.update({'status': tier_configuration_status})
        return self

    def product(
            self,
            key: Optional[str] = None,
            default: Optional[Any] = None,
    ) -> Optional[Any]:
        product = self._tier_config.get('product')
        if product is None:
            return None

        return product if key is None else product.get(key, default)

    def with_product(
            self,
            product_id: str,
            product_status: str = 'published',
    ) -> TierConfiguration:
        self._tier_config.update({'product': merge(self._tier_config.get('product', {}), {
            'id': product_id,
            'status': product_status,
        })})
        return self

    def marketplace(
            self,
            key: Optional[str] = None,
            default: Optional[Any] = None,
    ) -> Optional[Any]:
        marketplace = self._tier_config.get('marketplace')
        if marketplace is None:
            return None

        return marketplace if key is None else marketplace.get(key, default)

    def with_marketplace(
            self,
            marketplace_id: str,
            marketplace_name: Optional[str] = None,
    ) -> TierConfiguration:
        self._tier_config.update({'marketplace': merge(self._tier_config.get('marketplace', {}), {
            'id': marketplace_id,
            'name': marketplace_name,
        })})
        return self

    def connection(
            self,
            key: Optional[str] = None,
            default: Optional[Any] = None,
    ) -> Optional[Any]:
        connection = self._tier_config.get('connection')
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
    ) -> TierConfiguration:
        self._tier_config.update({'connection': merge(self._tier_config.get('connection', {}), {
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

    def connection_provider(
            self,
            key: Optional[str] = None,
            default: Optional[Any] = None,
    ) -> Optional[Any]:
        provider = self.connection('provider')
        if provider is None:
            return None

        return provider if key is None else provider.get(key, default)

    def with_connection_provider(
            self,
            provider_id: str,
            provider_name: Optional[str] = None,
    ) -> TierConfiguration:
        self._tier_config.update({'connection': merge(self._tier_config.get('connection', {}), {'provider': {
            'id': provider_id,
            'name': provider_name,
        }})})
        return self

    def connection_vendor(
            self,
            key: Optional[str] = None,
            default: Optional[Any] = None,
    ) -> Optional[Any]:
        vendor = self.connection('vendor')
        if vendor is None:
            return None

        return vendor if key is None else vendor.get(key, default)

    def with_connection_vendor(
            self,
            vendor_id: str,
            vendor_name: Optional[str] = None,
    ) -> TierConfiguration:
        self._tier_config.update({'connection': merge(self._tier_config.get('connection', {}), {'vendor': {
            'id': vendor_id,
            'name': vendor_name,
        }})})
        return self

    def connection_hub(
            self,
            key: Optional[str] = None,
            default: Optional[Any] = None,
    ) -> Optional[Any]:
        hub = self.connection('hub')
        if hub is None:
            return None

        return hub if key is None else hub.get(key, default)

    def with_connection_hub(
            self,
            hub_id: str,
            hub_name: Optional[str] = None,
    ) -> TierConfiguration:
        self._tier_config.update({'connection': merge(self._tier_config.get('connection', {}), {'hub': {
            'id': hub_id,
            'name': hub_name,
        }})})
        return self

    def account(
            self,
            key: Optional[str] = None,
            default: Optional[Any] = None,
    ) -> Optional[Any]:
        account = self._tier_config.get('account')
        if account is None:
            return None

        return account if key is None else account.get(key, default)

    def with_account(
            self,
            account: Optional[Union[str, dict]] = 'random',
    ) -> TierConfiguration:
        if isinstance(account, str):
            self._tier_config.get('account', {}).clear()
            account = make_tier('reseller') if account == 'random' else {'id': account}

        self._tier_config.update({'account': merge(self._tier_config.get('account', {}), account)})
        return self

    def tier_level(self) -> Optional[int]:
        return self._tier_config.get('tier_level')

    def with_tier_level(self, level: int) -> TierConfiguration:
        self._tier_config.update({'tier_level': level})
        return self

    def params(self) -> List[dict]:
        return self._tier_config.get('params', [])

    def param(
            self,
            param_id: str,
            key: Optional[str] = None,
            default: Optional[Any] = None,
    ) -> Optional[Any]:
        parameter = find_by_id(self.params(), param_id)
        if parameter is None:
            raise MissingParameterError(f'Missing parameter {param_id}', param_id)

        return parameter if key is None else parameter.get(key, default)

    def with_params(self, params: List[dict]) -> TierConfiguration:
        for param in params:
            self.with_param(**param)
        return self

    def with_param(
            self,
            param_id: str,
            value: Optional[Union[str, dict, list]] = None,
            value_error: Optional[str] = None,
            value_type: Optional[str] = None,
    ) -> TierConfiguration:
        try:
            param = self.param(param_id)
        except MissingParameterError:
            param = {'id': param_id}
            self._tier_config.update({'params': self.params() + [param]})

        members = make_param(param_id, value, value_error, value_type)
        param.update({k: v for k, v in members.items() if v is not None})
        return self

    def configuration_params(self) -> List[dict]:
        return self._tier_config.get('configuration', {}).get('params', [])

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

    def with_configuration_param(
            self,
            param_id: str,
            value: Optional[Union[str, dict, list]] = None,
            value_error: Optional[str] = None,
            value_type: Optional[str] = None,
    ) -> TierConfiguration:
        if 'configuration' not in self._tier_config:
            self._tier_config.update({'configuration': {}})

        if 'params' not in self._tier_config.get('configuration', {}):
            self._tier_config.get('configuration', {}).update({'params': []})

        try:
            param = self.configuration_param(param_id)
        except MissingParameterError:
            param = {'id': param_id}
            self._tier_config.get('configuration', {}).get('params', []).append(param)

        members = make_param(param_id, value, value_error, value_type)
        param.update({k: v for k, v in members.items() if v is not None})
        return self
