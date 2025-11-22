from datetime import datetime
from typing import List, Tuple, Union

class CompteBancaire:

    def __init__(self, titulaire: str, solde_initial: float = 0.0):
        self._titulaire = titulaire
        self.__solde = float(solde_initial)
        self._operations: List[Tuple[str, float, str]] = []

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
            self._journaliser_operation("RETRAIT", montant, "ECHEC: Fonds Insuffisants")
            raise ValueError(f"Fonds insuffisants. Solde actuel : {self.solde} €")

    @property
    def solde(self) -> float:
        return self.__solde

    def afficher_historique(self):
        print(f"\n--- Historique des opérations pour {self._titulaire} ---")
        for type_op, montant, statut, horodatage in self._operations:
            print(f"[{horodatage}] {type_op} {montant} € ({statut})")

    def __str__(self):
        return f"Titulaire : {self._titulaire}, Solde : {self.solde:.2f} €"

class CompteEpargne(CompteBancaire):

    def __init__(self, titulaire: str, solde_initial: float = 0.0, taux_interet_annuel: float = 0.03):
        super().__init__(titulaire, solde_initial)
        
        if taux_interet_annuel < 0:
            raise ValueError("Le taux d'intérêt ne peut pas être négatif.")
            
        self._taux_annuel = taux_interet_annuel
        
    def calculer_interet(self) -> float:
        """Calcule et ajoute l'intérêt annuel au solde."""
        interets = self.solde * self._taux_annuel
        
        self.deposer(interets)
        self._journaliser_operation("INTERETS", interets, "OK")
        
        return interets

    def __str__(self):
        parent_str = super().__str__()
        return f"{parent_str} (Taux : {self._taux_annuel * 100:.2f} %)"


if __name__ == "__main__":
    
    print("--- Test du CompteBancaire standard ---")
    compte = CompteBancaire("Ali", 1000)
    
    compte.deposer(200)
    compte.retirer(150)
    
    print(compte)
    print("Solde accessible (lecture) :", compte.solde)

    print("\n--- Tentative de modification directe du solde ---")
    try:
        compte.solde = 500  
    except AttributeError as e:
        print("Erreur capturée :", e) 
    except Exception as e:
        print("Erreur inattendue :", e)

    print(f"Solde final après tentative d'affectation : {compte.solde} € (inchangé)")

    compte.afficher_historique()

    print("\n" + "="*50)
    print("--- Test de la classe CompteEpargne ---")
    
    compte_epargne = CompteEpargne("Sara", 5000, 0.05)
    print(compte_epargne)

    try:
        compte_epargne.retirer(6000)
    except ValueError as e:
        print(f"Retrait impossible capturé : {e}")

    interets = compte_epargne.calculer_interet()
    print(f"Intérêts calculés (5% de 5000 €) : {interets:.2f} €")
    print(compte_epargne)
    
    compte_epargne.afficher_historique()