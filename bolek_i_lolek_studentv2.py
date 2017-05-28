#
# Bolek i Lolek pracuja na dwu-stanowiskowej linii produkcyjnej i wytwarzaja
# pudelka. W ten sposob ze Bolek je sklada a Lolek je skleja
#
# pudelko  -->  B (skladanie) --> L (sklejanie) --> stos gotowych pudel
#
# Pudelko po zlozeniu poczostaju u B tak dlugo az nie moze byc przejete przez L
#
# Oczekiwane wartosci czasu skladania i sklejania sa takie same,
# ale zmienne maja rozne rozklady

czasyA = { #czas : liczba pudel
  10 : 4,
  20 : 6,
  30 : 10,
  40 : 20,
  50 : 40,
  60 : 11,
  70 : 5,
  80 : 4         
}

czasyB = { #czas : liczba pudel
  10 : 4,
  20 : 5,
  30 : 6,
  40 : 7,
  50 : 10,
  60 : 8,
  70 : 6,
  80 : 2         
}

#
# Jaka jest wydajnosc tej linii produkcyjnej?
# Jak na wydajnosc wplynie umieszczenie pomiedzy pracownikami magazynu?
#

import random as rd
from timeit import itertools
from bisect import bisect
import scipy as sp

listaCzasow = sp.sort(list(czasyA.keys()))

#skumulowane prawd dla metody odwracania dystrubanty
probCumB = list(itertools.accumulate([czasyA[x]/sum(czasyA.values()) for x in listaCzasow] ))
probCumL = list(itertools.accumulate([czasyB[x]/sum(czasyB.values()) for x in listaCzasow] ))

def wyszukajpionowo(los, skumulowanePraw,listaWartosci):
    return listaWartosci[bisect(skumulowanePrawd, los)]

	
rd.seed(0)

# Dwustanowiskowa linia produkcyjna
# Bolek sklada pudelka a Lolek skleja
class LiniaProdukcyjna:
    
    bolekDzialanieKoniec = None   #w sekundach
    lolekDzialanieKoniec = None   #w sekundach
	bolekMaPudlo = False #Bolek ma w rekach pudlo dla Lolka

    tick = 0   #mierzone w krokach symulacji
    zegar = 0  #mierzone w sekundach
    gotowePudla = 0 #mierzone w sztukach
    def __init__(self):
        print("#inicjalizacja modelu")
        
    
    def step(self):
        #Metoda przegladu zdarzen:
        # Zdarzenia bezwarunkowe : przybycie nowego zgloszenia i zakonczenie obslugi
        # Zdarzenia warunkowe : rozpoczecie obslugi
        #Algorytm postepowanie: 
        # 1. Wyznacz moment czasu wystapienia zdarzenia bezwarunkowego
        # 2. W przypadku wystapieniu zdarzenia bezwarunkowe sprawdz czy moze wystapic zdarzenie warunkowe 
        
        #Bolek i Lolek
        #Zdarzenia bezwarunkowe: Lolek skonczyl skladac, Bolek skonczyl skladac
        #Zdarzenia warunkowe: Lolek rozpoczyna klejenie, Bolek rozpoczyna skladanie 
    
        print("tick=",self.tick,"zegar=",self.zegar,"bolek ma pudlo", self.bolekMaPudlo,"bolekDzialanieKoniec=",
              self.bolekDzialanieKoniec,
              "lolekDzialanieKoniec=",self.lolekDzialanieKoniec,
              "gotowePudla=",self.gotowePudla)

#uruchomienie modelu
wyniki = []
for powtorz in range(1):
    m = LiniaProdukcyjna()
    for krok in range(12):  
        m.step()
        #if m.zegar > 7200:
        #    break
    wyniki.append(m.gotowePudla)
