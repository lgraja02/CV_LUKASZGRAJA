import random
import copy
import timeit
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
            graph[inn - 1][out - 1] = 1
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
                matrix[kolumna][wiersz] = 1
                break  # Przerywamy pętlę while i przechodzimy do kolejnej krawędzi.

    return matrix  # Zwracamy wygenerowaną macierz sąsiedztwa.


# def lista_nastepnikow_konw(macierz_sasiedztwa):
#     nastepniki = []
#     for wierzcholek in range(len(macierz_sasiedztwa)):  # przejscie przez wszystkie elementy listy z sasiedztwa
#         nastepniki_wierzcholka = []  # chwilowa lista do przechowywania nastepnikow
#         for element in range(len(macierz_sasiedztwa[0])):
#             if macierz_sasiedztwa[wierzcholek][element] == 1:  # jezeli 1 to znaczy ze jest nastepnikiem
#                 nastepniki_wierzcholka.append(element + 1)  # dodanie 1 bo chce indeksuje od 1
#         nastepniki.append(nastepniki_wierzcholka)
#     return nastepniki

def lista_nastepnikow_plik(file_path):
    with open(file_path, 'r') as file:
        num_vertices, num_edges = map(int, file.readline().split())
        nastepniki = [[] for _ in range(num_vertices)]  # Tworzymy listę następników dla każdego wierzchołka

        for _ in range(num_edges):
            edge = file.readline().split()  # Wczytujemy linię krawędzi
            out, inn = map(int, edge)
            if out < 1 or out > num_vertices or inn < 1 or inn > num_vertices:
                raise ValueError("Indeks wierzchołka poza zakresem")
            nastepniki[out - 1].append(inn)  # Dodajemy następnika do odpowiedniego wierzchołka (indeks - 1)

    return nastepniki


#================"""CYKL HAMILTONA  NIESKIEROWANY SASIEDZTWA =======================
def czy_mozna_dodac(v, pozycja, sciezka, graf):
    # Sprawdzamy, czy ten wierzchołek jest sąsiednim wierzchołkiem do ostatnio dodanego wierzchołka
    if graf[sciezka[pozycja - 1]][v] == 0:
        return False

    # Sprawdzamy, czy wierzchołek nie został już dodany do ścieżki
    if v in sciezka:
        return False

    return True

def cykl_hamiltona_util(graf, sciezka, pozycja):
    # Przypadek bazowy: jeśli wszystkie wierzchołki są już w ścieżce
    if pozycja == len(graf):
        # Sprawdzamy, czy istnieje krawędź z ostatniego wierzchołka do pierwszego
        if graf[sciezka[pozycja - 1]][sciezka[0]] == 1:
            return True
        else:
            return False

    # Próbujemy różne wierzchołki jako następne w cyklu Hamiltona
    # Nie próbujemy pierwszego wierzchołka, ponieważ wiemy, że jest już w ścieżce
    for v in range(1, len(graf)):
        if czy_mozna_dodac(v, pozycja, sciezka, graf):
            sciezka[pozycja] = v

            if cykl_hamiltona_util(graf, sciezka, pozycja + 1) == True:
                return True

            # Usuwamy bieżący wierzchołek, jeśli nie prowadzi do rozwiązania
            sciezka[pozycja] = -1

    return False

def cykl_hamiltona(graf):
    sciezka = [-1] * len(graf)
    # Umieszczamy wierzchołek 0 jako pierwszy wierzchołek w ścieżce. Jeśli istnieje cykl Hamiltona,
    # to ścieżka może się zacząć od dowolnego punktu cyklu, ponieważ graf jest nieskierowany.
    sciezka[0] = 0

    if not cykl_hamiltona_util(graf, sciezka, 1):
        print("Cykl Hamiltona nie istnieje\n")
        return False
    else:
        # Zwiększamy wszystkie wartości o 1, aby poprawnie wyświetlić wynik (indeksowanie od 1)
        for i in range(len(sciezka)):
            sciezka[i] += 1
        print("Cykl Hamiltona: ", sciezka)
        return True
#================"""CYKL EULERA NIESKIEROWANY SASIEDZTWA =======================
def stopien_wierzcholka(graf):
    # Funkcja oblicza stopień każdego wierzchołka w grafie
    return [sum(row) for row in graf]

