# -*- coding: utf-8 -*-

import os
from imaxplore.Core.Parameters import param


class Configuration:
    def __init__(self, filePath):
        # Creat dictionnary
        self.config = dict()

        # Check if the configuration file exists
        if os.path.isfile(filePath):

            # Read the configuration file
            env = dict()
            execfile(filePath, env)

            # Save parameters
            self.config = env['param']

    def __call__(self, key):
        if key in self.config:
            return self.config[key]
        else:
            return param[key]

conf = Configuration(param['configuration_file'])
