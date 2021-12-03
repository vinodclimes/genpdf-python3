from generateur.pdf.document import DocumentPDF
from generateur.pdf.flux import FluxPDF
from generateur.pdf.mesure import PositionPDF
from generateur.pdf.ouverture import OuverturePDF
from generateur.pdf.page import ContenuPagePDF, PageRacinePDF, PagePDF
from generateur.pdf.objet import ObjetPDF
from generateur.pdf.police import PolicePDF
from generateur.pdf.reference import ReferenceObjetPDF
from generateur.pdf.catalogue import CataloguePDF
from generateur.pdf.tableref import TableReferencesPDF
from generateur.pdf.composant import ComposantPDF
from generateur.pdf.fermeture import FermeturePDF
from generateur.pdf.texte import BlocTextePDF


def construire_pdf_test():

    # Ouvrir un document
    document_pdf = DocumentPDF()
    document_pdf.inserer(OuverturePDF())

    # Insérer une page racine en tant qu'objet interne n°1
    page_racine = PageRacinePDF()
    objet_racine = ObjetPDF(1, page_racine)
    ref_page_racine = ReferenceObjetPDF(1)
    document_pdf.inserer(objet_racine)

    # Insérer une page fille en tant qu'objet interne n°2
    page = PagePDF()
    page.definir_page_parente(ref_page_racine)
    objet_page = ObjetPDF(2, page)
    ref_page = ReferenceObjetPDF(2)
    document_pdf.inserer(objet_page)

    # Refermer la référence bidirectionnelle entre page racine et page fille
    page_racine.ajouter_page_fille(ref_page)
    page_racine.finaliser()

    # Insérer une description de police en tant qu'objet interne n°3
    police = PolicePDF(16, serif=False, gras=True)
    police.definir_nom_interne("Font1")
    police.finaliser()
    objet_police = ObjetPDF(3, police)
    ref_police = ReferenceObjetPDF(3)
    document_pdf.inserer(objet_police)

    # Créer le contenu d'une page en tant qu'objet interne n°4
    position_texte = PositionPDF(25, 50)
    texte = BlocTextePDF(position_texte, police)
    texte.inserer("Ceci est un document PDF de démonstration. ")
    contenu_page = ContenuPagePDF()
    contenu_page.inserer(texte)
    contenu_page.finaliser()
    flux_page = FluxPDF()
    flux_page.inserer(contenu_page)
    flux_page.finaliser()
    objet_flux_page = ObjetPDF(4, flux_page)
    ref_flux_page = ReferenceObjetPDF(4)
    document_pdf.inserer(objet_flux_page)

    # Terminer la définition de la page fille
    page.definir_police(police, ref_police)
    page.definir_contenu(ref_flux_page)
    page.finaliser()

    # Insérer un catalogue en tant qu'objet interne n°5
    catalogue = CataloguePDF()
    catalogue.definir_page_racine(ref_page_racine)
    catalogue.finaliser()
    objet_catalogue = ObjetPDF(5, catalogue)
    ref_catalogue = ReferenceObjetPDF(5)
    document_pdf.inserer(objet_catalogue)

    # Capturer les positions internes des objets insérés jusqu'ici (n°1 à 5),
    # ainsi que la position finale (pour insertion de la table des références).
    positions_internes = document_pdf.lire_positions_internes()
    position_table = positions_internes[DocumentPDF.CLE_POSITION_FIN]

    # Insérer le dernier composant, pour la table des références + fermeture
    fin_document = ComposantPDF(separateur=DocumentPDF.SAUT_LIGNE)
    document_pdf.inserer(fin_document)

    # Constuire et insérer une table des références vers les objets internes
    table = TableReferencesPDF()
    table.ajouter_entree(positions_internes[1])
    table.ajouter_entree(positions_internes[2])
    table.ajouter_entree(positions_internes[3])
    table.ajouter_entree(positions_internes[4])
    table.ajouter_entree(positions_internes[5])
    table.finaliser()
    taille_table = table.lire_nombre_entrees()
    fin_document.inserer(table)

    # Construire et insérer la séquence de fermeture
    fermeture = FermeturePDF(taille_table, position_table, ref_catalogue)
    fin_document.inserer(fermeture)

    # Retourner le document complet
    return document_pdf


if __name__ == "__main__":

    document_pdf = construire_pdf_test()
    nom_fichier_pdf = "exemple.pdf"

    nombre_octets_ecrits = 0
    with open(nom_fichier_pdf, "wb") as fichier:
        nombre_octets_ecrits = fichier.write(bytes(document_pdf))

    print(f"Nombre d'octets écrits : {nombre_octets_ecrits}. ")
