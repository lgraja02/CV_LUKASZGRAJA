import random
import matplotlib.pyplot as plt
import timeit
import sys
import os
os.system('ulimit -s unlimited; some_executable')
sys.setrecursionlimit(10000000)
#----------------------------------------------------------------------
"""generator ciagu liczb losowych niepowtarzających sie"""
def random_generator(zakres_poczatek, zakres_koniec, ilosc_liczb):
    random_numbers = []
    while len(random_numbers) < ilosc_liczb:
        num = random.randint(zakres_poczatek, zakres_koniec)
        if num not in random_numbers:
            random_numbers.append(num)
    return random_numbers

# Przykład użycia:
zakres_poczatek = 1
zakres_koniec = 1000
ilosc_liczb = 10
#----------------------------------------------------------------------
"""BST"""
class Wezel:
    def __init__(self, dane=None):
        self.dane = dane
        self.lewe_dziecko = None
        self.prawe_dziecko = None
        self.wspolczynnik_rownowagi = 0

class BST:
    def __init__(self):
        self.korzen = None

    def dodaj(self, dane):
        if self.korzen is None:             #jeżeli w drzewie nie ma elementu
            self.korzen = Wezel(dane)       # to pierwszy dodany będzie korzeniem
        else:
            self.dodaj_do_wierzcholka(dane, self.korzen)         #jeżeli są już jakieś elementy to dodajemy je do istniejącej struktury

    def dodaj_do_wierzcholka(self, dane, wierzcholek):           #funkcja pomocnocz, pomaga w znalezeniu odpowiedniego miejsca do wstawienia elementu w drzewie
        if dane < wierzcholek.dane:                              #jeżeli dane(input) są mniejsze od danego wierzchołka (patrzymy w lewo)
            if wierzcholek.lewe_dziecko is None:                 #jeżeli lewe dziecko nie istnieje to   lewe = dane
                wierzcholek.lewe_dziecko = Wezel(dane)
            else:
                self.dodaj_do_wierzcholka(dane, wierzcholek.lewe_dziecko)       #jeżeli lewe dziecko istnieje to rekurencyjnie wywołujemy funkcje by znalezc odpowiednie miejsce
        elif dane > wierzcholek.dane:                                 #jeżeli dane(input) są większe od danego wierzchołka (patrzymy w prawo)
            if wierzcholek.prawe_dziecko is None:                     #jeżeli prawe dziecko nie istnieje to    prawe = dane
                wierzcholek.prawe_dziecko = Wezel(dane)
            else:
                self.dodaj_do_wierzcholka(dane, wierzcholek.prawe_dziecko)          #jeżeli prawe dziecko istnieje to rekurencyjnie szukamy kolejnego miejsca na nowy element

        # Po dodaniu węzła, aktualizujemy wartość współczynnika równowagi dla każdego węzła
        wierzcholek.wspolczynnik_rownowagi = self.oblicz_wspolczynnik_rownowagi(wierzcholek)     #po dodaniu elementu aktualizujemy wspoczynnik rownowagi (potrzebne do rownowazenia)


    def dodaj_z_listy(self, lista):                 #funkcja pomocnicza do dodawania elementów z listy
        for element in lista:
            self.dodaj(element)


#=======================================================================================================================
#ROWNOWAZENIE DRZEWA PRZEZ USUWANIE KORZENI NIEZBALANSOWANYCH
    def rownowaz_drzewo(self):
        while True:
            # Sprawdzanie czy drzewo jest puste
            if self.korzen is None:
                print("Drzewo jest puste.")
                return

            # zmienna przechowująca pierwszy niezbalansowany węzeł
            niezbalansowany_wezel = self.level_order_traversal()

            # Sprawdzanie czy znaleziono niezbalansowany węzeł
            if niezbalansowany_wezel is None:
                print("Drzewo jest zrównoważone.")
                return


            # Usuwanie niezbalansowanego węzeł
            self.usun(niezbalansowany_wezel)

            # Dodawanie usuniętego węzeła ponownie do drzewa
            self.dodaj(niezbalansowany_wezel)


            # Wyświetlanie współczynnika równowagi po równoważeniu drzewa
            self.wyswietl_wspolczynnik_rownowagi()

#=======================================================================================================================
#====================================================
#WSPOLCZYNNIK ROWNOWAGI MIEDZY WEZLAMI

    def oblicz_wysokosc(self, wezel):
        if wezel is None:              #warunek kończący rekurencje
            return 0
        lewa_wysokosc = self.oblicz_wysokosc(wezel.lewe_dziecko)    #obliczanie wysokosci lewego dziecka
        prawa_wysokosc = self.oblicz_wysokosc(wezel.prawe_dziecko)  #obliczanie wysokosci prawego dziecka
        return 1 + max(lewa_wysokosc, prawa_wysokosc)             #zwracanie wysokosci wiekszej (lewej lub prawej) +1 bo rodzic

    def oblicz_wspolczynnik_rownowagi(self, wezel):
        if wezel is None:             #warunek kończący rekurencje
            return 0
        lewa_wysokosc = self.oblicz_wysokosc(wezel.lewe_dziecko)    #obliczanie wysokosci lewego dizecka
        prawa_wysokosc = self.oblicz_wysokosc(wezel.prawe_dziecko)  #obliczanie wysokosci prawego dziecka
        return abs(lewa_wysokosc - prawa_wysokosc)                #zwracanie wartosci bezwzględnej wspolczynnika rownowagi

