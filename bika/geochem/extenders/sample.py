from archetypes.schemaextender.interfaces import IOrderableSchemaExtender
from archetypes.schemaextender.interfaces import ISchemaModifier
from bika.lims import bikaMessageFactory as _
from bika.lims.fields import *
from bika.lims.interfaces import ISample
from Products.CMFCore import permissions
from zope.component import adapts
from zope.interface import implements


class SampleSchemaExtender(object):
    adapts(ISample)
    implements(IOrderableSchemaExtender)

    fields = [
        ExtStringField(
            "IGSN",
            searchable=True,
            mode="rw",
            read_permission=permissions.View,
            write_permission=permissions.ModifyPortalContent,
            widget=StringWidget(
                label=_("IGSN"),
                visible={
                    'edit': 'invisible',
                    'view': 'visible',
                    'header_table': 'visible',
                    'sample_registered': {'view': 'visible',
                                          'edit': 'invisible'},
                    'to_be_sampled': {'view': 'visible', 'edit': 'invisible'},
                    'sampled': {'view': 'visible', 'edit': 'invisible'},
                    'to_be_preserved': {'view': 'visible', 'edit': 'invisible'},
                    'sample_due': {'view': 'visible', 'edit': 'invisible'},
                    'sample_received': {'view': 'visible', 'edit': 'invisible'},
                    'expired': {'view': 'visible', 'edit': 'invisible'},
                    'disposed': {'view': 'visible', 'edit': 'invisible'},
                },
                render_own_label=True,
            )
        ),

        ExtStringField(
            "SampleName",
            searchable=True,
            mode="rw",
            read_permission=permissions.View,
            write_permission=permissions.ModifyPortalContent,
            widget=StringWidget(
                label=_("Sample Name"),
                visible={
                    'edit': 'invisible',
                    'view': 'visible',
                    'header_table': 'visible',
                    'sample_registered': {'view': 'visible',
                                          'edit': 'invisible'},
                    'to_be_sampled': {'view': 'visible', 'edit': 'invisible'},
                    'sampled': {'view': 'visible', 'edit': 'invisible'},
                    'to_be_preserved': {'view': 'visible', 'edit': 'invisible'},
                    'sample_due': {'view': 'visible', 'edit': 'invisible'},
                    'sample_received': {'view': 'visible', 'edit': 'invisible'},
                    'expired': {'view': 'visible', 'edit': 'invisible'},
                    'disposed': {'view': 'visible', 'edit': 'invisible'},
                },
                render_own_label=True,
            )
        ),

        ExtStringField(
            "Latitude",
            searchable=True,
            mode="rw",
            read_permission=permissions.View,
            write_permission=permissions.ModifyPortalContent,
            widget=StringWidget(
                label=_("Latitude"),
                visible={
                    'edit': 'invisible',
                    'view': 'visible',
                    'header_table': 'visible',
                    'sample_registered': {'view': 'visible',
                                          'edit': 'invisible'},
                    'to_be_sampled': {'view': 'visible', 'edit': 'invisible'},
                    'sampled': {'view': 'visible', 'edit': 'invisible'},
                    'to_be_preserved': {'view': 'visible', 'edit': 'invisible'},
                    'sample_due': {'view': 'visible', 'edit': 'invisible'},
                    'sample_received': {'view': 'visible', 'edit': 'invisible'},
                    'expired': {'view': 'visible', 'edit': 'invisible'},
                    'disposed': {'view': 'visible', 'edit': 'invisible'},
                },
                render_own_label=True,
            )
        ),

        ExtStringField(
            "Longitude",
            searchable=True,
            mode="rw",
            read_permission=permissions.View,
            write_permission=permissions.ModifyPortalContent,
            widget=StringWidget(
                label=_("Longitude"),
                visible={
                    'edit': 'invisible',
                    'view': 'visible',
                    'header_table': 'visible',
                    'sample_registered': {'view': 'visible',
                                          'edit': 'invisible'},
                    'to_be_sampled': {'view': 'visible', 'edit': 'invisible'},
                    'sampled': {'view': 'visible', 'edit': 'invisible'},
                    'to_be_preserved': {'view': 'visible', 'edit': 'invisible'},
                    'sample_due': {'view': 'visible', 'edit': 'invisible'},
                    'sample_received': {'view': 'visible', 'edit': 'invisible'},
                    'expired': {'view': 'visible', 'edit': 'invisible'},
                    'disposed': {'view': 'visible', 'edit': 'invisible'},
                },
                render_own_label=True,
            )
        ),
    ]

    def __init__(self, context):
        self.context = context

    def getOrder(self, schematas):
        default = schematas['default']
        default.insert(default.index('SampleType'), 'SampleName')
        default.insert(default.index('SampleType'), 'IGSN')
        default.insert(default.index('SampleType'), 'Latitude')
        default.insert(default.index('SampleType'), 'Longitude')

        schematas['default'] = default
        return schematas

    def getFields(self):
        return self.fields


class SampleSchemaModifier(object):
    adapts(ISample)
    implements(ISchemaModifier)

    def __init__(self, context):
        self.context = context

    def fiddle(self, schema):
        return schema
