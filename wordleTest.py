from string import ascii_lowercase as letters
import random

def readInWords():
    with open("words.txt", "r") as wordsFile:
        return wordsFile.read().strip().replace("\"", "").split(",")

def getResult(answer, guess):
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
    def __init__(self, words, start = ""):
        self.words = words
        self.currentWord = start

    def chooseWord(self):
        # dictionary = {}
        # for word in self.words:
        #     dictionary[word] = 0
        # for letter in letters:
        #     wordsWithLetter = []
        #     for word in self.words:
        #         if letter in word:
        #             wordsWithLetter.append(word)
        #     count = len(wordsWithLetter)
        #     for word in wordsWithLetter:
        #         dictionary[word] += count
        # try:
        #    self.currentWord = max(dictionary, key = dictionary.get)
        # except:
        #     pass
        try:
            self.currentWord = random.choice(self.words)
        except:
            pass

    def filterIncorrect(self, letter, count):
        self.words = list(filter(lambda x: x.count(letter) <= count, self.words))

    def filterPartialCorrect(self, letter, i, count):
        self.words = list(filter(lambda x: x.count(letter) >= count and x[i] != letter, self.words))

    def filterFullCorrect(self, letter, i):
        self.words = list(filter(lambda x: x[i] == letter, self.words))

    def isInputValid(self, inp):
        if len(inp) != 5:
            return False
        for letter in inp:
            if letter not in "012":
                return False
        return True

    def playRound(self, result = ""):
        if self.isInputValid(result):
            for i in range(5):
                count = 0
                for j in range(5):
                    if self.currentWord[j] == self.currentWord[i] and (result[j] in "12"):
                        count += 1
                if result[i] == "0":
                    self.filterIncorrect(self.currentWord[i], count)
                elif result[i] == "1":
                    self.filterPartialCorrect(self.currentWord[i], i, count)
                elif result[i] == "2":
                    self.filterFullCorrect(self.currentWord[i], i)
            self.chooseWord()
        elif not self.currentWord:
            self.chooseWord()
        return self.currentWord

allWords = readInWords()
checked = 0
solutions = []
with open ("solutions.txt", "r") as file:
    solutions = file.read().strip().split("\n")
total = len(solutions)
# start = False
# startWord = "aback"
# for starter in solutions:
#     if not start:
#         if starter == startWord:
#             start = True
#         else:
#             continue
#     failed = 0
#     for word in solutions:
#         solver = Solver(allWords, starter)
#         result = ""
#         answer = ""
#         for i in range(6):
#             answer = solver.playRound(result)
#             if answer == word:
#                 break
#             result = getResult(word, answer)
#         if answer != word:
#             failed += 1
#     print(f"{starter}: {total - failed}")
#     with open("results.txt", "a") as file:
#         file.write(f"{starter} {total - failed}\n")
#     checked += 1
#     if (checked % 100 == 0):
#         print(f'Checked {checked} words')
# results = {}
# with open("results.txt", "r") as file:
#     saved = file.readlines()
#     for entry in saved:
#         line = entry.strip().split()
#         results[line[0]] = int(line[1])
# print(f"The best starting word is: {max(results, key = results.get)}")
failed = 0
for word in solutions:
    solver = Solver(allWords, "")
    result = ""
    answer = ""
    for i in range(6):
        answer = solver.playRound(result)
        if answer == word:
            break
        result = getResult(word, answer)
    if answer != word:
        failed += 1
    checked += 1
    if (checked % 500 == 0):
        print(f'Checked {checked} words')
print(f'Passed {total - failed} / {total} words')
