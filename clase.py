class Locatie:
    def __init__(self, nume, adresa):
        self.nume = nume
        self.adresa = adresa

class NarghileaLounge(Locatie):
    def __init__(self, nume, adresa, nota):
        super().__init__(nume, adresa)
        self.nota = nota
        
    def __str__(self):
        return f"{self.nume} | Nota: {self.nota}/5 | Adresa: {self.adresa}"
