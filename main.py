from math import floor
import random


def find_key(dict, value):
    return list(dict.keys())[list(dict.values()).index(value)]


def clear():
    print("\033[H\033[J", end="")


def yesno(text, default):
    text = text.lower()
    if not text:
        return default

    if text[0] == "y":
        return True
    if text[0] == "n":
        return False
    if text == "true":
        return True
    if text == "false":
        return False
    if text == "1":
        return True
    if text == "0":
        return False

    return default


def print_info(text):
    print("\x1b[36m" + "🛈  " + text + TEXT_RESET)


def print_error(text):
    print("\x1b[31m" + "🚫 " + text + TEXT_RESET)


def warning_confirmation(text):
    user_input = input(
        "\x1b[33m" + "⚠️  " + text + TEXT_RESET + " ",
    )
    result = yesno(user_input, None)

    if result == None:
        print("\x1b[33m\n   " + "Type 'yes' or 'no' to confirm/decline:" + TEXT_RESET)
        return warning_confirmation(text)

    return result


def generate_empty_attempt(items):
    output = []
    for i in range(items):
        output.append("")
    return output


def generate_solution(colors, width=4):
    solution = generate_empty_attempt(width)
    used_colors = []

    i = 0
    for color in solution:
        choice = ""
        while (choice in solution) or (choice == ""):
            choice = random.choice(colors)
        solution[i] = choice
        used_colors.append(solution[i])
        i += 1

    return solution


def calculate_correct_colors(attempt, solution):
    correct_colors = 0
    i = 0
    for correct_color in solution:
        # if `attempt` contains the color that we're checking for,
        # then increment `correct_colors`, unless it is also correctly-placed
        if attempt.count(correct_color) and correct_color != attempt[i]:
            correct_colors += 1
        i += 1
    return correct_colors


def calculate_correct_placements(attempt, solution):
    correct_placements = 0
    i = 0
    for attempted_color in attempt:
        if solution[i] == attempted_color:
            correct_placements += 1
        i += 1
    return correct_placements


def print_colors(colors, shorthands):
    print("Available colours:")
    for color in colors:
        shorthand = find_key(shorthands, color)
        index = color.index(shorthand)
        processed_color = "  " + color[:index] + f"[{shorthand}]" + color[index + 1 :]
        print(processed_color)
    print()


def display_topbar(current_attempt, total_attempts):
    print(f"=====| ATTEMPT {current_attempt}/{total_attempts} |=====")


def display_bottombar(correct_colors, correct_placements):
    print(f" ⚪ Correct colours:   ", correct_colors)
    print(f" ⚫ Correct placements:", correct_placements)
    print()


def config_max_attempts():
    global max_attempts
    print("Current maximum attempts:", max_attempts)
    max_attempts = int(input("New maximum attempts: "))


def config_inline_inputs():
    global use_inline_input
    print("'Inline input' lets you write your guess on a single line.")
    print("You type your guess by seperating each colour with a comma.")
    print("Inline input is currently:", "Enabled" if use_inline_input else "Disabled")
    print()
    use_inline_input = yesno(
        input("Do you want to use inline input? "), use_inline_input
    )


def validate_max_attempts(value):
    if value > 1:
        return True

    if value == 0:
        return warning_confirmation(
            "Are you sure that you don't want to give yourself any chances to guess the combination?"
        )

    if value == 1:
        return warning_confirmation(
            "Are you sure that you only want to give yourself one chance to guess the combination?"
        )


def validate_board_width(value):
    if value != 0:
        return True

    print()
    print_error("You cannot have a board width of zero!")
    input("Press enter keep original value...")


def run_action(action, message=""):
    clear()
    print("==== " + action["title"].title() + " ====")
    if action["description"]:
        print(action["description"] + "\n")

    print("Default value:", action["default"])
    current_value = config[action["key"]] if action["key"] in config else None
    if current_value:
        print("Current value:", current_value)

    print()
    if message:
        print(message)
    verb = "Change" if current_value else "Set"
    new_value = input(verb + " value: ")
    if new_value == "":
        return False

    if action["number"]:
        if new_value.isnumeric():
            new_value = int(new_value)
            if new_value < 0:
                return run_action(action, "Enter a positive number!")
        else:
            return run_action(action, "Input needs to be a number!")

    if action["validator"]:
        keep_new_value = action["validator"](new_value)
        if not keep_new_value:
            return False

    if action["transformer"]:
        config[action["key"]] = action["transformer"](new_value)
        return True

    config[action["key"]] = new_value
    return True


