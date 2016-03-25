#!/usr/bin/env python3
# -*- coding: utf-8-*-

"""Marvin Entry Point

Make sure to give this file execution permissions and then run it to start
Marvin.

Execution Plan:
1. Load settings from console arguments and config files
2. Perform startup checks to ensure everything is present and ready to run
3. Start the main loop
"""

import marvin.setup.loader
import marvin.app

if __name__ == '__main__':
    settings = marvin.setup.loader.load()
    app = marvin.app.Marvin(settings)
    app.perform_startup_checks()
    app.run()
