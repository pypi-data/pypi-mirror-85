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
    name='gromos_nomadmetainfo_json',
    description='None',
    a_legacy=LegacyDefinition(name='gromos.nomadmetainfo.json'))


class x_gromos_mdin_input_output_files(MCategory):
    '''
    Parameters of mdin belonging to x_gromos_section_control_parameters.
    '''

    m_def = Category(
        a_legacy=LegacyDefinition(name='x_gromos_mdin_input_output_files'))


class x_gromos_mdin_control_parameters(MCategory):
    '''
    Parameters of mdin belonging to x_gromos_section_control_parameters.
    '''

    m_def = Category(
        a_legacy=LegacyDefinition(name='x_gromos_mdin_control_parameters'))


class x_gromos_mdin_method(MCategory):
    '''
    Parameters of mdin belonging to section method.
    '''

    m_def = Category(
        a_legacy=LegacyDefinition(name='x_gromos_mdin_method'))


class x_gromos_mdout_single_configuration_calculation(MCategory):
    '''
    Parameters of mdout belonging to section_single_configuration_calculation.
    '''

    m_def = Category(
        a_legacy=LegacyDefinition(name='x_gromos_mdout_single_configuration_calculation'))


class x_gromos_mdout_method(MCategory):
    '''
    Parameters of mdin belonging to section method.
    '''

    m_def = Category(
        a_legacy=LegacyDefinition(name='x_gromos_mdout_method'))


class x_gromos_mdout_run(MCategory):
    '''
    Parameters of mdin belonging to settings run.
    '''

    m_def = Category(
        categories=[public.settings_run],
        a_legacy=LegacyDefinition(name='x_gromos_mdout_run'))


class x_gromos_mdin_run(MCategory):
    '''
    Parameters of mdin belonging to settings run.
    '''

    m_def = Category(
        categories=[public.settings_run],
        a_legacy=LegacyDefinition(name='x_gromos_mdin_run'))


class x_gromos_section_input_output_files(MSection):
    '''
    Section to store input and output file names
    '''

    m_def = Section(validate=False, a_legacy=LegacyDefinition(name='x_gromos_section_input_output_files'))


