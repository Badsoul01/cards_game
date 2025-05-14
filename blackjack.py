import random
#Kolo protihráče
def opponent_turn(computer_hand,pack,computer_value):
    while sum(computer_value) <=16:
        computer_hand,pack = deal_cards(computer_hand,pack)
        computer_value = value_of_opponent_hand(computer_hand,computer_value)
        print(f"Karty na ruce protihráče: {computer_hand}")
    return computer_hand,pack,computer_value
# funkce na zjištění hodnot karet oponenta
def value_of_opponent_hand(hand,value):
    list_of_cards = hand.split()
    for i in range(len(list_of_cards)):
        if len(list_of_cards)>2:
            i+=1
            i*=-1
        if len(value)!= len(list_of_cards):
            if list_of_cards[i][1] in "JQKA":
                if list_of_cards[i][1] =="A":
                    if len(list_of_cards) <=2:
                        value.append(11)
                    else:
                        if sum(value) >=10:
                            value.append(11)
                        else:
                            value.append(1)
                else:
                    value.append(10)
            elif list_of_cards[i][1].isdigit():
                if int(list_of_cards[i][1]) == 1:
                    value.append(10)
                else:
                    value.append(int(list_of_cards[i][1]))
    return value
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
def cards_menu(p_hand,computer_hand,pack,tip, value,computer_value):
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
                print(f"Karty na ruce: {p_hand}\nKarty na ruce protivníka jsou: {computer_hand}")
                return tip, p_hand,computer_hand, value, computer_value
        elif choice == "2":
            tip*=2
            hand,pack = deal_cards(p_hand, pack)
            print(f"Tvoje sázka jsou nyní {tip} a tvá nová karta je {p_hand[len(p_hand)-3::]}.\nKarty na ruce: {hand}.")
            print(f"Karty protivníka jsou: {computer_hand}")
            value = value_of_card_on_hand(p_hand, value)
            computer_hand,pack,computer_value = opponent_turn(computer_hand,pack,computer_value)
            return tip, p_hand,computer_hand, value, computer_value
        elif choice == "3":
            print(f"Karty na tvé ruce: {p_hand}\nKarty protivníka:{computer_hand}")
            computer_hand, pack, computer_value = opponent_turn(computer_hand, pack, computer_value)
            return tip, p_hand,computer_hand, value, computer_value
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
    if sum(player_value) == 21 and len(p_hand.split())==2:
        tip*=1,5
        ts+=tip
        print(f"Tvá hodnota karet je {sum(player_value)},soupeř měl {sum(computer_value)}, vyhrál jsi {tip} zlaťáků!")

    if sum(player_value) == sum(computer_value) and sum(player_value)<=21:
        ts+=tip//2
        print(f"Tvá hodnota karet je stejná jako hodnota karet na protivníkovy ruce, dostal jsi {tip//2} zlaťáků.")

    if sum(player_value)>21:
        ts-=tip
        print(f"Tvá hodnota karet je větší než 21, proto jsi prohrál {tip} zlaťáků.")
    if 21>=sum(computer_value)>sum(player_value):
        ts-=tip
        print(f"Protivník měl hodnotu karet blíže 21.Prohrál jsi {tip} zlaťáků.")
    if 21 >= sum(player_value) > sum(computer_value):
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
        bet, p_hand,computer_hand, value,ai_value = cards_menu(p_hand,computer_hand,pack, bet, value, ai_value)

        ts = checking_winning_condition(p_hand, value, ai_value, bet,total_score)
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


