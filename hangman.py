#! python3
#by Victour Bue

# commandlineHangman.py - A simple hangman game where you save Jesus.

from random import randint
import time


def invite_player():
    response = input("\nDo you want to play Hangman? Yes/No \n")
    if response.lower() == "yes" or response.lower() == "no":
        return response
    else:
        print("Please enter yes or no.")
        return invite_player()


def load_phrases():
    with open("wordphrases.txt") as phrase_file:
        phrase_content = phrase_file.read()
        phrase_content = phrase_content.lower()
        phrase_list = phrase_content.splitlines()

    return phrase_list


def parse_random_phrase(phrasels):
    selected_phrase = phrasels[randint(0, len(phrasels)-1)]
    spaced_selected_phrase = " ".join(selected_phrase)

    return spaced_selected_phrase


def obscure_phrase_from_list(phrase):
    obscured_phrase = ""
    for char in phrase:
        if char.isalpha():
            obscured_phrase += "_"
        else:
            obscured_phrase += char

    return obscured_phrase


def display_phrase(phrase, letterls):
    print("\n" + phrase + "\n")

    print(f"KNOWN LETTERS: {letterls}")
    

def get_player_guess():
    print("Type a letter to guess. Type the entire phrase to solve puzzle.")
    player_guess = input()
    print("\n")
    return player_guess
    

def update_phrase(guess, obscured_str, full_str, tried_letters, hangman_state):
    updated_phrase = ""
    index = 0
    if len(guess) == 1:
        for char in full_str:
            if char == guess.lower():
                updated_phrase += full_str[index]
                index += 1
            else:
                updated_phrase += obscured_str[index]
                index += 1

        if not guess in tried_letters:
            tried_letters.append(guess)
        if updated_phrase == obscured_str: hangman_state += 1
        return updated_phrase, tried_letters, hangman_state
    else:
        spaced_guess = " ".join(guess)
        if(spaced_guess.lower() == full_str):
            print("You guessed the whole phrase? \n")
            updated_phrase = full_str
            return updated_phrase, tried_letters, hangman_state
        else:
            hangman_state += 1
            updated_phrase = obscured_str
            return updated_phrase, tried_letters, hangman_state


def draw_hangman(current_state):
    hangman_str = ""
    with open("hangman_states.txt") as hangman_text:
        hangman_content = hangman_text.read()
        hangman_states = hangman_content.split("%")
        print(hangman_states[len(hangman_states) - current_state - 1])


def check_gameover(hangman_state, obscured_str, full_str):
    if(hangman_state > 5):
        print("you Lose :( \n")
        time.sleep(3)
        return False
    if(obscured_str == full_str):
        print("You Win! \n")
        time.sleep(3)
        return False

    return True


def main():
    if invite_player() == "no":
        return

    phrase_list = load_phrases()
    parsed_phrase_str = parse_random_phrase(phrase_list)
    obscured_phrase = obscure_phrase_from_list(parsed_phrase_str)
    hangman_state = 0
    tried_letters = []
    display_phrase(obscured_phrase, tried_letters)
    draw_hangman(hangman_state)
    
    while True:
        player_guess = get_player_guess()
        obscured_phrase, tried_letters, hangman_state = update_phrase(player_guess, obscured_phrase, parsed_phrase_str, tried_letters, hangman_state)
        display_phrase(obscured_phrase, tried_letters)
        draw_hangman(hangman_state)
        if not check_gameover(hangman_state, obscured_phrase, parsed_phrase_str):
            break

    return main()

if __name__ == "__main__":
    main()
