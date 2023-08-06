"""Core functions for thedatamine package.

This module contains a set of functions that are currently used as complimentary material for Purdue University's integrative data science initiative, The Data Mine. 
"""

def hello_datamine(name: str = 'student') -> str:
    """Prints and returns a hello message to a Data Mine student.

    Args:
        str (name, optional): The name of a student. Defaults to 'student'.

    Returns:
        str: A potentially customized hello message.
    """
    msg = f'Hello {name}! Welcome to The Data Mine!'
    print(msg)

    return msg