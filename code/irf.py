# irf.py
#   Improved Regula Falsi method by Soumen Shaw and Basudeb Mukhopadhyay, with parameter k = f(c)/f(a or b)
#   coded in python
# By: Andy Shapiro and Ian Wixom

import math
import matplotlib.pyplot as plt

# Approximate Earth-Moon system scaled values for CR3BP model
U_1 = 0.98785
U_2 = 1 - U_1


def f(x):
    return x - U_1 * (x + U_2) / (abs(x + U_2)) ** 3 - U_2 * (x - U_1) / (abs(x - U_1)) ** 3

def method(array, tolerance):
    lagrange = [[], [], []]

    for i in range(3):
        a = array[i][0]
        b = array[i][1]

        f_a = f(a)
        f_b = f(b)

        count = 0
        x = a
        error = abs(f_a)

        data = []
        print("Bound {}:".format(i+1))
        while error > tolerance:
            c = (a * f_b - b * f_a) / (f_b - f_a)
            f_c = f(c)

            if f_a * f_c < 0:
                k = (abs(f_c) % abs(f_b)) / (abs(f_b))

                x = ((k - 1) * b * f_a + a * f_b) / ((k - 1) * f_a + f_b)
                f_x = f(x)

                if f_a * f_x < 0:
                    b = x
                    f_b = f_x
                else:
                    a = x
                    f_a = f_x

                    b = c
                    f_b = f_c
            else:
                k = (abs(f_c) % abs(f_a)) / (abs(f_a))

                x = ((k - 1) * a * f_b + b * f_a) / ((k - 1) * f_b + f_a)
                f_x = f(x)

                if f_a * f_x < 0:
                    a = c
                    f_a = f_c

                    b = x
                    f_b = f_x
                else:
                    a = x
                    f_a = f_x

            count = count + 1
            error = abs(f_x)
            lagrange[i].append(error)

            print("Iteration {}: error = {} at x_3 = {}".format(count, error, x))

    print(lagrange)
    return lagrange


def main():
    tolerance = 1E-5

    bounds_1 = [[-2*U_1, -U_2 - tolerance], [-U_2 + tolerance, U_1 - tolerance], [U_1 + tolerance, 2*U_1]]
    bounds_2 = [[-1.1, -0.9], [0.75, 0.95], [1.05, 1.25]]
    print("original, guessed bounds: ")
    original_result = method(bounds_1, tolerance)
    print("approximated bounds: ")
    bounded_result = method(bounds_2, tolerance)

    plt.plot(original_result[0], color = 'r')
    plt.plot(original_result[1], color = 'b')
    plt.plot(original_result[2], color = 'g')

    plt.legend(["L_1", "L_2", " L_3"])
    
    plt.title('IRF Method Approx. with Original Bounds, New Bounds as Dashed')

    plt.plot(bounded_result[0], color =  'r', ls = '--')
    plt.plot(bounded_result[1], color = 'b', ls = '--')
    plt.plot(bounded_result[2], color = 'g', ls = '--')

    plt.axhline(y = 1e-5, color = 'k', linestyle = ':')
    plt.grid(True)
    
    plt.xlabel('iterations')
    plt.ylabel('log error')
    plt.yscale('log')  
    
    plt.show()
    


main()
