import os
import yaml

import marvin.support.path

# TODO: Documentation; validate ability queries

def compile():
    files = _find_ability_files()
    yaml_text = _combine_ability_files(files)
    return _load_abilities_from_yaml(yaml_text)

def _find_ability_files():
    path = os.path.join(marvin.support.path.LIB_PATH, 'abilities')
    files = filter(
        lambda found_file: found_file.endswith('.yml'),
        os.listdir(path))
    return map(
        lambda found_file: os.path.join(path, found_file),
        files
    )

def _combine_ability_files(files):
    ability_yaml = ''
    for index, file_path in enumerate(files):
        with open(file_path, 'r') as yaml_file:
            if index > 0:
                # skip the first line, because we need the root key only once
                next(yaml_file)
            for line in yaml_file:
                ability_yaml += line

    return ability_yaml

def _load_abilities_from_yaml(ability_yaml):
    abilities_dict = yaml.load(ability_yaml)['en']
    # Remove helpers before returning
    abilities_dict.pop('aliases', None)
    print(abilities_dict) #!
    return abilities_dict
