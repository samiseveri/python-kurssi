#Savolainen ajastin, suunnilleen oikeassa.
import random
import time
luku = 1
lista = []
kultakolikko = random.randrange(1, 1001)
pommi = random.randrange(1, 1001)
pisteet = 0
print("")
print("")
print ("Numero kenttään on piilotettu pommi ja kultakolikko")
print ("CURRENT OBJECTIVE: SURVIVE")
time.sleep(6.0)
while True:
    luku = random.randrange(1, 1001)
    print(luku)
    time.sleep(0.05)
    if luku not in lista:
        lista.append(luku)
    if luku == kultakolikko:
        break
    if luku %100 == 0:
        print ("olent löytänyt pyören numeron, pikku jee :3")
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
if luku ==kultakolikko:
    print(f"OSUIT Numeroon {kultakolikko}")
    print("Olet löytänyt Kultakolikon! Pelastuit!")
    print(f"Etsit kaukaa kolikkoa kävit {märä} eri numeroa läpi ennen kolikkoa")
    print(f"pistetiä sait {pisteet}")
elif luku == pommi:
    print ("RÄJÄHDIT")
    print (f"{vast} numeroa jäi käymättä läpi")
    print(f"pistetiä sait {pisteet}. En tiedä mitä pisteillä teet koska RÄJÄHDIT, muttä tässä ole hyvä...")
else:
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