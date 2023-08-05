#! /usr/local/python
# -*- coding: UTF-8 -*-

"""
Crea una lista de fonemas a partir de un diccionario fonetico
"""
import codecs


def execute_script(dict_file, output_file):

    f = codecs.open(dict_file, "rb", encoding="UTF-8")
    lines = f.readlines()

    all_phones = []

    for line in lines:
        phones = line.split()[1:]
        for phone in phones:
            if phone not in all_phones:
                all_phones.append(phone)

    o_file = codecs.open(output_file, 'w+', encoding="UTF-8")
    for phone in all_phones:
        o_file.write(phone + "\n")
    o_file.write("SIL\n")
    o_file.close()
