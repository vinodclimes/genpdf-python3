class Paragraphe:
    """Un paragraphe obéit à des règles de découpage des lignes. """

    def __init__(self, lignes_initiales=None):
        self.lignes = []
        if lignes_initiales is not None:
            self.lignes.extend(lignes_initiales)

    def est_vide(self):
        return (len(self.lignes) == 0)

    def ajouter_ligne(self, ligne):
        self.lignes.append(ligne)

    def reorganiser_lignes(self):
        LARGEUR_MAX_MM = 160
        LARGEUR_MAX_PREMIERE_LIGNE_MM = 145
        nouvelles_lignes = []

        # Réunir les lignes pour les redécouper selon un critère de largeur.
        texte = " ".join(self.lignes)

        # Parcourir le texte, caractère par caractère.
        ligne_en_cours = ""
        largeur_ligne_mm = 0
        position_dernier_espace = None
        for caractere in texte:

            # Tracer la position des espaces, pour couper le texte.
            if caractere == " ":
                position_dernier_espace = len(ligne_en_cours)

            # Accumuler les caractères de la ligne en cours.
            ligne_en_cours += caractere
            largeur_ligne_mm += CaractereImprimable.evaluer_largeur(caractere)

            # Déterminer la largeur maximale acceptée.
            largeur_max = LARGEUR_MAX_MM
            if len(nouvelles_lignes) == 0:
                largeur_max = LARGEUR_MAX_PREMIERE_LIGNE_MM

            # Gérer le découpage de la ligne en cas de dépassement.
            if largeur_ligne_mm > largeur_max:

                # Identifier une position idéale de coupure.
                if position_dernier_espace is None:
                    position_coupure = len(ligne_en_cours) - 1
                else:
                    position_coupure = position_dernier_espace

                # Découper, puis réinitialiser la ligne en cours.
                nouvelles_lignes.append(ligne_en_cours[:position_coupure])
                ligne_en_cours = ligne_en_cours[position_coupure:].lstrip()
                position_dernier_espace = None
                largeur_ligne_mm = 0
                for c in ligne_en_cours:
                    largeur_ligne_mm += CaractereImprimable.evaluer_largeur(c)

        # Récupérer la dernière ligne, qui n'a pas dépassé la largeur.
        if len(ligne_en_cours) > 0:
            nouvelles_lignes.append(ligne_en_cours)

        # Remplacer les anciennes lignes, après nettoyage des espaces.
        self.lignes = [ligne.strip() for ligne in nouvelles_lignes]


class CaractereImprimable:
    """Un caractère imprimable possède une largeur variable. """

    TAILLE_POLICE_POINTS = 12
    MARGE_SECURITE_POURCENTAGE = 5
    LARGEUR_RELATIVE_MOYENNE = 0.50

    LARGEURS_RELATIVES = {  # Largeurs relatives à une hauteur de 1 point.
        " !\"'()*,-./:;I[\\]fijlrt{|}•": 0.30,  # Caractères étroits.
        "&ABCDEFGHKNPQRSTUVXYZ_mw":      0.60,  # Caractères larges.
        "%@MOW":                         0.75,  # Caractères très larges.
    }

    @classmethod
    def evaluer_largeur_relative(cls, caractere):
        valeur = ord(caractere)
        if valeur <= 31:
            return 0
        if valeur >= 128 and valeur <= 160:
            return 0
        else:
            for categorie_caracteres in cls.LARGEURS_RELATIVES:
                if caractere in categorie_caracteres:
                    return cls.LARGEURS_RELATIVES[categorie_caracteres]
        return cls.LARGEUR_RELATIVE_MOYENNE

    @staticmethod
    def convertir_en_mm(valeur_points):
        return (valeur_points * 25.4 / 72)

    @classmethod
    def evaluer_largeur(cls, caractere):
        largeur_relative = cls.evaluer_largeur_relative(caractere)
        largeur_points = largeur_relative * cls.TAILLE_POLICE_POINTS
        largeur_mm = cls.convertir_en_mm(largeur_points)
        coef_securite = 1 + (cls.MARGE_SECURITE_POURCENTAGE / 100)
        largeur_retenue = largeur_mm * coef_securite
        return largeur_retenue
