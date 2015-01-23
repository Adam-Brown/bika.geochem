from archetypes.schemaextender.interfaces import IOrderableSchemaExtender
from bika.lims.fields import *
from bika.geochem import bikaMessageFactory as _
from bika.lims.interfaces import IBikaSetup
from zope.component import adapts
from zope.interface import implements


class BikaSetupExtender(object):
    adapts(IBikaSetup)
    implements(IOrderableSchemaExtender)

    fields = [
        ExtBooleanField(
            'EnableIGSNIdServer',
            schemata="ID Server",
            default=False,
            widget=BooleanWidget(
                label=_("Enable the IGSN ID Server for Sample Ids"),
                description=_(
                    "If enabled, the external igsn-server will be "
                    "queried when creating Sample Ids"))
        ),
        ExtStringField(
            'IGSNUsername',
            schemata="ID Server",
            widget=StringWidget(
                label=_("IGSN Username")
            ),
        ),
        ExtStringField(
            'IGSNPassword',
            schemata="ID Server",
            widget=PasswordWidget(
                label=_("IGSN Password")
            ),
        ),
        ExtStringField(
            'IGSNUsercode',
            schemata="ID Server",
            widget=StringWidget(
                label=_("IGSN Usercode")
            ),
        ),
    ]

    def __init__(self, context):
        self.context = context

    def getFields(self):
        return self.fields

    def getOrder(self, schematas):
        default = schematas['default']
        default.append('EnableIGSNIdServer')
        default.append('IGSNUsername')
        default.append('IGSNPassword')
        default.append('IGSNUsercode')
        schematas['default'] = default
        return schematas
