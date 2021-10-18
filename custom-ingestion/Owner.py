# Create resource object as database.schema.table

class Owner:

    def __init__(self,
                 name: str,
                 roles: str) -> object:
        self.name = name
        self.roles = roles

    def __str__(self) -> str:
        return f"Owner name: '{self.name}. Owner role: {self.roles}"

    # Instance methods
    def _get_owner_entry(self, i) -> str:
        i = 0 if len(self.roles.split(';')) == 1 else i
        try:
            return f"{{\"owner\": \"urn:li:corpuser:{self.name}\", \"type\": \"{self.roles.split(';')[i].upper()}\"}}"
        except Exception as e:
            print(f"{e} ---- Owners and roles given do not match the expected ----")
