import random
import matplotlib.pyplot as plt
import timeit
import sys
import os
os.system('ulimit -s unlimited; some_executable')
sys.setrecursionlimit(10000000)

def random_generator(zakres_poczatek, zakres_koniec, ilosc_liczb):
    random_numbers = []
    Num = random.randint(zakres_poczatek,zakres_koniec)
    random_numbers.append(Num)
    for i in range(ilosc_liczb-1):
        tmp = random.randint(zakres_poczatek,zakres_koniec)
        random_numbers.append(tmp)
    return random_numbers


def random_increase_generator(ilosc_liczb):
    random_numbers = []
    Num = random.randint(0,10000)
    random_numbers.append(Num)
    for i in range(ilosc_liczb-1):
        tmp = random_numbers[i] + random.randint(0,100)
        random_numbers.append(tmp)
    return random_numbers

def random_decrease_generator(ilosc_liczb):
    random_numbers = []
    Num = random.randint(0, 100000)
    random_numbers.append(Num)
    for i in range(ilosc_liczb - 1):
        tmp = random_numbers[i] - random.randint(0, 100)
        random_numbers.append(tmp)
    return random_numbers

def random_Ashape_generator(ilosc_liczb):
    First_Half = ilosc_liczb//2
    Sec_Half = ilosc_liczb-First_Half
    random_numbers = []
    Num = random.randint(0,10000)
    random_numbers.append(Num)
    for i in range(First_Half-1):
        tmp = random_numbers[-1] + random.randint(1,100)
        random_numbers.append(tmp)
    for j in range(Sec_Half):
        tmp = random_numbers[-1] - random.randint(1,100)
        random_numbers.append(tmp)
    return random_numbers

def random_Vshape_generator(ilosc_liczb):
    First_Half = ilosc_liczb//2
    Sec_Half = ilosc_liczb-First_Half
    random_numbers = []
    Num = random.randint(0,10000)
    random_numbers.append(Num)
    for i in range(First_Half-1):
        tmp = random_numbers[-1] - random.randint(1,100)
        random_numbers.append(tmp)
    for j in range(Sec_Half):
        tmp = random_numbers[-1] + random.randint(1,100)
        random_numbers.append(tmp)
    return random_numbers

#####################
zakres_poczatek = 0
zakres_koniec = 1000000
ilosc_liczb = 10
#####################

wylosowane_liczby_random = random_generator(zakres_poczatek, zakres_koniec, ilosc_liczb)
wylosowane_liczby_rising = random_increase_generator(ilosc_liczb)
wylosowane_liczby_decrease = random_decrease_generator(ilosc_liczb)
wylosowane_liczby_Aksztaltne = random_Ashape_generator(ilosc_liczb)
wylosowane_liczby_Vksztaltne = random_Vshape_generator(ilosc_liczb)



print("Wylosowane liczby random:", wylosowane_liczby_random)
print("Wylosowane liczby rosnace:", wylosowane_liczby_rising)
print("Wylosowane liczby malejoce:", wylosowane_liczby_decrease)
print("Wylosowane liczby Aksztaltne:", wylosowane_liczby_Aksztaltne)
print("Wylosowane liczby Vksztaltne:", wylosowane_liczby_Vksztaltne)
#==================================================================
def bubble_sort(liczby=[]):
    num_comparisons = 0

    for i in range(len(liczby) - 1):
        is_swap = False
        for j in range(len(liczby) - 1 - i):
            num_comparisons += 1
            if liczby[j] < liczby[j + 1]:
                num_comparisons += 1
                tmp = liczby[j + 1]
                liczby[j + 1] = liczby[j]
                liczby[j] = tmp
                is_swap = True

        if not is_swap:
            break

    return liczby, num_comparisons

#==================================================================
def insertion_sort(liczby=[]):
    num_comparisons = 0

    for i in range(1, len(liczby)):
        key = liczby[i]
        j = i - 1

        while j >= 0 and liczby[j] < key:
            liczby[j + 1] = liczby[j]
            j -= 1
            num_comparisons += 1

        liczby[j + 1] = key
        num_comparisons += 1

    return liczby, num_comparisons

#==================================================================
def selection_sort(liczby=[]):
    num_comparisons = 0


    for i in range(len(liczby) - 1):
        minindex = i

        for j in range(i + 1, len(liczby)):
            if liczby[j] > liczby[minindex]:
                minindex = j
                num_comparisons += 1

        liczby[i], liczby[minindex] = liczby[minindex], liczby[i]
        num_comparisons += 1

    return liczby, num_comparisons
#==================================================================

# def quick_sort(lista=[], IndeksMaxLeft=0, IndeksMinRight=0):
#     if IndeksMaxLeft < IndeksMinRight:
#         q = partition(lista, IndeksMaxLeft, IndeksMinRight)
#         quick_sort(lista, IndeksMaxLeft, q)
#         quick_sort(lista, q + 1, IndeksMinRight)
#     return lista

