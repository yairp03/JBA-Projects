# Write your code here
import random
WORDS = ('python', 'java', 'kotlin', 'javascript')
CMD_LIST = ('play', 'exit')


def main():
    print("H A N G M A N")
    while get_cmd() == 'play':
        secret_word = random.choice(WORDS)
        used_letters = set()
        misses = 0
        while True:
            print('\n' + get_secret_word(secret_word, used_letters))
            letter = input('Input a letter: ')
            if not validate_input(letter):
                continue
            if letter in used_letters:
                print('You already typed this letter')
            else:
                used_letters.add(letter)
                if letter not in secret_word:
                    print('No such letter in the word')
                    misses += 1
                    if misses == 8:
                        break
                else:
                    if get_secret_word(secret_word, used_letters).find('-') == -1:
                        break

        if misses < 8:
            print('You guessed the word', secret_word)
            print('You survived!')
        else:
            print('You are hanged!')


def get_cmd():
    cmd = input('Type "play" to play the game, "exit" to quit: ')
    while cmd not in CMD_LIST:
        cmd = input('Type "play" to play the game, "exit" to quit: ')
    return cmd


def validate_input(letter: str):
    if len(letter) != 1:
        print('You should input a single letter')
    elif not (letter.isalpha() and letter.islower()):
        print('It is not an ASCII lowercase letter')
    else:
        return True
    return False


def get_secret_word(secret_word: str, used_letters: set):
    res = ''
    for c in secret_word:
        if c in used_letters:
            res += c
        else:
            res += '-'
    return res


if __name__ == '__main__':
    main()
