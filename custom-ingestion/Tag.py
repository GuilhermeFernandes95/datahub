class Tag:

    def __init__(self,
                 name: str) -> object:
        self.name = name.capitalize()

    def __str__(self) -> str:
        return f"Tag Name: {self.name}"

    # Instance methods
    def _get_tag_entry(self) -> str:
        return f'{{"tag": "urn:li:tag:{self.name}"}}'