# ====================================================
    # WYSWIETLANIE WSPOLCZYNNIKA ROWNOWAGI
    def wyswietl_wspolczynnik_rownowagi(self):
        if self.korzen is None:
            print("Drzewo jest puste.")     #sprawdzanie czy drzewo jest puste
            return

        stos = []                       #lista pomocnicza do przechodzenia po węzłach drzewa
        stos.append(self.korzen)        #na początku umieszczamy korzeń do stosu

        while stos:         #while będzie trwać do puki stos nie będzie pusty (dopuki nie przejdziemy po wszystkich wierzchołkach drzewa)
            wierzcholek = stos.pop()    #zdjęcie wierzchołka z stosu - potrzebne by wypisać dane, i dzieci

            print(f"\nWspółczynnik równowagi dla węzła {wierzcholek.dane}: {wierzcholek.wspolczynnik_rownowagi}")       #WYPISANIE WR

            if wierzcholek.lewe_dziecko:
                stos.append(wierzcholek.lewe_dziecko)       #przekazanie lewego dziecka do wypisania WR
            if wierzcholek.prawe_dziecko:
                stos.append(wierzcholek.prawe_dziecko)      #przekazanie prawego dziecka do wypisania WR

#====================================================
#LEVEL-ORDER + znajdowanie pierwszego niezbalansowanego wierzchołka
    def level_order_traversal(self):
        if self.korzen is None:                #sprawdzanie czy drzewo jest puste
            print("Drzewo jest puste.")
            return

        # Inicjalizacja pustej listy, która będzie wykorzystana jako kolejka
        kolejka = [self.korzen]
        niezsbalansowany_wezel = None  # Zmienna przechowująca dane pierwszego niezbalansowanego węzła

        # Pętla przetwarzająca wierzchołki w kolejności level-order
        while kolejka:
            # Pobranie pierwszego wierzchołka z kolejki
            wierzcholek = kolejka.pop(0)

            # Sprawdzenie współczynnika równowagi dla bieżącego węzła
            wspolczynnik = self.oblicz_wspolczynnik_rownowagi(wierzcholek)
            # Jeśli współczynnik równowagi jest większy niż 1 i jeszcze nie zapisaliśmy niezrównoważonego węzła,
            # to zapisujemy dane bieżącego węzła
            if wspolczynnik > 1 and niezsbalansowany_wezel is None:
                niezsbalansowany_wezel = wierzcholek.dane

            # Dodanie lewego i prawego dziecka bieżącego węzła do kolejki
            if wierzcholek.lewe_dziecko:
                kolejka.append(wierzcholek.lewe_dziecko)
            if wierzcholek.prawe_dziecko:
                kolejka.append(wierzcholek.prawe_dziecko)

        # Wyświetlenie danych pierwszego niezrównoważonego węzła, jeśli taki został znaleziony
        if niezsbalansowany_wezel is not None:
            print(f"Pierwszy niezbalansowany węzeł: {niezsbalansowany_wezel}")
            return niezsbalansowany_wezel
        else:
            print("Nie znaleziono niezbalansowanego węzła.")
#=======================================================================================================================
#====================================================
#ZNALEZIENIE NAJMNIEJSZEGO I NAJWIEKSZEGO ELEMENTU
    def najmniejszy(self):
        if self.korzen is None:     #sprawdzenie czy drzewo jest puste
            return None, []

        sciezka = []              #zapisanie sciezki
        aktualny = self.korzen
        while aktualny.lewe_dziecko:    #najmniejszy element znajduje się maksymalnie po lewej stronie
            sciezka.append(aktualny.dane)     #zapis do sciezki
            aktualny = aktualny.lewe_dziecko    #zmiana aktualnego
        sciezka.append(aktualny.dane)     #zapis ostatniego elementu do sciezki

        return aktualny.dane, sciezka

    def najwiekszy(self):
        if self.korzen is None:     #sprawdzenie czy drzeow jest puste
            return None, []

        sciezka = []               #zapis sciezki
        aktualny = self.korzen
        while aktualny.prawe_dziecko:   #najwiekszy element znajduje się maksymalnie po prawej stronie
            sciezka.append(aktualny.dane)
            aktualny = aktualny.prawe_dziecko
        sciezka.append(aktualny.dane)   #zapis ostatniego elementu do sciezki

        return aktualny.dane, sciezka
