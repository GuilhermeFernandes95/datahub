# Create resource object as database.schema.table

class Path:
    platform = 'Metabase'  # 1st version only considers Metabase tools
    separator = '/'

    def __init__(self,
                 department: str,
                 sub_folders: str,
                 title: str) -> object:
        self.platform = self.platform
        self.department = department
        self.sub_folders = sub_folders
        self.title = title

    def __str__(self) -> str:
        return f"Path built: {self.platform}/{self.department}/{self.sub_folders}/{self.title}"

    # Instance methods
    def _get_path(self, i) -> str:
        i = 0 if len(self.sub_folders.split(';')) == 1 else i
        _title = self.title.replace("/", "")  # to ensure that path is properly built

        # to get department specific <sub_folder>
        try:
            return self.separator.join(
                ['', self.platform, self.department, self.sub_folders.split(';')[i], _title]
            )  # empty string given to add a <separator> at the beginning
        except Exception as e:
            print(f"{e} ---- Departments and paths given do not match the expected ----")

    # Maybe using the question number instead of title
    # Only one id per entity, so no issue with repeated numbers
    def get_urn_path(self) -> str:
        return ','.join([self.platform, self.title])

    @staticmethod
    def get_path_entries(paths: list) -> str:
        return ',\n'.join((f'"{w}"' for w in list(
            map(lambda x: (x[1]._get_path(i=x[0])), enumerate(paths)))))  # return each path surrounded by double quotes
