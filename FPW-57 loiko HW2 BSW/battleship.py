import time

from random import randint, choice
from field_battleShip import BoardWrongShipException
from field_battleShip import Dot, Ship, Board, Player


class AI(Player):
    def ask(self):

        local_bound = []
        if self.last_shot:
            x, y = self.last_ask
            local_bound = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]
            local_bound = [bound for bound in local_bound if bound in self.enemy.available_turns]

        cell = choice(local_bound) if local_bound else choice(self.enemy.available_turns)
        self.last_ask = cell
        self.enemy.available_turns.remove(cell)
        d = Dot(*cell)
        print(f"Ход компьютера: {d.x + 1} {d.y + 1}")
        return d


class User(Player):
    def ask(self):
        while True:
            cords = input("Ваш ход: ").split()

            if len(cords) != 2:
                print(" Введите 2 координаты!")
                continue

            x, y = cords

            if not (x.isdigit()) or not (y.isdigit()):
                print(" Введите числа!")
                continue

            x, y = int(x), int(y)

            return Dot(x - 1, y - 1)


class Game:
    def __init__(self, size=6):
        self.size = size
        pl = self.random_board()
        co = self.random_board()
        co.hid = True

        self.ai = AI(co, pl)
        self.us = User(pl, co)

    def try_board(self):
        lens = [3, 2, 2, 1, 1, 1, 1]
        board = Board(size=self.size)
        attempts = 0
        for l in lens:
            while True:
                attempts += 1
                if attempts > 2000:
                    return None
                ship = Ship(Dot(randint(0, self.size), randint(0, self.size)), l, randint(0, 1))
                try:
                    board.add_ship(ship)
                    break
                except BoardWrongShipException:
                    pass
        board.begin()
        return board

    def random_board(self):
        board = None
        while board is None:
            board = self.try_board()
        return board

    def greet(self):
        print(" ~" * 11)
        print("   Добро пожаловать в игру   ")
        print("         МОРСКОЙ БОЙ !       ")
        print("~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~")
        print(" Потопи коробли противника - ")
        print("артифишл интэлиджента (AI),  ")
        print(" вводя координаты его коробля")
        print(" в формате 'x y', где:       ")
        print(" x - номер строки  ")
        print(" y - номер столбца ")
        self.myname = (input("Как тебя зовут? Представься:"))

    def loop(self):
        num = 0
        while True:
            time.sleep(1)
            print(" ~" * 11)
            print("Доска пользователя:")
            print(self.us.board)
            print(" ~" * 11)
            print("Доска компьютера:")
            print(self.ai.board)
            print(" ~" * 11)
            if num % 2 == 0:
                print(f"Ходит {self.myname}!")
                repeat = self.us.move()
            else:
                print("Ходит компьютер!")
                repeat = self.ai.move()
            if repeat:
                num -= 1

            if self.ai.board.defeat():
                print(" ~" * 11)
                print(f"{self.myname} выиграл!")
                print("Доска компьютера:")
                print(self.ai.board)
                break

            if self.us.board.defeat():
                print(" ~" * 11)
                print("Артифишл интэлиджент выиграл!")
                print("Доска пользователя:")
                print(self.us.board)
                break
            num += 1

    def start(self):
        self.greet()
        self.loop()


if __name__ == '__main__':
    war = Game()
    war.start()
