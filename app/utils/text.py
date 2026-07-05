import random
from app.data import letters, smile
from app.config import PUBLIC_IP


def replace(string) -> str:
    string = string.replace('переведи ', '')
    arr = []
    for name in string:
        if letters.get(name.upper()):
            arr.append(letters.get(name.upper()))
        else:
            arr.append(name)
    return ''.join(arr)


def im_here():
    return f"я тут {PUBLIC_IP}"


def lucky():
    # Генерируем рандомный смаил
    return f"{random.choice(smile)}{random.choice(smile)}{random.choice(smile)}"
