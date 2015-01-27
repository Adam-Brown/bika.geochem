from archetypes.schemaextender.interfaces import IOrderableSchemaExtender
from archetypes.schemaextender.interfaces import ISchemaModifier
from bika.lims import bikaMessageFactory as _
from bika.lims.fields import *
from bika.lims.interfaces import IAnalysisRequest
from Products.CMFCore import permissions
from zope.component import adapts
from zope.interface import implements


class IGSNField(ExtStringField):
    def set(self, instance, value):
        sample = instance.getSample()
        if sample:
            return sample.Schema()['IGSN'].set(sample, value)

    def get(self, instance):
        sample = instance.getSample()
        if sample:
            return sample.Schema()['IGSN'].get(sample)


class SampleNameField(ExtStringField):
    def set(self, instance, value):
        sample = instance.getSample()
        if sample:
            return sample.Schema()['SampleName'].set(sample, value)

    def get(self, instance):
        sample = instance.getSample()
        if sample:
            return sample.Schema()['SampleName'].get(sample)


class AnalysisRequestSchemaExtender(object):
    adapts(IAnalysisRequest)
    implements(IOrderableSchemaExtender)

    fields = [
        IGSNField(
            'IGSN',
            required=0,
            searchable=True,
            mode="rw",
            read_permission=permissions.View,
            write_permission=permissions.ModifyPortalContent,
            widget=StringWidget(
                label=_('IGSN'),
                size=20,
                render_own_label=True,
                visible={
                    'edit': 'visible',
                    'view': 'visible',
                    'add': 'edit',
                    'secondary': 'disabled',
                    'header_table': 'visible',
                    'sample_registered': {'view': 'visible', 'edit': 'visible', 'add': 'edit'},
                    'to_be_sampled': {'view': 'visible', 'edit': 'invisible'},
                    'sampled': {'view': 'visible', 'edit': 'invisible'},
                    'to_be_preserved': {'view': 'visible', 'edit': 'invisible'},
                    'sample_due': {'view': 'visible', 'edit': 'invisible'},
                    'sample_prep': {'view': 'visible', 'edit': 'invisible'},
                    'sample_received': {'view': 'visible', 'edit': 'invisible'},
                    'attachment_due': {'view': 'visible', 'edit': 'invisible'},
                    'to_be_verified': {'view': 'visible', 'edit': 'invisible'},
                    'verified': {'view': 'visible', 'edit': 'invisible'},
                    'published': {'view': 'visible', 'edit': 'invisible'},
                    'invalid': {'view': 'visible', 'edit': 'invisible'}
                }
            )
        ),

        SampleNameField(
            'SampleName',
            required=1,
            searchable=True,
            mode="rw",
            read_permission=permissions.View,
            write_permission=permissions.ModifyPortalContent,
            widget=StringWidget(
                label=_('Sample Name'),
                size=20,
                render_own_label=True,
                visible={
                    'edit': 'visible',
                    'view': 'visible',
                    'add': 'edit',
                    'secondary': 'disabled',
                    'header_table': 'visible',
                    'sample_registered': {'view': 'visible', 'edit': 'visible', 'add': 'edit'},
                    'to_be_sampled': {'view': 'visible', 'edit': 'invisible'},
                    'sampled': {'view': 'visible', 'edit': 'invisible'},
                    'to_be_preserved': {'view': 'visible', 'edit': 'invisible'},
                    'sample_due': {'view': 'visible', 'edit': 'invisible'},
                    'sample_prep': {'view': 'visible', 'edit': 'invisible'},
                    'sample_received': {'view': 'visible', 'edit': 'invisible'},
                    'attachment_due': {'view': 'visible', 'edit': 'invisible'},
                    'to_be_verified': {'view': 'visible', 'edit': 'invisible'},
                    'verified': {'view': 'visible', 'edit': 'invisible'},
                    'published': {'view': 'visible', 'edit': 'invisible'},
                    'invalid': {'view': 'visible', 'edit': 'invisible'}
                }
            )
        )
    ]


    def __init__(self, context):
        self.context = context


    def getOrder(self, schematas):
        default = schematas['default']
        default.insert(default.index('SampleType'), 'SampleName')
        default.insert(default.index('SampleType'), 'IGSN')
        schematas['default'] = default
        return schematas


    def getFields(self):
        return self.fields


class AnalysisRequestSchemaModifier(object):
    adapts(IAnalysisRequest)
    implements(ISchemaModifier)

    def __init__(self, context):
        self.context = context

    def fiddle(self, schema):
        return schema
