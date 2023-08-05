import numpy as np            # pylint: disable=unused-import
import typing                 # pylint: disable=unused-import
from nomad.metainfo import (  # pylint: disable=unused-import
    MSection, MCategory, Category, Package, Quantity, Section, SubSection, SectionProxy,
    Reference
)
from nomad.metainfo.legacy import LegacyDefinition

from nomad.datamodel.metainfo import public

m_package = Package(
    name='fleur_nomadmetainfo_json',
    description='None',
    a_legacy=LegacyDefinition(name='fleur.nomadmetainfo.json'))


class x_fleur_header(MSection):
    '''
    header (labels) of fleur.
    '''

    m_def = Section(validate=False, a_legacy=LegacyDefinition(name='x_fleur_header'))

    x_fleur_version = Quantity(
        type=str,
        shape=[],
        description='''
        Version of Fleur
        ''',
        a_legacy=LegacyDefinition(name='x_fleur_version'))


class x_fleur_section_equiv_atoms(MSection):
    '''
    section containing a class of equivalent atoms
    '''

    m_def = Section(validate=False, a_legacy=LegacyDefinition(name='x_fleur_section_equiv_atoms'))

    x_fleur_atom_name = Quantity(
        type=str,
        shape=[],
        description='''
        name of atom, labelling non-equvalent atoms
        ''',
        a_legacy=LegacyDefinition(name='x_fleur_atom_name'))

    x_fleur_atom_pos_x = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        description='''
        position of atom x
        ''',
        a_legacy=LegacyDefinition(name='x_fleur_atom_pos_x'))

    x_fleur_atom_pos_y = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        description='''
        position of atom y
        ''',
        a_legacy=LegacyDefinition(name='x_fleur_atom_pos_y'))

    x_fleur_atom_pos_z = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        description='''
        position of atom z
        ''',
        a_legacy=LegacyDefinition(name='x_fleur_atom_pos_z'))

    x_fleur_atom_coord_scale = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        description='''
        scales coordinates by 1/scale. If film=T, scales only x&y coordinates, if film=F
        also z
        ''',
        a_legacy=LegacyDefinition(name='x_fleur_atom_coord_scale'))

    x_fleur_atomic_number_Z = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        description='''
        atomic number Z
        ''',
        a_legacy=LegacyDefinition(name='x_fleur_atomic_number_Z'))

    x_fleur_nr_equiv_atoms_in_this_atom_type = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        description='''
        number_equiv_atoms_in_this_atom_type
        ''',
        a_legacy=LegacyDefinition(name='x_fleur_nr_equiv_atoms_in_this_atom_type'))


class x_fleur_section_XC(MSection):
    '''
    exchange-correlation potential
    '''

    m_def = Section(validate=False, a_legacy=LegacyDefinition(name='x_fleur_section_XC'))

    x_fleur_exch_pot = Quantity(
        type=str,
        shape=[],
        description='''
        exchange-correlation potential, in out
        ''',
        a_legacy=LegacyDefinition(name='x_fleur_exch_pot'))

    x_fleur_xc_correction = Quantity(
        type=str,
        shape=[],
        description='''
        informaion on relativistic correction for the exchange-correlation potential, in
        out
        ''',
        a_legacy=LegacyDefinition(name='x_fleur_xc_correction'))


class section_run(public.section_run):

    m_def = Section(validate=False, extends_base_section=True, a_legacy=LegacyDefinition(name='section_run'))

    x_fleur_header = SubSection(
        sub_section=SectionProxy('x_fleur_header'),
        repeats=True,
        a_legacy=LegacyDefinition(name='x_fleur_header'))


