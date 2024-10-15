import pprint
import sys
from helper_func import (generate_binary_subnet_mask, subnet_to_octet, needed_bits_to_complete_octet,
                         octet_dec_to_bin, apply_pipe, calc_bin_with_pipe, construct_network_address,
                         format_address_into_string, classify_address_class, calc_num_of_subnets, calc_num_of_host,
                         calc_subnet_increment, gen_subnet_table, octet_bin_to_dec, subnetting_logic_followed)

pp = pprint.PrettyPrinter(indent=2, depth=8, sort_dicts=False)

user_ip_address = [198, 22, 45, 193]
user_subnet_mask = 27

# Makesure the logic of subnetting is followed before proceeding the calculation
address_class = classify_address_class(address=user_ip_address)
try:
    if not subnetting_logic_followed(subnet_mask=user_subnet_mask, class_info=address_class):
        raise ValueError(
            "Subnetting Logic Error\n"
            f"You have Class {address_class['class']} IP Address, which have to follow its rules :\n"
            f"Default Subnet Mask : {address_class['default_subnet_mask']}\n"
            f"Subnetting Range (subnet mask) : /{address_class['subnetting_range'][0]} to "
            f"/{address_class['subnetting_range'][1]}"
        )
except ValueError as e:
    print(e)
    sys.exit(1)

# TODO: do something when user enter /31 subnet mask (section 8, 44)

subnet_mask = f"/{user_subnet_mask}"
on_octet = subnet_to_octet(n=user_subnet_mask)

# Translate slash notation subnet mask into binary
binary_subnet_mask = generate_binary_subnet_mask(n=user_subnet_mask)

# Translate binary notation subnet mask into decimal
decimal_subnet_mask = []
for bin_octet in binary_subnet_mask:
    decimal_subnet_mask.append(octet_bin_to_dec(bin_octet))

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
number_of_available_subnets = calc_num_of_subnets(
    address_default_subnet_mask=address_class["default_subnet_mask"],
    custom_subnet_mask=user_subnet_mask
)

# Number of Hosts
number_of_hosts = calc_num_of_host(custom_subnet_mask=user_subnet_mask)

# Subnet Increment Value
subnet_increment_value = calc_subnet_increment(missing_bit=bits_needed_to_complete_corresponding_octet)

# Generate subnet table
subnet_table = gen_subnet_table(network_address=network_address, target_octet=on_octet, n_subnets=number_of_available_subnets, n_host=number_of_hosts, increment_val=subnet_increment_value)

identification = {
    "IP Address": format_address_into_string(address=user_ip_address),
    "Subnet Mask": {
        "Slash Notation": subnet_mask,
        "Binary Subnet Mask": format_address_into_string(address=binary_subnet_mask, is_binary=True),
        "Decimal Subnet Mask": format_address_into_string(address=decimal_subnet_mask),
        "Network Portion": network_portion,
        "Host Portion": host_portion,
        "On Octet": on_octet,
        f"Bits Needed to Complete Octet-{on_octet}": bits_needed_to_complete_corresponding_octet,
    },
    "class": {
        "IP Address Class": address_class['class'],
        "Class Range": f"{address_class["1st_octet_range"][0]} to {address_class["1st_octet_range"][1]}",
        "Default Subnet Mask": f"/{address_class['default_subnet_mask']}",
        "Subnetting Range": f"/{address_class['subnetting_range'][0]} to /{address_class['subnetting_range'][1]}"
    },
    "Target Octet": {
        f"Octet-{on_octet} on Address Decimal Version": target_octet_on_address_dec,
        f"Octet-{on_octet} on Address Binary Version": format_address_into_string(
            address=target_octet_on_address_bin, is_binary=True),
        f"Pipe Symbol Applied": format_address_into_string(address=target_octet_bin_pipe_applied, is_binary=True),
        f"Left Side of Pipe Symbol Value": left_side_pipe_value,
    },
    f"Network Address": f"{format_address_into_string(network_address)}/{user_subnet_mask}",
    "Number Of Available Subnets": number_of_available_subnets,
    "Number of Hosts per Subnet": number_of_hosts,
    "Subnet Increment Value": subnet_increment_value,
}

pp.pprint(identification)

print("\nSubnet table (Network Address only):")
for subnet in subnet_table:
    print(subnet)