def jest_spojny(graf):
    # Funkcja sprawdza, czy graf jest spójny

    # Inicjalizujemy listę odwiedzonych wierzchołków
    visited = [False] * len(graf)

    # Funkcja DFS (przeszukiwanie w głąb) dla sprawdzania spójności
    def dfs(v):
        visited[v] = True
        # Przechodzimy przez wszystkie wierzchołki
        for i in range(len(graf)):
            if graf[v][i] == 1 and not visited[i]:
                dfs(i)

    # Uruchamiamy DFS z pierwszego znalezionego wierzchołka, który ma krawędzie
    for i in range(len(graf)):
        if any(graf[i]):
            dfs(i)
            break

    # Sprawdzamy, czy wszystkie wierzchołki są odwiedzone lub izolowane
    return all(visited[i] or not any(graf[i]) for i in range(len(graf)))

def znajdz_cykl_eulera(graf):
    # Funkcja znajduje cykl Eulera w grafie

    # Sprawdzamy, czy graf jest spójny
    if not jest_spojny(graf):
        print("Graf nie jest spójny")
        return False

    # Obliczamy stopnie wierzchołków
    stopnie = stopien_wierzcholka(graf)
    # Sprawdzamy, czy każdy wierzchołek ma parzysty stopień
    if any(stopien % 2 != 0 for stopien in stopnie):
        print("Graf ma wierzchołek o nieparzystym stopniu")
        return False

    # Funkcja znajduje cykl Eulera zaczynając od wierzchołka v
    def znajdz_cykl(v):
        stos = [v]  # Stos używany do przechowywania bieżącej ścieżki
        cykl = []  # Lista przechowująca cykl Eulera

        while stos:
            u = stos[-1]
            # Szukamy sąsiedniego wierzchołka z krawędzią
            for w in range(len(graf)):
                if graf[u][w] == 1:
                    graf[u][w] = graf[w][u] = 0  # Usuwamy krawędź z grafu
                    stos.append(w)  # Dodajemy wierzchołek do stosu
                    break
            else:
                cykl.append(stos.pop())  # Dodajemy wierzchołek do cyklu, jeśli brak sąsiadów

        return cykl

    # Znajdujemy cykl Eulera zaczynając od wierzchołka 0
    cykl = znajdz_cykl(0)
    # Zwiększamy każdy wierzchołek o 1, aby indeksowanie zaczynało się od 1
    for i in range(len(cykl)):
        cykl[i] += 1
    print("Cykl Eulera: ", cykl)
    return True

#================"""CYKL HAMILTONA SKIEROWANY NASTEPNIKÓW=======================
def cykl_hamiltona_lista_nastepnikow(lista_nastepnikow):
    # Inicjalizacja listy odwiedzonych wierzchołków
    odwiedzone = [False] * len(lista_nastepnikow)
    # Inicjalizacja listy przechowującej aktualną ścieżkę
    sciezka = []

    # Funkcja DFS (przeszukiwanie w głąb) dla znajdowania cyklu Hamiltona
    def dfs(v, odwiedzone, sciezka):
        # Dodanie bieżącego wierzchołka do ścieżki
        sciezka.append(v)
        # Oznaczenie bieżącego wierzchołka jako odwiedzony
        odwiedzone[v - 1] = True

        # Warunek zakończenia DFS: jeśli długość ścieżki jest równa liczbie wierzchołków,
        # sprawdzamy, czy istnieje krawędź z ostatniego wierzchołka ścieżki do pierwszego wierzchołka
        if len(sciezka) == len(lista_nastepnikow):
            if sciezka[0] in lista_nastepnikow[v - 1]:
                sciezka.append(sciezka[0])
                print("Cykl Hamiltona:", sciezka)
                return True
            else:
                sciezka.pop()
                odwiedzone[v - 1] = False
                return False

        # Rekurencyjnie kontynuujemy DFS dla wszystkich sąsiadów bieżącego wierzchołka
        for sasiad in lista_nastepnikow[v - 1]:
            if not odwiedzone[sasiad - 1]:
                if dfs(sasiad, odwiedzone, sciezka):
                    return True

        # Po zakończeniu rekurencji dla danego wierzchołka, usuwamy go ze ścieżki i oznaczamy jako nieodwiedzony
        sciezka.pop()
        odwiedzone[v - 1] = False
        return False

    # Rozpoczynamy DFS dla każdego wierzchołka grafu
    for start in range(1, len(lista_nastepnikow) + 1):
        sciezka = []
        odwiedzone = [False] * len(lista_nastepnikow)
        if dfs(start, odwiedzone, sciezka):
            return True

    # Jeśli nie znaleziono cyklu Hamiltona, wyświetlamy komunikat
    print("Cykl Hamiltona nie istnieje")
    return False
