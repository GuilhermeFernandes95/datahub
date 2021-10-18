from Snapshot import Snapshot


class Dashboard(Snapshot):
    platform = 'Metabase'  # 1st version only considers Metabase tools

    def __init__(self,
                 number: int,
                 title: str,
                 description: str,
                 documentation: object,
                 link: str,
                 owners: list,
                 tags: list,
                 paths: list,
                 inputs: list = '') -> str:
        super().__init__(number, title, description, documentation, link, owners, inputs, tags, paths)
        self.type = Dashboard.__name__

    # Instance methods
    def get_urn_path(self) -> str:
        return ','.join([self.platform, ' '.join([self.platform, Dashboard.__name__, str(self.number)])])