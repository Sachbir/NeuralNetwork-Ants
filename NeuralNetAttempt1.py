from Simulation import Simulation
import math


def main():

    simulation = Simulation()
    simulation.run()

#     u = (1, 0)
#     v = (math.cos(3 * math.pi / 4), -math.sin(3 * math.pi / 4))
#
#     numerator = dot_product(u, v)
#     denominator = magnitude(u) * magnitude(v)
#
#     angle_between = math.acos(numerator / denominator)
#
#     print(rad_to_degree(angle_between))
#
#
# def dot_product(u, v):
#
#     return u[0] * v[0] + u[1] * v[1]
#
#
# def magnitude(u):
#
#     return math.sqrt(u[0] ** 2 + u[1] ** 2)
#
#
# def rad_to_degree(x):
#
#     return x / math.pi * 180


main()
