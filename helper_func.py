import math

from typing import List

bits_value = [128, 64, 32, 16, 8, 4, 2, 1]

address_classes_and_subnet_mask = [
    {
        "class": "A",
        "1st_octet_range": [1, 126],
        "default_subnet_mask": 8,
        "subnetting_range": [8, 30]
    },
    {
        "class": "B",
        "1st_octet_range": [128, 191],
        "default_subnet_mask": 16,
        "subnetting_range": [16, 30]
    },
    {
        "class": "C",
        "1st_octet_range": [192, 223],
        "default_subnet_mask": 24,
        "subnetting_range": [24, 30]
    }
]


def classify_address_class(address: list) -> dict:
    """
    Classify the class of the IP Address.
    :param address: (list) Address to classify
    :return: (dict) complete information of the IP Address Class
    """
    user_octet_1 = address[0]

    if user_octet_1 == 0 or user_octet_1 == 127:
        raise Exception("Address is either identification for 'this network' or a loop back.")

    for address_class in address_classes_and_subnet_mask:
        octet_range = address_class['1st_octet_range']
        left_bound = octet_range[0]
        right_bound = octet_range[1]
        if left_bound <= user_octet_1 <= right_bound:
            return address_class


def subnetting_logic_followed(subnet_mask: int, class_info: dict) -> bool:
    """
    Check whether the Custom Subnet is in range of the Address Class's subnet mask boundary.
    :param subnet_mask: (int) user custom subnet
    :param class_info: (Dict) complete info of an Address (data from `classify_address_class` function)
    :return: (Bool) True if Custom Subnet is in range, False otherwise.
    """

    subnet_mask_left_bound = class_info['subnetting_range'][0]
    subnet_mask_right_bound = class_info['subnetting_range'][1]

    if subnet_mask_left_bound <= subnet_mask <= subnet_mask_right_bound:
        return True
    else:
        return False


def generate_binary_subnet_mask(n: int) -> list:
    """
    Generate subnet mask in binary from slash notation
    :param n: number of the subnet mask
    :return: (list of list) subnet mask in binary
    """

    n_full_1s = math.floor(n / 8)
    bits_left = n - (n_full_1s * 8)
    result = []
    for i in range(n_full_1s):
        octet = []
        for j in range(8):
            octet.append(1)
        result.append(octet)
    if bits_left:
        octet = []
        for i in range(bits_left):
            octet.append(1)
        while len(octet) < 8:
            octet.append(0)
        result.append(octet)
    while len(result) < 4:
        octet = []
        for i in range(8):
            octet.append(0)
        result.append(octet)
    return result


def subnet_to_octet(n: int) -> int:
    """
    Calculate which octet the subnet mask on.
    :param n: subnet mask
    :return: (int) the octet number
    """
    return math.ceil(n / 8)


def needed_bits_to_complete_octet(octet: list) -> int:
    """
    Calculate number of bit 1s needed to complete an octet.
    :param octet: (list) the octet
    :return: (int) bit 1s needed
    """

    if len(octet) != 8:
        raise Exception("The input is not an octet")

    count = 0
    for i in octet:
        if i == 0:
            count += 1
    return count


def octet_dec_to_bin(n: int, bits_val=None) -> list:
    """
    Translate a decimal octet into its binary form.
    :param bits_val: (default argument)
    :param n: octet
    :return: (list) binary result
    """
    if bits_val is None:
        bits_val = bits_value
    if not (0 <= n <= 255):
        raise Exception("Octet decimal value is between 1 and 255 inclusive")

    # bits_value = [128, 64, 32, 16, 8, 4, 2, 1]

    result = []
    for value in bits_val:
        if n - value >= 0:
            result.append(1)
            n = n - value
        else:
            result.append(0)

    return result


def octet_bin_to_dec(oct_bin: List[int], bits_val=None) -> int:
    """
    Translate binary octet (list of int) into its decimal value
    :param oct_bin: (list of int) the binary octet
    :param bits_val: (default argument)
    :return: (int) decimal value of the binary
    """
    # e.g. input : [1, 1, 0, 1, 1, 0, 1]
    if bits_val is None:
        bits_val = bits_value

    if len(oct_bin) != 8:
        raise Exception("Octet should have 8 bits or binary number")

    result = 0
    for bit_index in range(len(oct_bin)):
        if oct_bin[bit_index] == 1:
            result = result + bits_val[bit_index]
    return result


def apply_pipe(binary: list, at: int) -> list:
    """
    Apply pipe symbol (|) to mark bits needed to complete a target octet
    :param binary: (list) target octet binary
    :param at: (int) the position that the pipe will be applied
    :return: (list) binary with pipe symbol applied
    """
    binary.append('|')

    for i in range(-1, -at - 1, -1):
        bucket = binary[i - 1]
        binary[i - 1] = binary[i]
        binary[i] = bucket

    return binary


