import random
import copy
file_path = 'graf.txt'

#WCZYTYWANIE Z PLIKU MACIERZY SASIEDZTWA
def macierz_sasiedztwa_plik(file_path):
    with open(file_path, 'r') as file:
        num_vertices, num_edges = map(int, file.readline().split())
        graph = [[0] * num_vertices for _ in range(num_vertices)]
        for _ in range(num_edges):
            edge = file.readline().split()  # wczytaj linię i usuń białe znaki z początku i końca
            out, inn = map(int, edge)  # pomijamy pierwszy i ostatni znak "(" i ")"
            graph[out - 1][inn - 1] = 1
            graph[inn - 1][out - 1] = -1
        return graph

#GENERATOR MACIERZY SASIEDZTWA
def macierz_sasiedztwa_generator(liczba_wierzcholkow, liczba_krawedzi):
    #tworzenie pustej macierzy wypelnionej zerami
    matrix = []
    for i in range(liczba_wierzcholkow):
        row = []
        for j in range(liczba_wierzcholkow):
            row.append(0)
        matrix.append(row)

    # Iterujemy się przez wszystkie krawędzie, które chcemy dodać.
    for _ in range(liczba_krawedzi):
        while True:  # Pętla, która będzie powtarzać losowanie, dopóki nie znajdziemy odpowiedniej krawędzi.
            wiersz = random.randint(0, liczba_wierzcholkow - 1)
            kolumna = random.randint(0, liczba_wierzcholkow - 1)
            # Sprawdzamy, czy wylosowana krawędź już istnieje (wartość różna od 0) oraz czy nie tworzy pętli.
            if wiersz != kolumna and matrix[wiersz][kolumna] == 0:
                # Jeśli warunki są spełnione, ustawiamy krawędź między wierzchołkami na 1.
                matrix[wiersz][kolumna] = 1
                matrix[kolumna][wiersz] = -1
                break  # Przerywamy pętlę while i przechodzimy do kolejnej krawędzi.

    return matrix  # Zwracamy wygenerowaną macierz sąsiedztwa.

