from file_reader import FileReader

from os import listdir
from os.path import isfile, join

from markov_model import MarkovModel
from tester import Tester

onlyfiles = [f for f in listdir("author_attribution/trainikc/") if isfile(join("author_attribution/trainikc/", f))]

chainz_list = []

for i in onlyfiles:
    with open("author_attribution/trainikc/" + i, encoding="UTF-8") as file:
        file_content = file.read()
        file_reader = FileReader(file_content)
        chainz_list.append(file_reader.chain)


trainikc_transition_matrix = []

for chain in chainz_list:
    trainikc_transition_matrix.append(MarkovModel(chain.split()).transition_matrix)

testfilez = []
onlyfiles_test = [f for f in listdir("author_attribution/testikc/") if isfile(join("author_attribution/testikc/", f))]

for i in onlyfiles_test:
    with open("author_attribution/testikc/" + i, encoding="UTF-8") as file:
        file_content = file.read()
        file_reader = FileReader(file_content)
        testfilez.append(file_reader.chain)


for chain in range(0, len(testfilez)):
    max_accuracy = 0
    best_index = None
    for matrix in range(0, len(trainikc_transition_matrix)):
        tester = Tester(trainikc_transition_matrix[matrix], testfilez[chain].split())
        if tester.accuracy > max_accuracy:
            max_accuracy = tester.accuracy
            best_index = matrix
    print("Most Probable Author for Text", onlyfiles_test[chain], "is", onlyfiles[best_index], ".")
