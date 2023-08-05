import copy
import yaml
from k8sgen import data_file, utils

def str_presenter(dumper, data):
    if len(data.splitlines()) > 1:  # check for multiline string
        return dumper.represent_scalar("tag:yaml.org,2002:str", data, style="|")
    return dumper.represent_scalar("tag:yaml.org,2002:str", data)


def represent_none(self, _):
    return self.represent_scalar("tag:yaml.org,2002:null", "")


yaml.add_representer(str, str_presenter)
yaml.add_representer(type(None), represent_none)


class K8sObject:
    def __init__(self, name, data_source):
        self.name = name
        self.data_source = data_source
        self.elements = {}

    # set any specific field to a value
    def set(self, **kwargs):
        ret = []
        key_strings = utils.get_key_string(self.fields())
        for key, value in kwargs.items():
            ky = key.replace("_", ".")
            if ky.startswith("."):
                ky = ky[1:]
                if ky in key_strings:
                    self.elements[ky] = value
                    ret.append(True)
                else:
                    ret.append((False, "invalid key name"))
            else:
                matches = []
                for k in key_strings:
                    if k.endswith(ky):
                        matches.append(k)
                if len(matches) == 1:
                    self.elements[matches[0]] = value
                    ret.append(True)
                elif len(matches) == 0:
                    ret.append((False, "invalid key name"))
                else:
                    ret.append((False, "ambiguous key name"))
        return ret

    # get the values that have been set for specific fields
    def get(self, *args):
        ret = {}
        for key in args:
            ky = key.replace("_", ".")
            if ky in self.elements.keys():
                ret[key] = self.elements[ky]
            else:
                return ("Invalid key", key)
        return ret

    # get the fields that the API resource utilizes and return them
    def fields(self):
        data = copy.deepcopy(data_file.k8sgen_data[self.data_source][self.name])
        if self.data_source == 'api_resources_data':
            return data["json"]
        else:
            return data

    # write out the API resource class to a json object
    def to_json(self):
        data = copy.deepcopy(data_file.k8sgen_data[self.data_source][self.name])
        components_list = copy.deepcopy(data_file.k8sgen_data["components"])
        if self.data_source == 'api_resources_data':
            data = utils.recurse_build(data["json"], [], self.elements)
        else:
            data = utils.recurse_build(data, [], self.elements)
        expanded = utils.recurse_expand(data, components_list)
        filtered = utils.clean_null(expanded)
        return filtered

    # write out the API resource class to a yaml object
    def to_yaml(self):
        data = self.to_json()
        return yaml.dump(data)

    def to_string(self):
        variables = utils.clean_null(
            utils.clean_unset(
                {k.replace(".", "_"): v for (k, v) in self.elements.items()}
            )
        )
        str_rep = ""
        for v in variables:
            str_rep += "{}={}, ".format(v, variables[v])
        class_name = type(self).__name__
        return "{}({})".format(class_name, str_rep[:-2])

    def __repr__(self):
        return self.to_string()

    def __str__(self):
        return self.to_string()
