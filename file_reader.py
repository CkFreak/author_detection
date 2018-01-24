import string


class FileReader:

    def __init__(self, file_content, create_validation_set):
        self.chain = self.filter(file_content)
        if create_validation_set:
            self.training_chain, self.validation_chain = self.split_training_validation(self.chain)

    # Calls all other methods of the class to process the given file
    def filter(self, file_content):
        return_content = self.remove_punctuation(file_content)
        return_content = self.remove_upper_case_words(return_content.split())
        return_content = self.remove_extra_spaces(return_content)
        return return_content

    # Removes all punctuation from the file
    def remove_punctuation(self, file_content):
        file_content = file_content.replace("<s>", "")
        table = str.maketrans({key: None for key in string.punctuation})
        return file_content.translate(table)

    # Removes all upper case words from the text. It turns out they are not as important for the accuracy
    def remove_upper_case_words(self, file_content):
        return " ".join([word for word in file_content if word.islower()])

    # Removes extra spaces such as linebreaks and two spaces in a row
    def remove_extra_spaces(self, file_content):
        return " ".join(file_content.split())

    # Splits the content of the file into two part representing 80% and 20% of the original content
    def split_training_validation(self, return_content):
        train_size = int(len(return_content) * 0.8)
        training_chain = return_content[:train_size]
        validation_chain = return_content[train_size:]
        return training_chain, validation_chain

