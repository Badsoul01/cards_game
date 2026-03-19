import random
#Kolo protihráče
def opponent_turn(computer_hand,pack,computer_value,):
    while sum(computer_value) <=17:
        computer_hand,pack = deal_cards(computer_hand,pack)
        computer_value = value_of_opponent_hand(computer_hand,computer_value)
        print(f"Karty na ruce protihráče: {computer_hand}")
    return computer_hand,pack,computer_value
# funkce na zjištění hodnot karet oponenta
def value_of_opponent_hand(hand,value):
    list_of_cards = hand.split()
    if len(list_of_cards) == 2 and  list_of_cards[0][1] =="A" and list_of_cards[1][1] =="A":
            value.clear()
            value.append(21)
            return value
    while len(value)< len(list_of_cards):
        card = list_of_cards[len(value)]
        if len(value)!= len(list_of_cards):
            if card[1:] in"JQKA":
                if card[1:] =="A":
                    if sum(value) <=10:
                            value.append(11)
                    else:
                            value.append(1)
                else:
                    value.append(10)
            elif card[1:].isdigit():
                value.append(int(card[1:]))
    return value
# funkce na zjištění hodnot karet v ruce
def value_of_card_on_hand(hand,value):
    list_hand = hand.split()
    while  len(value)< len(list_hand):
            current_card= list_hand[len(value)]
            if current_card[1:] in "KJQA":
                if current_card[1:]== "A":
                    value.append(value_of_player_aces(hand))
                else:
                    value.append(10)
            elif current_card[1:].isdigit():
                value.append(int(current_card[1:]))
    return value
# funkce na zjištění hodnot Esa u hráče
def value_of_player_aces(hand):
    print(f"Karty na tvé ruce {hand}")
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
    random.shuffle(pack)
    print("Zamíchali se všechny karty a vytvořil se nový balík!")
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
def main_menu(p_hand,computer_hand,pack,value,ai_value,ts):
    print("Vítej v této karetní hře!")
    print("""Co bys rád udělal?
    1) Začal novou hru
    2) Přečetl si pravidla
    3) Ukončil hru
    """)
    while True:
        choice = input("Tvé rozhodnutí: ")
        if choice == "1":
            game_round(p_hand,computer_hand,pack,value,ai_value,ts)
            break

        elif choice == "2":
            print("""
            Cíl hry je mít součet karet na ruce co nejblíže 21.Pokud budeš mít na ruce Eso, můžeš zvolit jeho hodnotu jako 1 nebo 11.
            K, Q a J je za 10bodů, zbytek podle hodnoty dané karty.Pokud překročíš 21 prohráváš a to co vsadíš se odečítá od tvé celkové výhry.\nPokud trefíš stejný bodový součet jako protivník dostaneš polovinu. A pokud vyhraješ tak dostáváš částku kterou vsadíš.\nJeště máš možnost zdvojnásobit částku.
            Dokud jsi na tahu tak z karet protivníka vidíš pouze první kartu. Poté co ukončíš svůj tah, dostane protivník případné další karty a vyhodnotí se kolo.
            """)

        elif choice == "3":
            break
        else:
            print("Prosím vyber z menu!")

    return choice
