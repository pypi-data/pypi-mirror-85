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
    name='namd_nomadmetainfo_json',
    description='None',
    a_legacy=LegacyDefinition(name='namd.nomadmetainfo.json'))


class x_namd_mdin_input_output_files(MCategory):
    '''
    Parameters of mdin belonging to x_namd_section_control_parameters.
    '''

    m_def = Category(
        a_legacy=LegacyDefinition(name='x_namd_mdin_input_output_files'))


class x_namd_mdin_control_parameters(MCategory):
    '''
    Parameters of mdin belonging to x_namd_section_control_parameters.
    '''

    m_def = Category(
        a_legacy=LegacyDefinition(name='x_namd_mdin_control_parameters'))


class x_namd_mdin_method(MCategory):
    '''
    Parameters of mdin belonging to section method.
    '''

    m_def = Category(
        a_legacy=LegacyDefinition(name='x_namd_mdin_method'))


class x_namd_mdout_single_configuration_calculation(MCategory):
    '''
    Parameters of mdout belonging to section_single_configuration_calculation.
    '''

    m_def = Category(
        a_legacy=LegacyDefinition(name='x_namd_mdout_single_configuration_calculation'))


class x_namd_mdout_method(MCategory):
    '''
    Parameters of mdin belonging to section method.
    '''

    m_def = Category(
        a_legacy=LegacyDefinition(name='x_namd_mdout_method'))


class x_namd_mdout_run(MCategory):
    '''
    Parameters of mdin belonging to settings run.
    '''

    m_def = Category(
        categories=[public.settings_run],
        a_legacy=LegacyDefinition(name='x_namd_mdout_run'))


class x_namd_mdin_run(MCategory):
    '''
    Parameters of mdin belonging to settings run.
    '''

    m_def = Category(
        categories=[public.settings_run],
        a_legacy=LegacyDefinition(name='x_namd_mdin_run'))


class x_namd_section_input_output_files(MSection):
    '''
    Section to store input and output file names
    '''

    m_def = Section(validate=False, a_legacy=LegacyDefinition(name='x_namd_section_input_output_files'))

    x_namd_inout_file_structure = Quantity(
        type=str,
        shape=[],
        description='''
        NAMD input topology file.
        ''',
        a_legacy=LegacyDefinition(name='x_namd_inout_file_structure'))

    x_namd_inout_file_traj_coord = Quantity(
        type=str,
        shape=[],
        description='''
        NAMD output trajectory file.
        ''',
        a_legacy=LegacyDefinition(name='x_namd_inout_file_traj_coord'))

    x_namd_inout_file_traj_vel = Quantity(
        type=str,
        shape=[],
        description='''
        NAMD output file for velocities in the trajectory.
        ''',
        a_legacy=LegacyDefinition(name='x_namd_inout_file_traj_vel'))

    x_namd_inout_file_traj_force = Quantity(
        type=str,
        shape=[],
        description='''
        NAMD output file for forces in the trajectory.
        ''',
        a_legacy=LegacyDefinition(name='x_namd_inout_file_traj_force'))

    x_namd_inout_file_output_coord = Quantity(
        type=str,
        shape=[],
        description='''
        NAMD output coordinates file.
        ''',
        a_legacy=LegacyDefinition(name='x_namd_inout_file_output_coord'))

    x_namd_inout_file_output_vel = Quantity(
        type=str,
        shape=[],
        description='''
        NAMD output velocities file.
        ''',
        a_legacy=LegacyDefinition(name='x_namd_inout_file_output_vel'))

    x_namd_inout_file_output_force = Quantity(
        type=str,
        shape=[],
        description='''
        NAMD output forces file.
        ''',
        a_legacy=LegacyDefinition(name='x_namd_inout_file_output_force'))

    x_namd_inout_file_input_coord = Quantity(
        type=str,
        shape=[],
        description='''
        NAMD input coordinates file.
        ''',
        a_legacy=LegacyDefinition(name='x_namd_inout_file_input_coord'))

    x_namd_inout_file_input_vel = Quantity(
        type=str,
        shape=[],
        description='''
        NAMD input velocities file.
        ''',
        a_legacy=LegacyDefinition(name='x_namd_inout_file_input_vel'))

    x_namd_inout_file_restart_coord = Quantity(
        type=str,
        shape=[],
        description='''
        NAMD restart coordinates file.
        ''',
        a_legacy=LegacyDefinition(name='x_namd_inout_file_restart_coord'))

    x_namd_inout_file_restart_vel = Quantity(
        type=str,
        shape=[],
        description='''
        NAMD restart velocities file.
        ''',
        a_legacy=LegacyDefinition(name='x_namd_inout_file_restart_vel'))

    x_namd_inout_file_fftw_datafile = Quantity(
        type=str,
        shape=[],
        description='''
        NAMD FFTW data file.
        ''',
        a_legacy=LegacyDefinition(name='x_namd_inout_file_fftw_datafile'))

    x_namd_inout_file_mdlog = Quantity(
        type=str,
        shape=[],
        description='''
        NAMD MD output log file.
        ''',
        a_legacy=LegacyDefinition(name='x_namd_inout_file_mdlog'))


