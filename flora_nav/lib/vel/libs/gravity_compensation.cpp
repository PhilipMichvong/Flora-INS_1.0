#include "gravity_compensation.hpp"

/*
Aby skompensować przyspieszenie ziemskie z odczytów akcelerometru wykorzystując dane z akcelerometru i filtr Madgwicka, 
można postępować zgodnie z poniższymi krokami:

1. Odczytaj dane z akcelerometru - pomiary przyspieszenia w trzech osiach (x, y, z).

2. Przetwórz dane z akcelerometru przy użyciu filtru Madgwicka. 
    Filtr Madgwicka jest algorytmem filtracji żyroskopowej, 
    który pozwala na równoczesną korektę błędów pomiarów przyspieszenia 
    i prędkości kątowej w trzech osiach. Filtr ten zwraca trzy wartości 
    określające orientację urządzenia w przestrzeni (czyli wartości w trzech osiach obrotu).

3. Skompensuj przyspieszenie ziemskie z odczytów akcelerometru. 
    W tym celu należy wykorzystać dane uzyskane w kroku 2, czyli 
    wartości orientacji urządzenia w przestrzeni. 
    Skompensowane wartości przyspieszenia w osiach x, y i z można 
    obliczyć za pomocą poniższego równania:

        X: ax_skomp = ax - g*sin(pitch)
        Y: ay_skomp = ay + g*sin(roll)*cos(pitch)
        Z: az_skomp = az + g*cos(roll)*cos(pitch)

        gdzie:

        ax, ay, az - nie skompensowane wartości przyspieszenia w trzech osiach,
        g - wartość przyspieszenia ziemskiego (około 9,81 m/s^2),
        pitch - kąt nachylenia w płaszczyźnie x-y,
        roll - kąt nachylenia w płaszczyźnie y-z.

 Po skompensowaniu przyspieszenia ziemskiego z odczytów akcelerometru, 
 można je wykorzystać do dalszych obliczeń lub do sterowania urządzeniem.
*/
void compensateGravity(double *acc, double pitch, double roll, double *compensatedGravity)
{
    compensatedGravity[0] = acc[0] - GRAVITY * sin(pitch);  // compensated acceleration of X axis
    compensatedGravity[1] = acc[1] + GRAVITY * sin(roll) * cos(pitch);  // compensated acceleration of Y axis
    compensatedGravity[2] = acc[2] + GRAVITY * cos(roll) * sin(pitch);  // compensated acceleration of Z axis
}
