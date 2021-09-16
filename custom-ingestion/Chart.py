from Snapshot import Snapshot


class Chart(Snapshot):
    snapshot_type = 'Chart'
    platform = 'Metabase'  # 1st version only considers Metabase tools

    def __init__(self,
                 number: int,
                 title: str,
                 description: str,
                 link: str,
                 owners: list,
                 inputs: list,
                 tags: list,
                 paths: list) -> object:
        super().__init__(number, title, description, link, owners, inputs, tags, paths)
        self.type = self.snapshot_type

    # Instance methods
    def get_urn_path(self) -> str:
        return ','.join([self.platform, ' '.join([self.platform, 'Question', str(self.number)])])
