#
# This file is part of the Ingram Micro CloudBlue RnD Integration Connectors SDK.
#
# Copyright (c) 2023 Ingram Micro. All Rights Reserved.
#
from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any, Dict, List, Optional, TypeVar, Union

TConfigurationBuilder = TypeVar('TConfigurationBuilder', bound='ConfigurationBuilder')
TConnectionBuilder = TypeVar('TConnectionBuilder', bound='ConnectionBuilder')
TContractBuilder = TypeVar('TContractBuilder', bound='ContractBuilder')
TEventsBuilder = TypeVar('TEventsBuilder', bound='EventsBuilder')
TMarketPlaceBuilder = TypeVar('TMarketPlaceBuilder', bound='MarketPlaceBuilder')
TParametersBuilder = TypeVar('TParametersBuilder', bound='ParametersBuilder')
TProductBuilder = TypeVar('TProductBuilder', bound='ProductBuilder')
TRequestBuilder = TypeVar('TRequestBuilder', bound='RequestBuilder')
TAssetBuilder = TypeVar('TAssetBuilder', bound='AssetBuilder')
TTierConfigurationBuilder = TypeVar('TTierConfigurationBuilder', bound='TierConfigurationBuilder')


class ConfigurationSource(ABC):
    @abstractmethod
    def configuration_params(self) -> List[Dict[Any, Any]]:
        """
        Provide the list of configuration parameters.
        :return: List[Dict[Any, Any]]
        """

    @abstractmethod
    def configuration_param(
            self,
            param_id: str,
            key: Optional[str] = None,
            default: Optional[Any] = None,
    ) -> Optional[Any]:
        """
        Provide the requested configuration parameter by id.
        :param param_id: str The unique parameter id.
        :param key: str If provided will return the key value if available.
        :param default: Any If provided will return default value if key value is not found.
        :return:
        """


class ConfigurationBuilder(ABC):
    @abstractmethod
    def with_configuration_params(self, params: List[dict]) -> TConfigurationBuilder:
        """
        Replaces the whole list of configuration parameters.
        :param params: List[dict] The new list of parameters.
        :return: TConfigurationBuilder
        """

    @abstractmethod
    def with_configuration_param(
            self,
            param_id: str,
            value: Optional[Union[str, dict, list]] = None,
            value_error: Optional[str] = None,
            value_type: Optional[str] = None,
            title: Optional[str] = None,
            description: Optional[str] = None,
    ) -> TConfigurationBuilder:
        """
        Replaces a configuration parameter information by id.
        :param param_id: str The unique parameter id.
        :param value: Optional[Union[str, dict, list]] The new parameter value.
        :param value_error: Optional[str] The new parameter value error.
        :param value_type: Optional[str] The new parameter type.
        :param title: Optional[str] The new parameter title.
        :param description: Optional[str] The new parameter description.
        :return: TConfigurationBuilder
        """


class ConnectionSource(ABC):
    @abstractmethod
    def connection(self, key: Optional[str] = None, default: Optional[Any] = None) -> Optional[Any]:
        """
        Provide access to the connection object.
        :param key: str If provided will return the key value if available.
        :param default: Any If provided will return default value if key value is not found.
        :return: Optional[Any] The requested value by key, the whole connection dict or None.
        """

    @abstractmethod
    def connection_provider(self, key: Optional[str] = None, default: Optional[Any] = None) -> Optional[Any]:
        """
        Provide access to the connection provider object.
        :param key: str If provided will return the key value if available.
        :param default: Any If provided will return default value if key value is not found.
        :return: Optional[Any] The requested value by key, the whole connection provider dict or None.
        """

    @abstractmethod
    def connection_vendor(self, key: Optional[str] = None, default: Optional[Any] = None) -> Optional[Any]:
        """
        Provide access to the connection vendor object.
        :param key: str If provided will return the key value if available.
        :param default: Any If provided will return default value if key value is not found.
        :return: Optional[Any] The requested value by key, the whole connection vendor dict or None.
        """

    @abstractmethod
    def connection_hub(self, key: Optional[str] = None, default: Optional[Any] = None) -> Optional[Any]:
        """
        Provide access to the connection hub object.
        :param key: str If provided will return the key value if available.
        :param default: Any If provided will return default value if key value is not found.
        :return: Optional[Any] The requested value by key, the whole connection hub dict or None.
        """


