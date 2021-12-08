from ..pdf.document import DocumentPDF
from ..pdf.ouverture import OuverturePDF
from ..pdf.page import PageRacinePDF, PagePDF, ContenuPagePDF
from ..pdf.objet import ObjetPDF
from ..pdf.reference import ReferenceObjetPDF
from ..pdf.police import PolicePDF
from ..pdf.mesure import PositionPDF
from ..pdf.texte import BlocTextePDF
from ..pdf.flux import FluxPDF
from ..pdf.catalogue import CataloguePDF
from ..pdf.composant import ComposantPDF
from ..pdf.tableref import TableReferencesPDF
from ..pdf.fermeture import FermeturePDF


class GenerateurDocumentPDF:
    """Encapsule la logique de création d'une structure de document PDF. """

    @classmethod
    def generer_courrier(cls, courrier):
        return cls.generer_document(courrier.document)

    @staticmethod
    def generer_document(document):

        # Ouvrir un document PDF.
        pdf_document = DocumentPDF()
        pdf_document.inserer(OuverturePDF())

        # Insérer une page racine en tant qu'objet interne n°1.
        numero_objet = 1
        pdf_page_racine = PageRacinePDF()
        pdf_objet_racine = ObjetPDF(numero_objet, pdf_page_racine)
        pdf_ref_page_racine = ReferenceObjetPDF(numero_objet)
        pdf_document.inserer(pdf_objet_racine)

        # Insérer les pages filles en tant qu'objets internes.
        pdf_pages = []
        for index_page in range(len(document.pages)):
            numero_objet += 1
            pdf_page = PagePDF()
            pdf_page.definir_page_parente(pdf_ref_page_racine)
            pdf_objet_page = ObjetPDF(numero_objet, pdf_page)
            pdf_ref_page = ReferenceObjetPDF(numero_objet)
            pdf_page_racine.ajouter_page_fille(pdf_ref_page)
            pdf_document.inserer(pdf_objet_page)
            pdf_pages.append(pdf_page)
        pdf_page_racine.finaliser()

        # Insérer les descriptions des polices en tant qu'objets internes.
        pdf_polices = []
        pdf_polices_refs = []
        for index_police in range(len(document.polices)):
            numero_objet += 1
            numero_police = index_police + 1
            police = document.polices[index_police]
            pdf_police = PolicePDF(police.taille, police.serif, police.gras)
            pdf_police.definir_nom_interne(f"Font{numero_police}")
            pdf_police.finaliser()
            pdf_objet_police = ObjetPDF(numero_objet, pdf_police)
            pdf_ref_police = ReferenceObjetPDF(numero_objet)
            pdf_document.inserer(pdf_objet_police)
            pdf_polices.append(pdf_police)
            pdf_polices_refs.append(pdf_ref_police)

        # Insérer le contenu texte.
        # Page par page ...
        for index_page in range(len(document.pages)):
            numero_objet += 1
            page = document.pages[index_page]
            pdf_contenu_page = ContenuPagePDF()

            # ... puis bloc par bloc.
            for index_bloc in range(len(page.blocs)):
                bloc = page.blocs[index_bloc]

                # Identifier la police à utiliser pour ce bloc.
                index_police = document.retrouver_index_police(bloc.police)
                pdf_police = pdf_polices[index_police]
                pdf_ref_police = pdf_polices_refs[index_police]

                # Ajouter cette police aux polices de la page si nécessaire.
                pdf_pages[index_page].definir_police(
                    pdf_police, pdf_ref_police)

                # Démarrer un nouveau bloc de texte à la position souhaitée.
                pdf_position_texte = PositionPDF(bloc.droite, bloc.bas)
                pdf_bloc_texte = BlocTextePDF(pdf_position_texte, pdf_police)

                # Ecrire chaque ligne de texte dans le bloc.
                for ligne in bloc.lignes:
                    pdf_bloc_texte.inserer(ligne.texte)

                # Insérer le bloc dans le contenu de la page PDF.
                pdf_contenu_page.inserer(pdf_bloc_texte)

            # Finaliser le contenu de la page et l'encapsuler dans un flux PDF.
            pdf_contenu_page.finaliser()
            pdf_flux_page = FluxPDF()
            pdf_flux_page.inserer(pdf_contenu_page)
            pdf_flux_page.finaliser()

            # Référencer ce flux et le désigner aux pages qui vont l'héberger.
            pdf_objet_flux_page = ObjetPDF(numero_objet, pdf_flux_page)
            pdf_ref_flux_page = ReferenceObjetPDF(numero_objet)
            pdf_pages[index_page].definir_contenu(pdf_ref_flux_page)
            pdf_pages[index_page].finaliser()
            pdf_document.inserer(pdf_objet_flux_page)

        # Construire le catalogue et l'insérer en tant qu'objet interne.
        numero_objet += 1
        pdf_catalogue = CataloguePDF()
        pdf_catalogue.definir_page_racine(pdf_ref_page_racine)
        pdf_catalogue.finaliser()
        pdf_objet_catalogue = ObjetPDF(numero_objet, pdf_catalogue)
        pdf_ref_catalogue = ReferenceObjetPDF(numero_objet)
        pdf_document.inserer(pdf_objet_catalogue)

        # Capturer les positions internes des objets insérés jusqu'ici,
        # ainsi que la position finale (pour insérer la table des références).
        positions_internes = pdf_document.lire_positions_internes()
        position_table = positions_internes[DocumentPDF.CLE_POSITION_FIN]

        # Insérer le dernier composant pour la table des références + fermeture.
        pdf_fin_document = ComposantPDF(separateur=DocumentPDF.SAUT_LIGNE)
        pdf_document.inserer(pdf_fin_document)

        # Constuire et insérer la table des références vers les objets internes.
        pdf_table = TableReferencesPDF()
        for numero_objet in positions_internes:
            if numero_objet != DocumentPDF.CLE_POSITION_FIN:
                pdf_table.ajouter_entree(positions_internes[numero_objet])
        pdf_table.finaliser()
        taille_table = pdf_table.lire_nombre_entrees()
        pdf_fin_document.inserer(pdf_table)

        # Construire et insérer la séquence de fermeture.
        pdf_fermeture = FermeturePDF(
            taille_table, position_table, pdf_ref_catalogue)
        pdf_fin_document.inserer(pdf_fermeture)

        # Retourner la structure du document PDF complet.
        return pdf_document
