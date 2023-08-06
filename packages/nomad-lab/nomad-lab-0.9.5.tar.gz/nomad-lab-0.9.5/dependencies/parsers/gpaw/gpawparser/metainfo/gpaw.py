import numpy as np            # pylint: disable=unused-import
import typing                 # pylint: disable=unused-import
from nomad.metainfo import (  # pylint: disable=unused-import
    MSection, MCategory, Category, Package, Quantity, Section, SubSection, SectionProxy,
    Reference
)
from nomad.metainfo.legacy import LegacyDefinition

from nomad.datamodel.metainfo import public

m_package = Package(
    name='gpaw_nomadmetainfo_json',
    description='None',
    a_legacy=LegacyDefinition(name='gpaw.nomadmetainfo.json'))


class x_gpaw_section_paw_method(MSection):
    '''
    GPAW PAW specific information
    '''

    m_def = Section(validate=False, a_legacy=LegacyDefinition(name='x_gpaw_section_paw_method'))

    x_gpaw_number_of_packed_ap_elements = Quantity(
        type=int,
        shape=[],
        description='''
        number of PAW projector matrix elements in packed format
        ''',
        a_legacy=LegacyDefinition(name='x_gpaw_number_of_packed_ap_elements'))

    x_gpaw_number_of_projectors = Quantity(
        type=int,
        shape=[],
        description='''
        number of PAW projectors
        ''',
        a_legacy=LegacyDefinition(name='x_gpaw_number_of_projectors'))


class section_single_configuration_calculation(public.section_single_configuration_calculation):

    m_def = Section(validate=False, extends_base_section=True, a_legacy=LegacyDefinition(name='section_single_configuration_calculation'))

    x_gpaw_atomic_density_matrices = Quantity(
        type=np.dtype(np.float64),
        shape=['number_of_spin_channels', 'x_gpaw_number_of_packed_ap_elements'],
        description='''
        atomic density matrices in the PAW formalism
        ''',
        a_legacy=LegacyDefinition(name='x_gpaw_atomic_density_matrices'))

    x_gpaw_fixed_spin_Sz = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        description='''
        Target value (fixed) of the z projection of the spin moment operator $S^z$ for the
        converged calculation with the XC_method.
        ''',
        a_legacy=LegacyDefinition(name='x_gpaw_fixed_spin_Sz'))

    x_gpaw_magnetic_moments = Quantity(
        type=np.dtype(np.float64),
        shape=['number_of_atoms'],
        description='''
        Magnetic moments projected onto atoms. The sum gives the total magnetic moment
        ''',
        a_legacy=LegacyDefinition(name='x_gpaw_magnetic_moments'))

    x_gpaw_projections_imag = Quantity(
        type=np.dtype(np.float64),
        shape=['number_of_spin_channels', 'number_of_eigenvalues_kpoints', 'number_of_eigenvalues', 'x_gpaw_number_of_projectors'],
        description='''
        projections in the PAW formalism (imaginary part)
        ''',
        a_legacy=LegacyDefinition(name='x_gpaw_projections_imag'))

    x_gpaw_projections_real = Quantity(
        type=np.dtype(np.float64),
        shape=['number_of_spin_channels', 'number_of_eigenvalues_kpoints', 'number_of_eigenvalues', 'x_gpaw_number_of_projectors'],
        description='''
        projections in the PAW formalism (real part)
        ''',
        a_legacy=LegacyDefinition(name='x_gpaw_projections_real'))

    x_gpaw_spin_Sz = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        description='''
        Value of the z projection of the spin moment operator $S^z$ for the converged
        calculation with the XC_method.
        ''',
        a_legacy=LegacyDefinition(name='x_gpaw_spin_Sz'))


class section_method(public.section_method):

    m_def = Section(validate=False, extends_base_section=True, a_legacy=LegacyDefinition(name='section_method'))

    x_gpaw_density_convergence_criterion = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        description='''
        Density convergence criteria for break the SCF cycle
        ''',
        a_legacy=LegacyDefinition(name='x_gpaw_density_convergence_criterion'))

    x_gpaw_fix_density = Quantity(
        type=bool,
        shape=[],
        description='''
        Was it a calculation with a fixed density?
        ''',
        a_legacy=LegacyDefinition(name='x_gpaw_fix_density'))

    x_gpaw_fix_magnetic_moment = Quantity(
        type=bool,
        shape=[],
        description='''
        Was the magnetic moment fixed? If yes the x_gpaw_fixed_sZ is set
        ''',
        a_legacy=LegacyDefinition(name='x_gpaw_fix_magnetic_moment'))

    x_gpaw_maximum_angular_momentum = Quantity(
        type=np.dtype(np.int32),
        shape=[],
        description='''
        Maxium angular momentum (L) for projectors
        ''',
        a_legacy=LegacyDefinition(name='x_gpaw_maximum_angular_momentum'))

    x_gpaw_mix_beta = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        description='''
        Damping parameter in the density mixer
        ''',
        a_legacy=LegacyDefinition(name='x_gpaw_mix_beta'))

    x_gpaw_mix_class = Quantity(
        type=str,
        shape=[],
        description='''
        The density mixer class name (Mixer, MixerSum, MixerDiff)
        ''',
        a_legacy=LegacyDefinition(name='x_gpaw_mix_class'))

    x_gpaw_mix_old = Quantity(
        type=np.dtype(np.int32),
        shape=[],
        description='''
        Number of old densities in the density mixer
        ''',
        a_legacy=LegacyDefinition(name='x_gpaw_mix_old'))

    x_gpaw_mix_weight = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        description='''
        Mixing weight in density mixer
        ''',
        a_legacy=LegacyDefinition(name='x_gpaw_mix_weight'))

    x_gpaw_symmetry_time_reversal_switch = Quantity(
        type=bool,
        shape=[],
        description='''
        Was time reserval symmetry used
        ''',
        a_legacy=LegacyDefinition(name='x_gpaw_symmetry_time_reversal_switch'))

    x_gpaw_xc_functional = Quantity(
        type=str,
        shape=[],
        description='''
        The XC functional name used in gpaw as input
        ''',
        a_legacy=LegacyDefinition(name='x_gpaw_xc_functional'))

    x_gpaw_section_paw_method = SubSection(
        sub_section=SectionProxy('x_gpaw_section_paw_method'),
        repeats=True,
        a_legacy=LegacyDefinition(name='x_gpaw_section_paw_method'))


m_package.__init_metainfo__()
