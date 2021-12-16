#!/usr/bin/env python3
from dataclasses import dataclass
import fileinput
from functools import reduce
from io import BytesIO
import operator
from typing import List

# If True, this script solves the first part of the puzzle, the second one otherwise.
EASY = False
# If True, example from the puzzle condition is used as input.
TEST = False
DAY = 16

INPUT_FILE = f'{DAY}{"t" if TEST else ""}.txt'


TYPEID_LITERAL = 4
LENID_IN_BITS = 0
LENID_IN_PACKETS = 1
REDUCE_PACKETS_FUNC = {
    0: sum,
    1: lambda x: reduce(operator.mul, x, 1),
    2: min,
    3: max,
}
LOGIC_PACKETS_FUNC = {
    5: operator.gt,
    6: operator.lt,
    7: operator.eq,
}


@dataclass
class BasePacket:
    version: int
    type_id: int
    bit_length: int


@dataclass
class ValuePacket(BasePacket):
    value: int


@dataclass
class OperatorPacket(BasePacket):
    subpackets: List[BasePacket]


def pad_zeros(s: str, length=4) -> str:
    n = len(s)
    return '0' * (length - n) + s


def from_bits(bits: bytes):
    return int(bits.decode(), base=2)


def read_packet(istream: BytesIO) -> BasePacket:
    version = from_bits(istream.read(3))
    type_id = from_bits(istream.read(3))
    bit_length = 6
    if type_id == TYPEID_LITERAL:
        incomplete = True
        value = 0
        while incomplete:
            part = from_bits(istream.read(5))
            bit_length += 5
            incomplete = (part >= 0b10000)
            value = (value << 4) + (part & 0b1111)
        return ValuePacket(version, type_id, bit_length=bit_length, value=value)
    else:
        length_type_id = from_bits(istream.read(1))
        bit_length += 1
        subpackets = []
        if length_type_id == 0:
            remaining_bits = from_bits(istream.read(15))
            bit_length += 15
            while remaining_bits > 0:
                packet = read_packet(istream)
                bit_length += packet.bit_length
                remaining_bits -= packet.bit_length
                subpackets.append(packet    )
        else:
            remaining_packets = from_bits(istream.read(11))
            bit_length += 11
            for _ in range(remaining_packets):
                packet = read_packet(istream)
                bit_length += packet.bit_length
                subpackets.append(packet)
        return OperatorPacket(version, type_id, bit_length, subpackets)


def fold(packet: BasePacket) -> int:
    if EASY:
        version_sum = packet.version
        if isinstance(packet, OperatorPacket):
            for subpacket in packet.subpackets:
                version_sum += fold(subpacket)
        return version_sum
    else:
        if isinstance(packet, ValuePacket):
            return packet.value
        assert isinstance(packet, OperatorPacket)

        if packet.type_id in REDUCE_PACKETS_FUNC:
            func = REDUCE_PACKETS_FUNC[packet.type_id]
            return func(fold(subpacket) for subpacket in packet.subpackets)
        elif packet.type_id in LOGIC_PACKETS_FUNC:
            subp1, subp2 = packet.subpackets
            op = LOGIC_PACKETS_FUNC[packet.type_id]
            return int(op(fold(subp1), fold(subp2)))
        else:
            raise ValueError("unknown type_id")



line = None
for line in fileinput.input(INPUT_FILE):
    # There is only one line in input.
    line = line.strip()
assert line

bits = ''.join(pad_zeros(bin(int(hexdigit, base=16))[2:]) for hexdigit in line).encode()
stream = BytesIO(bits)
packet = read_packet(stream)
result = fold(packet)

print(result)

