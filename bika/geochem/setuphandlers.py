""" Bika setup handlers. """


class Empty:
    pass


def setupVarious(context):
    """
    Final Bika import steps.
    """
    if context.readDataFile('bika.geochem_various.txt') is None:
        return

    site = context.getSite()
    pass
