##############################################################################
#
# Copyright (c) 2007 Zope Foundation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
"""zope.app.broken interfaces.
"""

from zope.deferredimport import deprecated

# BBB zope.app.broken 5.0: Names now moved to ZODB itself.
deprecated(
    'Please import from ZODB.interfaces.'
    ' This module will go away in zope.app.broken 5.0.',
    IBroken='ZODB.interfaces:IBroken',
)
