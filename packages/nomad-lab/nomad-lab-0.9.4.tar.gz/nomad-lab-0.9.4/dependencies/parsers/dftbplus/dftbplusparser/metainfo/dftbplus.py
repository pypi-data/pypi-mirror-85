import numpy as np            # pylint: disable=unused-import
import typing                 # pylint: disable=unused-import
from nomad.metainfo import (  # pylint: disable=unused-import
    MSection, MCategory, Category, Package, Quantity, Section, SubSection, SectionProxy,
    Reference
)
from nomad.metainfo.legacy import LegacyDefinition

from nomad.datamodel.metainfo import common
from nomad.datamodel.metainfo import public

m_package = Package(
    name='dftbplus_nomadmetainfo_json',
    description='None',
    a_legacy=LegacyDefinition(name='dftbplus.nomadmetainfo.json'))


class section_molecule_type(common.section_molecule_type):

    m_def = Section(validate=False, extends_base_section=True, a_legacy=LegacyDefinition(name='section_molecule_type'))

    atom = Quantity(
        type=np.dtype(np.int32),
        shape=[],
        description='''
        -
        ''',
        categories=[common.settings_atom_in_molecule],
        a_legacy=LegacyDefinition(name='atom'))

    x_dftbp_charge = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        description='''
        -
        ''',
        a_legacy=LegacyDefinition(name='x_dftbp_charge'))


class section_system(public.section_system):

    m_def = Section(validate=False, extends_base_section=True, a_legacy=LegacyDefinition(name='section_system'))

    x_dftbp_atom_positions_X = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        description='''
        -
        ''',
        a_legacy=LegacyDefinition(name='x_dftbp_atom_positions_X'))

    x_dftbp_atom_positions_Y = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        description='''
        -
        ''',
        a_legacy=LegacyDefinition(name='x_dftbp_atom_positions_Y'))

    x_dftbp_atom_positions_Z = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        description='''
        -
        ''',
        a_legacy=LegacyDefinition(name='x_dftbp_atom_positions_Z'))


class section_eigenvalues(public.section_eigenvalues):

    m_def = Section(validate=False, extends_base_section=True, a_legacy=LegacyDefinition(name='section_eigenvalues'))

    x_dftbp_eigenvalues_values = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        description='''
        -
        ''',
        a_legacy=LegacyDefinition(name='x_dftbp_eigenvalues_values'))

    x_dftbp_eigenvalues_occupation = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        description='''
        -
        ''',
        a_legacy=LegacyDefinition(name='x_dftbp_eigenvalues_occupation'))


class section_single_configuration_calculation(public.section_single_configuration_calculation):

    m_def = Section(validate=False, extends_base_section=True, a_legacy=LegacyDefinition(name='section_single_configuration_calculation'))

    x_dftbp_atom_forces_X = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        description='''
        -
        ''',
        a_legacy=LegacyDefinition(name='x_dftbp_atom_forces_X'))

    x_dftbp_atom_forces_Y = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        description='''
        -
        ''',
        a_legacy=LegacyDefinition(name='x_dftbp_atom_forces_Y'))

    x_dftbp_atom_forces_Z = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        description='''
        -
        ''',
        a_legacy=LegacyDefinition(name='x_dftbp_atom_forces_Z'))

    x_dftbp_force_max = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        description='''
        -
        ''',
        a_legacy=LegacyDefinition(name='x_dftbp_force_max'))

    x_dftbp_force_max_mov = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        description='''
        -
        ''',
        a_legacy=LegacyDefinition(name='x_dftbp_force_max_mov'))


m_package.__init_metainfo__()
