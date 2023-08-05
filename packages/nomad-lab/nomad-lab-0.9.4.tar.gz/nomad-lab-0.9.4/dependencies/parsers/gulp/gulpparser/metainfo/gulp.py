import numpy as np            # pylint: disable=unused-import
import typing                 # pylint: disable=unused-import
from nomad.metainfo import (  # pylint: disable=unused-import
    MSection, MCategory, Category, Package, Quantity, Section, SubSection, SectionProxy,
    Reference
)
from nomad.metainfo.legacy import LegacyDefinition

from nomad.datamodel.metainfo import public

m_package = Package(
    name='gulp_nomadmetainfo_json',
    description='None',
    a_legacy=LegacyDefinition(name='gulp.nomadmetainfo.json'))


class x_gulp_section_main_keyword(MSection):
    '''
    Section for GULP calculation mode input variable
    '''

    m_def = Section(validate=False, a_legacy=LegacyDefinition(name='x_gulp_section_main_keyword'))

    x_gulp_main_keyword = Quantity(
        type=str,
        shape=[],
        description='''
        GULP calculation mode input variable
        ''',
        a_legacy=LegacyDefinition(name='x_gulp_main_keyword'))


class x_gulp_section_forcefield(MSection):
    '''
    Section for GULP force field specification
    '''

    m_def = Section(validate=False, a_legacy=LegacyDefinition(name='x_gulp_section_forcefield'))

    x_gulp_forcefield_species_1 = Quantity(
        type=str,
        shape=[],
        description='''
        GULP force field species 1
        ''',
        a_legacy=LegacyDefinition(name='x_gulp_forcefield_species_1'))

    x_gulp_forcefield_species_2 = Quantity(
        type=str,
        shape=[],
        description='''
        GULP force field species 2
        ''',
        a_legacy=LegacyDefinition(name='x_gulp_forcefield_species_2'))

    x_gulp_forcefield_species_3 = Quantity(
        type=str,
        shape=[],
        description='''
        GULP force field species 3
        ''',
        a_legacy=LegacyDefinition(name='x_gulp_forcefield_species_3'))

    x_gulp_forcefield_species_4 = Quantity(
        type=str,
        shape=[],
        description='''
        GULP force field species 4
        ''',
        a_legacy=LegacyDefinition(name='x_gulp_forcefield_species_4'))

    x_gulp_forcefield_speciestype_1 = Quantity(
        type=str,
        shape=[],
        description='''
        GULP force field speciestype 1
        ''',
        a_legacy=LegacyDefinition(name='x_gulp_forcefield_speciestype_1'))

    x_gulp_forcefield_speciestype_2 = Quantity(
        type=str,
        shape=[],
        description='''
        GULP force field speciestype 2
        ''',
        a_legacy=LegacyDefinition(name='x_gulp_forcefield_speciestype_2'))

    x_gulp_forcefield_speciestype_3 = Quantity(
        type=str,
        shape=[],
        description='''
        GULP force field speciestype 3
        ''',
        a_legacy=LegacyDefinition(name='x_gulp_forcefield_speciestype_3'))

    x_gulp_forcefield_speciestype_4 = Quantity(
        type=str,
        shape=[],
        description='''
        GULP force field speciestype 4
        ''',
        a_legacy=LegacyDefinition(name='x_gulp_forcefield_speciestype_4'))

    x_gulp_forcefield_potential_name = Quantity(
        type=str,
        shape=[],
        description='''
        GULP force field potential name
        ''',
        a_legacy=LegacyDefinition(name='x_gulp_forcefield_potential_name'))

    x_gulp_forcefield_parameter_a = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        description='''
        GULP force field parameter A
        ''',
        a_legacy=LegacyDefinition(name='x_gulp_forcefield_parameter_a'))

    x_gulp_forcefield_parameter_b = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        description='''
        GULP force field parameter B
        ''',
        a_legacy=LegacyDefinition(name='x_gulp_forcefield_parameter_b'))

    x_gulp_forcefield_parameter_c = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        description='''
        GULP force field parameter C
        ''',
        a_legacy=LegacyDefinition(name='x_gulp_forcefield_parameter_c'))

    x_gulp_forcefield_parameter_d = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        description='''
        GULP force field parameter D
        ''',
        a_legacy=LegacyDefinition(name='x_gulp_forcefield_parameter_d'))

    x_gulp_forcefield_cutoff_min = Quantity(
        type=str,
        shape=[],
        description='''
        GULP force field cutoff min (can also be a string like 3Bond for some reason)
        ''',
        a_legacy=LegacyDefinition(name='x_gulp_forcefield_cutoff_min'))

    x_gulp_forcefield_cutoff_max = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        description='''
        GULP force field cutoff max
        ''',
        a_legacy=LegacyDefinition(name='x_gulp_forcefield_cutoff_max'))

    x_gulp_forcefield_threebody_1 = Quantity(
        type=str,
        shape=[],
        description='''
        GULP 3-body force field parameter 1
        ''',
        a_legacy=LegacyDefinition(name='x_gulp_forcefield_threebody_1'))

    x_gulp_forcefield_threebody_2 = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        description='''
        GULP 3-body force field parameter 2
        ''',
        a_legacy=LegacyDefinition(name='x_gulp_forcefield_threebody_2'))

    x_gulp_forcefield_threebody_3 = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        description='''
        GULP 3-body force field parameter 3
        ''',
        a_legacy=LegacyDefinition(name='x_gulp_forcefield_threebody_3'))

    x_gulp_forcefield_threebody_theta = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        description='''
        GULP 3-body force field parameter theta
        ''',
        a_legacy=LegacyDefinition(name='x_gulp_forcefield_threebody_theta'))

    x_gulp_forcefield_fourbody_force_constant = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        description='''
        GULP 4-body force field parameter force constant
        ''',
        a_legacy=LegacyDefinition(name='x_gulp_forcefield_fourbody_force_constant'))

    x_gulp_forcefield_fourbody_sign = Quantity(
        type=str,
        shape=[],
        description='''
        GULP 4-body force field parameter sign
        ''',
        a_legacy=LegacyDefinition(name='x_gulp_forcefield_fourbody_sign'))

    x_gulp_forcefield_fourbody_phase = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        description='''
        GULP 4-body force field parameter phase
        ''',
        a_legacy=LegacyDefinition(name='x_gulp_forcefield_fourbody_phase'))

    x_gulp_forcefield_fourbody_phi0 = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        description='''
        GULP 4-body force field parameter phi0
        ''',
        a_legacy=LegacyDefinition(name='x_gulp_forcefield_fourbody_phi0'))


