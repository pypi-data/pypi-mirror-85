import numpy as np            # pylint: disable=unused-import
import typing                 # pylint: disable=unused-import
from nomad.metainfo import (  # pylint: disable=unused-import
    MSection, MCategory, Category, Package, Quantity, Section, SubSection, SectionProxy,
    Reference
)
from nomad.metainfo.legacy import LegacyDefinition

from nomad.datamodel.metainfo import public

m_package = Package(
    name='molcas_nomadmetainfo_json',
    description='None',
    a_legacy=LegacyDefinition(name='molcas.nomadmetainfo.json'))


class x_molcas_section_frequency(MSection):
    '''
    Section for Molcas frequency (symmetry, frequency, intensity)
    '''

    m_def = Section(validate=False, a_legacy=LegacyDefinition(name='x_molcas_section_frequency'))

    x_molcas_frequency_value = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        description='''
        Molcas frequency value
        ''',
        a_legacy=LegacyDefinition(name='x_molcas_frequency_value'))

    x_molcas_imaginary_frequency_value = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        description='''
        Molcas imaginary frequency value
        ''',
        a_legacy=LegacyDefinition(name='x_molcas_imaginary_frequency_value'))

    x_molcas_frequency_intensity = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        description='''
        Molcas intensity value
        ''',
        a_legacy=LegacyDefinition(name='x_molcas_frequency_intensity'))

    x_molcas_frequency_symmetry = Quantity(
        type=str,
        shape=[],
        description='''
        Molcas symmetry for frequencies
        ''',
        a_legacy=LegacyDefinition(name='x_molcas_frequency_symmetry'))


class x_molcas_section_basis(MSection):
    '''
    Section for Molcas basis sets
    '''

    m_def = Section(validate=False, a_legacy=LegacyDefinition(name='x_molcas_section_basis'))

    x_molcas_basis_atom_label = Quantity(
        type=str,
        shape=[],
        description='''
        Molcas basis set atom label.
        ''',
        a_legacy=LegacyDefinition(name='x_molcas_basis_atom_label'))

    x_molcas_basis_name = Quantity(
        type=str,
        shape=[],
        description='''
        Molcas basis set name.  Repeated strings of '.' are compressed to a single '.'.
        Any leading or trailing '.' are stripped.
        ''',
        a_legacy=LegacyDefinition(name='x_molcas_basis_name'))


class section_method(public.section_method):

    m_def = Section(validate=False, extends_base_section=True, a_legacy=LegacyDefinition(name='section_method'))

    x_molcas_method_name = Quantity(
        type=str,
        shape=[],
        description='''
        Molcas method name (without UHF; see x_molcas_uhf)
        ''',
        a_legacy=LegacyDefinition(name='x_molcas_method_name'))

    x_molcas_uhf = Quantity(
        type=bool,
        shape=[],
        description='''
        If the Molcas method is UHF.
        ''',
        a_legacy=LegacyDefinition(name='x_molcas_uhf'))

    x_molcas_section_basis = SubSection(
        sub_section=SectionProxy('x_molcas_section_basis'),
        repeats=True,
        a_legacy=LegacyDefinition(name='x_molcas_section_basis'))


class section_single_configuration_calculation(public.section_single_configuration_calculation):

    m_def = Section(validate=False, extends_base_section=True, a_legacy=LegacyDefinition(name='section_single_configuration_calculation'))

    x_molcas_slapaf_grad_norm = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        description='''
        Molcas slapaf (geometry optimization) grad (force) norm
        ''',
        a_legacy=LegacyDefinition(name='x_molcas_slapaf_grad_norm'))

    x_molcas_slapaf_grad_max = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        description='''
        Molcas slapaf (geometry optimization) grad (force) max
        ''',
        a_legacy=LegacyDefinition(name='x_molcas_slapaf_grad_max'))

    x_molcas_section_frequency = SubSection(
        sub_section=SectionProxy('x_molcas_section_frequency'),
        repeats=True,
        a_legacy=LegacyDefinition(name='x_molcas_section_frequency'))


m_package.__init_metainfo__()