class section_system(public.section_system):

    m_def = Section(validate=False, extends_base_section=True, a_legacy=LegacyDefinition(name='section_system'))

    x_fleur_lattice_vector_x = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        unit='meter',
        description='''
        x component of vector of unit cell
        ''',
        a_legacy=LegacyDefinition(name='x_fleur_lattice_vector_x'))

    x_fleur_lattice_vector_y = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        unit='meter',
        description='''
        y component of vector of unit cell
        ''',
        a_legacy=LegacyDefinition(name='x_fleur_lattice_vector_y'))

    x_fleur_lattice_vector_z = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        unit='meter',
        description='''
        z component of vector of unit cell
        ''',
        a_legacy=LegacyDefinition(name='x_fleur_lattice_vector_z'))

    x_fleur_rec_lattice_vector_x = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        unit='meter',
        description='''
        x component of reciprocal lattice vector
        ''',
        a_legacy=LegacyDefinition(name='x_fleur_rec_lattice_vector_x'))

    x_fleur_rec_lattice_vector_y = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        unit='meter',
        description='''
        y component of reciprocal lattice vector
        ''',
        a_legacy=LegacyDefinition(name='x_fleur_rec_lattice_vector_y'))

    x_fleur_rec_lattice_vector_z = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        unit='meter',
        description='''
        z component of reciprocal lattice vector
        ''',
        a_legacy=LegacyDefinition(name='x_fleur_rec_lattice_vector_z'))

    x_fleur_space_group = Quantity(
        type=str,
        shape=[],
        description='''
        space group
        ''',
        a_legacy=LegacyDefinition(name='x_fleur_space_group'))

    x_fleur_name_of_atom_type = Quantity(
        type=str,
        shape=[],
        description='''
        name of atom type
        ''',
        a_legacy=LegacyDefinition(name='x_fleur_name_of_atom_type'))

    x_fleur_system_nameIn = Quantity(
        type=str,
        shape=[],
        description='''
        user given name for this system given in the inp file
        ''',
        a_legacy=LegacyDefinition(name='x_fleur_system_nameIn'))

    x_fleur_system_name = Quantity(
        type=str,
        shape=[],
        description='''
        user given name for this system
        ''',
        a_legacy=LegacyDefinition(name='x_fleur_system_name'))

    x_fleur_total_atoms = Quantity(
        type=np.dtype(np.int32),
        shape=[],
        description='''
        total number of atoms
        ''',
        a_legacy=LegacyDefinition(name='x_fleur_total_atoms'))

    x_fleur_nr_of_atom_types = Quantity(
        type=np.dtype(np.int32),
        shape=[],
        description='''
        number of atom types
        ''',
        a_legacy=LegacyDefinition(name='x_fleur_nr_of_atom_types'))

    x_fleur_nuclear_number = Quantity(
        type=np.dtype(np.int32),
        shape=[],
        description='''
        nuclear number
        ''',
        a_legacy=LegacyDefinition(name='x_fleur_nuclear_number'))

    x_fleur_number_of_core_levels = Quantity(
        type=np.dtype(np.int32),
        shape=[],
        description='''
        x_fleur_number_of_core_levels
        ''',
        a_legacy=LegacyDefinition(name='x_fleur_number_of_core_levels'))

    x_fleur_lexpansion_cutoff = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        description='''
        l-expansion cutoff
        ''',
        a_legacy=LegacyDefinition(name='x_fleur_lexpansion_cutoff'))

    x_fleur_mt_gridpoints = Quantity(
        type=np.dtype(np.int32),
        shape=[],
        description='''
        muffin-tin gridpoints
        ''',
        a_legacy=LegacyDefinition(name='x_fleur_mt_gridpoints'))

    x_fleur_mt_radius = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        description='''
        muffin-tin radius
        ''',
        a_legacy=LegacyDefinition(name='x_fleur_mt_radius'))

    x_fleur_logarythmic_increment = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        description='''
        logarythmic increment
        ''',
        a_legacy=LegacyDefinition(name='x_fleur_logarythmic_increment'))

    x_fleur_k_max = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        description='''
        Kmax is the plane wave cut-off
        ''',
        a_legacy=LegacyDefinition(name='x_fleur_k_max'))

    x_fleur_G_max = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        description='''
        Gmax
        ''',
        a_legacy=LegacyDefinition(name='x_fleur_G_max'))

    x_fleur_tot_nucl_charge = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        description='''
        total nuclear charge
        ''',
        a_legacy=LegacyDefinition(name='x_fleur_tot_nucl_charge'))

    x_fleur_tot_elec_charge = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        description='''
        total electronic charge
        ''',
        a_legacy=LegacyDefinition(name='x_fleur_tot_elec_charge'))

    x_fleur_unit_cell_volume = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        unit='bohr ** 3',
        description='''
        unit cell volume
        ''',
        a_legacy=LegacyDefinition(name='x_fleur_unit_cell_volume'))

    x_fleur_unit_cell_volume_omega = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        description='''
        unit cell volume omega tilda
        ''',
        a_legacy=LegacyDefinition(name='x_fleur_unit_cell_volume_omega'))

    x_fleur_vol_interstitial = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        description='''
        volume of interstitial region
        ''',
        a_legacy=LegacyDefinition(name='x_fleur_vol_interstitial'))

    x_fleur_section_equiv_atoms = SubSection(
        sub_section=SectionProxy('x_fleur_section_equiv_atoms'),
        repeats=True,
        a_legacy=LegacyDefinition(name='x_fleur_section_equiv_atoms'))