class x_namd_section_control_parameters(MSection):
    '''
    Section to store the input and output control parameters
    '''

    m_def = Section(validate=False, a_legacy=LegacyDefinition(name='x_namd_section_control_parameters'))

    x_namd_inout_control_timestep = Quantity(
        type=str,
        shape=[],
        description='''
        NAMD running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_namd_inout_control_timestep'))

    x_namd_inout_control_number_of_steps = Quantity(
        type=str,
        shape=[],
        description='''
        NAMD running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_namd_inout_control_number_of_steps'))

    x_namd_inout_control_steps_per_cycle = Quantity(
        type=str,
        shape=[],
        description='''
        NAMD running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_namd_inout_control_steps_per_cycle'))

    x_namd_inout_control_periodic_cell_basis_1 = Quantity(
        type=str,
        shape=[],
        description='''
        NAMD running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_namd_inout_control_periodic_cell_basis_1'))

    x_namd_inout_control_periodic_cell_basis_2 = Quantity(
        type=str,
        shape=[],
        description='''
        NAMD running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_namd_inout_control_periodic_cell_basis_2'))

    x_namd_inout_control_periodic_cell_basis_3 = Quantity(
        type=str,
        shape=[],
        description='''
        NAMD running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_namd_inout_control_periodic_cell_basis_3'))

    x_namd_inout_control_periodic_cell_center = Quantity(
        type=str,
        shape=[],
        description='''
        NAMD running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_namd_inout_control_periodic_cell_center'))

    x_namd_inout_control_load_balancer = Quantity(
        type=str,
        shape=[],
        description='''
        NAMD running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_namd_inout_control_load_balancer'))

    x_namd_inout_control_load_balancing_strategy = Quantity(
        type=str,
        shape=[],
        description='''
        NAMD running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_namd_inout_control_load_balancing_strategy'))

    x_namd_inout_control_ldb_period = Quantity(
        type=str,
        shape=[],
        description='''
        NAMD running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_namd_inout_control_ldb_period'))

    x_namd_inout_control_first_ldb_timestep = Quantity(
        type=str,
        shape=[],
        description='''
        NAMD running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_namd_inout_control_first_ldb_timestep'))

    x_namd_inout_control_last_ldb_timestep = Quantity(
        type=str,
        shape=[],
        description='''
        NAMD running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_namd_inout_control_last_ldb_timestep'))

    x_namd_inout_control_ldb_background_scaling = Quantity(
        type=str,
        shape=[],
        description='''
        NAMD running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_namd_inout_control_ldb_background_scaling'))

    x_namd_inout_control_hom_background_scaling = Quantity(
        type=str,
        shape=[],
        description='''
        NAMD running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_namd_inout_control_hom_background_scaling'))

    x_namd_inout_control_pme_background_scaling = Quantity(
        type=str,
        shape=[],
        description='''
        NAMD running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_namd_inout_control_pme_background_scaling'))

    x_namd_inout_control_min_atoms_per_patch = Quantity(
        type=str,
        shape=[],
        description='''
        NAMD running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_namd_inout_control_min_atoms_per_patch'))

    x_namd_inout_control_initial_temperature = Quantity(
        type=str,
        shape=[],
        description='''
        NAMD running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_namd_inout_control_initial_temperature'))

    x_namd_inout_control_center_of_mass_moving_initially = Quantity(
        type=str,
        shape=[],
        description='''
        NAMD running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_namd_inout_control_center_of_mass_moving_initially'))

    x_namd_inout_control_dielectric = Quantity(
        type=str,
        shape=[],
        description='''
        NAMD running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_namd_inout_control_dielectric'))

    x_namd_inout_control_excluded_species_or_groups = Quantity(
        type=str,
        shape=[],
        description='''
        NAMD running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_namd_inout_control_excluded_species_or_groups'))

    x_namd_inout_control_1_4_electrostatics_scale = Quantity(
        type=str,
        shape=[],
        description='''
        NAMD running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_namd_inout_control_1_4_electrostatics_scale'))

    x_namd_inout_control_traj_dcd_filename = Quantity(
        type=str,
        shape=[],
        description='''
        NAMD running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_namd_inout_control_traj_dcd_filename'))

    x_namd_inout_control_traj_dcd_frequency = Quantity(
        type=str,
        shape=[],
        description='''
        NAMD running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_namd_inout_control_traj_dcd_frequency'))

    x_namd_inout_control_traj_dcd_first_step = Quantity(
        type=str,
        shape=[],
        description='''
        NAMD running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_namd_inout_control_traj_dcd_first_step'))

    x_namd_inout_control_velocity_dcd_filename = Quantity(
        type=str,
        shape=[],
        description='''
        NAMD running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_namd_inout_control_velocity_dcd_filename'))

    x_namd_inout_control_velocity_dcd_frequency = Quantity(
        type=str,
        shape=[],
        description='''
        NAMD running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_namd_inout_control_velocity_dcd_frequency'))

    x_namd_inout_control_velocity_dcd_first_step = Quantity(
        type=str,
        shape=[],
        description='''
        NAMD running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_namd_inout_control_velocity_dcd_first_step'))

    x_namd_inout_control_force_dcd_filename = Quantity(
        type=str,
        shape=[],
        description='''
        NAMD running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_namd_inout_control_force_dcd_filename'))

    x_namd_inout_control_force_dcd_frequency = Quantity(
        type=str,
        shape=[],
        description='''
        NAMD running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_namd_inout_control_force_dcd_frequency'))

    x_namd_inout_control_force_dcd_first_step = Quantity(
        type=str,
        shape=[],
        description='''
        NAMD running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_namd_inout_control_force_dcd_first_step'))

    x_namd_inout_control_output_filename = Quantity(
        type=str,
        shape=[],
        description='''
        NAMD running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_namd_inout_control_output_filename'))

    x_namd_inout_control_binary_output = Quantity(
        type=str,
        shape=[],
        description='''
        NAMD running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_namd_inout_control_binary_output'))

    x_namd_inout_control_restart_filename = Quantity(
        type=str,
        shape=[],
        description='''
        NAMD running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_namd_inout_control_restart_filename'))

    x_namd_inout_control_restart_frequency = Quantity(
        type=str,
        shape=[],
        description='''
        NAMD running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_namd_inout_control_restart_frequency'))

    x_namd_inout_control_binary_restart = Quantity(
        type=str,
        shape=[],
        description='''
        NAMD running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_namd_inout_control_binary_restart'))

    x_namd_inout_control_switching = Quantity(
        type=str,
        shape=[],
        description='''
        NAMD running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_namd_inout_control_switching'))

    x_namd_inout_control_switching_on = Quantity(
        type=str,
        shape=[],
        description='''
        NAMD running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_namd_inout_control_switching_on'))

    x_namd_inout_control_switching_off = Quantity(
        type=str,
        shape=[],
        description='''
        NAMD running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_namd_inout_control_switching_off'))

    x_namd_inout_control_pairlist_distance = Quantity(
        type=str,
        shape=[],
        description='''
        NAMD running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_namd_inout_control_pairlist_distance'))

    x_namd_inout_control_pairlist_shrink_rate = Quantity(
        type=str,
        shape=[],
        description='''
        NAMD running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_namd_inout_control_pairlist_shrink_rate'))

    x_namd_inout_control_pairlist_grow_rate = Quantity(
        type=str,
        shape=[],
        description='''
        NAMD running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_namd_inout_control_pairlist_grow_rate'))

    x_namd_inout_control_pairlist_trigger = Quantity(
        type=str,
        shape=[],
        description='''
        NAMD running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_namd_inout_control_pairlist_trigger'))

    x_namd_inout_control_pairlists_per_cycle = Quantity(
        type=str,
        shape=[],
        description='''
        NAMD running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_namd_inout_control_pairlists_per_cycle'))

    x_namd_inout_control_pairlists = Quantity(
        type=str,
        shape=[],
        description='''
        NAMD running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_namd_inout_control_pairlists'))

    x_namd_inout_control_margin = Quantity(
        type=str,
        shape=[],
        description='''
        NAMD running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_namd_inout_control_margin'))

    x_namd_inout_control_hydrogen_group_cutoff = Quantity(
        type=str,
        shape=[],
        description='''
        NAMD running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_namd_inout_control_hydrogen_group_cutoff'))

    x_namd_inout_control_patch_dimension = Quantity(
        type=str,
        shape=[],
        description='''
        NAMD running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_namd_inout_control_patch_dimension'))

    x_namd_inout_control_energy_output_steps = Quantity(
        type=str,
        shape=[],
        description='''
        NAMD running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_namd_inout_control_energy_output_steps'))

    x_namd_inout_control_crossterm_energy = Quantity(
        type=str,
        shape=[],
        description='''
        NAMD running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_namd_inout_control_crossterm_energy'))

    x_namd_inout_control_timing_output_steps = Quantity(
        type=str,
        shape=[],
        description='''
        NAMD running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_namd_inout_control_timing_output_steps'))

    x_namd_inout_control_velocity_rescale_freq = Quantity(
        type=str,
        shape=[],
        description='''
        NAMD running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_namd_inout_control_velocity_rescale_freq'))

    x_namd_inout_control_velocity_rescale_temp = Quantity(
        type=str,
        shape=[],
        description='''
        NAMD running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_namd_inout_control_velocity_rescale_temp'))

    x_namd_inout_control_velocity_reassignment_freq = Quantity(
        type=str,
        shape=[],
        description='''
        NAMD running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_namd_inout_control_velocity_reassignment_freq'))

    x_namd_inout_control_velocity_reassignment_temp = Quantity(
        type=str,
        shape=[],
        description='''
        NAMD running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_namd_inout_control_velocity_reassignment_temp'))

    x_namd_inout_control_velocity_reassignment_incr = Quantity(
        type=str,
        shape=[],
        description='''
        NAMD running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_namd_inout_control_velocity_reassignment_incr'))

    x_namd_inout_control_velocity_reassignment_hold = Quantity(
        type=str,
        shape=[],
        description='''
        NAMD running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_namd_inout_control_velocity_reassignment_hold'))

    x_namd_inout_control_lowe_andersen_dynamics = Quantity(
        type=str,
        shape=[],
        description='''
        NAMD running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_namd_inout_control_lowe_andersen_dynamics'))

    x_namd_inout_control_lowe_andersen_temperature = Quantity(
        type=str,
        shape=[],
        description='''
        NAMD running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_namd_inout_control_lowe_andersen_temperature'))

    x_namd_inout_control_lowe_andersen_rate = Quantity(
        type=str,
        shape=[],
        description='''
        NAMD running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_namd_inout_control_lowe_andersen_rate'))

    x_namd_inout_control_lowe_andersen_cutoff = Quantity(
        type=str,
        shape=[],
        description='''
        NAMD running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_namd_inout_control_lowe_andersen_cutoff'))

    x_namd_inout_control_langevin_dynamics = Quantity(
        type=str,
        shape=[],
        description='''
        NAMD running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_namd_inout_control_langevin_dynamics'))

    x_namd_inout_control_langevin_temperature = Quantity(
        type=str,
        shape=[],
        description='''
        NAMD running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_namd_inout_control_langevin_temperature'))

    x_namd_inout_control_langevin_integrator = Quantity(
        type=str,
        shape=[],
        description='''
        NAMD running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_namd_inout_control_langevin_integrator'))

    x_namd_inout_control_langevin_damping_file = Quantity(
        type=str,
        shape=[],
        description='''
        NAMD running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_namd_inout_control_langevin_damping_file'))

    x_namd_inout_control_langevin_damping_column = Quantity(
        type=str,
        shape=[],
        description='''
        NAMD running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_namd_inout_control_langevin_damping_column'))

    x_namd_inout_control_langevin_damping_coefficient_unit = Quantity(
        type=str,
        shape=[],
        description='''
        NAMD running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_namd_inout_control_langevin_damping_coefficient_unit'))

    x_namd_inout_control_langevin_dynamics_not_applied_to = Quantity(
        type=str,
        shape=[],
        description='''
        NAMD running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_namd_inout_control_langevin_dynamics_not_applied_to'))

    x_namd_inout_control_temperature_coupling = Quantity(
        type=str,
        shape=[],
        description='''
        NAMD running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_namd_inout_control_temperature_coupling'))

    x_namd_inout_control_coupling_temperature = Quantity(
        type=str,
        shape=[],
        description='''
        NAMD running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_namd_inout_control_coupling_temperature'))

    x_namd_inout_control_berendsen_pressure_coupling = Quantity(
        type=str,
        shape=[],
        description='''
        NAMD running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_namd_inout_control_berendsen_pressure_coupling'))

    x_namd_inout_control_berendsen_compressibility_estimate = Quantity(
        type=str,
        shape=[],
        description='''
        NAMD running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_namd_inout_control_berendsen_compressibility_estimate'))

    x_namd_inout_control_berendsen_relaxation_time = Quantity(
        type=str,
        shape=[],
        description='''
        NAMD running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_namd_inout_control_berendsen_relaxation_time'))

    x_namd_inout_control_berendsen_coupling_frequency = Quantity(
        type=str,
        shape=[],
        description='''
        NAMD running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_namd_inout_control_berendsen_coupling_frequency'))

    x_namd_inout_control_langevin_piston_pressure_control = Quantity(
        type=str,
        shape=[],
        description='''
        NAMD running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_namd_inout_control_langevin_piston_pressure_control'))

    x_namd_inout_control_target_pressure = Quantity(
        type=str,
        shape=[],
        description='''
        NAMD running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_namd_inout_control_target_pressure'))

    x_namd_inout_control_langevin_oscillation_period = Quantity(
        type=str,
        shape=[],
        description='''
        NAMD running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_namd_inout_control_langevin_oscillation_period'))

    x_namd_inout_control_langevin_decay_time = Quantity(
        type=str,
        shape=[],
        description='''
        NAMD running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_namd_inout_control_langevin_decay_time'))

    x_namd_inout_control_langevin_piston_temperature = Quantity(
        type=str,
        shape=[],
        description='''
        NAMD running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_namd_inout_control_langevin_piston_temperature'))

    x_namd_inout_control_pressure_control = Quantity(
        type=str,
        shape=[],
        description='''
        NAMD running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_namd_inout_control_pressure_control'))

    x_namd_inout_control_initial_strain_rate = Quantity(
        type=str,
        shape=[],
        description='''
        NAMD running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_namd_inout_control_initial_strain_rate'))

    x_namd_inout_control_cell_fluctuation = Quantity(
        type=str,
        shape=[],
        description='''
        NAMD running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_namd_inout_control_cell_fluctuation'))

    x_namd_inout_control_particle_mesh_ewald = Quantity(
        type=str,
        shape=[],
        description='''
        NAMD running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_namd_inout_control_particle_mesh_ewald'))

    x_namd_inout_control_pme_tolerance = Quantity(
        type=str,
        shape=[],
        description='''
        NAMD running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_namd_inout_control_pme_tolerance'))

    x_namd_inout_control_pme_ewald_coefficient = Quantity(
        type=str,
        shape=[],
        description='''
        NAMD running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_namd_inout_control_pme_ewald_coefficient'))

    x_namd_inout_control_pme_interpolation_order = Quantity(
        type=str,
        shape=[],
        description='''
        NAMD running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_namd_inout_control_pme_interpolation_order'))

    x_namd_inout_control_pme_grid_dimensions = Quantity(
        type=str,
        shape=[],
        description='''
        NAMD running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_namd_inout_control_pme_grid_dimensions'))

    x_namd_inout_control_pme_maximum_grid_spacing = Quantity(
        type=str,
        shape=[],
        description='''
        NAMD running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_namd_inout_control_pme_maximum_grid_spacing'))

    x_namd_inout_control_fftw_data_file = Quantity(
        type=str,
        shape=[],
        description='''
        NAMD running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_namd_inout_control_fftw_data_file'))

    x_namd_inout_control_full_electrostatic_evaluation_frequency = Quantity(
        type=str,
        shape=[],
        description='''
        NAMD running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_namd_inout_control_full_electrostatic_evaluation_frequency'))

    x_namd_inout_control_minimization = Quantity(
        type=str,
        shape=[],
        description='''
        NAMD running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_namd_inout_control_minimization'))

    x_namd_inout_control_velocity_quenching = Quantity(
        type=str,
        shape=[],
        description='''
        NAMD running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_namd_inout_control_velocity_quenching'))

    x_namd_inout_control_verlet_integrator = Quantity(
        type=str,
        shape=[],
        description='''
        NAMD running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_namd_inout_control_verlet_integrator'))

    x_namd_inout_control_random_number_seed = Quantity(
        type=str,
        shape=[],
        description='''
        NAMD running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_namd_inout_control_random_number_seed'))

    x_namd_inout_control_use_hydrogen_bonds = Quantity(
        type=str,
        shape=[],
        description='''
        NAMD running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_namd_inout_control_use_hydrogen_bonds'))

    x_namd_inout_control_coordinate_pdb = Quantity(
        type=str,
        shape=[],
        description='''
        NAMD running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_namd_inout_control_coordinate_pdb'))

    x_namd_inout_control_structure_file = Quantity(
        type=str,
        shape=[],
        description='''
        NAMD running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_namd_inout_control_structure_file'))

    x_namd_inout_control_parameter_file = Quantity(
        type=str,
        shape=[],
        description='''
        NAMD running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_namd_inout_control_parameter_file'))

    x_namd_inout_control_number_of_parameters = Quantity(
        type=np.dtype(np.int32),
        shape=[],
        description='''
        NAMD running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_namd_inout_control_number_of_parameters'))

    x_namd_inout_control_parameters = Quantity(
        type=str,
        shape=['x_namd_inout_control_number_of_parameters'],
        description='''
        NAMD running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_namd_inout_control_parameters'))


class x_namd_section_atom_to_atom_type_ref(MSection):
    '''
    Section to store atom label to atom type definition list
    '''

    m_def = Section(validate=False, a_legacy=LegacyDefinition(name='x_namd_section_atom_to_atom_type_ref'))

    x_namd_atom_to_atom_type_ref = Quantity(
        type=np.dtype(np.int64),
        shape=['number_of_atoms_per_type'],
        description='''
        Reference to the atoms of each atom type.
        ''',
        a_legacy=LegacyDefinition(name='x_namd_atom_to_atom_type_ref'))


class x_namd_section_single_configuration_calculation(MSection):
    '''
    section for gathering values for MD steps
    '''

    m_def = Section(validate=False, a_legacy=LegacyDefinition(name='x_namd_section_single_configuration_calculation'))


class section_system(public.section_system):

    m_def = Section(validate=False, extends_base_section=True, a_legacy=LegacyDefinition(name='section_system'))

    x_namd_atom_positions_image_index = Quantity(
        type=np.dtype(np.int32),
        shape=['number_of_atoms', 3],
        unit='dimensionless',
        description='''
        PBC image flag index.
        ''',
        a_legacy=LegacyDefinition(name='x_namd_atom_positions_image_index'))

    x_namd_atom_positions_scaled = Quantity(
        type=np.dtype(np.float64),
        shape=['number_of_atoms', 3],
        unit='dimensionless',
        description='''
        Position of the atoms in a scaled format [0, 1].
        ''',
        a_legacy=LegacyDefinition(name='x_namd_atom_positions_scaled'))

    x_namd_atom_positions_wrapped = Quantity(
        type=np.dtype(np.float64),
        shape=['number_of_atoms', 3],
        unit='meter',
        description='''
        Position of the atoms wrapped back to the periodic box.
        ''',
        a_legacy=LegacyDefinition(name='x_namd_atom_positions_wrapped'))

    x_namd_lattice_lengths = Quantity(
        type=np.dtype(np.float64),
        shape=[3],
        description='''
        Lattice dimensions in a vector. Vector includes [a, b, c] lengths.
        ''',
        categories=[public.configuration_core],
        a_legacy=LegacyDefinition(name='x_namd_lattice_lengths'))

    x_namd_lattice_angles = Quantity(
        type=np.dtype(np.float64),
        shape=[3],
        description='''
        Angles of lattice vectors. Vector includes [alpha, beta, gamma] in degrees.
        ''',
        categories=[public.configuration_core],
        a_legacy=LegacyDefinition(name='x_namd_lattice_angles'))

    x_namd_dummy = Quantity(
        type=str,
        shape=[],
        description='''
        dummy
        ''',
        a_legacy=LegacyDefinition(name='x_namd_dummy'))

    x_namd_mdin_finline = Quantity(
        type=str,
        shape=[],
        description='''
        finline in mdin
        ''',
        a_legacy=LegacyDefinition(name='x_namd_mdin_finline'))

    x_namd_traj_timestep_store = Quantity(
        type=str,
        shape=[],
        description='''
        tmp
        ''',
        a_legacy=LegacyDefinition(name='x_namd_traj_timestep_store'))

    x_namd_traj_number_of_atoms_store = Quantity(
        type=str,
        shape=[],
        description='''
        tmp
        ''',
        a_legacy=LegacyDefinition(name='x_namd_traj_number_of_atoms_store'))

    x_namd_traj_box_bound_store = Quantity(
        type=str,
        shape=[],
        description='''
        tmp
        ''',
        a_legacy=LegacyDefinition(name='x_namd_traj_box_bound_store'))

    x_namd_traj_box_bounds_store = Quantity(
        type=str,
        shape=[],
        description='''
        tmp
        ''',
        a_legacy=LegacyDefinition(name='x_namd_traj_box_bounds_store'))

    x_namd_traj_variables_store = Quantity(
        type=str,
        shape=[],
        description='''
        tmp
        ''',
        a_legacy=LegacyDefinition(name='x_namd_traj_variables_store'))

    x_namd_traj_atoms_store = Quantity(
        type=str,
        shape=[],
        description='''
        tmp
        ''',
        a_legacy=LegacyDefinition(name='x_namd_traj_atoms_store'))


class section_sampling_method(public.section_sampling_method):

    m_def = Section(validate=False, extends_base_section=True, a_legacy=LegacyDefinition(name='section_sampling_method'))

    x_namd_barostat_target_pressure = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        unit='pascal',
        description='''
        MD barostat target pressure.
        ''',
        categories=[public.settings_molecular_dynamics, public.settings_sampling, public.settings_barostat],
        a_legacy=LegacyDefinition(name='x_namd_barostat_target_pressure'))

    x_namd_barostat_tau = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        unit='second',
        description='''
        MD barostat relaxation time.
        ''',
        categories=[public.settings_molecular_dynamics, public.settings_sampling, public.settings_barostat],
        a_legacy=LegacyDefinition(name='x_namd_barostat_tau'))

    x_namd_barostat_type = Quantity(
        type=str,
        shape=[],
        description='''
        MD barostat type, valid values are defined in the barostat_type wiki page.
        ''',
        categories=[public.settings_molecular_dynamics, public.settings_sampling, public.settings_barostat],
        a_legacy=LegacyDefinition(name='x_namd_barostat_type'))

    x_namd_integrator_dt = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        unit='second',
        description='''
        MD integration time step.
        ''',
        categories=[public.settings_molecular_dynamics, public.settings_sampling, public.settings_integrator],
        a_legacy=LegacyDefinition(name='x_namd_integrator_dt'))

    x_namd_integrator_type = Quantity(
        type=str,
        shape=[],
        description='''
        MD integrator type, valid values are defined in the integrator_type wiki page.
        ''',
        categories=[public.settings_molecular_dynamics, public.settings_sampling, public.settings_integrator],
        a_legacy=LegacyDefinition(name='x_namd_integrator_type'))

    x_namd_periodicity_type = Quantity(
        type=str,
        shape=[],
        description='''
        Periodic boundary condition type in the sampling (non-PBC or PBC).
        ''',
        categories=[public.settings_molecular_dynamics, public.settings_sampling, public.settings_integrator],
        a_legacy=LegacyDefinition(name='x_namd_periodicity_type'))

    x_namd_langevin_gamma = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        unit='second',
        description='''
        Langevin thermostat damping factor.
        ''',
        categories=[public.settings_sampling, public.settings_molecular_dynamics, public.settings_thermostat],
        a_legacy=LegacyDefinition(name='x_namd_langevin_gamma'))

    x_namd_number_of_steps_requested = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        description='''
        Number of requested MD integration time steps.
        ''',
        categories=[public.settings_molecular_dynamics, public.settings_sampling, public.settings_integrator],
        a_legacy=LegacyDefinition(name='x_namd_number_of_steps_requested'))

    x_namd_thermostat_level = Quantity(
        type=str,
        shape=[],
        description='''
        MD thermostat level (see wiki: single, multiple, regional).
        ''',
        categories=[public.settings_sampling, public.settings_molecular_dynamics, public.settings_thermostat],
        a_legacy=LegacyDefinition(name='x_namd_thermostat_level'))

    x_namd_thermostat_target_temperature = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        unit='kelvin',
        description='''
        MD thermostat target temperature.
        ''',
        categories=[public.settings_sampling, public.settings_molecular_dynamics, public.settings_thermostat],
        a_legacy=LegacyDefinition(name='x_namd_thermostat_target_temperature'))

    x_namd_thermostat_tau = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        unit='second',
        description='''
        MD thermostat relaxation time.
        ''',
        categories=[public.settings_sampling, public.settings_molecular_dynamics, public.settings_thermostat],
        a_legacy=LegacyDefinition(name='x_namd_thermostat_tau'))

    x_namd_thermostat_type = Quantity(
        type=str,
        shape=[],
        description='''
        MD thermostat type, valid values are defined in the thermostat_type wiki page.
        ''',
        categories=[public.settings_sampling, public.settings_molecular_dynamics, public.settings_thermostat],
        a_legacy=LegacyDefinition(name='x_namd_thermostat_type'))


class section_atom_type(common.section_atom_type):

    m_def = Section(validate=False, extends_base_section=True, a_legacy=LegacyDefinition(name='section_atom_type'))

    x_namd_atom_name = Quantity(
        type=str,
        shape=[],
        description='''
        Atom name of an atom in topology definition.
        ''',
        a_legacy=LegacyDefinition(name='x_namd_atom_name'))

    x_namd_atom_type = Quantity(
        type=str,
        shape=[],
        description='''
        Atom type of an atom in topology definition.
        ''',
        a_legacy=LegacyDefinition(name='x_namd_atom_type'))

    x_namd_atom_element = Quantity(
        type=str,
        shape=[],
        description='''
        Atom type of an atom in topology definition.
        ''',
        a_legacy=LegacyDefinition(name='x_namd_atom_element'))

    x_namd_atom_type_element = Quantity(
        type=str,
        shape=[],
        description='''
        Element symbol of an atom type.
        ''',
        a_legacy=LegacyDefinition(name='x_namd_atom_type_element'))

    x_namd_atom_type_radius = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        description='''
        van der Waals radius of an atom type.
        ''',
        a_legacy=LegacyDefinition(name='x_namd_atom_type_radius'))

    number_of_atoms_per_type = Quantity(
        type=int,
        shape=[],
        description='''
        Number of atoms involved in this type.
        ''',
        a_legacy=LegacyDefinition(name='number_of_atoms_per_type'))


class section_interaction(common.section_interaction):

    m_def = Section(validate=False, extends_base_section=True, a_legacy=LegacyDefinition(name='section_interaction'))

    x_namd_interaction_atom_to_atom_type_ref = Quantity(
        type=common.section_atom_type,
        shape=['number_of_atoms_per_interaction'],
        description='''
        Reference to the atom type of each interaction atoms.
        ''',
        a_legacy=LegacyDefinition(name='x_namd_interaction_atom_to_atom_type_ref'))

    x_namd_number_of_defined_pair_interactions = Quantity(
        type=np.dtype(np.int32),
        shape=[],
        description='''
        Number of defined pair interactions (L-J pairs).
        ''',
        a_legacy=LegacyDefinition(name='x_namd_number_of_defined_pair_interactions'))

    x_namd_pair_interaction_atom_type_ref = Quantity(
        type=common.section_atom_type,
        shape=['x_namd_number_of_defined_pair_interactions', 'number_of_atoms_per_interaction'],
        description='''
        Reference to the atom type for pair interactions.
        ''',
        a_legacy=LegacyDefinition(name='x_namd_pair_interaction_atom_type_ref'))

    x_namd_pair_interaction_parameters = Quantity(
        type=np.dtype(np.float64),
        shape=['x_namd_number_of_defined_pair_interactions', 2],
        description='''
        Pair interactions parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_namd_pair_interaction_parameters'))


class section_molecule_interaction(common.section_molecule_interaction):

    m_def = Section(validate=False, extends_base_section=True, a_legacy=LegacyDefinition(name='section_molecule_interaction'))

    x_namd_molecule_interaction_atom_to_atom_type_ref = Quantity(
        type=common.section_atom_type,
        shape=['number_of_atoms_per_interaction'],
        description='''
        Reference to the atom type of each molecule interaction atoms.
        ''',
        a_legacy=LegacyDefinition(name='x_namd_molecule_interaction_atom_to_atom_type_ref'))

    x_namd_number_of_defined_molecule_pair_interactions = Quantity(
        type=np.dtype(np.int32),
        shape=[],
        description='''
        Number of defined pair interactions within a molecule (L-J pairs).
        ''',
        a_legacy=LegacyDefinition(name='x_namd_number_of_defined_molecule_pair_interactions'))

    x_namd_pair_molecule_interaction_parameters = Quantity(
        type=np.dtype(np.float64),
        shape=['number_of_defined_molecule_pair_interactions', 2],
        description='''
        Molecule pair interactions parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_namd_pair_molecule_interaction_parameters'))

    x_namd_pair_molecule_interaction_to_atom_type_ref = Quantity(
        type=common.section_atom_type,
        shape=['x_namd_number_of_defined_pair_interactions', 'number_of_atoms_per_interaction'],
        description='''
        Reference to the atom type for pair interactions within a molecule.
        ''',
        a_legacy=LegacyDefinition(name='x_namd_pair_molecule_interaction_to_atom_type_ref'))


class section_run(public.section_run):

    m_def = Section(validate=False, extends_base_section=True, a_legacy=LegacyDefinition(name='section_run'))

    x_namd_program_version_date = Quantity(
        type=str,
        shape=[],
        description='''
        Program version date.
        ''',
        a_legacy=LegacyDefinition(name='x_namd_program_version_date'))

    x_namd_parallel_task_nr = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        description='''
        Program task no.
        ''',
        a_legacy=LegacyDefinition(name='x_namd_parallel_task_nr'))

    x_namd_build_osarch = Quantity(
        type=str,
        shape=[],
        description='''
        Program Build OS/ARCH
        ''',
        a_legacy=LegacyDefinition(name='x_namd_build_osarch'))

    x_namd_program_build_date = Quantity(
        type=str,
        shape=[],
        description='''
        Program Build date
        ''',
        a_legacy=LegacyDefinition(name='x_namd_program_build_date'))

    x_namd_program_citation = Quantity(
        type=str,
        shape=[],
        description='''
        Program citations
        ''',
        a_legacy=LegacyDefinition(name='x_namd_program_citation'))

    x_namd_number_of_tasks = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        description='''
        Number of tasks in parallel program (MPI).
        ''',
        a_legacy=LegacyDefinition(name='x_namd_number_of_tasks'))

    x_namd_program_module_version = Quantity(
        type=str,
        shape=[],
        description='''
        NAMD program module version.
        ''',
        a_legacy=LegacyDefinition(name='x_namd_program_module_version'))

    x_namd_program_license = Quantity(
        type=str,
        shape=[],
        description='''
        NAMD program license.
        ''',
        a_legacy=LegacyDefinition(name='x_namd_program_license'))

    x_namd_xlo_xhi = Quantity(
        type=str,
        shape=[],
        description='''
        test
        ''',
        a_legacy=LegacyDefinition(name='x_namd_xlo_xhi'))

    x_namd_data_file_store = Quantity(
        type=str,
        shape=[],
        description='''
        Filename of data file
        ''',
        a_legacy=LegacyDefinition(name='x_namd_data_file_store'))

    x_namd_program_working_path = Quantity(
        type=str,
        shape=[],
        description='''
        tmp
        ''',
        a_legacy=LegacyDefinition(name='x_namd_program_working_path'))

    x_namd_program_execution_host = Quantity(
        type=str,
        shape=[],
        description='''
        tmp
        ''',
        a_legacy=LegacyDefinition(name='x_namd_program_execution_host'))

    x_namd_program_execution_path = Quantity(
        type=str,
        shape=[],
        description='''
        tmp
        ''',
        a_legacy=LegacyDefinition(name='x_namd_program_execution_path'))

    x_namd_program_module = Quantity(
        type=str,
        shape=[],
        description='''
        tmp
        ''',
        a_legacy=LegacyDefinition(name='x_namd_program_module'))

    x_namd_program_execution_date = Quantity(
        type=str,
        shape=[],
        description='''
        tmp
        ''',
        a_legacy=LegacyDefinition(name='x_namd_program_execution_date'))

    x_namd_program_execution_time = Quantity(
        type=str,
        shape=[],
        description='''
        tmp
        ''',
        a_legacy=LegacyDefinition(name='x_namd_program_execution_time'))

    x_namd_mdin_header = Quantity(
        type=str,
        shape=[],
        description='''
        tmp
        ''',
        a_legacy=LegacyDefinition(name='x_namd_mdin_header'))

    x_namd_mdin_wt = Quantity(
        type=str,
        shape=[],
        description='''
        tmp
        ''',
        a_legacy=LegacyDefinition(name='x_namd_mdin_wt'))

    x_namd_section_input_output_files = SubSection(
        sub_section=SectionProxy('x_namd_section_input_output_files'),
        repeats=True,
        a_legacy=LegacyDefinition(name='x_namd_section_input_output_files'))

    x_namd_section_control_parameters = SubSection(
        sub_section=SectionProxy('x_namd_section_control_parameters'),
        repeats=True,
        a_legacy=LegacyDefinition(name='x_namd_section_control_parameters'))


class section_topology(common.section_topology):

    m_def = Section(validate=False, extends_base_section=True, a_legacy=LegacyDefinition(name='section_topology'))

    x_namd_input_units_store = Quantity(
        type=str,
        shape=[],
        description='''
        It determines the units of all quantities specified in the input script and data
        file, as well as quantities output to the screen, log file, and dump files.
        ''',
        a_legacy=LegacyDefinition(name='x_namd_input_units_store'))

    x_namd_data_bond_types_store = Quantity(
        type=np.dtype(np.int32),
        shape=[],
        description='''
        store temporarly
        ''',
        a_legacy=LegacyDefinition(name='x_namd_data_bond_types_store'))

    x_namd_data_bond_count_store = Quantity(
        type=np.dtype(np.int32),
        shape=[],
        description='''
        store temporarly
        ''',
        a_legacy=LegacyDefinition(name='x_namd_data_bond_count_store'))

    x_namd_data_angle_count_store = Quantity(
        type=np.dtype(np.int32),
        shape=[],
        description='''
        store temporarly
        ''',
        a_legacy=LegacyDefinition(name='x_namd_data_angle_count_store'))

    x_namd_data_atom_types_store = Quantity(
        type=np.dtype(np.int32),
        shape=[],
        description='''
        store temporarly
        ''',
        a_legacy=LegacyDefinition(name='x_namd_data_atom_types_store'))

    x_namd_data_dihedral_count_store = Quantity(
        type=np.dtype(np.int32),
        shape=[],
        description='''
        store temporarly
        ''',
        a_legacy=LegacyDefinition(name='x_namd_data_dihedral_count_store'))

    x_namd_data_angles_store = Quantity(
        type=str,
        shape=[],
        description='''
        store temporarly
        ''',
        a_legacy=LegacyDefinition(name='x_namd_data_angles_store'))

    x_namd_data_angle_list_store = Quantity(
        type=str,
        shape=[],
        description='''
        tmp
        ''',
        a_legacy=LegacyDefinition(name='x_namd_data_angle_list_store'))

    x_namd_data_bond_list_store = Quantity(
        type=str,
        shape=[],
        description='''
        tmp
        ''',
        a_legacy=LegacyDefinition(name='x_namd_data_bond_list_store'))

    x_namd_data_dihedral_list_store = Quantity(
        type=str,
        shape=[],
        description='''
        tmp
        ''',
        a_legacy=LegacyDefinition(name='x_namd_data_dihedral_list_store'))

    x_namd_data_dihedral_coeff_list_store = Quantity(
        type=str,
        shape=[],
        description='''
        tmp
        ''',
        a_legacy=LegacyDefinition(name='x_namd_data_dihedral_coeff_list_store'))

    x_namd_masses_store = Quantity(
        type=str,
        shape=[],
        description='''
        tmp
        ''',
        a_legacy=LegacyDefinition(name='x_namd_masses_store'))

    x_namd_data_topo_list_store = Quantity(
        type=str,
        shape=[],
        description='''
        tmp
        ''',
        a_legacy=LegacyDefinition(name='x_namd_data_topo_list_store'))

    x_namd_section_atom_to_atom_type_ref = SubSection(
        sub_section=SectionProxy('x_namd_section_atom_to_atom_type_ref'),
        repeats=True,
        a_legacy=LegacyDefinition(name='x_namd_section_atom_to_atom_type_ref'))


class section_frame_sequence(public.section_frame_sequence):

    m_def = Section(validate=False, extends_base_section=True, a_legacy=LegacyDefinition(name='section_frame_sequence'))

    x_namd_number_of_volumes_in_sequence = Quantity(
        type=int,
        shape=[],
        description='''
        Gives the number of volumes in this sequence of frames, see
        x_namd_frame_sequence_volume.
        ''',
        a_legacy=LegacyDefinition(name='x_namd_number_of_volumes_in_sequence'))

    x_namd_number_of_densities_in_sequence = Quantity(
        type=int,
        shape=[],
        description='''
        Gives the number of densities in this sequence of frames, see
        x_namd_frame_sequence_density.
        ''',
        a_legacy=LegacyDefinition(name='x_namd_number_of_densities_in_sequence'))

    x_namd_number_of_bond_energies_in_sequence = Quantity(
        type=int,
        shape=[],
        description='''
        Gives the number of bond_energies in this sequence of frames, see
        x_namd_frame_sequence_bond_energy.
        ''',
        a_legacy=LegacyDefinition(name='x_namd_number_of_bond_energies_in_sequence'))

    x_namd_number_of_angle_energies_in_sequence = Quantity(
        type=int,
        shape=[],
        description='''
        Gives the number of angle_energies in this sequence of frames, see
        x_namd_frame_sequence_angle_energy.
        ''',
        a_legacy=LegacyDefinition(name='x_namd_number_of_angle_energies_in_sequence'))

    x_namd_number_of_proper_dihedral_energies_in_sequence = Quantity(
        type=int,
        shape=[],
        description='''
        Gives the number of proper_dihedral_energies in this sequence of frames, see
        x_namd_frame_sequence_proper_dihedral_energy.
        ''',
        a_legacy=LegacyDefinition(name='x_namd_number_of_proper_dihedral_energies_in_sequence'))

    x_namd_number_of_improper_dihedral_energies_in_sequence = Quantity(
        type=int,
        shape=[],
        description='''
        Gives the number of improper_dihedral_energies in this sequence of frames, see
        x_namd_frame_sequence_improper_dihedral_energy.
        ''',
        a_legacy=LegacyDefinition(name='x_namd_number_of_improper_dihedral_energies_in_sequence'))

    x_namd_number_of_cmap_dihedral_energies_in_sequence = Quantity(
        type=int,
        shape=[],
        description='''
        Gives the number of cmap_dihedral_energies in this sequence of frames, see
        x_namd_frame_sequence_cmap_dihedral_energy.
        ''',
        a_legacy=LegacyDefinition(name='x_namd_number_of_cmap_dihedral_energies_in_sequence'))

    x_namd_number_of_vdw_energies_in_sequence = Quantity(
        type=int,
        shape=[],
        description='''
        Gives the number of vdw_energies in this sequence of frames, see
        x_namd_frame_sequence_vdw_energy.
        ''',
        a_legacy=LegacyDefinition(name='x_namd_number_of_vdw_energies_in_sequence'))

    x_namd_number_of_boundary_energies_in_sequence = Quantity(
        type=int,
        shape=[],
        description='''
        Gives the number of boundary_energies in this sequence of frames, see
        x_namd_frame_sequence_boundary_energy.
        ''',
        a_legacy=LegacyDefinition(name='x_namd_number_of_boundary_energies_in_sequence'))

    x_namd_number_of_electrostatic_energies_in_sequence = Quantity(
        type=int,
        shape=[],
        description='''
        Gives the number of electrostatic_energies in this sequence of frames, see
        x_namd_frame_sequence_electrostatic_energy.
        ''',
        a_legacy=LegacyDefinition(name='x_namd_number_of_electrostatic_energies_in_sequence'))

    x_namd_number_of_total2_energies_in_sequence = Quantity(
        type=int,
        shape=[],
        description='''
        Gives the number of total2_energies in this sequence of frames, see
        x_namd_frame_sequence_total2_energy.
        ''',
        a_legacy=LegacyDefinition(name='x_namd_number_of_total2_energies_in_sequence'))

    x_namd_number_of_total3_energies_in_sequence = Quantity(
        type=int,
        shape=[],
        description='''
        Gives the number of total3_energies in this sequence of frames, see
        x_namd_frame_sequence_total3_energy.
        ''',
        a_legacy=LegacyDefinition(name='x_namd_number_of_total3_energies_in_sequence'))

    x_namd_number_of_misc_energies_in_sequence = Quantity(
        type=int,
        shape=[],
        description='''
        Gives the number of misc_energies in this sequence of frames, see
        x_namd_frame_sequence_misc_energy.
        ''',
        a_legacy=LegacyDefinition(name='x_namd_number_of_misc_energies_in_sequence'))

    x_namd_frame_sequence_density_frames = Quantity(
        type=np.dtype(np.int32),
        shape=['x_namd_number_of_densities_in_sequence'],
        description='''
        Array containing the strictly increasing indices of the frames the
        x_namd_frame_sequence_densities values refers to. If not given it defaults to the
        trivial mapping 0,1,...
        ''',
        a_legacy=LegacyDefinition(name='x_namd_frame_sequence_density_frames'))

    x_namd_frame_sequence_density = Quantity(
        type=np.dtype(np.float64),
        shape=['x_namd_number_of_densities_in_sequence'],
        description='''
        Array containing the values of the density along this sequence of frames (i.e., a
        trajectory, a frame is one section_single_configuration_calculation). If not all
        frames have a value the indices of the frames that have a value are stored in
        frame_sequence_density_frames.
        ''',
        a_legacy=LegacyDefinition(name='x_namd_frame_sequence_density'))

    x_namd_frame_sequence_cmap_dihedral_energy_frames = Quantity(
        type=np.dtype(np.int32),
        shape=['x_namd_number_of_cmap_dihedral_energy_in_sequence'],
        description='''
        Array containing the strictly increasing indices of the frames the
        x_namd_frame_sequence_cmap_dihedral_energy values refers to. If not given it
        defaults to the trivial mapping 0,1,...
        ''',
        a_legacy=LegacyDefinition(name='x_namd_frame_sequence_cmap_dihedral_energy_frames'))

    x_namd_frame_sequence_cmap_dihedral_energy = Quantity(
        type=np.dtype(np.float64),
        shape=['x_namd_number_of_cmap_dihedral_energy_in_sequence'],
        description='''
        Array containing the values of the cmap_dihedral_energy along this sequence of
        frames (i.e., a trajectory, a frame is one
        section_single_configuration_calculation). If not all frames have a value the
        indices of the frames that have a value are stored in
        frame_sequence_cmap_dihedral_energy_frames.
        ''',
        a_legacy=LegacyDefinition(name='x_namd_frame_sequence_cmap_dihedral_energy'))

    x_namd_frame_sequence_improper_dihedral_energy_frames = Quantity(
        type=np.dtype(np.int32),
        shape=['x_namd_number_of_improper_dihedral_energy_in_sequence'],
        description='''
        Array containing the strictly increasing indices of the frames the
        x_namd_frame_sequence_improper_dihedral_energy values refers to. If not given it
        defaults to the trivial mapping 0,1,...
        ''',
        a_legacy=LegacyDefinition(name='x_namd_frame_sequence_improper_dihedral_energy_frames'))

    x_namd_frame_sequence_improper_dihedral_energy = Quantity(
        type=np.dtype(np.float64),
        shape=['x_namd_number_of_improper_dihedral_energy_in_sequence'],
        description='''
        Array containing the values of the improper_dihedral_energy along this sequence of
        frames (i.e., a trajectory, a frame is one
        section_single_configuration_calculation). If not all frames have a value the
        indices of the frames that have a value are stored in
        frame_sequence_improper_dihedral_energy_frames.
        ''',
        a_legacy=LegacyDefinition(name='x_namd_frame_sequence_improper_dihedral_energy'))

    x_namd_frame_sequence_proper_dihedral_energy_frames = Quantity(
        type=np.dtype(np.int32),
        shape=['x_namd_number_of_proper_dihedral_energy_in_sequence'],
        description='''
        Array containing the strictly increasing indices of the frames the
        x_namd_frame_sequence_proper_dihedral_energy values refers to. If not given it
        defaults to the trivial mapping 0,1,...
        ''',
        a_legacy=LegacyDefinition(name='x_namd_frame_sequence_proper_dihedral_energy_frames'))

    x_namd_frame_sequence_proper_dihedral_energy = Quantity(
        type=np.dtype(np.float64),
        shape=['x_namd_number_of_proper_dihedral_energy_in_sequence'],
        description='''
        Array containing the values of the proper_dihedral_energy along this sequence of
        frames (i.e., a trajectory, a frame is one
        section_single_configuration_calculation). If not all frames have a value the
        indices of the frames that have a value are stored in
        frame_sequence_proper_dihedral_energy_frames.
        ''',
        a_legacy=LegacyDefinition(name='x_namd_frame_sequence_proper_dihedral_energy'))

    x_namd_frame_sequence_bond_energy_frames = Quantity(
        type=np.dtype(np.int32),
        shape=['x_namd_number_of_bond_energies_in_sequence'],
        description='''
        Array containing the strictly increasing indices of the frames the
        x_namd_frame_sequence_bond_energy values refers to. If not given it defaults to
        the trivial mapping 0,1,...
        ''',
        a_legacy=LegacyDefinition(name='x_namd_frame_sequence_bond_energy_frames'))

    x_namd_frame_sequence_bond_energy = Quantity(
        type=np.dtype(np.float64),
        shape=['x_namd_number_of_bond_energies_in_sequence'],
        description='''
        Array containing the values of the bond_energy along this sequence of frames
        (i.e., a trajectory, a frame is one section_single_configuration_calculation). If
        not all frames have a value the indices of the frames that have a value are stored
        in frame_sequence_bond_energy_frames.
        ''',
        a_legacy=LegacyDefinition(name='x_namd_frame_sequence_bond_energy'))

    x_namd_frame_sequence_boundary_frames = Quantity(
        type=np.dtype(np.int32),
        shape=['x_namd_number_of_boundary_energies_in_sequence'],
        description='''
        Array containing the strictly increasing indices of the frames the
        x_namd_frame_sequence_boundary values refers to. If not given it defaults to the
        trivial mapping 0,1,...
        ''',
        a_legacy=LegacyDefinition(name='x_namd_frame_sequence_boundary_frames'))

    x_namd_frame_sequence_boundary = Quantity(
        type=np.dtype(np.float64),
        shape=['x_namd_number_of_boundary_energies_in_sequence'],
        description='''
        Array containing the values of the boundary along this sequence of frames (i.e., a
        trajectory, a frame is one section_single_configuration_calculation). If not all
        frames have a value the indices of the frames that have a value are stored in
        frame_sequence_boundary_frames.
        ''',
        a_legacy=LegacyDefinition(name='x_namd_frame_sequence_boundary'))

    x_namd_frame_sequence_angle_energy_frames = Quantity(
        type=np.dtype(np.int32),
        shape=['x_namd_number_of_angle_energies_in_sequence'],
        description='''
        Array containing the strictly increasing indices of the frames the
        x_namd_frame_sequence_angle_energy values refers to. If not given it defaults to
        the trivial mapping 0,1,...
        ''',
        a_legacy=LegacyDefinition(name='x_namd_frame_sequence_angle_energy_frames'))

    x_namd_frame_sequence_angle_energy = Quantity(
        type=np.dtype(np.float64),
        shape=['x_namd_number_of_angle_energies_in_sequence'],
        description='''
        Array containing the values of the angle_energy along this sequence of frames
        (i.e., a trajectory, a frame is one section_single_configuration_calculation). If
        not all frames have a value the indices of the frames that have a value are stored
        in frame_sequence_angle_energy_frames.
        ''',
        a_legacy=LegacyDefinition(name='x_namd_frame_sequence_angle_energy'))

    x_namd_frame_sequence_vdw_energy_frames = Quantity(
        type=np.dtype(np.int32),
        shape=['x_namd_number_of_vdw_energies_in_sequence'],
        description='''
        Array containing the strictly increasing indices of the frames the
        x_namd_frame_sequence_vdw_energy values refers to. If not given it defaults to the
        trivial mapping 0,1,...
        ''',
        a_legacy=LegacyDefinition(name='x_namd_frame_sequence_vdw_energy_frames'))

    x_namd_frame_sequence_vdw_energy = Quantity(
        type=np.dtype(np.float64),
        shape=['x_namd_number_of_vdw_energies_in_sequence'],
        description='''
        Array containing the values of the vdw_energy along this sequence of frames (i.e.,
        a trajectory, a frame is one section_single_configuration_calculation). If not all
        frames have a value the indices of the frames that have a value are stored in
        frame_sequence_vdw_energy_frames.
        ''',
        a_legacy=LegacyDefinition(name='x_namd_frame_sequence_vdw_energy'))

    x_namd_frame_sequence_electrostatic_energy_frames = Quantity(
        type=np.dtype(np.int32),
        shape=['x_namd_number_of_electrostatic_energies_in_sequence'],
        description='''
        Array containing the strictly increasing indices of the frames the
        x_namd_frame_sequence_electrostatic_energy values refers to. If not given it
        defaults to the trivial mapping 0,1,...
        ''',
        a_legacy=LegacyDefinition(name='x_namd_frame_sequence_electrostatic_energy_frames'))

    x_namd_frame_sequence_electrostatic_energy = Quantity(
        type=np.dtype(np.float64),
        shape=['x_namd_number_of_electrostatic_energies_in_sequence'],
        description='''
        Array containing the values of the electrostatic_energy along this sequence of
        frames (i.e., a trajectory, a frame is one
        section_single_configuration_calculation). If not all frames have a value the
        indices of the frames that have a value are stored in
        frame_sequence_electrostatic_energy_frames.
        ''',
        a_legacy=LegacyDefinition(name='x_namd_frame_sequence_electrostatic_energy'))

    x_namd_frame_sequence_total2_energy_frames = Quantity(
        type=np.dtype(np.int32),
        shape=['x_namd_number_of_total2_energies_in_sequence'],
        description='''
        Array containing the strictly increasing indices of the frames the
        x_namd_frame_sequence_total2_energy values refers to. If not given it defaults to
        the trivial mapping 0,1,...
        ''',
        a_legacy=LegacyDefinition(name='x_namd_frame_sequence_total2_energy_frames'))

    x_namd_frame_sequence_total2_energy = Quantity(
        type=np.dtype(np.float64),
        shape=['x_namd_number_of_total2_energies_in_sequence'],
        description='''
        Array containing the values of the total2_energy along this sequence of frames
        (i.e., a trajectory, a frame is one section_single_configuration_calculation). If
        not all frames have a value the indices of the frames that have a value are stored
        in frame_sequence_total2_energy_frames.
        ''',
        a_legacy=LegacyDefinition(name='x_namd_frame_sequence_total2_energy'))

    x_namd_frame_sequence_total3_energy_frames = Quantity(
        type=np.dtype(np.int32),
        shape=['x_namd_number_of_total3_energies_in_sequence'],
        description='''
        Array containing the strictly increasing indices of the frames the
        x_namd_frame_sequence_total3_energy values refers to. If not given it defaults to
        the trivial mapping 0,1,...
        ''',
        a_legacy=LegacyDefinition(name='x_namd_frame_sequence_total3_energy_frames'))

    x_namd_frame_sequence_total3_energy = Quantity(
        type=np.dtype(np.float64),
        shape=['x_namd_number_of_total3_energies_in_sequence'],
        description='''
        Array containing the values of the total3_energy along this sequence of frames
        (i.e., a trajectory, a frame is one section_single_configuration_calculation). If
        not all frames have a value the indices of the frames that have a value are stored
        in frame_sequence_total3_energy_frames.
        ''',
        a_legacy=LegacyDefinition(name='x_namd_frame_sequence_total3_energy'))

    x_namd_frame_sequence_misc_energy_frames = Quantity(
        type=np.dtype(np.int32),
        shape=['x_namd_number_of_misc_energies_in_sequence'],
        description='''
        Array containing the strictly increasing indices of the frames the
        x_namd_frame_sequence_misc_energy values refers to. If not given it defaults to
        the trivial mapping 0,1,...
        ''',
        a_legacy=LegacyDefinition(name='x_namd_frame_sequence_misc_energy_frames'))

    x_namd_frame_sequence_misc_energy = Quantity(
        type=np.dtype(np.float64),
        shape=['x_namd_number_of_misc_energies_in_sequence'],
        description='''
        Array containing the values of the misc_energy along this sequence of frames
        (i.e., a trajectory, a frame is one section_single_configuration_calculation). If
        not all frames have a value the indices of the frames that have a value are stored
        in frame_sequence_misc_energy_frames.
        ''',
        a_legacy=LegacyDefinition(name='x_namd_frame_sequence_misc_energy'))

    x_namd_frame_sequence_volume_frames = Quantity(
        type=np.dtype(np.int32),
        shape=['x_namd_number_of_volumes_in_sequence'],
        description='''
        Array containing the strictly increasing indices of the frames the
        x_namd_frame_sequence_volume values refers to. If not given it defaults to the
        trivial mapping 0,1,...
        ''',
        a_legacy=LegacyDefinition(name='x_namd_frame_sequence_volume_frames'))

    x_namd_frame_sequence_volume = Quantity(
        type=np.dtype(np.float64),
        shape=['x_namd_number_of_volumes_in_sequence'],
        description='''
        Array containing the values of the volume along this sequence of frames (i.e., a
        trajectory, a frame is one section_single_configuration_calculation). If not all
        frames have a value the indices of the frames that have a value are stored in
        frame_sequence_volume_frames.
        ''',
        a_legacy=LegacyDefinition(name='x_namd_frame_sequence_volume'))


class section_single_configuration_calculation(public.section_single_configuration_calculation):

    m_def = Section(validate=False, extends_base_section=True, a_legacy=LegacyDefinition(name='section_single_configuration_calculation'))

    x_namd_section_single_configuration_calculation = SubSection(
        sub_section=SectionProxy('x_namd_section_single_configuration_calculation'),
        repeats=True,
        a_legacy=LegacyDefinition(name='x_namd_section_single_configuration_calculation'))


m_package.__init_metainfo__()
