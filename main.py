from file_reader import FileReader

from os import listdir
from os.path import isfile, join

from markov_model import MarkovModel
from tester import Tester


# Reads the training files and splits them into 80:20 pairings to test on the 20% later
def read_training_files():
    for i in onlyfiles:
        with open("author_attribution/trainikc/" + i, encoding="UTF-8") as file:
            file_content = file.read()
            file_reader = FileReader(file_content, create_validation_set=True)
            training_chain_list.append(file_reader.training_chain)
            validation_chain_list.append(file_reader.validation_chain)


# Processes the input files into transition matrices
def train_models():
    for chain in training_chain_list:
        training_transition_matrix.append(MarkovModel(chain.split()).transition_matrix)


# Reads the test files into memory and preprocesses them for evaluation
def read_test_files():
    for i in onlyfiles_test:
        with open("author_attribution/testikc/" + i, encoding="UTF-8") as file:
            file_content = file.read()
            file_reader = FileReader(file_content, create_validation_set= False)
            test_chain_list.append(file_reader.chain)


# Tries to guess which author wrote which text.
# Evaluated are the training matrices against the test texts
def predict_text(texts, test_name, training_name):
    for chain in range(0, len(texts)):
        max_accuracy = 0
        best_index = None
        for matrix in range(0, len(training_transition_matrix)):
            tester = Tester(training_transition_matrix[matrix], texts[chain].split())
            if tester.accuracy > max_accuracy:
                max_accuracy = tester.accuracy
                best_index = matrix
        print("Most Probable Author for Text", test_name[chain], "is", training_name[best_index], ".")


onlyfiles = [f for f in listdir("author_attribution/trainikc/") if isfile(join("author_attribution/trainikc/", f))]
onlyfiles_test = [f for f in listdir("author_attribution/testikc/") if isfile(join("author_attribution/testikc/", f))]


# Allocating memory for all the chains and matrices that we are reading in and evaluating
training_chain_list = []
validation_chain_list = []
training_transition_matrix = []
test_chain_list = []

# Performing preprocessing
read_training_files()
train_models()
read_test_files()

# Using all the matrices and chains that we build, we are now trying to guess the author.
# The test chains are used to test accuracy
predict_text(validation_chain_list, onlyfiles, onlyfiles)
predict_text(test_chain_list, onlyfiles_test, onlyfiles)