#=====================================================
#USUWANIE DANEGO ELEMENTU
    def usun(self, dane):
        """Metoda usuwająca wierzchołek o podanej wartości."""
        self.korzen = self._usun_wierzcholek(self.korzen, dane)

    def _usun_wierzcholek(self, wierzcholek, dane):
        """Metoda pomocnicza usuwająca wierzchołek o podanej wartości."""
        #dane - które chcemy usunąć
        #wierzchołek - aktualnie sprawdzany wierzchołek

        if wierzcholek is None:
            return None

        if dane < wierzcholek.dane:             #sprawdzanie/szukanie wierzchołka do usunięcia, (zasada prawe większe lewo mniejsze)
            wierzcholek.lewe_dziecko = self._usun_wierzcholek(wierzcholek.lewe_dziecko, dane)
        elif dane > wierzcholek.dane:
            wierzcholek.prawe_dziecko = self._usun_wierzcholek(wierzcholek.prawe_dziecko, dane)
        else:
            if wierzcholek.lewe_dziecko is None:        #jeżeli drzewo ma tylko prawe dziecko - prawe jest następnikiem
                return wierzcholek.prawe_dziecko
            elif wierzcholek.prawe_dziecko is None:     #jeżeli drzewo ma tylko lewe dziecko - lewe jest następnikiem
                return wierzcholek.lewe_dziecko
            else:
                nastepnik, rodzaj = self._nastepnik(wierzcholek)    #jeżeli drzewo ma dwoje dzieci szukamy następnika za pomocą _nastepnik SLAJDY!!!
                wierzcholek.dane = nastepnik.dane             #ustawienie znalezionego nastepnika

                if rodzaj == "prawe":        #po ustawieniu wierzhołka na nastepnik, mamy "duplikat" więc musimy usunąć następnik z drzewa
                    wierzcholek.prawe_dziecko = self._usun_wierzcholek(wierzcholek.prawe_dziecko, nastepnik.dane)
                else:
                    wierzcholek.lewe_dziecko = self._usun_wierzcholek(wierzcholek.lewe_dziecko, nastepnik.dane)

        #aktualizacja wspoczynnika rownowagi wierzcholka
        wierzcholek.wspolczynnik_rownowagi = self.oblicz_wspolczynnik_rownowagi(wierzcholek)

        return wierzcholek

    def _nastepnik(self, wierzcholek):
        if wierzcholek is None:
            return None

        klucze_in_order = self.in_order(wierzcholek)          #stworzenie listy kluczy "posortowanych"

        lewa_wysokosc = self.oblicz_wysokosc(wierzcholek.lewe_dziecko)      #sprawdzenie lewej i prawej wysokosci by zadecydowac
        prawa_wysokosc = self.oblicz_wysokosc(wierzcholek.prawe_dziecko)    # z ktorej strony wziac następnik (z klucze_in_order)  - potrzebne do balansowania drzewa

        # Znajdowanie indeksu klucza, który ma być usunięty w liscie
        indeks = klucze_in_order.index(wierzcholek.dane)

        if lewa_wysokosc > prawa_wysokosc and indeks - 1 >= 0:    #jeżeli lewa wys jest większa od prawej to bierzemy następnik z lewego dziecka
            rodzaj = "lewe"                               #rodzaj potrzebny do ifa w funkcji _usun_wierzcholek
            nastepnik_dane = klucze_in_order[indeks - 1]          # -1 - z lewej strony listy
            nastepnik_wezel = self.znajdz_wartosc(nastepnik_dane)
        elif lewa_wysokosc < prawa_wysokosc and indeks + 1 < len(klucze_in_order): #jeżeli prawa wys jest większa od lewej to bierzemy następnik z prawego dziecka
            rodzaj = "prawe"
            nastepnik_dane = klucze_in_order[indeks + 1]     # +1 - z prawej strony listy
            nastepnik_wezel = self.znajdz_wartosc(nastepnik_dane)
        else:
            return None

        return nastepnik_wezel, rodzaj
#
    def znajdz_wartosc(self, wartosc, wierzcholek=None):       #potrzebne do _nastepnik bo zwracał klucz jako wartość a nie obiekt
        if wierzcholek is None:
            wierzcholek = self.korzen       #jeżeli nie podamy żadnego wierzchołka, to automatycznie jest on ustawiany jako korzeń

        if wierzcholek is None:             #sprawdzanie czy wierzchołek jest pusty (czy drzewo jest puste)
            return None

        if wartosc == wierzcholek.dane:     #zwracanie wierzchołka jeżeli został znaleziony
            return wierzcholek

        if wartosc < wierzcholek.dane:                                       #szykanie wierzchołka po drzewie kierując się zasadą;
            return self.znajdz_wartosc(wartosc, wierzcholek.lewe_dziecko)    # większe na prawo, mniejsze na lewo
        else:
            return self.znajdz_wartosc(wartosc, wierzcholek.prawe_dziecko)
