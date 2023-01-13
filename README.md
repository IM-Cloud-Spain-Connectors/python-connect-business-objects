# Python Connect Business Objects

[![Test](https://github.com/othercodes/python-connect-business-objects/actions/workflows/test.yml/badge.svg)](https://github.com/othercodes/python-connect-business-objects/actions/workflows/test.yml)

Connect Business Object (Request, Asset and Tier Configuration) Interface.

## Installation

The easiest way to install the Connect Business Objects library is to get the latest version from PyPI:

```bash
# using poetry
poetry add rndi-connect-business-objects
# using pip
pip install rndi-connect-business-objects
```

## The Contracts

This package provides the following contracts or interfaces:

* `ConfigurationSource`
* `ConfigurationBuilder`
* `ConnectionSource`
* `ConnectionBuilder`
* `ContractSource`
* `ContractBuilder`
* `EventsSource`
* `EventsBuilder`
* `MarketplaceSource`
* `MarketPlaceBuilder`
* `ParametersSource`
* `ProductSource`
* `ProductBuilder`
* `RequestSource`
* `RequestBuilder`
* `AssetSource`
* `AssetBuilder`
* `TierConfigurationSource`
* `TierConfigurationBuilder`

## The Adapters

This package provides several adapters and mixins that implements the contracts above. The main Adapters are:

### Request

Allow you to operate with a Connect Request Object (Asset Request or Tier Config Request).

* Contracts: `RequestSource`, `RequestBuilder`.
* Mixins: `HasContract`, `HasEvents`, `HasMarketplace`, `HasParameters`, `RequestSource`.

```python
from rndi.connect.business_objects.adapters import Request

# Create a new Request and set some values.
r = Request()
r.with_id('PR-000-000-001')
r.with_type('purchase')
r.with_status('pending')

# You can read the values too.
r.id()  # PR-000-000-001
```

### Asset

Allow you to operate with a Connect Asset Object.

* Contracts: `AssetSource`, `AssetBuilder`.
* Mixins: `HasConfiguration`, `HasConnection`, `HasContract`, `HasMarketplace`, `HasParameters`, `HasProduct`.

```python
from rndi.connect.business_objects.adapters import Asset

# Create a new Asset and set some values.
a = Asset()
a.with_id('AS-000-000-001')
a.with_status('active')
a.with_external_id('123456789')
a.with_external_uid('9fb50525-a4a4-41a7-ace0-dc3c73796d32')
a.with_product('PRD-000-000-100', 'enabled')

# You can read the values too.
a.id()  # AS-000-000-001
```

### TierConfiguration

Allow you to operate with a Connect Tier Configuration Object.

* Contracts: `TierConfigurationSource`, `TierConfigurationBuilder`.
* Mixins: `HasConfiguration`, `HasConnection`, `HasMarketplace`, `HasParameters`, `HasProduct`.

```python
from rndi.connect.business_objects.adapters import TierConfiguration

# Create a new TierConfiguration and set some values.
t = TierConfiguration()
t.with_id('TC-000-000-000')
t.with_status('active')
t.with_marketplace('MP-12345')

# You can read the values too.
t.id()  # TC-000-000-000
```
