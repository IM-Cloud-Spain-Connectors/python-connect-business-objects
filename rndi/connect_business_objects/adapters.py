#
# This file is part of the Ingram Micro CloudBlue Connect Processors Toolkit.
#
# Copyright (c) 2023 Ingram Micro. All Rights Reserved.
#
from __future__ import annotations

from copy import deepcopy
from datetime import datetime
from typing import Any, Dict, List, Optional, Union

from rndi.connect_business_objects.contracts import (
    AssetBuilder,
    AssetSource,
    RequestBuilder,
    RequestSource,
    TierConfigurationBuilder,
    TierConfigurationSource,
)
from rndi.connect_business_objects.helpers import find_by_id, make_param, make_tier, merge, request_model
from rndi.connect_business_objects.exceptions import MissingItemError
from rndi.connect_business_objects.mixin import (
    HasConfiguration,
    HasConnection,
    HasContract,
    HasEvents,
    HasMarketplace,
    HasParameters,
    HasProduct,
)


class Request(
    HasContract,
    HasEvents,
    HasMarketplace,
    HasParameters,
    RequestSource,
    RequestBuilder,
):
    def __init__(self, request: Optional[dict] = None):
        request = {} if request is None else request

        if not isinstance(request, dict):
            raise ValueError('Request must be a dictionary.')

        self._data = request

    def __repr__(self) -> str:
        return '{class_name}(request={request})'.format(
            class_name=self.__class__.__name__,
            request=self._data,
        )

    def __str__(self) -> str:
        return str(self._data)

    def raw(self, deep_copy: bool = False) -> dict:
        return deepcopy(self._data) if deep_copy else self._data

    def without(self, key: str) -> Request:
        self._data.pop(key, None)
        return self

    def get(self, key: Optional[str] = None, default: Optional[Any] = None) -> Optional[Any]:
        return self._data.get(key, default)

    def request_model(self) -> str:
        return request_model(self.raw())

    def is_tier_config_request(self) -> bool:
        return 'tier-config' == self.request_model()

    def is_asset_request(self) -> bool:
        return 'asset' == self.request_model()

    def id(self) -> Optional[str]:
        return self._data.get('id')

    def with_id(self, request_id: str) -> Request:
        self._data.update({'id': request_id})
        return self

    def type(self) -> Optional[str]:
        return self._data.get('type')

    def with_type(self, request_type: str) -> Request:
        self._data.update({'type': request_type})
        return self

    def status(self) -> Optional[str]:
        return self._data.get('status')

    def with_status(self, request_status) -> Request:
        self._data.update({'status': request_status})
        return self

    def created(self) -> Optional[datetime]:
        created = self._data.get('created')
        return created if created is None else datetime.fromisoformat(created)

    def with_created(self, created: datetime) -> Request:
        self._data.update({'created': created.isoformat()})
        return self

    def updated(self) -> Optional[datetime]:
        updated = self._data.get('updated')
        return updated if updated is None else datetime.fromisoformat(updated)

    def with_updated(self, updated: datetime) -> Request:
        self._data.update({'updated': updated.isoformat()})
        return self

    def note(self) -> Optional[str]:
        return self._data.get('note')

    def with_note(self, note: str) -> Request:
        self._data.update({'note': note})
        return self

    def reason(self) -> Optional[str]:
        return self._data.get('reason')

    def with_reason(self, reason: str) -> Request:
        self._data.update({'reason': reason})
        return self

    def assignee(self, key: Optional[str] = None, default: Optional[Any] = None) -> Optional[Any]:
        assignee = self._data.get('assignee')
        if assignee is None:
            return None

        return assignee if key is None else assignee.get(key, default)

    def with_assignee(self, assignee_id: str, assignee_name: str, assignee_email: str) -> Request:
        self._data.update({'assignee': merge(self._data.get('assignee', {}), {
            'id': assignee_id,
            'name': assignee_name,
            'email': assignee_email,
        })})
        return self

    def asset(self) -> Asset:
        return Asset(self._data.get('asset', {}))

    def with_asset(self, asset: Asset) -> Request:
        self._data.update({'asset': asset.raw()})
        return self

    def tier_configuration(self) -> TierConfiguration:
        return TierConfiguration(self._data.get('configuration', {}))

    def with_tier_configuration(self, configuration: TierConfiguration) -> Request:
        self._data.update({'configuration': configuration.raw()})
        return self


