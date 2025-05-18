import random
import sys


def get_machine_guess_number(start_num, end_num):
    return random.randint(start_num, end_num)
    
def get_level_conditions(difficult_level):
  if difficult_level == 1:
    start_num = 1
    end_num = 100
    no_of_chance = 5
  elif difficult_level == 2:
    start_num = 1 
    end_num = 500
    no_of_chance = 7
  elif difficult_level == 3:
    start_num =1 
    end_num = 1000
    no_of_chance = 10
  else:
     pass
  return start_num, end_num, no_of_chance

def get_user_guess_number(difficult_level):
  try:
    print("Difficult_level", difficult_level)
    start_num, end_num, _ = get_level_conditions(difficult_level)
    usr_guess_num = int(input(f"What is your guess ({start_num} - {end_num}) : "))

    if start_num <= usr_guess_num <= end_num:
      print(usr_guess_num)
      return usr_guess_num
    else:
      print("Enter within range")
      usr_guess_num = get_user_guess_number(difficult_level)
      return usr_guess_num
  except ValueError as ve:
    print('Please Enter Valid Number.', ve)
    return get_user_guess_number(difficult_level)
      

def get_difficulty_level_from_user(repeat_count=1):
    print("""
Select Dificulty user_difficult_level
1. Easy (Guess number 1 to 100, Max 05 chances)
2. Normal (Guess number 1 to 500, Max 07 chances)
3. Hard (Guess number 1 to 1000, Max 10 chances)
9. Exit Game
  """)

    get_difficulty_level = input("Enter your choice: ")

    if get_difficulty_level in ["1", "2", "3"]:
        return int(get_difficulty_level)
    elif get_difficulty_level == "9" or repeat_count >= 3:
        print("Thank you. Comeagain!")
        sys.exit(0)
    else:
        print("Please check your input and try again")
        repeat_count += 1
        get_difficulty_level_from_user(repeat_count)


def game_score(attempt, difficult_level):
    if difficult_level == 1:
       max_score = 100
       max_tries = 5
    elif difficult_level == 2:
       max_score = 200
       max_tries = 7
    elif difficult_level == 3:
       max_score = 300
       max_tries = 10

    score = max_score/max_tries* (max_tries + 1 - attempt)
    print (f"| Your Score {score:0.2f}  |")
    print('\n =================== \n')


def game_logic(m_guess, u_guess):
  print(m_guess, u_guess)

  def game_hint(high, low):
     hint_value = ((high - low ) / high) * 100
     return "You're getting closer!" if hint_value < 50 else "Still far from the correct guess."
   
  if m_guess == u_guess:
    return True, "🏆"
  
  elif m_guess > u_guess:
     return False, f"{game_hint(m_guess, u_guess)}, It's higher than you think."
  
  else:
     return False, f"{game_hint(u_guess, m_guess)}, It's lower than you think."


def game_over():
    print('\n----------------')
    print("  Game Over!!!  ")
    print('----------------\n')
    get_play_again()


def get_play_again():
    play_again = input("Do you wamt play again. (yes/no) : ").lower().strip()
    if play_again in ['yes', 'y'] :
        main()
    else:
        print("Thank you, Come Again")
        sys.exit(0)


def get_user_guess_number_game(difficult_level):
  start_num, end_num, chances = get_level_conditions(difficult_level)
  m_guess = get_machine_guess_number (start_num, end_num)
  attempt = 0
  while True:
    attempt += 1
    u_guess = get_user_guess_number(difficult_level)
    g_logic = game_logic(m_guess, u_guess)

    if g_logic[0] == True:
      print('\n =================== \n')
      print(f"| You are Win!!! {g_logic[1]} |")
      game_score(attempt, difficult_level)
      get_play_again()


    if chances == attempt:
      game_over()
      return False
    
def main():
    d_level = get_difficulty_level_from_user()
    get_user_guess_number_game(d_level)


main() 