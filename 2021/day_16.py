#!/usr/bin/env python

from pathlib import Path


FILE_PATH = Path(__file__)

HEXADECIMAL_BITS = {
    '0': '0000',
    '1': '0001',
    '2': '0010',
    '3': '0011',
    '4': '0100',
    '5': '0101',
    '6': '0110',
    '7': '0111',
    '8': '1000',
    '9': '1001',
    'A': '1010',
    'B': '1011',
    'C': '1100',
    'D': '1101',
    'E': '1110',
    'F': '1111'
}


def int_from_bits(bits: str) -> int:
    return sum((2 ** index if bit == '1' else 0) for index, bit in enumerate(reversed(bits)))


class Packet:
    def __init__(self, bits: str, version: int, type_id: int) -> None:
        self.bits = bits
        self.length = len(bits)
        self.version = version
        self.type_id = type_id


class LiteralValuePacket(Packet):
    def __init__(self, bits: str, version: int, type_id: int, value: int) -> None:
        super().__init__(bits, version, type_id)
        self.value = value


class OperatorPacket(Packet):
    def __init__(self, bits: str, version: int, type_id: int, sub_packets: list[Packet]) -> None:
        super().__init__(bits, version, type_id)
        self.sub_packets = sub_packets


def parse_packet(bits: str) -> Packet:
    version = int_from_bits(bits[0:3])
    type_id = int_from_bits(bits[3:6])
    content_offset = 6
    if type_id == 4:
        packet = parse_literal_value_packet(bits, version, type_id, content_offset)
        print(f"Parsed literal value {packet.value} packet (version {version}).")
    else:
        packet = parse_operator_packet(bits, version, type_id, content_offset)
        print(f"Parsed operator type {type_id} packet (version {version}) with {len(packet.sub_packets)} sub-packets.")
    return packet


def parse_literal_value_packet(bits: str, version: int, type_id: int, content_offset: int) -> LiteralValuePacket:
    current_value_offset = content_offset
    value_bits = ''
    while True:
        value_bits += bits[current_value_offset + 1:current_value_offset + 5]
        if bits[current_value_offset] == '0':
            break
        else:
            current_value_offset += 5
    packet_end_offset = current_value_offset + 5
    packet_bits = bits[:packet_end_offset]
    value = int_from_bits(value_bits)
    return LiteralValuePacket(packet_bits, version, type_id, value)


def parse_operator_packet(bits: str, version: int, type_id: int, content_offset: int) -> OperatorPacket:
    length_type = 'length' if bits[content_offset] == '0' else 'count'
    if length_type == 'length':
        total_sub_packets_bit_length = int_from_bits(bits[content_offset + 1:content_offset + 16])
        current_sub_packets_offset = content_offset + 16
    else:
        total_sub_packets_count = int_from_bits(bits[content_offset + 1:content_offset + 12])
        current_sub_packets_offset = content_offset + 12

    sub_packets: list[Packet] = []
    current_sub_packets_bit_length = 0

    while (
        (length_type == 'length' and current_sub_packets_bit_length < total_sub_packets_bit_length)
        or (length_type == 'count' and len(sub_packets) < total_sub_packets_count)
    ):
        sub_packet = parse_packet(bits[current_sub_packets_offset:])
        sub_packets.append(sub_packet)
        current_sub_packets_bit_length += sub_packet.length
        current_sub_packets_offset += sub_packet.length

    packet_bits = bits[:current_sub_packets_offset]
    return OperatorPacket(packet_bits, version, type_id, sub_packets)


def sum_packet_versions(packet: Packet) -> int:
    versions_sum = packet.version
    if isinstance(packet, OperatorPacket):
        versions_sum += sum(sum_packet_versions(sub_packet) for sub_packet in packet.sub_packets)
    return versions_sum


if __name__ == '__main__':
    with open(FILE_PATH.parent / f'{FILE_PATH.stem}_input.txt') as file:
        transmission_hexadecimal = file.readline().rstrip()

    transmission_bits = ''.join(HEXADECIMAL_BITS[char] for char in transmission_hexadecimal)
    packet = parse_packet(transmission_bits)

    packet_versions_sum = sum_packet_versions(packet)
    print(f"Packet versions sum:  {packet_versions_sum}")
