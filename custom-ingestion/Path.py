# Create resource object as database.schema.table

class Path:
    platform = 'Metabase'  # 1st version only considers Metabase tools
    separator = '/'

    def __init__(self,
                 department: str,
                 sub_folders: str,
                 resource_number: int,
                 title: str) -> object:
        self.platform = self.platform
        self.department = department
        self.sub_folders = sub_folders
        self.resource_number = resource_number
        self.title = title

    def __str__(self) -> str:
        return f"Path built: {self.platform}/{self.department}/{self.sub_folders}/{self.title}"

    # Instance methods
    def _get_path(self, i, id) -> str:
        i = 0 if len(self.sub_folders.split(';')) == 1 else i

        # to get department specific <sub_folder>
        try:
            return self.separator.join(
                ['', self.platform, self.department, self.sub_folders.split(';')[i], id]
            )  # empty string given to add a <separator> at the beginning
        except Exception as e:
            print(f"{e} ---- Departments and paths given do not match the expected ----")
