# Wordle
You will need the scipy package to run this project.<br />
To play, run the file play.py. After entering the prompted word into Wordle, enter a 5-digit number representing the result given by Wordle. The digit 0 represents the letter not being present in the word. The digit 1 means the letter is present but not in that location. The digit 2 means the letter is correct and in the correct position. <br />
This Wordle algorithm is able to solve all available words (12 947 words) with 99.44% accuracy. The file test.py is used to test the algorithm against all possible solutions. This file takes an optional command line argument, representing the word in words.txt it should start at.
The files wordleFirstWord.py and wordleSecondWord.py are scripts for generating the first and second words used by wordleBot.py. Since the algorithm would take a long time to compute its first and second guesses, it instead reads those guesses from firstWord.txt and secondWord.txt.
