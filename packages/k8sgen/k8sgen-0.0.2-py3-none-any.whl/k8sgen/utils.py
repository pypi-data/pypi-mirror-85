def get_json(obj):
    if type(obj) == dict:
        return obj
    else:
        return obj.to_json()

def get_from_key_list(data, keys):
    # if the key doesn't exist then return None
    if not keys[0] in data.keys():
        return None
    if len(keys) > 1:
        # if we aren't at the last key then go a level deeper
        return get_from_key_list(data[keys[0]], keys[1:])
    else:
        # return the value we want
        return data[keys[0]]

def set_from_key_list(data, keys, value):
    # if the key doesn't exist then return None
    if not keys[0] in data.keys():
        if len(keys) == 1:
            data[keys[0]] = value
            return data
        else:
            return None
        return None
    if len(keys) > 1:
        # if we aren't at the last key then go a level deeper
        ret = set_from_key_list(data[keys[0]], keys[1:], value)
        if ret == None:
            return None
        else:
            data[keys[0]] = ret
    else:
        # return the value we want
        data[keys[0]] = value
    return data

def add_in_values(data, values):
    for k in values:
        if values[k] != None:
            keys = k.split('.')
            data = set_from_key_list(data, keys, values[k])
    return data

def stringify(obj):
    name = type(obj).__name__
    variables = vars(obj)
    str_rep = ''
    for v in variables:
        str_rep += '{}={}, '.format(v, getattr(obj, v))
    return name + '(' + str_rep[:-2] + ')'

def clean_null(d):
    clean = {}
    if type(d) == dict:
        for k, v in d.items():
            if type(v) == dict:
                nested = clean_null(v)
                if len(nested.keys()) > 0:
                    clean[k] = nested
            elif type(v) == list:
                for i in range(0, len(v)):
                    v[i] = clean_null(v[i])
                v = [i for i in v if i]
                if len(v) > 0:
                    clean[k] = v
            elif v:
                clean[k] = v
            for k in clean:
                if clean[k] == {} or clean[k] == []:
                    del clean[k]
    else:
        clean = d
    return clean

def clean_unset(data):
    if type(data) == dict:
        for k in data:
            if type(data[k]) == dict:
                data[k] = clean_unset(data[k])
            elif type(data[k]) == list:
                data[k] = clean_unset(data[k])
            elif type(data[k]) == str:
                if data[k].startswith('<') and data[k].endswith('>'):
                    data[k] = None
    else:
        for k in range(0, len(data)):
            if type(data[k]) == dict:
                data[k] = clean_unset(data[k])
            elif type(data[k]) == list:
                data[k] = clean_unset(data[k])
            elif type(data[k]) == str:
                if data[k].startswith('<') and data[k].endswith('>'):
                    data[k] = None
    return data

def recurse_expand(data, components_list, indent=0):
    # print(' ' * indent + str(data))
    if type(data) == dict:
        for k in data:
            if type(data[k]).__name__ in components_list:
                data[k] = data[k].to_json()
            else:
                if type(data[k]) == dict:
                    data[k] = recurse_expand(data[k], components_list, indent = indent+2)
                elif type(data[k]) == list:
                    data[k] = recurse_expand(data[k], components_list, indent = indent+2)
                elif type(data[k]) == str:
                    if data[k].startswith('<') and data[k].endswith('>'):
                        data[k] = None
    else:
        for k in range(0, len(data)):
            if type(data[k]).__name__ in components_list:
                data[k] = data[k].to_json()
            else:
                if type(data[k]) == dict:
                    data[k] = recurse_expand(data[k], components_list, indent = indent+2)
                elif type(data[k]) == list:
                    data[k] = recurse_expand(data[k], components_list, indent = indent+2)
                elif type(data[k]) == str:
                    if data[k].startswith('<') and data[k].endswith('>'):
                        data[k] = None
    return data

def recurse_build(data, key_list, elements, indent=0):
    # print(' ' * indent + str(data))
    if type(data) == dict:
        for k in data:
            key = '.'.join(key_list + [k])
            if key in elements.keys():
                data[k] = elements[key]
            else:
                if type(data[k]) == dict:
                    data[k] = recurse_build(data[k], key_list + [k], elements, indent = indent+2)
                elif type(data[k]) == list:
                    data[k] = recurse_build(data[k], key_list + [k], elements, indent = indent+2)
    else:
        for k in range(0, len(data)):
            key = '.'.join(key_list)
            if key in elements.keys():
                data[k] = elements[key]
            else:
                if type(data[k]) == dict:
                    data[k] = recurse_build(data[k], key_list, elements, indent = indent+2)
                elif type(data[k]) == list:
                    data[k] = recurse_build(data[k], key_list, elements, indent = indent+2)
    return data

def get_key_string(data):
    temp = list(get_paths(data))
    ret = ['.'.join(a) for i, a in enumerate(temp) if a not in temp[:i]]
    return ret

def get_paths(d, current = []):
    for a, b in d.items():
        yield current+[a]
        if isinstance(b, dict):
            yield from get_paths(b, current+[a])
        elif isinstance(b, list):
            for i in b:
                yield from get_paths(i, current+[a])
