import redis
import random
import sys

# Redis setup
r = redis.Redis(host='localhost', port=6379, db=0)
LEADERBOARD_KEY = "guess_game_leaderboard"

# ---------------- Redis Leaderboard Functions ----------------
def add_or_update_player_score(player_id, score):
    r.zadd(LEADERBOARD_KEY, {player_id: score})
    print(f"✅ {player_id}'s score is recorded as {score}")

def get_top_n_players(n=10):
    top_players = r.zrevrange(LEADERBOARD_KEY, 0, n - 1, withscores=True)
    print(f"\n🏆 Top {n} Players:")
    for rank, (player, score) in enumerate(top_players, start=1):
        print(f"{rank}. {player.decode()} - Score: {int(score)}")

def get_player_rank(player_id):
    rank = r.zrevrank(LEADERBOARD_KEY, player_id)
    if rank is not None:
        return rank + 1
    return None

# ---------------- Game Functions ----------------
def welcome_message():
    print("🎮 Welcome to Number Guessing Game!\n")

def generate_random_number(user_difficulty_level):
    if user_difficulty_level == 1:
        return random.randint(1, 50), 5
    elif user_difficulty_level == 2:
        return random.randint(1, 100), 7
    elif user_difficulty_level == 3:
        return random.randint(1, 1000), 10

def get_user_input():
    return int(input("🔢 Enter your guess: "))

def check_equality(user_input, random_number):
    if user_input > random_number:
        print("📉 Your Guess is Higher")
    elif user_input < random_number:
        print("📈 Your Guess is Lower")
    else:
        print("🎉 You have Won!")
        return True
    return False

def get_difficulty_levels():
    print("Select Difficulty Level:")
    print("1: Easy (1-50)")
    print("2: Medium (1-100)")
    print("3: Hard (1-1000)")
    return int(input("Enter your choice: "))

def wanna_retry():
    user_wish = input("🔁 Do you want to play again? (yes/no): ").strip().lower()
    if user_wish == "yes":
        main()
    else:
        print("👋 Thanks for playing! See you soon.")

def play(random_number, max_tries):
    attempts = 0
    while attempts < max_tries:
        attempts += 1
        try:
            user_input = get_user_input()
        except ValueError:
            print("⚠️ Invalid input, please enter a number.")
            continue

        if check_equality(user_input, random_number):
            save_leaderboard(attempts)
            break
    else:
        print("💥 You've exceeded the max attempts. Game Over!")

def save_leaderboard(attempts):
    name = input("📝 Enter your name for the leaderboard: ").strip()
    score = max(0, 1000 - (attempts - 1) * 100)  # Minimum score 0
    add_or_update_player_score(name, score)
    rank = get_player_rank(name)
    if rank:
        print(f"🏅 You are currently ranked #{rank} on the leaderboard!")

# ---------------- Main Entry ----------------
def main():
    welcome_message()
    level = get_difficulty_levels()
    number, tries = generate_random_number(level)
    # Uncomment for testing:
    # print(f"Debug: Random number is {number}")
    play(number, tries)
    wanna_retry()

# ---------------- Leaderboard CLI ----------------
if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "list":
        get_top_n_players(10)
    else:
        main()
