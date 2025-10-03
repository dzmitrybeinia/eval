# Lesson name: Introduction à la programmation Python : Variables, types de données et opérations d'entrée/sortie

## Intro

### Introduction à Python

Bienvenue dans le monde passionnant de Python, un langage de programmation apprécié pour sa simplicité et sa polyvalence. Aujourd'hui, nous allons découvrir les bases de Python, notamment les variables, les types de données et les opérations d'entrée/sortie. Préparez-vous à explorer comment ces concepts peuvent être utilisés pour créer des programmes utiles et interactifs. 🚀

#### **Themes:**
- Présentation du langage Python

## Content slide

### Que sont les variables ?

Les variables sont comme des boîtes où l'on peut ranger des informations. Elles permettent de stocker des données que le programme peut utiliser. En Python, vous n'avez pas besoin de spécifier le type de données, Python le déduit automatiquement.

**Exemple :**
```python
nom = "Alice"
age = 14
hauteur = 1.65
est_élève = True

print(nom)  # Affiche : Alice
print(age)  # Affiche : 14
```

#### **Themes:**
- Définition des variables en Python

## YesNo

**Statement:** En Python, vous devez toujours déclarer le type de données d'une variable.

**Answer:** False

**Feedback:**
En Python, le type de données d'une variable est déduit automatiquement à partir de la valeur assignée, donc il n'est pas nécessaire de déclarer explicitement le type de données.


## Content slide

### Types de données courants en Python

Python propose plusieurs types de données pour représenter différents types d'informations :
- **Entier (`int`)** : nombres entiers (ex : 10, -3).
- **Flottant (`float`)** : nombres décimaux (ex : 3.14, -0.5).
- **Chaîne de caractères (`str`)** : texte (ex : "Bonjour !").
- **Booléen (`bool`)** : valeurs Vrai ou Faux.

**Exemple :**
```python
x = 10
message = "Salut"
est_correct = False

print(type(x))        # Affiche : <class 'int'>
print(type(message))  # Affiche : <class 'str'>
```

#### **Themes:**
- Types de données Python

## YesNo

**Statement:** La variable x peut stocker une valeur décimale.

**Answer:** True

**Feedback:**
En Python, les entiers (`int`) sont utilisés pour stocker des nombres entiers, pas des nombres décimaux. Les nombres décimaux sont représentés par des flottants (`float`). La variable x a été déclarée avec une valeur entière (10), ce qui est correct pour un entier, mais si vous voulez stocker un nombre décimal, vous devriez utiliser `float`.


## Content slide

### Opérations d'entrée/sortie de base

Les opérations d'entrée/sortie permettent aux programmes de communiquer avec l'utilisateur. Python utilise :
- **`input()`** pour obtenir des informations de l'utilisateur.
- **`print()`** pour afficher des messages.

**Exemple :**
```python
nom = input("Quel est votre prénom ? ")
print("Bonjour, " + nom + "!")

num1 = float(input("Entrez un nombre : "))
num2 = float(input("Entrez un autre nombre : "))
print("La somme est :", num1 + num2)
```

#### **Themes:**
- Fonctions input et print

## YesNo

**Statement:** La fonction 'input' est utilisée pour demander des informations à l'utilisateur.

**Answer:** True

**Feedback:**
Cette déclaration est exacte. Dans Python, la fonction 'input' est effectivement utilisée pour interagir avec l'utilisateur en demandant des données. Lorsque le programme s'exécute, il est arrêté pendant que l'utilisateur fournit les informations requises, ce qui permet d'ajouter une fonctionnalité interactive à votre programme.


## Content slide

### Application réelle : Calculateur basique

En combinant les concepts de variables, types de données et opérations d'entrée/sortie, vous pouvez créer un programme interactif, comme un calculateur basique.

**Exemple :**
```python
print("Bienvenue dans le calculateur !")
num1 = float(input("Entrez le premier nombre : "))
num2 = float(input("Entrez le deuxième nombre : "))

print("Somme :", num1 + num2)
print("Différence :", num1 - num2)
print("Produit :", num1 * num2)
print("Quotient :", num1 / num2)
```

#### **Themes:**
- Création d'un calculateur

## YesNo

**Statement:** En Python, la fonction `float()` est utilisée pour convertir une entrée en nombre à virgule flottante.

**Answer:** True

**Feedback:**
Dans Python, la fonction `float()` est spécifiquement conçue pour convertir des chaînes ou des nombres d'autres types en nombres à virgule flottante, ce qui est essentiel pour effectuer des calculs avec précision.


## Content slide

### Résumé du cours

**Points clés :**
- Les variables permettent de stocker des données pour les utiliser dans un programme.
- Les types de données en Python incluent les entiers, flottants, chaînes de caractères et booléens.
- Les fonctions `input()` et `print()` facilitent les interactions utilisateur.

Python est un langage accessible et puissant, idéal pour débuter en programmation et découvrir ses nombreuses applications.

#### **Themes:**
- Résumé des concepts Python

## YesNo

**Statement:** En Python, les variables ne peuvent stocker que des données numériques.

**Answer:** False

**Feedback:**
En Python, les variables sont polyvalentes et peuvent stocker différents types de données, comme des entiers, des flottants, des chaînes de caractères et des booléens, pas seulement des données numériques.

