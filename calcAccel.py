"""
Skript zur Berechnung sinnvoller Parameter für die Bewegungsgleichung, um die
Sprung-Animation in remakeBenny.py cool zu gestalten.
Außerdem kann das verwenden von Matplotlib und Numpy geübt werden.

Idee: max. Sprunghöhe soll etwa 100 px betragen, beim Absprung kann ein v0
gesetzt werden und dann wirkt eine "Gravitationsbeschleunigung" G. Diese Parameter
gilt es sinnvoll zu bestimmen.
Ein Zeitschritt im Programm kann aus der framerate bestimmt werden:
1/FPS

Bewegungsgleichung (Startpunkt y_max, Sprung nach oben, also in negative y-Richtung):
y(t) = y_max - v0 * t + 0.5 a * t²

y_min(t) bei y'(t) = 0
y'(t) = -v0 + a*t
<->
v0/a = t = T/2, Tbezeichnet Gesamtdauer, da hoch und runter

Randbedingung für T(kann als Simulationsdauer gesetzt werden.
z.B T soll 1.5s

y_min(t) soll 500
y_min = y_max - v0 * (v0/a) + 0.5*a * (v0/a)²
      = y_max - v0² / a + 0.5 v0²/a
      = y_max - 0.5 v0² / a
    
0.5 v0² / a = y_max-y_min = delta    !!!
            = 100
<->
v0²/a = 2*(delta)
      = 200
    
-> einen der Parameter setzen, dann der andere frei wählbar
a = v0²/(2*(delta))    !!!
    v0²/200

und t = v0/a

t = v0/a          !!!
<->
t*a = v0

<->
a = v0²/200 = (t *a)² / 200
<->
1 = t²*a / 200
<->
200/t² = 200/(T/2)² = a = 200/0.75² = 356
-> v0 = a * T/2 = 356 * 0.75 = 267

Beispielplot:

import numpy as np
from matplotlib import pyplot as plt

t = np.linspace(0, 1.5, 50)
y_max = 600
v0 = 267
a = 356

# y(t) = y_max - v0 * t + 0.5 a * t²
y = y_max - v0 * t + 0.5 * a * t**2

plt.plot(t, y)
plt.show()

# Parabel entspricht genau dem erwünschten Ergebnis.





"""

def calcAandV0(T, deltaY):
    # Input: Gesamtsprungdauer T in s und Sprunghöhe deltaY in px
    # Output: Beschleunigung a in px/s² und Initialsprunggeschwindigkeit v0 in px/s

    a = (2*(deltaY))/(T/2)**2
    v0 = a * T/2
    
    return (a,v0)