class section_scf_iteration(public.section_scf_iteration):

    m_def = Section(validate=False, extends_base_section=True, a_legacy=LegacyDefinition(name='section_scf_iteration'))

    x_fleur_tot_for_x = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        description='''
        TOTAL FORCE FOR ATOM TYPE, X
        ''',
        a_legacy=LegacyDefinition(name='x_fleur_tot_for_x'))

    x_fleur_tot_for_y = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        description='''
        TOTAL FORCE FOR ATOM TYPE, Y
        ''',
        a_legacy=LegacyDefinition(name='x_fleur_tot_for_y'))

    x_fleur_tot_for_z = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        description='''
        TOTAL FORCE FOR ATOM TYPE, Z
        ''',
        a_legacy=LegacyDefinition(name='x_fleur_tot_for_z'))

    x_fleur_tot_for_fx = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        description='''
        TOTAL FORCE FOR ATOM TYPE, FX_TOT
        ''',
        a_legacy=LegacyDefinition(name='x_fleur_tot_for_fx'))

    x_fleur_tot_for_fy = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        description='''
        TOTAL FORCE FOR ATOM TYPE, FY_TOT
        ''',
        a_legacy=LegacyDefinition(name='x_fleur_tot_for_fy'))

    x_fleur_tot_for_fz = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        description='''
        TOTAL FORCE FOR ATOM TYPE, FZ_TOT
        ''',
        a_legacy=LegacyDefinition(name='x_fleur_tot_for_fz'))

    x_fleur_iteration_number = Quantity(
        type=np.dtype(np.int32),
        shape=[],
        description='''
        scf iteration number
        ''',
        a_legacy=LegacyDefinition(name='x_fleur_iteration_number'))

    x_fleur_energy_total = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        unit='joule',
        description='''
        energy total
        ''',
        a_legacy=LegacyDefinition(name='x_fleur_energy_total'))

    x_fleur_free_energy = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        unit='joule',
        description='''
        free energy
        ''',
        a_legacy=LegacyDefinition(name='x_fleur_free_energy'))

    x_fleur_entropy = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        unit='joule',
        description='''
        (tkb*entropy) TS
        ''',
        a_legacy=LegacyDefinition(name='x_fleur_entropy'))


class section_method(public.section_method):

    m_def = Section(validate=False, extends_base_section=True, a_legacy=LegacyDefinition(name='section_method'))

    x_fleur_nkptd = Quantity(
        type=np.dtype(np.int32),
        shape=[],
        description='''
        number of all the k-points
        ''',
        a_legacy=LegacyDefinition(name='x_fleur_nkptd'))

    x_fleur_k_point_x = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        description='''
        x component of vector of k point
        ''',
        a_legacy=LegacyDefinition(name='x_fleur_k_point_x'))

    x_fleur_k_point_y = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        description='''
        y component of vector of k point
        ''',
        a_legacy=LegacyDefinition(name='x_fleur_k_point_y'))

    x_fleur_k_point_z = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        description='''
        z component of vector of k point
        ''',
        a_legacy=LegacyDefinition(name='x_fleur_k_point_z'))

    x_fleur_k_point_weight = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        description='''
        weights of k point
        ''',
        a_legacy=LegacyDefinition(name='x_fleur_k_point_weight'))

    x_fleur_smearing_kind = Quantity(
        type=str,
        shape=[],
        description='''
        The Brillouin zone integration mode. It can be one of hist - Use the histogram
        mode, this is the default; gauss - Use Gaussian smearing, tria - Use the
        tetrahedron method
        ''',
        a_legacy=LegacyDefinition(name='x_fleur_smearing_kind'))

    x_fleur_smearing_width = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        unit='joule',
        description='''
        specifies the width of the broadening, smearing for calculation of fermi-energy &
        weights. The Fermi smearing can be parametrized by this energy
        ''',
        a_legacy=LegacyDefinition(name='x_fleur_smearing_width'))

    x_fleur_nr_of_valence_electrons = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        description='''
        The number of electrons to be represented within the valence electron framework
        ''',
        a_legacy=LegacyDefinition(name='x_fleur_nr_of_valence_electrons'))

    x_fleur_smearing_temperature = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        unit='kelvin',
        description='''
        Fermi smearing temperature set in Kelvin
        ''',
        a_legacy=LegacyDefinition(name='x_fleur_smearing_temperature'))

    x_fleur_section_XC = SubSection(
        sub_section=SectionProxy('x_fleur_section_XC'),
        repeats=True,
        a_legacy=LegacyDefinition(name='x_fleur_section_XC'))


m_package.__init_metainfo__()
