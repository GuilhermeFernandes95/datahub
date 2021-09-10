import json
import pandas as pd
import numpy as np
from Chart import Chart
from Dashboard import Dashboard
from Input import Input


# MCE is a Metadata Change Event JSON with specific structure to feed DataHub with legacy (or custom) data
def generate_mce(json_template: str,
                 snapshot_list: list):
    content = json_template.read()
    json_template.seek(0)

    mce = []
    # for snapshot in snapshot_list:
    #    mce.append(
    #        content.replace('$upper_snapshot$', snapshot.type.capitalize()
    #                        ).replace('$lower_snapshot$', snapshot.type.lower()
    #                                  ).replace('$resource_link$', snapshot.link
    #                                            ).replace('$resource_title$', snapshot.title
    #                                                      ).replace('$resource_description$', snapshot.description
    #                                                                ).replace('$owner_name$', snapshot.owner
    #                                                                          ).replace('$inputs$',
    #                                                                                    snapshot.inputs.get_input_entry()
    #                                                                                    )
    #    )

    return mce


if __name__ == '__main__':
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
                                                 table=x) for x in row['tables'].split(',')]
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
                                                     table=x) for x in row['tables'].split(',')]
                                       )  # arg: inputs can have more than one entry (comma separated)
                             )
        else:
            print('---- Resource Type not Recognized ----')

    template = open('template.json', 'r+')
    mces = generate_mce(template, snapshots)


    def _convert(k):
        return k.replace('.', '||')

    def _revert(k):
        return k.replace('||', '.')

    def _change_keys(obj, convert):
        """
        Recursively goes through the dictionary obj and replaces keys with the convert function.
        source: https://stackoverflow.com/questions/11700705/python-recursively-replace-character-in-keys-of-nested-dictionary
        """
        if isinstance(obj, (str, int, float)):
            return obj
        if isinstance(obj, dict):
            new = obj.__class__()
            for k, v in obj.items():
                new[convert(k)] = _change_keys(v, convert)
        elif isinstance(obj, (list, set, tuple)):
            new = obj.__class__(_change_keys(v, convert) for v in obj)
        else:
            return obj
        return new

    def generate_mce1(json_template: dict,
                      snapshot_list: list) -> list:
        print(json_template)
        print(type(json_template))
        print(json_template.keys())
        mce1 = []

        #for snapshot in snapshot_list:
        #    mce1.append(
        #json_template = json_template['proposedSnapshot'].replace(".", "|")
        print(json_template)

        json_template = _change_keys(json_template, _convert)
        print(json_template)
        print(_change_keys(json_template, _revert))
        print(json_template)
        print('|||||||||||||||||||||||||||||||||||||||||||||')
        print(json_template.update({'auditHeader': 'wwww'}))
        print(type(json_template))
        ['']['DQWD']
        #print(json_template['proposedSnapshot']['com||linkedin||pegasus2avro||metadata||snapshot||$upper_snapshotSnapshot'])
        json_template.update({'auditHeader': 'wwww', 'proposedSnapshot.com||linkedin||pegasus2avro||metadata||snapshot||upper_snapshotSnapshot': 'a'})
        print(json_template)
        #    )

        return mce1


    # for snap in snapshots:  chack snapshot data
    #    print(snap)

    # output = ',\n'.join(mces)
    # output = '\n'.join(('[', output, ']'))
    ####################################################################################################################
    # print(type(d))
    # print(output.to_dict())
    # print(json.dumps(output.to_dict(), separators=(',', ':')))

    # output = ',\n'.join(hope.toString())
    ## dict.update({'Name': 'dsadas', 'Age': 1})
    with open('template.json') as json_file:
        data = json.load(json_file)
        #print(data)
        # pretty = json.dumps(data, sort_keys=True, indent=4)

    print('||||||||||||||||||||')
    print(generate_mce1(json_template=data, snapshot_list=snapshots))