class ConnectionBuilder(ABC):
    @abstractmethod
    def with_connection(
            self,
            connection_id: str,
            connection_type: str,
            provider: Optional[dict] = None,
            vendor: Optional[dict] = None,
            hub: Optional[dict] = None,
    ) -> TConnectionBuilder:
        """
        Replaces the connection objects information with the given values.
        :param connection_id: str The connection id.
        :param connection_type: str The connection type.
        :param provider: dict The new provider connection information.
        :param vendor: dit The new vendor connection information.
        :param hub: dict The new hub connection information.s
        :return:
        """

    @abstractmethod
    def with_connection_provider(self, provider_id: str, provider_name: Optional[str] = None) -> TConnectionBuilder:
        """
        Replaces the provider connection information with the given values.
        :param provider_id: str The provider id.
        :param provider_name: str The provider name.
        :return: TConnectionBuilder
        """

    @abstractmethod
    def with_connection_vendor(self, vendor_id: str, vendor_name: Optional[str] = None) -> TConnectionBuilder:
        """
        Replaces the provider connection information with the given values.
        :param vendor_id: str The vendor id.
        :param vendor_name: str The vendor name.
        :return: TConnectionBuilder
        """

    @abstractmethod
    def with_connection_hub(self, hub_id: str, hub_name: Optional[str] = None) -> TConnectionBuilder:
        """
        Replaces the hub connection information with the given values.
        :param hub_id: str The hub id.
        :param hub_name: str The hub name.
        :return: TConnectionBuilder
        """


class ContractSource(ABC):
    @abstractmethod
    def contract(self, key: Optional[str] = None, default: Optional[Any] = None) -> Optional[Any]:
        """
        Provide access to the contract object.
        :param key: str If provided will return the key value if available.
        :param default: Any If provided will return default value if key value is not found.
        :return: Optional[Any] The requested value by key, the whole contract dict or None.
        """


class ContractBuilder(ABC):
    @abstractmethod
    def with_contract(self, contract_id: str, contract_name: Optional[str] = None) -> TContractBuilder:
        """
        Replaces the contract object values with the given ones.
        :param contract_id: str The new contract id.
        :param contract_name: Optional[str] The new contract name.
        :return: TContractBuilder
        """


class EventsSource(ABC):
    @abstractmethod
    def events(self, key: Optional[str] = None, default: Optional[Any] = None) -> Optional[Any]:
        """
        Provide access to the events object.
        :param key: str If provided will return the key value if available.
        :param default: Any If provided will return default value if key value is not found.
        :return: Optional[Any] The requested value by key, the whole marketplace dict or None.
        """


class EventsBuilder(ABC):
    @abstractmethod
    def with_events(self, created: datetime, updated: datetime) -> TEventsBuilder:
        """
        Replaces the events object values with the given ones.
        :param created: datetime The new created at value.
        :param updated: datetime The new updated at value.
        :return: TEventsBuilder
        """


class MarketplaceSource(ABC):
    @abstractmethod
    def marketplace(self, key: Optional[str] = None, default: Optional[Any] = None) -> Optional[Any]:
        """
        Provide access to the marketplace object.
        :param key: str If provided will return the key value if available.
        :param default: Any If provided will return default value if key value is not found.
        :return: Optional[Any] The requested value by key, the whole marketplace dict or None.
        """


class MarketPlaceBuilder(ABC):
    @abstractmethod
    def with_marketplace(self, marketplace_id: str, marketplace_name: Optional[str] = None) -> TMarketPlaceBuilder:
        """
        Replaces the marketplace object values with the given ones.
        :param marketplace_id: str The new marketplace id.
        :param marketplace_name: Optional[str] The new marketplace name.
        :return: TMarketPlaceBuilder
        """


