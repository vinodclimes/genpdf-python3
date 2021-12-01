from generateur.pdf.ouverture import OuverturePDF
from generateur.pdf.page import PageRacinePDF, PagePDF
from generateur.pdf.objet import ObjetPDF
from generateur.pdf.reference import ReferenceObjetPDF
from generateur.pdf.assistant import FIN_LIGNE, en_octets
from generateur.pdf.catalogue import CataloguePDF
from generateur.pdf.tableref import TableReferencesPDF
from generateur.pdf.dictionnaire import DictionnairePDF
from generateur.pdf.nom import NomPDF
from generateur.pdf.fermeture import FermeturePDF


def construire_pdf_vide():

    ouverture = OuverturePDF()

    page_racine = PageRacinePDF()
    objet_racine = ObjetPDF(1, page_racine)
    ref_page_racine = ReferenceObjetPDF(1)

    page = PagePDF(ref_page_racine)
    objet_page = ObjetPDF(2, page)
    ref_page = ReferenceObjetPDF(2)

    page_racine.ajouter_page_fille(objet_page)

    catalogue = CataloguePDF(ref_page_racine)
    objet_catalogue = ObjetPDF(3, catalogue)
    ref_catalogue = ReferenceObjetPDF(3)

    octets = b""
    position = 0

    position_ouverture = position
    octets_ouverture = ouverture.lire_octets()
    octets += octets_ouverture
    position += len(octets_ouverture)

    octets += FIN_LIGNE
    position += len(FIN_LIGNE)

    position_racine = position
    octets_racine = objet_racine.lire_octets()
    octets += octets_racine
    position += len(octets_racine)

    octets += FIN_LIGNE
    position += len(FIN_LIGNE)

    position_page = position
    octets_page = objet_page.lire_octets()
    octets += octets_page
    position += len(octets_page)

    octets += FIN_LIGNE
    position += len(FIN_LIGNE)

    position_catalogue = position
    octets_catalogue = objet_catalogue.lire_octets()
    octets += octets_catalogue
    position += len(octets_catalogue)

    octets += FIN_LIGNE
    position += len(FIN_LIGNE)

    position_table = position

    table = TableReferencesPDF(position_table)
    table.ajouter_reference(position_racine)
    table.ajouter_reference(position_page)
    table.ajouter_reference(position_catalogue)

    octets_table = table.lire_octets()
    octets += octets_table
    position += len(octets_table)

    octets += FIN_LIGNE
    position += len(FIN_LIGNE)

    position_fermeture = position

    dico_fermeture = DictionnairePDF()
    dico_fermeture.ajouter(
        NomPDF("Size"), en_octets(len(table.references) + 1))
    dico_fermeture.ajouter(
        NomPDF("Root"), ref_catalogue.lire_octets())

    fermeture = FermeturePDF(table, dico_fermeture)
    octets_fermeture = fermeture.lire_octets()
    octets += octets_fermeture
    position += len(octets_fermeture)

    return octets


if __name__ == "__main__":

    nom_fichier_pdf = "exemple.pdf"

    nombre_octets = 0
    with open(nom_fichier_pdf, "wb") as fichier:
        octets = construire_pdf_vide()
        nombre_octets = fichier.write(octets)

    print(f"Nombre d'octets écrits : {nombre_octets}. ")
