import sys
from scipy.stats import entropy
from wordleBot import getResult

firstWord = "raise"
if len(sys.argv) > 1:
    firstWord = sys.argv[1]
words = []
solutions = []
with open ("words.txt", "r") as file:
    words = file.read().strip().replace("\"", "").split(",")
with open ("words.txt", "r") as file:
    solutions = file.read().strip().replace("\"", "").split(",")
allResults = {}
for word in solutions:
    result = getResult(firstWord, word)
    if result in allResults:
        allResults[result].append(word)
    else:
        allResults[result] = [word]
for result in allResults:
    total = len(allResults[result])
    entropies = {}
    for word in words:
        results = {}
        for answer in allResults[result]:
            currentResult = getResult(word, answer)
            if currentResult in results:
                results[currentResult] += 1
            else:
                results[currentResult] = 1
        freqs = list(results.values())
        probs = [(freq / total) for freq in freqs]
        info = entropy(probs, base = 2)
        entropies[word] = info
    bestwords = []
    for i in range(10):
        bestWord = max(entropies, key = entropies.get)
        bestwords.append(bestWord)
        del entropies[bestWord]
    print(f"{result} {bestWord}")
    with open("secondword.txt", "a") as file:
        file.write(result + " ".join(bestwords))
