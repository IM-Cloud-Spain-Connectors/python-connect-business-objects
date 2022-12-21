from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any, Dict, List, Optional


class EventsSource(ABC):
    @abstractmethod
    def events(self, key: Optional[str] = None, default: Optional[Any] = None) -> Optional[Any]:
        """
        Provide access to the events object.
        :param key: str If provided will return the key value if available.
        :param default: Any If provided will return default value if key value is not found.
        :return: Optional[Any] The requested value by key, the whole marketplace dict or None.
        """


class MarketplaceSource(ABC):  # pragma: no cover
    @abstractmethod
    def marketplace(self, key: Optional[str] = None, default: Optional[Any] = None) -> Optional[Any]:
        """
        Provide access to the marketplace object.
        :param key: str If provided will return the key value if available.
        :param default: Any If provided will return default value if key value is not found.
        :return: Optional[Any] The requested value by key, the whole marketplace dict or None.
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


class ContractSource(ABC):
    @abstractmethod
    def contract(self, key: Optional[str] = None, default: Optional[Any] = None) -> Optional[Any]:
        """
        Provide access to the contract object.
        :param key: str If provided will return the key value if available.
        :param default: Any If provided will return default value if key value is not found.
        :return: Optional[Any] The requested value by key, the whole contract dict or None.
        """


class RequestSource(
    MarketplaceSource,
    ParametersSource,
    EventsSource,
    ContractSource,
    ABC,
):  # pragma: no cover
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
    def get(self, key: Optional[str] = None, default: Optional[Any] = None) -> Optional[Any]:
        """
        Provides the required value by key.
        :param key: str If provided will return the key value if available.
        :param default: Any If provided will return default value if key value is not found.
        :return: Optional[Any] The requested value by key or None if not available.
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


class AssetSource(
    MarketplaceSource,
    ParametersSource,
    ContractSource,
    ABC,
):
    pass


class TierConfigurationSource(
    MarketplaceSource,
    ABC,
):
    pass
