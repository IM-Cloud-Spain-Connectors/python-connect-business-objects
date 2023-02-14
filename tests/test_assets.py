import pytest
from rndi.connect.business_objects.adapters import Asset
from rndi.connect.business_objects.exceptions import MissingItemError


def test_asset_builder_should_raise_value_error_on_invalid_init_value():
    with pytest.raises(ValueError):
        Asset([])


def test_asset_builder_should_return_none_on_not_initialized_members():
    a = Asset()
    a.with_item('ITM_ID_1', 'ITM_MPN_1')

    assert a.product() is None
    assert a.marketplace() is None
    assert a.connection() is None
    assert a.connection_provider() is None
    assert a.connection_vendor() is None
    assert a.connection_hub() is None
    assert a.tier('customer') is None
    assert a.tier('tier1') is None
    assert a.tier('tier2') is None


def test_asset_builder_should_remove_required_member_from_asset():
    a = Asset()
    a.with_id('PR-0000-0000-0000-100')
    a.without_member('id')

    assert a.id() is None


def test_asset_builder_should_raise_exception_on_adding_parameter_to_missing_asset_item():
    with pytest.raises(MissingItemError):
        a = Asset()
        a.with_item('ITEM_ID_001', 'ITEM_MPN_001')
        a.item_param('ITEM_ID_001', 'PARAM_ID', 'The value')

    with pytest.raises(MissingItemError):
        a = Asset()
        a.with_item_param('MISSING', 'PARAM_ID', 'The value')


