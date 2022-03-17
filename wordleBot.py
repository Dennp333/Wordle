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
            #self.solutions = list(filter(lambda x: getResult(self.currentWord, x) == result, self.solutions))
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

allWords = []
with open("words.txt", "r") as file:
    allWords = file.read().strip().replace("\"", "").split(",")
solutions = []
with open("words.txt", "r") as file:
    solutions = file.read().strip().replace("\"", "").split(",")
solver = Solver(allWords, solutions)
result = "00000"
while solver.round < 6:
    word = solver.playRound(result)
    print(f"Next word: {word}")
    result = input("Enter the result: ")
    if result == "22222":
        print(f"Possible words remaining: {','.join(solver.solutions)}")
        break

# allWords = []
# with open("words.txt", "r") as file:
#     allWords = file.read().strip().replace("\"", "").split(",")
# solutions = []
# with open ("words.txt", "r") as file:
#     solutions = file.read().strip().replace("\"", "").split(",")
# checked = 0
# start = False
# beginningWord = "patty"
# startTime = time.time()
# for word in solutions:
#     if not start:
#         if word == beginningWord:
#             start = True
#         else:
#             checked += 1
#             continue
#     solver = Solver(allWords, solutions)
#     result = ""
#     choice = ""
#     while solver.round < 6:
#         choice = solver.playRound(result)
#         if choice == word:
#             break
#         result = getResult(choice, word)
#     if choice != word:
#         print(f"Failed: {word}")
#         with open("results.txt", "a") as file:
#             file.write(f"{word} failed\n")
#     else:
#         with open("results.txt", "a") as file:
#             file.write(f"{word} passed\n")
#     checked += 1
#     if (checked % 100 == 0):
#         print(f'Checked {checked} words')
#         currentTime = time.time()
#         remaining = (12947 - checked) / 100 * (currentTime - startTime)
#         startTime = currentTime
#         print(f"Remaining time: {datetime.timedelta(seconds=remaining)}")
# failed = 0
# with open("results.txt", "r") as file:
#     saved = file.readlines()
#     for entry in saved:
#         line = entry.strip().split()
#         if line[1] == "failed":
#             failed += 1

# print(f'Passed {12947 - failed} / 12947 words')
