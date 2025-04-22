import itertools
import copy

file_path = 'przedmioty.txt'
def przedmioty_plik(file_path):
    with open(file_path, 'r') as file:
        liczba_przedmiotow, pojemnosc = map(int, file.readline().split())
        przedmioty = []
        for _ in range(liczba_przedmiotow):
            przedmiot1 = []
            line = file.readline().split()
            rozmiar, waga = map(int, line)
            przedmiot1.append(rozmiar)
            przedmiot1.append(waga)
            przedmioty.append(przedmiot1)
        return pojemnosc, przedmioty

#===========================================================================================================
"""WCZYTANIE DANYCH"""
pojemnosc, przedmioty = przedmioty_plik(file_path)
print("POJEMNOSC: ",pojemnosc, "   \nPRZEDMIOTY: ", przedmioty)

#========================ALGORYTM ZACHLANNY III   WSPOLCZYNNIK OPLACALNOSCI==================================
#rozmiar wartosc [2, 4]
def zachlanny(przedmioty1, pojemnosc_plecaka):
    przedmioty = copy.deepcopy(przedmioty1)

    # Dodaj wartość na jednostkę masy do każdej z list
    for przedmiot in przedmioty:
        wjm = przedmiot[1] / przedmiot[0]  # Oblicz wartość na jednostkę masy (wartość / rozmiar)
        przedmiot.append(wjm)  # Dodaj tę wartość jako trzeci element w każdej zagnieżdżonej liście

    # Posortuj przedmioty względem wartości na jednostkę masy malejąco
    posortowane_przedmioty = sorted(przedmioty, key=lambda x: x[2], reverse=True)  # Sortuj według wartości na jednostkę masy (trzecia wartość w każdej liście), malejąco

    plecak = []                           # Lista do przechowywania wybranych przedmiotów
    waga_w_plecaku = 0                    # Całkowita waga przedmiotów w plecaku
    wartosc_w_plecaku = 0                 # Całkowita wartość przedmiotów w plecaku
    dostepne_miejsce = pojemnosc_plecaka  # Dostępne miejsce w plecaku

    for przedmiot in posortowane_przedmioty:    # Przejdź przez posortowaną listę przedmiotów
        if przedmiot[0] <= dostepne_miejsce:    # Jeśli przedmiot mieści się w pozostałym miejscu plecaka
            plecak.append(przedmiot)            # Dodaj przedmiot do plecaka
            dostepne_miejsce -= przedmiot[0]    # Zmniejsz dostępne miejsce w plecaku o wagę przedmiotu
            waga_w_plecaku += przedmiot[0]      # Dodaj wagę przedmiotu do całkowitej wagi w plecaku
            wartosc_w_plecaku += przedmiot[1]   # Dodaj wartość przedmiotu do całkowitej wartości w plecaku
        elif dostepne_miejsce == 0:             # Jeśli nie ma już dostępnego miejsca w plecaku
            break  # Przerwij pętlę

    return wartosc_w_plecaku, waga_w_plecaku,  plecak  # Zwróć listę wybranych przedmiotów, całkowitą wagę, pozostałe dostępne miejsce i całkowitą wartość


#=====================================   SILOWY  ==================================================================
# Funkcja sumująca wartość (wartosc) i wagę (waga) dla listy przedmiotów (przedmioty)
def sum_rozwiazan(przedmioty):
    wartosc, waga = 0, 0             # Inicjalizacja zmiennych przechowujących łączną wartość i wagę
    for przedm in przedmioty:        # Iteracja przez każdy przedmiot w rozwiązaniu
        wartosc += przedm[1]         # Dodaj wartość przedmiotu do łącznej wartości
        waga += przedm[0]            # Dodaj wagę przedmiotu do łącznej wagi
    return wartosc, waga             # Zwróć łączną wartość i wagę jako krotkę (wartosc, waga)

# Funkcja rozwiązująca problem plecakowy metodą siłową
def silowy(pojemnosc_plecaka, przedmioty):
    res = []  # Inicjalizacja listy do przechowywania możliwych rozwiązań

    # Iteracja przez wszystkie możliwe liczby przedmiotów (od 0 do liczby przedmiotów)
    for przedmiot in range(len(przedmioty) + 1):
        # Generowanie wszystkich możliwych kombinacji 'przedmiot' przedmiotów
        for rozwiazania in itertools.combinations(przedmioty, przedmiot):
            # Oblicz łączną wartość i wagę dla danej kombinacji przedmiotów
            wartosc, waga = sum_rozwiazan(rozwiazania)
            # Sprawdź, czy łączna waga jest mniejsza lub równa pojemności plecaka
            if waga <= pojemnosc_plecaka:
                # Jeśli tak, dodaj kombinację do listy rozwiązań
                res.append((wartosc, waga, rozwiazania))

    # Sortuj listę rozwiązań w porządku malejącym według łącznej wartości
    res.sort(reverse=True, key=lambda x: x[0])

    # Zwróć posortowaną listę rozwiązań
    return res
#=====================================   DYNAMICZNY  ==================================================================
def dynamiczny(pojemnosc_plecaka, przedmioty):
    n = len(przedmioty)
    # Inicjalizacja tablicy dp o wymiarach (n+1) x (pojemnosc_plecaka+1) wypełnionej zerami
    # +1 bo kolumny z 0 pozwala na przechowywanie wyników dla przypadków gdy mamy 0 przedmiotów
    dp = [[0] * (pojemnosc_plecaka + 1) for _ in range(n + 1)]

    # Przechodzenie przez każdy przedmiot
    for i in range(1, n + 1):
        # Przechodzenie przez każdą możliwą wagę plecaka od 1 do pojemnosc_plecaka
        for w in range(1, pojemnosc_plecaka + 1):
            # Sprawdzenie, czy aktualny przedmiot może być dodany do plecaka (czy jego waga jest mniejsza lub równa bieżącej pojemności)
            if przedmioty[i - 1][0] <= w:
                # Wybór maksymalnej wartości między:
                # 1. Nie dodaniem aktualnego przedmiotu (wartość bez tego przedmiotu)
                # 2. Dodaniem aktualnego przedmiotu (wartość z uwzględnieniem tego przedmiotu)
                #max{𝑉[𝑖 − 1,𝑗] , 𝑉[𝑖 − 1,𝑗 − 𝑤𝑖] + 𝑝𝑖}
                dp[i][w] = max(dp[i - 1][w], dp[i - 1][w - przedmioty[i - 1][0]] + przedmioty[i - 1][1])
            else:
                # Jeśli przedmiot nie może być dodany, zachowujemy poprzednią wartość (bez tego przedmiotu)
                dp[i][w] = dp[i - 1][w]

    # Zwrócenie maksymalnej wartości plecaka (znajduje się w dp[n][pojemnosc_plecaka])
    # oraz całej tablicy dp do dalszej analizy lub debugowania
    return dp[n][pojemnosc_plecaka], dp

#========================================================================
"""ROZWIAZANIA"""

x = zachlanny(przedmioty, pojemnosc)
print("\n==========================\nZACHLANNY: \n", x)

y = silowy(pojemnosc, przedmioty)
print("\n==========================\nSILOWY: ")
for wynik in y:
    print(wynik)

z = dynamiczny(pojemnosc, przedmioty)
print("\n=======================\nDYNAMICZNY: ", z)
