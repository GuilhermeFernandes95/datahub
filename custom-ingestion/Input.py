# Create resource object as database.schema.table

class Input:
    input_type = 'dataset'  # only type needed for a first versions

    def __init__(self,
                 database: str,
                 schema: str,
                 table: str) -> object:
        self.database = database
        self.schema = schema
        self.table = table
        self.type = self.input_type

    def __str__(self) -> str:
        return f"Input type: {self.type} - '{self.table}' table, from '{self.schema}' 'schema and database '{self.database}'"

    # Instance methods
    def _get_path(self) -> str:
        return '.'.join([self.database, self.schema, self.table])

    def _get_input_entry(self) -> str:
        return f"{{\"string\": \"urn:li:{self.type}:(urn:li:dataPlatform:prod,{self._get_path()},PROD)\"}}"

    @staticmethod
    def get_input_entries(inputs: list, snapshot_type: str) -> str:
        if snapshot_type == 'chart':
            return ',"inputs": [' + ',\n'.join(list(map(lambda x: x._get_input_entry(), inputs))) + ']'
        else:
            return ''