#=====================================================
#POST ORDER USUNIECIE DRZEWA
    def post_order(self, wierzcholek):
        if wierzcholek:                #sprawdzenie czy wierzchołek istnieje
            self.post_order(wierzcholek.lewe_dziecko)       #LEWE ---- rekurencyjnie do lewego i prawego dziecka
            self.post_order(wierzcholek.prawe_dziecko)      #PRAWE ---- kolejnosc ma znaczeni bo ---> post-order: lewe poddrzewo, prawe poddrzewo, korzeń
            if wierzcholek.dane:       #KORZEŃ --- jeżeli wierzchołek istnieje to go usuwamy
                print("usunieto: ", str(wierzcholek.dane))
                self.usun(wierzcholek.dane)

#=====================================================
#PODDRZEWO PRE-ORDER
    def pre_order(self, wierzcholek):
        if wierzcholek:                 #pre-order: korzeń, lewe poddrzewo, prawe poddrzewo
            if wierzcholek.dane:       #KORZEŃ
                print(str(wierzcholek.dane), end='-')
                self.pre_order(wierzcholek.lewe_dziecko)  #LEWE
                self.pre_order(wierzcholek.prawe_dziecko)  #PRAWE

    def pre_order_subtree(self, wierzcholek, klucz):
        if wierzcholek is None:  #warunek kończący rekurencje
            return

        if wierzcholek.dane == klucz:  # Jeśli klucz został znaleziony, wypisujemy poddrzewo
            print("Pre-order poddrzewa o korzeniu", klucz, ":")
            self.pre_order(wierzcholek)  # Wywołana metoda pre_order na korzeniu poddrzewa o danym kluczu
            return

        # Rekurencyjnie wywołanie pre_order_subtree dla lewego i prawego poddrzewa
        self.pre_order_subtree(wierzcholek.lewe_dziecko, klucz)
        self.pre_order_subtree(wierzcholek.prawe_dziecko, klucz)


#=====================================================
#WYSWIETLADNIE
    def wyswietl(self):                 #pomocnicze do debbugowania
        def pre_order2(wierzcholek):
            if wierzcholek:
                if wierzcholek.dane:
                    print(str(wierzcholek.dane), end='-')
                    pre_order2(wierzcholek.lewe_dziecko)
                    pre_order2(wierzcholek.prawe_dziecko)
        print("Pre-order:")
        pre_order2(self.korzen)

    def in_order(self, wierzcholek):
        kolejnosc = []
        if wierzcholek:
            kolejnosc.extend(self.in_order(wierzcholek.lewe_dziecko))
            if wierzcholek.dane:
                kolejnosc.append(wierzcholek.dane)
            kolejnosc.extend(self.in_order(wierzcholek.prawe_dziecko))
        return kolejnosc



#=====================================================
"""BST"""
#=====================================================
# # Obsługa danych wejściowych jako generator

# def random_generator(zakres_poczatek, zakres_koniec, ilosc_liczb):
#     random_numbers = []
#     while len(random_numbers) < ilosc_liczb:
#         num = random.randint(zakres_poczatek, zakres_koniec)
#         if num not in random_numbers:
#             random_numbers.append(num)
#     return random_numbers
#
# # Przykład użycia:
# zakres_poczatek = 1
# zakres_koniec = 20
# ilosc_liczb = 10
#
# random_dane = random_generator(zakres_poczatek, zakres_koniec, ilosc_liczb)
# print(random_dane)
# #[13, 18, 17, 16, 4, 2, 12, 14, 10, 1]
# drzewo = BST()
# drzewo.dodaj_z_listy(random_dane)
# drzewo.wyswietl()
# print("\n--------------------")
#=====================================================
# print("MIN MAX")
# najmniejszy, sciezkamin = drzewo.najmniejszy()
# najwiekszy, sciezkamax = drzewo.najwiekszy()
#
# print("Najmniejszy element w drzewie:", najmniejszy, "sciezka: ",sciezkamin)
# print("Największy element w drzewie:", najwiekszy, "sciecka: ",sciezkamax)
# print("\n--------------------")
#=====================================================
# print("USUWANIE PODANEGO PRZEZ UZYTKOWNIKA ELEMENTU")
# key = 6
# print("usuwane: ", key)
# drzewo.usun(key)
# drzewo.wyswietl()
# print("\n--------------------")
#=====================================================
# klucz = 6  # Klucz korzenia poddrzewa do wypisania
# drzewo.pre_order_subtree(drzewo.korzen, klucz)
# print("\n--------------------")
# #=====================================================
# print("\nUSUWANIE POST ORDER")
# print(drzewo.post_order(drzewo.korzen))
# print("\n--------------------")
# #=====================================================
# drzewo.wyswietl_wspolczynnik_rownowagi()
# print("\n--------------------")
#=====================================================
# #BALANSOWANIE DRZEWA
# print("balansowanie drzewa")
# print("drzewo przed zbalansowaniem")
# drzewo.wyswietl()
# drzewo.wyswietl_wspolczynnik_rownowagi()
# drzewo.rownowaz_drzewo()
# print("drzewo po zbalansowaniu: ")
# drzewo.wyswietl()

