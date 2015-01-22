import urllib

from bika.lims import bikaMessageFactory as _
from bika.lims.interfaces import IIdServer
from zope.interface import implements
from bika.lims.idserver import IDServerUnavailable, DefaultBikaIdServer


class IGSNSampleIdServer(DefaultBikaIdServer):
    """This returns IGSN Ids for Samples.
    """
    implements(IIdServer)

    def get_external_id(self, context, prefix, batch_size=None):
        import pdb, sys; pdb.Pdb(stdout=sys.__stdout__).set_trace()
        plone = self.context.portal_url.getPortalObject()
        url = self.context.bika_setup.getIDServerURL()
        query = {'batch_size': batch_size} if batch_size else {}
        sample = self.context

        # won't handle multivalued fields very well XXX
        for field in sample.schema.fields():
            if field.widget.visible.get('igsn_idserver', None) == 'visible':
                field_type = field.getType()
                field_name = field.getName()
                field_value = field.get(sample)
                val = field_value.Title() if \
                    field_type.endswith('ReferenceField') else field_value
                query[field_name] = val
        try:
            # GET
            query = urllib.urlencode(query)
            f = urllib.urlopen('%s/%s/%s%s%s' % (
                url, plone.getId(), prefix, "?" if query else "", query))
            new_id = f.read()
            f.close()
        except:
            from sys import exc_info

            info = exc_info()
            import zLOG;

            zLOG.LOG('INFO', 0, '',
                     'generate_id raised exception: %s, %s \n ID server URL: %s' % (
                         info[0], info[1], url))
            raise IDServerUnavailable(_('ID Server unavailable'))

        return new_id
