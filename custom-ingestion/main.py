import pandas as pd
import os
from Chart import Chart
from Dashboard import Dashboard
from Input import Input
from Path import Path
from Owner import Owner
from Tag import Tag
from pathlib import Path as wd

split_sep = ';'  # Define in a YAML file
input_placeholder = ',"$input_placeholder$":'  # Dashboard structure stopped supporting 'input'


# MCE is a Metadata Change Event JSON with specific structure to feed DataHub with legacy (or custom) data
def generate_mce(json_template: dict,
                 snapshot_list: list):
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
                .replace('"$inputs$"', Input.get_input_entries(snapshot.inputs, snapshot.type.lower()))
                .replace('"$owners$"', Owner.get_owner_entries(snapshot.owners))
                .replace('"$paths$"', Path.get_path_entries(snapshot.paths, snapshot.get_urn_path()))
                .replace('"$tags$"', Tag.get_tag_entries(snapshot.tags))
                .replace(input_placeholder, '')
        )

    return mce


if __name__ == '__main__':
    os.chdir(wd(__file__).resolve().parents[0])  # change working directory
    df = pd.read_csv('resources.csv', sep=',')  # ideally would read from google sheet
    snapshots = []

    for index, row in df.iterrows():
        if row['resource_type'].lower() == 'question':
            snapshots.append(Chart(number=row['resource_number'],
                                   title=row['resource_title'],
                                   description=row['resource_description'],
                                   link=row['resource_link'],
                                   owners=[Owner(name=x,
                                                 roles=row['owners_roles']) for x in
                                           row['resource_owners'].split(split_sep)
                                           ] if not isinstance(row['resource_owners'], float) else '',
                                   inputs=[Input(database=row['database'],
                                                 schema=row['schema'],
                                                 table=x) for x in row['tables'].split(split_sep)
                                           ] if not isinstance(row['tables'], float) else '',
                                   tags=[Tag(name=x) for x in row['tags'].split(split_sep)
                                         ] if not isinstance(row['tags'], float) else '',
                                   paths=[Path(department=x,
                                               sub_folders=row['sub_folders'],
                                               resource_number=row['resource_number'],
                                               title=row['resource_title']) for x in row['department'].split(split_sep)]

                                   )  # arg: inputs and paths can have more than one entry (comma separated)
                             )
        elif row['resource_type'].lower() == 'dashboard':
            snapshots.append(Dashboard(number=row['resource_number'],
                                       title=row['resource_title'],
                                       description=row['resource_description'],
                                       link=row['resource_link'],
                                       owners=[Owner(name=x,
                                                     roles=row['owners_roles']) for x in
                                               row['resource_owners'].split(split_sep)
                                               ] if not isinstance(row['resource_owners'], float) else '',
                                       tags=[Tag(name=x) for x in row['tags'].split(split_sep)
                                             ] if not isinstance(row['tags'], float) else '',
                                       paths=[Path(department=x,
                                                   sub_folders=row['sub_folders'],
                                                   resource_number=row['resource_number'],
                                                   title=row['resource_title']) for x in
                                              row['department'].split(split_sep)]

                                       )  # arg: inputs and paths can have more than one entry (comma separated)
                             )
        else:
            raise ValueError('---- Resource Type not Recognized. Check the input file ----')

    template = open('template.json', 'r+')
    mces = generate_mce(template, snapshots)

    output = ',\n'.join(mces)
    output = '\n'.join(('[', output, ']'))

    with open("output.json", "w") as text_file:
        text_file.write(output)