#====================================================
#====================================================
# Obsługa danych wejściowych jako lista

# lista_danych = [8,2,1,5,6,14,10,9,12,13]
# print(lista_danych)
# print("\n--------------------")
# print("WYSWIETLANIE")
# drzewoBST = BST()
# drzewoBST.dodaj_z_listy(lista_danych)
# drzewoBST.wyswietl()
# print("\n---------------------")










#=================== XX ============== XX ====== XX ==== XX ============================================================
#================= XX  XX ============ XX ====== XX ==== XX ============================================================
#=============== XXXXXXXXXXX =========== XX == XX ====== XX ============================================================
#============= XX  ======  XX ========== XX == XX ====== XX ============================================================
#=========== XX  ============XX ==========  XX ========  XXXXXXX =======================================================
""" AVL """
class AVL:
    def __init__(self):
        self.korzen = None

    def dodaj(self, dane):
        if self.korzen is None:
            self.korzen = Wezel(dane)
        else:
            self.dodaj_do_wierzcholka(dane, self.korzen)

    def dodaj_do_wierzcholka(self, dane, wierzcholek):
        if dane < wierzcholek.dane:
            if wierzcholek.lewe_dziecko is None:
                wierzcholek.lewe_dziecko = Wezel(dane)
            else:
                self.dodaj_do_wierzcholka(dane, wierzcholek.lewe_dziecko)
        elif dane > wierzcholek.dane:
            if wierzcholek.prawe_dziecko is None:
                wierzcholek.prawe_dziecko = Wezel(dane)
            else:
                self.dodaj_do_wierzcholka(dane, wierzcholek.prawe_dziecko)

        # Po dodaniu węzła, aktualizujemy wartość współczynnika równowagi dla każdego węzła
        wierzcholek.wspolczynnik_rownowagi = self.oblicz_wspolczynnik_rownowagi(wierzcholek)

    def dodaj_z_listy(self, lista):
        if len(lista) == 0:  # Sprawdzamy czy lista jest pusta
            return

        srodkowy_indeks = len(lista) // 2  # Znajdujemy indeks środkowego elementu
        srodkowy_element = lista[srodkowy_indeks]  # Pobieramy środkowy element
        self.dodaj(srodkowy_element)  # Dodajemy środkowy element do drzewa AVL

        lewa = lista[:srodkowy_indeks]  # Tworzymy listę elementów po lewej stronie
        prawa = lista[srodkowy_indeks + 1:]  # Tworzymy listę elementów po prawej stronie

        self.dodaj_z_listy(lewa)  # Rekurencyjnie dodajemy lewą część do drzewa AVL
        self.dodaj_z_listy(prawa)  # Rekurencyjnie dodajemy prawą część do drzewa AVL


#=======================================================================================================================
#ROWNOWAZENIE DRZEWA PRZEZ USUWANIE KORZENI NIEZBALANSOWANYCH
    def rownowaz_drzewo(self):
        while True:
            # Sprawdzanie czy drzewo jest puste
            if self.korzen is None:
                print("Drzewo jest puste.")
                return

            # zmienna przechowująca pierwszy niezbalansowany węzeł
            niezbalansowany_wezel = self.level_order_traversal()

            # Sprawdzanie czy znaleziono niezbalansowany węzeł
            if niezbalansowany_wezel is None:
                print("Drzewo jest zrównoważone.")
                return


            # Usuwanie niezbalansowanego węzeł
            self.usun(niezbalansowany_wezel)

            # Dodawanie usuniętego węzeła ponownie do drzewa
            self.dodaj(niezbalansowany_wezel)


            # Wyświetlanie współczynnika równowagi po równoważeniu drzewa
            self.wyswietl_wspolczynnik_rownowagi()

#=======================================================================================================================
#====================================================
#WSPOLCZYNNIK ROWNOWAGI MIEDZY WEZLAMI

    def oblicz_wysokosc(self, wezel):
        if wezel is None:              #warunek kończący rekurencje
            return 0
        lewa_wysokosc = self.oblicz_wysokosc(wezel.lewe_dziecko)    #obliczanie wysokosci lewego dziecka
        prawa_wysokosc = self.oblicz_wysokosc(wezel.prawe_dziecko)  #obliczanie wysokosci prawego dziecka
        return 1 + max(lewa_wysokosc, prawa_wysokosc)             #zwracanie wysokosci wiekszej (lewej lub prawej) +1 bo rodzic

    def oblicz_wspolczynnik_rownowagi(self, wezel):
        if wezel is None:             #warunek kończący rekurencje
            return 0
        lewa_wysokosc = self.oblicz_wysokosc(wezel.lewe_dziecko)    #obliczanie wysokosci lewego dizecka
        prawa_wysokosc = self.oblicz_wysokosc(wezel.prawe_dziecko)  #obliczanie wysokosci prawego dziecka
        return abs(lewa_wysokosc - prawa_wysokosc)                #zwracanie wartosci bezwzględnej wspolczynnika rownowagi