class section_system(public.section_system):

    m_def = Section(validate=False, extends_base_section=True, a_legacy=LegacyDefinition(name='section_system'))

    x_gulp_patterson_group = Quantity(
        type=str,
        shape=[],
        description='''
        Patterson group
        ''',
        a_legacy=LegacyDefinition(name='x_gulp_patterson_group'))

    x_gulp_space_group = Quantity(
        type=str,
        shape=[],
        description='''
        Space group
        ''',
        a_legacy=LegacyDefinition(name='x_gulp_space_group'))

    x_gulp_formula = Quantity(
        type=str,
        shape=[],
        description='''
        GULP chemical formula
        ''',
        a_legacy=LegacyDefinition(name='x_gulp_formula'))

    x_gulp_cell_alpha = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        description='''
        grrr
        ''',
        a_legacy=LegacyDefinition(name='x_gulp_cell_alpha'))

    x_gulp_cell_beta = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        description='''
        grrr
        ''',
        a_legacy=LegacyDefinition(name='x_gulp_cell_beta'))

    x_gulp_cell_gamma = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        description='''
        grrr
        ''',
        a_legacy=LegacyDefinition(name='x_gulp_cell_gamma'))

    x_gulp_cell_a = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        description='''
        grrr
        ''',
        a_legacy=LegacyDefinition(name='x_gulp_cell_a'))

    x_gulp_cell_b = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        description='''
        grrr
        ''',
        a_legacy=LegacyDefinition(name='x_gulp_cell_b'))

    x_gulp_cell_c = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        description='''
        grrr
        ''',
        a_legacy=LegacyDefinition(name='x_gulp_cell_c'))

    x_gulp_prim_cell_alpha = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        description='''
        grrr
        ''',
        a_legacy=LegacyDefinition(name='x_gulp_prim_cell_alpha'))

    x_gulp_prim_cell_beta = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        description='''
        grrr
        ''',
        a_legacy=LegacyDefinition(name='x_gulp_prim_cell_beta'))

    x_gulp_prim_cell_gamma = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        description='''
        grrr
        ''',
        a_legacy=LegacyDefinition(name='x_gulp_prim_cell_gamma'))

    x_gulp_prim_cell_a = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        description='''
        grrr
        ''',
        a_legacy=LegacyDefinition(name='x_gulp_prim_cell_a'))

    x_gulp_prim_cell_b = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        description='''
        grrr
        ''',
        a_legacy=LegacyDefinition(name='x_gulp_prim_cell_b'))

    x_gulp_prim_cell_c = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        description='''
        grrr
        ''',
        a_legacy=LegacyDefinition(name='x_gulp_prim_cell_c'))

    x_gulp_pbc = Quantity(
        type=np.dtype(np.int32),
        shape=[],
        description='''
        grrr
        ''',
        a_legacy=LegacyDefinition(name='x_gulp_pbc'))