class ParametersSource(ABC):
    @abstractmethod
    def params(self) -> List[Dict[Any, Any]]:
        """
        Provide the list of parameters.
        :return: List[Dict[Any, Any]] The list of parameters.
        """

    @abstractmethod
    def param(self, param_id: str, key: Optional[str] = None, default: Optional[Any] = None) -> Optional[Any]:
        """
        Provide access to the parameter object.
        :param param_id: str The unique parameter id.
        :param key: str If provided will return the key value if available.
        :param default: Any If provided will return default value if key value is not found.
        :raises: MissingParameterError If the requested parameter by id is not available.
        :return: Optional[Any] The requested value by key or the whole parameter by id.
        """


class ParametersBuilder(ABC):
    @abstractmethod
    def with_params(self, params: List[dict]) -> TParametersBuilder:
        """
        Replaces the whole list of parameters with the given one.
        :param params: LIst[dict] The new list of parameters.
        :return: TParametersBuilder
        """

    @abstractmethod
    def with_param(
            self,
            param_id: str,
            value: Optional[Union[str, dict, list]] = None,
            value_error: Optional[str] = None,
            value_type: str = 'text',
            create: bool = True,
    ) -> TParametersBuilder:
        """
        Replaces a parameter value with the given ones.
        :param param_id: str The parameters id operate with, if no exist will be created.
        :param value: Optional[Union[str, dict, list]] The parameter value.
        :param value_error: Optional[str] The parameter value error.
        :param value_type: str The parameter value type (text, object, email...).
        :param create: bool If True, creates dynamically the parameter if not exists.
        :return: TParametersBuilder
        """


class ProductSource(ABC):
    @abstractmethod
    def product(self, key: Optional[str] = None, default: Optional[Any] = None) -> Optional[Any]:
        """
        Provide access to the product object.
        :param key: str If provided will return the key value if available.
        :param default: Any If provided will return default value if key value is not found.
        :return: Optional[Any] The requested value by key, the whole product dict or None.
        """


class ProductBuilder(ABC):
    @abstractmethod
    def with_product(self, product_id: str, product_status: str = 'published') -> TProductBuilder:
        """
        Replaces the asset product with the given values.
        :param product_id: str The new product id.
        :param product_status: str The new product status.
        :return: TAssetBuilder
        """


class RequestSource(ContractSource, EventsSource, MarketplaceSource, ParametersSource, ABC):
    @abstractmethod
    def request_model(self) -> str:
        """
        Provides the request model: asset or configuration.
        :return: str The model: asset or configuration.
        """

    @abstractmethod
    def is_tier_config_request(self) -> bool:
        """
        True of the request model is a configuration, false otherwise.
        :return: bool
        """

    @abstractmethod
    def is_asset_request(self) -> bool:
        """
        True of the request model is an asset, false otherwise.
        :return: bool
        """

    @abstractmethod
    def id(self) -> Optional[str]:
        """
        Provides the unique id of the request if it is available.
        :return: Optional[str] The id, None if not available.
        """

    @abstractmethod
    def type(self) -> Optional[str]:
        """
        Provides the request type.
        One of: adjustment, purchase, change, suspend, resume, cancel, setup
        :return: Optional[str] The type, None if not available.
        """

    @abstractmethod
    def status(self) -> Optional[str]:
        """
        Provides the request status.
        One of: pending, draft, inquiring, tiers_setup, approved, rescheduled, revoking, revoked, failed.
        :return: Optional[str] The status, None if not available.
        """

    @abstractmethod
    def created(self) -> Optional[datetime]:
        """
        Provides the request created datetime object.
        :return: Optional[datetime] The datetime object, None if not available.
        """

    def updated(self) -> Optional[datetime]:
        """
        Provides the request updated datetime object.
        :return: Optional[datetime] The datetime object, None if not available.
        """

    @abstractmethod
    def note(self) -> Optional[str]:
        """
        Provides the request note.
        :return: Optional[str] The note, None if not available.
        """

    @abstractmethod
    def reason(self) -> Optional[str]:
        """
        Provides the request reason.
        :return: Optional[str] The reason, None if not available.
        """

    @abstractmethod
    def assignee(self, key: Optional[str] = None, default: Optional[Any] = None) -> Optional[Any]:
        """
        Provide access to the assignee object.
        :param key: str If provided will return the key value if available.
        :param default: Any If provided will return default value if key value is not found.
        :return: Optional[Any] The requested value by key, the whole assignee dict or None.
        """

    @abstractmethod
    def asset(self) -> AssetSource:
        """
        Provides the AssetSource object if it is available.
        :return: AssetSource
        """

    @abstractmethod
    def tier_configuration(self) -> TierConfigurationSource:
        """
        Provides the TierConfigurationSource if it is available.
        :return:
        """


