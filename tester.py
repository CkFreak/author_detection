class Tester:

    def __init__(self, matrix, chain):
        self.accuracy = self.give_accuracy(matrix, chain)

    def give_accuracy(self, matrix, chain):
        total_probability = 0
        for word in range (0, len(chain) - 1):
            if chain[word] in matrix and chain[word + 1] in matrix[chain[word]]:
                total_probability += matrix[chain[word]][chain[word + 1]]
        return total_probability