class section_run(public.section_run):

    m_def = Section(validate=False, extends_base_section=True, a_legacy=LegacyDefinition(name='section_run'))

    x_gulp_title = Quantity(
        type=str,
        shape=[],
        description='''
        Title of GULP calculation
        ''',
        a_legacy=LegacyDefinition(name='x_gulp_title'))

    x_gulp_section_main_keyword = SubSection(
        sub_section=SectionProxy('x_gulp_section_main_keyword'),
        repeats=True,
        a_legacy=LegacyDefinition(name='x_gulp_section_main_keyword'))


class section_method(public.section_method):

    m_def = Section(validate=False, extends_base_section=True, a_legacy=LegacyDefinition(name='section_method'))

    x_gulp_number_of_species = Quantity(
        type=int,
        shape=[],
        description='''
        Number of species in GULP
        ''',
        a_legacy=LegacyDefinition(name='x_gulp_number_of_species'))

    x_gulp_species_charge = Quantity(
        type=np.dtype(np.float64),
        shape=['x_gulp_number_of_species'],
        description='''
        Number of species in GULP
        ''',
        a_legacy=LegacyDefinition(name='x_gulp_species_charge'))

    x_gulp_section_forcefield = SubSection(
        sub_section=SectionProxy('x_gulp_section_forcefield'),
        repeats=True,
        a_legacy=LegacyDefinition(name='x_gulp_section_forcefield'))


