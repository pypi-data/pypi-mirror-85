def main():
    from .Live import welcome, load_game
    
    user_name = input("Hi, What is your name? ")
    print(f"{welcome(user_name)}\n")
    load_game()