def show_config_screen():
    def add_action(
        name,
        key,
        default,
        title=None,
        description=None,
        number=False,
        validator=None,
        transformer=None,
    ):
        actions.append(
            {
                "name": name,
                "key": key,
                "default": default,
                "title": title or f"Configuring {name.lower()}",
                "text": title or f"Edit {name.lower()}",
                "description": description,
                "number": number or type(default) is int,
                "validator": validator,
                "transformer": transformer,
            }
        )

    actions = []

    clear()
    print("\033[1m" + "CUSTOMISE YOUR GAME OF MASTERMIND" + "\033[0m" + "\n")

    add_action(
        "Maximum attempts",
        "max_attempts",
        10,
        title="Change maximum attempts",
        validator=validate_max_attempts,
    )
    add_action(
        "Board width",
        "width",
        4,
        description="'Board width' represents the number of colours that the combination has.\nIt is recommended to keep it at the default for optimal gameplay, but you can change it if you're feeling adventurous.",
        validator=validate_board_width,
    )
    # add_action("Disable shorthands")
    # add_action("Configure inline colour input")

    print_info(
        "Press Enter to start the game, or enter a number to configure an option.\n"
    )

    if config == {}:
        for action in actions:
            config[action["key"]] = action["default"]

    i = 0
    for action in actions:
        spaced_number = str(i + 1)
        for i in range(floor(len(actions) / 10) - len(spaced_number)):
            spaced_number += " "

        print(f"  {spaced_number}. {action['text']}")
        i += 1

    input_text = input("> ")
    if not input_text:
        return clear()

    chosen_action = int(input_text) - 1
    if chosen_action == -1:
        return clear()
    if chosen_action > len(actions):
        print("Not a valid option! Enter a number from the list, or 0 to exit.")
        print()
        show_config_screen()

    value_edited = run_action(actions[chosen_action])
    if value_edited:
        input("Value updated! Press enter to continue...")
    show_config_screen()


TEXT_RESET = "\x1b[0m"

dev = True
max_attempts = 10
use_inline_input = False
colors = ["blue", "green", "black", "red", "yellow", "white"]
config = {}
attempts = 0
last_response_was_valid = True
correct_colors = 0
correct_placements = 0
game_over = False
shorthands = {
    "b": "blue",
    "g": "green",
    "k": "black",
    "r": "red",
    "y": "yellow",
    "w": "white",
}

show_config_screen()
current_attempt = generate_empty_attempt(config["width"])
solution = generate_solution(colors, config["width"])
print_colors(colors, shorthands)
if dev:
    print("The solution is:", solution, "\n")

while current_attempt != solution:
    # Increment `attempts`
    attempts += 1

    # Check if the user has run out of turns
    if attempts > config["max_attempts"]:
        game_over = True
        break

    display_topbar(attempts, config["max_attempts"])

    # Reset `position` to 0
    position = 0
    while position < config["width"]:
        tag = " " if last_response_was_valid else "!"

        # Display the prompt, to let the user input their colour
        current_attempt[position] = input(f"{tag}{position+1}> ").lower()

        # Expand any shorthands that were used
        if len(current_attempt[position]) == 1:
            if current_attempt[position] in shorthands:
                current_attempt[position] = shorthands[current_attempt[position]]

        # Mark the response as valid if the user inputted a valid colour
        # TODO: Don't let the user put the same colour in multiple positions?
        if colors.count(current_attempt[position]):
            # Let the user move on to the next position
            position += 1
            last_response_was_valid = True
        else:
            last_response_was_valid = False

    # Re-calculate statistics
    correct_colors = calculate_correct_colors(current_attempt, solution)
    correct_placements = calculate_correct_placements(current_attempt, solution)

    display_bottombar(correct_colors, correct_placements)
print()

if game_over:
    # print("=============| GAME OVER |=============")
    print("=============| YOU DIED! |=============")
    print("⚪ Correct colours:         ", correct_colors + correct_placements)
    print("⚫ Correctly-placed colours:", correct_placements)
    print()

    print("The solution was: ")
    i = 0
    for position in solution:
        checkmark = "❎"
        if position == current_attempt[i]:
            checkmark = "✅"
        print(f" {checkmark} {i+1}. {position}")
        i += 1
else:
    print("=========| CONGRATULATIONS! |=========")
    print("⚪ Correct colours:         ", correct_colors + correct_placements, "🎉")
    print("⚫ Correctly-placed colours:", correct_placements, "🎉")
    print()
    print(f"You found the solution in {attempts} attempts!")

print()
print("Bye!")