#================"""CYKL EULERA SKIEROWANY NASTEPNIKÓW=======================
# nastepniki [[2], [3], [4], [5, 8], [6], [1], [4], [7]]
# krawedzie: [[[1, 2, True]], [[2, 3, True]], [[3, 4, True]], [[4, 5, True], [4, 8, True]], [[5, 6, True]], [[6, 1, True]], [[7, 4, True]], [[8, 7, True]]]
pierwszy = 1
def dfs_euler(v, krawedzie, stack, ilosc_krawedzi, gl_len):
    # Dodaj bieżący wierzchołek do stosu
    stack.append(v)
    global pierwszy

    # Sprawdzenie warunku na cykl Eulera
    if gl_len == ilosc_krawedzi:
        # Jeśli ilość odwiedzonych krawędzi jest równa całkowitej liczbie krawędzi,
        # sprawdź, czy zakończyliśmy cykl wierzchołkiem początkowym
        if v == pierwszy:
            print("cykl eulera: ", stack)
        # Zdejmij bieżący wierzchołek ze stosu i zakończ funkcję
        stack.pop()
        return

    # Przejście po krawędziach bieżącego wierzchołka
    for krawedz in krawedzie[v - 1]:
        if krawedz[2]:  # Jeśli krawędź jest aktywna
            # Dezaktywuj krawędź, aby oznaczyć jej odwiedzenie
            krawedz[2] = False
            # Rekurencyjnie wywołaj dfs_euler dla następnego wierzchołka
            dfs_euler(krawedz[1], krawedzie, stack, ilosc_krawedzi, gl_len + 1)
            # Ponownie aktywuj krawędź (backtrack), aby umożliwić inne ścieżki
            krawedz[2] = True

    # Zdejmij bieżący wierzchołek ze stosu po przejściu przez wszystkie krawędzie
    stack.pop()
def cykl_eulera_lista_nastepnikow(lista_nastepnikow):
    krawedzie = []  # Stworzenie listy krawędzi
    ilosc_krawedzi = 0
    for i in range(len(lista_nastepnikow)):
        krawedzie_wierzcholka = []
        for j in range(len(lista_nastepnikow[i])):
            krawedz = []
            krawedz.append(i + 1)  # Numer wierzchołka początkowego
            krawedz.append(lista_nastepnikow[i][j])  # Numer wierzchołka końcowego
            krawedz.append(True)  # Początkowo krawędź jest aktywna
            krawedzie_wierzcholka.append(krawedz)
            ilosc_krawedzi += 1  # Zwiększ liczbę krawędzi
        krawedzie.append(krawedzie_wierzcholka)  # Dodaj listę krawędzi do listy krawędzi

    global pierwszy  # Ustaw wierzchołek początkowy na pierwszy wierzchołek z listy następników
    pierwszy = krawedzie[0][0][0]

    # Rozpocznij przeszukiwanie dfs_euler od wierzchołka początkowego
    dfs_euler(pierwszy, krawedzie, [], ilosc_krawedzi, 0)

    x = "CYKL EULERA NIE ISTNIEJE"

    return krawedzie, x  # Zwróć listę krawędzi po zakończeniu przeszukiwania

#============================================================================
"""#######################################################################"""
graph_matrix = macierz_sasiedztwa_plik(file_path)
print("\nsasiedztwa", graph_matrix)

lista_nastepnikow = lista_nastepnikow_plik(file_path)
print("\nnastepniki",lista_nastepnikow)

"""#######################################################################"""
print("\n===SASIEDZTWA NIESKIEROWANY===")
#====CYKL HAMILTONA SASIEDZTWA====
cykl_hamiltona(graph_matrix)
#====CYKL EULERA SASIEDZTWA====
znajdz_cykl_eulera(graph_matrix)

"""#######################################################################"""
print("\n===LISTA NASTEPNIKOW SKIEROWANY===")
#===CYKL HAMILTONA NASTEPNIKI====
cykl_hamiltona_lista_nastepnikow(lista_nastepnikow)

#===CYKL EULERA NASTEPNIKI====
x = cykl_eulera_lista_nastepnikow(lista_nastepnikow)
print(x)