def macierz_grafu_plik(file_path):
    macierz_sasiedztwa = macierz_sasiedztwa_plik(file_path) #wykorzystanie macierzy sasiedztwa do stworzenia listy nastepnikow, poprzednikow, i incydencji
    graf = []
    for i in range(len(macierz_sasiedztwa)):
        graf.append(macierz_sasiedztwa[i] + [0] * 3)  #stworzenie pustej macierzy grafu wypelnionej 0

    for wiersz in range(len(graf)):             #wyzerowanie macirzy
        for kolumna in range(len(graf[0])):
            graf[wiersz][kolumna] = 0


    nastepniki = []
    for wierzcholek in range(len(macierz_sasiedztwa)):  #przejscie przez wszystkie elementy listy z sasiedztwa
        nastepniki_wierzcholka = []                 #chwilowa lista do przechowywania nastepnikow
        for element in range(len(macierz_sasiedztwa[0])):
            if macierz_sasiedztwa[wierzcholek][element] == 1:      #jezeli 1 to znaczy ze jest nastepnikiem
                nastepniki_wierzcholka.append(element+1)        #dodanie 1 bo chce indeksuje od 1
        nastepniki.append(nastepniki_wierzcholka)

    poprzedniki = []
    for wierzcholek in range(len(macierz_sasiedztwa)):  #przejscie przez wszystkie elementy listy z sasiedztwa
        poprzedniki_wierzcholka = []                 #chwilowa lista do przechowywania poprzednikow
        for element in range(len(macierz_sasiedztwa[0])):
            if macierz_sasiedztwa[wierzcholek][element] == -1:      #jezeli -1 to znaczy ze jest poprzednikiem
                poprzedniki_wierzcholka.append(element+1)        #dodanie 1 bo chce indeksuje od 1
        poprzedniki.append(poprzedniki_wierzcholka)

    brak_incydencji = []
    for wierzcholek in range(len(macierz_sasiedztwa)):  #przejscie przez wszystkie elementy listy z sasiedztwa
        brak_incydencji_wierzcholka = []                 #chwilowa lista do przechowywania poprzednikow
        for element in range(len(macierz_sasiedztwa[0])):
            if macierz_sasiedztwa[wierzcholek][element] == 0:      #jezeli -1 to znaczy ze jest poprzednikiem
                brak_incydencji_wierzcholka.append(element+1)        #dodanie 1 bo chce indeksuje od 1
        brak_incydencji.append(brak_incydencji_wierzcholka)


    """KROK 1"""  # =========================================
    for wiersz in range(len(nastepniki)):            #wypełnienie 3 kolumny od konca pierwszym nastepnikiem
        if nastepniki[wiersz]:
            graf[wiersz][-3] = nastepniki[wiersz][0]

    for i in range(len(macierz_sasiedztwa)):         #sprawdzenie czy istnieje polaczenie vi -> vj
        dl_nastepnik = 1
        for j in range(len(macierz_sasiedztwa[0])):
            if macierz_sasiedztwa[i][j] == 1:        #jezeli tak to zamieniamy miejsce [i,j] na kolejny nastepnik
                if nastepniki[i]:       #jezeli istnieje nastepnik
                    if len(nastepniki[i]) > 1 and dl_nastepnik < len(nastepniki[i]):      #jezeli lista nastepnikow jest wieksza od 1 to bierzemy drugi z koleji
                        graf[i][j] = nastepniki[i][dl_nastepnik]
                        dl_nastepnik += 1
                    else:
                        graf[i][j] = nastepniki[i][-1] #jezeli nie to bierzemy pierwszy

    """KROK 2"""  # =========================================
    for wiersz in range(len(poprzedniki)):            #wypełnienie 2 kolumny od konca pierwszym poprzednikiem
        if poprzedniki[wiersz]:
            graf[wiersz][-2] = poprzedniki[wiersz][0]


    for g in range(len(macierz_sasiedztwa)):         #sprawdzenie czy istnieje polaczenie vj -> vi
        dl_poprzednik = 1
        for j in range(len(macierz_sasiedztwa[0])):
            if macierz_sasiedztwa[g][j] == -1:        #jezeli tak to zamieniamy miejsce [i,j] na kolejny poprzednik + liczba wierzcholkow
                if poprzedniki[g]:       #jezeli istnieje poprzednik
                    if len(poprzedniki[g]) > 1 and dl_poprzednik < len(poprzedniki[g]):      #jezeli lista poprzednikow jest wieksza od 1 to bierzemy drugi z koleji
                        graf[g][j] = poprzedniki[g][dl_poprzednik] + len(graf)
                        dl_poprzednik += 1
                    else:
                        graf[g][j] = poprzedniki[g][-1] + len(graf) #jezeli nie to bierzemy pierwszy
    """KROK 3"""  # =========================================
    for wiersz in range(len(brak_incydencji)):            #wypełnienie 2 kolumny od konca pierwszym poprzednikiem
        if brak_incydencji[wiersz]:
            graf[wiersz][-1] = brak_incydencji[wiersz][0]


    for i in range(len(macierz_sasiedztwa)):         #sprawdzenie czy nie istnieje polaczenie vi -> vj
        dl_incydencji = 1
        for j in range(len(macierz_sasiedztwa[0])):
            if macierz_sasiedztwa[i][j] == 0:        #jezeli tak to zamieniamy miejsce [i,j] na kolejny z brak_incydencji
                if brak_incydencji[i]:       #jezeli istnieje brak_incydencji
                    if len(brak_incydencji[i]) > 1 and dl_incydencji < len(brak_incydencji[i]):      #jezeli lista brak_incydencji jest wieksza od 1 to bierzemy drugi z koleji
                        graf[i][j] = -brak_incydencji[i][dl_incydencji]
                        dl_incydencji += 1
                    else:
                        graf[i][j] = -brak_incydencji[i][-1]  #jezeli nie to bierzemy pierwszy

    return graf, poprzedniki

"""MACIERZ SASIEDZTWA ALGORYTMY"""#=====================================================================================
def Kahn_ms(matrix):
    result = []  # Lista, która będzie przechowywać wynik sortowania topologicznego.
    in_degree = [0] * len(matrix)  # Lista, która przechowuje stopnie wejścia dla każdego wierzchołka.

    # Obliczanie stopni wejścia dla każdego wierzchołka.
    for i in range(len(matrix)):
        for j in range(len(matrix)):
            if matrix[i][j] == -1:
                in_degree[i] += 1

    in_degree_none = []  # Lista, która będzie przechowywać indeksy wierzchołków o stopniu wejścia równym zero.

    # Przeglądanie listy stopni wejścia, aby znaleźć wierzchołki o stopniu wejścia równym zero.
    for i in range(len(in_degree)):
        if in_degree[i] == 0:
            in_degree_none.append(i)

    # Główna pętla sortowania topologicznego.
    while len(in_degree_none) > 0:
        sorted_element = in_degree_none[0]  # Wybierz pierwszy element z listy wierzchołków o stopniu wejścia równym zero.
        result.append(sorted_element+1)  # Dodaj ten element do wyniku.
        in_degree_none.remove(sorted_element)  # Usuń ten element z listy wierzchołków o stopniu wejścia równym zero.

        # Zmniejsz stopień wejścia dla sąsiadów wybranego wierzchołka i dodaj do listy wierzchołków o stopniu wejścia równym zero, jeśli ich stopień wejścia staje się równy zero.
        for i in range(len(matrix)):
            if matrix[sorted_element][i] == 1:
                in_degree[i] -= 1   #obnizamy stopien wejsciowy sąsiadów
                if in_degree[i] == 0:   #jeżeli stopien wejsciowy sasiada rowny zero to dodajemy go do kolejki
                    in_degree_none.append(i)
                    in_degree_none.sort() #posortowanie

    # Sprawdzenie, czy graf zawiera cykl. Jeśli nie, zwróć wynik sortowania topologicznego. W przeciwnym razie zwróć komunikat o błędzie.
    else:
        for num in in_degree:
            if num != 0:
                return "Graf zawiera cykl. Sortowanie niemożliwe."
        return result

