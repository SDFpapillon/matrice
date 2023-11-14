def copy_maticiel(matrice):
    """
    les matrice sont en réalité des pointeurs, il faut donc les copy pour evité tout problème

    :param matrice:
    :return:
    """

    new_contenue = matrice.contenue.copy()

    new_matrice = Matrice(matrice.i, matrice.j, 0)

    for ligne in range(matrice.i):
        for collone in range(matrice.j):
            new_matrice.contenue[ligne][collone] = new_contenue[ligne][collone]

    return new_matrice


def produit_matriciel(matriceA, matriceB):
    """
    ne modifie pas les matrice A et B

    comment savoir si deux matrice sont multipliable : https://fr.wikipedia.org/wiki/Matrice_(math%C3%A9matiques)#Produit_matriciel

    :param matriceA:
    :param matriceB:
    :return matriceP:
    """
    matriceA = copy_maticiel(matriceA)
    matriceB = copy_maticiel(matriceB)

    if matriceA.j == matriceB.i:
        matriceP = Matrice(matriceA.i, matriceB.j, 0)

        for ligne in range(matriceP.i):
            for colonne in range(matriceP.j):
                for k in range(matriceA.j):
                    matriceP.contenue[ligne][colonne] += matriceA.contenue[ligne][k] * matriceB.contenue[k][colonne]

        return matriceP

    else:
        raise ValueError("matrice non multipliable")


def determinant(matrice):
    """
    calcule le determinant d'une matrice, ne modifie pas la matrice donner

    :param matrice:
    :return:
    """
    if matrice.i != matrice.j:
        raise ValueError("les matrices non carrés n'ont pas de determinant")

    if matrice.i == 2:
        return matrice.contenue[0][0]*matrice.contenue[1][1] - matrice.contenue[1][0]*matrice.contenue[0][1]

    else:
        det = 0
        for j in range(matrice.j):
            new_contenue = matrice.contenue[1:]
            for ligne in range(len(new_contenue)):
                new_contenue[ligne] = new_contenue[ligne][:j] + new_contenue[ligne][j+1:]
            det += matrice.contenue[0][j] * ((-1)**j) * determinant(Matrice(matrice.i-1, matrice.i-1, new_contenue))
        return det

###########################################################################
def trouver_indice_ligne_max(matrice, j):
    maxi = matrice.contenue[0][j]
    k = 0
    for i in range(1, j):
        if matrice.contenue[i][j] > maxi:
            maxi = matrice.contenue[i][j]
            k = i

    return k


def multiplier_ligne(matrice, j, l):
    """
    multiplie la ligne j par l

    /!\ modifi la matrice donner en paramettre /!\

    :param matrice:
    :param j:
    :param l:
    :return:
    """

    for i in range(matrice.i):
        matrice.contenue[i][j] *= l


def gauss(matrice):


    M = copy_maticiel(matrice)

    r = -1

    for j in range(M.j):
        k = trouver_indice_ligne_max(M, j)

        if M.contenue[k][j] != 0:
            r += 1
            multiplier_ligne(M, j, 1/M.contenue[k][j])

            if k != r:
                pass
                #echanger les lignes k et r

            for i in range(M.i):
                if i != r:
                    pass
                    #Soustraire à la ligne i la ligne r multipliée par A[i,j] (de façon à annuler A[i,j])


def invertion(matrice):  # @todo
    """
    return une matrice inverce de la matrice donner en param, ne modifi pas la matrice donner en param

    :param matrice:
    :return matrice_inverce:
    """

    if matrice.i != matrice.j:
        raise ValueError("les matrices non carrés ne sont pas inversible")

    matriceT = copy_maticiel(matrice)
    matriceT.contenue = 0

    return matriceT
#################################################

class Matrice:

    def __init__(self, i, j, contenue):
        """
        génère une matrice de taille i*j
        PLEINE DE 0 (ne pas changer, ca casserais tout)
        (i lignes (verticale) et j colonne (horizontale))

        :param i:
        :param j:
        """
        self.i = i
        self.j = j
        if contenue == 0:
            self.contenue = [[0 for colonne in range(j)] for ligne in range(i)]

        elif type(contenue) == list:
            self.contenue = contenue
            if self.i != len(self.contenue):
                raise ValueError("dimention indiquer pour i diff des dimentions du contenue")
            if self.j != len(self.contenue[0]):
                print(len(self.contenue[0]), self.j)
                raise ValueError("dimention indiquer pour j diff des dimentions du contenue")
        else:
            raise TypeError("le contenue ne correspond pas a une matrice")

    def __str__(self):
        string = ""
        for i in range(self.i):
            string += str(self.contenue[i]) + "\n"
        return string
