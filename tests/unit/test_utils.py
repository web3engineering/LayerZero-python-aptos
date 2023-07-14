from src.utils import (
    get_raw_address,
    get_u64_raw_address,
    full_address,
    is_same_address,
    is_zero_address,
    merge_config
)


def test_get_raw_address():
    assert get_raw_address('0xaabbcc') == 'aabbcc'


def test_get_u64_raw_address():
    assert get_u64_raw_address('0xaabbccc') == "000000000000000000000000000000000000000000000000000000000aabbccc"


def test_full_address():
    assert isinstance(full_address('0xaabbcc'), bytes)
    assert full_address('0xaa') == b'00000000000000000000000000000000000000000000000000000000000000aa'


def test_is_same_address():
    assert is_same_address('0x0', '0x0')
    assert not is_same_address('0x0', '0x1')


def test_is_zero_address():
    assert is_zero_address('0x0')
    assert not is_zero_address('0x1')


def test_merge_config():
    config = {
        'oracle': '0x0',
        'relayer': '0x1',
        'inbound_confirmations': 2,
        'outbound_confirmations': 3,
    }
    default_config = {
        'oracle': '0x0',
        'relayer': '0x0',
        'inbound_confirmations': 0,
        'outbound_confirmations': 0,
    }
    expected_result = {
        'oracle': '0x0',
        'relayer': '0x1',
        'inbound_confirmations': 2,
        'outbound_confirmations': 3,
    }
    assert merge_config(config, default_config) == expected_result
