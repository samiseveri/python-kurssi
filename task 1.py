#passiiviagressiivinen savolainen ajastin
import random
import time
luku = 1
lista = []
kultakolikko = random.randrange(1, 1001)
pommi = random.randrange(1, 1001)
pisteet = 0



#nimi osuus
print("")
print("")
print("")
pelaajan_nimi = input("Pelaajan nimi: ")
nimi = sorted(pelaajan_nimi.lower())

print(f"Nimesi on paloiteltu aakkosjärjsetykseen")
print(nimi)
print("")
time.sleep(2.5)



#pelin alkuilmoitus
print ("Numero kenttään on piilotettu pommi ja kultakolikko")
print ("CURRENT OBJECTIVE: SURVIVE")
time.sleep(6.0)

#pelialue numeroita tippuu
while True:
    luku = random.randrange(1, 1001)
    print(luku)
    time.sleep(0.05)
    if luku not in lista:
        lista.append(luku)
        lista.sort()
    if luku == kultakolikko:
        break
    if luku == pommi:
        break
    if luku %100 == 0:
        print ("olet löytänyt pyöreän numeron, pikku jee :3")
        print ("ota tästä säälipiste")
        pisteet += 1
        time.sleep(3.0)
    if luku == 1 or luku == 1000:
        print("vau olet yksi tuhannesta ota tästä hiukan pisteitä")
        pisteet += 3
        time.sleep(3.0)
    if len(lista) == 998:
        break


märä = len(lista)
vast = 1000 - märä

#kultakolikko voitto
if luku ==kultakolikko:
    print("")
    print(f"OSUIT Numeroon {kultakolikko}")
    print("Olet löytänyt Kultakolikon! Pelastuit!")
    print(f"Etsit kaukaa kolikkoa kävit {märä} eri numeroa läpi ennen kolikkoa")
    print(f"pistetiä sait {pisteet}")
    print("")
    vast_k = input("haluatko nähdä todisteet? y/n ")
    if vast_k == "y":
        print("Tässä vielä kerrämäsi numerot suuruus järjsetyksessä")
        time.sleep(0.4)
        print(lista)

#pommi häviö
elif luku == pommi:
    print("")
    print ("RÄJÄHDIT")
    print (f"{vast} numeroa jäi käymättä läpi")
    print(f"pistetiä sait {pisteet}. En tiedä mitä pisteillä teet koska RÄJÄHDIT, muttä tässä ole hyvä...")
    print("")
    vast_p = input("haluatko nähdä todisteet? y/n ")
    if vast_p == "y":
        print("Tässä vielä kerrämäsi numerot suuruus järjsetyksessä")
        time.sleep(0.4)
        print(lista)

#salainen voitto
else:
    print("")
    print (f"Olet käynyt kaikki muut numerot läpi paitsi pommin({pommi}) ja kultakolikon({kultakolikko}).")
    print ("Olet matemaattinen mahdottomuus.... lahjakis saat tämän tähden")
    print ("""
                  ooo OOOAOOO ooo
              oOO       / \       OOo
          oOO          /   \          OOo
       oOO            /     \            OOo
     oOO             /       \             OOo
   oOO -_-----------/---------\-----------_- OOo
  oOO     -_       /           \       _-     OOo
 oOO         -_   /             \   _-         OOo
oOO             -/_             _\-             OOo
oOO             /  -_         _-  \             OOo
oOO            /      -_   _-      \            OOo
oOO           /         _-_         \           OOo
oOO          /       _-     -_       \          OOo
 oOO        /     _-           -_     \        OOo
  oOO      /   _-                 -_   \      OOo
   oOO    / _-                       -_ \    OOo
     oOO _-                             -_ OOo
      oOO                                OOo
          oOO                         OOo
             oOO                 OOo
                  ooo OOO OOO ooo

           """)
    
#pisteiden lisäys
print("")
pisteen_lisäys = input("Haluatko lisätä pisteitä, niinkuin joku luuseri? y = kyllä /n = ei/3k = kolmen kerroin lisäys /r = random lisäys 1-6 /k = kivi, sakset ja paperi ")
if pisteen_lisäys == "y":
    piste_lisäys_määrä = int(input("No paljonko lisätään pisteitä.... luuseri"))
    pisteet += piste_lisäys_määrä
    time.sleep(1.0)
    print(f"pisteet on lisätty, pisteitä on {pisteet}")
    time.sleep(2.0)
    print("nyt peli loppuu, koska oot tyhmä ja huijasit lisäämällä pisteitä >:(")
    print("")
    print("")

