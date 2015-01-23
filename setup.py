import os
from setuptools import setup, find_packages

version = '0.1'

def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

setup(name='bika.geochem',
      version=version,
      description="Bika Geo-Chemistry",
      long_description=read("README.md") + read("CHANGELOG.txt"),
      # Get more strings from
      # http://pypi.python.org/pypi?:action=list_classifiers
      classifiers=[
          "Framework :: Plone",
          "Programming Language :: Python",
          "Development Status :: 5 - Production/Stable",
          "Environment :: Web Environment",
          "Intended Audience :: Information Technology",
          "Intended Audience :: Science/Research",
      ],
      keywords='Bika Open Source LIMS - Geo-Chemistry',
      author='Bika Laboratory Systems',
      author_email='support@bikalabs.com',
      url='www.bikalabs.com',
      license='AGPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['bika'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'archetypes.schemaextender',
          'bika.lims',
          'SESAR-Web-Services-Library',
      ],
      extras_require={
          'test': [
              'plone.app.testing',
              'robotsuite',
              'robotframework',
              'robotframework-selenium2library',
              'plone.app.robotframework',
              'Products.PloneTestCase',
          ]
      },
      entry_points="""
      [z3c.autoinclude.plugin]
      target = plone
      """,
)