# ====================================================
    # WYSWIETLANIE WSPOLCZYNNIKA ROWNOWAGI
    def wyswietl_wspolczynnik_rownowagi(self):
        if self.korzen is None:
            print("Drzewo jest puste.")     #sprawdzanie czy drzewo jest puste
            return

        stos = []                       #lista pomocnicza do przechodzenia po węzłach drzewa
        stos.append(self.korzen)        #na początku umieszczamy korzeń do stosu

        while stos:         #while będzie trwać do puki stos nie będzie pusty (dopuki nie przejdziemy po wszystkich wierzchołkach drzewa)
            wierzcholek = stos.pop()    #zdjęcie wierzchołka z stosu - potrzebne by wypisać dane, i dzieci

            print(f"\nWspółczynnik równowagi dla węzła {wierzcholek.dane}: {wierzcholek.wspolczynnik_rownowagi}")       #WYPISANIE WR

            if wierzcholek.lewe_dziecko:
                stos.append(wierzcholek.lewe_dziecko)       #przekazanie lewego dziecka do wypisania WR
            if wierzcholek.prawe_dziecko:
                stos.append(wierzcholek.prawe_dziecko)      #przekazanie prawego dziecka do wypisania WR

#====================================================
#LEVEL-ORDER + znajdowanie pierwszego niezbalansowanego wierzchołka
    def level_order_traversal(self):
        if self.korzen is None:                #sprawdzanie czy drzewo jest puste
            print("Drzewo jest puste.")
            return

        # Inicjalizacja pustej listy, która będzie wykorzystana jako kolejka
        kolejka = [self.korzen]
        niezsbalansowany_wezel = None  # Zmienna przechowująca dane pierwszego niezbalansowanego węzła

        # Pętla przetwarzająca wierzchołki w kolejności level-order
        while kolejka:
            # Pobranie pierwszego wierzchołka z kolejki
            wierzcholek = kolejka.pop(0)

            # Sprawdzenie współczynnika równowagi dla bieżącego węzła
            wspolczynnik = self.oblicz_wspolczynnik_rownowagi(wierzcholek)
            # Jeśli współczynnik równowagi jest większy niż 1 i jeszcze nie zapisaliśmy niezrównoważonego węzła,
            # to zapisujemy dane bieżącego węzła
            if wspolczynnik > 1 and niezsbalansowany_wezel is None:
                niezsbalansowany_wezel = wierzcholek.dane

            # Dodanie lewego i prawego dziecka bieżącego węzła do kolejki
            if wierzcholek.lewe_dziecko:
                kolejka.append(wierzcholek.lewe_dziecko)
            if wierzcholek.prawe_dziecko:
                kolejka.append(wierzcholek.prawe_dziecko)

        # Wyświetlenie danych pierwszego niezrównoważonego węzła, jeśli taki został znaleziony
        if niezsbalansowany_wezel is not None:
            print(f"Pierwszy niezbalansowany węzeł: {niezsbalansowany_wezel}")
            return niezsbalansowany_wezel
        else:
            print("Nie znaleziono niezbalansowanego węzła.")
#=======================================================================================================================
#====================================================
#ZNALEZIENIE NAJMNIEJSZEGO I NAJWIEKSZEGO ELEMENTU
    def najmniejszy(self):
        if self.korzen is None:     #sprawdzenie czy drzewo jest puste
            return None, []

        sciezka = []              #zapisanie sciezki
        aktualny = self.korzen
        while aktualny.lewe_dziecko:    #najmniejszy element znajduje się maksymalnie po lewej stronie
            sciezka.append(aktualny.dane)     #zapis do sciezki
            aktualny = aktualny.lewe_dziecko    #zmiana aktualnego
        sciezka.append(aktualny.dane)     #zapis ostatniego elementu do sciezki

        return aktualny.dane, sciezka

    def najwiekszy(self):
        if self.korzen is None:     #sprawdzenie czy drzeow jest puste
            return None, []

        sciezka = []               #zapis sciezki
        aktualny = self.korzen
        while aktualny.prawe_dziecko:   #najwiekszy element znajduje się maksymalnie po prawej stronie
            sciezka.append(aktualny.dane)
            aktualny = aktualny.prawe_dziecko
        sciezka.append(aktualny.dane)   #zapis ostatniego elementu do sciezki

        return aktualny.dane, sciezka
