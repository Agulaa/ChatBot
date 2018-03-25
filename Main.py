from Rasa_nlu import Rasa_NLU
import warnings
from functools import wraps
import json

def ignore_warnings(f):
    """Function to ignore warnings in main method"""
    @wraps(f)
    def inner(*args, **kwargs):
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("ignore")
            response = f(*args, **kwargs)
        return response
    return inner


@ignore_warnings
def main():
    rasa_nlu = Rasa_NLU()
    rasa_nlu.training_nlu()
    while True:
        message = input('User:')
        print('User: {}'.format(message))
        respond = rasa_nlu.find_respond_from_bot(message)
        print('BOT: {}'.format(respond))
        if rasa_nlu.parse_message(message)['intent']['name'] == 'goodbye':
            return



if __name__ == '__main__':
    main()