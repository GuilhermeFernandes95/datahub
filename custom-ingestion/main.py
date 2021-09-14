import pandas as pd
import os
from Chart import Chart
from Dashboard import Dashboard
from Input import Input
from Path import Path
from pathlib import Path as wd


# MCE is a Metadata Change Event JSON with specific structure to feed DataHub with legacy (or custom) data
def generate_mce(json_template: dict,
                 snapshot_list: list):
    content = json_template.read()
    json_template.seek(0)

    mce = []
    for snapshot in snapshot_list:
        mce.append(
            content.replace('$upper_snapshot$', snapshot.type.capitalize()
                            ).replace('$lower_snapshot$', snapshot.type.lower()
                                      ).replace('$resource_link$', snapshot.link
                                                ).replace('$resource_title$', snapshot.title
                                                          ).replace('$resource_description$', snapshot.description
                                                                    ).replace('$owner_name$', snapshot.owner
                                                                              ).replace('"$inputs$"',
                                                                                        Input.get_input_entries(
                                                                                            snapshot.inputs)
                                                                                        )
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
                                   owner=row['resource_owner'],
                                   inputs=[Input(database=row['database'],
                                                 schema=row['schema'],
                                                 table=x) for x in row['tables'].split(',')
                                           ] if not isinstance(row['tables'], float) else ''
                                   )  # arg: inputs can have more than one entry (comma separated)
                             )
        elif row['resource_type'].lower() == 'dashboard':
            snapshots.append(Dashboard(number=row['resource_number'],
                                       title=row['resource_title'],
                                       description=row['resource_description'],
                                       link=row['resource_link'],
                                       owner=row['resource_owner'],
                                       inputs=[Input(database=row['database'],
                                                     schema=row['schema'],
                                                     table=x) for x in row['tables'].split(',')
                                               ] if not isinstance(row['tables'], float) else ''
                                       )  # arg: inputs can have more than one entry (comma separated)
                             )
        else:
            print('---- Resource Type not Recognized ----')

    template = open('template.json', 'r+')
    mces = generate_mce(template, snapshots)

    output = ',\n'.join(mces)
    output = '\n'.join(('[', output, ']'))
    output = "".join(output.split())

    # with open("output.json", "w") as text_file:
    #    text_file.write(output)

    paths = []
    for index, row in df.iterrows():
        #paths.append(Path(department=row['department'],
        #                  sub_folders=row['sub_folders'],
        #                  title=row['resource_title'])
        #             )
        paths.append([Path(department=x,
                       sub_folders=row['sub_folders'],
                       title=row['resource_title']) for x in row['department'].split(';')])


    for path in paths:
        print(Path.get_path_entries(path))
