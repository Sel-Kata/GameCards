import random
import math


class card:
    def __init__(self, power, suit, value):
        self.power = power
        self.suit = suit
        self.value = value


class pocker_hand:
    def __init__(self, cards):
        self.cards = cards

    def flush(self):
        suit = self.cards[0].suit
        for card in self.cards:
            if card.suit != suit:
                return False
        return True

    def straight(self):
        sorted_cards = sorted(self.cards, key=lambda c: c.power)
        powers = [card.power for card in sorted_cards]
        if powers == [2, 3, 4, 5, 14]:
            return True
        for i in range(4):
            if powers[i + 1] != powers[i] + 1:
                return False
        return True

    def royal_flush(self):
        powers = sorted(card.power for card in self.cards)
        return self.flush() and powers == [10, 11, 12, 13, 14]

    def four_of_a_kind(self):
        powers = [card.power for card in self.cards]
        for i in range(3):
            if powers[i + 1] != powers[i]:
                return False
        return True

    def three_of_a_kind(self):
        powers = [card.power for card in self.cards]
        for i in range(2):
            if powers[i + 1] != powers[i]:
                return False
        return True

    def pair(self):
        powers = [card.power for card in self.cards]
        if powers[0] != powers[1]:
            return False
        return True

    def two_pairs(self):
        powers = sorted([card.power for card in self.cards])
        if powers[0] == powers[1] and powers[2] == powers[3] and powers[0] != powers[2]:
            return True
        return False

    def full_house(self):
        powers = sorted([card.power for card in self.cards])
        if powers[0] == powers[1] == powers[2] and powers[3] == powers[4] and powers[0] != powers[4]:
            return True
        elif powers[0] == powers[1] and powers[2] == powers[3] == powers[4] and powers[0] != powers[4]:
            return True
        return False

    def comb_check(self, combinations):
        count = 0
        strength=0 #how strong is this hand
#  One Pair = 1
#  Two Pair = 2  
#  Three of a Kind = 3 
#  Straight = 4  
#  Flush = 5 
#  Full House = 6 
#  Four of a Kind = 7 
#  Straight Flush = 8 
#  Royal Flush = 9 
        
        for comb in combinations[0]:  # Только комбинации по 5 карт
            desc = ", ".join(f"{card.value} / {card.suit}" for card in comb)
            if pocker_hand(comb).straight() and pocker_hand(comb).flush():
                count+=1
                strength+=8
                print(desc, "is straight flush")
            elif pocker_hand(comb).flush():
                count+=1
                strength+=5
                print(desc, "is flush")
            elif pocker_hand(comb).straight():
                count+=1
                strength+=4
                print(desc, "is straight")
            elif pocker_hand(comb).royal_flush():
                count+=1
                strength+=9
                print(desc, "is royal flush")
            elif pocker_hand(comb).full_house():
                count+=1
                strength+=6
                print(desc, "is full house")
        for comb in combinations[1]:  # Для 4 карт
            desc = ", ".join(f"{card.value} / {card.suit}" for card in comb)
            if pocker_hand(comb).four_of_a_kind():
                count+=1
                strength+=7
                print(desc, "is four of a kind")
            if pocker_hand(comb).two_pairs():
                count+=1
                strength+=2
                print(desc, "is two pairs")
        for comb in combinations[2]:  # Для 3 карт
            desc = ", ".join(f"{card.value} / {card.suit}" for card in comb)
            if pocker_hand(comb).three_of_a_kind():
                count+=1
                strength+=3
                print(desc, "is three of a kind")
        for comb in combinations[3]:  # Для 2 карт
            desc = ", ".join(f"{card.value} / {card.suit}" for card in comb)
            if pocker_hand(comb).pair():
                count+=1
                strength+=1
                print(desc, "is pair")
        if count==0:
            print("You don't have any combinations")
        else:    
            print("Total combinations found: ", count)
        return strength


