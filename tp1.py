# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
from numpy.linalg import norm


class Dioptre:
    diametre = 25.4  # diametre du dioptre en mm, c'est un pouce

    def __init__(self, z0, R, n_1, n_2, diametre=None):
        self.z0 = z0

        self.R = float(R)
        if diametre is not None:
            self.diametre = diametre
        self.n_1 = n_1
        self.n_2 = n_2
        self.z_center = self.z0 + self.R

    def __repr__(self):

        rep = 'z0 = ' + str(self.z0) + '\nR  = ' + str(self.R) + '\nn1 = ' + str(
            self.n_1) + '\nn2 = ' + str(self.n_2) + '\ndiametre = ' + str(self.diametre)
        return rep

    def equation(self, x):
        self.x = x
        z = self.z_center + np.sign(self.R)*np.sqrt(self.R**2 - self.x**2)
        return z

    def plot(self):
        x = np.linspace(-self.diametre/2, self.diametre/2)
        plt.plot(self.equation(x), x)

    def intersection(self, rayon):
        # trinôme at²+bt+c = 0
        # a = ||k||²
        # b = 2k.(p0-C)
        # c = ||p0-C||² - R²
        a = norm(rayon.k)**2
        p0_moins_z_center = rayon.p0 - np.array([0, 0, self.z_center])
        b = 2*np.dot(rayon.k, p0_moins_z_center)
        c = norm(p0_moins_z_center)**2 - self.R**2

        discriminant = b**2 - 4*a*c
        if discriminant < 0:
            print("Intersection : pas de solution")
        if self.R > 0:
            t = (-b - np.sqrt(discriminant))/(2*a)
        else:
            t = (-b + np.sqrt(discriminant))/(2*a)
        return rayon.p0 + t*rayon.k  # array de taille 3

    def traversee(self, rayon):
        p2 = self.intersection(rayon)
        # Dessiner les vecteurs pour le voir
        n = p2 - np.array([0, 0, self.z_center])
        n = n/norm(n)
        k_par = rayon.k - np.dot(rayon.k, n)*n
        alpha = np.sqrt(self.n_2**2 - norm(k_par)**2)
        # Le vecteur doit pointer à droite
        # (faire une dessin)
        if self.R > 0:
            k2 = k_par - alpha*n
        else:
            k2 = k_par + alpha*n
        return Rayon(p2, k2)


class Rayon:
    def __init__(self, p0, k, n=1):
        self.p0 = p0
        self.k = k/norm(k) * n

    def __repr__(self):
        rep = 'p0 =' + str(self.p0) + '\nk = ' + str(self.k)
        return rep


class Faisceau(list):
    def plot(self):
        x = []
        z = []
        for rayon in self:
            x.append(rayon.p0[1])
            z.append(rayon.p0[2])
        plt.plot(z, x)


class SystemeOptique(list):
    def calcul_faisceau(self, r0):
        faisceau = Faisceau()
        faisceau.append(r0)
        for dioptre in self:
            faisceau.append(dioptre.traversee(faisceau[-1]))
            return faisceau

    def plot(self):
        for dioptre in self:

            return dioptre


p1 = np.array([0, 0, -3])
z0 = 0
R = 6
n1 = 1
n2 = 1.5
k1_x = np.array([0, .5, np.sqrt(.75)])

dioptre_1 = Dioptre(z0, R, n1, n2)
dioptre_2 = Dioptre(15, 20, 1.5, 1)
rayon_1 = Rayon(p1, k1_x, n1)
rayon_2 = dioptre_1.traversee(rayon_1)

faisceau_1 = Faisceau([rayon_1, rayon_2])
faisceau_1.plot()

systeme_optique_1 = SystemeOptique([dioptre_1, dioptre_2])
systeme_optique_1.plot()
