# -*- coding: utf-8 -*-

"""
direct Python Toolbox
All-in-one toolbox to encapsulate Python runtime variants
----------------------------------------------------------------------------
(C) direct Netware Group - All rights reserved
https://www.direct-netware.de/redirect?dpt;threading

This Source Code Form is subject to the terms of the Mozilla Public License,
v. 2.0. If a copy of the MPL was not distributed with this file, You can
obtain one at http://mozilla.org/MPL/2.0/.
----------------------------------------------------------------------------
https://www.direct-netware.de/redirect?licenses;mpl2
----------------------------------------------------------------------------
v1.0.1
dpt_threading/thread.py
"""

from threading import Thread as _Thread

from dpt_logging.log_line import LogLine
from dpt_runtime.exception_log_trap import ExceptionLogTrap

class Thread(_Thread):
    """
"Thread" represents a deactivatable Thread implementation.

:author:     direct Netware Group et al.
:copyright:  direct Netware Group - All rights reserved
:package:    dpt
:subpackage: threading
:since:      v1.0.0
:license:    https://www.direct-netware.de/redirect?licenses;mpl2
             Mozilla Public License, v. 2.0
    """

    __slots__ = [ ]
    """
python.org: __slots__ reserves space for the declared variables and prevents
the automatic creation of __dict__ and __weakref__ for each instance.
    """
    _active = True
    """
True if new non-daemon threads are allowed to be started.
    """

    def run(self):
        """
python.org: Method representing the thread’s activity.

:since: v1.0.0
        """

        with ExceptionLogTrap("dpt_threading"): _Thread.run(self)
    #

    def start(self):
        """
python.org: Start the thread's activity.

:since: v1.0.0
        """

        if (self.daemon or Thread._active): _Thread.start(self)
        else: LogLine.debug("{0!r} prevented new non-daemon thread", self, context = "dpt_threading")
    #

    @staticmethod
    def set_inactive():
        """
Prevents new non-daemon threads to be started.

:since: v1.0.0
        """

        Thread._active = False
    #
#