#============================DFS===================
def czyaktywny(matrix):       #stworzenie czyaktywny = [0,0,0,0,0]
    res = []
    for i in range(len(matrix)):
        res.append(1)
    return res
DFS_matrix = macierz_sasiedztwa_plik(file_path)         #pomocnicze zmienne globalne
CzyAktywny = czyaktywny(DFS_matrix)
wynik_dfs =[]
stopien_stacka = 0

def DFS_ms():
    global CzyAktywny, stopien_stacka
    for i in range(len(DFS_matrix)):        #znalezienie pierwszej krawedzi wierzcholka
        if CzyAktywny[i] == 1:
            Nastepnik(i)
def Nastepnik(wierzcholek):
    global stopien_stacka
    wynik_dfs.append(wierzcholek)   #1.dodanie wierzcholka do wyniku
    CzyAktywny[wierzcholek] = 0     #2.zmiana aktywnosci wierzcholka
    print(wynik_dfs[-1]+1)
    stopien_stacka += 1             #zmiana stopnia stacka
    for i in range(len(DFS_matrix)):    #znalezienie kolejnego aktywnego wierzczholka ktory jest aktywny i rekurencyjne znalezienie nastepnika
        if DFS_matrix[wierzcholek][i] == 1 and CzyAktywny[i] == 1:
            Nastepnik(i)

"""MACIERZ GRAFU ALGORYTMY"""#=====================================================================================

def Kahs_mg(matrix, poprzedniki):
    aktywny = []
    for i in range(len(matrix)):    #stworzenie listy [1,1,1,1] gdzie 1 oznacza aktywnosc wierzcholka
        aktywny.append(1)

    stopnie = []
    for i in range(len(poprzedniki)):   #stworzenie listy wypelnionej stopniami wierzcholkow o odpowiednim indeksie
        stopien = 0
        for j in range(len(poprzedniki[i])):    #za pomoca listy poprzednikow
            stopien += 1
        stopnie.append(stopien)

    res = []
    CzyAktywne = True       #warunek konczoncy petle while
    while(CzyAktywne):
        for i in range(len(stopnie)):       #przejscie przez wszystkie stopnie
            if stopnie[i] == 0 and aktywny[i] == 1:  #znalezenie pierwszego aktywnego o stopniu rownym 0
                res.append(i+1)     #dodanie do wyniku wierzcholka
                aktywny[i] =0       #zmiana aktywnosci na 0
                for j in range(len(poprzedniki)):
                    for k in range(len(poprzedniki[j])):   #przejscie przez wszystkie poprzedniki wierzcholkow
                        if poprzedniki[j][k] == i+1:       #jezeli wierzczholek ma poprzednik jako wczesniej sprawdzany wierzczholek
                            stopnie[j] -=1                #obnizamy jego stopien o jeden

        czywszystkie = True         #czy mozna zakonczyc petle while
        for l in range(len(stopnie)):   #czy wszystkie stopnie sa rowne zero, wszystkie musza byc nie aktywne
            if stopnie[l] == 0 and aktywny[l] == 0 and czywszystkie == True:
                czywszystkie = True
            else:
                czywszystkie = False
        if czywszystkie == True:
            break
        elif len(matrix) < len(res):
            print("Graf zawiera cykl")
            break

    return res

#=====DFS=====================================




#[[0,1,-1,0,-1],[-1,0,-1,1,1],[1,1,0,-1,0],[0,-1,1,0,-1],[1,-1,0,1,0]]
#=====================================================================
print("=======MS========")
# Testowanie dla generatora macierzy grafu
graph = macierz_sasiedztwa_generator(5,8)
# Testowanie dla wczytywania z pliku
graph_matrix = macierz_sasiedztwa_plik(file_path)

print("z generatora MS: ", graph)
print("z pliku MS: ", graph_matrix)
print("\n=======MG========")
macierz_grafu, poprzedniki = macierz_grafu_plik(file_path)
print(macierz_grafu)


#=======KAHN MACIERZ SASIEDZTWA=======:
print("\n=======kahn MS========")
kahn = Kahn_ms(graph_matrix)
print(kahn)

#=======DFS MACIERZ SASIEDZTWA=======:
print("\n=======dfs MS========")
DFS_ms()

#=======KAHN MACIERZ GRAFU=======:
print("\n=======kahn MG========")
kahn_mg = Kahs_mg(macierz_grafu, poprzedniki)
print(kahn_mg)

#=======DFS MACIERZ GRAFU=======:
print("\n=======DFS MG========")
