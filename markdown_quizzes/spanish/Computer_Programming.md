# Lesson name: Introducción a Variables y Tipos de Datos en Programación

## Intro

### Introducción

¡Bienvenidos a un mundo lleno de posibilidades! Hoy exploraremos cómo los programadores usan variables y tipos de datos para crear programas dinámicos y funcionales. 🌟

#### **Themes:**
- concepto de variables

## Content slide

### ¿Qué es una variable?

Las variables son contenedores que almacenan datos en un programa. Cada variable tiene:

1. **Un Nombre**: Identificador único.
2. **Un Valor**: Información almacenada.
3. **Un Tipo de Dato**: Clase de información que puede guardar.

Ejemplo en Python:
```python
puntaje_jugador = 10
```
- **Nombre de la Variable**: `puntaje_jugador`
- **Valor**: `10`
- **Tipo de Dato**: Entero.

#### **Themes:**
- definición de variable
- componentes de una variable

## YesNo

**Statement:** Las variables en programación no pueden almacenar información.

**Answer:** False

**Feedback:**
En programación, las variables son específicamente utilizadas para almacenar y procesar información, lo cual es fundamental para el funcionamiento de cualquier programa. La idea de que las variables no puedan almacenar información es incorrecta y va en contra de los principios básicos de programación.


## Content slide

### Reglas para nombrar variables

Las reglas para nombrar variables incluyen:
- Usar nombres significativos (ejemplo: `nombre_usuario`).
- Comenzar con una letra o guion bajo (_), pero no con un número.
- Evitar espacios o caracteres especiales.
- Usar letras minúsculas para consistencia.

Ejemplo:
Correcto: `color_favorito`
Incorrecto: `3color`

#### **Themes:**
- reglas de nombres de variables

## YesNo

**Statement:** En programación, es permisible comenzar los nombres de variables con números.

**Answer:** False

**Feedback:**
En la programación, los nombres de variables deben comenzar con una letra o un guion bajo (_), no con un número. Esto ayuda a mantener la claridad y las convenciones de programación establecidas.


## Content slide

### Tipos de datos comunes

Los tipos de datos más comunes son:

1. **Entero**: Números enteros.
   - Ejemplo: `edad = 13`
2. **Flotante**: Números con decimales.
   - Ejemplo: `pi = 3.14`
3. **Cadena**: Texto o caracteres.
   - Ejemplo: `saludo = "Hola"`
4. **Booleano**: Verdadero o falso.
   - Ejemplo: `es_estudiante = True`

Ejemplo en código:
```python
precio = 19.99  # Flotante
usuario = "Ana"  # Cadena
activo = False  # Booleano
```

#### **Themes:**
- tipos de datos
- ejemplos de datos

## YesNo

**Statement:** Los enteros pueden representar tanto números positivos como negativos.

**Answer:** True

**Feedback:**
En el lenguaje de programación, los enteros son capaces de almacenar números sin signo, lo que incluye valores positivos y negativos. Esto es fundamental para manejar operaciones matemáticas que requieren substractar o añadir cantidades de valor negativo.


## Content slide

### Operaciones con variables

Las variables permiten realizar operaciones:

1. **Operaciones aritméticas**:
   - Ejemplo:
     ```python
     a = 5
     b = 3
     resultado = a + b  # Resultado: 8
     ```

2. **Operaciones con cadenas**:
   - Concatenación:
     ```python
     nombre = "Juan"
     apellido = "Pérez"
     nombre_completo = nombre + " " + apellido  # Resultado: "Juan Pérez"
     ```

3. **Operaciones lógicas**:
   - Ejemplo:
     ```python
     es_usuario = True
     es_admin = False
     puede_acceder = es_usuario or es_admin  # Resultado: True
     ```

#### **Themes:**
- operaciones aritméticas
- operaciones con cadenas
- operaciones lógicas

## YesNo

**Statement:** En operaciones aritméticas, la suma de dos variables siempre produce un resultado de tipo cadena.

**Answer:** False

**Feedback:**
Las operaciones aritméticas, como la suma, resultan en tipos numéricos, no de tipo cadena. En el ejemplo proporcionado, la suma de dos enteros (5 + 3) da como resultado un entero (8), no una cadena.


## Content slide

### Aplicaciones de variables en la vida real

Las variables se usan en programación para:
- Almacenar datos de entrada del usuario.
- Monitorear puntajes en juegos.
- Gestionar inventarios en tiendas virtuales.
- Configurar ajustes en aplicaciones.

Ejemplo en código:
```python
jugador = "Luis"
puntaje = 40
print(jugador + " tiene " + str(puntaje) + " puntos.")
```

#### **Themes:**
- usos de variables
- ejemplo práctico

## YesNo

**Statement:** En programación, las variables solo pueden almacenar valores de tipo entero.

**Answer:** False

**Feedback:**
Esta afirmación es incorrecta porque las variables en programación pueden almacenar varios tipos de datos, incluyendo enteros, cadenas de texto, booleanos, y más. La versatilidad de las variables permite su uso en una amplia gama de aplicaciones, no limitándose solo a valores enteros.


## Content slide

### Resumen: Variables y Tipos de Datos

Resumen:
- Las variables son contenedores nombrados que almacenan datos.
- Cada variable tiene un nombre, un valor y un tipo de dato.
- Los tipos de datos comunes son enteros, flotantes, cadenas y booleanos.
- Las variables se usan para realizar operaciones y crear programas dinámicos.

Dominar las variables y los tipos de datos es esencial para la programación eficiente.

#### **Themes:**
- resumen de conceptos claves

## YesNo

**Statement:** Las variables pueden almacenar valores de diferentes tipos de datos.

**Answer:** True

**Feedback:**
Esto es correcto porque en la programación, las variables sirven como recipientes para almacenar información, y estos recipientes pueden contener elementos de varios tipos, como números, texto o valores lógicos.

