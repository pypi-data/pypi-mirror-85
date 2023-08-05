def _needs_number(user_input):
    """
    An inturnal use func, it forces the user to enter a number.
    :param user_input: The user input, which will be checked if it is a number.
    :return: returns an integer number.
    """
    while not user_input.isdigit():
        user_input = input("You need to enter a number ")
    return int(user_input)
