import random
# funkce na zjištění hodnot karet v ruce
def value_of_card_on_hand(hand,value):
    list_hand = hand.split()
    for i in range(len(list_hand)):
        if len(list_hand)>2:
            i+=1
            i*=-1
        if len(value) != len(list_hand):
            if list_hand[i][1] =="KJQA":
                if list_hand[i][1]== "A":
                    value.append(value_of_player_aces(hand))
                else:
                    value.append(10)
            elif list_hand[i][1].isdigit():
                if list_hand[i][1] ==1:
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
    deck  = []
    numbers = [2,3,4,5,6,7,8,9,10,"J","Q","K","A"]
    signs = ["♠","♥","♦","♣"]
    for sign in signs:
        for number in numbers:
            deck.append(sign+str(number))
    random.shuffle(deck)
    return deck
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

    return " ".join(new_hand)
# hlavní nabídka
def main_menu():
    print("Vítej v této karetní hře!")
    print("""Co bys rád udělal?
    1) Začal novou hru
    2) Přečetl si pravidla
    3) Ukončil hru
    """)
    while True:
        choice = input("Tvé rozhodnutí: ")
        if choice == "1":
            game_round()
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
        choice = int(input("Vyber si: "))
        if choice == 1:
            hand = deal_cards(hand, pack)
            print(f"Zde je tvá nová karta {hand[len(hand)-3::]}.")
            value = value_of_card_on_hand(hand,value)

        elif choice == 2:
            tip*=2
            hand = deal_cards(hand, pack)
            print(f"Tvoje sázka jsou nyní {tip} a tvá nová karta je {hand[len(hand)-3::]}.")
            value = value_of_card_on_hand(hand, value)
            return tip , hand,value
        elif choice == 3:
            return tip, hand,value
        else:
            print("Vyber z menu!")
# možnost sázek
def betting(ts):
    while True:
        amount_of_bet = input(f"Kolik zlaťáků by jsi chtěl vsadit? 1-{ts + 200}: ")
        if amount_of_bet.isdigit() and 0 < int(amount_of_bet) <= ts + 200:
            return int(amount_of_bet)

        else:
            print("Zadej číslo v určeném rozsahu!")
# kontrola výhry/prohry/remízy
def checking_winning_condition(player_value,tip,ts):
    if sum(player_value)>21:
        ts-=tip
        print(f"Tvá hodnota karet je více než 21, proto jsi prohrál {tip} zlaťáků, zatím jsi získal {ts} zlaťáků.")

    elif sum(player_value)<=21:
        ts+=tip
        print(f"Tvá hodnota karet je menší než 21. Vyhrál jsi {tip} zlaťáků, tvá celková zásoba je {ts}.")

    return ts
#herní kolo
def game_round():
    player_hand = ""  #karty hráče
    value_of_player_cards = [] # list hodnot karet na ruce u hráče
    ai_hand = "" #karty od protihráče
    deck= []   #balík karet
    total_score = 0 #celkové zlaťáků, v případě záporného čísla je prohra
    playing = True
    while playing:
        bet = betting(total_score)
        player_hand = deal_cards(player_hand, deck)
        bet, player_hand, value_of_player_cards = cards_menu(player_hand,deck,bet,value_of_player_cards)

        if not value_of_player_cards:
            value_of_player_cards = value_of_card_on_hand(player_hand,value_of_player_cards)

        total_score = checking_winning_condition(value_of_player_cards, bet, total_score)
        if total_score <=0:
            break
        while True:
            new_round = input("Chceš hrát znova? A/N: ").capitalize()
            if new_round == "A":
                player_hand = ""
                value_of_player_cards = []
                print(f"Tvoje celková momentální výhra je {total_score}!")
                break
            elif new_round == "N":
                playing = False
                break
            else:
                print("Ano nebo ne stačí.")
    #print(f"Celková hodnota tvých karet: {sum(value_of_player_cards)}")

    input()



main_menu()