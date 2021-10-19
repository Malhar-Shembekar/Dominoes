import itertools
import random
import sys

from varname import argname

full_set = itertools.combinations_with_replacement('0123456', 2)  # Creates a tuple with the pieces.
stock = [list(ele) for ele in full_set]  # Tuple in tuple to list in list transform.
for j in stock:
    j[0] = int(j[0])
    j[1] = int(j[1])
player = []
computer = []
snake = []
status = 0


# Distributes pieces before the game starts.
def pieces(a):
    while len(a) < 7:
        add = stock[random.randint(0, int(len(stock) - 1))]
        if add not in a:
            a.append(add)

    for i in a:
        if i in stock:
            stock.remove(i)


# Finds the first piece on the snake and assigns status.
def comparator(a, b):
    global status
    if max(a) > max(b):
        status = argname('b')
        return a.pop(a.index(max(a)))
    elif max(b) > max(a):
        status = argname('a')
        return b.pop(b.index(max(b)))


# The display menu.
def display():
    print(70 * '=')
    print(f"Stock size: {len(stock)}")
    print(f"Computer pieces: {len(computer)}")
    print()
    if len(snake) > 6:
        print(f"{snake[0]}{snake[1]}{snake[2]}...{snake[-3]}{snake[-2]}{snake[-1]}")
    elif len(snake) <= 6:
        def snake_printer():
            x = f"{snake}".removeprefix("[")
            x = x.removesuffix("]")
            x = x.replace("], [", "][")
            print(x)

        snake_printer()
    print()
    for i in player:
        print(f"{player.index(i) + 1}:{i}")
    print()
    if (status == 'player') and (len(player) != 0):
        print("Status: It's your turn to make a move. Enter your command.")
    elif (status == 'computer') and (len(computer) != 0):
        input("Status: Computer is about to make a move. Press Enter to continue...")


# Player's turn
def player_plays():
    global status
    case = 1
    while True:
        try:
            piece_num = int(input())
            piece = player[abs(piece_num) - 1]
            snake_ends = [snake[0][0], snake[-1][-1]]
            if piece_num not in range(-len(player) - 1, len(player) + 1):
                raise ValueError
            if set(piece).isdisjoint(snake_ends):
                raise FileNotFoundError
        except ValueError:
            print("Invalid input. Please try again.")
            case = 0
        except FileNotFoundError:
            print("Illegal move. Please try again.")
            case = 0
        else:
            if piece_num < 0:
                snake.insert(0, piece)
            elif piece_num > 0:
                snake.append(piece)
            elif piece_num == 0:
                if len(stock) != 0:
                    player.append(stock[random.randint(0, len(stock) - 1)])
                    stock.remove(player[-1])
            if piece_num != 0:
                if case == 1:
                    player.remove(piece)
            status = 'computer'
            break


# Computer's turn
def computer_plays():
    global status
    i = random.randint(0, len(computer) - 1)
    choice = random.randint(0, 1)
    if choice == 1:
        snake.append(computer[i])
    elif choice == 0:
        snake.insert(0, computer[i])
    computer.remove(computer[i])
    status = 'player'


def snake_blocked():
    global snake
    elements = list(itertools.chain.from_iterable(snake))
    if elements[0] == elements[-1]:
        if elements.count(elements[0]) == 8:
            return 0
        else:
            return 1
    else:
        return 1


pieces(computer)
pieces(player)
snake.append(comparator(computer, player))
display()

while True:
    if snake_blocked() == 1:
        if (len(player) != 0) and (len(computer) != 0):
            if status == 'player':
                player_plays()
                display()
            elif status == 'computer':
                computer_plays()
                display()
        elif len(player) == 0:
            print("Status: The game is over. You won!")
            sys.exit()
        elif len(computer) == 0:
            print("Status: The game is over. The computer won!")
            sys.exit()
    else:
        print("Status: The game is over. It's a draw!")
        sys.exit()

