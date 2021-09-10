data = {
    'a': 42,
    'b': {
        'ba': 23,
        'bb.wdwd.d': {
            'bba': 420
        }
    }
}


d = {
    "auditHeader": None,
    "proposedSnapshot": {
        "com.linkedin.pegasus2avro.metadata.snapshot.upper_snapshotSnapshot": {
            "urn": "urn:li:$lower_snapshot$:(metabase,InfoSec)",
            "aspects": [
                {
                    "com.linkedin.pegasus2avro.$lower_snapshot$.$upper_snapshot$Info": {
                        "customProperties": {},
                        "externalUrl": "$resource_link$",
                        "title": "$resource_title$",
                        "description": "resource_description",
                        "lastModified": {
                            "created": {
                                "time": 0,
                                "actor": "urn:li:corpuser:$owner_name$",
                                "impersonator": None
                            },
                            "lastModified": {
                                "time": 0,
                                "actor": "urn:li:corpuser:$owner_name$",
                                "impersonator": None
                            },
                            "deleted": None
                        },
                        "$lower_snapshot$Url": None,
                        "inputs": [
                            "$inputs$"
                        ],
                        "type": None,
                        "access": None,
                        "lastRefreshed": None
                    }
                }
            ]
        }
    },
    "proposedDelta": None
}
def recursive_lookup(k, d, i=9):
    if k in d:
        #d[k] = i
        print(type(d[k]))
        return d[k]
    if isinstance(d, list):
        for i in d:
            for v in d.values():
                if isinstance(v, dict):
                    return recursive_lookup(k, v)
    for v in d.values():
        if isinstance(v, dict):
            return recursive_lookup(k, v)
    return None

print('a', recursive_lookup('a', data))
print('ba', recursive_lookup('ba', data))
print('bb.wdwd.d', recursive_lookup('bb.wdwd.d', data))
print('bba', recursive_lookup('bba', data, 9))

#|||||||||||||||||||||||||||||||||||||||||||||||||||||||


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

