import numpy as np            # pylint: disable=unused-import
import typing                 # pylint: disable=unused-import
from nomad.metainfo import (  # pylint: disable=unused-import
    MSection, MCategory, Category, Package, Quantity, Section, SubSection, SectionProxy,
    Reference
)
from nomad.metainfo.legacy import LegacyDefinition

from nomad.datamodel.metainfo import public
from nomad.datamodel.metainfo import common

m_package = Package(
    name='tinker_nomadmetainfo_json',
    description='None',
    a_legacy=LegacyDefinition(name='tinker.nomadmetainfo.json'))


class x_tinker_mdin_input_output_files(MCategory):
    '''
    Parameters of mdin belonging to x_tinker_section_control_parameters.
    '''

    m_def = Category(
        a_legacy=LegacyDefinition(name='x_tinker_mdin_input_output_files'))


class x_tinker_mdin_control_parameters(MCategory):
    '''
    Parameters of mdin belonging to x_tinker_section_control_parameters.
    '''

    m_def = Category(
        a_legacy=LegacyDefinition(name='x_tinker_mdin_control_parameters'))


class x_tinker_mdin_method(MCategory):
    '''
    Parameters of mdin belonging to section method.
    '''

    m_def = Category(
        a_legacy=LegacyDefinition(name='x_tinker_mdin_method'))


class x_tinker_mdout_single_configuration_calculation(MCategory):
    '''
    Parameters of mdout belonging to section_single_configuration_calculation.
    '''

    m_def = Category(
        a_legacy=LegacyDefinition(name='x_tinker_mdout_single_configuration_calculation'))


class x_tinker_mdout_method(MCategory):
    '''
    Parameters of mdin belonging to section method.
    '''

    m_def = Category(
        a_legacy=LegacyDefinition(name='x_tinker_mdout_method'))


class x_tinker_mdout_run(MCategory):
    '''
    Parameters of mdin belonging to settings run.
    '''

    m_def = Category(
        categories=[public.settings_run],
        a_legacy=LegacyDefinition(name='x_tinker_mdout_run'))


class x_tinker_mdin_run(MCategory):
    '''
    Parameters of mdin belonging to settings run.
    '''

    m_def = Category(
        categories=[public.settings_run],
        a_legacy=LegacyDefinition(name='x_tinker_mdin_run'))


class x_tinker_section_input_output_files(MSection):
    '''
    Section to store input and output file names
    '''

    m_def = Section(validate=False, a_legacy=LegacyDefinition(name='x_tinker_section_input_output_files'))


