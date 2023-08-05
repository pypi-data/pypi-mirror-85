import numpy as np            # pylint: disable=unused-import
import typing                 # pylint: disable=unused-import
from nomad.metainfo import (  # pylint: disable=unused-import
    MSection, MCategory, Category, Package, Quantity, Section, SubSection, SectionProxy,
    Reference
)
from nomad.metainfo.legacy import LegacyDefinition

from nomad.datamodel.metainfo import general_experimental

m_package = Package(
    name='skeleton_nomadmetainfo_json',
    description='None',
    a_legacy=LegacyDefinition(name='skeleton.nomadmetainfo.json'))


class section_experiment(general_experimental.section_experiment):

    m_def = Section(validate=False, extends_base_section=True, a_legacy=LegacyDefinition(name='section_experiment'))

    experiment_location = Quantity(
        type=str,
        shape=[],
        description='''
        Contains information relating to an archive.
        ''',
        a_legacy=LegacyDefinition(name='experiment_location'))


m_package.__init_metainfo__()