def test_asset_builder_should_build_successfully_a_valid_asset():
    a = Asset()
    a.with_id('AS-001')
    a.with_status('active')
    a.with_external_id('123456789')
    a.with_external_uid('9fb50525-a4a4-41a7-ace0-dc3c73796d32')
    a.with_product('PRD-000-000-100', 'disabled')
    a.with_tier_customer('random')
    a.with_tier_tier1('random')
    a.with_tier_tier2('random')
    a.with_tier_tier2({'contact_info': {'country': 'ES'}})
    a.with_marketplace('MP-12345')
    a.with_connection(connection_id='CT-0000-0000-0000', connection_type='test',
                      provider={"id": "PA-800-926", "name": "Gamma Team Provider"},
                      vendor={"id": "VA-610-138", "name": "Gamma Team Vendor"},
                      hub={"id": "HB-0000-0000", "name": "None"})
    a.with_params([
        {'param_id': 'PARAM_ID_001', 'value': 'VALUE_001'},
        {'param_id': 'PARAM_ID_002', 'value': 'VALUE_002'},
        {'param_id': 'PARAM_ID_003', 'value': '', 'value_error': 'Some value error'},
        {'param_id': 'PARAM_ID_001', 'value': 'VALUE_001_UPDATED'},
    ])
    a.with_items([
        {
            'item_id': 'ITEM_ID_001',
            'item_mpn': 'ITEM_MPN_001',
            'params': [{'param_id': 'SOME_ITEM_PARAM_ID', 'value': 'ITEM_ID_001_PARAM_VALUE'}],
        },
        {
            'item_id': 'ITEM_ID_001',
            'item_mpn': 'ITEM_MPN_001_UPDATED',
        },
        {
            'item_id': 'ITEM_ID_001',
            'item_mpn': 'ITEM_MPN_001_UPDATED',
            'params': [{'param_id': 'SOME_ITEM_PARAM_ID', 'value': 'ITEM_ID_001_PARAM_VALUE_UPDATED'}],
        },
    ])
    a.with_configuration_params([
        {'param_id': 'AS_CFG_ID_001', 'value': 'Cfg value', 'value_error': 'Cfg error value'},
        {'param_id': 'AS_CFG_ID_001', 'value': 'Cfg value updated', 'value_error': 'Cfg error value updated'},
    ])

    raw = a.raw()

    assert raw['id'] == a.id() == 'AS-001'
    assert raw['status'] == a.status() == 'active'

    assert raw['external_id'] == a.external_id() == '123456789'
    assert raw['external_uid'] == a.external_uid() == '9fb50525-a4a4-41a7-ace0-dc3c73796d32'

    assert raw['marketplace']['id'] == a.marketplace('id') == 'MP-12345'

    assert a.tier_customer('id') is None
    assert raw['tiers']['customer']['external_id'] == a.tier_customer('external_id')
    assert raw['tiers']['customer']['external_uid'] == a.tier_customer('external_uid')
    assert a.tier_tier1('id') is None
    assert raw['tiers']['tier1']['external_id'] == a.tier_tier1('external_id')
    assert raw['tiers']['tier1']['external_uid'] == a.tier_tier1('external_uid')
    assert a.tier_tier2('id') is None
    assert raw['tiers']['tier2']['external_id'] == a.tier_tier2('external_id')
    assert raw['tiers']['tier2']['external_uid'] == a.tier_tier2('external_uid')
    assert raw['tiers']['tier2']['contact_info']['country'] == a.tier_tier2('contact_info', {}).get('country')
    assert a.tier_tier2('contact_info', {}).get('country') == 'ES'

    assert raw['connection']['id'] == a.connection('id') == 'CT-0000-0000-0000'
    assert raw['connection']['type'] == a.connection('type') == 'test'
    assert raw['connection']['provider']['id'] == a.connection_provider('id') == 'PA-800-926'
    assert raw['connection']['provider']['name'] == a.connection_provider('name') == 'Gamma Team Provider'
    assert raw['connection']['vendor']['id'] == a.connection_vendor('id') == 'VA-610-138'
    assert raw['connection']['vendor']['name'] == a.connection_vendor('name') == 'Gamma Team Vendor'
    assert raw['connection']['hub']['id'] == a.connection_hub('id') == 'HB-0000-0000'
    assert raw['connection']['hub']['name'] == a.connection_hub('name') == 'None'

    assert raw['product']['id'] == a.product('id') == 'PRD-000-000-100'
    assert raw['product']['status'] == a.product('status') == 'disabled'

    assert len(a.params()) == 3
    assert raw['params'][0]['id'] == a.param('PARAM_ID_001', 'id') == 'PARAM_ID_001'
    assert raw['params'][0]['value'] == a.param('PARAM_ID_001', 'value') == 'VALUE_001_UPDATED'

    assert raw['params'][1]['id'] == a.param('PARAM_ID_002', 'id') == 'PARAM_ID_002'
    assert raw['params'][1]['value'] == a.param('PARAM_ID_002', 'value') == 'VALUE_002'

    assert raw['params'][2]['id'] == a.param('PARAM_ID_003', 'id') == 'PARAM_ID_003'
    assert raw['params'][2]['value'] == a.param('PARAM_ID_003', 'value') == ''
    assert raw['params'][2]['value_error'] == a.param('PARAM_ID_003', 'value_error') == 'Some value error'

    assert len(a.items()) == 1
    assert raw['items'][0]['id'] == a.item('ITEM_ID_001', 'id') == 'ITEM_ID_001'
    assert raw['items'][0]['mpn'] == a.item('ITEM_ID_001', 'mpn') == 'ITEM_MPN_001_UPDATED'

    assert len(a.item_params('ITEM_ID_001')) == 1

    item = raw['items'][0]['params'][0]
    assert item['id'] == a.item_param('ITEM_ID_001', 'SOME_ITEM_PARAM_ID', 'id') == 'SOME_ITEM_PARAM_ID'
    assert item['value'] == a.item_param(
        'ITEM_ID_001',
        'SOME_ITEM_PARAM_ID',
        'value',
    ) == 'ITEM_ID_001_PARAM_VALUE_UPDATED'

    param = raw['configuration']['params'][0]
    assert param['id'] == a.configuration_param('AS_CFG_ID_001', 'id') == 'AS_CFG_ID_001'
    assert param['value'] == a.configuration_param('AS_CFG_ID_001', 'value') == 'Cfg value updated'
    assert param['value_error'] == a.configuration_param('AS_CFG_ID_001', 'value_error') == 'Cfg error value updated'
