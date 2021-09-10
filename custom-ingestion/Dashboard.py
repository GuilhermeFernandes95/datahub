from Snapshot import Snapshot


class Dashboard(Snapshot):
    snapshot_type = 'Dashboard'

    def __init__(self,
                 number: int,
                 title: str,
                 description: str,
                 link: str,
                 owner: list,
                 inputs: list) -> object:
        super().__init__(number, title, description, link, owner, inputs)
        self.type = self.snapshot_type
