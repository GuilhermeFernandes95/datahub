# Create resource object as database.schema.table

class Path:
    platform = 'Metabase'  # 1st version only considers Metabase tools
    separator = '/'

    def __init__(self,
                 department: str,
                 sub_folders: str,
                 title: str) -> object:
        self.type = self.platform
        self.department = department
        self.sub_folders = sub_folders
        self.title = title

    def __str__(self) -> str:
        return f"Path built: {self.platform}/{self.department}/{self.sub_folders}/{self.title}"

    # Instance methods
    def get_urn_path(self) -> str:
        return ','.join([self.platform, self.title])

    def _set_sub_folder(self, sub_folder) -> object:
        self.sub_folder = sub_folder

    def _get_path(self, i) -> str:
        return self.separator.join(
            ['', self.platform, self.department,
             self.sub_folders.split(';')[i], self.title]  # to get department specific <sub_folder>
        )  # empty string given to add a <separator> at the beginning

    @staticmethod
    def get_path_entries(paths: list) -> str:
        return ',\n'.join((f'"{w}"' for w in list(
            map(lambda x: (x[1]._get_path(i=x[0])), enumerate(paths)))))  # return each path surrounded by double quotes