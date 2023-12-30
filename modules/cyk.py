import os
import streamlit as st

TRIANGULAR_TABLE = {}
RESULT = {}


def get_grammar():
    global RESULT
    RESULT.clear()

    dirpath = os.path.dirname(os.path.abspath(__file__))

    with open(os.path.join(dirpath, "../cnf.txt"), "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            lhs, rhs = line.split(" -> ")
            rhs = rhs.split(" | ")

            if lhs in RESULT:
                RESULT[lhs].extend(rhs)
            else:
                RESULT[lhs] = rhs

    for key, value in RESULT.items():
        if key == "Propnoun":
            RESULT[key] = list(set(map(str.lower, value)))

    print(RESULT)
    return RESULT


def is_accepted(input_string):
    production_rules = get_grammar()

    initialize_triangular_table(input_string)

    for i in reversed(range(1, len(input_string) + 1)):
        for j in range(1, i + 1):
            if j == j + len(input_string) - i:
                update_bottom_row(input_string, j)
            else:
                combine_cells(input_string, j, i)

    return "K" in TRIANGULAR_TABLE[(1, len(input_string))]


def initialize_triangular_table(input_string):
    for i in range(1, len(input_string) + 1):
        for j in range(i, len(input_string) + 1):
            TRIANGULAR_TABLE[(i, j)] = []


def update_bottom_row(input_string, j):
    temp_list = []
    production_rules = get_grammar()

    for key, value in production_rules.items():
        for val in value:
            if val == input_string[j - 1] and key not in temp_list:
                temp_list.append(key)

    TRIANGULAR_TABLE[(j, j + len(input_string) - len(input_string))] = temp_list


def combine_cells(input_string, j, i):
    temp_list = []
    result_list = []
    production_rules = get_grammar()

    for k in range(len(input_string) - i):
        first = TRIANGULAR_TABLE[(j, j + k)]
        second = TRIANGULAR_TABLE[(j + k + 1, j + len(input_string) - i)]

        for fi in first:
            for se in second:
                combined_key = f"{fi} {se}"
                if combined_key not in temp_list:
                    temp_list.append(combined_key)

    for key, value in production_rules.items():
        for val in value:
            if val in temp_list and key not in result_list:
                result_list.append(key)

    TRIANGULAR_TABLE[(j, j + len(input_string) - i)] = result_list


def get_table_element(input_string):
    global TRIANGULAR_TABLE
    result = []
    n = len(input_string.split(" "))

    for i in range(1, n + 1):
        temp = []
        for j in range(i):
            res = TRIANGULAR_TABLE[(j + 1, n - i + j + 1)]
            temp.append("\u2205") if not res else temp.append(
                "{" + ", ".join(res) + "}"
            )

        result.append(temp)

    result.append(input_string.split(" "))
    return result