from .paragraphe import Paragraphe
from ..document.courrier import Courrier


class Description:
    """Un fichier de description de document.

    Le format de description est un format texte permettant de construire
    un dictionnaire de clés/valeurs dont les valeurs sont des lignes de texte.

    Par exemple, la clé "Infos" est ajoutée via la ligne : [Infos]
    Toutes les lignes de texte suivantes, jusqu'à la prochaine ligne vide,
    sont chargées en tant que liste dans cette clé du dictionnaire.

    Si une clé est déclarée plusieurs fois, ses lignes de texte s'accumulent.

    Les lignes de texte qui ne sont pas précédées d'une clé spécifique,
    mais d'une ou plusieurs lignes vides, sont chargées en tant que paragraphe.

    Dans ce cas, la fin d'un paragraphe est marquée par une ligne vide,
    et chaque nouveau bloc de lignes non précédé d'une clé constitue
    un nouveau paragraphe dans le document.

    Exemple : document avec 2 clés (adresse et pagination) et 2 paragraphes

        [adresse]
        42, rue Principale
        75001 Paris

        Ceci est le premier
        paragraphe du document.

        Ceci est le deuxième
        paragraphe du document.

        [pagination]
        (page 1/1)

    """

    ENCODAGE_FICHIER = "utf_8"
    PREFIXE_CLE = "["
    SUFFIXE_CLE = "]"
    CLE_PARAGRAPHES = "paragraphes"

    @classmethod
    def lire_cles_valeurs_fichier(cls, chemin_fichier):
        cles_valeurs = {}
        cles_valeurs[cls.CLE_PARAGRAPHES] = [Paragraphe()]
        cle_courante = cls.CLE_PARAGRAPHES
        with open(chemin_fichier,
                  encoding=cls.ENCODAGE_FICHIER, errors="strict") as fichier:
            ligne = fichier.readline()
            while len(ligne) > 0:
                ligne = ligne.strip()

                if len(ligne) == 0:
                    cle_courante = cls.CLE_PARAGRAPHES
                    paragraphes = cles_valeurs[cls.CLE_PARAGRAPHES]
                    cls.terminer_dernier_paragraphe(paragraphes)
                else:
                    cle = cls.lire_cle(ligne)
                    if cle is not None:
                        cle_courante = cle
                        if cle_courante not in cles_valeurs:
                            cles_valeurs[cle_courante] = []
                    else:
                        if cle_courante == cls.CLE_PARAGRAPHES:
                            paragraphes = cles_valeurs[cls.CLE_PARAGRAPHES]
                            dernier_paragraphe = paragraphes[-1]
                            dernier_paragraphe.ajouter_ligne(ligne)
                        else:
                            cles_valeurs[cle_courante].append(ligne)

                ligne = fichier.readline()
        return cles_valeurs

    @staticmethod
    def terminer_dernier_paragraphe(paragraphes):
        dernier_paragraphe = paragraphes[-1]
        if not dernier_paragraphe.est_vide():
            nouveau_paragraphe = Paragraphe()
            paragraphes.append(nouveau_paragraphe)

    @classmethod
    def lire_cle(cls, ligne):
        cle = None
        if (len(ligne) > 2
                and ligne[0] == cls.PREFIXE_CLE
                and ligne[-1] == cls.SUFFIXE_CLE):
            cle = ligne[1:-1]
        return cle

    def __init__(self, chemin_fichier):
        self.cles_valeurs = self.lire_cles_valeurs_fichier(chemin_fichier)


