import string
import random

SECRET_KEY = ''.join([random.SystemRandom().choice("{}{}{}".format(
    string.ascii_letters, string.digits, string.punctuation)) for i in range(50)])

with open('./key.py', 'w', encoding='utf-8') as inputfile:
    inputfile.write('key="' + SECRET_KEY + '"')

