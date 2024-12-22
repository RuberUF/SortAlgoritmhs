# utils.py
import random

def generate_random_data(start_range, end_range, data_count):
    return [random.randint(start_range, end_range) for _ in range(data_count)]

def read_data_from_file(file):
    return file.read().decode('utf-8').splitlines()
