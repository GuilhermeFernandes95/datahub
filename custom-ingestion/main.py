import pandas as pd
import yaml
import os
from Chart import Chart
from Dashboard import Dashboard
from Documentation import Documentation
from Input import Input
from Path import Path
from Owner import Owner
from Tag import Tag
from Snapshot import Snapshot
from pathlib import Path as wd


def build_snapshot(instance, snapshot_type, split_separator, cols):
    snapshots.append(
        snapshot_type(number=instance[cols['number']],
                      title=instance[cols['title']],
                      description=instance[cols['description']],
                      documentation=Documentation(title=instance[cols['title']],
                                                  description=instance[cols['description']],
                                                  extended_description=instance[cols['extended_description']],
                                                  caveats=instance[cols['caveats']],
                                                  special_instructions=instance[cols['special_instructions']]),
                      link=instance[cols['link']],
                      owners=[Owner(name=x.strip(),
                                    roles=instance[cols['roles']]) for x in
                              instance[cols['owners']].split(split_sep)
                              ] if not isinstance(instance[cols['owners']], float) else '',
                      tags=[Tag(name=x.strip()) for x in instance[cols['tags']].split(split_separator)
                            ] if not isinstance(instance[cols['tags']], float) else '',
                      paths=[Path(department=x.strip(),
                                  sub_folders=instance[cols['sub_folders']],
                                  resource_number=instance[cols['number']],
                                  title=instance[cols['title']]) for x in
                             instance[cols['department']].split(split_separator)]

                      )
    )

    if snapshot_type == Chart:
        snapshots[-1].inputs = [Input(database=row['database'],
                                      schema=row['schema'],
                                      table=x.strip()) for x in row['tables'].split(split_sep)
                                ] if not isinstance(row['tables'], float) else ''

    return snapshots


# MCE is a Metadata Change Event JSON with specific structure to feed DataHub with legacy (or custom) data
def generate_mce(json_template: dict,
                 snapshot_list: list,
                 input_placeholder: str):
    content = json_template.read()
    json_template.seek(0)
    mce = []
    for snapshot in snapshot_list:
        mce.append(
            content.replace('$upper_snapshot$', snapshot.type.capitalize())
                .replace('$lower_snapshot$', snapshot.type.lower())
                .replace('$snapshot_id$', snapshot.get_urn_path())
                .replace('$resource_link$', snapshot.link)
                .replace('$resource_title$', snapshot.title)
                .replace('$resource_description$', snapshot.description)
                .replace('$documentation$', snapshot.documentation.build_documentation())
                .replace('"$inputs$"', Snapshot.get_input_entries(snapshot.inputs, snapshot.type.lower()))
                .replace('"$owners$"', Snapshot.get_owner_entries(snapshot.owners))
                .replace('"$paths$"', Snapshot.get_path_entries(snapshot.paths, snapshot.get_urn_path()))
                .replace('"$tags$"', Snapshot.get_tag_entries(snapshot.tags))
                .replace(input_placeholder, '')  # Dashboard stopped supporting 'input'
        )

    return mce


if __name__ == '__main__':
    os.chdir(wd(__file__).resolve().parents[0])  # change working directory
    with open(r'config.yml') as file:
        config = yaml.load(file, Loader=yaml.FullLoader)
        split_sep = config['configurations']['split']
        columns = config['configurations']['columns']

    df = pd.read_csv(config['configurations']['resource_file'], sep=',')  # ideally would read from google sheet
    snapshots = []

    for index, row in df.iterrows():
        if row['resource_type'].lower() == 'question':
            snapshots = build_snapshot(row, Chart, split_sep, columns)
        elif row['resource_type'].lower() == 'dashboard':
            snapshots = build_snapshot(row, Dashboard, split_sep, columns)
        else:
            raise ValueError('---- Resource Type not Recognized. Check the input file ----')

    template = open('template.json', 'r+')
    mces = generate_mce(template, snapshots, config['configurations']['input_placeholder'])

    output = ',\n'.join(mces)
    output = '\n'.join(('[', output, ']'))

    with open("output.json", "w") as text_file:
        text_file.write(output)
