from Snapshot import Snapshot


class Dashboard(Snapshot):
    snapshot_type = 'Dashboard'

    def __init__(self,
                 number: int,
                 title: str,
                 description: str,
                 link: str,
                 owners: list,
                 inputs: list,
                 paths: list) -> object:
        super().__init__(number, title, description, link, owners, inputs, paths)
        self.type = self.snapshot_type