def create_deck(deck):
    for j in range(2, 15):
        deck.append(card(j, "♣", j))
    for j in range(2, 15):
        deck.append(card(j, "♦", j))
    for j in range(2, 15):
        deck.append(card(j, "♥", j))
    for j in range(2, 15):
        deck.append(card(j, "♠", j))
    for i in deck:
        if i.power == 14:
            i.value = "A"
        if i.power == 11:
            i.value = "J"
        elif i.power == 12:
            i.value = "Q"
        elif i.power == 13:
            i.value = "K"

    return deck


def print_summary(card):
    print(card.value, '/', card.suit)


def card_pick(deck, hand):
    try:
        amount = int(input("Please type the amount of cards (from 3 to 15) you would like to take (only arabic numbers):"))
        if amount <= 15 and amount >= 3:
            for i in range(amount):
                c = random.randint(0, len(deck) - 1)
                hand.append(deck[c])
                deck.pop(c)
            sorting_method = input("Sorting method? \n 1 = Heap sort \n 2 = Binary Insertion Sort \n 3 = Merge Sort \n 4 = Tim Sort \n")
            hand = sort(int(sorting_method), hand)
            for i in hand:
                print_summary(i)
        else:
            print("Read previous sentence again.")
            card_pick(deck, hand)
        return int(sorting_method)

    except ValueError:
        card_pick(deck,hand)


#sort
def get_valid_number(prompt="Enter a number from 1 to 4: "):
    while True:
        user_input = input(prompt)
        if user_input.isdigit():
            number = int(user_input)
            if 1 <= number <= 4:
                return number  # Возвращаем правильное число
            else:
                print(f"Number should be from 1 to 4")
        else:
            print("Please enter an integer")

def sort(answer, hand):
    if answer == 1:
        return heap_sort(hand)
    elif answer == 2:
        return binary_insertion_sort(hand)
    elif answer == 3:
        return merge_sort(hand)
    elif answer == 4:
        return tim_sort(hand)
    else:
        print("Unknown sorting method.")
        valid_number = get_valid_number()
        return sort(valid_number, hand)


#heap sort
def heapify(arr, n, i):
    largest = i
    l = 2 * i + 1
    r = 2 * i + 2

    if l < n and arr[l].power > arr[largest].power:
        largest = l
    if r < n and arr[r].power > arr[largest].power:
        largest = r
    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]
        heapify(arr, n, largest)


