import pprint
from helper_func import (generate_binary_subnet_mask, subnet_to_octet, needed_bits_to_complete_octet,
                         octet_dec_to_bin, apply_pipe, calc_bin_with_pipe, construct_network_address,
                         format_address_into_string, classify_address_class, calc_num_of_subnets, calc_num_of_host,
                         calc_subnet_increment)

pp = pprint.PrettyPrinter(indent=2, depth=8, sort_dicts=False)

user_ip_address = [172, 20, 10, 45]
user_subnet_mask = 22

subnet_mask = f"/{user_subnet_mask}"
on_octet = subnet_to_octet(n=user_subnet_mask)
binary_subnet_mask = generate_binary_subnet_mask(n=user_subnet_mask)
network_portion = user_subnet_mask
host_portion = 32 - user_subnet_mask
bits_needed_to_complete_corresponding_octet = needed_bits_to_complete_octet(binary_subnet_mask[on_octet-1])
target_octet_on_address_dec = user_ip_address[on_octet - 1]
target_octet_on_address_bin = octet_dec_to_bin(target_octet_on_address_dec)
target_octet_bin_pipe_applied = apply_pipe(
    binary=octet_dec_to_bin(target_octet_on_address_dec),
    at=bits_needed_to_complete_corresponding_octet
)
left_side_pipe_value = calc_bin_with_pipe(binary=target_octet_bin_pipe_applied)

# The Network Address
copy_ip_address_1 = user_ip_address.copy()
network_address = construct_network_address(
    ip_add=copy_ip_address_1,
    oc_tar=on_octet,
    left_side_pipe_val=left_side_pipe_value
)

# Number of Available Subnets
address_class = classify_address_class(address=user_ip_address)
number_of_available_subnets = calc_num_of_subnets(
    address_default_subnet_mask=address_class["default_subnet_mask"],
    custom_subnet_mask=user_subnet_mask
)

# Number of Hosts
number_of_hosts = calc_num_of_host(custom_subnet_mask=user_subnet_mask)

# Subnet Increment Value
subnet_increment_value = calc_subnet_increment(missing_bit=bits_needed_to_complete_corresponding_octet)


identification = {
    "ip_address": format_address_into_string(address=user_ip_address),
    "subnet_mask": subnet_mask,
    "class": {
        "IP Address Class": address_class['class'],
        "Default Subnet Mask": f"/{address_class['default_subnet_mask']}",
        "Class Range": f"{address_class["1st_octet_range"][0]} to {address_class["1st_octet_range"][1]}"
    },
    "on_octet": on_octet,
    "binary_subnet_mask": format_address_into_string(address=binary_subnet_mask, is_binary=True),
    "network_portion": network_portion,
    "host_portion": host_portion,
    f"bits_needed_to_complete_octet_{on_octet}": bits_needed_to_complete_corresponding_octet,
    "target_octet": {
        f"octet_{on_octet}_on_address_dec": target_octet_on_address_dec,
        f"octet_{on_octet}_on_address_bin": format_address_into_string(
            address=target_octet_on_address_bin, is_binary=True),
        f"pipe_symbol_applied": format_address_into_string(address=target_octet_bin_pipe_applied, is_binary=True),
        f"left_side_of_pipe_val": left_side_pipe_value,
    },
    f"network_address": f"{format_address_into_string(network_address)}/{user_subnet_mask}",
    "Number Of Available Subnets": number_of_available_subnets,
    "Number of Hosts per Subnet": number_of_hosts,
    "Subnet Increment Value": subnet_increment_value,
}

pp.pprint(identification)
