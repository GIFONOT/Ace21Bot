import random
from random import randint


Card_deck = {1: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 2: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
             3: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 4: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]}
Masti = {1: 'bubi', 2: 'piki', 3: 'chervi', 4: 'krresi'}


ai = []
user = []
sumUser = 0
sumAi = 0

check = 1

while sumUser < 22:
    if sumUser == 21:
        print("Ты выиграл!!!")
    print(f"1: ещё 2: стоп \n")
    check = int(input())

    if check == 1:
        #карты игрока
        mast = randint(1, 4)
        rnd = random.choice(Card_deck[mast])
        Card_deck[mast].remove(rnd)

        sumUser += rnd
        user.append(f"{Masti[mast]} {rnd}")
        for i in user:
            print(i)
        print(f"Сумма: {sumUser}")
    else:
        if randint(0, 100) > 51:
            sumAi = sumUser + 1
        else:
            sumAi = randint(10, 21)

        print(f"Сумма твоя: {sumUser}")
        print(f"Сумма моя: {sumAi}")
        if sumUser > sumAi:
            print("Ты выиграл!!!")
        else:
            print("ты проебал)")
        break
else:
    print("ты проебал)")
