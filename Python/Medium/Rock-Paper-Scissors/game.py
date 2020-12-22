# Write your code here
import random

RATING_FILE_NAME = 'rating.txt'
ROCK = 'rock'
PAPER = 'paper'
SCISSORS = 'scissors'
DEFAULT_OPTIONS = [ROCK, PAPER, SCISSORS]
RATING = '!rating'
EXIT = '!exit'
COMMANDS = [RATING]

WIN = 1
DRAW = 0
LOSE = -1


def main():
    score = greet(RATING_FILE_NAME)
    choices = input().split(',')
    if choices == ['']:
        choices = DEFAULT_OPTIONS
    print("Okay, let's start")
    option = input()
    while option != EXIT:
        if option in COMMANDS:
            handle_cmd(option, score)
        elif option in choices:
            score += play(option, choices)
        else:
            print('Invalid input')
        option = input()


def play(choice, choices):
    computer_choice = random.choice(choices)
    res = fight(choice, computer_choice, choices)
    if res == WIN:
        print(f'Well done. Computer chose {computer_choice} and failed')
        return 100
    elif res == LOSE:
        print(f'Sorry, but computer chose {computer_choice}')
        return 0
    print(f'There is a draw ({choice})')
    return 50


def fight(player_choice, computer_choice, choices):
    p, c = choices.index(player_choice), choices.index(computer_choice)
    if p == c:
        return DRAW
    d = p - c
    if d < 0:
        d += len(choices)
    if d <= len(choices) // 2:
        return WIN
    return LOSE


def handle_cmd(cmd, score):
    if cmd == RATING:
        print(f'Your rating: {score}')


def greet(f_name):
    name = input('Enter your name: ')
    print('Hello, ' + name)
    with open(f_name, 'r') as file:
        scores = {line.split()[0]: line.split()[1] for line in file.read().splitlines()}
    return 0 if name not in scores else scores[name]


if __name__ == '__main__':
    main()