class RequestBuilder(ContractBuilder, EventsBuilder, MarketPlaceBuilder, ParametersBuilder, ABC):
    @abstractmethod
    def with_id(self, request_id: str) -> TRequestBuilder:
        """
        Replaces the request id with the given value.
        :param request_id: str
        :return: TRequestBuilder
        """

    @abstractmethod
    def with_type(self, request_type: str) -> TRequestBuilder:
        """
        Replaces the request type with the given value.
        :param request_type: str
        :return: TRequestBuilders
        """

    @abstractmethod
    def with_status(self, request_status) -> TRequestBuilder:
        """
        Replaces the request status with the given value.
        :param request_status: str
        :return: TRequestBuilder
        """

    @abstractmethod
    def with_created(self, created: datetime) -> TRequestBuilder:
        """
        Replaces the request created date time with the given value.
        :param created: datetime
        :return: TRequestBuilder
        """

    @abstractmethod
    def with_updated(self, updated: datetime) -> TRequestBuilder:
        """
        Replaces the request updated date time with the given value.
        :param updated: datetime
        :return: TRequestBuilder
        """

    @abstractmethod
    def with_note(self, note: str) -> TRequestBuilder:
        """
        Replaces the request note with the given value.
        :param note: str
        :return: TRequestBuilder
        """

    @abstractmethod
    def with_reason(self, reason: str) -> TRequestBuilder:
        """
        Replaces the request reason with the given value.
        :param reason: str
        :return: TRequestBuilder
        """

    @abstractmethod
    def with_assignee(self, assignee_id: str, assignee_name: str, assignee_email: str) -> TRequestBuilder:
        """
        Replaces the assignee information with the given values.
        :param assignee_id: str The assignee unique id.
        :param assignee_name: str The assignee name.
        :param assignee_email: str The assignee email.
        :return: TRequestBuilder
        """

    @abstractmethod
    def with_asset(self, asset: TAssetBuilder) -> TRequestBuilder:
        """
        Replaces the asset object with the given one.
        :param asset: TAssetBuilder
        :return: TRequestBuilder
        """

    @abstractmethod
    def with_tier_configuration(self, configuration: TTierConfigurationBuilder) -> TRequestBuilder:
        """
        Replaces the tier configuration with the given one.
        :param configuration: TTierConfigurationBuilder
        :return: TRequestBuilder
        """