class Asset(
    HasConfiguration,
    HasConnection,
    HasContract,
    HasMarketplace,
    HasParameters,
    HasProduct,
    AssetSource,
    AssetBuilder,
):
    def __init__(self, asset: Optional[dict] = None):
        if asset is None:
            asset = {}

        if not isinstance(asset, dict):
            raise ValueError('Asset must be a dictionary.')

        self._data = asset

    def __repr__(self) -> str:
        return '{class_name}(asset={asset})'.format(
            class_name=self.__class__.__name__,
            asset=self._data,
        )

    def __str__(self) -> str:
        return str(self._data)

    def raw(self, deep_copy: bool = False) -> dict:
        return deepcopy(self._data) if deep_copy else self._data

    def without(self, key: str) -> Asset:
        self._data.pop(key, None)
        return self

    def id(self) -> Optional[str]:
        return self._data.get('id')

    def with_id(self, asset_id: str) -> Asset:
        self._data.update({'id': asset_id})
        return self

    def external_id(self) -> Optional[str]:
        return self._data.get('external_id')

    def with_external_id(self, asset_external_id: str) -> Asset:
        self._data.update({'external_id': asset_external_id})
        return self

    def external_uid(self) -> Optional[str]:
        return self._data.get('external_uid')

    def with_external_uid(self, asset_external_uid: str) -> Asset:
        self._data.update({'external_uid': asset_external_uid})
        return self

    def status(self) -> Optional[str]:
        return self._data.get('status')

    def with_status(self, asset_status: str) -> Asset:
        self._data.update({'status': asset_status})
        return self

    def tier(self, tier_name: str, key: Optional[str] = None, default: Optional[Any] = None) -> Optional[Any]:
        tier = self._data.get('tiers', {}).get(tier_name)
        if tier is None:
            return None

        return tier if key is None else tier.get(key, default)

    def with_tier(self, tier_name: str, tier: Union[str, dict]) -> Asset:
        if 'tiers' not in self._data:
            self._data.update({'tiers': {}})

        if tier_name not in self._data.get('tiers', {}):
            self._data.get('tiers', {}).update({tier_name: {}})

        if isinstance(tier, str):
            self._data.get('tiers', {}).get(tier_name, {}).clear()
            tier = make_tier(tier_name) if tier == 'random' else {'id': tier}

        self._data.get('tiers', {}).get(tier_name).update(
            merge(self._data.get('tiers', {}).get(tier_name), tier),
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

    def items(self) -> List[Dict[Any, Any]]:
        return self._data.get('items', [])

    def item(self, item_id: str, key: Optional[str] = None, default: Optional[Any] = None) -> Optional[Any]:
        item = find_by_id(self.items(), item_id)
        if item is None:
            raise MissingItemError(f'Missing item {item_id}', item_id)

        return item if key is None else item.get(key, default)

    def with_items(self, items: List[dict]) -> Asset:
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
            self._data.update({'items': self.items() + [item]})

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


class TierConfiguration(
    HasConfiguration,
    HasConnection,
    HasMarketplace,
    HasParameters,
    HasProduct,
    TierConfigurationSource,
    TierConfigurationBuilder,
):
    def __init__(self, tier_config: Optional[dict] = None):
        if tier_config is None:
            tier_config = {}

        if not isinstance(tier_config, dict):
            raise ValueError('Tier Configuration must be a dictionary.')

        self._data = tier_config

    def __repr__(self) -> str:
        return '{class_name}(tier_config={tier_config})'.format(
            class_name=self.__class__.__name__,
            tier_config=self._data,
        )

    def __str__(self) -> str:
        return str(self._data)

    def raw(self, deep_copy: bool = False) -> dict:
        return deepcopy(self._data) if deep_copy else self._data

    def without(self, key: str) -> TierConfiguration:
        self._data.pop(key, None)
        return self

    def id(self) -> Optional[str]:
        return self._data.get('id')

    def with_id(self, tier_configuration_id: str) -> TierConfiguration:
        self._data.update({'id': tier_configuration_id})
        return self

    def status(self) -> Optional[str]:
        return self._data.get('status')

    def with_status(self, tier_configuration_status: str) -> TierConfiguration:
        self._data.update({'status': tier_configuration_status})
        return self

    def account(self, key: Optional[str] = None, default: Optional[Any] = None) -> Optional[Any]:
        account = self._data.get('account')
        if account is None:
            return None

        return account if key is None else account.get(key, default)

    def with_account(self, account: Optional[Union[str, dict]] = 'random') -> TierConfiguration:
        if isinstance(account, str):
            self._data.get('account', {}).clear()
            account = make_tier('reseller') if account == 'random' else {'id': account}

        self._data.update({'account': merge(self._data.get('account', {}), account)})
        return self

    def tier_level(self) -> Optional[int]:
        return self._data.get('tier_level')

    def with_tier_level(self, level: int) -> TierConfiguration:
        self._data.update({'tier_level': level})
        return self