def calc_bin_with_pipe(binary: list, bits_val=None) -> int:
    """
    Calculate the left side bits of an octet that has pipe symbol applied.
    :param binary: (list) binary with pipe applied
    :param bits_val: (default argument)
    :return: (int) the value of the left side bits from the pipe
    """
    if bits_val is None:
        bits_val = bits_value
    if "|" not in binary:
        raise Exception("The binary doesn't contain pipe symbol (|) yet")

    # bits_value = [128, 64, 32, 16, 8, 4, 2, 1]

    total = 0
    for i in range(len(binary)):
        if binary[i] == "|":
            break
        elif binary[i] == 1:
            total = total + bits_val[i]
        elif binary[i] == 0:
            pass
    return total


def calc_subnet_increment(missing_bit: int) -> int:
    """
    Calculate subnet increment value for calculating the network address.
    :param missing_bit: (int) missing bit or bits needed to complete the 'on_octet' or target octet.
    :return: (int) subnets network address increment value
    """
    bit_index = - (missing_bit + 1)
    increment_value = bits_value[bit_index]
    return increment_value


def construct_network_address(ip_add: list, oc_tar: int, left_side_pipe_val: int) -> list:
    """
    Construct network address based on `identification` dictionary.
    :param ip_add: (list) IP Address to construct
    :param oc_tar: (int) Targeted Octet
    :param left_side_pipe_val: (int) Value in decimal after applying the pipe of the Targeted Octet
    :return: (list) The Network address in list format.
    """

    # oc_tar = 1
    if oc_tar < 1 or oc_tar > 4:
        raise Exception("The octet target is invalid, it should be between 1 and 4 inclusive")

    if oc_tar < 4:
        ip_add[oc_tar - 1] = left_side_pipe_val
        for i in range(oc_tar + 1, 4 + 1, 1):
            ip_add[i - 1] = 0
    elif oc_tar == 4:
        ip_add[oc_tar - 1] = left_side_pipe_val

    return ip_add


def format_address_into_string(address: list, is_binary=False) -> str:
    """
    Convert address in list format into string.
    :param is_binary: set this to True if converting list of binary, otherwise False as default
    :param address: (list) the address to convert
    :return: (str) string of the address
    """

    def is_type_harmony() -> bool:
        """
        Check whether a list contain same type of elements or not.
        :return: (bool) True if all element is the same type, otherwise False
        """

        type_determination = None
        for i in range(len(address)):
            if i == 0:
                type_determination = type(address[i])
                if type_determination == int or type_determination == str:
                    type_determination = (int, str)
            else:
                if not isinstance(address[i], type_determination):
                    return False
        return True

    if not is_type_harmony():
        raise Exception("The list is suppose to contain same types of elements.")

    result = None

    if is_binary:
        type_to_follow = type(address[0])
        if type_to_follow != list:
            # e.g. [1, 1, 1, 0, 0, 0, 0]
            result = ''.join([str(el) for el in address])
        elif type_to_follow == list:
            # e.g. [[1, 1, 1, 0, 0, 0, 0], [1, 1, 1, 0, 0, 0, 0]]
            result = '.'.join([str(''.join([str(el) for el in each_list])) for each_list in address])
        return result

    # e.g. [172, 26, 200, 55]
    result = '.'.join([str(el) for el in address])
    return result


def calc_num_of_subnets(address_default_subnet_mask: int, custom_subnet_mask: int) -> int:
    """
    Calculate number of available subnets
    :param address_default_subnet_mask: (int) Class's default subnet mask
    :param custom_subnet_mask: (int) User custom subnet mask
    :return: (int) number of available subnets
    """
    borrowed_bits = custom_subnet_mask - address_default_subnet_mask
    num_subnets = 2**borrowed_bits
    return num_subnets


def calc_num_of_host(custom_subnet_mask: int) -> int:
    """
    Calculate number of hosts
    :param custom_subnet_mask: (int) User custom subnet mask
    :return: (int) number of available hosts
    """
    host_bits = 32 - custom_subnet_mask
    num_hosts = (2**host_bits) - 2
    return num_hosts


def gen_subnet_table(network_address: list, target_octet: int, n_subnets: int, n_host: int, increment_val: int):
    """
    Generate Subnet's Network Address.
    :param network_address: (list) Calculated network address
    :param target_octet: (int) The number of octet to start
    :param n_subnets: (int) Number of subnets to create
    :param n_host: (int) Number of hosts per subnet
    :param increment_val: (int) Increment value of the network address.
    :return: (list) of Subnet's Network Address.
    """

    target_octet -= 1
    result = []
    for i in range(n_subnets):
        if i == 0:
            network_address_c = network_address.copy()
            network_address_c[target_octet] = 0
            result.append(network_address_c)
        else:
            network_address_c = result[i - 1].copy()

            if network_address_c[target_octet] + increment_val <= 255:
                network_address_c[target_octet] += increment_val
            else:
                network_address_c[target_octet] = 0
                # preparing for while loop
                i = target_octet - 1
                while i >= 0:
                    if network_address_c[i] < 255:
                        network_address_c[i] += 1
                        # shutdown the while loop
                        i = -1
                    else:
                        network_address_c[i] = 0
                        i -= 1

            result.append(network_address_c)

    return result
