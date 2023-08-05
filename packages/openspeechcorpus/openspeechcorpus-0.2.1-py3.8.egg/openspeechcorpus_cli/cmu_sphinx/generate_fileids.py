__author__ = 'ma0'
"""
Genera los identificadores de los archivos que se van a procesar
"""
import os
import codecs

unconvert_file_ids = "ops_T22/ops_T22_etc/all.fileids"
so_path_separator = "/"

output_file = "ops_T22/ops_T22_etc/ops_T22.fileids"

f = codecs.open(unconvert_file_ids, 'rb', encoding="UTF-8")
f_content = f.readlines()
fo = codecs.open(output_file, 'w+', encoding="UTF-8")
for line in f_content:
    if "3gp" in line:
        fo.write(line.replace(".3gp", "_3gp"))
    elif "mp4" in line:
        fo.write(line.replace(".mp4", ""))
fo.close()