# def partition(lista=[], IndeksMaxLeft=0, IndeksMinRight=0):
#     pivot = lista[IndeksMinRight - 1]
#     i = IndeksMaxLeft
#     j = IndeksMinRight - 2
#
#     while True:
#         while i <= j and lista[i] >= pivot:
#             i += 1
#         while i <= j and lista[j] <= pivot:
#             j -= 1
#         if i < j:
#             lista[i], lista[j] = lista[j], lista[i]
#             i += 1
#             j -= 1
#         else:
#             lista[i], lista[IndeksMinRight - 1] = lista[IndeksMinRight - 1], lista[i]
#             return i
#==================================================================

def quick_sort(array, x):
    """Sort the array by using quicksort."""
    global comparisons
    less = []
    equal = []
    greater = []

    if len(array) > 1:
        if x == 'right':
            pivot = array[len(array)-1]
        else:
            pivot = array[len(array) // 2]
        for x in array:
            comparisons += 1
            if x < pivot:
                greater.append(x)
            elif x == pivot:
                equal.append(x)
            elif x > pivot:
                less.append(x)
        return quick_sort(less, x) + equal + quick_sort(greater, x)  # Just use the + operator to join lists
    # Note that you want equal ^^^^^ not pivot
    else:  # You need to handle the part at the end of the recursion - when you only have one element in your array, just return the array.
        return array
#=======================================================================================
def merge_sort(list_to_sort):
    global comparisons
    if len(list_to_sort) > 1:  # lista do sortowania musi mieć więcej niż jeden element
        division_point = len(list_to_sort) // 2  # ustalenie punktu podziału w połowie listy
        # podzelenie listy na dwie części
        left_side = list_to_sort[:division_point]
        right_side = list_to_sort[division_point:]

        # sortowanie obu połówek
        merge_sort(left_side)
        merge_sort(right_side)

        # scalanie posortowanych połówek w jedną listę
        i = j = k = 0  # i - indeks lewej połówki, j - indeks prawej połówki, k - indeks listy wynikowej

        while i < len(left_side) and j < len(right_side):
            comparisons += 1
            # sprawdzenie który z elementów obu list, na które wskazują indexy jest mniejszy
            # wstawienie go w oznaczone miejsce listy wynikowej i przesunięcie wykorzystanych indexów
            if left_side[i] >= right_side[j]:
                list_to_sort[k] = left_side[i]
                i += 1
            else:
                list_to_sort[k] = right_side[j]
                j += 1
            k += 1

        # dodanie pozostałych elementów z lewej połówki, jeśli istnieją
        while i < len(left_side):
            comparisons +=1
            list_to_sort[k] = left_side[i]
            i += 1
            k += 1
        # dodanie pozostałych elementów z prawej połówki, jeśli istnieją
        while j < len(right_side):
            comparisons += 1
            list_to_sort[k] = right_side[j]
            j += 1
            k += 1
    return list_to_sort

#=============================================================================
def heapify(arr, n, i):
    global comparisons
    largest = i  # Initialize largest as root
    l = 2 * i + 1  # left = 2*i + 1
    r = 2 * i + 2  # right = 2*i + 2

    # See if left child of root exists and is
    # greater than root
    if l < n and arr[l] < arr[largest]:
        comparisons += 1
        largest = l

    # See if right child of root exists and is
    # greater than root
    if r < n and arr[r] < arr[largest]:
        comparisons += 1
        largest = r

    # Change root, if needed
    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]  # swap
        comparisons += 1
        heapify(arr, n, largest)


