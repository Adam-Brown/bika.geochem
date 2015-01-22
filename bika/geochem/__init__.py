import warnings
import pkg_resources

PROJECTNAME = 'bika.geochem'
__version__ = pkg_resources.get_distribution(PROJECTNAME).version

# import this to create messages in the bika domain.
from zope.i18nmessageid import MessageFactory
bikaMessageFactory = MessageFactory('bika.geochem')

# import this to log messages
import logging
logger = logging.getLogger('Bika geochem')

from bika.lims.permissions import *

from AccessControl import allow_module
from Products.Archetypes.atapi import process_types, listTypes
from Products.CMFCore.utils import ContentInit

allow_module('AccessControl')
allow_module('bika.lims')

def initialize(context):
    content_types, constructors, ftis = process_types(
        listTypes(PROJECTNAME),
        PROJECTNAME)
    # Register each type with it's own Add permission
    # use ADD_CONTENT_PERMISSION as default
    allTypes = zip(content_types, constructors)
    for atype, constructor in allTypes:
        kind = "%s: Add %s" % (PROJECTNAME, atype.portal_type)
        perm = ADD_CONTENT_PERMISSIONS.get(atype.portal_type,
                                           ADD_CONTENT_PERMISSION)
        ContentInit(kind,
                    content_types=(atype,),
                    permission=perm,
                    extra_constructors=(constructor,),
                    fti=ftis,
        ).initialize(context)
