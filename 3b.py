#!/usr/bin/env python3
import fileinput

# If True, this script solves the first part of the puzzle, the second one otherwise.
EASY = False
DAY = 3

assert not EASY


def split_by_bit(numbers, bit):
    numbers_with_1 = []
    numbers_with_0 = []
    for num in numbers:
        if num[bit] == '1':
            numbers_with_1.append(num)
        elif num[bit] == '0':
            numbers_with_0.append(num)
        else:
            raise ValueError(f"Incorrect value of bit: '{num[bit]}'")
    
    if len(numbers_with_1) >= len(numbers_with_0):
        return numbers_with_1, numbers_with_0
    else:
        return numbers_with_0, numbers_with_1


numbers = []
for line in fileinput.input(f'{DAY}.txt'):
    line = line.strip()
    numbers.append(line)


oxygen_numbers = numbers
prev_len = len(oxygen_numbers)
for i in range(prev_len):
    oxygen_numbers, _ = split_by_bit(oxygen_numbers, bit=i)
    if len(oxygen_numbers) in (1, prev_len):
        assert len(set(oxygen_numbers)) == 1
        break
    prev_len = len(oxygen_numbers)


co2_numbers = numbers
prev_len = len(co2_numbers)
for i in range(prev_len):
    _, co2_numbers = split_by_bit(co2_numbers, bit=i)
    if len(co2_numbers) in (1, prev_len):
        assert len(set(co2_numbers)) == 1
        break
    prev_len = len(oxygen_numbers)


assert oxygen_numbers
assert co2_numbers

oxygen_rating = int(oxygen_numbers[0], base=2)
co2_rating = int(co2_numbers[0], base=2)

print(oxygen_rating * co2_rating)
