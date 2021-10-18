import yaml


class Documentation:

    def __init__(self,
                 title: str,
                 description: str,
                 extended_description: str,
                 caveats: str,
                 special_instructions: str) -> object:
        with open(r'config.yml') as file:
            config = yaml.load(file, Loader=yaml.FullLoader)
            split_sep = config['configurations']['split']
        self.title = title
        self.description = description
        self.extended_description = extended_description
        self.caveats = caveats.split(split_sep) if not isinstance(caveats, float) else ['None']
        self.special_instructions = special_instructions.split(split_sep) if not isinstance(special_instructions,
                                                                                            float) else ['None']
        self.markdown = config['documentation']['markdown']

    def __str__(self):
        return f'Title - Description: {self.title} - {self.description} \n' \
               f'Caveats: {self.caveats} \n' \
               f'Special Instructions: {self.special_instructions} \n'

    def _build_title(self):
        return ''.join([self.markdown['bold'], self.title, self.markdown['bold']])

    def _build_description(self):
        return f"{self.markdown['italic']}{self.description}{self.markdown['italic']}\\n{self.markdown['hr']}"

    def _build_extended_description(self):
        return ''.join([self.markdown['quote'],self.extended_description])

    @staticmethod
    def _build_points(points: list, point_type: str = 'bullet'):
        if point_type == 'bullet':
            return '\\n'.join(['- ' + p.strip() for p in points])
        elif point_type == 'number':
            return '\\n'.join([str(i + 1) + '. ' + p.strip() for i, p in enumerate(points)])
        else:
            raise ValueError('---- Point Type not Recognized ----')

    def _build_caveats_instructions(self):
        return '\\n'.join([f"{self.markdown['bold']}Caveats{self.markdown['bold']}",
                           Documentation._build_points(points=self.caveats),
                           f"\\n{self.markdown['bold']}Special Instructions{self.markdown['bold']}\\n",
                           Documentation._build_points(points=self.special_instructions,
                                                       point_type='number')
                           ])

    def build_documentation(self):
        return '\\n'.join([self._build_title(),
                           self._build_description(),
                           self._build_extended_description(),
                           self._build_caveats_instructions()
                           ])
