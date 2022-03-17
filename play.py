from wordleBot import Solver

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
