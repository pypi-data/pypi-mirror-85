#    This script is part of pymaid (http://www.github.com/schlegelp/pymaid).
#    Copyright (C) 2017 Philipp Schlegel
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

"""Functions to remote control CATMAID frontend."""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from matplotlib.colors import to_rgb
import matplotlib.pyplot as plt

from . import config, core, utils

# Set up logging
logger = config.logger

driver = None


def init(use_existing=False, chrome_driver='chromedriver'):
    """Initialize session."""
    global driver

    if use_existing:
        driver = get_current_window(chrome_driver=chrome_driver)
    else:
        driver = new_window(chrome_driver=chrome_driver)


def new_window(chrome_driver='chromedriver'):
    """Open new browser window and return driver."""
    return webdriver.Chrome(chrome_driver)


def get_current_window(chrome_driver='chrome_driver'):
    r"""Attempt to connect to open Chrome window and return driver.

    For this to work, the browser has to be started with the following options::

        # Mac
        Google\ Chrome --remote-debugging-port=9222

        # Windows
        chrome.exe --remote-debugging-port=9222

    """
    chrome_options = Options()
    chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    # It doesn't work like this unfortunately
    return webdriver.Chrome(chrome_driver, options=chrome_options)


class SelectionTable:
    """CATMAID Selection table."""

    def __init__(self, table_no):
        """Initialize."""
        self.table_no = table_no

        # Get the table instance
        self.st = """
                  var st = CATMAID.SelectionTable.prototype.getInstances()[{}];
                  """.format(self.table_no)

    @property
    def models(self):
        """Return object in selection table as dictionary."""
        # Generate script to be executed
        script = """
                 {}
                 var models = st.getSkeletonModels();
                 return models;
                 """.format(self.st)

        # Get requested selection table
        models = driver.execute_script(script)

        return models

    @property
    def neurons(self):
        """Return neurons in selection table as CatmaidNeuronList."""
        models = self.models

        # Create NeuronList
        nl = core.CatmaidNeuronList(list(models))

        # Add names
        for n in nl:
            n.neuron_name = models[n.skeleton_id]['baseName']

        # Make sure URL matches
        client = utils._eval_remote_instance(None, raise_error=False)
        if client and driver.current_url != client.server:
            logger.warning("Global client's url does not match website URL.")

        return nl

    def clear(self):
        """Clear selection table."""
        script = """
                 {0}
                 st.clear();
                 """.format(self.st)

        # Get requested selection table
        driver.execute_script(script)

    def append(self, x, colors=None):
        """Append neurons to selection table.

        Parameters
        ----------
        x :         skeleton ID(s) | CatmaidNeuron/List
        colors
                    Colors passed to ``colorize``.

        """
        skids = utils.eval_skids(x)

        script = """
                 {0}
                 st.appendSkeletons({1});
                 """.format(self.st,
                            list(skids))

        # Get requested selection table
        driver.execute_script(script)

        if colors:
            self.colorize(colors)

    def colorize(self, colors):
        """Color neurons in selection table.

        Parameters
        ----------
        colors
                    Can be either:
                     - str, e.g. ``"r"`` or ``"red"``
                     - RGB tuple, e.g. ``(1, 1, 0)``
                     - list of the above, e.g. ``[(1, 0, 1), (0, 1, 0)]``
                     - matplotlib palette
                     - dict mapping skeleton IDs to a color, e.g. ``{16: 'r'}``

        """
        skids = list(self.models)

        if isinstance(colors, dict):
            colors = {s: to_rgb(c) for s, c in colors.items()}
        elif isinstance(colors, list):
            colors = dict(zip(skids,
                              [to_rgb(c) for c in colors]))
        elif isinstance(colors, str):
            try:
                cmap = plt.get_cmap(colors)
                colors = dict(zip(skids,
                                  [cmap(1 / len(skids) * i) for i in range(len(skids))]))
            except BaseException:
                colors = dict(zip(skids,
                                  [to_rgb(colors)] * len(skids)))
        elif isinstance(colors, tuple):
            colors = dict(zip(skids, [colors] * len(skids)))
        elif isinstance(colors, list):
            colors = dict(zip(skids, colors))

        if not isinstance(colors, dict):
            raise TypeError('Unable to extract colors from "{}"'.format(type(colors)))

        for s, c in colors.items():
            script = """
                     {st}
                     var c = new THREE.Color().setRGB({r},{g},{b});
                     st.colorSkeleton({s}, false, c, 1, true);
                     """.format(st=self.st,
                                r=c[0], g=c[1], b=c[2],
                                s=s)
            driver.execute_script(script)
