import random
import string

def generate_random_login(length=8):
    letters = string.ascii_lowercase
    login = ''.join(random.choice(letters) for i in range(length))
    return login
