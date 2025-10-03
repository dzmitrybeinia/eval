# Lesson name: Wprowadzenie do programowania w Pythonie: zmienne, typy danych i podstawowe operacje wejścia/wyjścia

## Intro

### Wprowadzenie do tematu

Python jest jednym z najpopularniejszych języków programowania na świecie dzięki swojej prostocie i wszechstronności. W tym temacie poznasz podstawowe elementy programowania w Pythonie, takie jak zmienne, typy danych oraz operacje wejścia i wyjścia. Te fundamenty pozwolą Ci tworzyć programy, które przechowują i manipulują danymi oraz komunikują się z użytkownikami.

#### **Themes:**
- Python jako język programowania

## Content slide

### Co to są zmienne?

Zmienne to podstawowe elementy każdego programu. Są to etykiety, które przechowują dane w pamięci komputera i mogą być modyfikowane w trakcie działania programu.

### Cechy zmiennych:
- Mają nazwy (np. `wiek`, `nazwa`, `cena`).
- Przechowują wartości danych (np. liczby, tekst).
- Mogą być modyfikowane w trakcie działania programu.

### Przykład:
```python
wiek = 15
print(wiek)  # Wyjście: 15
wiek = 16
print(wiek)  # Wyjście: 16
```

#### **Themes:**
- Definicja zmiennych
- Przykłady użycia zmiennych

## YesNo

**Statement:** Zmienne w Pythonie mogą używać nazw dla przechowywania tylko liczb całkowitych.

**Answer:** False

**Feedback:**
W Pythonie zmienne mogą przechowywać różne typy danych, takie jak liczby całkowite, liczby zmienniste, ciągi znaków, listy, słowniki, a nawet obiekty klas. Oprócz liczb całkowitych, nazwy mogą być użyte również do przechowywania tekstu, co umożliwia bardziej zróżnicowaną i wszechstronną programowanie.


## YesNo

**Statement:** W Pythonie liczby całkowite i liczby dziesiętne mogą być używane do reprezentowania różnych wartości.

**Answer:** True

**Feedback:**
To jest prawda. Python ma typy danych `int` i `float`, które są używane do reprezentowania liczb całkowitych i liczb dziesiętnych odpowiednio. To umożliwia przechowywanie i manipulację różnymi rodzajami danych liczbowych.


## Content slide

### Typy danych w Pythonie

Typy danych określają rodzaj informacji, które zmienna może przechowywać. Python obsługuje różne typy danych, takie jak:

- **Integer (`int`)**: Liczby całkowite
  Przykład: `x = 10`
- **Float (`float`)**: Liczby dziesiętne
  Przykład: `cena = 19.99`
- **String (`str`)**: Tekst
  Przykład: `nazwa = "Ala"`
- **Boolean (`bool`)**: Wartości logiczne Prawda/Fałsz
  Przykład: `czy_student = True`

### Dlaczego typy danych są ważne?
Typy danych pomagają komputerowi zrozumieć, jak przechowywać i przetwarzać informacje.

### Przykład kodu:
```python
x = 5
y = 3.14
nazwa = "Jan"
czy_aktywny = False
print(x, y, nazwa, czy_aktywny)
```

#### **Themes:**
- Rodzaje typów danych
- Znaczenie typów danych

## YesNo

**Statement:** Funkcja `input()` może bezpośrednio wykonywać działania na komputerze bez żadnych zaawansowanych funkcji.

**Answer:** False

**Feedback:**
Funkcja `input()` w Pythonie pozwala na pobieranie danych wejściowych od użytkownika, ale nie wykonywa żadnych operacji bezpośrednio na sprzęcie komputerowym. Funkcje, które wykonują działania na komputerze, zwane są 'system calls' lub 'system calls', i w Pythonie są one zazwyczaj wykonywane za pomocą modułów takich jak 'os' lub 'subprocess'. Funkcja `input()` jest wyłącznie służąca do interakcji z użytkownikiem, a nie do operacji systemowych.


## YesNo

**Statement:** Kod wyprowadza liczbę znaków wprowadzoną przez użytkownika.

**Answer:** False

**Feedback:**
Kod skupia się na zbieraniu i wyświetlaniu informacji o imieniu i wieku, nie na liczbę znaków. Aby wyprowadzić liczbę znaków, niezbędne byłoby użycie funkcji, która zajmuje ciąg jako dane wejściowe, takiej jak `len()`.


## Content slide

### Podstawowe operacje wejścia/wyjścia w Pythonie

Python umożliwia interakcję z użytkownikiem dzięki funkcjom wejścia i wyjścia.

### Wejście:
Funkcja `input()` pozwala użytkownikowi wprowadzić dane do programu.

Przykład:
```python
nazwa = input("Podaj swoje imię: ")
print("Cześć, " + nazwa + "!")
```

### Wyjście:
Funkcja `print()` wyświetla dane użytkownikowi.

Przykład:
```python
wiek = 15
print("Twój wiek to:", wiek)
```

### Łączenie wejścia i wyjścia:
Często używamy obu funkcji, aby stworzyć interaktywne programy.

Przykład:
```python
liczba = input("Podaj liczbę: ")
print("Podałeś liczbę:", liczba)
```

#### **Themes:**
- Funkcja input
- Funkcja print

## YesNo

**Statement:** W Pythonie zmienne mogą przechowywać tylko liczby całkowite.

**Answer:** False

**Feedback:**
W Pythonie zmienne mogą przechowywać różne typy danych, nie tylko liczby całkowite. Obejmuje ono również liczby dziesiętne, tekst, i inne. Ta różnorodność pozwala na bardziej elastyczne i wszechstronne programowanie.

