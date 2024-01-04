import os
import streamlit as st

TRIANGULAR_TABLE = {}
RESULT = {}


# untuk membuka file grammar yaitu rules CNF
def get_grammar():
    global RESULT
    RESULT.clear()

    dirpath = os.path.dirname(os.path.abspath(__file__))

    with open(os.path.join(dirpath, "../full-cnf.txt"), "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            lhs, rhs = line.split(" -> ")
            rhs = rhs.split(" | ")

            # menyimpan aturan produksi
            if lhs in RESULT:
                RESULT[lhs].extend(rhs)
            else:
                RESULT[lhs] = rhs

    # mengkonversi PropNoun agar dapat menjadi huruf kecil
    for key, value in RESULT.items():
        if key == "PropNoun":
            RESULT[key] = list(set(map(str.lower, value)))

    print(RESULT)
    return RESULT


# memeriksa apakah string dapat diterima atau ditolak
def is_accepted(text_input):
    initialize_triangular_table(text_input)

    for i in reversed(range(1, len(text_input) + 1)):
        for j in range(1, i + 1):
            if j == j + len(text_input) - i:
                update_bottom_row(text_input, j)
            else:
                combine_cells(text_input, j, i)

    return "K" in TRIANGULAR_TABLE[(1, len(text_input))]


# menginisialisasi tabel triangular cyk
def initialize_triangular_table(text_input):
    for i in range(1, len(text_input) + 1):
        for j in range(i, len(text_input) + 1):
            TRIANGULAR_TABLE[(i, j)] = []


# memperbarui baris terbawah tabel triangular cyk
def update_bottom_row(text_input, j):
    temp_list = []
    production_rules = get_grammar()

    for key, value in production_rules.items():
        for val in value:
            if val == text_input[j - 1] and key not in temp_list:
                temp_list.append(key)

    TRIANGULAR_TABLE[(j, j + len(text_input) - len(text_input))] = temp_list


# menggabungkan cells dalam tabel cyk
def combine_cells(text_input, j, i):
    temp_list = []
    result_list = []
    production_rules = get_grammar()

    for k in range(len(text_input) - i):
        first = TRIANGULAR_TABLE[(j, j + k)]
        second = TRIANGULAR_TABLE[(j + k + 1, j + len(text_input) - i)]

        for fi in first:
            for se in second:
                combined_key = f"{fi} {se}"
                if combined_key not in temp_list:
                    temp_list.append(combined_key)

    for key, value in production_rules.items():
        for val in value:
            if val in temp_list and key not in result_list:
                result_list.append(key)

    TRIANGULAR_TABLE[(j, j + len(text_input) - i)] = result_list


# mendapatkan elemen elemen dari tabel hasil
def get_table_element(text_input):
    global TRIANGULAR_TABLE
    result = []
    n = len(text_input.split(" "))

    for i in range(1, n + 1):
        temp = []
        for j in range(i):
            res = TRIANGULAR_TABLE[(j + 1, n - i + j + 1)]
            temp.append("\u2205") if not res else temp.append(
                "{" + ", ".join(res) + "}"
            )

        result.append(temp)

    result.append(text_input.split(" "))
    return result
