import string


class FileReader:

    def __init__(self, file_content):
        self.chain = self.filter(file_content)

    def filter(self, file_content):
        return_content = self.remove_punctuation(file_content)
        return_content = self.remove_upper_case_words(return_content.split())
        return_content = self.remove_extra_spaces(return_content)
        return return_content

    def remove_punctuation(self, file_content):
        file_content = file_content.replace("<s>", "")
        table = str.maketrans({key: None for key in string.punctuation})
        return file_content.translate(table)

    def remove_upper_case_words(self, file_content):
        return " ".join([word for word in file_content if word.islower()])

    def remove_extra_spaces(self, file_content):
        return " ".join(file_content.split())