#možnosti mezi tahy
def cards_menu(p_hand,computer_hand,pack,tip, value,computer_value,ts):
    print(f"""Tvé karty na ruce: {p_hand}\nKarta na ruce protivníka je: {computer_hand[:3]}\n\nCo bys chtěl udělat?
    1. Dej mi další kartu.
    2. Zdvojnásobím sázku.
    3. Ukončit tah.
    """)
    while True:
        choice = input("Vyber si: ")
        if choice == "1":
            p_hand,pack  = deal_cards(p_hand, pack)
            value = value_of_card_on_hand(p_hand, value)
            print(f"Zde je tvá nová karta {p_hand[len(p_hand)-3::]}.\nKarty na ruce: {p_hand}.\nKarta na ruce protivníka je: {computer_hand[:3]}")

            if sum(value) >21:
               return tip, p_hand,computer_hand, pack, value, computer_value


        elif choice == "2":
            tip*=2
            if tip >ts:
                tip = ts
            p_hand,pack = deal_cards(p_hand, pack)
            print(f"Tvoje sázka jsou nyní {tip} a tvá nová karta je {p_hand.split()[-1]}.\nKarty na ruce: {p_hand}.")
            print(f"Karty protivníka jsou: {computer_hand}")
            value = value_of_card_on_hand(p_hand, value)
            computer_hand,pack,computer_value = opponent_turn(computer_hand,pack,computer_value,)
            return tip, p_hand,computer_hand, pack,value, computer_value
        elif choice == "3":
            print(f"Karty na tvé ruce: {p_hand}\nKarty protivníka:{computer_hand}")
            computer_hand, pack, computer_value = opponent_turn(computer_hand, pack, computer_value,)
            return tip, p_hand,computer_hand, pack, value, computer_value
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
def checking_winning_condition(p_hand, player_value,computer_value,tip,ts):
    if sum(player_value) > 21:
        ts -= tip
        print(f"Tvá hodnota karet je větší než 21, proto jsi prohrál {tip} zlaťáků.Tvá aktualní zásoba je {ts}")
    elif sum(computer_value)> 21:
        ts+=tip
        print(f"Počítač nasbíral větší hodnotu karet než je dovoleno.  Získáváš {tip} zlaťáků. Celkem již máš {ts}.")

    elif sum(player_value) == 21 and len(p_hand.split())==2:
        tip*=1.5
        ts+=int(tip)
        print(f"Tvá hodnota karet je {sum(player_value)},soupeř měl {sum(computer_value)}, vyhrál jsi {tip} zlaťáků! Máš {ts} zlaťáků.")

    elif sum(player_value) == sum(computer_value):
        ts+=tip//2
        print(f"Tvá hodnota karet je stejná jako hodnota karet na protivníkovy ruce, dostal jsi {tip//2} zlaťáků.Aktualně máš {ts}")

    elif sum(player_value) < sum(computer_value) <= 21:
        ts-=tip
        print(f"Tvá hodnota karet je {sum(player_value)}.Tvůj soupěř měl hodnoty karet {sum(computer_value)}. Prohrál  jsi {tip} zlaťáků, tvá celková zásoba je {ts}.")
    else:
        ts+=tip
        print(f"Tvá hodnota karet je {sum(player_value)}.Tvůj soupěř měl hodnoty karet {sum(computer_value)}. Vyhrál jsi {tip} zlaťáků, tvá celková zásoba je {ts}.")

    return ts
#herní kolo
def game_round(p_hand,computer_hand,pack,value,ai_value,ts):
    playing = True
    while playing:
        bet = betting(ts)

        p_hand, pack  = deal_cards(p_hand, pack)
        computer_hand,pack = deal_cards(computer_hand,pack)

        value = value_of_card_on_hand(p_hand,value)
        ai_value = value_of_opponent_hand(computer_hand,ai_value)

        bet, p_hand,computer_hand, pack, value,ai_value = cards_menu(p_hand,computer_hand,pack, bet, value, ai_value,ts)

        ts = checking_winning_condition(p_hand, value, ai_value, bet,ts)
        if ts <=0:
            print("Promiň, ale nemáš zlaťáky na další hru.")
            break
        while True:
            new_round = input("Chceš hrát znova? A/N: ").capitalize()
            if new_round == "A":
                p_hand = ""
                value = []
                computer_hand = ""
                ai_value = []
                print(f"Tvoje celková zásoba zlaťáků je {ts}!")
                break
            elif new_round == "N":
                playing = False
                print(f"Díky že jsi hrál. Ukořistil jsi {ts} zlaťáků..!")
                break
            else:
                print("Ano nebo ne stačí.")


    input()

player_hand = ""  #karty hráče
value_of_player_cards = [] # list hodnot karet na ruce u hráče
ai_hand = "" #karty od protihráče
value_of_ai_hand = []   # list hodnot karet na ruce protihráče
deck= []   #balík karet
total_score = 10 #celkové zlaťáků, v případě záporného čísla je prohra


if __name__ == "__main__":
    main_menu(player_hand,ai_hand,deck,value_of_player_cards,value_of_ai_hand,total_score)