if pisteen_lisäys == "n":
    print("Hyvä, olet kunniallinen otus.")
    print(f"Kunnialliset pisteesi on {pisteet}. Voit olla ylpe OIKEISTA pisteistäsi")
    print("")
    print("")
if pisteen_lisäys == "3k":
    korroin_määrä = int(input("montako kertaa kolme haluat että lisätään pisteitä?.... Luuseri"))
    valmis_kerroin = korroin_määrä*3
    pisteet += valmis_kerroin
    time.sleep(1.0)
    print(f"pistetiä lisätään {valmis_kerroin}")
    time.sleep(1.0)
    print(f"pisteet on lisätty, pisteitä on {pisteet}")
    time.sleep(2.0)
    print("nyt peli loppuu, koska oot tyhmä ja huijasit lisäämällä pisteitä >:(")
    print("")
    print("")
if pisteen_lisäys == "r":
    print("annetaan satunnainen märä pisteitä 1 ja 6 väliltä")
    piste_random_kerroin = random.randrange(1, 7)
    time.sleep(1.0)
    print(f"Pistetä lisätään {piste_random_kerroin}")
    pisteet += piste_random_kerroin
    print(f"pisteet on lisätty, pisteitä on {pisteet}")
    time.sleep(2.0)
    print("nyt peli loppuu, koska oot tyhmä ja huijasit lisäämällä pisteitä >:(")
    print("")
    print("")




if pisteen_lisäys == "k":
    def get_user_choice():
        return input("Valitse kivi, sakset vai paperi: ").lower()

def get_computer_choice(options):
    return random.choice(options)

def determine_round_winner(user_choice, computer_choice):
    if user_choice == computer_choice:
        return "tie"
    elif (user_choice == "kivi" and computer_choice == "sakset") or \
         (user_choice == "paperi" and computer_choice == "kivi") or \
         (user_choice == "sakset" and computer_choice == "paperi"):
        return "user"
    else:
        return "computer"

def play_rock_paper_scissors():
    options = ["kivi", "paperi", "sakset"]
    p_pisteet, pc_pisteet = 0, 0

    while p_pisteet < 3 and pc_pisteet < 3:
        time.sleep(2.0)
        print(f"Tilanne on tietokone: {pc_pisteet} ja pelaajan pisteet: {p_pisteet}")
        
        user_choice = get_user_choice()
        if user_choice not in options:
            print("Virheellinen valinta. Yritä uudelleen.")
            continue

        computer_choice = get_computer_choice(options)
        print("Pelasit: ", user_choice)
        time.sleep(1.5)
        print("Tietokone valitsi: ", computer_choice)
        time.sleep(1.0)

        winner = determine_round_winner(user_choice, computer_choice)

        if winner == "tie":
            print("Tasapeli")
        elif winner == "user":
            print("Voitit")
            p_pisteet += 1
        else:
            print("Hävisit")
            pc_pisteet += 1

    if pc_pisteet == 3:
        print("Sinä hävisit")
    elif p_pisteet == 3:
        print("Sinä voitit")

if __name__ == "__main__":
    play_rock_paper_scissors()


    """"
    options = ["kivi", "paperi", "sakset"]
    p_pisteet = 0
    pc_pisteet = 0

    while p_pisteet != 3 or pc_pisteet != 3:
        time.sleep(2.0)
        print(f"tilanne on tietokone: {pc_pisteet} ja pelaajan pisteet {p_pisteet}")
        user_choice = input("valitse kivi, sakset vai paperi: ")
        computer_choice = random.choice(options)
        print("pelasit: ", user_choice)
        time.sleep(1.5)
        print("tietokone valitsi: ", computer_choice)
        time.sleep(1.0)
    
        if user_choice == computer_choice:
            print("tasapeli")

        elif user_choice == "kivi" and computer_choice == "sakset":
            print("voitit")
            p_pisteet += 1

        elif user_choice == "paperi" and computer_choice == "kivi":
            print("voitit")
            p_pisteet += 1

        elif user_choice == "sakset" and computer_choice == "paperi":
            print("voitit")
            p_pisteet += 1
        else:
            print("hävisit")
            pc_pisteet += 1
    if pc_pisteet == 3:
        print("sinä hävisit")
    if p_pisteet == 3:
        print("sinä voitit")

"""

