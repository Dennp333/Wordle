import time
import datetime
import sys
from wordleBot import *

beginningWord = "cigar"
if len(sys.argv > 1):
    beginningWord = sys.argv[1]
allWords = []
with open("words.txt", "r") as file:
    allWords = file.read().strip().replace("\"", "").split(",")
solutions = []
with open ("words.txt", "r") as file:
    solutions = file.read().strip().replace("\"", "").split(",")
checked = 0
start = False
startTime = time.time()
for word in solutions:
    if not start:
        if word == beginningWord:
            start = True
        else:
            checked += 1
            continue
    solver = Solver(allWords, solutions)
    result = ""
    choice = ""
    while solver.round < 6:
        choice = solver.playRound(result)
        if choice == word:
            break
        result = getResult(choice, word)
    if choice != word:
        print(f"Failed: {word}")
        with open("results.txt", "a") as file:
            file.write(f"{word} failed\n")
    else:
        with open("results.txt", "a") as file:
            file.write(f"{word} passed\n")
    checked += 1
    if (checked % 100 == 0):
        print(f'Checked {checked} words')
        currentTime = time.time()
        remaining = (12947 - checked) / 100 * (currentTime - startTime)
        startTime = currentTime
        print(f"Remaining time: {datetime.timedelta(seconds=remaining)}")
failed = 0
with open("results.txt", "r") as file:
    saved = file.readlines()
    for entry in saved:
        line = entry.strip().split()
        if line[1] == "failed":
            failed += 1

print(f'Passed {12947 - failed} / 12947 words')
