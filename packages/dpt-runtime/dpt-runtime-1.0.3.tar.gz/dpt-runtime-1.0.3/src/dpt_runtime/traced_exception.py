# -*- coding: utf-8 -*-

"""
direct Python Toolbox
All-in-one toolbox to encapsulate Python runtime variants
----------------------------------------------------------------------------
(C) direct Netware Group - All rights reserved
https://www.direct-netware.de/redirect?dpt;runtime

This Source Code Form is subject to the terms of the Mozilla Public License,
v. 2.0. If a copy of the MPL was not distributed with this file, You can
obtain one at http://mozilla.org/MPL/2.0/.
----------------------------------------------------------------------------
https://www.direct-netware.de/redirect?licenses;mpl2
----------------------------------------------------------------------------
v1.0.3
dpt_runtime/traced_exception.py
"""

# pylint: disable=invalid-name

try: from types import new_class
except ImportError: new_class = None

from .traced_exception_mixin import TracedExceptionMixin

class _TracedExceptionMetaClass(type):
    """
The "_TracedExceptionMetaClass" is used as a Python 2 and Python 3 compatible
metaclass to return true for all inherited classes implementing
"dpt_runtime.TracedExceptionMixin".

:author:     direct Netware Group et al.
:copyright:  direct Netware Group - All rights reserved
:package:    dpt
:subpackage: runtime
:since:      v1.0.0
:license:    https://www.direct-netware.de/redirect?licenses;mpl2
             Mozilla Public License, v. 2.0
    """

    __slots__ = [ ]
    """
python.org: __slots__ reserves space for the declared variables and prevents
the automatic creation of __dict__ and __weakref__ for each instance.
    """

    def __instancecheck__(cls, instance):
        """
python.org: Return "true" if instance should be considered a (direct or
indirect) instance of class.

:param cls: Python class
:param instance: Instance to check

:return: (bool) True of instance of "TracedExceptionMixin"
:since:  v1.0.0
        """

        return isinstance(instance, TracedExceptionMixin)
    #
#

class _TracedException(RuntimeError, TracedExceptionMixin):
    """
The "_TracedException" class is used in connection with the
"_TracedExceptionMetaClass" to return true for all inherited ones
implementing "dpt_runtime.TracedExceptionMixin".

:author:     direct Netware Group et al.
:copyright:  direct Netware Group - All rights reserved
:package:    pas
:subpackage: runtime
:since:      v1.0.0
:license:    https://www.direct-netware.de/redirect?licenses;mpl2
             Mozilla Public License, v. 2.0
    """

    __slots__ = TracedExceptionMixin._mixin_slots_
    """
python.org: __slots__ reserves space for the declared variables and prevents
the automatic creation of __dict__ and __weakref__ for each instance.
    """

    def __init__(self, value, _exception = None):
        """
Constructor __init__(TracedException)

:param value: Exception message value
:param _exception: Inner exception

:since: v1.0.0
        """

        super(_TracedException, self).__init__(value)
        TracedExceptionMixin.__init__(self, _exception)
    #

    __str__ = TracedExceptionMixin.__str__
    """
python.org: Called by the str(object) and the built-in functions format()
and print() to compute the "informal" or nicely printable string
representation of an object.

:return: (str) The "informal" or nicely printable string representation
:since:  v1.0.0
    """

    with_traceback = TracedExceptionMixin.with_traceback
    """
python.org: This method sets tb as the new traceback for the exception and
returns the exception object.

:param tb: New traceback for the exception

:return: (object) Manipulated exception instance
:since:  v1.0.0
    """
#

TracedException = (_TracedExceptionMetaClass("TracedException", ( _TracedException, ), { })
                   if (new_class is None) else
                   new_class("TracedException", ( _TracedException, ), { "metaclass": _TracedExceptionMetaClass })
                  )
"""
The extended "RuntimeError" is used to redirect exceptions to output
streams.

:author:     direct Netware Group et al.
:copyright:  direct Netware Group - All rights reserved
:package:    pas
:subpackage: runtime
:since:      v1.0.0
:license:    https://www.direct-netware.de/redirect?licenses;mpl2
            Mozilla Public License, v. 2.0
"""