class section_single_configuration_calculation(public.section_single_configuration_calculation):

    m_def = Section(validate=False, extends_base_section=True, a_legacy=LegacyDefinition(name='section_single_configuration_calculation'))

    x_gulp_energy_attachment_energy = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        description='''
        GULP energy term for attachment_energy
        ''',
        a_legacy=LegacyDefinition(name='x_gulp_energy_attachment_energy'))

    x_gulp_energy_attachment_energy_unit = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        description='''
        GULP energy term for attachment_energy_unit
        ''',
        a_legacy=LegacyDefinition(name='x_gulp_energy_attachment_energy_unit'))

    x_gulp_energy_bond_order_potentials = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        description='''
        GULP energy term for bond_order_potentials
        ''',
        a_legacy=LegacyDefinition(name='x_gulp_energy_bond_order_potentials'))

    x_gulp_energy_brenner_potentials = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        description='''
        GULP energy term for brenner_potentials
        ''',
        a_legacy=LegacyDefinition(name='x_gulp_energy_brenner_potentials'))

    x_gulp_energy_bulk_energy = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        description='''
        GULP energy term for bulk_energy
        ''',
        a_legacy=LegacyDefinition(name='x_gulp_energy_bulk_energy'))

    x_gulp_energy_dispersion_real_recip = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        description='''
        GULP energy term for dispersion_real_recip
        ''',
        a_legacy=LegacyDefinition(name='x_gulp_energy_dispersion_real_recip'))

    x_gulp_energy_electric_field_times_distance = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        description='''
        GULP energy term for electric_field_times_distance
        ''',
        a_legacy=LegacyDefinition(name='x_gulp_energy_electric_field_times_distance'))

    x_gulp_energy_energy_shift = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        description='''
        GULP energy term for energy_shift
        ''',
        a_legacy=LegacyDefinition(name='x_gulp_energy_energy_shift'))

    x_gulp_energy_four_body_potentials = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        description='''
        GULP energy term for four_body_potentials
        ''',
        a_legacy=LegacyDefinition(name='x_gulp_energy_four_body_potentials'))

    x_gulp_energy_improper_torsions = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        description='''
        GULP energy term for improper_torsions
        ''',
        a_legacy=LegacyDefinition(name='x_gulp_energy_improper_torsions'))

    x_gulp_energy_interatomic_potentials = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        description='''
        GULP energy term for interatomic_potentials
        ''',
        a_legacy=LegacyDefinition(name='x_gulp_energy_interatomic_potentials'))

    x_gulp_energy_many_body_potentials = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        description='''
        GULP energy term for many_body_potentials
        ''',
        a_legacy=LegacyDefinition(name='x_gulp_energy_many_body_potentials'))

    x_gulp_energy_monopole_monopole_real = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        description='''
        GULP energy term for monopole_monopole_real
        ''',
        a_legacy=LegacyDefinition(name='x_gulp_energy_monopole_monopole_real'))

    x_gulp_energy_monopole_monopole_recip = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        description='''
        GULP energy term for monopole_monopole_recip
        ''',
        a_legacy=LegacyDefinition(name='x_gulp_energy_monopole_monopole_recip'))

    x_gulp_energy_monopole_monopole_total = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        description='''
        GULP energy term for monopole_monopole_total
        ''',
        a_legacy=LegacyDefinition(name='x_gulp_energy_monopole_monopole_total'))

    x_gulp_energy_neutralising_energy = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        description='''
        GULP energy term for neutralising_energy
        ''',
        a_legacy=LegacyDefinition(name='x_gulp_energy_neutralising_energy'))

    x_gulp_energy_non_primitive_unit_cell = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        description='''
        GULP energy term for non_primitive_unit_cell
        ''',
        a_legacy=LegacyDefinition(name='x_gulp_energy_non_primitive_unit_cell'))

    x_gulp_energy_out_of_plane_potentials = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        description='''
        GULP energy term for out_of_plane_potentials
        ''',
        a_legacy=LegacyDefinition(name='x_gulp_energy_out_of_plane_potentials'))

    x_gulp_energy_primitive_unit_cell = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        description='''
        GULP energy term for primitive_unit_cell
        ''',
        a_legacy=LegacyDefinition(name='x_gulp_energy_primitive_unit_cell'))

    x_gulp_energy_reaxff_force_field = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        description='''
        GULP energy term for reaxff_force_field
        ''',
        a_legacy=LegacyDefinition(name='x_gulp_energy_reaxff_force_field'))

    x_gulp_energy_region_1_2_interaction = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        description='''
        GULP energy term for region_1_2_interaction
        ''',
        a_legacy=LegacyDefinition(name='x_gulp_energy_region_1_2_interaction'))

    x_gulp_energy_region_2_2_interaction = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        description='''
        GULP energy term for region_2_2_interaction
        ''',
        a_legacy=LegacyDefinition(name='x_gulp_energy_region_2_2_interaction'))

    x_gulp_energy_self_energy_eem_qeq_sm = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        description='''
        GULP energy term for self_energy_eem_qeq_sm
        ''',
        a_legacy=LegacyDefinition(name='x_gulp_energy_self_energy_eem_qeq_sm'))

    x_gulp_energy_sm_coulomb_correction = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        description='''
        GULP energy term for sm_coulomb_correction
        ''',
        a_legacy=LegacyDefinition(name='x_gulp_energy_sm_coulomb_correction'))

    x_gulp_energy_solvation_energy = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        description='''
        GULP energy term for solvation_energy
        ''',
        a_legacy=LegacyDefinition(name='x_gulp_energy_solvation_energy'))

    x_gulp_energy_three_body_potentials = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        description='''
        GULP energy term for three_body_potentials
        ''',
        a_legacy=LegacyDefinition(name='x_gulp_energy_three_body_potentials'))

    x_gulp_energy_total_lattice_energy = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        description='''
        GULP energy term for total_lattice_energy
        ''',
        a_legacy=LegacyDefinition(name='x_gulp_energy_total_lattice_energy'))

    x_gulp_md_time = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        description='''
        GULP molecular dynamics time
        ''',
        a_legacy=LegacyDefinition(name='x_gulp_md_time'))

    x_gulp_md_kinetic_energy = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        description='''
        GULP molecular dynamics kinetic energy
        ''',
        a_legacy=LegacyDefinition(name='x_gulp_md_kinetic_energy'))

    x_gulp_md_potential_energy = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        description='''
        GULP molecular dynamics potential energy
        ''',
        a_legacy=LegacyDefinition(name='x_gulp_md_potential_energy'))

    x_gulp_md_total_energy = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        description='''
        GULP molecular dynamics total energy
        ''',
        a_legacy=LegacyDefinition(name='x_gulp_md_total_energy'))

    x_gulp_md_temperature = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        description='''
        GULP molecular dynamics temperature
        ''',
        a_legacy=LegacyDefinition(name='x_gulp_md_temperature'))

    x_gulp_md_pressure = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        description='''
        GULP molecular dynamics pressure
        ''',
        a_legacy=LegacyDefinition(name='x_gulp_md_pressure'))


m_package.__init_metainfo__()
