import random

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

def print_colors(colors, shorthands):
    print("Available colours:")
    for color in colors:        
        if color == "black":
            print(f"  blac[k]")
        else:
            print(f"  [{color[0]}]{color[1:]}")
    print()

dev = True
MAX_ATTEMPTS = 10
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

solution = generate_solution(colors)
print_colors(colors, shorthands)
if dev: print("The solution is:", solution, "\n")

while attempt != solution:
    # Increment `attempts`
    attempts += 1

    # Check if the user has run out of turns
    if attempts > MAX_ATTEMPTS:
        game_over = True
        break

    # Display the statusbar
    print(f"===| {attempts}/{MAX_ATTEMPTS} |===========| ⚪ {correct_colors}   ⚫ {correct_placements} |===")

    # Reset `position` to 0
    position = 0
    while position <= 3:
        if last_response_was_valid:
            tag = " "
        else:
            # This will show an exclamation mark before the prompt,
            # to tell them that their last input was invalid
            tag = "!"

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


    ## UPDATE STATISTICS ##

    # Reset everything to 0
    correct_colors = 0
    correct_placements = 0

    # Update `correct_colors`
    for correct_color in solution:
        # if `attempt` contains the color that we're checking for,
        # increment `correct_colors`
        if attempt.count(correct_color):
            correct_colors += 1

    # Update `correct_placements`
    i = 0
    for attempted_color in attempt:
        if solution[i] == attempted_color:
            # Increment `correct_placements`, and
            # decrement `correct_colors` so that
            # the 'pin' isn't counted twice
            correct_placements += 1
            correct_colors -= 1
        i += 1

    print()
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