class x_tinker_section_control_parameters(MSection):
    '''
    Section to store the input and output control parameters
    '''

    m_def = Section(validate=False, a_legacy=LegacyDefinition(name='x_tinker_section_control_parameters'))

    x_tinker_inout_file_structure = Quantity(
        type=str,
        shape=[],
        description='''
        tinker input topology file.
        ''',
        a_legacy=LegacyDefinition(name='x_tinker_inout_file_structure'))

    x_tinker_inout_file_trajectory = Quantity(
        type=str,
        shape=[],
        description='''
        tinker output trajectory file.
        ''',
        a_legacy=LegacyDefinition(name='x_tinker_inout_file_trajectory'))

    x_tinker_inout_file_traj_coord = Quantity(
        type=str,
        shape=[],
        description='''
        tinker output trajectory file.
        ''',
        a_legacy=LegacyDefinition(name='x_tinker_inout_file_traj_coord'))

    x_tinker_inout_file_traj_vel = Quantity(
        type=str,
        shape=[],
        description='''
        tinker output file for velocities in the trajectory.
        ''',
        a_legacy=LegacyDefinition(name='x_tinker_inout_file_traj_vel'))

    x_tinker_inout_file_traj_force = Quantity(
        type=str,
        shape=[],
        description='''
        tinker output file for forces in the trajectory.
        ''',
        a_legacy=LegacyDefinition(name='x_tinker_inout_file_traj_force'))

    x_tinker_inout_file_output_coord = Quantity(
        type=str,
        shape=[],
        description='''
        tinker output coordinates file.
        ''',
        a_legacy=LegacyDefinition(name='x_tinker_inout_file_output_coord'))

    x_tinker_inout_file_output_vel = Quantity(
        type=str,
        shape=[],
        description='''
        tinker output velocities file.
        ''',
        a_legacy=LegacyDefinition(name='x_tinker_inout_file_output_vel'))

    x_tinker_inout_file_output_force = Quantity(
        type=str,
        shape=[],
        description='''
        tinker output forces file.
        ''',
        a_legacy=LegacyDefinition(name='x_tinker_inout_file_output_force'))

    x_tinker_inout_file_input_coord = Quantity(
        type=str,
        shape=[],
        description='''
        tinker input coordinates file.
        ''',
        a_legacy=LegacyDefinition(name='x_tinker_inout_file_input_coord'))

    x_tinker_inout_file_input_vel = Quantity(
        type=str,
        shape=[],
        description='''
        tinker input velocities file.
        ''',
        a_legacy=LegacyDefinition(name='x_tinker_inout_file_input_vel'))

    x_tinker_inout_file_restart_coord = Quantity(
        type=str,
        shape=[],
        description='''
        tinker restart coordinates file.
        ''',
        a_legacy=LegacyDefinition(name='x_tinker_inout_file_restart_coord'))

    x_tinker_inout_file_restart_vel = Quantity(
        type=str,
        shape=[],
        description='''
        tinker restart velocities file.
        ''',
        a_legacy=LegacyDefinition(name='x_tinker_inout_file_restart_vel'))

    x_tinker_inout_file_output_log = Quantity(
        type=str,
        shape=[],
        description='''
        tinker MD output log file.
        ''',
        a_legacy=LegacyDefinition(name='x_tinker_inout_file_output_log'))

    x_tinker_inout_control_number_of_steps = Quantity(
        type=str,
        shape=[],
        description='''
        tinker running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_tinker_inout_control_number_of_steps'))

    x_tinker_inout_control_polar_eps = Quantity(
        type=str,
        shape=[],
        description='''
        tinker running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_tinker_inout_control_polar_eps'))

    x_tinker_inout_control_initial_temperature = Quantity(
        type=str,
        shape=[],
        description='''
        tinker running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_tinker_inout_control_initial_temperature'))

    x_tinker_inout_control_dielectric = Quantity(
        type=str,
        shape=[],
        description='''
        tinker running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_tinker_inout_control_dielectric'))

    x_tinker_inout_control_minimization = Quantity(
        type=str,
        shape=[],
        description='''
        tinker running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_tinker_inout_control_minimization'))

    x_tinker_inout_control_integrator = Quantity(
        type=str,
        shape=[],
        description='''
        tinker running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_tinker_inout_control_integrator'))

    x_tinker_inout_control_parameters = Quantity(
        type=str,
        shape=[],
        description='''
        tinker running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_tinker_inout_control_parameters'))

    x_tinker_inout_control_verbose = Quantity(
        type=bool,
        shape=[],
        description='''
        tinker running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_tinker_inout_control_verbose'))

    x_tinker_inout_control_a_axis = Quantity(
        type=str,
        shape=[],
        description='''
        tinker running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_tinker_inout_control_a_axis'))

    x_tinker_inout_control_b_axis = Quantity(
        type=str,
        shape=[],
        description='''
        tinker running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_tinker_inout_control_b_axis'))

    x_tinker_inout_control_c_axis = Quantity(
        type=str,
        shape=[],
        description='''
        tinker running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_tinker_inout_control_c_axis'))

    x_tinker_inout_control_alpha = Quantity(
        type=str,
        shape=[],
        description='''
        tinker running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_tinker_inout_control_alpha'))

    x_tinker_inout_control_beta = Quantity(
        type=str,
        shape=[],
        description='''
        tinker running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_tinker_inout_control_beta'))

    x_tinker_inout_control_gamma = Quantity(
        type=str,
        shape=[],
        description='''
        tinker running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_tinker_inout_control_gamma'))

    x_tinker_inout_control_tau_pressure = Quantity(
        type=str,
        shape=[],
        description='''
        tinker running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_tinker_inout_control_tau_pressure'))

    x_tinker_inout_control_tau_temperature = Quantity(
        type=str,
        shape=[],
        description='''
        tinker running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_tinker_inout_control_tau_temperature'))

    x_tinker_inout_control_debug = Quantity(
        type=bool,
        shape=[],
        description='''
        tinker running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_tinker_inout_control_debug'))

    x_tinker_inout_control_group = Quantity(
        type=bool,
        shape=[],
        description='''
        tinker running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_tinker_inout_control_group'))

    x_tinker_inout_control_group_inter = Quantity(
        type=str,
        shape=[],
        description='''
        tinker running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_tinker_inout_control_group_inter'))

    x_tinker_inout_control_vib_roots = Quantity(
        type=str,
        shape=[],
        description='''
        tinker running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_tinker_inout_control_vib_roots'))

    x_tinker_inout_control_spacegroup = Quantity(
        type=str,
        shape=[],
        description='''
        tinker running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_tinker_inout_control_spacegroup'))

    x_tinker_inout_control_digits = Quantity(
        type=str,
        shape=[],
        description='''
        tinker running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_tinker_inout_control_digits'))

    x_tinker_inout_control_printout = Quantity(
        type=str,
        shape=[],
        description='''
        tinker running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_tinker_inout_control_printout'))

    x_tinker_inout_control_enforce_chirality = Quantity(
        type=bool,
        shape=[],
        description='''
        tinker running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_tinker_inout_control_enforce_chirality'))

    x_tinker_inout_control_neighbor_list = Quantity(
        type=bool,
        shape=[],
        description='''
        tinker running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_tinker_inout_control_neighbor_list'))

    x_tinker_inout_control_vdw_cutoff = Quantity(
        type=str,
        shape=[],
        description='''
        tinker running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_tinker_inout_control_vdw_cutoff'))

    x_tinker_inout_control_vdw_correction = Quantity(
        type=bool,
        shape=[],
        description='''
        tinker running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_tinker_inout_control_vdw_correction'))

    x_tinker_inout_control_ewald = Quantity(
        type=bool,
        shape=[],
        description='''
        tinker running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_tinker_inout_control_ewald'))

    x_tinker_inout_control_ewald_cutoff = Quantity(
        type=bool,
        shape=[],
        description='''
        tinker running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_tinker_inout_control_ewald_cutoff'))

    x_tinker_inout_control_archive = Quantity(
        type=bool,
        shape=[],
        description='''
        tinker running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_tinker_inout_control_archive'))

    x_tinker_inout_control_barostat = Quantity(
        type=str,
        shape=[],
        description='''
        tinker running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_tinker_inout_control_barostat'))

    x_tinker_inout_control_aniso_pressure = Quantity(
        type=bool,
        shape=[],
        description='''
        tinker running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_tinker_inout_control_aniso_pressure'))

    x_tinker_inout_control_lights = Quantity(
        type=bool,
        shape=[],
        description='''
        tinker running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_tinker_inout_control_lights'))

    x_tinker_inout_control_randomseed = Quantity(
        type=str,
        shape=[],
        description='''
        tinker running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_tinker_inout_control_randomseed'))

    x_tinker_inout_control_saddlepoint = Quantity(
        type=bool,
        shape=[],
        description='''
        tinker running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_tinker_inout_control_saddlepoint'))

    x_tinker_inout_control_vdwtype = Quantity(
        type=str,
        shape=[],
        description='''
        tinker running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_tinker_inout_control_vdwtype'))

    x_tinker_inout_control_title = Quantity(
        type=str,
        shape=[],
        description='''
        tinker running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_tinker_inout_control_title'))

    x_tinker_inout_control_step_t = Quantity(
        type=str,
        shape=[],
        description='''
        tinker running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_tinker_inout_control_step_t'))

    x_tinker_inout_control_step_dt = Quantity(
        type=str,
        shape=[],
        description='''
        tinker running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_tinker_inout_control_step_dt'))

    x_tinker_inout_control_random_number_generator_seed = Quantity(
        type=str,
        shape=[],
        description='''
        tinker running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_tinker_inout_control_random_number_generator_seed'))

    x_tinker_inout_control_radiusrule = Quantity(
        type=str,
        shape=[],
        description='''
        tinker running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_tinker_inout_control_radiusrule'))

    x_tinker_inout_control_radiustype = Quantity(
        type=str,
        shape=[],
        description='''
        tinker running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_tinker_inout_control_radiustype'))

    x_tinker_inout_control_radiussize = Quantity(
        type=str,
        shape=[],
        description='''
        tinker running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_tinker_inout_control_radiussize'))

    x_tinker_inout_control_epsilonrule = Quantity(
        type=str,
        shape=[],
        description='''
        tinker running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_tinker_inout_control_epsilonrule'))

    x_tinker_inout_control_rattle = Quantity(
        type=str,
        shape=[],
        description='''
        tinker running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_tinker_inout_control_rattle'))

    x_tinker_inout_control_lambda = Quantity(
        type=str,
        shape=[],
        description='''
        tinker running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_tinker_inout_control_lambda'))

    x_tinker_inout_control_mutate = Quantity(
        type=str,
        shape=[],
        description='''
        tinker running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_tinker_inout_control_mutate'))

    x_tinker_inout_control_basin = Quantity(
        type=str,
        shape=[],
        description='''
        tinker running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_tinker_inout_control_basin'))

    x_tinker_inout_control_pme_grid = Quantity(
        type=str,
        shape=[],
        description='''
        tinker running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_tinker_inout_control_pme_grid'))

    x_tinker_inout_control_pme_order = Quantity(
        type=str,
        shape=[],
        description='''
        tinker running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_tinker_inout_control_pme_order'))

    x_tinker_inout_control_nstep = Quantity(
        type=np.dtype(np.int32),
        shape=[],
        description='''
        tinker running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_tinker_inout_control_nstep'))

    x_tinker_inout_control_initial_configuration_file = Quantity(
        type=str,
        shape=[],
        description='''
        tinker running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_tinker_inout_control_initial_configuration_file'))

    x_tinker_inout_control_final_configuration_file = Quantity(
        type=str,
        shape=[],
        description='''
        tinker running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_tinker_inout_control_final_configuration_file'))

    x_tinker_inout_control_initial_trajectory_file = Quantity(
        type=str,
        shape=[],
        description='''
        tinker running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_tinker_inout_control_initial_trajectory_file'))

    x_tinker_inout_control_restart_file = Quantity(
        type=str,
        shape=[],
        description='''
        tinker running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_tinker_inout_control_restart_file'))

    x_tinker_inout_control_archive_file = Quantity(
        type=str,
        shape=[],
        description='''
        tinker running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_tinker_inout_control_archive_file'))

    x_tinker_inout_control_force_field_file = Quantity(
        type=str,
        shape=[],
        description='''
        tinker running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_tinker_inout_control_force_field_file'))

    x_tinker_inout_control_key_file = Quantity(
        type=str,
        shape=[],
        description='''
        tinker running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_tinker_inout_control_key_file'))

    x_tinker_inout_control_coordinate_file_list = Quantity(
        type=str,
        shape=[],
        description='''
        tinker running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_tinker_inout_control_coordinate_file_list'))

    x_tinker_inout_control_structure_file = Quantity(
        type=str,
        shape=[],
        description='''
        tinker running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_tinker_inout_control_structure_file'))

    x_tinker_inout_control_parameter_file = Quantity(
        type=str,
        shape=[],
        description='''
        tinker running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_tinker_inout_control_parameter_file'))

    x_tinker_inout_control_input_file = Quantity(
        type=str,
        shape=[],
        description='''
        tinker running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_tinker_inout_control_input_file'))

    x_tinker_inout_control_topology_file = Quantity(
        type=str,
        shape=[],
        description='''
        tinker running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_tinker_inout_control_topology_file'))

    x_tinker_inout_control_configuration_file = Quantity(
        type=str,
        shape=[],
        description='''
        tinker running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_tinker_inout_control_configuration_file'))

    x_tinker_inout_control_number_of_parameter_files = Quantity(
        type=np.dtype(np.int32),
        shape=[],
        description='''
        tinker running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_tinker_inout_control_number_of_parameter_files'))

    x_tinker_inout_control_parameter_files = Quantity(
        type=str,
        shape=['x_tinker_inout_control_number_of_parameter_files'],
        description='''
        tinker running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_tinker_inout_control_parameter_files'))

    x_tinker_section_input_output_files = SubSection(
        sub_section=SectionProxy('x_tinker_section_input_output_files'),
        repeats=True,
        a_legacy=LegacyDefinition(name='x_tinker_section_input_output_files'))


class x_tinker_section_atom_to_atom_type_ref(MSection):
    '''
    Section to store atom label to atom type definition list
    '''

    m_def = Section(validate=False, a_legacy=LegacyDefinition(name='x_tinker_section_atom_to_atom_type_ref'))

    x_tinker_atom_to_atom_type_ref = Quantity(
        type=np.dtype(np.int64),
        shape=['number_of_atoms_per_type'],
        description='''
        Reference to the atoms of each atom type.
        ''',
        a_legacy=LegacyDefinition(name='x_tinker_atom_to_atom_type_ref'))


class x_tinker_section_single_configuration_calculation(MSection):
    '''
    section for gathering values for MD steps
    '''

    m_def = Section(validate=False, a_legacy=LegacyDefinition(name='x_tinker_section_single_configuration_calculation'))


class section_system(public.section_system):

    m_def = Section(validate=False, extends_base_section=True, a_legacy=LegacyDefinition(name='section_system'))

    x_tinker_atom_positions_image_index = Quantity(
        type=np.dtype(np.int32),
        shape=['number_of_atoms', 3],
        unit='dimensionless',
        description='''
        PBC image flag index.
        ''',
        a_legacy=LegacyDefinition(name='x_tinker_atom_positions_image_index'))

    x_tinker_atom_positions_scaled = Quantity(
        type=np.dtype(np.float64),
        shape=['number_of_atoms', 3],
        unit='dimensionless',
        description='''
        Position of the atoms in a scaled format [0, 1].
        ''',
        a_legacy=LegacyDefinition(name='x_tinker_atom_positions_scaled'))

    x_tinker_atom_positions_wrapped = Quantity(
        type=np.dtype(np.float64),
        shape=['number_of_atoms', 3],
        unit='meter',
        description='''
        Position of the atoms wrapped back to the periodic box.
        ''',
        a_legacy=LegacyDefinition(name='x_tinker_atom_positions_wrapped'))

    x_tinker_lattice_lengths = Quantity(
        type=np.dtype(np.float64),
        shape=[3],
        description='''
        Lattice dimensions in a vector. Vector includes [a, b, c] lengths.
        ''',
        categories=[public.configuration_core],
        a_legacy=LegacyDefinition(name='x_tinker_lattice_lengths'))

    x_tinker_lattice_angles = Quantity(
        type=np.dtype(np.float64),
        shape=[3],
        description='''
        Angles of lattice vectors. Vector includes [alpha, beta, gamma] in degrees.
        ''',
        categories=[public.configuration_core],
        a_legacy=LegacyDefinition(name='x_tinker_lattice_angles'))

    x_tinker_dummy = Quantity(
        type=str,
        shape=[],
        description='''
        dummy
        ''',
        a_legacy=LegacyDefinition(name='x_tinker_dummy'))

    x_tinker_mdin_finline = Quantity(
        type=str,
        shape=[],
        description='''
        finline in mdin
        ''',
        a_legacy=LegacyDefinition(name='x_tinker_mdin_finline'))

    x_tinker_traj_timestep_store = Quantity(
        type=str,
        shape=[],
        description='''
        tmp
        ''',
        a_legacy=LegacyDefinition(name='x_tinker_traj_timestep_store'))

    x_tinker_traj_number_of_atoms_store = Quantity(
        type=str,
        shape=[],
        description='''
        tmp
        ''',
        a_legacy=LegacyDefinition(name='x_tinker_traj_number_of_atoms_store'))

    x_tinker_traj_box_bound_store = Quantity(
        type=str,
        shape=[],
        description='''
        tmp
        ''',
        a_legacy=LegacyDefinition(name='x_tinker_traj_box_bound_store'))

    x_tinker_traj_box_bounds_store = Quantity(
        type=str,
        shape=[],
        description='''
        tmp
        ''',
        a_legacy=LegacyDefinition(name='x_tinker_traj_box_bounds_store'))

    x_tinker_traj_variables_store = Quantity(
        type=str,
        shape=[],
        description='''
        tmp
        ''',
        a_legacy=LegacyDefinition(name='x_tinker_traj_variables_store'))

    x_tinker_traj_atoms_store = Quantity(
        type=str,
        shape=[],
        description='''
        tmp
        ''',
        a_legacy=LegacyDefinition(name='x_tinker_traj_atoms_store'))


class section_sampling_method(public.section_sampling_method):

    m_def = Section(validate=False, extends_base_section=True, a_legacy=LegacyDefinition(name='section_sampling_method'))

    x_tinker_barostat_target_pressure = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        unit='pascal',
        description='''
        MD barostat target pressure.
        ''',
        categories=[public.settings_molecular_dynamics, public.settings_barostat, public.settings_sampling],
        a_legacy=LegacyDefinition(name='x_tinker_barostat_target_pressure'))

    x_tinker_barostat_tau = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        unit='second',
        description='''
        MD barostat relaxation time.
        ''',
        categories=[public.settings_molecular_dynamics, public.settings_barostat, public.settings_sampling],
        a_legacy=LegacyDefinition(name='x_tinker_barostat_tau'))

    x_tinker_barostat_type = Quantity(
        type=str,
        shape=[],
        description='''
        MD barostat type, valid values are defined in the barostat_type wiki page.
        ''',
        categories=[public.settings_molecular_dynamics, public.settings_barostat, public.settings_sampling],
        a_legacy=LegacyDefinition(name='x_tinker_barostat_type'))

    x_tinker_integrator_dt = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        unit='second',
        description='''
        MD integration time step.
        ''',
        categories=[public.settings_molecular_dynamics, public.settings_integrator, public.settings_sampling],
        a_legacy=LegacyDefinition(name='x_tinker_integrator_dt'))

    x_tinker_integrator_type = Quantity(
        type=str,
        shape=[],
        description='''
        MD integrator type, valid values are defined in the integrator_type wiki page.
        ''',
        categories=[public.settings_molecular_dynamics, public.settings_integrator, public.settings_sampling],
        a_legacy=LegacyDefinition(name='x_tinker_integrator_type'))

    x_tinker_periodicity_type = Quantity(
        type=str,
        shape=[],
        description='''
        Periodic boundary condition type in the sampling (non-PBC or PBC).
        ''',
        categories=[public.settings_molecular_dynamics, public.settings_integrator, public.settings_sampling],
        a_legacy=LegacyDefinition(name='x_tinker_periodicity_type'))

    x_tinker_langevin_gamma = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        unit='second',
        description='''
        Langevin thermostat damping factor.
        ''',
        categories=[public.settings_molecular_dynamics, public.settings_sampling, public.settings_thermostat],
        a_legacy=LegacyDefinition(name='x_tinker_langevin_gamma'))

    x_tinker_number_of_steps_requested = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        description='''
        Number of requested MD integration time steps.
        ''',
        categories=[public.settings_molecular_dynamics, public.settings_integrator, public.settings_sampling],
        a_legacy=LegacyDefinition(name='x_tinker_number_of_steps_requested'))

    x_tinker_thermostat_level = Quantity(
        type=str,
        shape=[],
        description='''
        MD thermostat level (see wiki: single, multiple, regional).
        ''',
        categories=[public.settings_molecular_dynamics, public.settings_sampling, public.settings_thermostat],
        a_legacy=LegacyDefinition(name='x_tinker_thermostat_level'))

    x_tinker_thermostat_target_temperature = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        unit='kelvin',
        description='''
        MD thermostat target temperature.
        ''',
        categories=[public.settings_molecular_dynamics, public.settings_sampling, public.settings_thermostat],
        a_legacy=LegacyDefinition(name='x_tinker_thermostat_target_temperature'))

    x_tinker_thermostat_tau = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        unit='second',
        description='''
        MD thermostat relaxation time.
        ''',
        categories=[public.settings_molecular_dynamics, public.settings_sampling, public.settings_thermostat],
        a_legacy=LegacyDefinition(name='x_tinker_thermostat_tau'))

    x_tinker_thermostat_type = Quantity(
        type=str,
        shape=[],
        description='''
        MD thermostat type, valid values are defined in the thermostat_type wiki page.
        ''',
        categories=[public.settings_molecular_dynamics, public.settings_sampling, public.settings_thermostat],
        a_legacy=LegacyDefinition(name='x_tinker_thermostat_type'))


class section_atom_type(common.section_atom_type):

    m_def = Section(validate=False, extends_base_section=True, a_legacy=LegacyDefinition(name='section_atom_type'))

    x_tinker_atom_name = Quantity(
        type=str,
        shape=[],
        description='''
        Atom name of an atom in topology definition.
        ''',
        a_legacy=LegacyDefinition(name='x_tinker_atom_name'))

    x_tinker_atom_type = Quantity(
        type=str,
        shape=[],
        description='''
        Atom type of an atom in topology definition.
        ''',
        a_legacy=LegacyDefinition(name='x_tinker_atom_type'))

    x_tinker_atom_element = Quantity(
        type=str,
        shape=[],
        description='''
        Atom type of an atom in topology definition.
        ''',
        a_legacy=LegacyDefinition(name='x_tinker_atom_element'))

    x_tinker_atom_type_element = Quantity(
        type=str,
        shape=[],
        description='''
        Element symbol of an atom type.
        ''',
        a_legacy=LegacyDefinition(name='x_tinker_atom_type_element'))

    x_tinker_atom_type_radius = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        description='''
        van der Waals radius of an atom type.
        ''',
        a_legacy=LegacyDefinition(name='x_tinker_atom_type_radius'))

    number_of_atoms_per_type = Quantity(
        type=int,
        shape=[],
        description='''
        Number of atoms involved in this type.
        ''',
        a_legacy=LegacyDefinition(name='number_of_atoms_per_type'))


class section_interaction(common.section_interaction):

    m_def = Section(validate=False, extends_base_section=True, a_legacy=LegacyDefinition(name='section_interaction'))

    x_tinker_interaction_atom_to_atom_type_ref = Quantity(
        type=common.section_atom_type,
        shape=['number_of_atoms_per_interaction'],
        description='''
        Reference to the atom type of each interaction atoms.
        ''',
        a_legacy=LegacyDefinition(name='x_tinker_interaction_atom_to_atom_type_ref'))

    x_tinker_number_of_defined_pair_interactions = Quantity(
        type=np.dtype(np.int32),
        shape=[],
        description='''
        Number of defined pair interactions (L-J pairs).
        ''',
        a_legacy=LegacyDefinition(name='x_tinker_number_of_defined_pair_interactions'))

    x_tinker_pair_interaction_atom_type_ref = Quantity(
        type=common.section_atom_type,
        shape=['x_tinker_number_of_defined_pair_interactions', 'number_of_atoms_per_interaction'],
        description='''
        Reference to the atom type for pair interactions.
        ''',
        a_legacy=LegacyDefinition(name='x_tinker_pair_interaction_atom_type_ref'))

    x_tinker_pair_interaction_parameters = Quantity(
        type=np.dtype(np.float64),
        shape=['x_tinker_number_of_defined_pair_interactions', 2],
        description='''
        Pair interactions parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_tinker_pair_interaction_parameters'))


class section_molecule_interaction(common.section_molecule_interaction):

    m_def = Section(validate=False, extends_base_section=True, a_legacy=LegacyDefinition(name='section_molecule_interaction'))

    x_tinker_molecule_interaction_atom_to_atom_type_ref = Quantity(
        type=common.section_atom_type,
        shape=['number_of_atoms_per_interaction'],
        description='''
        Reference to the atom type of each molecule interaction atoms.
        ''',
        a_legacy=LegacyDefinition(name='x_tinker_molecule_interaction_atom_to_atom_type_ref'))

    x_tinker_number_of_defined_molecule_pair_interactions = Quantity(
        type=np.dtype(np.int32),
        shape=[],
        description='''
        Number of defined pair interactions within a molecule (L-J pairs).
        ''',
        a_legacy=LegacyDefinition(name='x_tinker_number_of_defined_molecule_pair_interactions'))

    x_tinker_pair_molecule_interaction_parameters = Quantity(
        type=np.dtype(np.float64),
        shape=['number_of_defined_molecule_pair_interactions', 2],
        description='''
        Molecule pair interactions parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_tinker_pair_molecule_interaction_parameters'))

    x_tinker_pair_molecule_interaction_to_atom_type_ref = Quantity(
        type=common.section_atom_type,
        shape=['x_tinker_number_of_defined_pair_interactions', 'number_of_atoms_per_interaction'],
        description='''
        Reference to the atom type for pair interactions within a molecule.
        ''',
        a_legacy=LegacyDefinition(name='x_tinker_pair_molecule_interaction_to_atom_type_ref'))


class section_run(public.section_run):

    m_def = Section(validate=False, extends_base_section=True, a_legacy=LegacyDefinition(name='section_run'))

    x_tinker_program_version_date = Quantity(
        type=str,
        shape=[],
        description='''
        Program version date.
        ''',
        a_legacy=LegacyDefinition(name='x_tinker_program_version_date'))

    x_tinker_parallel_task_nr = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        description='''
        Program task no.
        ''',
        a_legacy=LegacyDefinition(name='x_tinker_parallel_task_nr'))

    x_tinker_build_osarch = Quantity(
        type=str,
        shape=[],
        description='''
        Program Build OS/ARCH
        ''',
        a_legacy=LegacyDefinition(name='x_tinker_build_osarch'))

    x_tinker_output_created_by_user = Quantity(
        type=str,
        shape=[],
        description='''
        Output file creator
        ''',
        a_legacy=LegacyDefinition(name='x_tinker_output_created_by_user'))

    x_tinker_most_severe_warning_level = Quantity(
        type=str,
        shape=[],
        description='''
        Highest tinker warning level in the run.
        ''',
        a_legacy=LegacyDefinition(name='x_tinker_most_severe_warning_level'))

    x_tinker_program_build_date = Quantity(
        type=str,
        shape=[],
        description='''
        Program Build date
        ''',
        a_legacy=LegacyDefinition(name='x_tinker_program_build_date'))

    x_tinker_program_citation = Quantity(
        type=str,
        shape=[],
        description='''
        Program citations
        ''',
        a_legacy=LegacyDefinition(name='x_tinker_program_citation'))

    x_tinker_program_copyright = Quantity(
        type=str,
        shape=[],
        description='''
        Program copyright
        ''',
        a_legacy=LegacyDefinition(name='x_tinker_program_copyright'))

    x_tinker_number_of_tasks = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        description='''
        Number of tasks in parallel program (MPI).
        ''',
        a_legacy=LegacyDefinition(name='x_tinker_number_of_tasks'))

    x_tinker_program_module_version = Quantity(
        type=str,
        shape=[],
        description='''
        tinker program module version.
        ''',
        a_legacy=LegacyDefinition(name='x_tinker_program_module_version'))

    x_tinker_program_license = Quantity(
        type=str,
        shape=[],
        description='''
        tinker program license.
        ''',
        a_legacy=LegacyDefinition(name='x_tinker_program_license'))

    x_tinker_xlo_xhi = Quantity(
        type=str,
        shape=[],
        description='''
        test
        ''',
        a_legacy=LegacyDefinition(name='x_tinker_xlo_xhi'))

    x_tinker_data_file_store = Quantity(
        type=str,
        shape=[],
        description='''
        Filename of data file
        ''',
        a_legacy=LegacyDefinition(name='x_tinker_data_file_store'))

    x_tinker_program_working_path = Quantity(
        type=str,
        shape=[],
        description='''
        tmp
        ''',
        a_legacy=LegacyDefinition(name='x_tinker_program_working_path'))

    x_tinker_program_execution_host = Quantity(
        type=str,
        shape=[],
        description='''
        tmp
        ''',
        a_legacy=LegacyDefinition(name='x_tinker_program_execution_host'))

    x_tinker_program_execution_path = Quantity(
        type=str,
        shape=[],
        description='''
        tmp
        ''',
        a_legacy=LegacyDefinition(name='x_tinker_program_execution_path'))

    x_tinker_program_module = Quantity(
        type=str,
        shape=[],
        description='''
        tmp
        ''',
        a_legacy=LegacyDefinition(name='x_tinker_program_module'))

    x_tinker_program_execution_date = Quantity(
        type=str,
        shape=[],
        description='''
        tmp
        ''',
        a_legacy=LegacyDefinition(name='x_tinker_program_execution_date'))

    x_tinker_program_execution_time = Quantity(
        type=str,
        shape=[],
        description='''
        tmp
        ''',
        a_legacy=LegacyDefinition(name='x_tinker_program_execution_time'))

    x_tinker_mdin_header = Quantity(
        type=str,
        shape=[],
        description='''
        tmp
        ''',
        a_legacy=LegacyDefinition(name='x_tinker_mdin_header'))

    x_tinker_mdin_wt = Quantity(
        type=str,
        shape=[],
        description='''
        tmp
        ''',
        a_legacy=LegacyDefinition(name='x_tinker_mdin_wt'))

    x_tinker_section_control_parameters = SubSection(
        sub_section=SectionProxy('x_tinker_section_control_parameters'),
        repeats=True,
        a_legacy=LegacyDefinition(name='x_tinker_section_control_parameters'))


class section_topology(common.section_topology):

    m_def = Section(validate=False, extends_base_section=True, a_legacy=LegacyDefinition(name='section_topology'))

    x_tinker_input_units_store = Quantity(
        type=str,
        shape=[],
        description='''
        It determines the units of all quantities specified in the input script and data
        file, as well as quantities output to the screen, log file, and dump files.
        ''',
        a_legacy=LegacyDefinition(name='x_tinker_input_units_store'))

    x_tinker_data_bond_types_store = Quantity(
        type=np.dtype(np.int32),
        shape=[],
        description='''
        store temporarly
        ''',
        a_legacy=LegacyDefinition(name='x_tinker_data_bond_types_store'))

    x_tinker_data_bond_count_store = Quantity(
        type=np.dtype(np.int32),
        shape=[],
        description='''
        store temporarly
        ''',
        a_legacy=LegacyDefinition(name='x_tinker_data_bond_count_store'))

    x_tinker_data_angle_count_store = Quantity(
        type=np.dtype(np.int32),
        shape=[],
        description='''
        store temporarly
        ''',
        a_legacy=LegacyDefinition(name='x_tinker_data_angle_count_store'))

    x_tinker_data_atom_types_store = Quantity(
        type=np.dtype(np.int32),
        shape=[],
        description='''
        store temporarly
        ''',
        a_legacy=LegacyDefinition(name='x_tinker_data_atom_types_store'))

    x_tinker_data_dihedral_count_store = Quantity(
        type=np.dtype(np.int32),
        shape=[],
        description='''
        store temporarly
        ''',
        a_legacy=LegacyDefinition(name='x_tinker_data_dihedral_count_store'))

    x_tinker_data_angles_store = Quantity(
        type=str,
        shape=[],
        description='''
        store temporarly
        ''',
        a_legacy=LegacyDefinition(name='x_tinker_data_angles_store'))

    x_tinker_data_angle_list_store = Quantity(
        type=str,
        shape=[],
        description='''
        tmp
        ''',
        a_legacy=LegacyDefinition(name='x_tinker_data_angle_list_store'))

    x_tinker_data_bond_list_store = Quantity(
        type=str,
        shape=[],
        description='''
        tmp
        ''',
        a_legacy=LegacyDefinition(name='x_tinker_data_bond_list_store'))

    x_tinker_data_dihedral_list_store = Quantity(
        type=str,
        shape=[],
        description='''
        tmp
        ''',
        a_legacy=LegacyDefinition(name='x_tinker_data_dihedral_list_store'))

    x_tinker_data_dihedral_coeff_list_store = Quantity(
        type=str,
        shape=[],
        description='''
        tmp
        ''',
        a_legacy=LegacyDefinition(name='x_tinker_data_dihedral_coeff_list_store'))

    x_tinker_masses_store = Quantity(
        type=str,
        shape=[],
        description='''
        tmp
        ''',
        a_legacy=LegacyDefinition(name='x_tinker_masses_store'))

    x_tinker_data_topo_list_store = Quantity(
        type=str,
        shape=[],
        description='''
        tmp
        ''',
        a_legacy=LegacyDefinition(name='x_tinker_data_topo_list_store'))

    x_tinker_section_atom_to_atom_type_ref = SubSection(
        sub_section=SectionProxy('x_tinker_section_atom_to_atom_type_ref'),
        repeats=True,
        a_legacy=LegacyDefinition(name='x_tinker_section_atom_to_atom_type_ref'))


class section_frame_sequence(public.section_frame_sequence):

    m_def = Section(validate=False, extends_base_section=True, a_legacy=LegacyDefinition(name='section_frame_sequence'))

    x_tinker_number_of_volumes_in_sequence = Quantity(
        type=int,
        shape=[],
        description='''
        Gives the number of volumes in this sequence of frames, see
        x_tinker_frame_sequence_volume.
        ''',
        a_legacy=LegacyDefinition(name='x_tinker_number_of_volumes_in_sequence'))

    x_tinker_number_of_density_in_sequence = Quantity(
        type=int,
        shape=[],
        description='''
        Gives the number of densities in this sequence of frames, see
        x_tinker_frame_sequence_density.
        ''',
        a_legacy=LegacyDefinition(name='x_tinker_number_of_density_in_sequence'))

    x_tinker_number_of_bond_energies_in_sequence = Quantity(
        type=int,
        shape=[],
        description='''
        Gives the number of bond_energies in this sequence of frames, see
        x_tinker_frame_sequence_bond_energy.
        ''',
        a_legacy=LegacyDefinition(name='x_tinker_number_of_bond_energies_in_sequence'))

    x_tinker_number_of_virial_energies_in_sequence = Quantity(
        type=int,
        shape=[],
        description='''
        Gives the number of bond_energies in this sequence of frames, see
        x_tinker_frame_sequence_virial_energy.
        ''',
        a_legacy=LegacyDefinition(name='x_tinker_number_of_virial_energies_in_sequence'))

    x_tinker_number_of_angle_energies_in_sequence = Quantity(
        type=int,
        shape=[],
        description='''
        Gives the number of angle_energies in this sequence of frames, see
        x_tinker_frame_sequence_angle_energy.
        ''',
        a_legacy=LegacyDefinition(name='x_tinker_number_of_angle_energies_in_sequence'))

    x_tinker_number_of_proper_dihedral_energies_in_sequence = Quantity(
        type=int,
        shape=[],
        description='''
        Gives the number of proper_dihedral_energies in this sequence of frames, see
        x_tinker_frame_sequence_proper_dihedral_energy.
        ''',
        a_legacy=LegacyDefinition(name='x_tinker_number_of_proper_dihedral_energies_in_sequence'))

    x_tinker_number_of_improper_dihedral_energies_in_sequence = Quantity(
        type=int,
        shape=[],
        description='''
        Gives the number of improper_dihedral_energies in this sequence of frames, see
        x_tinker_frame_sequence_improper_dihedral_energy.
        ''',
        a_legacy=LegacyDefinition(name='x_tinker_number_of_improper_dihedral_energies_in_sequence'))

    x_tinker_number_of_cross_dihedral_energies_in_sequence = Quantity(
        type=int,
        shape=[],
        description='''
        Gives the number of cross_dihedral_energies in this sequence of frames, see
        x_tinker_frame_sequence_cross_dihedral_energy.
        ''',
        a_legacy=LegacyDefinition(name='x_tinker_number_of_cross_dihedral_energies_in_sequence'))

    x_tinker_number_of_vdw_energies_in_sequence = Quantity(
        type=int,
        shape=[],
        description='''
        Gives the number of vdw_energies in this sequence of frames, see
        x_tinker_frame_sequence_vdw_energy.
        ''',
        a_legacy=LegacyDefinition(name='x_tinker_number_of_vdw_energies_in_sequence'))

    x_tinker_number_of_boundary_energies_in_sequence = Quantity(
        type=int,
        shape=[],
        description='''
        Gives the number of boundary_energies in this sequence of frames, see
        x_tinker_frame_sequence_boundary_energy.
        ''',
        a_legacy=LegacyDefinition(name='x_tinker_number_of_boundary_energies_in_sequence'))

    x_tinker_number_of_electrostatic_energies_in_sequence = Quantity(
        type=int,
        shape=[],
        description='''
        Gives the number of electrostatic_energies in this sequence of frames, see
        x_tinker_frame_sequence_electrostatic_energy.
        ''',
        a_legacy=LegacyDefinition(name='x_tinker_number_of_electrostatic_energies_in_sequence'))

    x_tinker_number_of_total_energies_in_sequence = Quantity(
        type=int,
        shape=[],
        description='''
        Gives the number of total_energies in this sequence of frames, see
        x_tinker_frame_sequence_total_energy.
        ''',
        a_legacy=LegacyDefinition(name='x_tinker_number_of_total_energies_in_sequence'))

    x_tinker_number_of_total_kinetic_energies_in_sequence = Quantity(
        type=int,
        shape=[],
        description='''
        Gives the number of total_kinetic_energies in this sequence of frames, see
        x_tinker_frame_sequence_total_kinetic_energy_frames.
        ''',
        a_legacy=LegacyDefinition(name='x_tinker_number_of_total_kinetic_energies_in_sequence'))

    x_tinker_number_of_misc_energies_in_sequence = Quantity(
        type=int,
        shape=[],
        description='''
        Gives the number of misc_energies in this sequence of frames, see
        x_tinker_frame_sequence_misc_energy.
        ''',
        a_legacy=LegacyDefinition(name='x_tinker_number_of_misc_energies_in_sequence'))

    x_tinker_frame_sequence_density_frames = Quantity(
        type=np.dtype(np.int32),
        shape=['x_tinker_number_of_density_in_sequence'],
        description='''
        Array containing the strictly increasing indices of the frames the
        x_tinker_frame_sequence_density values refers to. If not given it defaults to the
        trivial mapping 0,1,...
        ''',
        a_legacy=LegacyDefinition(name='x_tinker_frame_sequence_density_frames'))

    x_tinker_frame_sequence_density = Quantity(
        type=np.dtype(np.float64),
        shape=['x_tinker_number_of_density_in_sequence'],
        description='''
        Array containing the values of the density along this sequence of frames (i.e., a
        trajectory, a frame is one section_single_configuration_calculation). If not all
        frames have a value the indices of the frames that have a value are stored in
        frame_sequence_density_frames.
        ''',
        a_legacy=LegacyDefinition(name='x_tinker_frame_sequence_density'))

    x_tinker_frame_sequence_cross_dihedral_energy_frames = Quantity(
        type=np.dtype(np.int32),
        shape=['x_tinker_number_of_cross_dihedral_energy_in_sequence'],
        description='''
        Array containing the strictly increasing indices of the frames the
        x_tinker_frame_sequence_cross_dihedral_energy values refers to. If not given it
        defaults to the trivial mapping 0,1,...
        ''',
        a_legacy=LegacyDefinition(name='x_tinker_frame_sequence_cross_dihedral_energy_frames'))

    x_tinker_frame_sequence_cross_dihedral_energy = Quantity(
        type=np.dtype(np.float64),
        shape=['x_tinker_number_of_cross_dihedral_energy_in_sequence'],
        description='''
        Array containing the values of the cross_dihedral_energy along this sequence of
        frames (i.e., a trajectory, a frame is one
        section_single_configuration_calculation). If not all frames have a value the
        indices of the frames that have a value are stored in
        frame_sequence_cross_dihedral_energy_frames.
        ''',
        a_legacy=LegacyDefinition(name='x_tinker_frame_sequence_cross_dihedral_energy'))

    x_tinker_frame_sequence_improper_dihedral_energy_frames = Quantity(
        type=np.dtype(np.int32),
        shape=['x_tinker_number_of_improper_dihedral_energy_in_sequence'],
        description='''
        Array containing the strictly increasing indices of the frames the
        x_tinker_frame_sequence_improper_dihedral_energy values refers to. If not given it
        defaults to the trivial mapping 0,1,...
        ''',
        a_legacy=LegacyDefinition(name='x_tinker_frame_sequence_improper_dihedral_energy_frames'))

    x_tinker_frame_sequence_improper_dihedral_energy = Quantity(
        type=np.dtype(np.float64),
        shape=['x_tinker_number_of_improper_dihedral_energy_in_sequence'],
        description='''
        Array containing the values of the improper_dihedral_energy along this sequence of
        frames (i.e., a trajectory, a frame is one
        section_single_configuration_calculation). If not all frames have a value the
        indices of the frames that have a value are stored in
        frame_sequence_improper_dihedral_energy_frames.
        ''',
        a_legacy=LegacyDefinition(name='x_tinker_frame_sequence_improper_dihedral_energy'))

    x_tinker_frame_sequence_proper_dihedral_energy_frames = Quantity(
        type=np.dtype(np.int32),
        shape=['x_tinker_number_of_proper_dihedral_energy_in_sequence'],
        description='''
        Array containing the strictly increasing indices of the frames the
        x_tinker_frame_sequence_proper_dihedral_energy values refers to. If not given it
        defaults to the trivial mapping 0,1,...
        ''',
        a_legacy=LegacyDefinition(name='x_tinker_frame_sequence_proper_dihedral_energy_frames'))

    x_tinker_frame_sequence_proper_dihedral_energy = Quantity(
        type=np.dtype(np.float64),
        shape=['x_tinker_number_of_proper_dihedral_energy_in_sequence'],
        description='''
        Array containing the values of the proper_dihedral_energy along this sequence of
        frames (i.e., a trajectory, a frame is one
        section_single_configuration_calculation). If not all frames have a value the
        indices of the frames that have a value are stored in
        frame_sequence_proper_dihedral_energy_frames.
        ''',
        a_legacy=LegacyDefinition(name='x_tinker_frame_sequence_proper_dihedral_energy'))

    x_tinker_frame_sequence_bond_energy_frames = Quantity(
        type=np.dtype(np.int32),
        shape=['x_tinker_number_of_bond_energies_in_sequence'],
        description='''
        Array containing the strictly increasing indices of the frames the
        x_tinker_frame_sequence_bond_energy values refers to. If not given it defaults to
        the trivial mapping 0,1,...
        ''',
        a_legacy=LegacyDefinition(name='x_tinker_frame_sequence_bond_energy_frames'))

    x_tinker_frame_sequence_virial_energy_frames = Quantity(
        type=np.dtype(np.int32),
        shape=['x_tinker_number_of_virial_energies_in_sequence'],
        description='''
        Array containing the strictly increasing indices of the frames the
        x_tinker_frame_sequence_virial_energy values refers to. If not given it defaults
        to the trivial mapping 0,1,...
        ''',
        a_legacy=LegacyDefinition(name='x_tinker_frame_sequence_virial_energy_frames'))

    x_tinker_frame_sequence_bond_energy = Quantity(
        type=np.dtype(np.float64),
        shape=['x_tinker_number_of_bond_energies_in_sequence'],
        description='''
        Array containing the values of the bond_energy along this sequence of frames
        (i.e., a trajectory, a frame is one section_single_configuration_calculation). If
        not all frames have a value the indices of the frames that have a value are stored
        in frame_sequence_bond_energy_frames.
        ''',
        a_legacy=LegacyDefinition(name='x_tinker_frame_sequence_bond_energy'))

    x_tinker_frame_sequence_virial_energy = Quantity(
        type=np.dtype(np.float64),
        shape=['x_tinker_number_of_virial_energies_in_sequence'],
        description='''
        Array containing the values of the virial_energy along this sequence of frames
        (i.e., a trajectory, a frame is one section_single_configuration_calculation). If
        not all frames have a value the indices of the frames that have a value are stored
        in frame_sequence_virial_energy_frames.
        ''',
        a_legacy=LegacyDefinition(name='x_tinker_frame_sequence_virial_energy'))

    x_tinker_frame_sequence_boundary_frames = Quantity(
        type=np.dtype(np.int32),
        shape=['x_tinker_number_of_boundary_energies_in_sequence'],
        description='''
        Array containing the strictly increasing indices of the frames the
        x_tinker_frame_sequence_boundary values refers to. If not given it defaults to the
        trivial mapping 0,1,...
        ''',
        a_legacy=LegacyDefinition(name='x_tinker_frame_sequence_boundary_frames'))

    x_tinker_frame_sequence_boundary = Quantity(
        type=np.dtype(np.float64),
        shape=['x_tinker_number_of_boundary_energies_in_sequence'],
        description='''
        Array containing the values of the boundary along this sequence of frames (i.e., a
        trajectory, a frame is one section_single_configuration_calculation). If not all
        frames have a value the indices of the frames that have a value are stored in
        frame_sequence_boundary_frames.
        ''',
        a_legacy=LegacyDefinition(name='x_tinker_frame_sequence_boundary'))

    x_tinker_frame_sequence_angle_energy_frames = Quantity(
        type=np.dtype(np.int32),
        shape=['x_tinker_number_of_angle_energies_in_sequence'],
        description='''
        Array containing the strictly increasing indices of the frames the
        x_tinker_frame_sequence_angle_energy values refers to. If not given it defaults to
        the trivial mapping 0,1,...
        ''',
        a_legacy=LegacyDefinition(name='x_tinker_frame_sequence_angle_energy_frames'))

    x_tinker_frame_sequence_angle_energy = Quantity(
        type=np.dtype(np.float64),
        shape=['x_tinker_number_of_angle_energies_in_sequence'],
        description='''
        Array containing the values of the angle_energy along this sequence of frames
        (i.e., a trajectory, a frame is one section_single_configuration_calculation). If
        not all frames have a value the indices of the frames that have a value are stored
        in frame_sequence_angle_energy_frames.
        ''',
        a_legacy=LegacyDefinition(name='x_tinker_frame_sequence_angle_energy'))

    x_tinker_frame_sequence_vdw_energy_frames = Quantity(
        type=np.dtype(np.int32),
        shape=['x_tinker_number_of_vdw_energies_in_sequence'],
        description='''
        Array containing the strictly increasing indices of the frames the
        x_tinker_frame_sequence_vdw_energy values refers to. If not given it defaults to
        the trivial mapping 0,1,...
        ''',
        a_legacy=LegacyDefinition(name='x_tinker_frame_sequence_vdw_energy_frames'))

    x_tinker_frame_sequence_vdw_energy = Quantity(
        type=np.dtype(np.float64),
        shape=['x_tinker_number_of_vdw_energies_in_sequence'],
        description='''
        Array containing the values of the vdw_energy along this sequence of frames (i.e.,
        a trajectory, a frame is one section_single_configuration_calculation). If not all
        frames have a value the indices of the frames that have a value are stored in
        frame_sequence_vdw_energy_frames.
        ''',
        a_legacy=LegacyDefinition(name='x_tinker_frame_sequence_vdw_energy'))

    x_tinker_frame_sequence_electrostatic_energy_frames = Quantity(
        type=np.dtype(np.int32),
        shape=['x_tinker_number_of_electrostatic_energies_in_sequence'],
        description='''
        Array containing the strictly increasing indices of the frames the
        x_tinker_frame_sequence_electrostatic_energy values refers to. If not given it
        defaults to the trivial mapping 0,1,...
        ''',
        a_legacy=LegacyDefinition(name='x_tinker_frame_sequence_electrostatic_energy_frames'))

    x_tinker_frame_sequence_electrostatic_energy = Quantity(
        type=np.dtype(np.float64),
        shape=['x_tinker_number_of_electrostatic_energies_in_sequence'],
        description='''
        Array containing the values of the electrostatic_energy along this sequence of
        frames (i.e., a trajectory, a frame is one
        section_single_configuration_calculation). If not all frames have a value the
        indices of the frames that have a value are stored in
        frame_sequence_electrostatic_energy_frames.
        ''',
        a_legacy=LegacyDefinition(name='x_tinker_frame_sequence_electrostatic_energy'))

    x_tinker_frame_sequence_total_energy_frames = Quantity(
        type=np.dtype(np.int32),
        shape=['x_tinker_number_of_total_energies_in_sequence'],
        description='''
        Array containing the strictly increasing indices of the frames the
        x_tinker_frame_sequence_total_energy values refers to. If not given it defaults to
        the trivial mapping 0,1,...
        ''',
        a_legacy=LegacyDefinition(name='x_tinker_frame_sequence_total_energy_frames'))

    x_tinker_frame_sequence_total_energy = Quantity(
        type=np.dtype(np.float64),
        shape=['x_tinker_number_of_total_energies_in_sequence'],
        description='''
        Array containing the values of the total_energy along this sequence of frames
        (i.e., a trajectory, a frame is one section_single_configuration_calculation). If
        not all frames have a value the indices of the frames that have a value are stored
        in frame_sequence_total_energy_frames.
        ''',
        a_legacy=LegacyDefinition(name='x_tinker_frame_sequence_total_energy'))

    x_tinker_frame_sequence_total_kinetic_energy_frames = Quantity(
        type=np.dtype(np.int32),
        shape=['x_tinker_number_of_total_kinetic_energies_in_sequence'],
        description='''
        Array containing the strictly increasing indices of the frames the
        x_tinker_frame_sequence_total_kinetic_energy values refers to. If not given it
        defaults to the trivial mapping 0,1,...
        ''',
        a_legacy=LegacyDefinition(name='x_tinker_frame_sequence_total_kinetic_energy_frames'))

    x_tinker_frame_sequence_total_kinetic_energy = Quantity(
        type=np.dtype(np.float64),
        shape=['x_tinker_number_of_total_kinetic_energies_in_sequence'],
        description='''
        Array containing the values of the total_kinetic_energy along this sequence of
        frames (i.e., a trajectory, a frame is one
        section_single_configuration_calculation). If not all frames have a value the
        indices of the frames that have a value are stored in
        frame_sequence_total_kinetic_energy_frames.
        ''',
        a_legacy=LegacyDefinition(name='x_tinker_frame_sequence_total_kinetic_energy'))

    x_tinker_frame_sequence_misc_energy_frames = Quantity(
        type=np.dtype(np.int32),
        shape=['x_tinker_number_of_misc_energies_in_sequence'],
        description='''
        Array containing the strictly increasing indices of the frames the
        x_tinker_frame_sequence_misc_energy values refers to. If not given it defaults to
        the trivial mapping 0,1,...
        ''',
        a_legacy=LegacyDefinition(name='x_tinker_frame_sequence_misc_energy_frames'))

    x_tinker_frame_sequence_misc_energy = Quantity(
        type=np.dtype(np.float64),
        shape=['x_tinker_number_of_misc_energies_in_sequence'],
        description='''
        Array containing the values of the misc_energy along this sequence of frames
        (i.e., a trajectory, a frame is one section_single_configuration_calculation). If
        not all frames have a value the indices of the frames that have a value are stored
        in frame_sequence_misc_energy_frames.
        ''',
        a_legacy=LegacyDefinition(name='x_tinker_frame_sequence_misc_energy'))

    x_tinker_frame_sequence_volume_frames = Quantity(
        type=np.dtype(np.int32),
        shape=['x_tinker_number_of_volumes_in_sequence'],
        description='''
        Array containing the strictly increasing indices of the frames the
        x_tinker_frame_sequence_volume values refers to. If not given it defaults to the
        trivial mapping 0,1,...
        ''',
        a_legacy=LegacyDefinition(name='x_tinker_frame_sequence_volume_frames'))

    x_tinker_frame_sequence_volume = Quantity(
        type=np.dtype(np.float64),
        shape=['x_tinker_number_of_volumes_in_sequence'],
        description='''
        Array containing the values of the volume along this sequence of frames (i.e., a
        trajectory, a frame is one section_single_configuration_calculation). If not all
        frames have a value the indices of the frames that have a value are stored in
        frame_sequence_volume_frames.
        ''',
        a_legacy=LegacyDefinition(name='x_tinker_frame_sequence_volume'))


class section_single_configuration_calculation(public.section_single_configuration_calculation):

    m_def = Section(validate=False, extends_base_section=True, a_legacy=LegacyDefinition(name='section_single_configuration_calculation'))

    x_tinker_section_single_configuration_calculation = SubSection(
        sub_section=SectionProxy('x_tinker_section_single_configuration_calculation'),
        repeats=True,
        a_legacy=LegacyDefinition(name='x_tinker_section_single_configuration_calculation'))


m_package.__init_metainfo__()
