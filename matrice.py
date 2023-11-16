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

def trouver_indice_ligne_max(matrice, j):
    maxi = matrice.contenue[0][j]
    k = 0
    for i in range(1, j):
        if matrice.contenue[i][j] > maxi:
            maxi = matrice.contenue[i][j]
            k = i

    return k


def multiplier_ligne_out(martice, i, l):
    """
    ne modifie pas la matrice donner en paramètre, copi, multiplie par l puis return la ligne i

    :param martice:
    :param i:
    :param l:
    :return:
    """

    new_ligne = []

    for elm in martice.contenue[i]:
        new_ligne += [elm*l]

    return new_ligne


def inverce_gauss(A0):
    """ Pivot de Gauss : on se ramène à la matrice identité
        A.X=B <=> I.X=solution
    """

    if determinant(A0) == 0:
        raise ValueError("det = 0")

    lignes, colonnes = A0.i, A0.j
    A, B = copy_maticiel(A0), Matrice(lignes, colonnes, 'idd')

    for j in range(colonnes):
        for i in range(lignes):
            if i != j:
                mu = -A.contenue[i][j]/A.contenue[j][j]     # Ajj : pivot
                A.add_lignes(i, multiplier_ligne_out(A, j, mu))
                B.add_lignes(i, multiplier_ligne_out(B, j, mu))

    # ici, A est une matrice diagonale
    for i in range(lignes):
        coeff = 1/A.contenue[i][i]
        A.multiplier_ligne(i, coeff) # Pour avoir des 1 sur la diagonale
        B.multiplier_ligne(i, coeff)

    return B                  # A est la matrice identité ; B est la matrice A^-1


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

        elif contenue == 'idd':
            self.contenue = [[0 for colonne in range(j)] for ligne in range(i)]
            for i in range(self.i):
                self.contenue[i][i] = 1

        elif type(contenue) == list:
            self.contenue = contenue
            if self.i != len(self.contenue):
                raise ValueError("dimention indiquer pour i diff des dimentions du contenue")
            if self.j != len(self.contenue[0]):
                print(len(self.contenue[0]), self.j)
                raise ValueError("dimention indiquer pour j diff des dimentions du contenue")
        else:
            raise TypeError("le contenue ne correspond pas a une matrice")

    def multiplier_ligne(self, i, l):
        """
        multiplie la ligne j par l

        /!\ modifi la matrice donner en paramettre /!\

        :param matrice:
        :param j:
        :param l:
        :return:
        """

        for j in range(self.j):
            self.contenue[i][j] *= l

    def echange_ligne(self, j, k):
        """
        echange les lignes j et k

        :param j:
        :param k:
        :return:
        """

        self.contenue[j], self.contenue[k] = self.contenue[k], self.contenue[j]

    def add_lignes(self, i, k):
        """
        additione la ligne k a la ligne d'indice i

        :param i:
        :param k:
        :return:
        """

        for j in range(len(self.contenue[i])):
            self.contenue[i][j] += k[j]

    def __str__(self):
        string = ""
        for i in range(self.i):
            string += str(self.contenue[i]) + "\n"
        return string