def heap_sort(arr):
    arr = arr.copy()
    n = len(arr)

    for i in range(n // 2 - 1, -1, -1):
        heapify(arr, n, i)

    for i in range(n - 1, 0, -1):
        arr[i], arr[0] = arr[0], arr[i]
        heapify(arr, i, 0)

    return arr


#binary insertion sort
def binary_search(arr, val, start, end):
    while start < end:
        mid = (start + end) // 2
        if arr[mid].power < val.power:
            start = mid + 1
        else:
            end = mid
    return start


def binary_insertion_sort(arr):
    res = arr.copy()
    for i in range(1, len(res)):
        val = res[i]
        j = binary_search(res, val, 0, i)
        res = res[:j] + [val] + res[j:i] + res[i + 1:]
    return res


#merge sort
def merge_sort(arr):
    if len(arr) <= 1:
        return arr

    mid = len(arr) // 2
    L = merge_sort(arr[:mid])
    R = merge_sort(arr[mid:])

    result = []
    i = j = 0
    while i < len(L) and j < len(R):
        if L[i].power < R[j].power:
            result.append(L[i])
            i += 1
        else:
            result.append(R[j])
            j += 1

    result.extend(L[i:])
    result.extend(R[j:])
    return result


#tim sort
def insertion_sort(arr, left, right):
    for i in range(left + 1, right + 1):
        key = arr[i]
        j = i - 1
        while j >= left and arr[j].power > key.power:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key


def merge(arr, l, m, r):
    left = arr[l:m + 1]
    right = arr[m + 1:r + 1]
    i = j = 0
    k = l

    while i < len(left) and j < len(right):
        if left[i].power <= right[j].power:
            arr[k] = left[i]
            i += 1
        else:
            arr[k] = right[j]
            j += 1
        k += 1

    while i < len(left):
        arr[k] = left[i]
        i += 1
        k += 1
    while j < len(right):
        arr[k] = right[j]
        j += 1
        k += 1


def tim_sort(arr):
    res = arr.copy()
    n = len(res)
    RUN = 32

    for i in range(0, n, RUN):
        insertion_sort(res, i, min(i + RUN - 1, n - 1))

    size = RUN
    while size < n:
        for left in range(0, n, 2 * size):
            mid = min(left + size - 1, n - 1)
            right = min(left + 2 * size - 1, n - 1)
            if mid < right:
                merge(res, left, mid, right)
        size *= 2

    return res


def card_combinations(hand):
    all_combinations = []
    if len(hand) >= 5:
        combinations = []
        for i in range(len(hand)):
            for j in range(i + 1, len(hand)):
                for k in range(j + 1, len(hand)):
                    for l in range(k + 1, len(hand)):
                        for m in range(l + 1, len(hand)):
                            combinations.append([hand[i], hand[j], hand[k], hand[l], hand[m]])
        all_combinations.append(combinations)
    else:
        all_combinations.append([])

    if len(hand) >= 4:
        combinations = []
        for i in range(len(hand)):
            for j in range(i + 1, len(hand)):
                for k in range(j + 1, len(hand)):
                    for l in range(k + 1, len(hand)):
                        combinations.append([hand[i], hand[j], hand[k], hand[l]])
        all_combinations.append(combinations)
    else:
        all_combinations.append([])

    if len(hand) >= 3:
        combinations = []
        for i in range(len(hand)):
            for j in range(i + 1, len(hand)):
                for k in range(j + 1, len(hand)):
                    combinations.append([hand[i], hand[j], hand[k]])
        all_combinations.append(combinations)
    else:
        all_combinations.append([])

    if len(hand) >= 2:
        combinations = []
        for i in range(len(hand)):
            for j in range(i + 1, len(hand)):
                combinations.append([hand[i], hand[j]])
        all_combinations.append(combinations)
    else:
        all_combinations.append([])

    return all_combinations

def complexity_program(hand, sort_alg):
# card_combinations(hand) + comb_check(combinations) + card_pick(deck, hand)
# O(n^5) + O(n^5) + depends
    n = len(hand)
    if sort_alg == 2:
        complexity_of_program = n**5 + n**5 + n**2
    else:
        complexity_of_program = n**5 + n**5 + n*math.log(n, 2)
    print("Complexity of this program: O(n^5), but if you want to know the exact complexity:  ", complexity_of_program)

def competition(strength1):
    hand2 = []
    sorting_method = card_pick(deck, hand2)
    combinations = card_combinations(hand2)
    ph2 = pocker_hand([])
    strength2 = ph2.comb_check(combinations)
    if strength1 > strength2:
        print("-----------------------------")
        print(" 💫 hand 1 is stronger and has more or stronger combinations 💫 ")
        print("-----------------------------")
    elif strength2 > strength1:
        print("-----------------------------")
        print(" 💫 hand 2 is stronger and has more or stronger combinations 💫 ")
        print("-----------------------------")
    else:
        print("-----------------------------")
        print(" 💫 both hands are absolutely identical 💫")
        print("-----------------------------")

while True:
    deck = []
    hand = []
    create_deck(deck)
    sorting_method = card_pick(deck, hand)
    combinations = card_combinations(hand)
    ph = pocker_hand([])
    strength1 = ph.comb_check(combinations)
    
    complexity_program(hand, sorting_method)
    
    compet = input("Do you want to play little bit another game? (yes/no): ").lower()
    if compet == 'yes':
        competition(strength1)
    
    
    play_again = input("Do you want to play again? (yes/no): ").lower()
        
    if play_again != 'yes':
        print("-----------------------------")
        print("💥 Thanks for playing! 💥 ")
        
        break 
    else:
        print("-----------------------------")
        print("New round begins...")
        print("-----------------------------")
