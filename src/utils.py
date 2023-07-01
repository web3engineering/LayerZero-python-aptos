def full_address(address):
    raw_value = address.replace("0x", "")
    hexadecimal = raw_value.zfill(64).encode()
    return hexadecimal


ZERO_ADDRESS_HEX = full_address("0x0").decode()


def is_same_address(address1, address2):
    return full_address(address1).decode() == full_address(address2).decode()


def is_zero_address(address):
    return is_same_address(address, ZERO_ADDRESS_HEX)


def merge_config(config, default_config):
    merged_config = default_config.copy()
    if not is_zero_address(config["oracle"]):
        merged_config["oracle"] = config["oracle"]
    if not is_zero_address(config["relayer"]):
        merged_config["relayer"] = config["relayer"]
    if config["inbound_confirmations"] > 0:
        merged_config["inbound_confirmations"] = config["inbound_confirmations"]
    if config["outbound_confirmations"] > 0:
        merged_config["outbound_confirmations"] = config["outbound_confirmations"]
    return merged_config
