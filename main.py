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
            validation_chain_list.append(file_reader.validation_chain_list)


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
            test_chain_list.append(file_reader.chains)


def predict_all_texts(all_texts, true_names, training_files, verbose, validation):
    if validation:
        average_accuracy = 0
        for i in range (0, len(all_texts)):
            average_accuracy += predict_text_by_comment(all_texts[i], true_names[i], training_files, verbose, validation)
        print(average_accuracy / len(all_texts))
    else:
        for i in range (0, len(all_texts)):
            predict_text_by_comment(all_texts[i], None, training_files, True, validation)

def predict_text_by_comment(text_list, true_name, training_files, verbose, validation):
    total_accuracy = 0
    for comment in range (0, len(text_list)):
        max_accuracy = 0
        best_index = 0
        for matrix in range (0, len(training_transition_matrix)):
            tester = Tester(training_transition_matrix[matrix], text_list[comment].split())
            if tester.accuracy > max_accuracy:
                max_accuracy = tester.accuracy
                best_index = matrix
        if validation:
            if verbose:
                print("Most probable Author for Comment", text_list[comment], "is", training_files[best_index], "with ", max_accuracy, "% accuracy, but true author is", true_name)
            if (training_files[best_index] == true_name):
                total_accuracy += 1
        else :
            if verbose:
                print("Most probable Author for Comment", text_list[comment], "is", training_files[best_index], "with ",
                      max_accuracy, "% accuracy")

    return (total_accuracy / len(text_list))

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


#The input block to choose between validation and testing mode.
input_correct = False
while not input_correct:
    input = input("If you want to see the validation set accuracy, enter 'v'.\n"
                  "If you want to see the assigned text for every single comment of every text, press 't'.")

    if (input == 'v'):
        input_correct = True
        predict_all_texts(validation_chain_list, onlyfiles, onlyfiles, verbose=False, validation = True)
    elif (input == 'p'):
        input_correct = True
        predict_all_texts(test_chain_list, None, onlyfiles, verbose=True, validation=False)
    else:
        input ("Input not correct. Please try again.")











