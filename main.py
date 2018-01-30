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

# Predicts all texts by comment or not by comment.
def predict_all_texts(all_texts, true_names, training_files, verbose, validation, num_of_tokens_per_text):
    average_accuracy = 0
    if validation:
        for i in range (0, len(all_texts)):
            average_accuracy += predict_text_by_comment(all_texts[i], true_names[i], training_files, verbose, validation, num_of_tokens_per_text)
        print("Accuracy for Validation Set with ", num_of_tokens_per_text, "tokens per text: ", average_accuracy / len(all_texts), "%.")
    else:
        for i in range (0, len(all_texts)):
            average_accuracy += predict_text_by_comment(all_texts[i], test_author_information[true_names[i]], training_files, verbose, validation, num_of_tokens_per_text)
        print("Accuracy for Test Set with ", num_of_tokens_per_text, "tokens per text: ", average_accuracy / len(all_texts), "%.")

#Predicts the author by comment, returns the total success rate
def predict_text_by_comment(text_list, true_name, training_files, verbose, validation, num_of_tokens_per_text):
    total_accuracy = 0
    if num_of_tokens_per_text == 0:
        num_of_tokens_per_text = len(text_list)
    for comment in range (0, num_of_tokens_per_text):
        max_accuracy = 0
        best_index = 0
        for matrix in range (0, len(training_transition_matrix)):
            tester = Tester(training_transition_matrix[matrix], text_list[comment].split())
            if tester.accuracy > max_accuracy:
                max_accuracy = tester.accuracy
                best_index = matrix
            if verbose:
                if validation:
                    print("Most probable Author for Comment", text_list[comment], "is", training_files[best_index], "with ", max_accuracy, "% accuracy, but true author is", true_name)
                else:
                    print("Most probable Author for Comment", text_list[comment], "is", training_files[best_index], "with ",
                          max_accuracy, "% accuracy")
        if (training_files[best_index] == ("train_" + true_name)):
            total_accuracy += 1

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

def join_test_chain_list(test_chain_list):
    new_list = []
    for i in range (0, len(test_chain_list)):
        new_list.append(" ".join(test_chain_list[i]))
    return new_list

onlyfiles = [f for f in listdir("author_attribution/trainikc/") if isfile(join("author_attribution/trainikc/", f))]
onlyfiles_test = [f for f in listdir("author_attribution/testikc/") if isfile(join("author_attribution/testikc/", f))]


# Allocating memory for all the chains and matrices that we are reading in and evaluating
training_chain_list = []
validation_chain_list = []
training_transition_matrix = []
test_chain_list = []

#The true files for the test, in order to measure accuracy on the test set
test_author_information = {'McSpain.txt': 'test_b', 'Thomas_Barth.txt': 'test_v', 'Pro4you.txt': 'test_x',
'ChuckBROOZeG.txt': 'test_q', 'Slaytanic.txt': 'test_w', 'Hendrik_-ZG-.txt': 'test_m',
'Vidar.txt': 'test_i', 'Larnak.txt': 'test_z', 'Sven_Gellersen.txt': 'test_h',
'Freylis.txt': 'test_a', 'Darth_Spengler.txt': 'test_t', 'Green_Yoshi.txt': 'test_u',
'maddccat.txt': 'test_d', 'Sp00kyFox.txt': 'test_e', 'Toxe.txt': 'test_k',
'Noodles.txt': 'test_n', 'floppi.txt': 'test_y', 'Ganon.txt': 'test_o',
'Dennis_Ziesecke.txt': 'test_p', 'Spiritogre.txt': 'test_l'}
test_author_information = inv_map = {v: k for k, v in test_author_information.items()}


# Performing preprocessing
read_training_files()
train_models()
read_test_files()


#The input block to choose between validation and testing mode.
input_correct = False
while not input_correct:
    tokens = input("Please enter the number of tokens that you want to test (0 if you want all):")
    tokens = int(tokens)
    input = input("If you want to see the validation set (80/20) accuracy, enter 'v'.\n"
                  "If you want to see the attribution of the test set by Text, press 't'.\n"
                  "If you want to see the attribution of an author for each test text, press 'o'")

    if (input == 'v'):
        input_correct = True
        predict_all_texts(validation_chain_list, onlyfiles, onlyfiles, verbose=False, validation = True, num_of_tokens_per_text=tokens)
    elif (input == 't'):
        input_correct = True
        predict_all_texts(test_chain_list, onlyfiles_test, onlyfiles, verbose=False, validation=False, num_of_tokens_per_text=tokens)
    elif (input == 'o'):
        input_correct = True
        predict_text(join_test_chain_list(test_chain_list), onlyfiles_test, onlyfiles)
    else:
        input ("Input not correct. Please try again.")











