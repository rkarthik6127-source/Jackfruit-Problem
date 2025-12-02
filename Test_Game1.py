# Simple 2-choice Text Adventure Game

def ask_choice(prompt, option1, option2):
    """
    Shows a prompt with 2 choices.
    Returns 1 or 2 depending on the player's choice.
    """
    while True:
        print("\n" + prompt)
        print("1)", option1)
        print("2)", option2)
        choice = input("Enter 1 or 2: ").strip()
        if choice in ("1", "2"):
            return int(choice)
        else:
            print("Invalid input! Please type 1 or 2.")


def scene_intro():
    print("\n=== DARK FOREST ADVENTURE ===")
    print("You wake up in a dark forest. You don't remember how you got here.")
    print("In front of you is a narrow path. Behind you is a creepy cave.")

    choice = ask_choice(
        "What do you do?",
        "Follow the narrow path.",
        "Go into the creepy cave."
    )

    if choice == 1:
        return scene_path
    else:
        return scene_cave


def scene_path():
    print("\nYou follow the path and reach a broken wooden bridge over a deep river.")
    print("The bridge looks weak, but you can see a village on the other side.")
    print("You also see a small boat tied to a rock nearby.")

    choice = ask_choice(
        "What do you do?",
        "Cross the broken bridge.",
        "Use the small boat."
    )

    if choice == 1:
        return scene_bridge
    else:
        return scene_boat


def scene_cave():
    print("\nYou enter the cave. It is cold and dark.")
    print("You see a shiny chest and a tunnel going deeper.")

    choice = ask_choice(
        "What do you do?",
        "Open the shiny chest.",
        "Ignore the chest and go deeper into the tunnel."
    )

    if choice == 1:
        return scene_chest
    else:
        return scene_tunnel


def scene_bridge():
    print("\nYou carefully step onto the bridge...")
    print("Halfway through, the wood cracks!")

    choice = ask_choice(
        "Quick! What do you do?",
        "Run as fast as you can.",
        "Drop to the floor and crawl slowly."
    )

    if choice == 1:
        print("\nYou sprint and barely make it to the other side!")
        return scene_village
    else:
        print("\nThe bridge collapses while you are crawling...")
        print("You fall into the river and are swept away.")
        return scene_game_over


def scene_boat():
    print("\nYou untie the boat and start rowing.")
    print("The river current is strong, but you manage to control the boat.")

    choice = ask_choice(
        "In the middle of the river you see something in the water.",
        "Stop to check what it is.",
        "Ignore it and keep rowing to the village."
    )

    if choice == 1:
        print("\nIt was just a floating log. You lose some time, but you reach the village safely.")
        return scene_village
    else:
        print("\nYou ignore it and reach the village quickly.")
        return scene_village


def scene_chest():
    print("\nYou open the shiny chest...")
    print("It's a trap! Poisonous gas fills the room.")

    choice = ask_choice(
        "What do you do?",
        "Try to run out of the cave.",
        "Cover your mouth and search for an exit inside."
    )

    if choice == 1:
        print("\nYou don't make it out in time. The gas is too strong.")
        return scene_game_over
    else:
        print("\nYou find a small hole in the wall and crawl through it.")
        print("You escape the gas and end up outside near a riverside village.")
        return scene_village


def scene_tunnel():
    print("\nYou go deeper into the tunnel and find an underground river.")
    print("There is a small raft and a strange glowing door on the wall.")

    choice = ask_choice(
        "What do you do?",
        "Take the raft down the river.",
        "Open the glowing door."
    )

    if choice == 1:
        print("\nThe raft takes you to the outside world near a village.")
        return scene_village
    else:
        print("\nYou open the glowing door and step through...")
        print("You are teleported directly into the centre of the village!")
        return scene_village


def scene_village():
    print("\n=== THE VILLAGE ===")
    print("You arrive safely at the village.")
    print("People welcome you and offer you food and shelter.")

    choice = ask_choice(
        "Do you want to stay in the village, or continue exploring?",
        "Stay in the village (end the game).",
        "Ask about the forest and plan another adventure."
    )

    if choice == 1:
        print("\nYou live happily in the village. YOU WIN!")
        return scene_game_end
    else:
        print("\nYou rest for a while and then prepare for a new adventure.")
        print("To be continued...")
        return scene_game_end


def scene_game_over():
    print("\n=== GAME OVER ===")
    print("You did not survive this adventure.")

    choice = ask_choice(
        "Do you want to play again?",
        "Yes, restart from the beginning.",
        "No, quit."
    )

    if choice == 1:
        return scene_intro
    else:
        return None  # End the game


def scene_game_end():
    choice = ask_choice(
        "\nThanks for playing! Do you want to play again?",
        "Yes, restart from the beginning.",
        "No, quit."
    )

    if choice == 1:
        return scene_intro
    else:
        return None  # End the game


def main():
    current_scene = scene_intro

    while current_scene is not None:
        current_scene = current_scene()


if __name__ == "__main__":
    main()
