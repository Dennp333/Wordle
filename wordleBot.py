from scipy.stats import entropy

def getResult(guess, answer):
    result = [0, 0, 0, 0, 0]
    for i in range(5):
        if answer[i] == guess[i]:
            result[i] = 2
        elif guess[i] not in answer:
            result[i] = 0
        else:
            result[i] = 1
    for letter in guess:
        diff = guess.count(letter) - answer.count(letter)
        for i in range(5):
            if result[i] == 0 and guess[i] == letter:
                diff -= 1
        if diff > 0:
            indices = []
            for i in range(5):
                if result[i] == 1 and guess[i] == letter:
                    indices.append(i)
            for i in range(diff):
                result[indices[i]] = 0
    
    return "".join(str(n) for n in result)

class Solver:
    def __init__(self, words, solutions):
        self.words = words
        self.solutions = solutions
        self.currentWord = "raise"
        self.round = 0
        self.entropies = {}
        self.secondWords = []

    def chooseWord(self):
        if len(self.solutions) == 1:
            self.currentWord = self.solutions[0]
        else:
            total = len(self.solutions)
            entropies = {}
            for word in self.words:
                results = {}
                for answer in self.solutions:
                    result = getResult(word, answer)
                    if result in results:
                        results[result] += 1
                    else:
                        results[result] = 1
                freqs = list(results.values())
                probs = [(freq / total) for freq in freqs]
                info = entropy(probs, base = 2)
                entropies[word] = info
            self.entropies = entropies
            self.selectFromEntropyDict(entropies)
    
    def selectFromEntropyDict(self, entropies):
        maxEntropy = 0
        for word in entropies:
            if entropies[word] > maxEntropy:
                maxEntropy = entropies[word]
                self.currentWord = word
            elif entropies[word] == maxEntropy and word in self.solutions:
                self.currentWord = word

    def isInputValid(self, inp):
        if len(inp) != 5:
            return False
        for letter in inp:
            if letter not in "012":
                return False
        return True

    def filterSolutions(self, result):
        for i in range(5):
            count = 0
            for j in range(5):
                if self.currentWord[j] == self.currentWord[i] and (result[j] in "12"):
                    count += 1
            if result[i] == "0":
                self.solutions = list(filter(lambda x: x.count(self.currentWord[i]) <= count, self.solutions))
            elif result[i] == "1":
                self.solutions = list(filter(lambda x: x.count(self.currentWord[i]) >= count and x[i] != self.currentWord[i], self.solutions))
            elif result[i] == "2":
                self.solutions = list(filter(lambda x: x[i] == self.currentWord[i], self.solutions))

    def playRound(self, result):
        if self.round == 0:
            self.round += 1
            return self.currentWord
        if self.isInputValid(result):
            self.round += 1
            if self.round == 2:
                self.filterSolutions(result)
                choices = {}
                with open("secondword.txt", "r") as file:
                    contents = file.read().strip().splitlines()
                    for line in contents:
                        entry = line.split()
                        choices[entry[0]] = entry[1:]
                self.currentWord = choices[result][0]
                self.secondWords = choices[result]
            else:
                self.filterSolutions(result)
                self.chooseWord()
        elif self.round == 2:
            self.words.remove(self.currentWord)
            self.secondWords.pop(0)
            self.currentWord = self.secondWords[0]
        else:
            self.words.remove(self.currentWord)
            del self.entropies[self.currentWord]
            self.selectFromEntropyDict(self.entropies)
        return self.currentWord
