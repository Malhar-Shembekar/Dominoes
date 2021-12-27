import itertools
import random
from sys import exit as end
from random import randint
from varname import argname

full_set = itertools.combinations_with_replacement('0123456', 2)  # Creates a tuple with the pieces.
stock = [list([int(i), int(j)]) for i, j in full_set]
random.shuffle(stock)
player, computer, snake, status, gameplay = stock[:7], stock[7:14], [], "", 1
stock = stock[14:]


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
    if len(player) > 0:
        for i in player:
            print(f"{player.index(i) + 1}:{i}")
    print()
    if gameplay == 1:
        if status == 'player':
            print("Status: It's your turn to make a move. Enter your command.")
        elif status == 'computer':
            input("Status: Computer is about to make a move. Press Enter to continue...")


# Player's turn
def player_plays():
    def is_in(a, b):
        return not set(a).isdisjoint(b)
    global status, gameplay, snake
    snake_ends = [snake[0][0], snake[-1][-1]]
    while status == "player" and gameplay == 1:  # to exit the loop when status changes.
        if gameplay == 1:
            if len(player) > 0:
                try:
                    piece_num = int(input())
                except ValueError:
                    print("Invalid Input. Please try again.")
                    continue
                piece_check = (abs(piece_num) in range(1, len(player) + 1)) or (piece_num == 0)
                if piece_check:  # checks for valid input
                    piece = 0 if piece_num == 0 else player[abs(piece_num) - 1]
                    if piece != 0:
                        snake_check = is_in(piece, snake_ends)
                        if snake_check:  # checks for legal move
                            if piece_num > 0:  # adding piece to the right
                                if is_in([piece[0]], [snake_ends[-1]]):
                                    snake.append(piece)
                                    player.remove(piece)
                                elif is_in([piece[-1]], [snake_ends[-1]]):
                                    snake.append(piece[::-1])
                                    player.remove(piece)
                                else:
                                    print("Illegal move. Please try again.")
                                    continue
                            elif piece_num < 0:  # adding piece to the left
                                if is_in([piece[0]], [snake_ends[0]]):
                                    snake.insert(0, piece[::-1])
                                    player.remove(piece)
                                elif is_in([piece[-1]], [snake_ends[0]]):
                                    snake.insert(0, piece)
                                    player.remove(piece)
                                else:
                                    print("Illegal move. Please try again.")
                                    continue
                            status = 'computer'
                        else:
                            print("Illegal move. Please try again.")
                            continue
                    elif piece_num == 0:  # drawing from the stock
                        if len(stock) > 0:
                            add_piece = stock[-1]
                            player.append(add_piece)
                            stock.remove(add_piece)
                            status = 'computer'
                        elif len(stock) == 0:
                            gameplay = 0
                else:
                    print("Invalid input. Please try again.")
                    continue
            if len(player) == 0:
                gameplay = 0


# Computer's turn
def computer_plays():
    global status, snake, gameplay
    valid = {}  # empty dict
    snake_ends = [snake[0][0], snake[-1][-1]]
    case = 0
    for i in computer:
        if set(i).intersection(snake_ends):
            case += 1
            valid[case] = i
    if gameplay == 1:
        if len(computer) == 0:
            gameplay = 0
        elif len(computer) > 0:
            if len(valid) == 0:
                if len(stock) > 0:
                    computer.append(stock[-1])
                    stock.remove(stock[-1])
                    status = 'player'
                if len(stock) == 0:
                    gameplay = 0
            elif len(valid) > 0:
                choice = valid[randint(1, len(valid))]
                place = randint(0, 1)
                if len(set(choice)) == 1:  # choice == [a, a]
                    if len(set(snake_ends)) == 1:  # ends == [a, a]
                        if place == 1:
                            snake.append(choice)
                        elif place == 0:
                            snake.insert(0, choice)
                    elif len(set(snake_ends)) == 2:  # ends == [a, b] or [b, a]
                        if choice[0] == snake_ends[0]:
                            snake.insert(0, choice)
                        elif choice[0] == snake_ends[1]:
                            snake.append(choice)
                elif len(set(choice)) == 2:  # choice == [a, b]
                    if len(set(snake_ends)) == 1:  # ends == [a, a]
                        if choice[0] == snake_ends[0]:  # [a, b] and [a, a]
                            if place == 0:
                                snake.insert(0, choice[::-1])
                            elif place == 1:
                                snake.append(choice)
                        elif choice[1] == snake_ends[0]:  # [b, a] and [a, a]
                            if place == 0:
                                snake.insert(0, choice)
                            elif place == 1:
                                snake.append(choice[::-1])
                    elif len(set(snake_ends)) == 2:  # ends == [a, c] or [c, a] or effectively [a, b]
                        common = set(choice).intersection(snake_ends)
                        if len(common) == 2:
                            if set(choice) == set(snake_ends):  # ends == effectively [a, b]
                                if choice[0] == snake_ends[0]:  # [a, b] and [a, b]
                                    if place == 0:
                                        snake.insert(0, choice[::-1])
                                    elif place == 1:
                                        snake.append(choice[::-1])
                                elif choice[0] == snake_ends[1]:  # [a, b] and [b, a]
                                    if place == 0:
                                        snake.insert(0, choice)
                                    elif place == 1:
                                        snake.append(choice)
                        elif len(common) == 1:  # ends == [a, c] or [c, a]
                            get = choice.index(*common)
                            if choice[get] == snake_ends[0]:  # choice and [a, c]
                                if get == 0:  # choice == [a, b]
                                    snake.insert(0, choice[::-1])
                                elif get == 1:  # choice == [b, a]
                                    snake.insert(0, choice)
                            if choice[get] == snake_ends[1]:  # choice and [c, a]
                                if get == 0:  # choice == [a, b]
                                    snake.append(choice)
                                elif get == 1:  # choice == [b, a]
                                    snake.append(choice[::-1])
                computer.remove(choice)
            status = 'player'


def comp_ai(valid, computer, snake):
    itertools.chain.from_iterable(snake + computer)

# If the snake has fulfilled draw conditions
def snake_blocked():
    global snake, gameplay
    elements = list(itertools.chain.from_iterable(snake))
    if elements[0] == elements[-1]:
        if elements.count(elements[0]) == 8:
            gameplay = 0
            return True
        else:
            return False
    else:
        return False


snake.append(comparator(computer, player))
display()

while gameplay == 1:
    if status == 'player':
        player_plays()
        display()
    elif status == 'computer':
        computer_plays()
        display()

if gameplay == 0:
    if len(computer) == 0:
        print("the game is over. the computer won")
        end()
    if len(player) == 0:
        print("the game is over. you won")
        end()
    if snake_blocked() or len(stock) == 0:
        print("the game is over. it's a draw")
        end()