class x_gromos_section_control_parameters(MSection):
    '''
    Section to store the input and output control parameters
    '''

    m_def = Section(validate=False, a_legacy=LegacyDefinition(name='x_gromos_section_control_parameters'))

    x_gromos_inout_file_structure = Quantity(
        type=str,
        shape=[],
        description='''
        gromos input topology file.
        ''',
        a_legacy=LegacyDefinition(name='x_gromos_inout_file_structure'))

    x_gromos_inout_file_trajectory = Quantity(
        type=str,
        shape=[],
        description='''
        gromos output trajectory file.
        ''',
        a_legacy=LegacyDefinition(name='x_gromos_inout_file_trajectory'))

    x_gromos_inout_file_traj_coord = Quantity(
        type=str,
        shape=[],
        description='''
        gromos output trajectory file.
        ''',
        a_legacy=LegacyDefinition(name='x_gromos_inout_file_traj_coord'))

    x_gromos_inout_file_traj_vel = Quantity(
        type=str,
        shape=[],
        description='''
        gromos output file for velocities in the trajectory.
        ''',
        a_legacy=LegacyDefinition(name='x_gromos_inout_file_traj_vel'))

    x_gromos_inout_file_traj_force = Quantity(
        type=str,
        shape=[],
        description='''
        gromos output file for forces in the trajectory.
        ''',
        a_legacy=LegacyDefinition(name='x_gromos_inout_file_traj_force'))

    x_gromos_inout_file_output_coord = Quantity(
        type=str,
        shape=[],
        description='''
        gromos output coordinates file.
        ''',
        a_legacy=LegacyDefinition(name='x_gromos_inout_file_output_coord'))

    x_gromos_inout_file_output_vel = Quantity(
        type=str,
        shape=[],
        description='''
        gromos output velocities file.
        ''',
        a_legacy=LegacyDefinition(name='x_gromos_inout_file_output_vel'))

    x_gromos_inout_file_output_force = Quantity(
        type=str,
        shape=[],
        description='''
        gromos output forces file.
        ''',
        a_legacy=LegacyDefinition(name='x_gromos_inout_file_output_force'))

    x_gromos_inout_file_input_coord = Quantity(
        type=str,
        shape=[],
        description='''
        gromos input coordinates file.
        ''',
        a_legacy=LegacyDefinition(name='x_gromos_inout_file_input_coord'))

    x_gromos_inout_file_input_vel = Quantity(
        type=str,
        shape=[],
        description='''
        gromos input velocities file.
        ''',
        a_legacy=LegacyDefinition(name='x_gromos_inout_file_input_vel'))

    x_gromos_inout_file_restart_coord = Quantity(
        type=str,
        shape=[],
        description='''
        gromos restart coordinates file.
        ''',
        a_legacy=LegacyDefinition(name='x_gromos_inout_file_restart_coord'))

    x_gromos_inout_file_restart_vel = Quantity(
        type=str,
        shape=[],
        description='''
        gromos restart velocities file.
        ''',
        a_legacy=LegacyDefinition(name='x_gromos_inout_file_restart_vel'))

    x_gromos_inout_file_output_log = Quantity(
        type=str,
        shape=[],
        description='''
        gromos MD output log file.
        ''',
        a_legacy=LegacyDefinition(name='x_gromos_inout_file_output_log'))

    x_gromos_inout_control_number_of_steps = Quantity(
        type=str,
        shape=[],
        description='''
        gromos running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_gromos_inout_control_number_of_steps'))

    x_gromos_inout_control_steps_per_cycle = Quantity(
        type=str,
        shape=[],
        description='''
        gromos running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_gromos_inout_control_steps_per_cycle'))

    x_gromos_inout_control_initial_temperature = Quantity(
        type=str,
        shape=[],
        description='''
        gromos running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_gromos_inout_control_initial_temperature'))

    x_gromos_inout_control_dielectric = Quantity(
        type=str,
        shape=[],
        description='''
        gromos running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_gromos_inout_control_dielectric'))

    x_gromos_inout_control_minimization = Quantity(
        type=str,
        shape=[],
        description='''
        gromos running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_gromos_inout_control_minimization'))

    x_gromos_inout_control_verlet_integrator = Quantity(
        type=str,
        shape=[],
        description='''
        gromos running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_gromos_inout_control_verlet_integrator'))

    x_gromos_inout_control_topology_parameters = Quantity(
        type=str,
        shape=[],
        description='''
        gromos running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_gromos_inout_control_topology_parameters'))

    x_gromos_inout_control_topology_type = Quantity(
        type=str,
        shape=[],
        description='''
        gromos running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_gromos_inout_control_topology_type'))

    x_gromos_inout_control_resname = Quantity(
        type=str,
        shape=[],
        description='''
        gromos running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_gromos_inout_control_resname'))

    x_gromos_inout_control_number_of_atom_types = Quantity(
        type=str,
        shape=[],
        description='''
        gromos running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_gromos_inout_control_number_of_atom_types'))

    x_gromos_inout_control_number_of_atoms_solute = Quantity(
        type=str,
        shape=[],
        description='''
        gromos running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_gromos_inout_control_number_of_atoms_solute'))

    x_gromos_inout_control_lennard_jones_exceptions = Quantity(
        type=str,
        shape=[],
        description='''
        gromos running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_gromos_inout_control_lennard_jones_exceptions'))

    x_gromos_inout_control_number_of_h_bonds_at_constraint = Quantity(
        type=str,
        shape=[],
        description='''
        gromos running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_gromos_inout_control_number_of_h_bonds_at_constraint'))

    x_gromos_inout_control_number_of_bonds_at_constraint = Quantity(
        type=str,
        shape=[],
        description='''
        gromos running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_gromos_inout_control_number_of_bonds_at_constraint'))

    x_gromos_inout_control_bondangles_containing_hydrogens = Quantity(
        type=str,
        shape=[],
        description='''
        gromos running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_gromos_inout_control_bondangles_containing_hydrogens'))

    x_gromos_inout_control_bondangles_not_containing_hydrogens = Quantity(
        type=str,
        shape=[],
        description='''
        gromos running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_gromos_inout_control_bondangles_not_containing_hydrogens'))

    x_gromos_inout_control_improper_dihedrals_not_containing_hydrogens = Quantity(
        type=str,
        shape=[],
        description='''
        gromos running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_gromos_inout_control_improper_dihedrals_not_containing_hydrogens'))

    x_gromos_inout_control_improper_dihedrals_containing_hydrogens = Quantity(
        type=str,
        shape=[],
        description='''
        gromos running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_gromos_inout_control_improper_dihedrals_containing_hydrogens'))

    x_gromos_inout_control_dihedrals_not_containing_hydrogens = Quantity(
        type=str,
        shape=[],
        description='''
        gromos running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_gromos_inout_control_dihedrals_not_containing_hydrogens'))

    x_gromos_inout_control_dihedrals_containing_hydrogens = Quantity(
        type=str,
        shape=[],
        description='''
        gromos running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_gromos_inout_control_dihedrals_containing_hydrogens'))

    x_gromos_inout_control_crossdihedrals_not_containing_hydrogens = Quantity(
        type=str,
        shape=[],
        description='''
        gromos running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_gromos_inout_control_crossdihedrals_not_containing_hydrogens'))

    x_gromos_inout_control_crossdihedrals_containing_hydrogens = Quantity(
        type=str,
        shape=[],
        description='''
        gromos running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_gromos_inout_control_crossdihedrals_containing_hydrogens'))

    x_gromos_inout_control_number_of_solvent_atoms = Quantity(
        type=str,
        shape=[],
        description='''
        gromos running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_gromos_inout_control_number_of_solvent_atoms'))

    x_gromos_inout_control_number_of_solvent_constraints = Quantity(
        type=str,
        shape=[],
        description='''
        gromos running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_gromos_inout_control_number_of_solvent_constraints'))

    x_gromos_inout_control_number_of_solvents_added = Quantity(
        type=str,
        shape=[],
        description='''
        gromos running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_gromos_inout_control_number_of_solvents_added'))

    x_gromos_inout_control_number_of_molecules_in_solute = Quantity(
        type=str,
        shape=[],
        description='''
        gromos running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_gromos_inout_control_number_of_molecules_in_solute'))

    x_gromos_inout_control_number_of_temperature_groups_for_solute = Quantity(
        type=str,
        shape=[],
        description='''
        gromos running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_gromos_inout_control_number_of_temperature_groups_for_solute'))

    x_gromos_inout_control_number_of_pressure_groups_for_solute = Quantity(
        type=str,
        shape=[],
        description='''
        gromos running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_gromos_inout_control_number_of_pressure_groups_for_solute'))

    x_gromos_inout_control_bond_angle_interaction_in_force_field = Quantity(
        type=str,
        shape=[],
        description='''
        gromos running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_gromos_inout_control_bond_angle_interaction_in_force_field'))

    x_gromos_inout_control_improper_dihedral_interaction_in_force_field = Quantity(
        type=str,
        shape=[],
        description='''
        gromos running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_gromos_inout_control_improper_dihedral_interaction_in_force_field'))

    x_gromos_inout_control_dihedral_interaction_in_force_field = Quantity(
        type=str,
        shape=[],
        description='''
        gromos running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_gromos_inout_control_dihedral_interaction_in_force_field'))

    x_gromos_inout_control_nonbonded_definitions_in_force_field = Quantity(
        type=str,
        shape=[],
        description='''
        gromos running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_gromos_inout_control_nonbonded_definitions_in_force_field'))

    x_gromos_inout_control_pairlist_algorithm = Quantity(
        type=str,
        shape=[],
        description='''
        gromos running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_gromos_inout_control_pairlist_algorithm'))

    x_gromos_inout_control_periodic_boundary_conditions = Quantity(
        type=str,
        shape=[],
        description='''
        gromos running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_gromos_inout_control_periodic_boundary_conditions'))

    x_gromos_inout_control_virial = Quantity(
        type=str,
        shape=[],
        description='''
        gromos running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_gromos_inout_control_virial'))

    x_gromos_inout_control_cutoff_type = Quantity(
        type=str,
        shape=[],
        description='''
        gromos running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_gromos_inout_control_cutoff_type'))

    x_gromos_inout_control_shortrange_cutoff = Quantity(
        type=str,
        shape=[],
        description='''
        gromos running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_gromos_inout_control_shortrange_cutoff'))

    x_gromos_inout_control_longrange_cutoff = Quantity(
        type=str,
        shape=[],
        description='''
        gromos running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_gromos_inout_control_longrange_cutoff'))

    x_gromos_inout_control_pairlist_update_step_frequency = Quantity(
        type=str,
        shape=[],
        description='''
        gromos running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_gromos_inout_control_pairlist_update_step_frequency'))

    x_gromos_inout_control_reactionfield_cutoff = Quantity(
        type=str,
        shape=[],
        description='''
        gromos running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_gromos_inout_control_reactionfield_cutoff'))

    x_gromos_inout_control_force_field_epsilon = Quantity(
        type=str,
        shape=[],
        description='''
        gromos running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_gromos_inout_control_force_field_epsilon'))

    x_gromos_inout_control_reactionfield_epsilon = Quantity(
        type=str,
        shape=[],
        description='''
        gromos running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_gromos_inout_control_reactionfield_epsilon'))

    x_gromos_inout_control_force_field_kappa = Quantity(
        type=str,
        shape=[],
        description='''
        gromos running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_gromos_inout_control_force_field_kappa'))

    x_gromos_inout_control_force_field_perturbation = Quantity(
        type=str,
        shape=[],
        description='''
        gromos running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_gromos_inout_control_force_field_perturbation'))

    x_gromos_inout_control_title = Quantity(
        type=str,
        shape=[],
        description='''
        gromos running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_gromos_inout_control_title'))

    x_gromos_inout_control_emin_ntem = Quantity(
        type=str,
        shape=[],
        description='''
        gromos running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_gromos_inout_control_emin_ntem'))

    x_gromos_inout_control_emin_ncyc = Quantity(
        type=str,
        shape=[],
        description='''
        gromos running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_gromos_inout_control_emin_ncyc'))

    x_gromos_inout_control_emin_dele = Quantity(
        type=str,
        shape=[],
        description='''
        gromos running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_gromos_inout_control_emin_dele'))

    x_gromos_inout_control_emin_dx0 = Quantity(
        type=str,
        shape=[],
        description='''
        gromos running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_gromos_inout_control_emin_dx0'))

    x_gromos_inout_control_emin_dxm = Quantity(
        type=str,
        shape=[],
        description='''
        gromos running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_gromos_inout_control_emin_dxm'))

    x_gromos_inout_control_emin_nmin = Quantity(
        type=str,
        shape=[],
        description='''
        gromos running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_gromos_inout_control_emin_nmin'))

    x_gromos_inout_control_emin_flim = Quantity(
        type=str,
        shape=[],
        description='''
        gromos running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_gromos_inout_control_emin_flim'))

    x_gromos_inout_control_sys_npm = Quantity(
        type=str,
        shape=[],
        description='''
        gromos running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_gromos_inout_control_sys_npm'))

    x_gromos_inout_control_sys_nsm = Quantity(
        type=str,
        shape=[],
        description='''
        gromos running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_gromos_inout_control_sys_nsm'))

    x_gromos_inout_control_init_ntivel = Quantity(
        type=str,
        shape=[],
        description='''
        gromos running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_gromos_inout_control_init_ntivel'))

    x_gromos_inout_control_init_ntishk = Quantity(
        type=str,
        shape=[],
        description='''
        gromos running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_gromos_inout_control_init_ntishk'))

    x_gromos_inout_control_init_ntinht = Quantity(
        type=str,
        shape=[],
        description='''
        gromos running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_gromos_inout_control_init_ntinht'))

    x_gromos_inout_control_init_ntinhb = Quantity(
        type=str,
        shape=[],
        description='''
        gromos running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_gromos_inout_control_init_ntinhb'))

    x_gromos_inout_control_init_ntishi = Quantity(
        type=str,
        shape=[],
        description='''
        gromos running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_gromos_inout_control_init_ntishi'))

    x_gromos_inout_control_init_ntirtc = Quantity(
        type=str,
        shape=[],
        description='''
        gromos running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_gromos_inout_control_init_ntirtc'))

    x_gromos_inout_control_init_nticom = Quantity(
        type=str,
        shape=[],
        description='''
        gromos running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_gromos_inout_control_init_nticom'))

    x_gromos_inout_control_init_ntisti = Quantity(
        type=str,
        shape=[],
        description='''
        gromos running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_gromos_inout_control_init_ntisti'))

    x_gromos_inout_control_init_ig = Quantity(
        type=str,
        shape=[],
        description='''
        gromos running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_gromos_inout_control_init_ig'))

    x_gromos_inout_control_init_tempi = Quantity(
        type=str,
        shape=[],
        description='''
        gromos running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_gromos_inout_control_init_tempi'))

    x_gromos_inout_control_step_nstlim = Quantity(
        type=str,
        shape=[],
        description='''
        gromos running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_gromos_inout_control_step_nstlim'))

    x_gromos_inout_control_step_t = Quantity(
        type=str,
        shape=[],
        description='''
        gromos running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_gromos_inout_control_step_t'))

    x_gromos_inout_control_step_dt = Quantity(
        type=str,
        shape=[],
        description='''
        gromos running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_gromos_inout_control_step_dt'))

    x_gromos_inout_control_bcnd_ntb = Quantity(
        type=str,
        shape=[],
        description='''
        gromos running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_gromos_inout_control_bcnd_ntb'))

    x_gromos_inout_control_bcnd_ndfmin = Quantity(
        type=str,
        shape=[],
        description='''
        gromos running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_gromos_inout_control_bcnd_ndfmin'))

    x_gromos_inout_control_bath_alg = Quantity(
        type=str,
        shape=[],
        description='''
        gromos running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_gromos_inout_control_bath_alg'))

    x_gromos_inout_control_bath_num = Quantity(
        type=str,
        shape=[],
        description='''
        gromos running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_gromos_inout_control_bath_num'))

    x_gromos_inout_control_bath_nbaths = Quantity(
        type=str,
        shape=[],
        description='''
        gromos running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_gromos_inout_control_bath_nbaths'))

    x_gromos_inout_control_bath_temp = Quantity(
        type=str,
        shape=[],
        description='''
        gromos running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_gromos_inout_control_bath_temp'))

    x_gromos_inout_control_bath_tau = Quantity(
        type=str,
        shape=[],
        description='''
        gromos running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_gromos_inout_control_bath_tau'))

    x_gromos_inout_control_bath_dofset = Quantity(
        type=str,
        shape=[],
        description='''
        gromos running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_gromos_inout_control_bath_dofset'))

    x_gromos_inout_control_bath_last = Quantity(
        type=str,
        shape=[],
        description='''
        gromos running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_gromos_inout_control_bath_last'))

    x_gromos_inout_control_bath_combath = Quantity(
        type=str,
        shape=[],
        description='''
        gromos running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_gromos_inout_control_bath_combath'))

    x_gromos_inout_control_bath_irbath = Quantity(
        type=str,
        shape=[],
        description='''
        gromos running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_gromos_inout_control_bath_irbath'))

    x_gromos_inout_control_pres_couple = Quantity(
        type=str,
        shape=[],
        description='''
        gromos running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_gromos_inout_control_pres_couple'))

    x_gromos_inout_control_pres_scale = Quantity(
        type=str,
        shape=[],
        description='''
        gromos running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_gromos_inout_control_pres_scale'))

    x_gromos_inout_control_pres_comp = Quantity(
        type=str,
        shape=[],
        description='''
        gromos running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_gromos_inout_control_pres_comp'))

    x_gromos_inout_control_pres_taup = Quantity(
        type=str,
        shape=[],
        description='''
        gromos running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_gromos_inout_control_pres_taup'))

    x_gromos_inout_control_pres_virial = Quantity(
        type=str,
        shape=[],
        description='''
        gromos running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_gromos_inout_control_pres_virial'))

    x_gromos_inout_control_pres_aniso = Quantity(
        type=str,
        shape=[],
        description='''
        gromos running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_gromos_inout_control_pres_aniso'))

    x_gromos_inout_control_pres_init0 = Quantity(
        type=str,
        shape=[],
        description='''
        gromos running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_gromos_inout_control_pres_init0'))

    x_gromos_inout_control_covf_ntbbh = Quantity(
        type=str,
        shape=[],
        description='''
        gromos running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_gromos_inout_control_covf_ntbbh'))

    x_gromos_inout_control_covf_ntbah = Quantity(
        type=str,
        shape=[],
        description='''
        gromos running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_gromos_inout_control_covf_ntbah'))

    x_gromos_inout_control_covf_ntbdn = Quantity(
        type=str,
        shape=[],
        description='''
        gromos running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_gromos_inout_control_covf_ntbdn'))

    x_gromos_inout_control_solm_nspm = Quantity(
        type=str,
        shape=[],
        description='''
        gromos running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_gromos_inout_control_solm_nspm'))

    x_gromos_inout_control_solm_nsp = Quantity(
        type=str,
        shape=[],
        description='''
        gromos running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_gromos_inout_control_solm_nsp'))

    x_gromos_inout_control_comt_nscm = Quantity(
        type=str,
        shape=[],
        description='''
        gromos running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_gromos_inout_control_comt_nscm'))

    x_gromos_inout_control_prnt_ntpr = Quantity(
        type=str,
        shape=[],
        description='''
        gromos running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_gromos_inout_control_prnt_ntpr'))

    x_gromos_inout_control_prnt_ntpp = Quantity(
        type=str,
        shape=[],
        description='''
        gromos running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_gromos_inout_control_prnt_ntpp'))

    x_gromos_inout_control_writ_ntwx = Quantity(
        type=str,
        shape=[],
        description='''
        gromos running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_gromos_inout_control_writ_ntwx'))

    x_gromos_inout_control_writ_ntwse = Quantity(
        type=str,
        shape=[],
        description='''
        gromos running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_gromos_inout_control_writ_ntwse'))

    x_gromos_inout_control_writ_ntwv = Quantity(
        type=str,
        shape=[],
        description='''
        gromos running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_gromos_inout_control_writ_ntwv'))

    x_gromos_inout_control_writ_ntwf = Quantity(
        type=str,
        shape=[],
        description='''
        gromos running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_gromos_inout_control_writ_ntwf'))

    x_gromos_inout_control_writ_ntwe = Quantity(
        type=str,
        shape=[],
        description='''
        gromos running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_gromos_inout_control_writ_ntwe'))

    x_gromos_inout_control_writ_ntwg = Quantity(
        type=str,
        shape=[],
        description='''
        gromos running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_gromos_inout_control_writ_ntwg'))

    x_gromos_inout_control_writ_ntwb = Quantity(
        type=str,
        shape=[],
        description='''
        gromos running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_gromos_inout_control_writ_ntwb'))

    x_gromos_inout_control_cnst_ntc = Quantity(
        type=str,
        shape=[],
        description='''
        gromos running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_gromos_inout_control_cnst_ntc'))

    x_gromos_inout_control_cnst_ntcp = Quantity(
        type=str,
        shape=[],
        description='''
        gromos running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_gromos_inout_control_cnst_ntcp'))

    x_gromos_inout_control_cnst_ntcp0 = Quantity(
        type=str,
        shape=[],
        description='''
        gromos running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_gromos_inout_control_cnst_ntcp0'))

    x_gromos_inout_control_cnst_ntcs = Quantity(
        type=str,
        shape=[],
        description='''
        gromos running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_gromos_inout_control_cnst_ntcs'))

    x_gromos_inout_control_cnst_ntcs0 = Quantity(
        type=str,
        shape=[],
        description='''
        gromos running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_gromos_inout_control_cnst_ntcs0'))

    x_gromos_inout_control_forc_bonds = Quantity(
        type=str,
        shape=[],
        description='''
        gromos running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_gromos_inout_control_forc_bonds'))

    x_gromos_inout_control_forc_angs = Quantity(
        type=str,
        shape=[],
        description='''
        gromos running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_gromos_inout_control_forc_angs'))

    x_gromos_inout_control_forc_imps = Quantity(
        type=str,
        shape=[],
        description='''
        gromos running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_gromos_inout_control_forc_imps'))

    x_gromos_inout_control_forc_dihs = Quantity(
        type=str,
        shape=[],
        description='''
        gromos running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_gromos_inout_control_forc_dihs'))

    x_gromos_inout_control_forc_elec = Quantity(
        type=str,
        shape=[],
        description='''
        gromos running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_gromos_inout_control_forc_elec'))

    x_gromos_inout_control_forc_vdw = Quantity(
        type=str,
        shape=[],
        description='''
        gromos running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_gromos_inout_control_forc_vdw'))

    x_gromos_inout_control_forc_negr = Quantity(
        type=str,
        shape=[],
        description='''
        gromos running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_gromos_inout_control_forc_negr'))

    x_gromos_inout_control_forc_nre = Quantity(
        type=str,
        shape=[],
        description='''
        gromos running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_gromos_inout_control_forc_nre'))

    x_gromos_inout_control_pair_alg = Quantity(
        type=str,
        shape=[],
        description='''
        gromos running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_gromos_inout_control_pair_alg'))

    x_gromos_inout_control_pair_nsnb = Quantity(
        type=str,
        shape=[],
        description='''
        gromos running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_gromos_inout_control_pair_nsnb'))

    x_gromos_inout_control_pair_rcutp = Quantity(
        type=str,
        shape=[],
        description='''
        gromos running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_gromos_inout_control_pair_rcutp'))

    x_gromos_inout_control_pair_rcutl = Quantity(
        type=str,
        shape=[],
        description='''
        gromos running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_gromos_inout_control_pair_rcutl'))

    x_gromos_inout_control_pair_size = Quantity(
        type=str,
        shape=[],
        description='''
        gromos running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_gromos_inout_control_pair_size'))

    x_gromos_inout_control_pair_type = Quantity(
        type=str,
        shape=[],
        description='''
        gromos running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_gromos_inout_control_pair_type'))

    x_gromos_inout_control_nonb_nlrele = Quantity(
        type=str,
        shape=[],
        description='''
        gromos running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_gromos_inout_control_nonb_nlrele'))

    x_gromos_inout_control_nonb_appak = Quantity(
        type=str,
        shape=[],
        description='''
        gromos running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_gromos_inout_control_nonb_appak'))

    x_gromos_inout_control_nonb_rcrf = Quantity(
        type=str,
        shape=[],
        description='''
        gromos running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_gromos_inout_control_nonb_rcrf'))

    x_gromos_inout_control_nonb_epsrf = Quantity(
        type=str,
        shape=[],
        description='''
        gromos running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_gromos_inout_control_nonb_epsrf'))

    x_gromos_inout_control_nonb_nslfexcl = Quantity(
        type=str,
        shape=[],
        description='''
        gromos running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_gromos_inout_control_nonb_nslfexcl'))

    x_gromos_inout_control_nonb_nshape = Quantity(
        type=str,
        shape=[],
        description='''
        gromos running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_gromos_inout_control_nonb_nshape'))

    x_gromos_inout_control_nonb_ashape = Quantity(
        type=str,
        shape=[],
        description='''
        gromos running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_gromos_inout_control_nonb_ashape'))

    x_gromos_inout_control_nonb_na2clc = Quantity(
        type=str,
        shape=[],
        description='''
        gromos running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_gromos_inout_control_nonb_na2clc'))

    x_gromos_inout_control_nonb_tola2 = Quantity(
        type=str,
        shape=[],
        description='''
        gromos running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_gromos_inout_control_nonb_tola2'))

    x_gromos_inout_control_nonb_epsls = Quantity(
        type=str,
        shape=[],
        description='''
        gromos running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_gromos_inout_control_nonb_epsls'))

    x_gromos_inout_control_nonb_nkx = Quantity(
        type=str,
        shape=[],
        description='''
        gromos running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_gromos_inout_control_nonb_nkx'))

    x_gromos_inout_control_nonb_nky = Quantity(
        type=str,
        shape=[],
        description='''
        gromos running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_gromos_inout_control_nonb_nky'))

    x_gromos_inout_control_nonb_nkz = Quantity(
        type=str,
        shape=[],
        description='''
        gromos running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_gromos_inout_control_nonb_nkz'))

    x_gromos_inout_control_nonb_kcut = Quantity(
        type=str,
        shape=[],
        description='''
        gromos running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_gromos_inout_control_nonb_kcut'))

    x_gromos_inout_control_nonb_ngx = Quantity(
        type=str,
        shape=[],
        description='''
        gromos running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_gromos_inout_control_nonb_ngx'))

    x_gromos_inout_control_nonb_ngy = Quantity(
        type=str,
        shape=[],
        description='''
        gromos running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_gromos_inout_control_nonb_ngy'))

    x_gromos_inout_control_nonb_ngz = Quantity(
        type=str,
        shape=[],
        description='''
        gromos running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_gromos_inout_control_nonb_ngz'))

    x_gromos_inout_control_nonb_nasord = Quantity(
        type=str,
        shape=[],
        description='''
        gromos running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_gromos_inout_control_nonb_nasord'))

    x_gromos_inout_control_nonb_nfdord = Quantity(
        type=str,
        shape=[],
        description='''
        gromos running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_gromos_inout_control_nonb_nfdord'))

    x_gromos_inout_control_nonb_nalias = Quantity(
        type=str,
        shape=[],
        description='''
        gromos running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_gromos_inout_control_nonb_nalias'))

    x_gromos_inout_control_nonb_nspord = Quantity(
        type=str,
        shape=[],
        description='''
        gromos running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_gromos_inout_control_nonb_nspord'))

    x_gromos_inout_control_nonb_nqeval = Quantity(
        type=str,
        shape=[],
        description='''
        gromos running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_gromos_inout_control_nonb_nqeval'))

    x_gromos_inout_control_nonb_faccur = Quantity(
        type=str,
        shape=[],
        description='''
        gromos running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_gromos_inout_control_nonb_faccur'))

    x_gromos_inout_control_nonb_nrdgrd = Quantity(
        type=str,
        shape=[],
        description='''
        gromos running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_gromos_inout_control_nonb_nrdgrd'))

    x_gromos_inout_control_nonb_nwrgrd = Quantity(
        type=str,
        shape=[],
        description='''
        gromos running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_gromos_inout_control_nonb_nwrgrd'))

    x_gromos_inout_control_nonb_nlrlj = Quantity(
        type=str,
        shape=[],
        description='''
        gromos running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_gromos_inout_control_nonb_nlrlj'))

    x_gromos_inout_control_nonb_slvdns = Quantity(
        type=str,
        shape=[],
        description='''
        gromos running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_gromos_inout_control_nonb_slvdns'))

    x_gromos_inout_control_structure_file = Quantity(
        type=str,
        shape=[],
        description='''
        gromos running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_gromos_inout_control_structure_file'))

    x_gromos_inout_control_parameter_file = Quantity(
        type=str,
        shape=[],
        description='''
        gromos running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_gromos_inout_control_parameter_file'))

    x_gromos_inout_control_input_file = Quantity(
        type=str,
        shape=[],
        description='''
        gromos running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_gromos_inout_control_input_file'))

    x_gromos_inout_control_topology_file = Quantity(
        type=str,
        shape=[],
        description='''
        gromos running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_gromos_inout_control_topology_file'))

    x_gromos_inout_control_configuration_file = Quantity(
        type=str,
        shape=[],
        description='''
        gromos running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_gromos_inout_control_configuration_file'))

    x_gromos_inout_control_number_of_parameters = Quantity(
        type=np.dtype(np.int32),
        shape=[],
        description='''
        gromos running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_gromos_inout_control_number_of_parameters'))

    x_gromos_inout_control_parameters = Quantity(
        type=str,
        shape=['x_gromos_inout_control_number_of_parameters'],
        description='''
        gromos running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_gromos_inout_control_parameters'))

    x_gromos_section_input_output_files = SubSection(
        sub_section=SectionProxy('x_gromos_section_input_output_files'),
        repeats=True,
        a_legacy=LegacyDefinition(name='x_gromos_section_input_output_files'))


class x_gromos_section_atom_to_atom_type_ref(MSection):
    '''
    Section to store atom label to atom type definition list
    '''

    m_def = Section(validate=False, a_legacy=LegacyDefinition(name='x_gromos_section_atom_to_atom_type_ref'))

    x_gromos_atom_to_atom_type_ref = Quantity(
        type=np.dtype(np.int64),
        shape=['number_of_atoms_per_type'],
        description='''
        Reference to the atoms of each atom type.
        ''',
        a_legacy=LegacyDefinition(name='x_gromos_atom_to_atom_type_ref'))


class x_gromos_section_single_configuration_calculation(MSection):
    '''
    section for gathering values for MD steps
    '''

    m_def = Section(validate=False, a_legacy=LegacyDefinition(name='x_gromos_section_single_configuration_calculation'))


class section_system(public.section_system):

    m_def = Section(validate=False, extends_base_section=True, a_legacy=LegacyDefinition(name='section_system'))

    x_gromos_atom_positions_image_index = Quantity(
        type=np.dtype(np.int32),
        shape=['number_of_atoms', 3],
        unit='dimensionless',
        description='''
        PBC image flag index.
        ''',
        a_legacy=LegacyDefinition(name='x_gromos_atom_positions_image_index'))

    x_gromos_atom_positions_scaled = Quantity(
        type=np.dtype(np.float64),
        shape=['number_of_atoms', 3],
        unit='dimensionless',
        description='''
        Position of the atoms in a scaled format [0, 1].
        ''',
        a_legacy=LegacyDefinition(name='x_gromos_atom_positions_scaled'))

    x_gromos_atom_positions_wrapped = Quantity(
        type=np.dtype(np.float64),
        shape=['number_of_atoms', 3],
        unit='meter',
        description='''
        Position of the atoms wrapped back to the periodic box.
        ''',
        a_legacy=LegacyDefinition(name='x_gromos_atom_positions_wrapped'))

    x_gromos_lattice_lengths = Quantity(
        type=np.dtype(np.float64),
        shape=[3],
        description='''
        Lattice dimensions in a vector. Vector includes [a, b, c] lengths.
        ''',
        categories=[public.configuration_core],
        a_legacy=LegacyDefinition(name='x_gromos_lattice_lengths'))

    x_gromos_lattice_angles = Quantity(
        type=np.dtype(np.float64),
        shape=[3],
        description='''
        Angles of lattice vectors. Vector includes [alpha, beta, gamma] in degrees.
        ''',
        categories=[public.configuration_core],
        a_legacy=LegacyDefinition(name='x_gromos_lattice_angles'))

    x_gromos_dummy = Quantity(
        type=str,
        shape=[],
        description='''
        dummy
        ''',
        a_legacy=LegacyDefinition(name='x_gromos_dummy'))

    x_gromos_mdin_finline = Quantity(
        type=str,
        shape=[],
        description='''
        finline in mdin
        ''',
        a_legacy=LegacyDefinition(name='x_gromos_mdin_finline'))

    x_gromos_traj_timestep_store = Quantity(
        type=str,
        shape=[],
        description='''
        tmp
        ''',
        a_legacy=LegacyDefinition(name='x_gromos_traj_timestep_store'))

    x_gromos_traj_number_of_atoms_store = Quantity(
        type=str,
        shape=[],
        description='''
        tmp
        ''',
        a_legacy=LegacyDefinition(name='x_gromos_traj_number_of_atoms_store'))

    x_gromos_traj_box_bound_store = Quantity(
        type=str,
        shape=[],
        description='''
        tmp
        ''',
        a_legacy=LegacyDefinition(name='x_gromos_traj_box_bound_store'))

    x_gromos_traj_box_bounds_store = Quantity(
        type=str,
        shape=[],
        description='''
        tmp
        ''',
        a_legacy=LegacyDefinition(name='x_gromos_traj_box_bounds_store'))

    x_gromos_traj_variables_store = Quantity(
        type=str,
        shape=[],
        description='''
        tmp
        ''',
        a_legacy=LegacyDefinition(name='x_gromos_traj_variables_store'))

    x_gromos_traj_atoms_store = Quantity(
        type=str,
        shape=[],
        description='''
        tmp
        ''',
        a_legacy=LegacyDefinition(name='x_gromos_traj_atoms_store'))


class section_sampling_method(public.section_sampling_method):

    m_def = Section(validate=False, extends_base_section=True, a_legacy=LegacyDefinition(name='section_sampling_method'))

    x_gromos_barostat_target_pressure = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        unit='pascal',
        description='''
        MD barostat target pressure.
        ''',
        categories=[public.settings_barostat, public.settings_sampling, public.settings_molecular_dynamics],
        a_legacy=LegacyDefinition(name='x_gromos_barostat_target_pressure'))

    x_gromos_barostat_tau = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        unit='second',
        description='''
        MD barostat relaxation time.
        ''',
        categories=[public.settings_barostat, public.settings_sampling, public.settings_molecular_dynamics],
        a_legacy=LegacyDefinition(name='x_gromos_barostat_tau'))

    x_gromos_barostat_type = Quantity(
        type=str,
        shape=[],
        description='''
        MD barostat type, valid values are defined in the barostat_type wiki page.
        ''',
        categories=[public.settings_barostat, public.settings_sampling, public.settings_molecular_dynamics],
        a_legacy=LegacyDefinition(name='x_gromos_barostat_type'))

    x_gromos_integrator_dt = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        unit='second',
        description='''
        MD integration time step.
        ''',
        categories=[public.settings_sampling, public.settings_molecular_dynamics, public.settings_integrator],
        a_legacy=LegacyDefinition(name='x_gromos_integrator_dt'))

    x_gromos_integrator_type = Quantity(
        type=str,
        shape=[],
        description='''
        MD integrator type, valid values are defined in the integrator_type wiki page.
        ''',
        categories=[public.settings_sampling, public.settings_molecular_dynamics, public.settings_integrator],
        a_legacy=LegacyDefinition(name='x_gromos_integrator_type'))

    x_gromos_periodicity_type = Quantity(
        type=str,
        shape=[],
        description='''
        Periodic boundary condition type in the sampling (non-PBC or PBC).
        ''',
        categories=[public.settings_sampling, public.settings_molecular_dynamics, public.settings_integrator],
        a_legacy=LegacyDefinition(name='x_gromos_periodicity_type'))

    x_gromos_langevin_gamma = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        unit='second',
        description='''
        Langevin thermostat damping factor.
        ''',
        categories=[public.settings_thermostat, public.settings_sampling, public.settings_molecular_dynamics],
        a_legacy=LegacyDefinition(name='x_gromos_langevin_gamma'))

    x_gromos_number_of_steps_requested = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        description='''
        Number of requested MD integration time steps.
        ''',
        categories=[public.settings_sampling, public.settings_molecular_dynamics, public.settings_integrator],
        a_legacy=LegacyDefinition(name='x_gromos_number_of_steps_requested'))

    x_gromos_thermostat_level = Quantity(
        type=str,
        shape=[],
        description='''
        MD thermostat level (see wiki: single, multiple, regional).
        ''',
        categories=[public.settings_thermostat, public.settings_sampling, public.settings_molecular_dynamics],
        a_legacy=LegacyDefinition(name='x_gromos_thermostat_level'))

    x_gromos_thermostat_target_temperature = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        unit='kelvin',
        description='''
        MD thermostat target temperature.
        ''',
        categories=[public.settings_thermostat, public.settings_sampling, public.settings_molecular_dynamics],
        a_legacy=LegacyDefinition(name='x_gromos_thermostat_target_temperature'))

    x_gromos_thermostat_tau = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        unit='second',
        description='''
        MD thermostat relaxation time.
        ''',
        categories=[public.settings_thermostat, public.settings_sampling, public.settings_molecular_dynamics],
        a_legacy=LegacyDefinition(name='x_gromos_thermostat_tau'))

    x_gromos_thermostat_type = Quantity(
        type=str,
        shape=[],
        description='''
        MD thermostat type, valid values are defined in the thermostat_type wiki page.
        ''',
        categories=[public.settings_thermostat, public.settings_sampling, public.settings_molecular_dynamics],
        a_legacy=LegacyDefinition(name='x_gromos_thermostat_type'))


class section_atom_type(common.section_atom_type):

    m_def = Section(validate=False, extends_base_section=True, a_legacy=LegacyDefinition(name='section_atom_type'))

    x_gromos_atom_name = Quantity(
        type=str,
        shape=[],
        description='''
        Atom name of an atom in topology definition.
        ''',
        a_legacy=LegacyDefinition(name='x_gromos_atom_name'))

    x_gromos_atom_type = Quantity(
        type=str,
        shape=[],
        description='''
        Atom type of an atom in topology definition.
        ''',
        a_legacy=LegacyDefinition(name='x_gromos_atom_type'))

    x_gromos_atom_element = Quantity(
        type=str,
        shape=[],
        description='''
        Atom type of an atom in topology definition.
        ''',
        a_legacy=LegacyDefinition(name='x_gromos_atom_element'))

    x_gromos_atom_type_element = Quantity(
        type=str,
        shape=[],
        description='''
        Element symbol of an atom type.
        ''',
        a_legacy=LegacyDefinition(name='x_gromos_atom_type_element'))

    x_gromos_atom_type_radius = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        description='''
        van der Waals radius of an atom type.
        ''',
        a_legacy=LegacyDefinition(name='x_gromos_atom_type_radius'))

    number_of_atoms_per_type = Quantity(
        type=int,
        shape=[],
        description='''
        Number of atoms involved in this type.
        ''',
        a_legacy=LegacyDefinition(name='number_of_atoms_per_type'))


class section_interaction(common.section_interaction):

    m_def = Section(validate=False, extends_base_section=True, a_legacy=LegacyDefinition(name='section_interaction'))

    x_gromos_interaction_atom_to_atom_type_ref = Quantity(
        type=common.section_atom_type,
        shape=['number_of_atoms_per_interaction'],
        description='''
        Reference to the atom type of each interaction atoms.
        ''',
        a_legacy=LegacyDefinition(name='x_gromos_interaction_atom_to_atom_type_ref'))

    x_gromos_number_of_defined_pair_interactions = Quantity(
        type=np.dtype(np.int32),
        shape=[],
        description='''
        Number of defined pair interactions (L-J pairs).
        ''',
        a_legacy=LegacyDefinition(name='x_gromos_number_of_defined_pair_interactions'))

    x_gromos_pair_interaction_atom_type_ref = Quantity(
        type=common.section_atom_type,
        shape=['x_gromos_number_of_defined_pair_interactions', 'number_of_atoms_per_interaction'],
        description='''
        Reference to the atom type for pair interactions.
        ''',
        a_legacy=LegacyDefinition(name='x_gromos_pair_interaction_atom_type_ref'))

    x_gromos_pair_interaction_parameters = Quantity(
        type=np.dtype(np.float64),
        shape=['x_gromos_number_of_defined_pair_interactions', 2],
        description='''
        Pair interactions parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_gromos_pair_interaction_parameters'))


class section_molecule_interaction(common.section_molecule_interaction):

    m_def = Section(validate=False, extends_base_section=True, a_legacy=LegacyDefinition(name='section_molecule_interaction'))

    x_gromos_molecule_interaction_atom_to_atom_type_ref = Quantity(
        type=common.section_atom_type,
        shape=['number_of_atoms_per_interaction'],
        description='''
        Reference to the atom type of each molecule interaction atoms.
        ''',
        a_legacy=LegacyDefinition(name='x_gromos_molecule_interaction_atom_to_atom_type_ref'))

    x_gromos_number_of_defined_molecule_pair_interactions = Quantity(
        type=np.dtype(np.int32),
        shape=[],
        description='''
        Number of defined pair interactions within a molecule (L-J pairs).
        ''',
        a_legacy=LegacyDefinition(name='x_gromos_number_of_defined_molecule_pair_interactions'))

    x_gromos_pair_molecule_interaction_parameters = Quantity(
        type=np.dtype(np.float64),
        shape=['number_of_defined_molecule_pair_interactions', 2],
        description='''
        Molecule pair interactions parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_gromos_pair_molecule_interaction_parameters'))

    x_gromos_pair_molecule_interaction_to_atom_type_ref = Quantity(
        type=common.section_atom_type,
        shape=['x_gromos_number_of_defined_pair_interactions', 'number_of_atoms_per_interaction'],
        description='''
        Reference to the atom type for pair interactions within a molecule.
        ''',
        a_legacy=LegacyDefinition(name='x_gromos_pair_molecule_interaction_to_atom_type_ref'))


class section_run(public.section_run):

    m_def = Section(validate=False, extends_base_section=True, a_legacy=LegacyDefinition(name='section_run'))

    x_gromos_program_version_date = Quantity(
        type=str,
        shape=[],
        description='''
        Program version date.
        ''',
        a_legacy=LegacyDefinition(name='x_gromos_program_version_date'))

    x_gromos_parallel_task_nr = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        description='''
        Program task no.
        ''',
        a_legacy=LegacyDefinition(name='x_gromos_parallel_task_nr'))

    x_gromos_build_osarch = Quantity(
        type=str,
        shape=[],
        description='''
        Program Build OS/ARCH
        ''',
        a_legacy=LegacyDefinition(name='x_gromos_build_osarch'))

    x_gromos_output_created_by_user = Quantity(
        type=str,
        shape=[],
        description='''
        Output file creator
        ''',
        a_legacy=LegacyDefinition(name='x_gromos_output_created_by_user'))

    x_gromos_most_severe_warning_level = Quantity(
        type=str,
        shape=[],
        description='''
        Highest gromos warning level in the run.
        ''',
        a_legacy=LegacyDefinition(name='x_gromos_most_severe_warning_level'))

    x_gromos_program_build_date = Quantity(
        type=str,
        shape=[],
        description='''
        Program Build date
        ''',
        a_legacy=LegacyDefinition(name='x_gromos_program_build_date'))

    x_gromos_program_citation = Quantity(
        type=str,
        shape=[],
        description='''
        Program citations
        ''',
        a_legacy=LegacyDefinition(name='x_gromos_program_citation'))

    x_gromos_program_copyright = Quantity(
        type=str,
        shape=[],
        description='''
        Program copyright
        ''',
        a_legacy=LegacyDefinition(name='x_gromos_program_copyright'))

    x_gromos_number_of_tasks = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        description='''
        Number of tasks in parallel program (MPI).
        ''',
        a_legacy=LegacyDefinition(name='x_gromos_number_of_tasks'))

    x_gromos_program_module_version = Quantity(
        type=str,
        shape=[],
        description='''
        gromos program module version.
        ''',
        a_legacy=LegacyDefinition(name='x_gromos_program_module_version'))

    x_gromos_program_license = Quantity(
        type=str,
        shape=[],
        description='''
        gromos program license.
        ''',
        a_legacy=LegacyDefinition(name='x_gromos_program_license'))

    x_gromos_xlo_xhi = Quantity(
        type=str,
        shape=[],
        description='''
        test
        ''',
        a_legacy=LegacyDefinition(name='x_gromos_xlo_xhi'))

    x_gromos_data_file_store = Quantity(
        type=str,
        shape=[],
        description='''
        Filename of data file
        ''',
        a_legacy=LegacyDefinition(name='x_gromos_data_file_store'))

    x_gromos_program_working_path = Quantity(
        type=str,
        shape=[],
        description='''
        tmp
        ''',
        a_legacy=LegacyDefinition(name='x_gromos_program_working_path'))

    x_gromos_program_execution_host = Quantity(
        type=str,
        shape=[],
        description='''
        tmp
        ''',
        a_legacy=LegacyDefinition(name='x_gromos_program_execution_host'))

    x_gromos_program_execution_path = Quantity(
        type=str,
        shape=[],
        description='''
        tmp
        ''',
        a_legacy=LegacyDefinition(name='x_gromos_program_execution_path'))

    x_gromos_program_module = Quantity(
        type=str,
        shape=[],
        description='''
        tmp
        ''',
        a_legacy=LegacyDefinition(name='x_gromos_program_module'))

    x_gromos_program_execution_date = Quantity(
        type=str,
        shape=[],
        description='''
        tmp
        ''',
        a_legacy=LegacyDefinition(name='x_gromos_program_execution_date'))

    x_gromos_program_execution_time = Quantity(
        type=str,
        shape=[],
        description='''
        tmp
        ''',
        a_legacy=LegacyDefinition(name='x_gromos_program_execution_time'))

    x_gromos_mdin_header = Quantity(
        type=str,
        shape=[],
        description='''
        tmp
        ''',
        a_legacy=LegacyDefinition(name='x_gromos_mdin_header'))

    x_gromos_mdin_wt = Quantity(
        type=str,
        shape=[],
        description='''
        tmp
        ''',
        a_legacy=LegacyDefinition(name='x_gromos_mdin_wt'))

    x_gromos_section_control_parameters = SubSection(
        sub_section=SectionProxy('x_gromos_section_control_parameters'),
        repeats=True,
        a_legacy=LegacyDefinition(name='x_gromos_section_control_parameters'))


class section_topology(common.section_topology):

    m_def = Section(validate=False, extends_base_section=True, a_legacy=LegacyDefinition(name='section_topology'))

    x_gromos_input_units_store = Quantity(
        type=str,
        shape=[],
        description='''
        It determines the units of all quantities specified in the input script and data
        file, as well as quantities output to the screen, log file, and dump files.
        ''',
        a_legacy=LegacyDefinition(name='x_gromos_input_units_store'))

    x_gromos_data_bond_types_store = Quantity(
        type=np.dtype(np.int32),
        shape=[],
        description='''
        store temporarly
        ''',
        a_legacy=LegacyDefinition(name='x_gromos_data_bond_types_store'))

    x_gromos_data_bond_count_store = Quantity(
        type=np.dtype(np.int32),
        shape=[],
        description='''
        store temporarly
        ''',
        a_legacy=LegacyDefinition(name='x_gromos_data_bond_count_store'))

    x_gromos_data_angle_count_store = Quantity(
        type=np.dtype(np.int32),
        shape=[],
        description='''
        store temporarly
        ''',
        a_legacy=LegacyDefinition(name='x_gromos_data_angle_count_store'))

    x_gromos_data_atom_types_store = Quantity(
        type=np.dtype(np.int32),
        shape=[],
        description='''
        store temporarly
        ''',
        a_legacy=LegacyDefinition(name='x_gromos_data_atom_types_store'))

    x_gromos_data_dihedral_count_store = Quantity(
        type=np.dtype(np.int32),
        shape=[],
        description='''
        store temporarly
        ''',
        a_legacy=LegacyDefinition(name='x_gromos_data_dihedral_count_store'))

    x_gromos_data_angles_store = Quantity(
        type=str,
        shape=[],
        description='''
        store temporarly
        ''',
        a_legacy=LegacyDefinition(name='x_gromos_data_angles_store'))

    x_gromos_data_angle_list_store = Quantity(
        type=str,
        shape=[],
        description='''
        tmp
        ''',
        a_legacy=LegacyDefinition(name='x_gromos_data_angle_list_store'))

    x_gromos_data_bond_list_store = Quantity(
        type=str,
        shape=[],
        description='''
        tmp
        ''',
        a_legacy=LegacyDefinition(name='x_gromos_data_bond_list_store'))

    x_gromos_data_dihedral_list_store = Quantity(
        type=str,
        shape=[],
        description='''
        tmp
        ''',
        a_legacy=LegacyDefinition(name='x_gromos_data_dihedral_list_store'))

    x_gromos_data_dihedral_coeff_list_store = Quantity(
        type=str,
        shape=[],
        description='''
        tmp
        ''',
        a_legacy=LegacyDefinition(name='x_gromos_data_dihedral_coeff_list_store'))

    x_gromos_masses_store = Quantity(
        type=str,
        shape=[],
        description='''
        tmp
        ''',
        a_legacy=LegacyDefinition(name='x_gromos_masses_store'))

    x_gromos_data_topo_list_store = Quantity(
        type=str,
        shape=[],
        description='''
        tmp
        ''',
        a_legacy=LegacyDefinition(name='x_gromos_data_topo_list_store'))

    x_gromos_section_atom_to_atom_type_ref = SubSection(
        sub_section=SectionProxy('x_gromos_section_atom_to_atom_type_ref'),
        repeats=True,
        a_legacy=LegacyDefinition(name='x_gromos_section_atom_to_atom_type_ref'))


class section_frame_sequence(public.section_frame_sequence):

    m_def = Section(validate=False, extends_base_section=True, a_legacy=LegacyDefinition(name='section_frame_sequence'))

    x_gromos_number_of_volumes_in_sequence = Quantity(
        type=int,
        shape=[],
        description='''
        Gives the number of volumes in this sequence of frames, see
        x_gromos_frame_sequence_volume.
        ''',
        a_legacy=LegacyDefinition(name='x_gromos_number_of_volumes_in_sequence'))

    x_gromos_number_of_densities_in_sequence = Quantity(
        type=int,
        shape=[],
        description='''
        Gives the number of densities in this sequence of frames, see
        x_gromos_frame_sequence_density.
        ''',
        a_legacy=LegacyDefinition(name='x_gromos_number_of_densities_in_sequence'))

    x_gromos_number_of_bond_energies_in_sequence = Quantity(
        type=int,
        shape=[],
        description='''
        Gives the number of bond_energies in this sequence of frames, see
        x_gromos_frame_sequence_bond_energy.
        ''',
        a_legacy=LegacyDefinition(name='x_gromos_number_of_bond_energies_in_sequence'))

    x_gromos_number_of_virial_energies_in_sequence = Quantity(
        type=int,
        shape=[],
        description='''
        Gives the number of bond_energies in this sequence of frames, see
        x_gromos_frame_sequence_virial_energy.
        ''',
        a_legacy=LegacyDefinition(name='x_gromos_number_of_virial_energies_in_sequence'))

    x_gromos_number_of_angle_energies_in_sequence = Quantity(
        type=int,
        shape=[],
        description='''
        Gives the number of angle_energies in this sequence of frames, see
        x_gromos_frame_sequence_angle_energy.
        ''',
        a_legacy=LegacyDefinition(name='x_gromos_number_of_angle_energies_in_sequence'))

    x_gromos_number_of_proper_dihedral_energies_in_sequence = Quantity(
        type=int,
        shape=[],
        description='''
        Gives the number of proper_dihedral_energies in this sequence of frames, see
        x_gromos_frame_sequence_proper_dihedral_energy.
        ''',
        a_legacy=LegacyDefinition(name='x_gromos_number_of_proper_dihedral_energies_in_sequence'))

    x_gromos_number_of_improper_dihedral_energies_in_sequence = Quantity(
        type=int,
        shape=[],
        description='''
        Gives the number of improper_dihedral_energies in this sequence of frames, see
        x_gromos_frame_sequence_improper_dihedral_energy.
        ''',
        a_legacy=LegacyDefinition(name='x_gromos_number_of_improper_dihedral_energies_in_sequence'))

    x_gromos_number_of_cross_dihedral_energies_in_sequence = Quantity(
        type=int,
        shape=[],
        description='''
        Gives the number of cross_dihedral_energies in this sequence of frames, see
        x_gromos_frame_sequence_cross_dihedral_energy.
        ''',
        a_legacy=LegacyDefinition(name='x_gromos_number_of_cross_dihedral_energies_in_sequence'))

    x_gromos_number_of_vdw_energies_in_sequence = Quantity(
        type=int,
        shape=[],
        description='''
        Gives the number of vdw_energies in this sequence of frames, see
        x_gromos_frame_sequence_vdw_energy.
        ''',
        a_legacy=LegacyDefinition(name='x_gromos_number_of_vdw_energies_in_sequence'))

    x_gromos_number_of_boundary_energies_in_sequence = Quantity(
        type=int,
        shape=[],
        description='''
        Gives the number of boundary_energies in this sequence of frames, see
        x_gromos_frame_sequence_boundary_energy.
        ''',
        a_legacy=LegacyDefinition(name='x_gromos_number_of_boundary_energies_in_sequence'))

    x_gromos_number_of_electrostatic_energies_in_sequence = Quantity(
        type=int,
        shape=[],
        description='''
        Gives the number of electrostatic_energies in this sequence of frames, see
        x_gromos_frame_sequence_electrostatic_energy.
        ''',
        a_legacy=LegacyDefinition(name='x_gromos_number_of_electrostatic_energies_in_sequence'))

    x_gromos_number_of_total_energies_in_sequence = Quantity(
        type=int,
        shape=[],
        description='''
        Gives the number of total_energies in this sequence of frames, see
        x_gromos_frame_sequence_total_energy.
        ''',
        a_legacy=LegacyDefinition(name='x_gromos_number_of_total_energies_in_sequence'))

    x_gromos_number_of_total_kinetic_energies_in_sequence = Quantity(
        type=int,
        shape=[],
        description='''
        Gives the number of total_kinetic_energies in this sequence of frames, see
        x_gromos_frame_sequence_total_kinetic_energy_frames.
        ''',
        a_legacy=LegacyDefinition(name='x_gromos_number_of_total_kinetic_energies_in_sequence'))

    x_gromos_number_of_covalent_energies_in_sequence = Quantity(
        type=int,
        shape=[],
        description='''
        Gives the number of covalent_energies in this sequence of frames, see
        x_gromos_frame_sequence_covalent_energy.
        ''',
        a_legacy=LegacyDefinition(name='x_gromos_number_of_covalent_energies_in_sequence'))

    x_gromos_number_of_misc_energies_in_sequence = Quantity(
        type=int,
        shape=[],
        description='''
        Gives the number of misc_energies in this sequence of frames, see
        x_gromos_frame_sequence_misc_energy.
        ''',
        a_legacy=LegacyDefinition(name='x_gromos_number_of_misc_energies_in_sequence'))

    x_gromos_frame_sequence_density_frames = Quantity(
        type=np.dtype(np.int32),
        shape=['x_gromos_number_of_densities_in_sequence'],
        description='''
        Array containing the strictly increasing indices of the frames the
        x_gromos_frame_sequence_densities values refers to. If not given it defaults to
        the trivial mapping 0,1,...
        ''',
        a_legacy=LegacyDefinition(name='x_gromos_frame_sequence_density_frames'))

    x_gromos_frame_sequence_density = Quantity(
        type=np.dtype(np.float64),
        shape=['x_gromos_number_of_densities_in_sequence'],
        description='''
        Array containing the values of the density along this sequence of frames (i.e., a
        trajectory, a frame is one section_single_configuration_calculation). If not all
        frames have a value the indices of the frames that have a value are stored in
        frame_sequence_density_frames.
        ''',
        a_legacy=LegacyDefinition(name='x_gromos_frame_sequence_density'))

    x_gromos_frame_sequence_cross_dihedral_energy_frames = Quantity(
        type=np.dtype(np.int32),
        shape=['x_gromos_number_of_cross_dihedral_energy_in_sequence'],
        description='''
        Array containing the strictly increasing indices of the frames the
        x_gromos_frame_sequence_cross_dihedral_energy values refers to. If not given it
        defaults to the trivial mapping 0,1,...
        ''',
        a_legacy=LegacyDefinition(name='x_gromos_frame_sequence_cross_dihedral_energy_frames'))

    x_gromos_frame_sequence_cross_dihedral_energy = Quantity(
        type=np.dtype(np.float64),
        shape=['x_gromos_number_of_cross_dihedral_energy_in_sequence'],
        description='''
        Array containing the values of the cross_dihedral_energy along this sequence of
        frames (i.e., a trajectory, a frame is one
        section_single_configuration_calculation). If not all frames have a value the
        indices of the frames that have a value are stored in
        frame_sequence_cross_dihedral_energy_frames.
        ''',
        a_legacy=LegacyDefinition(name='x_gromos_frame_sequence_cross_dihedral_energy'))

    x_gromos_frame_sequence_improper_dihedral_energy_frames = Quantity(
        type=np.dtype(np.int32),
        shape=['x_gromos_number_of_improper_dihedral_energy_in_sequence'],
        description='''
        Array containing the strictly increasing indices of the frames the
        x_gromos_frame_sequence_improper_dihedral_energy values refers to. If not given it
        defaults to the trivial mapping 0,1,...
        ''',
        a_legacy=LegacyDefinition(name='x_gromos_frame_sequence_improper_dihedral_energy_frames'))

    x_gromos_frame_sequence_improper_dihedral_energy = Quantity(
        type=np.dtype(np.float64),
        shape=['x_gromos_number_of_improper_dihedral_energy_in_sequence'],
        description='''
        Array containing the values of the improper_dihedral_energy along this sequence of
        frames (i.e., a trajectory, a frame is one
        section_single_configuration_calculation). If not all frames have a value the
        indices of the frames that have a value are stored in
        frame_sequence_improper_dihedral_energy_frames.
        ''',
        a_legacy=LegacyDefinition(name='x_gromos_frame_sequence_improper_dihedral_energy'))

    x_gromos_frame_sequence_proper_dihedral_energy_frames = Quantity(
        type=np.dtype(np.int32),
        shape=['x_gromos_number_of_proper_dihedral_energy_in_sequence'],
        description='''
        Array containing the strictly increasing indices of the frames the
        x_gromos_frame_sequence_proper_dihedral_energy values refers to. If not given it
        defaults to the trivial mapping 0,1,...
        ''',
        a_legacy=LegacyDefinition(name='x_gromos_frame_sequence_proper_dihedral_energy_frames'))

    x_gromos_frame_sequence_proper_dihedral_energy = Quantity(
        type=np.dtype(np.float64),
        shape=['x_gromos_number_of_proper_dihedral_energy_in_sequence'],
        description='''
        Array containing the values of the proper_dihedral_energy along this sequence of
        frames (i.e., a trajectory, a frame is one
        section_single_configuration_calculation). If not all frames have a value the
        indices of the frames that have a value are stored in
        frame_sequence_proper_dihedral_energy_frames.
        ''',
        a_legacy=LegacyDefinition(name='x_gromos_frame_sequence_proper_dihedral_energy'))

    x_gromos_frame_sequence_bond_energy_frames = Quantity(
        type=np.dtype(np.int32),
        shape=['x_gromos_number_of_bond_energies_in_sequence'],
        description='''
        Array containing the strictly increasing indices of the frames the
        x_gromos_frame_sequence_bond_energy values refers to. If not given it defaults to
        the trivial mapping 0,1,...
        ''',
        a_legacy=LegacyDefinition(name='x_gromos_frame_sequence_bond_energy_frames'))

    x_gromos_frame_sequence_virial_energy_frames = Quantity(
        type=np.dtype(np.int32),
        shape=['x_gromos_number_of_virial_energies_in_sequence'],
        description='''
        Array containing the strictly increasing indices of the frames the
        x_gromos_frame_sequence_virial_energy values refers to. If not given it defaults
        to the trivial mapping 0,1,...
        ''',
        a_legacy=LegacyDefinition(name='x_gromos_frame_sequence_virial_energy_frames'))

    x_gromos_frame_sequence_bond_energy = Quantity(
        type=np.dtype(np.float64),
        shape=['x_gromos_number_of_bond_energies_in_sequence'],
        description='''
        Array containing the values of the bond_energy along this sequence of frames
        (i.e., a trajectory, a frame is one section_single_configuration_calculation). If
        not all frames have a value the indices of the frames that have a value are stored
        in frame_sequence_bond_energy_frames.
        ''',
        a_legacy=LegacyDefinition(name='x_gromos_frame_sequence_bond_energy'))

    x_gromos_frame_sequence_virial_energy = Quantity(
        type=np.dtype(np.float64),
        shape=['x_gromos_number_of_virial_energies_in_sequence'],
        description='''
        Array containing the values of the virial_energy along this sequence of frames
        (i.e., a trajectory, a frame is one section_single_configuration_calculation). If
        not all frames have a value the indices of the frames that have a value are stored
        in frame_sequence_virial_energy_frames.
        ''',
        a_legacy=LegacyDefinition(name='x_gromos_frame_sequence_virial_energy'))

    x_gromos_frame_sequence_boundary_frames = Quantity(
        type=np.dtype(np.int32),
        shape=['x_gromos_number_of_boundary_energies_in_sequence'],
        description='''
        Array containing the strictly increasing indices of the frames the
        x_gromos_frame_sequence_boundary values refers to. If not given it defaults to the
        trivial mapping 0,1,...
        ''',
        a_legacy=LegacyDefinition(name='x_gromos_frame_sequence_boundary_frames'))

    x_gromos_frame_sequence_boundary = Quantity(
        type=np.dtype(np.float64),
        shape=['x_gromos_number_of_boundary_energies_in_sequence'],
        description='''
        Array containing the values of the boundary along this sequence of frames (i.e., a
        trajectory, a frame is one section_single_configuration_calculation). If not all
        frames have a value the indices of the frames that have a value are stored in
        frame_sequence_boundary_frames.
        ''',
        a_legacy=LegacyDefinition(name='x_gromos_frame_sequence_boundary'))

    x_gromos_frame_sequence_angle_energy_frames = Quantity(
        type=np.dtype(np.int32),
        shape=['x_gromos_number_of_angle_energies_in_sequence'],
        description='''
        Array containing the strictly increasing indices of the frames the
        x_gromos_frame_sequence_angle_energy values refers to. If not given it defaults to
        the trivial mapping 0,1,...
        ''',
        a_legacy=LegacyDefinition(name='x_gromos_frame_sequence_angle_energy_frames'))

    x_gromos_frame_sequence_angle_energy = Quantity(
        type=np.dtype(np.float64),
        shape=['x_gromos_number_of_angle_energies_in_sequence'],
        description='''
        Array containing the values of the angle_energy along this sequence of frames
        (i.e., a trajectory, a frame is one section_single_configuration_calculation). If
        not all frames have a value the indices of the frames that have a value are stored
        in frame_sequence_angle_energy_frames.
        ''',
        a_legacy=LegacyDefinition(name='x_gromos_frame_sequence_angle_energy'))

    x_gromos_frame_sequence_vdw_energy_frames = Quantity(
        type=np.dtype(np.int32),
        shape=['x_gromos_number_of_vdw_energies_in_sequence'],
        description='''
        Array containing the strictly increasing indices of the frames the
        x_gromos_frame_sequence_vdw_energy values refers to. If not given it defaults to
        the trivial mapping 0,1,...
        ''',
        a_legacy=LegacyDefinition(name='x_gromos_frame_sequence_vdw_energy_frames'))

    x_gromos_frame_sequence_vdw_energy = Quantity(
        type=np.dtype(np.float64),
        shape=['x_gromos_number_of_vdw_energies_in_sequence'],
        description='''
        Array containing the values of the vdw_energy along this sequence of frames (i.e.,
        a trajectory, a frame is one section_single_configuration_calculation). If not all
        frames have a value the indices of the frames that have a value are stored in
        frame_sequence_vdw_energy_frames.
        ''',
        a_legacy=LegacyDefinition(name='x_gromos_frame_sequence_vdw_energy'))

    x_gromos_frame_sequence_electrostatic_energy_frames = Quantity(
        type=np.dtype(np.int32),
        shape=['x_gromos_number_of_electrostatic_energies_in_sequence'],
        description='''
        Array containing the strictly increasing indices of the frames the
        x_gromos_frame_sequence_electrostatic_energy values refers to. If not given it
        defaults to the trivial mapping 0,1,...
        ''',
        a_legacy=LegacyDefinition(name='x_gromos_frame_sequence_electrostatic_energy_frames'))

    x_gromos_frame_sequence_electrostatic_energy = Quantity(
        type=np.dtype(np.float64),
        shape=['x_gromos_number_of_electrostatic_energies_in_sequence'],
        description='''
        Array containing the values of the electrostatic_energy along this sequence of
        frames (i.e., a trajectory, a frame is one
        section_single_configuration_calculation). If not all frames have a value the
        indices of the frames that have a value are stored in
        frame_sequence_electrostatic_energy_frames.
        ''',
        a_legacy=LegacyDefinition(name='x_gromos_frame_sequence_electrostatic_energy'))

    x_gromos_frame_sequence_total_energy_frames = Quantity(
        type=np.dtype(np.int32),
        shape=['x_gromos_number_of_total_energies_in_sequence'],
        description='''
        Array containing the strictly increasing indices of the frames the
        x_gromos_frame_sequence_total_energy values refers to. If not given it defaults to
        the trivial mapping 0,1,...
        ''',
        a_legacy=LegacyDefinition(name='x_gromos_frame_sequence_total_energy_frames'))

    x_gromos_frame_sequence_total_energy = Quantity(
        type=np.dtype(np.float64),
        shape=['x_gromos_number_of_total_energies_in_sequence'],
        description='''
        Array containing the values of the total_energy along this sequence of frames
        (i.e., a trajectory, a frame is one section_single_configuration_calculation). If
        not all frames have a value the indices of the frames that have a value are stored
        in frame_sequence_total_energy_frames.
        ''',
        a_legacy=LegacyDefinition(name='x_gromos_frame_sequence_total_energy'))

    x_gromos_frame_sequence_total_kinetic_energy_frames = Quantity(
        type=np.dtype(np.int32),
        shape=['x_gromos_number_of_total_kinetic_energies_in_sequence'],
        description='''
        Array containing the strictly increasing indices of the frames the
        x_gromos_frame_sequence_total_kinetic_energy values refers to. If not given it
        defaults to the trivial mapping 0,1,...
        ''',
        a_legacy=LegacyDefinition(name='x_gromos_frame_sequence_total_kinetic_energy_frames'))

    x_gromos_frame_sequence_total_kinetic_energy = Quantity(
        type=np.dtype(np.float64),
        shape=['x_gromos_number_of_total_kinetic_energies_in_sequence'],
        description='''
        Array containing the values of the total_kinetic_energy along this sequence of
        frames (i.e., a trajectory, a frame is one
        section_single_configuration_calculation). If not all frames have a value the
        indices of the frames that have a value are stored in
        frame_sequence_total_kinetic_energy_frames.
        ''',
        a_legacy=LegacyDefinition(name='x_gromos_frame_sequence_total_kinetic_energy'))

    x_gromos_frame_sequence_misc_energy_frames = Quantity(
        type=np.dtype(np.int32),
        shape=['x_gromos_number_of_misc_energies_in_sequence'],
        description='''
        Array containing the strictly increasing indices of the frames the
        x_gromos_frame_sequence_misc_energy values refers to. If not given it defaults to
        the trivial mapping 0,1,...
        ''',
        a_legacy=LegacyDefinition(name='x_gromos_frame_sequence_misc_energy_frames'))

    x_gromos_frame_sequence_covalent_energy_frames = Quantity(
        type=np.dtype(np.int32),
        shape=['x_gromos_number_of_covalent_energies_in_sequence'],
        description='''
        Array containing the strictly increasing indices of the frames the
        x_gromos_frame_sequence_covalent_energy values refers to. If not given it defaults
        to the trivial mapping 0,1,...
        ''',
        a_legacy=LegacyDefinition(name='x_gromos_frame_sequence_covalent_energy_frames'))

    x_gromos_frame_sequence_covalent_energy = Quantity(
        type=np.dtype(np.float64),
        shape=['x_gromos_number_of_covalent_energies_in_sequence'],
        description='''
        Array containing the values of the covalent_energy along this sequence of frames
        (i.e., a trajectory, a frame is one section_single_configuration_calculation). If
        not all frames have a value the indices of the frames that have a value are stored
        in frame_sequence_covalent_energy_frames.
        ''',
        a_legacy=LegacyDefinition(name='x_gromos_frame_sequence_covalent_energy'))

    x_gromos_frame_sequence_misc_energy = Quantity(
        type=np.dtype(np.float64),
        shape=['x_gromos_number_of_misc_energies_in_sequence'],
        description='''
        Array containing the values of the misc_energy along this sequence of frames
        (i.e., a trajectory, a frame is one section_single_configuration_calculation). If
        not all frames have a value the indices of the frames that have a value are stored
        in frame_sequence_misc_energy_frames.
        ''',
        a_legacy=LegacyDefinition(name='x_gromos_frame_sequence_misc_energy'))

    x_gromos_frame_sequence_volume_frames = Quantity(
        type=np.dtype(np.int32),
        shape=['x_gromos_number_of_volumes_in_sequence'],
        description='''
        Array containing the strictly increasing indices of the frames the
        x_gromos_frame_sequence_volume values refers to. If not given it defaults to the
        trivial mapping 0,1,...
        ''',
        a_legacy=LegacyDefinition(name='x_gromos_frame_sequence_volume_frames'))

    x_gromos_frame_sequence_volume = Quantity(
        type=np.dtype(np.float64),
        shape=['x_gromos_number_of_volumes_in_sequence'],
        description='''
        Array containing the values of the volume along this sequence of frames (i.e., a
        trajectory, a frame is one section_single_configuration_calculation). If not all
        frames have a value the indices of the frames that have a value are stored in
        frame_sequence_volume_frames.
        ''',
        a_legacy=LegacyDefinition(name='x_gromos_frame_sequence_volume'))


class section_single_configuration_calculation(public.section_single_configuration_calculation):

    m_def = Section(validate=False, extends_base_section=True, a_legacy=LegacyDefinition(name='section_single_configuration_calculation'))

    x_gromos_section_single_configuration_calculation = SubSection(
        sub_section=SectionProxy('x_gromos_section_single_configuration_calculation'),
        repeats=True,
        a_legacy=LegacyDefinition(name='x_gromos_section_single_configuration_calculation'))


m_package.__init_metainfo__()
