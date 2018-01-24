class MarkovModel:

    # Initializes this class.
    # after this is done self.transition_matrix will hold the transition matrix for the given chain
    def __init__(self, chain):
        self.transition_matrix = {}
        self.create_transition_matrix(chain)

    # Creates a transition matrix using an array as input.
    # Every word is a key in the matrix for later.
    # Every key holds a dictionary that holds as keys words that followed the first word
    # and as value the probability that this word will actually follow.
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