# The main function to sort an array of given size
def heap_sort(arr):
    global comparisons
    n = len(arr)

    # Build a max heap.
    # Since the last parent will be at (n//2-1) we can start at that location.
    for i in range(n // 2 - 1, -1, -1):
        heapify(arr, n, i)

    # One by one extract elements
    for i in range(n - 1, 0, -1):
        arr[i], arr[0] = arr[0], arr[i]  # swap
        comparisons += 1
        heapify(arr, i, 0)

    return arr

print("-----------------------------------------------------")

BS_X = []
IS_X = []
SS_X = []
QS_X = []
MS_X = []
HS_X = []
n = []

RN_X = []
IN_X = []
DN_X = []
AN_X = []
VN_X = []

COMP_RN_X = []
COMP_IN_x = []
COMP_DN_X = []
COMP_VN_X = []
COMP_AN_X = []

COMP = []

for i in range(10,5011,500):
    random_arr = random_generator(zakres_poczatek, zakres_koniec, i)
    increase_arr = random_increase_generator(i)
    decrease_arr = random_decrease_generator(i)
    a_shape_arr = random_Ashape_generator(i)
    v_shape_arr = random_Vshape_generator(i)

    print(i)
#=======================================================================
#=======================================================================
#
#     BS_start = timeit.default_timer()
#     Bubble_sort = bubble_sort(v_shape_arr.copy())
#     BS_end = timeit.default_timer()
#
#     print("BS DONE")
#
#     IS_start = timeit.default_timer()
#     Insertion_sort = insertion_sort(v_shape_arr.copy())
#     IS_end = timeit.default_timer()
#
#     print("IS DONE")
#
#     SS_start = timeit.default_timer()
#     Selection_sort = selection_sort(v_shape_arr.copy())
#     SS_end = timeit.default_timer()
#
#     print("SS DONE")
#
#     QS_start = timeit.default_timer()
#     Quick_sort = quick_sort(v_shape_arr.copy(),"right")
#     QS_end = timeit.default_timer()
#
#     print("QS DONE")
#
#     MS_start = timeit.default_timer()
#     Merge_sort = merge_sort(v_shape_arr.copy())
#     MS_end = timeit.default_timer()
#
#     print("MS DONE")
#
#     HS_start = timeit.default_timer()
#     Heap_sort = heap_sort(v_shape_arr.copy())
#     HS_end = timeit.default_timer()
#
#     print("HS DONE")
#
#
#     BS_DURATION = BS_end - BS_start
#     IS_DURATION = IS_end - IS_start
#     SS_DURATION = SS_end - SS_start
#     QS_DURATION = QS_end - QS_start
#     MS_DURATION = MS_end - MS_start
#     HS_DURATION = HS_end - HS_start
#
#
#     BS_X.append(BS_DURATION)
#     IS_X.append(IS_DURATION)
#     SS_X.append(SS_DURATION)
#     QS_X.append(QS_DURATION)
#     MS_X.append(MS_DURATION)
#     HS_X.append(HS_DURATION)
#
#     n.append(i)
#
# plt.plot(n,IS_X, color='r', label='IS')
# plt.plot(n,SS_X, color='g', label='SS')
# plt.plot(n,BS_X,  color='b', label='BS')
# plt.plot(n,QS_X,  color='y', label='QS')
# plt.plot(n,MS_X,  color='#eca1a6', label='MS')
# plt.plot(n,HS_X,  color='#000000', label='HS')
#=======================================================================
#=======================================================================
    # RN_start = timeit.default_timer()
    # Random, RN_NUM_OF_COMP = selection_sort(random_arr.copy())
    # RN_end = timeit.default_timer()
    #
    # print("RN DONE")
    #
    # IN_start = timeit.default_timer()
    # Increase, IN_NUM_OF_COMP = selection_sort(increase_arr.copy())
    # IN_end = timeit.default_timer()
    #
    # print("IN DONE")
    #
    # DN_start = timeit.default_timer()
    # Decrease, DN_NUM_OF_COMP = selection_sort(decrease_arr.copy())
    # DN_end = timeit.default_timer()
    #
    # print("DN DONE")
    #
    # AN_start = timeit.default_timer()
    # A_shaped, AN_NUM_OF_COMP = selection_sort(a_shape_arr.copy())
    # AN_end = timeit.default_timer()
    #
    # print("AN DONE")
    #
    # VN_start = timeit.default_timer()
    # V_shaped, VN_NUM_OF_COMP = selection_sort(v_shape_arr.copy())
    # VN_end = timeit.default_timer()
    #
    # print("VN DONE")

    # RN_DURATION = RN_end - RN_start
    # IN_DURATION = IN_end - IN_start
    # DN_DURATION = DN_end - DN_start
    # AN_DURATION = AN_end - AN_start
    # VN_DURATION = VN_end - VN_start
    #
    # RN_X.append(RN_DURATION)
    # IN_X.append(IN_DURATION)
    # DN_X.append(DN_DURATION)
    # AN_X.append(AN_DURATION)
    # VN_X.append(VN_DURATION)

    n.append(i)

# print("rn",RN_X)
# print("in",IN_X)
# print("dn",DN_X)
# print("an",AN_X)
# print("vn",VN_X)
#
#
# plt.plot(n,RN_X,  color='r', label='RANDOM')
# plt.plot(n,IN_X,  color='g', label='INCREASE RANDOM')
# plt.plot(n,DN_X,  color='b', label='DECREASE RANDOM')
# plt.plot(n,VN_X,  color='#000000', label='V SHAPED')
# plt.plot(n,AN_X,  color='#eca1a6', label='A SHAPED ')
#=======================================================================
#=======================================================================
    comparisons = 0

    RN_start = timeit.default_timer()
    Random = heap_sort(a_shape_arr.copy())
    RN_end = timeit.default_timer()

    COMP.append(comparisons)

    #
    # COMP_RN_X.append(RN_NUM_OF_COMP)
    # COMP_IN_x.append(IN_NUM_OF_COMP)
    # COMP_DN_X.append(DN_NUM_OF_COMP)
    # COMP_AN_X.append(AN_NUM_OF_COMP)
    # COMP_VN_X.append(VN_NUM_OF_COMP)

print(COMP)

#
# plt.plot(n,COMP_RN_X,  color='r', label='RN')
# plt.plot(n,COMP_IN_x,  color='g', label='IN')
# plt.plot(n,COMP_DN_X,  color='b', label='DN')
# plt.plot(n,COMP_AN_X,  color='#000000', label='AN')
# plt.plot(n,COMP_VN_X,  color='#eca1a6', label='VN')
#
#
#
# plt.xlabel('N')
# plt.ylabel('ilosc porownan')
# plt.legend()
# plt.show()
#
#
