import random
import string

#генерим строку вида "0GTuLosLVuqy" (нижний, верхний регистры + цифры)
def generate_rnd_str_norm(length):
    letters_a = string.ascii_letters
    letters_b = string.digits
    random_string = ''.join(random.choice(letters_a+letters_b) for i in range(length))
    return random_string