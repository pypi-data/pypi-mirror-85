"""
logx: nice print.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Copyright (c) 2020 Min Latt.
License: MIT, see LICENSE for more details.
"""

import logging
from rich import print as p


class Plug:
    def __init__(self, debug=False):
        """Use __constructor__.out method, this will handle the rest.
        """
        self.debug = debug

        _format = "%(asctime)s: %(m_io)s"
        _level = logging.DEBUG if self.debug else logging.INFO
        logging.basicConfig(format=_format, level=_level, datefmt="%H:%M:%S")

    def c(self, *argv):
        self.m_io = list()
        self.t_io = list()
        self.shape = list()
        for arg in argv:
            try:
                self.m_io.append(arg)
                self.t_io.append(type(arg))
                self.shape.append(arg.shape)
            except AttributeError:
                self.shape.append(None)

            except Exception as e:
                p(e)

        if not self.debug:
            for i in range(len(self.m_io)):
                self.print_danger(self.m_io[i])
                if (self.shape[i]) == None:
                    p('{0}'.format(self.t_io[i]))
                else:
                    p('{0} => shape: {1}'.format(self.t_io[i], self.shape[i]))
        else:
            pass

    def print_danger(self, m):
        p('[italic red]{0}[/italic red]'.format(m))


""" this? maybe I previously play with JS -'D """
