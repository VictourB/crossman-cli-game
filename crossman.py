import pathlib
import time
import os
from random import randint

class CrossmanGame:
    """A OOP based CLI game were you must help a man on a cross."""

    def __init__(self, phrase_file: str ="wordphrases.txt", states_file: str = "crossman_states.txt") -> None:
        self.phrase_file = pathlib.Path(phrase_file)
        self.states_file = pathlib.Path(states_file)

        self.full_phrase = self._load_random_phrase()
        self.tried_letters = []
        self.crossman_state = 0
        self.max_lives = 6

    def _load_random_phrase(self) -> str:
        """Loads and parses"""
        try:
            with open(self.phrase_file, 'r', encoding="utf-8") as f:
                phrases = [line.strip().lower() for line in f if line.strip() and "[" not in line]

            if not phrases: return "memento more"
            return phrases[randint(0, len(phrases) - 1)]
        except FileNotFoundError:
            return "malum"

    def _format_view(self) -> str:
        """Returns a single string representing game screen"""
        output = []

        try:
            with open(self.states_file, "r", encoding="utf-8") as f:
                states = f.read().split("%")
                state_idx = min(self.crossman_state, len(states) -1)
                output.append(states[state_idx].strip())
        except FileNotFoundError:
            output.append(f"The crucified man's state: {self.crossman_state}")

        obscured = "".join([char if(not char.isalpha() or char in self.tried_letters) else "_" for char in self.full_phrase])
        output.append(f"\n{obscured.upper()}\n")

        output.append("-" * 30)
        output.append(f"KNOWN LETTERS: {', '.join(self.tried_letters).upper()}")
        output.append(f"TIME LEFT: {self.max_lives - self.crossman_state}")

        return "\n".join(output)

    @staticmethod
    def clear_screen() -> None:
        """Clears the terminal screen"""
        # Windows (nt) and Mac/linux (posix)
        if os.name == 'nt':
            os.system('cls')
        else:
            if os.environ.get("TERM"):
                os.system("clear")
            else:
                print('\n' * 100)

    def draw(self) -> None:
        """Renders the game state"""
        self.clear_screen()
        print(self._format_view())

    def process_guess(self, guess: str) -> None:
        """Handles guesses"""
        guess = guess.lower()

        if not guess:
            return

        # Full Phrase Guess
        if len(guess) > 1:
            if guess != self.full_phrase:
                self.crossman_state += 2
            else:
                self.tried_letters = list(set(self.full_phrase))
            return

        # single letter guess
        if guess not in self.full_phrase:
            self.crossman_state += 1

        if guess not in self.tried_letters:
            self.tried_letters.append(guess)

    @property
    def is_game_over(self) -> bool:
        """Checks for victory or failure"""
        won = all(c in self.tried_letters for c in self.full_phrase if c.isalpha())
        lost = self.crossman_state >= self.max_lives
        return won or lost

    def get_ending(self) -> str:
        """returns the ending message"""
        if self.crossman_state >= self.max_lives:
            return "The man died in horrible agony because of you."
        return "He shall be remembered for all time, and you with him. Thank you!"

def play_game() -> None :
    """Main game driver."""
    playing = True

    while playing:
        game = CrossmanGame()

        while not game.is_game_over:
            game.draw()
            guess = input("Can you hear what the man is saying? Type a letter or solve the phrase: ")
            game.process_guess(guess)

        game.draw()

        print(f"\n{game.get_ending()}\n")

        time.sleep(1)
        replay = input("\nWould you like another chance to be redeemed? (yes/no): ").lower().strip()
        if replay not in ['yes', 'y']:
            print("The History of Crossman ends here.")
            playing = False
            time.sleep(2)

if __name__ == "__main__":
    play_game()
