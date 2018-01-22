class Tester:

    def __init__(self, matrix, chain):
        self.accuracy = self.give_accuracy(matrix, chain)

    def give_accuracy(self, matrix, chain):
        total_probability = 0
        for char in range (0, len(chain) - 1):
            if chain[char] in matrix and chain[char + 1] in matrix[chain[char]]:
                total_probability += matrix[chain[char]][chain[char + 1]]
        return total_probability
