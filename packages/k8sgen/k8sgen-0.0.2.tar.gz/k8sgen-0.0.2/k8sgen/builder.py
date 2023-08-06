from k8sgen import APIResources, Components, utils
import jsonc
import re
import os

class K8sBuilder:
    def __init__(self):
        pass

    def build_manifest(self, definition=None, config=None, definition_path=None, config_path=None, path_replacements={}):
        if definition_path:
            with open(definition_path) as f:
                definition = f.read()

        if config_path:
            with open(config_path) as f:
                config = f.read()

        if definition == None or config == None:
            err = ValueError('Missing definition or config data')
            raise err

        if type(definition) == str:
            self.definition_data = jsonc.loads(definition)
        else:
            self.definition_data = definition

        if type(config) == str:
            self.config_data = jsonc.loads(config)
        else:
            self.config_data = config

        self.path_replacements = path_replacements

        local_pattern = re.compile('\$\{\.\S*\}')

        patterns = [
            '\$\{\.\S*\}',
            '\$\{config\.\S*\}',
            '\$\{file\.\S*\}',
            '\$\{files\.\S*\}'
        ]

        refs = {}

        components = self.definition_data['components']
        to_return  = self.definition_data['return']

        for c in components:
            refs[c] = self.find_refs(components[c]['fields'], local_pattern)

        order = self.get_order(refs)
        self.objs = {}

        for c in order:
            self.objs[c] = self.get_obj(components[c]['type'])
            fields = components[c]['fields']
            for pattern in patterns:
                compiled_pattern = re.compile(pattern)
                fields = self.replace_refs(fields, compiled_pattern)

            if fields == None:
                self.objs[c] = None
            else:
                keys = list(fields.keys())

                if 'env' in keys:
                    if fields['env'] != None:
                        fields['env'] = format_env(fields['env'])

                for k in keys:
                    fields['_' + k] = fields[k]
                    del fields[k]

                self.objs[c].set(**fields)

        return self.objs[to_return]
    
    def find_refs(self, data, pattern):
        refs = []
        if type(data) == dict:
            for k in data:
                if type(data[k]) == dict:
                    refs += self.find_refs(data[k], pattern)
                elif type(data[k]) == list:
                    refs += self.find_refs(data[k], pattern)
                elif type(data[k]) == str:
                    res = [r[:-1].split('.')[1] for r in pattern.findall(data[k])]
                    refs += res
        elif type(data) == list:
            for k in range(0, len(data)):
                if type(data[k]) == dict:
                    refs += self.find_refs(data[k], pattern)
                elif type(data[k]) == list:
                    refs += self.find_refs(data[k], pattern)
                elif type(data[k]) == str:
                    res = [r[:-1].split('.')[1] for r in pattern.findall(data[k])]
                    refs += res
        return refs

    def replace_refs(self, data, pattern):
        refs = []
        if type(data) == dict:
            for k in data:
                if type(data[k]) == dict:
                    refs += self.replace_refs(data[k], pattern)
                elif type(data[k]) == list:
                    refs += self.replace_refs(data[k], pattern)
                elif type(data[k]) == str:
                    res = [(r[2:-1].split('.')[0], r[2:-1].split('.')[1:]) for r in pattern.findall(data[k])]
                    if len(res) > 0:
                        data[k] = self.handle_ref(res[0][0], res[0][1])
        elif type(data) == list:
            for k in range(0, len(data)):
                if type(data[k]) == dict:
                    refs += self.replace_refs(data[k], pattern)
                elif type(data[k]) == list:
                    refs += self.replace_refs(data[k], pattern)
                elif type(data[k]) == str:
                    res = [(r[2:-1].split('.')[0], r[2:-1].split('.')[1:]) for r in pattern.findall(data[k])]
                    if len(res) > 0:
                        data[k] = self.handle_ref(res[0][0], res[0][1])
        elif type(data) == str:
            res = [(r[2:-1].split('.')[0], r[2:-1].split('.')[1:]) for r in pattern.findall(data)]
            if len(res) > 0:
                data = self.handle_ref(res[0][0], res[0][1])
        return data

    def handle_ref(self, ref_type, ref_path):
        if ref_type == '':
            out = self.objs[ref_path[0]]
            return out
        if ref_type == 'config':
            out = utils.get_from_key_list(self.config_data, ref_path)
            return out
        if ref_type == 'file':
            out = ''
            path = '.'.join(ref_path)
            for k in self.path_replacements:
                path = path.replace('<{}>'.format(k), self.path_replacements[k])
            with open(path) as f:
                out = f.read()
            return out
        if ref_type == 'files':
            out = {}
            path = '.'.join(ref_path)
            for k in self.path_replacements:
                path = path.replace('<{}>'.format(k), self.path_replacements[k])
            files = self.files_in(path)
            for file_path in files:
                filename = os.path.basename(file_path)
                with open(file_path) as f:
                    out[filename] = f.read()
            return out

    def get_order(self, refs):
        order = []
        to_remove = []
        while len(refs) > 0:
            for n in refs:
                if len(refs[n]) == 0:
                    order.append(n)
                    to_remove.append(n)
            for r in to_remove:
                del refs[r]
            for n in refs:
                refs[n] = [ref for ref in refs[n] if not ref in to_remove]
            to_remove = []

        return order

    def get_obj(self, obj_type):
        parts = obj_type.split('.')

        if parts[0] == 'APIResources':
            class_ = getattr(APIResources, parts[1])
            out = class_()
            return out
        if parts[0] == 'Components':
            class_ = getattr(Components, parts[1])
            out = class_()
            return out
        return None

    def format_env(self, data):
        out = []
        for k in data:
            if k.startswith('.comment'):
                continue
            if type(data[k]) != dict:
                if type(data[k]) == bool:
                    data[k] = '{}'.format(data[k]).lower()
                    out.append({
                        'name': k,
                        'value': data[k]
                    })
                elif type(data[k]) != str:
                    data[k] = '{}'.format(data[k])
                    out.append({
                        'name': k,
                        'value': data[k]
                    })
                else:
                    out.append({
                        'name': k,
                        'value': data[k]
                    })
            else:
                out.append({
                    'name': k,
                    'valueFrom': data[k]
                })
        if len(out) == 0:
            out = None
        return out

    def files_in(self, path):
        to_ignore = ['.DS_Store']

        files = []
        for root, folders, filenames in os.walk(path):
            for name in filenames:
                if name not in to_ignore:
                    files.append(os.path.join(root, name))
        return files

    def fix_brace_strings(self, text):
        text = text.replace('\'{}\'', '{}')
        return text
        

                

    