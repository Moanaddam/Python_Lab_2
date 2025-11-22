
from datetime import datetime
from typing import List, Tuple, Union

class CompteBancaire:
    _prochain_id = 1000

    def __init__(self, solde_initial: float = 0.0):
        self.__solde = float(solde_initial)
        self._operations: List[Tuple[str, float, str]] = []
        self.id = CompteBancaire._prochain_id
        CompteBancaire._prochain_id += 1

    def _journaliser_operation(self, type_op: str, montant: float, statut: str):
        horodatage = datetime.now().isoformat(timespec="seconds")
        self._operations.append((type_op, montant, statut, horodatage))

    def deposer(self, montant: Union[int, float]):
        if montant > 0:
            self.__solde += montant
            self._journaliser_operation("DEPOT", montant, "OK")
        else:
            raise ValueError("Le montant du dépôt doit être positif.")

    def retirer(self, montant: Union[int, float]):
        if montant <= 0:
            raise ValueError("Le montant du retrait doit être positif.")
        
        if montant <= self.__solde:
            self.__solde -= montant
            self._journaliser_operation("RETRAIT", montant, "OK")
        else:
            self._journaliser_operation("RETRAIT", montant, "ECHEC")
            raise ValueError(f"Fonds insuffisants. Solde actuel : {self.get_solde()} €")

    def get_solde(self) -> float:
        return self.__solde

    def generer_releve(self) -> None:
        print(f"\nRelevé du compte #{self.id} :")
        if not self._operations:
            print("Aucune opération enregistrée.")
            return

        for type_op, montant, statut, horodatage in self._operations:
            print(f"[{horodatage}] {type_op:<8} | {montant:>8.2f} € | Statut: {statut}")
        print("-" * 40)


class Client:

    def __init__(self, nom: str):
        self.nom = nom
        self.comptes: List[CompteBancaire] = []

    def ouvrir_compte(self, solde_initial: float = 0.0) -> CompteBancaire:
        nouveau_compte = CompteBancaire(solde_initial)
        self.comptes.append(nouveau_compte)
        print(f"Compte #{nouveau_compte.id} ouvert pour {self.nom} avec un solde de {solde_initial:.2f} €.")
        return nouveau_compte

    def afficher(self):
        solde_total = sum(compte.get_solde() for compte in self.comptes)
        print(f"\nClient : {self.nom}")
        print(f"Nombre de comptes : {len(self.comptes)}")
        print(f"Solde total consolidé : {solde_total:.2f} €")
        
        if len(self.comptes) > 0:
            print("\nDétail des comptes:")
            for compte in self.comptes:
                print(f"  Compte #{compte.id} (Solde: {compte.get_solde():.2f} €)")


if __name__ == "__main__":
    
    print("--- Test de l'association par Composition ---")

    cli = Client("Yassir")

    compte_principal = cli.ouvrir_compte(solde_initial=100.0)

    compte_principal.deposer(300)
    
    try:
        compte_principal.retirer(50)
    except ValueError as e:
        print(f"Erreur d'opération: {e}")

    print(f"\nRésultat attendu : Client : Yassir, Solde : {compte_principal.get_solde():.1f}€")

    cli.afficher()
    
    compte_epargne = cli.ouvrir_compte(solde_initial=500.0)
    compte_epargne.deposer(50)
    
    cli.afficher()

    compte_principal.generer_releve()
    compte_epargne.generer_releve()