class DescriptionCourrier(Description):
    """Description d'un courrier et de ses clés spécifiques. """

    CLE_NOM_EXPEDITEUR = "expediteur-nom"
    CLE_ADRESSE_EXPEDITEUR = "expediteur-adresse"
    CLE_CONTACT_EXPEDITEUR = "expediteur-contact"
    CLE_ADRESSE_DESTINATAIRE = "destinataire"
    CLE_LIEU_DATE = "lieu-date"
    CLE_OBJET_PJ = "objet-pj"
    CLE_FORMULE_APPEL = "formule-appel"
    CLE_FORMULE_POLITESSE = "formule-politesse"
    CLE_NOM_SIGNATAIRE = "signature-nom"

    def __init__(self, chemin_fichier):
        super().__init__(chemin_fichier)

    def preparer_courrier(self):
        """Utiliser les clés présentes pour constuire un Courrier.

        La structure de type Courrier précise une mise en page standard
        permettant ensuite de traduire un courrier en document de type PDF.
        """

        courrier = Courrier()

        # Nom de l'expéditeur.
        if self.CLE_NOM_EXPEDITEUR in self.cles_valeurs:
            lignes = self.cles_valeurs[self.CLE_NOM_EXPEDITEUR]
            if len(lignes) > 0:
                valeur = lignes[-1]
                courrier.ajouter_nom_expediteur(valeur)

        # Adresse de l'expéditeur.
        if self.CLE_ADRESSE_EXPEDITEUR in self.cles_valeurs:
            lignes = self.cles_valeurs[self.CLE_ADRESSE_EXPEDITEUR]
            if len(lignes) > 0:
                courrier.ajouter_adresse_expediteur(lignes)

        # Informations de contact de l'expéditeur.
        if self.CLE_CONTACT_EXPEDITEUR in self.cles_valeurs:
            lignes = self.cles_valeurs[self.CLE_CONTACT_EXPEDITEUR]
            if len(lignes) > 0:
                courrier.ajouter_contact_expediteur(lignes)

        # Adresse du destinataire.
        if self.CLE_ADRESSE_DESTINATAIRE in self.cles_valeurs:
            lignes = self.cles_valeurs[self.CLE_ADRESSE_DESTINATAIRE]
            if len(lignes) > 0:
                courrier.ajouter_adresse_destinataire(lignes)

        # Lieu et date d'écriture du courrier.
        if self.CLE_LIEU_DATE in self.cles_valeurs:
            lignes = self.cles_valeurs[self.CLE_LIEU_DATE]
            if len(lignes) > 0:
                valeur = lignes[-1]
                courrier.ajouter_lieu_date(valeur)

        # Lignes d'objet, de PJ, de référence, etc.
        if self.CLE_OBJET_PJ in self.cles_valeurs:
            lignes = self.cles_valeurs[self.CLE_OBJET_PJ]
            if len(lignes) > 0:
                courrier.ajouter_objet(lignes)

        # Formule d'appel (ex: Madame, Monsieur,).
        if self.CLE_FORMULE_APPEL in self.cles_valeurs:
            lignes = self.cles_valeurs[self.CLE_FORMULE_APPEL]
            if len(lignes) > 0:
                valeur = lignes[-1]
                courrier.ajouter_formule_appel(valeur)

        # Paragraphes successifs formant le corps du courrier.
        for paragraphe in self.cles_valeurs[self.CLE_PARAGRAPHES]:
            if not paragraphe.est_vide():
                paragraphe.reorganiser_lignes()
                courrier.ajouter_paragraphe(paragraphe.lignes)

        # Formule de politesse (dernier paragraphe).
        if self.CLE_FORMULE_POLITESSE in self.cles_valeurs:
            lignes = self.cles_valeurs[self.CLE_FORMULE_POLITESSE]
            paragraphe = Paragraphe(lignes)
            if not paragraphe.est_vide():
                paragraphe.reorganiser_lignes()
                courrier.ajouter_formule_politesse(paragraphe.lignes)

        # Nom du signataire.
        if self.CLE_NOM_SIGNATAIRE in self.cles_valeurs:
            lignes = self.cles_valeurs[self.CLE_NOM_SIGNATAIRE]
            if len(lignes) > 0:
                valeur = lignes[-1]
                courrier.ajouter_nom_signataire(valeur)

        return courrier
