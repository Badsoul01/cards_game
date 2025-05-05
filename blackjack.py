import random
# funkce na zjištění hodnot karet v ruce
def value_of_card_on_hand(hand,value):
    list_hand = hand.split()
    for i in range(len(list_hand)):
        if len(list_hand)>2:
            i+=1
            i*=-1
        if len(value) != len(list_hand):
            if list_hand[i][1] in "KJQA":
                if list_hand[i][1]== "A":
                    value.append(value_of_player_aces(hand))
                else:
                    value.append(10)
            elif list_hand[i][1].isdigit():
                if int(list_hand[i][1]) ==1:
                    value.append(10)
                else:
                    value.append(int(list_hand[i][1]))
    return value
# funkce na zjištění hodnot Esa u hráče
def value_of_player_aces(hand):
    print(f"Karty na tvé ruce {' '.join(hand)}")
    while True:
        aces = int(input("Máš v ruce Eso? Chceš za něho 11 bodů nebo 1 bod? "))
        if aces == 11:
            value_of_ace = 11
            break
        elif aces ==1:
            value_of_ace = 1
            break
        else:
            print("Musíš zadat 1 nebo 11!")

    return value_of_ace
# vytvoření balíku karet
def pack_of_cards():
    pack  = []
    numbers = [2,3,4,5,6,7,8,9,10,"J","Q","K","A"]
    signs = ["♠","♥","♦","♣"]
    for sign in signs:
        for number in numbers:
            pack.append(sign+str(number))
    random.shuffle(deck)
    return pack
#rozdávání karet
def deal_cards(hand,pack):
    new_hand = hand.split()
    if not pack:
         pack = pack_of_cards()

    if not new_hand:
        for _ in range(2):
            new_hand.append(pack[0])
            pack.pop(0)
    else:
        new_hand.append(pack[0])
        pack.pop(0)

    return " ".join(new_hand),pack
# hlavní nabídka
def main_menu(hand,pack,value,ts):
    print("Vítej v této karetní hře!")
    print("""Co bys rád udělal?
    1) Začal novou hru
    2) Přečetl si pravidla
    3) Ukončil hru
    """)
    while True:
        choice = input("Tvé rozhodnutí: ")
        if choice == "1":
            game_round(hand,pack,value,ts)
            break

        elif choice == "2":
            print("""Cíl hry je mít součet karet na ruce co nejblíže 21.\nPokud budeš mít na ruce Eso, můžeš zvolit jeho hodnotu jako 1 nebo 11.
            K, Q a J je za 10bodů, zbytek podle hodnoty dané karty.\nPokud překročíš 21 prohráváš a to co vsadíš se odečítá od tvé celkové výhry.\nPokud trefíš stejný bodový součet jako protivník dostaneš polovinu. A pokud vyhraješ tak dostáváš částku kterou vsadíš.\nJeště máš možnost zdvojnásobit částku.
                    """)

        elif choice == "3":
            break
        else:
            print("Prosím vyber z menu!")

    return choice
#možnosti mezi tahy
def cards_menu(hand,pack,tip, value):
    print(f"""Tvé karty na ruce: {hand}\n\nCo bys chtěl udělat?
    1. Dej mi další kartu.
    2. Zdvojnásobím sázku.
    3. Ukončit tah.
    """)
    while True:
        choice = input("Vyber si: ")
        if choice == "1":
            hand,pack  = deal_cards(hand, pack)
            value = value_of_card_on_hand(hand, value)
            print(f"Zde je tvá nová karta {hand[len(hand)-3::]}.\nKarty na ruce: {hand}")
            if sum(value) >21:
                return tip, hand, value
        elif choice == "2":
            tip*=2
            hand,pack = deal_cards(hand, pack)
            print(f"Tvoje sázka jsou nyní {tip} a tvá nová karta je {hand[len(hand)-3::]}.\nKarty na ruce: {hand}")
            value = value_of_card_on_hand(hand, value)
            return tip , hand,value
        elif choice == "3":
            return tip, hand,value
        else:
            print("Vyber z menu!")
# možnost sázek
def betting(ts):
    while True:
        amount_of_bet = input(f"Kolik zlaťáků by jsi chtěl vsadit? 1-{ts}: ")
        if amount_of_bet.isdigit() and 0 < int(amount_of_bet) <= ts:
            return int(amount_of_bet)

        else:
            print("Zadej číslo v určeném rozsahu!")
# kontrola výhry/prohry/remízy
def checking_winning_condition(hand, player_value,tip,ts):
    if sum(player_value) == 21 and len(hand.split())==2:
        tip*=1,5
        ts+=tip
        print(f"Tvá hodnota karet je {sum(player_value)}, vyhrál jsi {tip} zlaťáků!")

    if sum(player_value)>21:
        ts-=tip
        print(f"Tvá hodnota karet je {sum(player_value)} proto jsi prohrál {tip} zlaťáků.")

    elif sum(player_value)<=21:
        ts+=tip
        print(f"Tvá hodnota karet je {sum(player_value)}. Vyhrál jsi {tip} zlaťáků, tvá celková zásoba je {ts}.")

    return ts
#herní kolo
def game_round(hand,pack,value,ts):

    playing = True
    while playing:
        bet = betting(ts)
        hand, pack  = deal_cards(hand, pack)
        value = value_of_card_on_hand(hand,value)
        bet, hand, value = cards_menu(hand,pack,bet,value)

        ts = checking_winning_condition(hand,value, bet, ts)
        if ts <=0:
            print("Promiň, ale nemáš zlaťáky na další hru.")
            break
        while True:
            new_round = input("Chceš hrát znova? A/N: ").capitalize()
            if new_round == "A":
                hand = ""
                value = []
                print(f"Tvoje celková zásoba zlaťáků je {ts}!")
                break
            elif new_round == "N":
                playing = False
                break
            else:
                print("Ano nebo ne stačí.")


    input()

player_hand = ""  #karty hráče
value_of_player_cards = [] # list hodnot karet na ruce u hráče
ai_hand = "" #karty od protihráče
value_of_ai_hand = []   # list hodnot karet na ruce protihráče
deck= []   #balík karet
total_score = 50 #celkové zlaťáků, v případě záporného čísla je prohra

main_menu(player_hand, deck,value_of_player_cards, total_score)