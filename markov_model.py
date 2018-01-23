class MarkovModel:

    def __init__(self, chain):
        self.transition_matrix = {}
        self.create_transition_matrix(chain)

    def create_transition_matrix(self, chain):
        previous_char = chain[0]
        for char in range(1, len(chain)):
            if previous_char not in self.transition_matrix:
                self.transition_matrix[previous_char] = {}
                self.transition_matrix[previous_char][chain[char]] = 0
            if chain[char] not in self.transition_matrix[previous_char]:
                self.transition_matrix[previous_char][chain[char]] = 0
            self.transition_matrix[previous_char][chain[char]] += 1
            previous_char = chain[char]

        for letter in self.transition_matrix:
            total = 0
            for sub_letter in self.transition_matrix[letter]:
                total += self.transition_matrix[letter][sub_letter]
            for sub_letter in self.transition_matrix[letter]:
                self.transition_matrix[letter][sub_letter] /= total