# Lesson name: Einführung in die Grundlagen des Programmierens: Variablen, Datentypen und Syntax

## Intro

### Einleitung: Was ist Programmieren?

Programmieren ist eine Möglichkeit, mit Computern zu kommunizieren, um Aufgaben zu erledigen, Probleme zu lösen und Anwendungen zu erstellen. Die Grundlagen des Programmierens basieren auf drei wichtigen Konzepten: **Variablen**, **Datentypen** und **Syntax**. Diese Bausteine sind essenziell für das Schreiben von Code in jeder Programmiersprache. In dieser Lektion werden wir diese Konzepte näher betrachten und verstehen, wie sie zusammenarbeiten, um funktionalen Code zu erstellen.

#### **Themes:**
- Grundlagen des Programmierens

## Content slide

### Was sind Variablen?

Eine Variable ist wie ein Behälter, der Informationen speichert. Programmierer nutzen Variablen, um Daten zu speichern, die später im Programm verwendet oder verändert werden können.

**Beispiel:**
- Stell dir eine Box vor, die mit "Punktestand" beschriftet ist. Wenn du ein Spiel spielst, kann sich der Punktestand ändern, während du Punkte sammelst. In der Programmierung könnte eine Variable namens `punktestand` diese Zahl speichern.

```python
punktestand = 10  # Die Variable 'punktestand' enthält den Wert 10
punktestand = punktestand + 5  # Die Variable 'punktestand' wird auf 15 aktualisiert
```

#### **Themes:**
- Definition von Variablen

## YesNo

**Statement:** Variablen können nur mit Zahlenwerten gefüllt werden.

**Answer:** False

**Feedback:**
Variablen können Werte verschiedener Datentypen, wie ganze Zahlen, Zahlen mit Dezimalstellen oder sogar Zeichenfolgen, halten. In Python werden Variablen dynamisch zugewiesen, was bedeutet, dass sie verschiedene Datentypen annehmen können, solange sie zu dem zugewiesenen Wert passen.


## Content slide

### Was sind Datentypen?

Datentypen geben dem Computer an, welche Art von Information in einer Variable gespeichert ist. Dies hilft dem Computer, die Daten korrekt zu verarbeiten.

**Häufige Datentypen:**
- **Integer**: Ganze Zahlen (z. B. 5, -3, 100)
- **String**: Text (z. B. "Hallo", "Programmieren macht Spaß!")
- **Boolean**: Wahrheitswerte (True oder False)

**Beispiel:**
- Stell dir vor, du sortierst Gegenstände in Kategorien. Zahlen kommen in eine Box, Wörter in eine andere und Ja/Nein-Antworten in eine dritte. Ähnlich kategorisiert die Programmierung Informationen mit Datentypen.

```python
alter = 13  # Integer-Datentyp
name = "Alice"  # String-Datentyp
ist_schueler = True  # Boolean-Datentyp
```

#### **Themes:**
- Arten von Datentypen

## YesNo

**Statement:** Jede Variable muss einen Datentyp haben.

**Answer:** True

**Feedback:**
In der Programmierung ist es wichtig, dass jede Variable einen Datentyp hat, damit sie korrekt interpretiert werden kann. Ohne einen Datentyp könnte der Computer nicht wissen, ob die Variable eine Zahl, einen Text oder einen booleschen Wert darstellt.


## Content slide

### Was ist Syntax?

Syntax ist das Regelwerk, das definiert, wie Code in einer bestimmten Programmiersprache geschrieben werden muss. Ähnlich wie Grammatik in der deutschen Sprache sorgt Syntax dafür, dass Code klar und funktional ist.

**Beispiel:**
- Stell dir Syntax als Anleitungen für das Zusammenbauen eines Puzzles vor. Wenn du die Anleitungen nicht befolgst, passen die Puzzlestücke nicht korrekt zusammen.

```python
# Beispiel für korrekte Syntax in Python:
print("Hallo, Welt!")  # Zeigt "Hallo, Welt!" auf dem Bildschirm an

# Beispiel für fehlerhafte Syntax:
print(Hallo, Welt!)  # Fehler, da der Text nicht in Anführungszeichen steht
```

#### **Themes:**
- Definition von Syntax

## YesNo

**Statement:** Syntax beeinflusst, wie Programme auf verschiedenen Plattformen ausgeführt werden.

**Answer:** False

**Feedback:**
Syntax definiert die Regeln für den Code, aber die Ausführung von Programmen auf verschiedenen Plattformen wird durch die Kompatibilität der Programmiersprache und das Betriebssystem beeinflusst.


## Content slide

### Wie arbeiten diese Konzepte zusammen?

Variablen, Datentypen und Syntax arbeiten zusammen, um die Grundlage der Programmierung zu bilden. Variablen speichern Daten, Datentypen definieren die Art der Daten, und Syntax stellt sicher, dass der Code korrekt geschrieben wird, damit der Computer ihn verstehen kann.

**Beispiel:**
- Stell dir vor, du schreibst ein Rezept. Variablen sind wie die Zutaten, Datentypen sind die Kategorien der Zutaten (z. B. Flüssigkeiten, Feststoffe), und Syntax ist das Format der Rezeptanweisungen.

```python
# Beispiel für die Kombination von Variablen, Datentypen und Syntax:
name = "Sam"  # Variable mit String-Datentyp
alter = 14  # Variable mit Integer-Datentyp

print("Mein Name ist " + name + " und ich bin " + str(alter) + " Jahre alt.")
```

#### **Themes:**
- Zusammenarbeit von Konzepten

## YesNo

**Statement:** Ein Programm kann ohne Variablen nicht funktionieren.

**Answer:** True

**Feedback:**
Variablen sind entscheidend für die Speicherung von Daten innerhalb eines Programms. Ohne Variablen könnte ein Programm nicht Daten verarbeiten oder diese an verschiedene Teile des Codes weitergeben.


## Content slide

### Zusammenfassung: Die Grundlagen verstehen

**Wichtige Erkenntnisse:**
- **Variablen** speichern Daten, die in einem Programm verwendet und verändert werden können.
- **Datentypen** definieren die Art der Daten, die in einer Variable gespeichert sind (z. B. Zahlen, Text, Wahrheitswerte).
- **Syntax** sorgt dafür, dass Code korrekt geschrieben wird, damit er ohne Fehler ausgeführt werden kann.
- Zusammen bilden diese Konzepte die Grundlage der Programmierung und sind unerlässlich für das Erstellen funktionalen und organisierten Codes.

Programmieren mag anfangs komplex erscheinen, aber das Verständnis dieser Grundlagen wird dir helfen, Vertrauen zu gewinnen und dich auf fortgeschrittene Themen vorzubereiten.

#### **Themes:**
- Zusammenfassung der Konzepte

## YesNo

**Statement:** Variablen in einem Programm können nur eine einzelne Instanz eines Wertes halten.

**Answer:** False

**Feedback:**
Variablen sind flexibel und können mehr als einen Wert speichern. Während eine Variable einmal einen Wert hat, kann sie diesen Wert später ändern, was sie zu einem wesentlichen Werkzeug für dynamische Datenverwaltung macht.

