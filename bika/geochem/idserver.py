from bika.lims.interfaces import IIdServer
from zope.interface import implements
from bika.lims.idserver import DefaultBikaIdServer
from sesarwslib import categories as cat
from sesarwslib.sample import Sample
import sesarwslib.sesarwsclient as ws


class IGSNSampleIdServer(DefaultBikaIdServer):
    """This returns IGSN Ids for Samples.
    """
    implements(IIdServer)

    def generateUniqueId(self):

        bs = self.context.bika_setup
        if bs.Schema()['EnableIGSNIdServer'].get(bs):
            # generate IGSN Sample ID
            return self.new_igsn_id()
        else:
            # normal idserver routine
            return super(IGSNSampleIdServer, self).generateUniqueId()

    def new_igsn_id(self):
        import pdb, sys; pdb.Pdb(stdout=sys.__stdout__).set_trace()
        bs = self.context.bika_setup
        igsnusername = bs.Schema()['IGSNUsername'].get(bs)
        igsnpassword = bs.Schema()['IGSNPassword'].get(bs)
        igsnusercode = bs.Schema()['IGSNUsercode'].get(bs)

        self.client = ws.IgsnClient(igsnusername, igsnpassword)

        schema = self.context.Schema()
        sample_type = schema['SampleType'].get(self.context).Title()
        sample_name = schema['SampleName'].get(self.context)

        # Check that the sample type is valid:
        try:
            # We don't actually want to use the value of the reverse mapping,
            # just make sure it works.
            cat.SampleType.reverse_mapping[sample_type]
        except KeyError:
            sample_type = cat.SampleType.Other

        sample = Sample.sample(
            sample_type=sample_type,
            user_code=igsnusercode,
            name=sample_name,
            material=cat.Material.Rock)

        igsn = self.client.register_sample(sample)

        return igsn
