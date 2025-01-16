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
pisteen_lisäys = input("Haluatko lisätä pisteitä, niinkuin joku luuseri? y/n")
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