class AssetSource(
    ConfigurationSource,
    ConnectionSource,
    ContractSource,
    MarketplaceSource,
    ParametersSource,
    ProductSource,
    ABC,
):
    @abstractmethod
    def id(self) -> Optional[str]:
        """
        Provides the unique id of the asset if it is available.
        :return: Optional[str] The id, None if not available.
        """

    @abstractmethod
    def status(self) -> Optional[str]:
        """
        Provides the asset status.
        :return: Optional[str] The status, None if not available.
        """

    @abstractmethod
    def external_id(self) -> Optional[str]:
        """
        Provides the external id.
        :return: Optional[str]
        """

    @abstractmethod
    def external_uid(self) -> Optional[str]:
        """
        Provides the external uid.
        :return: Optional[str]
        """

    @abstractmethod
    def tier(self, tier_name: str, key: Optional[str] = None, default: Optional[Any] = None) -> Optional[Any]:
        """
        Provides access to the tier objects.
        :param tier_name: str The tier name we want to access (customer, tier1 or tier2).
        :param key: str If provided will return the key value if available.
        :param default: Any If provided will return default value if key value is not found.
        :return: Optional[Any]
        """

    def tier_customer(self, key: Optional[str] = None, default: Optional[Any] = None) -> Optional[Any]:
        """
        Provides access to the tier customer object.
        :param key: str If provided will return the key value if available.
        :param default: Any If provided will return default value if key value is not found.
        :return: Optional[Any]
        """

    def tier_tier1(self, key: Optional[str] = None, default: Optional[Any] = None) -> Optional[Any]:
        """
        Provides access to the tier tier1 object.
        :param key: str If provided will return the key value if available.
        :param default: Any If provided will return default value if key value is not found.
        :return: Optional[Any]
        """

    def tier_tier2(self, key: Optional[str] = None, default: Optional[Any] = None) -> Optional[Any]:
        """
        Provides access to the tier tier2 object.
        :param key: str If provided will return the key value if available.
        :param default: Any If provided will return default value if key value is not found.
        :return: Optional[Any]
        """

    @abstractmethod
    def items(self) -> List[Dict[Any, Any]]:
        """
        Provides asset the item list.
        :return: List[Dict[Any, Any]]
        """

    @abstractmethod
    def item(self, item_id: str, key: Optional[str] = None, default: Optional[Any] = None) -> Optional[Any]:
        """
        Provide access to an item object.
        :param item_id: str The unique parameter id.
        :param key: str If provided will return the key value if available.
        :param default: Any If provided will return default value if key value is not found.
        :raises: MissingParameterError If the requested parameter by id is not available.
        :return: Optional[Any] The requested value by key or the whole parameter by id.
        """

    @abstractmethod
    def item_params(self, item_id: str) -> List[Dict[Any, Any]]:
        """
        Provide the list of parameters of an item by id.
        :param item_id: str The unique item id.
        :return: List[Dict[Any, Any]]
        """

    @abstractmethod
    def item_param(
            self,
            item_id: str,
            param_id: str,
            key: Optional[str] = None,
            default: Optional[Any] = None,
    ) -> Optional[Any]:
        """
        Provide access to a parameter from an item by id.
        :param item_id: str The unique item id.
        :param param_id: str The unique parameter id.
        :param key: str If provided will return the key value if available.
        :param default: Any If provided will return default value if key value is not found.
        :raises: MissingItemError  If the requested parameter by id is not available.
        :return: Optional[Any] The requested value by key or the whole parameter by id.
        """


class AssetBuilder(
    ConfigurationBuilder,
    ConnectionBuilder,
    ContractBuilder,
    MarketPlaceBuilder,
    ParametersBuilder,
    ProductBuilder,
    ABC,
):
    @abstractmethod
    def with_id(self, asset_id: str) -> TAssetBuilder:
        """
        Replaces the asset id with the given value.
        :param asset_id: str
        :return: TAssetBuilder
        """

    @abstractmethod
    def with_external_id(self, asset_external_id: str) -> TAssetBuilder:
        """
        Replaces the asset external id with the given value.
        :param asset_external_id: str The new external id.
        :return: TAssetBuilder
        """

    @abstractmethod
    def with_external_uid(self, asset_external_uid: str) -> TAssetBuilder:
        """
        Replaces the asset external id with the given value.
        :param asset_external_uid: str The new external uid.
        :return: TAssetBuilder
        """

    @abstractmethod
    def with_status(self, asset_status: str) -> TAssetBuilder:
        """
        Replaces the asset status with the given value.
        :param asset_status: str The new status.
        :return: TAssetBuilder
        """

    @abstractmethod
    def with_tier(self, tier_name: str, tier: Union[str, dict]) -> TAssetBuilder:
        """
        Replaces the tier information by name customer, tier1 or tier2.
        :param tier_name: str The tier name to replace.
        :param tier: str The tier information.
        :return: TAssetBuilder
        """

    @abstractmethod
    def with_tier_customer(self, customer: Union[str, dict]) -> TAssetBuilder:
        """
        Replaces the tier customer information.
        :param customer: dict The new tier customer information.
        :return: TAssetBuilder
        """

    @abstractmethod
    def with_tier_tier1(self, tier1: Union[str, dict]) -> TAssetBuilder:
        """
        Replaces the tier1 information.
        :param tier1: dict The new tier1 information.
        :return: TAssetBuilder
        """

    @abstractmethod
    def with_tier_tier2(self, tier2: Union[str, dict]) -> TAssetBuilder:
        """
        Replaces the tier2 information.
        :param tier2: dict The new tier2 information.
        :return: TAssetBuilder
        """

    @abstractmethod
    def with_items(self, items: List[dict]) -> TAssetBuilder:
        """
        Replaces the list of items with the given one.
        :param items: List[dict] The new list of items.
        :return: TAssetBuilder
        """

    @abstractmethod
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
    ) -> TAssetBuilder:
        """
        Replaces an item with the given values.
        :param item_id: str The unique item id.
        :param item_mpn: str The unique mpn.
        :param quantity: str The quantity.
        :param old_quantity: Optional[str] The old quantity.
        :param item_type: Optional[str] The new item type.
        :param period: Optional[str] The item period.
        :param unit: Optional[str] The item unit.
        :param display_name: Optional[str] The item display name.
        :param global_id: Optional[str] The unique global id.
        :param params: Optional[List[dict]] The list of params of the item.
        :return: TAssetBuilder
        """

    @abstractmethod
    def with_item_params(self, item_id: str, params: List[dict]) -> TAssetBuilder:
        """
        Replace the parameters of an item by id.
        :param item_id: str The unique item id.
        :param params: The new list of parameters for the item.
        :return: TAssetBuilder
        """

    @abstractmethod
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
    ) -> TAssetBuilder:
        """
        Replaces an item parameter by id.
        :param item_id: str The unique item id.
        :param param_id: str The unique param id.
        :param value: Optional[Union[str, dict, list]] The new parameter value.
        :param value_type: Optional[str] The new parameter value type
        :param title: Optional[str] The new parameter title.
        :param description: Optional[str] The new parameter description.
        :param scope: Optional[str] The new parameter scope.
        :param phase: Optional[str] The new parameter phase.
        :return:
        """


