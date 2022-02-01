import math
import ipaddress
import tkinter as tk
from IPy import IP


def main():
    ip_address_and_mask = None
    while not check_ip_and_mask(ip_address_and_mask):
        ip_address_and_mask = input("Enter an IP Address and Mask: ")

    ip_address_and_mask_arr = ip_address_and_mask.split("/")
    ip_address = ip_address_and_mask_arr[0]
    mask = ip_address_and_mask_arr[1]

    subnets_count = int(input("Enter the amount of networks: "))

    ip_address_bin = get_ip_address_bin(ip_address)
    subnet_mask = get_subnet_mask(mask, subnets_count)
    net_ip = get_net_ip(ip_address_bin, mask)


    print(f"Global IP Net Address: {net_ip}\n"
    f"Mask: {mask}\n"
    f"SubNet Mask: {subnet_mask}")

    subnets_ip_list = get_subnets_ip(ip_address_bin, mask, subnet_mask, subnets_count)

    counter = 0
    for subnet_ip in subnets_ip_list:

            first_nets_ip_list = to_decimal(get_first_net_ip(subnet_ip))
            last_nets_ip_list = to_decimal(get_last_net_ip(subnet_ip, subnet_mask))
            broadcasts = to_decimal(get_broadcast(subnet_ip, subnet_mask))

            print(f"SubNet IP {counter}: {to_decimal(subnet_ip) + '/' +  str(subnet_mask)}\n"
                  f"\tFirst Net {counter} : {first_nets_ip_list}\n"
                  f"\tLast Net {counter}  : {last_nets_ip_list}\n"
                  f"\tBroadCast {counter} : {broadcasts}\n")
            counter += 1


def get_net_ip(ip_address_bin, mask):
    mask = int(mask)
    net_ip = ""

    for i in range(len(ip_address_bin)):
        if i <= mask - 1:
            net_ip += ip_address_bin[i]
        else:
            net_ip += "0"
    return net_ip


def get_subnet_mask(mask, subnets_count):
    bit_count = math.ceil(math.log2(subnets_count))
    return int(mask) + bit_count


def get_correct_bit_format(uncorrect_bin, count_of_bits):
    while len(uncorrect_bin) < count_of_bits:
        uncorrect_bin = "0" + uncorrect_bin
    return uncorrect_bin


def get_ip_address_bin(ip_address):
    ip_address_arr = ip_address.split(".")

    ip_address_bin_arr = []
    for octet in ip_address_arr:
        uncorrect_bin = format(int(octet), "b")
        ip_address_bin_arr.append(get_correct_bit_format(uncorrect_bin, 8))

    ip_address_bin = "".join(ip_address_bin_arr)
    return ip_address_bin


def get_subnets_ip(ip_address_bin, mask, subnet_mask, subnets_count):
    mask = int(mask)
    prefix_ip = ""
    subnet_ip_list = []

    for i in range(mask):
        prefix_ip += ip_address_bin[i]

    for subnet_number in range(subnets_count):
        uncorrect_bin = format(int(subnet_number), "b")
        subnet_bits = get_correct_bit_format(uncorrect_bin, subnet_mask - mask)
        subnet_ip = prefix_ip + subnet_bits

        for i in range(len(ip_address_bin) - subnet_mask):
            subnet_ip += "0"

        subnet_ip = "".join(subnet_ip)
        subnet_ip_list.append(subnet_ip)
    return subnet_ip_list


def get_first_net_ip(subnet_ip):
    subnet_ip = list(subnet_ip)
    subnet_ip[-1] = "1"
    first_net_ip = "".join(subnet_ip)
    return first_net_ip


def get_last_net_ip(subnet_ip, subnet_mask):
    for i in range(subnet_mask, len(subnet_ip)):
        subnet_ip = list(subnet_ip)
        subnet_ip[i] = "1"

    subnet_ip[-1] = "0"
    last_net_ip = "".join(subnet_ip)
    return last_net_ip


def get_broadcast(subnet_ip, subnet_mask):
    for i in range(subnet_mask, len(subnet_ip)):
        subnet_ip = list(subnet_ip)
        subnet_ip[i] = "1"

    broadcast = "".join(subnet_ip)
    return broadcast


def to_decimal(bin_ip):
    bin_ip = list(bin_ip)
    octet = ""
    decimal_ip = ""
    counter = 0

    for bit in bin_ip:
        octet += bit
        if len(octet) == 8:
            counter += 1
            decimal_ip += str(int(octet, 2))

            if counter < 4:
                decimal_ip += "."
            octet = ""

    return decimal_ip


def check_ip_and_mask(ip_address_and_mask):
    if not ip_address_and_mask:
        return

    if "/" not in ip_address_and_mask:
        print("Expected format: xxx.xxx.xxx.xxx/xx")
        return

    ip_address_and_mask_arr = ip_address_and_mask.split("/")
    ip_address = ip_address_and_mask_arr[0]
    mask = ip_address_and_mask_arr[1]

    if not mask.isdigit():
        print("Expected format: xxx.xxx.xxx.xxx/xx")
        return

    if int(mask) > 32:
        print("Mask should be less then 32")
        return

    try:
        ipaddress.ip_address(ip_address)
    except ValueError:
        print("Expected format: xxx.xxx.xxx.xxx/xx")
        return False
    else:
        return True


if __name__ == '__main__':
    main()