#=====================================================
#USUWANIE DANEGO ELEMENTU
    def usun(self, dane):
        """Metoda usuwająca wierzchołek o podanej wartości."""
        self.korzen = self._usun_wierzcholek(self.korzen, dane)

    def _usun_wierzcholek(self, wierzcholek, dane):
        """Metoda pomocnicza usuwająca wierzchołek o podanej wartości."""
        #dane - które chcemy usunąć
        #wierzchołek - aktualnie sprawdzany wierzchołek

        if wierzcholek is None:
            return None

        if dane < wierzcholek.dane:             #sprawdzanie/szukanie wierzchołka do usunięcia, (zasada prawe większe lewo mniejsze)
            wierzcholek.lewe_dziecko = self._usun_wierzcholek(wierzcholek.lewe_dziecko, dane)
        elif dane > wierzcholek.dane:
            wierzcholek.prawe_dziecko = self._usun_wierzcholek(wierzcholek.prawe_dziecko, dane)
        else:
            if wierzcholek.lewe_dziecko is None:        #jeżeli drzewo ma tylko prawe dziecko - prawe jest następnikiem
                return wierzcholek.prawe_dziecko
            elif wierzcholek.prawe_dziecko is None:     #jeżeli drzewo ma tylko lewe dziecko - lewe jest następnikiem
                return wierzcholek.lewe_dziecko
            else:
                nastepnik, rodzaj = self._nastepnik(wierzcholek)    #jeżeli drzewo ma dwoje dzieci szukamy następnika za pomocą _nastepnik SLAJDY!!!
                wierzcholek.dane = nastepnik.dane             #ustawienie znalezionego nastepnika

                if rodzaj == "prawe":        #po ustawieniu wierzhołka na nastepnik, mamy "duplikat" więc musimy usunąć następnik z drzewa
                    wierzcholek.prawe_dziecko = self._usun_wierzcholek(wierzcholek.prawe_dziecko, nastepnik.dane)
                else:
                    wierzcholek.lewe_dziecko = self._usun_wierzcholek(wierzcholek.lewe_dziecko, nastepnik.dane)

        #aktualizacja wspoczynnika rownowagi wierzcholka
        wierzcholek.wspolczynnik_rownowagi = self.oblicz_wspolczynnik_rownowagi(wierzcholek)

        #rownowazenie drzewa
        self.rownowaz_drzewo()

        return wierzcholek

    def _nastepnik(self, wierzcholek):
        if wierzcholek is None:
            return None

        klucze_in_order = self.in_order(wierzcholek)          #stworzenie listy kluczy "posortowanych"

        lewa_wysokosc = self.oblicz_wysokosc(wierzcholek.lewe_dziecko)      #sprawdzenie lewej i prawej wysokosci by zadecydowac
        prawa_wysokosc = self.oblicz_wysokosc(wierzcholek.prawe_dziecko)    # z ktorej strony wziac następnik (z klucze_in_order)  - potrzebne do balansowania drzewa

        # Znajdowanie indeksu klucza, który ma być usunięty w liscie
        indeks = klucze_in_order.index(wierzcholek.dane)

        if lewa_wysokosc >= prawa_wysokosc and indeks - 1 >= 0:    #jeżeli lewa wys jest większa od prawej to bierzemy następnik z lewego dziecka     ROWNE bo avl może mieć równe wysokosci
            rodzaj = "lewe"                               #rodzaj potrzebny do ifa w funkcji _usun_wierzcholek
            nastepnik_dane = klucze_in_order[indeks - 1]          # -1 - z lewej strony listy
            nastepnik_wezel = self.znajdz_wartosc(nastepnik_dane)
        elif lewa_wysokosc < prawa_wysokosc and indeks + 1 < len(klucze_in_order): #jeżeli prawa wys jest większa od lewej to bierzemy następnik z prawego dziecka
            rodzaj = "prawe"
            nastepnik_dane = klucze_in_order[indeks + 1]     # +1 - z prawej strony listy
            nastepnik_wezel = self.znajdz_wartosc(nastepnik_dane)
        else:
            return None

        return nastepnik_wezel, rodzaj
#
    def znajdz_wartosc(self, wartosc, wierzcholek=None):       #potrzebne do _nastepnik bo zwracał klucz jako wartość a nie obiekt
        if wierzcholek is None:
            wierzcholek = self.korzen       #jeżeli nie podamy żadnego wierzchołka, to automatycznie jest on ustawiany jako korzeń

        if wierzcholek is None:             #sprawdzanie czy wierzchołek jest pusty (czy drzewo jest puste)
            return None

        if wartosc == wierzcholek.dane:     #zwracanie wierzchołka jeżeli został znaleziony
            return wierzcholek

        if wartosc < wierzcholek.dane:                                       #szykanie wierzchołka po drzewie kierując się zasadą;
            return self.znajdz_wartosc(wartosc, wierzcholek.lewe_dziecko)    # większe na prawo, mniejsze na lewo
        else:
            return self.znajdz_wartosc(wartosc, wierzcholek.prawe_dziecko)
#=====================================================
#POST ORDER USUNIECIE DRZEWA
    def post_order(self, wierzcholek):
        if wierzcholek:                #sprawdzenie czy wierzchołek istnieje
            self.post_order(wierzcholek.lewe_dziecko)       #LEWE ---- rekurencyjnie do lewego i prawego dziecka
            self.post_order(wierzcholek.prawe_dziecko)      #PRAWE ---- kolejnosc ma znaczeni bo ---> post-order: lewe poddrzewo, prawe poddrzewo, korzeń
            if wierzcholek.dane:       #KORZEŃ --- jeżeli wierzchołek istnieje to go usuwamy
                print("usunieto: ", str(wierzcholek.dane))
                self.usun(wierzcholek.dane)

