import random
import sys
import redis
from leaderboard import Leaderboard

r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
lb = Leaderboard(r)

def welcome_message():
    print("Welcome to Number Guessing Game")

def generate_random_number(user_difficulty_level):
    if user_difficulty_level == 1:
        number, max_tries = random.randint(1, 50), 5
    elif user_difficulty_level == 2:
        number, max_tries = random.randint(1, 100), 7
    elif user_difficulty_level == 3:
        number, max_tries = random.randint(1, 1000), 10
    return number, max_tries

def get_user_input():
    return int(input("Enter your guess : "))

def check_equality(user_input, random_number):
    if user_input > random_number:
        print("Your Guess is Higher")
    elif user_input < random_number:
        print("Your Guess is Lower")
    else:
        print("You have Won !!!")
        return True
    return False

def get_difficulty_levels():
    print("Difficulty Levels : \n1: Easy 1-50\n2: Medium 1-100\n3: Hard 1-1000")
    return int(input("Enter your difficulty level : "))

def wanna_retry():
    if input("Do you want to re-play the game? (yes/no): ").lower() == "yes":
        main()
    else:
        print("Thanks for Playing the Game! See you again.")

def play(random_number, max_tries):
    attempts = 0
    while True:
        if attempts >= max_tries:
            print("You have exceeded MAX Attempts! Try Again.")
            break
        attempts += 1
        user_input = get_user_input()
        if check_equality(user_input, random_number):
            save_leaderboard(attempts)
            break

def save_leaderboard(attempts):
    name = input("Please enter your name for the Leaderboard: ")
    score = 1000 - ((attempts - 1) * 100)
    lb.add_score(name, score)
    print(f"✅ Score {score} added to the leaderboard for {name}!")

def list_leaderboard():
    print("\n🏆 Leaderboard (Top 10):")
    for rank, (user, score) in enumerate(lb.get_top_n(10), start=1):
        print(f"{rank}. {user} - {int(score)}")

def main():
    welcome_message()
    level = get_difficulty_levels()
    number, max_tries = generate_random_number(level)
    print(f"[DEBUG] Random Number is: {number}")  # Optional: remove in prod
    play(number, max_tries)
    wanna_retry()

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "list":
        list_leaderboard()
    else:
        main()
