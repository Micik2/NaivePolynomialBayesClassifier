import re
import sys

marks = []
texts = []

mark_pattern = re.compile("\d")#("\n(\d)\t")
text_pattern = re.compile("\d\t(.+)")
word_pattern = re.compile("\w+")

with open("../train/train.tsv", encoding="utf-8") as file:
    i = 0
    for line in file:
        if i < 100:    # 1000000 - max
            mark = mark_pattern.findall(line)
            text = text_pattern.findall(line)

            if len(text) > 0:
                texts.append(text[0])
                marks.append(mark[0])
            
            i += 1
    file.close()


length_of_marks = float(len(marks))
positives_marks = 0
negatives_marks = 0

for mark in marks:
    if mark == '1':
        positives_marks += 1
    else:
        negatives_marks += 1

# P(c)
P_positive_ = positives_marks / length_of_marks
# P(1 - c)
P_negative_ = 1 - P_positive_


positive_words = []
negative_words = []

for text in texts:
    index = texts.index(text)
    if marks[index] == '1':
        positive_words.extend(word_pattern.findall(text))
    else:
        negative_words.extend(word_pattern.findall(text))

length_of_positive_words = float(len(positive_words))  
length_of_negative_words = float(len(negative_words))
length_of_set_words = len(set(positive_words + negative_words))
extended_length_of_positive_words = float(length_of_positive_words + length_of_set_words)
extended_length_of_negative_words = float(length_of_negative_words + length_of_set_words)

expected_marks = []

with open("in.tsv", encoding="utf-8") as file:
    j = 1
    for line in file:
        print (str(float((j/21687) * 100)) + '%')
        positive_elements = 1
        negative_elements = 1
        words = word_pattern.findall(line)
        for word in words:
            positives = 0
            negatives = 0
            for positive_word in positive_words:
                if word == positive_word:
                    positives += 1
            for negative_word in negative_words:
                if word == negative_word:
                    negatives += 1
            positives += 1
            negatives += 1
            # P(t|c)
            positive_element = positives / extended_length_of_positive_words
            negative_element = negatives / extended_length_of_negative_words
            positive_elements *= positive_element
            negative_elements *= negative_element
        P_line_positive = P_positive_ * positive_elements
        P_line_negative = P_negative_ * negative_elements
        if P_line_negative > P_line_positive:
            expected_marks.append("0.3")
        elif P_line_negative < P_line_positive:
            expected_marks.append("0.7")
        else:
            expected_marks.append("0.5")
        j += 1
    file.close()         

with open("out.tsv", "w+") as file:
    for expected_mark in expected_marks:
        file.write(expected_mark)
        file.write("\n")
    file.close()
