import sys
import argparse
import logging
import pkgutil

from marvin.support.log import  Log
import marvin.support.path
import marvin.setup.ability_compiler
import marvin.setup.diagnose
import marvin.setup.lm_compiler

def load():
    configs = dict()
    configs['abilities'] = marvin.setup.ability_compiler.compile()
    # configs['modules'] = load_modules()
    configs['language_model'] = marvin.setup.lm_compiler.compile(
        configs['abilities'])

    return configs

def load_modules():
    """
        Dynamically loads all the modules in the modules folder and sorts
        them by the PRIORITY key. If no PRIORITY is defined for a given
        module, a priority of 0 is assumed.
    """

    # logger = logging.getLogger(__name__)
    locations = [marvin.support.path.PLUGIN_PATH]
    modules = []
    for finder, name, ispkg in pkgutil.walk_packages(locations):
        try:
            loader = finder.find_module(name)
            mod = loader.load_module(name)
        except:
            Log.warn("Skipped loading module '{0}' due to an error.", name)
        else:
            # if hasattr(mod, 'WORDS'):
            modules.append(mod)
            # else:
            #     Log.warn("Skipped loading module '{0}' because it misses " +
            #              "the WORDS constant.", name)
    modules.sort(key=lambda mod: mod.PRIORITY if hasattr(mod, 'PRIORITY')
                 else 0, reverse=True)
    return modules
