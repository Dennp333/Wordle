from scipy.stats import entropy
from wordleBot import getResult

words = []
with open ("words.txt", "r") as file:
    words = file.read().strip().replace("\"", "").split(",")
solutions = []
with open("solutions.txt", "r") as file:
    solutions = file.read().strip().split()
total = len(solutions)
entropies = {}

for word in words:
    results = {}
    for answer in solutions:
        result = getResult(word, answer)
        if result in results:
            results[result] += 1
        else:
            results[result] = 1
    freqs = list(results.values())
    probs = [(freq / total) for freq in freqs]
    info = entropy(probs, base = 2)
    entropies[word] = info
    print(f"{word}: {info}")
    with open("firstword.txt", "a") as file:
        file.write(f"{word} {info}\n")

print(f"The best starting word is: {max(entropies, key = entropies.get)}")
for i in range(10):
    best = max(entropies, key = entropies.get)
    print(best)
    del entropies[best]
