class MarkovModel:

    def __init__(self, chain):
        self.transition_matrix = {}
        self.create_transition_matrix(chain)

    def create_transition_matrix(self, chain):
        previous_word = chain[0]
        for word in range(1, len(chain)):
            if previous_word not in self.transition_matrix:
                self.transition_matrix[previous_word] = {}
                self.transition_matrix[previous_word][chain[word]] = 0
            if chain[word] not in self.transition_matrix[previous_word]:
                self.transition_matrix[previous_word][chain[word]] = 0
            self.transition_matrix[previous_word][chain[word]] += 1
            previous_word = chain[word]

        for word in self.transition_matrix:
            total = 0
            for sub_word in self.transition_matrix[word]:
                total += self.transition_matrix[word][sub_word]
            for sub_word in self.transition_matrix[word]:
                self.transition_matrix[word][sub_word] /= total
