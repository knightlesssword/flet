import json
import logging
import os.path
import random

import flet
from flet import Page
from flet_core import ScrollMode, TextField, ElevatedButton, Text, colors, FontWeight, AlertDialog, TextButton, \
    MainAxisAlignment, SnackBar, Column, TextAlign, Row, Icon, icons, CrossAxisAlignment, Container

logging.basicConfig(
    filename='number_guessing_game.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

SCORES_FILE = 'scores.json'
NUMBER_RANGE = (1, 100)
MAX_LIVES = 5

def initialize_score():
    default_scores = {
        "consecutive_score": 0,
        "high_score": {
            "score": 0,
            "player": ""
        }
    }
    if not os.path.exists(SCORES_FILE):
        with open(SCORES_FILE, 'w') as f:
            json.dump(default_scores, f, indent=4)
        return default_scores

    else:
        with open(SCORES_FILE, 'r') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                logging.error("Scores file is corrupted! Resetting scores.")
                with open(SCORES_FILE, 'w') as fw:
                    json.dump(default_scores, fw, indent=4)
                return default_scores

def save_scores(scores):
    with open(SCORES_FILE, 'w') as f:
        json.dump(scores, f, indent=4)

def build_lives_display(lives_remaining):
    hearts = []
    for _ in range(lives_remaining):
        hearts.append(
            Icon(
                icons.FAVORITE,
                color=colors.RED,
                size=30
            )
        )
    return Row(
        controls=hearts,
        alignment=MainAxisAlignment.CENTER,
        spacing=5
    )

def main(page: Page):
    page.title = "GuessMe - A number guessing game!"
    page.window.width = 500
    page.window.height = 500
    page.padding = 20
    page.scroll = ScrollMode.AUTO

    scores = initialize_score()

    game_state = {
        "target_number": random.randint(*NUMBER_RANGE),
        "lives": MAX_LIVES,
        "consecutive_score": scores.get("consecutive_score", 0),
        "high_score": scores.get("high_score", {"score": 0, "player":""}),
        "guesses": []
    }

    lives_display = build_lives_display(game_state["lives"])
    guess_input = TextField(label=f'Guess a number between 1 and 100', width=300)
    hints_text = Text(value="", size=14, color=colors.BLUE)
    score_text = Text(f"Score: {game_state['consecutive_score']}", size=16, weight=FontWeight.BOLD)
    high_score_text = Text(f"High Score: {scores['high_score']['score']} by {scores['high_score']['player']}", size=16, weight=FontWeight.BOLD)
    guess_button = ElevatedButton(text="Guess!", on_click=lambda e: process_guess(e, game_state, page, guess_input, lives_display, hints_text, score_text))

    # high score alert dialog
    high_score_dialog = AlertDialog(
        title= Text("New High Score!"),
        content= Column([
            Text("Congratulations! You have achieved a new high score!"),
            TextField(label="Enter your name", autofocus=True)
        ]),
        actions= [
            TextButton("Submit", on_click=lambda e: submit_high_score(e, high_score_dialog, game_state, scores, page, high_score_text))
        ],
        actions_alignment=MainAxisAlignment.END,
    )

    def process_guess(e, state, page, input_field, lives_display, hints, score):
        guess = input_field.value.strip()
        if not guess.isdigit():
            snack_bar = SnackBar(content=Text("Please enter a valid number!"))
            page.overlay.append(snack_bar)
            snack_bar.open = True
            page.update()
            return

        guess = int(guess)
        target = state["target_number"]

        if not (NUMBER_RANGE[0] <= guess <= NUMBER_RANGE[1]):
            snack_bar = SnackBar(content=Text("Please enter a number between 0-100!"))
            page.overlay.append(snack_bar)
            snack_bar.open = True
            page.update()
            return

        state["guesses"].append(guess)
        print(target)
        if guess == target:
            state["consecutive_score"] += 1
            hints.value = f"Correct! You've guessed {target} correctly!"
            snack_bar = SnackBar(content=Text("Congratulations! You guessed the correct number."))
            page.overlay.append(snack_bar)
            snack_bar.open = True
            page.update()
            state["target_number"] = random.randint(*NUMBER_RANGE)
        elif guess < target:
            state["lives"] -= 1
            hints.value = "Too low! Guess higher."
            snack_bar = SnackBar(content=Text("Too low! Guess higher."))
            page.overlay.append(snack_bar)
            snack_bar.open = True
            page.update()
            update_lives_display(state, page, lives_display)
        else:
            state["lives"] -= 1
            hints.value = "Too high! Guess lower."
            snack_bar = SnackBar(content=Text("Too high! Guess lower."))
            page.overlay.append(snack_bar)
            snack_bar.open = True
            page.update()
            update_lives_display(state, page, lives_display)

        if state["lives"] == 0:
            hints.value = f"Game over! The correct number was {target}."
            snack_bar = SnackBar(content=Text(f"Game Over! The correct number was {target}."))
            page.overlay.append(snack_bar)
            snack_bar.open = True
            page.update()
            check_high_score(state, scores, page, high_score_dialog)
            reset_game(state, page, input_field, lives_display, hints)

        score.value = f"Score: {state['consecutive_score']}"
        page.update()

    def update_lives_display(state, page, lives_display):
        lives_display.controls = build_lives_display(state["lives"]).controls
        page.update()

    def reset_game(state, page, input_field, lives_display, hints):
        state["target_number"] = random.randint(*NUMBER_RANGE)
        state["lives"] = MAX_LIVES
        state["guesses"] = []
        input_field.value = ""
        hints.value = ""
        lives_display.controls = build_lives_display(state["lives"]).controls
        page.update()

    def check_high_score(state, scores, page, dialog):
        if state["consecutive_score"] > scores["high_score"]["score"] and state["lives"] == 0:
            page.overlay.append(dialog)
            dialog.open = True
            page.update()

    def submit_high_score(e, dialog, state, scores, page, high_score_text):
        player_name = dialog.content.controls[1].value.strip()
        if not player_name:
            snack_bar = SnackBar(content=Text("Please enter your name to save the high score."))
            page.overlay.append(snack_bar)
            snack_bar.open = True
            page.update()
            return

        scores["high_score"]["score"] = state["consecutive_score"]
        scores["high_score"]["player"] = player_name
        save_scores(scores)
        high_score_text.value = f"High Score: {scores['high_score']['score']} by {scores['high_score']['player']}"
        snack_bar = SnackBar(content=Text("High score saved!"))
        page.overlay.append(snack_bar)
        snack_bar.open = True
        dialog.open = False
        page.update()

    page.add(
        Column(
                [
                    Text(
                        value= "GuessMe!",
                        size= 30,
                        weight= FontWeight.BOLD,
                        color= colors.ORANGE,
                        text_align=TextAlign.CENTER
                    ),
                    Text(
                        value= "A number guessing game",
                        size= 15,
                        weight=FontWeight.NORMAL,
                        color= colors.BLUE_ACCENT_100,
                        text_align=TextAlign.CENTER
                    ),
                    Row(
                        [
                            Text("Lives remaining: ", size=12, weight=FontWeight.W_500),
                            lives_display
                        ],
                        alignment=MainAxisAlignment.CENTER,
                        spacing=10
                    ),
                    Row(
                        [
                            guess_input,
                        ],
                        alignment=MainAxisAlignment.CENTER,
                        spacing=10
                    ),
                    Row(
                        [
                            guess_button
                        ],
                        alignment=MainAxisAlignment.CENTER,
                        spacing=10
                    ),
                    hints_text,
                    Row(
                        [
                            score_text,
                        ],
                        alignment=MainAxisAlignment.CENTER,
                        spacing=10
                    ),
                    Row(
                        [
                            high_score_text,
                        ],
                        alignment=MainAxisAlignment.CENTER,
                        spacing=10
                    ),
                ],
                alignment=MainAxisAlignment.CENTER,
                horizontal_alignment=CrossAxisAlignment.CENTER,
                spacing=20
        ),
        Container(
            Row(
                controls=[
                    Text("Made with", size=12),
                    Icon(icons.FAVORITE, size=12, color=colors.RED),
                    Text("in Flet by Abu Bakr.", size=12)
                ],
                alignment=MainAxisAlignment.CENTER
            )
        ),
    )

if __name__ == '__main__':
    flet.app(target=main)