class TierConfigurationSource(
    ConfigurationSource,
    ConnectionSource,
    MarketplaceSource,
    ParametersSource,
    ProductSource,
    ABC,
):
    @abstractmethod
    def id(self) -> Optional[str]:
        """
        Provides the unique id of the tier configuration if it is available.
        :return: Optional[str] The id, None if not available.
        """

    @abstractmethod
    def status(self) -> Optional[str]:
        """
        Provides the tier configuration status.
        :return: Optional[str] The status, None if not available.
        """

    @abstractmethod
    def tier_level(self) -> Optional[int]:
        """
        Provides the tier level.
        :return: Optional[int] The tier level, None if not available.
        """

    @abstractmethod
    def account(self, key: Optional[str] = None, default: Optional[Any] = None) -> Optional[Any]:
        """
        Provides the account object of the tier configuration.
        :param key: str If provided will return the key value if available.
        :param default: Any If provided will return default value if key value is not found.
        :return: Optional[Any]
        """


class TierConfigurationBuilder(
    ConfigurationBuilder,
    ConnectionBuilder,
    MarketPlaceBuilder,
    ParametersBuilder,
    ProductBuilder,
    ABC,
):
    @abstractmethod
    def with_id(self, tier_configuration_id: str) -> TTierConfigurationBuilder:
        """
        Replaces the tier configuration id with the given value.
        :param tier_configuration_id: str
        :return: TTierConfigurationBuilder
        """

    @abstractmethod
    def with_status(self, tier_configuration_status: str) -> TTierConfigurationBuilder:
        """
        Replaces the tier configuration status with the given value.
        :param tier_configuration_status: str The new status.
        :return: TTierConfigurationBuilder
        """

    @abstractmethod
    def with_tier_level(self, level: int) -> TTierConfigurationBuilder:
        """
        Replaces the tier level with the given value.
        :param level: int The new tier level value.
        :return: TTierConfigurationBuilder
        """

    @abstractmethod
    def with_account(self, account: Optional[Union[str, dict]] = 'random') -> TTierConfigurationBuilder:
        """
        Replaces the tier account of the tier configuration.
        :param account: Optional[Union[str, dict]] The tier account id or the new dictionary with
        the new values, if "random" is passed, a new random reseller account will be generated.
        :return: TTierConfigurationBuilder
        """
