import random

def guess_the_number():
    # Step 1: Generate a random number between 1 and 100
    target_number = random.randint(1, 100)

    print("Welcome to Guess the Number game!")
    print("I'm thinking of a number between 1 and 100.")
    
    # Step 2: Initialize variables
    attempts = 0
    guessed_correctly = False

    # Step 3: Start the game loop
    while not guessed_correctly:
        try:
            # Step 4: Prompt user for their guess
            user_guess = int(input("Please enter your guess: "))
            attempts += 1

            # Step 5: Check if the guess is correct, too high, or too low
            if user_guess == target_number:
                print(f"Congratulations! You guessed the correct number {target_number} in {attempts} attempts.")
                guessed_correctly = True  # Exit the loop if the guess is correct
                break
            elif user_guess < target_number:
                print("Too low! Try again.")
            else:
                print("Too high! Try again.")

            # Step 6: Optionally skip certain parts using continue or break
            # Example: If the guess is outside the range 1-100, prompt again without increasing attempts
            if user_guess < 1 or user_guess > 100:
                print("Your guess is out of range! Please guess a number between 1 and 100.")
                continue  # Skip the rest of the loop and prompt again

        except ValueError:
            # Handle invalid input (non-integer inputs)
            print("Invalid input! Please enter a number between 1 and 100.")
            continue  # Skip the rest of the loop and ask the user again

# Run the game
guess_the_number()