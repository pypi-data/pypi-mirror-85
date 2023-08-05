#! /usr/local/python
# -*- coding: UTF-8 -*-
import codecs

NAME = "ops_generic_test"

train_transcription = NAME+"/"+NAME+"_etc/"+NAME+"_train.transcription"
test_transcription = NAME+"/"+NAME+"_etc/"+NAME+"_test.transcription"

output = NAME+"/"+NAME+"_etc/"+NAME+".transcription"

train_transcription_file = codecs.open(train_transcription, encoding="UTF-8")
test_transcription_file = codecs.open(test_transcription, encoding="UTF-8")

output_file = codecs.open(output, "w+", encoding="UTF-8")

train_content = train_transcription_file.readlines()
for line in train_content:
    output_file.write(" ".join(line.split()[:-1])+"\n")

test_content = train_transcription_file.readlines()
for line in test_content:
    output_file.write(" ".join(line.split()[:-1])+"\n")


output_file.close()