#=====================================================
#PODDRZEWO PRE-ORDER
    def pre_order(self, wierzcholek):
        if wierzcholek:                 #pre-order: korzeń, lewe poddrzewo, prawe poddrzewo
            if wierzcholek.dane:       #KORZEŃ
                print(str(wierzcholek.dane), end='-')
                self.pre_order(wierzcholek.lewe_dziecko)  #LEWE
                self.pre_order(wierzcholek.prawe_dziecko)  #PRAWE

    def pre_order_subtree(self, wierzcholek, klucz):
        if wierzcholek is None:  #warunek kończący rekurencje
            return

        if wierzcholek.dane == klucz:  # Jeśli klucz został znaleziony, wypisujemy poddrzewo
            print("Pre-order poddrzewa o korzeniu", klucz, ":")
            self.pre_order(wierzcholek)  # Wywołana metoda pre_order na korzeniu poddrzewa o danym kluczu
            return

        # SZUKANIE - Rekurencyjnie wywołanie pre_order_subtree dla lewego i prawego poddrzewa
        self.pre_order_subtree(wierzcholek.lewe_dziecko, klucz)
        self.pre_order_subtree(wierzcholek.prawe_dziecko, klucz)


#=====================================================
#WYSWIETLADNIE
    def wyswietl(self):                 #pomocnicze do debbugowania
        def pre_order2(wierzcholek):
            if wierzcholek:
                if wierzcholek.dane:
                    print(str(wierzcholek.dane), end='-')
                    pre_order2(wierzcholek.lewe_dziecko)
                    pre_order2(wierzcholek.prawe_dziecko)
        print("Pre-order:")
        pre_order2(self.korzen)

    def in_order(self, wierzcholek):
        kolejnosc = []
        if wierzcholek:
            kolejnosc.extend(self.in_order(wierzcholek.lewe_dziecko))
            if wierzcholek.dane:
                kolejnosc.append(wierzcholek.dane)
            kolejnosc.extend(self.in_order(wierzcholek.prawe_dziecko))
        return kolejnosc

#Obsługa danych wejściowych jako lista

# lista_danych = [8, 2, 5, 14, 10, 12, 13, 6, 9, 1, 4]
# lista_danych = sorted(lista_danych)
# print(lista_danych)
# print("\n--------------------")
# print("WYSWIETLANIE")
# drzewoAVL = AVL()
# drzewoAVL.dodaj_z_listy(lista_danych)
# drzewoAVL.wyswietl()
#
# drzewoAVL.usun(8)
# drzewoAVL.wyswietl()
# print("\n---------------------")





################################################################################
############                                             #######################
############     BUDOWANIE WYKRESOW DRZEW AVL I BST      #######################
############                                             #######################
################################################################################
BST_X_rownowazenie = []
BST_X_in_order = []
BST_X_wyszukiwanie_min = []
BST_X_tworzenie_drzewa = []

AVL_X_rownowazenie = []
AVL_X_in_order = []
AVL_X_wyszukiwanie_min = []
AVL_X_tworzenie_drzewa = []

n = []

for i in range(10, 300, 50):
    random_dane = random_generator(zakres_poczatek, zakres_koniec, i)


    ####################
    drzewoBST = BST()
    ###################
    drzewoBST.dodaj_z_listy(random_dane)

    BST_rownowazenie_start = timeit.default_timer()
    drzewoBST.rownowaz_drzewo()
    BST_rownowazenie_end = timeit.default_timer()

    BST_rownowazenie_DURATION = BST_rownowazenie_end - BST_rownowazenie_start
    BST_X_rownowazenie.append(BST_rownowazenie_DURATION)

    print("bst rownowazenie done")

    # ####################
    # drzewoAVL = AVL()
    # random_dane = sorted(random_dane)
    # ####################
    # drzewoAVL.dodaj_z_listy(random_dane)
    #
    # AVL_rownowazenie_start = timeit.default_timer()
    # drzewoAVL.wyswietl()
    # AVL_rownowazenie_end = timeit.default_timer()
    #
    # AVL_rownowazenie_DURATION = AVL_rownowazenie_end - AVL_rownowazenie_start
    # AVL_X_rownowazenie.append(AVL_rownowazenie_DURATION)
    # print("avl rownowazenie done")
    #
    # # Dodanie wartości do listy n


    n.append(i)


print(n)
print(AVL_X_rownowazenie)
print(BST_X_rownowazenie)

plt.plot(n, BST_X_rownowazenie, color='r', label='BST TWORZENIE')
#plt.plot(n, AVL_X_rownowazenie, color='b', label='AVL TWORZENIE')
plt.legend()
plt.show()