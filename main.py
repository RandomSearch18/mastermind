import random

def find_key(dict, value):
    return list(dict.keys())[list(dict.values()).index(value)]

def clear(): print("\033[H\033[J", end="")

def yesno(text, default):
    text = text.lower()
    if text[0] == "y": return True
    if text[0] == "n": return False
    if text == "true": return True
    if text == "false": return False
    if text == "1": return True
    if text == "0": return False
    return default

def generate_solution(colors):
    solution = ["", "", "", ""]
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
        processed_color = "  " + color[:index] + f"[{shorthand}]" + color[index+1:]
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
    use_inline_input = yesno(input("Do you want to use inline input? "), use_inline_input)


def config_board_width():
    print("'Board width' represents the number of colours that the combination has")
    print


def show_config_screen():
    def add_action(name, function = None):
        actions.append({"name": name, "function": function})

    def add_configured_action(name, key, default, title = None, description = None):
        configured_actions.append({
            "name": name,
            "key": key,
            "title": title or name,
            "description": description
        })

    actions = []
    configured_actions = []

    clear()
    print("CUSTOMISE YOUR GAME OF MASTERMIND:")
    add_action("Change maximum attempts", config_max_attempts)
    add_action("Change board width", config_board_width)
    add_action("Disable shorthands")
    add_action("Configure inline colour input", config_inline_inputs)

    add_configured_action("Change maximum attempts", "max_attempts", 10)

    print("  0. Finish customising and start the game")
    
    i = 0
    for action in actions:
        name = action["name"]
        print(f"  {i+1}. {name}...")
        i += 1

    i = 0
    for action in configured_actions:
        print(f"  {i+1}. {action['name']}")
        i += 1
    
    chosen_action = int(input("> ")) - 1
    if chosen_action == -1: return clear()
    if chosen_action > len(actions):
        print("Not a valid option! Enter a number from the list, or 0 to exit.")
        print()
        show_config_screen()

    clear()
    actions[chosen_action]["function"]()
    input("Done! Press enter to continue...")
    show_config_screen()

dev = True
max_attempts = 10
use_inline_input = False
colors = ["blue", "green", "black", "red", "yellow", "white"]
attempt = ["", "", "", ""]
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
    "w": "white"
}

show_config_screen()
solution = generate_solution(colors)
print_colors(colors, shorthands)
if dev: print("The solution is:", solution, "\n")

while attempt != solution:
    # Increment `attempts`
    attempts += 1

    # Check if the user has run out of turns
    if attempts > max_attempts:
        game_over = True
        break

    display_topbar(attempts, max_attempts)

    # Reset `position` to 0
    position = 0
    while position <= 3:
        tag = " " if last_response_was_valid else "!"

        # Display the prompt, to let the user input their colour
        attempt[position] = input(f"{tag}{position+1}> ").lower()

        # Expand any shorthands that were used
        if len(attempt[position]) == 1:
            if attempt[position] in shorthands:
                attempt[position] = shorthands[attempt[position]]

        # Mark the response as valid if the user inputted a valid colour
        # TODO: Don't let the user put the same colour in multiple positions?
        if colors.count(attempt[position]):
            # Let the user move on to the next position
            position += 1
            last_response_was_valid = True
        else:
            last_response_was_valid = False


    # Re-calculate statistics
    correct_colors = calculate_correct_colors(attempt, solution)
    correct_placements = calculate_correct_placements(attempt, solution)

    display_bottombar(correct_colors, correct_placements)
print()

if game_over:
    #print("=============| GAME OVER |=============")
    print("=============| YOU DIED! |=============")
    print("⚪ Correct colours:         ", correct_colors + correct_placements)
    print("⚫ Correctly-placed colours:", correct_placements)
    print()

    print("The solution was: ")
    i = 0
    for position in solution:
        checkmark = "❎"
        if position == attempt[i]: checkmark = "✅"
        print(f" {checkmark} {i+1}> {position}")
        i += 1
else:
    print("=========| CONGRATULATIONS! |=========")
    print("⚪ Correct colours:         ", correct_colors + correct_placements, "🎉")
    print("⚫ Correctly-placed colours:", correct_placements, "🎉")
    print()
    print(f"You found the solution in {attempts} attempts!")