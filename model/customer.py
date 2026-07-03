from dataclasses import dataclass

@dataclass
class Customer:
    CustomerId: int
    FirstName: str
    LastName: str
    Company: str
    Address: str
    City: str
    State: str
    Country: str
    PostalCode: str
    Phone: str
    Fax: str
    Email: str
    SupportRepId: int
    Fatturato: int


    def __str__(self):
        return f"{self.FirstName} {self.LastName}"

    def __eq__(self, other):
        # SICUREZZA: Controllo che 'other' sia davvero un oggetto di questa classe.
        # Evita i crash se confronti l'oggetto con una stringa o con None.
        if isinstance(other, Customer):
            return self.CustomerId == other.CustomerId
        return False

    def __hash__(self):
        return hash(self.CustomerId)

