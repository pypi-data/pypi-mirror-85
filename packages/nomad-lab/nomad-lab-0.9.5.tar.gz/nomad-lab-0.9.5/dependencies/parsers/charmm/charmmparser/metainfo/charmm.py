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
    name='charmm_nomadmetainfo_json',
    description='None',
    a_legacy=LegacyDefinition(name='charmm.nomadmetainfo.json'))


class x_charmm_mdin_input_output_files(MCategory):
    '''
    Parameters of mdin belonging to x_charmm_section_control_parameters.
    '''

    m_def = Category(
        a_legacy=LegacyDefinition(name='x_charmm_mdin_input_output_files'))


class x_charmm_mdin_control_parameters(MCategory):
    '''
    Parameters of mdin belonging to x_charmm_section_control_parameters.
    '''

    m_def = Category(
        a_legacy=LegacyDefinition(name='x_charmm_mdin_control_parameters'))


class x_charmm_mdin_method(MCategory):
    '''
    Parameters of mdin belonging to section method.
    '''

    m_def = Category(
        a_legacy=LegacyDefinition(name='x_charmm_mdin_method'))


class x_charmm_mdout_single_configuration_calculation(MCategory):
    '''
    Parameters of mdout belonging to section_single_configuration_calculation.
    '''

    m_def = Category(
        a_legacy=LegacyDefinition(name='x_charmm_mdout_single_configuration_calculation'))


class x_charmm_mdout_method(MCategory):
    '''
    Parameters of mdin belonging to section method.
    '''

    m_def = Category(
        a_legacy=LegacyDefinition(name='x_charmm_mdout_method'))


class x_charmm_mdout_run(MCategory):
    '''
    Parameters of mdin belonging to settings run.
    '''

    m_def = Category(
        categories=[public.settings_run],
        a_legacy=LegacyDefinition(name='x_charmm_mdout_run'))


class x_charmm_mdin_run(MCategory):
    '''
    Parameters of mdin belonging to settings run.
    '''

    m_def = Category(
        categories=[public.settings_run],
        a_legacy=LegacyDefinition(name='x_charmm_mdin_run'))


class x_charmm_section_input_output_files(MSection):
    '''
    Section to store input and output file names
    '''

    m_def = Section(validate=False, a_legacy=LegacyDefinition(name='x_charmm_section_input_output_files'))


class x_charmm_section_control_parameters(MSection):
    '''
    Section to store the input and output control parameters
    '''

    m_def = Section(validate=False, a_legacy=LegacyDefinition(name='x_charmm_section_control_parameters'))

    x_charmm_inout_file_structure = Quantity(
        type=str,
        shape=[],
        description='''
        charmm input topology file.
        ''',
        a_legacy=LegacyDefinition(name='x_charmm_inout_file_structure'))

    x_charmm_inout_file_trajectory = Quantity(
        type=str,
        shape=[],
        description='''
        charmm output trajectory file.
        ''',
        a_legacy=LegacyDefinition(name='x_charmm_inout_file_trajectory'))

    x_charmm_inout_file_traj_coord = Quantity(
        type=str,
        shape=[],
        description='''
        charmm output trajectory file.
        ''',
        a_legacy=LegacyDefinition(name='x_charmm_inout_file_traj_coord'))

    x_charmm_inout_file_traj_vel = Quantity(
        type=str,
        shape=[],
        description='''
        charmm output file for velocities in the trajectory.
        ''',
        a_legacy=LegacyDefinition(name='x_charmm_inout_file_traj_vel'))

    x_charmm_inout_file_traj_force = Quantity(
        type=str,
        shape=[],
        description='''
        charmm output file for forces in the trajectory.
        ''',
        a_legacy=LegacyDefinition(name='x_charmm_inout_file_traj_force'))

    x_charmm_inout_file_output_coord = Quantity(
        type=str,
        shape=[],
        description='''
        charmm output coordinates file.
        ''',
        a_legacy=LegacyDefinition(name='x_charmm_inout_file_output_coord'))

    x_charmm_inout_file_out_coor_str = Quantity(
        type=str,
        shape=[],
        description='''
        charmm output coordinates on log.
        ''',
        a_legacy=LegacyDefinition(name='x_charmm_inout_file_out_coor_str'))

    x_charmm_inout_file_output_vel = Quantity(
        type=str,
        shape=[],
        description='''
        charmm output velocities file.
        ''',
        a_legacy=LegacyDefinition(name='x_charmm_inout_file_output_vel'))

    x_charmm_inout_file_output_force = Quantity(
        type=str,
        shape=[],
        description='''
        charmm output forces file.
        ''',
        a_legacy=LegacyDefinition(name='x_charmm_inout_file_output_force'))

    x_charmm_inout_file_input_coord = Quantity(
        type=str,
        shape=[],
        description='''
        charmm input coordinates file.
        ''',
        a_legacy=LegacyDefinition(name='x_charmm_inout_file_input_coord'))

    x_charmm_inout_file_in_coor_str = Quantity(
        type=str,
        shape=[],
        description='''
        charmm input coordinate on log file.
        ''',
        a_legacy=LegacyDefinition(name='x_charmm_inout_file_in_coor_str'))

    x_charmm_inout_file_input_vel = Quantity(
        type=str,
        shape=[],
        description='''
        charmm input velocities file.
        ''',
        a_legacy=LegacyDefinition(name='x_charmm_inout_file_input_vel'))

    x_charmm_inout_file_restart_coord = Quantity(
        type=str,
        shape=[],
        description='''
        charmm restart coordinates file.
        ''',
        a_legacy=LegacyDefinition(name='x_charmm_inout_file_restart_coord'))

    x_charmm_inout_file_restart_vel = Quantity(
        type=str,
        shape=[],
        description='''
        charmm restart velocities file.
        ''',
        a_legacy=LegacyDefinition(name='x_charmm_inout_file_restart_vel'))

    x_charmm_inout_file_rtf_file = Quantity(
        type=str,
        shape=[],
        description='''
        charmm RTF residue file.
        ''',
        a_legacy=LegacyDefinition(name='x_charmm_inout_file_rtf_file'))

    x_charmm_inout_file_prm_file = Quantity(
        type=str,
        shape=[],
        description='''
        charmm PRM parameter file.
        ''',
        a_legacy=LegacyDefinition(name='x_charmm_inout_file_prm_file'))

    x_charmm_inout_file_cor_file = Quantity(
        type=str,
        shape=[],
        description='''
        charmm CRD coordinates file.
        ''',
        a_legacy=LegacyDefinition(name='x_charmm_inout_file_cor_file'))

    x_charmm_inout_file_stream = Quantity(
        type=str,
        shape=[],
        description='''
        charmm stream input/output.
        ''',
        a_legacy=LegacyDefinition(name='x_charmm_inout_file_stream'))

    x_charmm_inout_file_rtf_str = Quantity(
        type=str,
        shape=[],
        description='''
        charmm stream RTF input.
        ''',
        a_legacy=LegacyDefinition(name='x_charmm_inout_file_rtf_str'))

    x_charmm_inout_file_par_str = Quantity(
        type=str,
        shape=[],
        description='''
        charmm stream parameter input.
        ''',
        a_legacy=LegacyDefinition(name='x_charmm_inout_file_par_str'))

    x_charmm_inout_file_output_log = Quantity(
        type=str,
        shape=[],
        description='''
        charmm MD output log file.
        ''',
        a_legacy=LegacyDefinition(name='x_charmm_inout_file_output_log'))

    x_charmm_inout_control_gaussian_option_is = Quantity(
        type=str,
        shape=[],
        description='''
        charmm running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_charmm_inout_control_gaussian_option_is'))

    x_charmm_inout_control_crystal = Quantity(
        type=str,
        shape=[],
        description='''
        charmm running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_charmm_inout_control_crystal'))

    x_charmm_inout_control_crystal_type = Quantity(
        type=str,
        shape=[],
        description='''
        charmm running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_charmm_inout_control_crystal_type'))

    x_charmm_inout_control_a_length = Quantity(
        type=str,
        shape=[],
        description='''
        charmm running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_charmm_inout_control_a_length'))

    x_charmm_inout_control_b_length = Quantity(
        type=str,
        shape=[],
        description='''
        charmm running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_charmm_inout_control_b_length'))

    x_charmm_inout_control_c_length = Quantity(
        type=str,
        shape=[],
        description='''
        charmm running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_charmm_inout_control_c_length'))

    x_charmm_inout_control_alpha = Quantity(
        type=str,
        shape=[],
        description='''
        charmm running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_charmm_inout_control_alpha'))

    x_charmm_inout_control_beta = Quantity(
        type=str,
        shape=[],
        description='''
        charmm running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_charmm_inout_control_beta'))

    x_charmm_inout_control_gamma = Quantity(
        type=str,
        shape=[],
        description='''
        charmm running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_charmm_inout_control_gamma'))

    x_charmm_inout_control_mini = Quantity(
        type=str,
        shape=[],
        description='''
        charmm running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_charmm_inout_control_mini'))

    x_charmm_inout_control_nstep = Quantity(
        type=str,
        shape=[],
        description='''
        charmm running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_charmm_inout_control_nstep'))

    x_charmm_inout_control_inbfrq = Quantity(
        type=str,
        shape=[],
        description='''
        charmm running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_charmm_inout_control_inbfrq'))

    x_charmm_inout_control_step = Quantity(
        type=str,
        shape=[],
        description='''
        charmm running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_charmm_inout_control_step'))

    x_charmm_inout_control_prtmin = Quantity(
        type=str,
        shape=[],
        description='''
        charmm running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_charmm_inout_control_prtmin'))

    x_charmm_inout_control_tolfun = Quantity(
        type=str,
        shape=[],
        description='''
        charmm running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_charmm_inout_control_tolfun'))

    x_charmm_inout_control_tolgrd = Quantity(
        type=str,
        shape=[],
        description='''
        charmm running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_charmm_inout_control_tolgrd'))

    x_charmm_inout_control_tolitr = Quantity(
        type=str,
        shape=[],
        description='''
        charmm running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_charmm_inout_control_tolitr'))

    x_charmm_inout_control_tolstp = Quantity(
        type=str,
        shape=[],
        description='''
        charmm running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_charmm_inout_control_tolstp'))

    x_charmm_inout_control_tfreq = Quantity(
        type=str,
        shape=[],
        description='''
        charmm running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_charmm_inout_control_tfreq'))

    x_charmm_inout_control_pcut = Quantity(
        type=str,
        shape=[],
        description='''
        charmm running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_charmm_inout_control_pcut'))

    x_charmm_inout_control_ihbfrq = Quantity(
        type=str,
        shape=[],
        description='''
        charmm running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_charmm_inout_control_ihbfrq'))

    x_charmm_inout_control_ncgcyc = Quantity(
        type=str,
        shape=[],
        description='''
        charmm running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_charmm_inout_control_ncgcyc'))

    x_charmm_inout_control_nprint = Quantity(
        type=str,
        shape=[],
        description='''
        charmm running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_charmm_inout_control_nprint'))

    x_charmm_inout_control_nonbond_option_flags = Quantity(
        type=str,
        shape=[],
        description='''
        charmm running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_charmm_inout_control_nonbond_option_flags'))

    x_charmm_inout_control_cutnb = Quantity(
        type=str,
        shape=[],
        description='''
        charmm running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_charmm_inout_control_cutnb'))

    x_charmm_inout_control_ctexnb = Quantity(
        type=str,
        shape=[],
        description='''
        charmm running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_charmm_inout_control_ctexnb'))

    x_charmm_inout_control_ctonnb = Quantity(
        type=str,
        shape=[],
        description='''
        charmm running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_charmm_inout_control_ctonnb'))

    x_charmm_inout_control_ctofnb = Quantity(
        type=str,
        shape=[],
        description='''
        charmm running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_charmm_inout_control_ctofnb'))

    x_charmm_inout_control_cgonnb = Quantity(
        type=str,
        shape=[],
        description='''
        charmm running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_charmm_inout_control_cgonnb'))

    x_charmm_inout_control_cgofnb = Quantity(
        type=str,
        shape=[],
        description='''
        charmm running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_charmm_inout_control_cgofnb'))

    x_charmm_inout_control_wmin = Quantity(
        type=str,
        shape=[],
        description='''
        charmm running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_charmm_inout_control_wmin'))

    x_charmm_inout_control_cdie = Quantity(
        type=str,
        shape=[],
        description='''
        charmm running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_charmm_inout_control_cdie'))

    x_charmm_inout_control_switch = Quantity(
        type=str,
        shape=[],
        description='''
        charmm running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_charmm_inout_control_switch'))

    x_charmm_inout_control_vswitch = Quantity(
        type=str,
        shape=[],
        description='''
        charmm running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_charmm_inout_control_vswitch'))

    x_charmm_inout_control_atoms = Quantity(
        type=str,
        shape=[],
        description='''
        charmm running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_charmm_inout_control_atoms'))

    x_charmm_inout_control_wrnmxd = Quantity(
        type=str,
        shape=[],
        description='''
        charmm running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_charmm_inout_control_wrnmxd'))

    x_charmm_inout_control_e14fac = Quantity(
        type=str,
        shape=[],
        description='''
        charmm running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_charmm_inout_control_e14fac'))

    x_charmm_inout_control_eps = Quantity(
        type=str,
        shape=[],
        description='''
        charmm running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_charmm_inout_control_eps'))

    x_charmm_inout_control_nbxmod = Quantity(
        type=str,
        shape=[],
        description='''
        charmm running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_charmm_inout_control_nbxmod'))

    x_charmm_inout_control_hydrogen_bond_cutoff_distance = Quantity(
        type=str,
        shape=[],
        description='''
        charmm running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_charmm_inout_control_hydrogen_bond_cutoff_distance'))

    x_charmm_inout_control_hydrogen_bond_cutoff_angle = Quantity(
        type=str,
        shape=[],
        description='''
        charmm running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_charmm_inout_control_hydrogen_bond_cutoff_angle'))

    x_charmm_inout_control_hydrogen_bond_switching_on_distance = Quantity(
        type=str,
        shape=[],
        description='''
        charmm running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_charmm_inout_control_hydrogen_bond_switching_on_distance'))

    x_charmm_inout_control_hydrogen_bond_switching_off_distance = Quantity(
        type=str,
        shape=[],
        description='''
        charmm running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_charmm_inout_control_hydrogen_bond_switching_off_distance'))

    x_charmm_inout_control_hydrogen_bond_switching_on_angle = Quantity(
        type=str,
        shape=[],
        description='''
        charmm running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_charmm_inout_control_hydrogen_bond_switching_on_angle'))

    x_charmm_inout_control_hydrogen_bond_switching_off_angle = Quantity(
        type=str,
        shape=[],
        description='''
        charmm running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_charmm_inout_control_hydrogen_bond_switching_off_angle'))

    x_charmm_inout_control_hbond_exclusions_due_to_distance_cutoff = Quantity(
        type=str,
        shape=[],
        description='''
        charmm running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_charmm_inout_control_hbond_exclusions_due_to_distance_cutoff'))

    x_charmm_inout_control_hbond_exclusions_due_to_angle_cutoff = Quantity(
        type=str,
        shape=[],
        description='''
        charmm running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_charmm_inout_control_hbond_exclusions_due_to_angle_cutoff'))

    x_charmm_inout_control_acceptor_antecedents = Quantity(
        type=str,
        shape=[],
        description='''
        charmm running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_charmm_inout_control_acceptor_antecedents'))

    x_charmm_inout_control_hbond_exclusions_due_to_duplications = Quantity(
        type=str,
        shape=[],
        description='''
        charmm running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_charmm_inout_control_hbond_exclusions_due_to_duplications'))

    x_charmm_inout_control_hbond_deletions_due_to_best_option = Quantity(
        type=str,
        shape=[],
        description='''
        charmm running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_charmm_inout_control_hbond_deletions_due_to_best_option'))

    x_charmm_inout_control_hbond_deletions_due_to_duplications = Quantity(
        type=str,
        shape=[],
        description='''
        charmm running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_charmm_inout_control_hbond_deletions_due_to_duplications'))

    x_charmm_inout_control_hbond_deletions_due_to_fixed_atoms = Quantity(
        type=str,
        shape=[],
        description='''
        charmm running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_charmm_inout_control_hbond_deletions_due_to_fixed_atoms'))

    x_charmm_inout_control_hbond_deletions_due_to_exclusion = Quantity(
        type=str,
        shape=[],
        description='''
        charmm running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_charmm_inout_control_hbond_deletions_due_to_exclusion'))

    x_charmm_inout_control_hydrogen_bonds_present = Quantity(
        type=str,
        shape=[],
        description='''
        charmm running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_charmm_inout_control_hydrogen_bonds_present'))

    x_charmm_inout_control_minimization_exit_status = Quantity(
        type=str,
        shape=[],
        description='''
        charmm running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_charmm_inout_control_minimization_exit_status'))

    x_charmm_inout_control_dyna = Quantity(
        type=str,
        shape=[],
        description='''
        charmm running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_charmm_inout_control_dyna'))

    x_charmm_inout_control_akmastp = Quantity(
        type=str,
        shape=[],
        description='''
        charmm running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_charmm_inout_control_akmastp'))

    x_charmm_inout_control_firstt = Quantity(
        type=str,
        shape=[],
        description='''
        charmm running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_charmm_inout_control_firstt'))

    x_charmm_inout_control_iseed = Quantity(
        type=str,
        shape=[],
        description='''
        charmm running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_charmm_inout_control_iseed'))

    x_charmm_inout_control_iprfrq = Quantity(
        type=str,
        shape=[],
        description='''
        charmm running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_charmm_inout_control_iprfrq'))

    x_charmm_inout_control_ihtfrq = Quantity(
        type=str,
        shape=[],
        description='''
        charmm running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_charmm_inout_control_ihtfrq'))

    x_charmm_inout_control_ieqfrq = Quantity(
        type=str,
        shape=[],
        description='''
        charmm running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_charmm_inout_control_ieqfrq'))

    x_charmm_inout_control_iunrea = Quantity(
        type=str,
        shape=[],
        description='''
        charmm running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_charmm_inout_control_iunrea'))

    x_charmm_inout_control_iunwri = Quantity(
        type=str,
        shape=[],
        description='''
        charmm running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_charmm_inout_control_iunwri'))

    x_charmm_inout_control_iunos = Quantity(
        type=str,
        shape=[],
        description='''
        charmm running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_charmm_inout_control_iunos'))

    x_charmm_inout_control_iuncrd = Quantity(
        type=str,
        shape=[],
        description='''
        charmm running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_charmm_inout_control_iuncrd'))

    x_charmm_inout_control_iunvel = Quantity(
        type=str,
        shape=[],
        description='''
        charmm running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_charmm_inout_control_iunvel'))

    x_charmm_inout_control_iunxyz = Quantity(
        type=str,
        shape=[],
        description='''
        charmm running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_charmm_inout_control_iunxyz'))

    x_charmm_inout_control_kunit = Quantity(
        type=str,
        shape=[],
        description='''
        charmm running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_charmm_inout_control_kunit'))

    x_charmm_inout_control_nsavc = Quantity(
        type=str,
        shape=[],
        description='''
        charmm running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_charmm_inout_control_nsavc'))

    x_charmm_inout_control_nsavv = Quantity(
        type=str,
        shape=[],
        description='''
        charmm running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_charmm_inout_control_nsavv'))

    x_charmm_inout_control_nsavx = Quantity(
        type=str,
        shape=[],
        description='''
        charmm running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_charmm_inout_control_nsavx'))

    x_charmm_inout_control_iscale = Quantity(
        type=str,
        shape=[],
        description='''
        charmm running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_charmm_inout_control_iscale'))

    x_charmm_inout_control_iscvel = Quantity(
        type=str,
        shape=[],
        description='''
        charmm running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_charmm_inout_control_iscvel'))

    x_charmm_inout_control_iasors = Quantity(
        type=str,
        shape=[],
        description='''
        charmm running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_charmm_inout_control_iasors'))

    x_charmm_inout_control_iasvel = Quantity(
        type=str,
        shape=[],
        description='''
        charmm running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_charmm_inout_control_iasvel'))

    x_charmm_inout_control_ichecw = Quantity(
        type=str,
        shape=[],
        description='''
        charmm running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_charmm_inout_control_ichecw'))

    x_charmm_inout_control_ntrfrq = Quantity(
        type=str,
        shape=[],
        description='''
        charmm running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_charmm_inout_control_ntrfrq'))

    x_charmm_inout_control_ilbfrq = Quantity(
        type=str,
        shape=[],
        description='''
        charmm running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_charmm_inout_control_ilbfrq'))

    x_charmm_inout_control_imgfrq = Quantity(
        type=str,
        shape=[],
        description='''
        charmm running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_charmm_inout_control_imgfrq'))

    x_charmm_inout_control_isvfrq = Quantity(
        type=str,
        shape=[],
        description='''
        charmm running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_charmm_inout_control_isvfrq'))

    x_charmm_inout_control_ncycle = Quantity(
        type=str,
        shape=[],
        description='''
        charmm running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_charmm_inout_control_ncycle'))

    x_charmm_inout_control_nsnos = Quantity(
        type=str,
        shape=[],
        description='''
        charmm running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_charmm_inout_control_nsnos'))

    x_charmm_inout_control_teminc = Quantity(
        type=str,
        shape=[],
        description='''
        charmm running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_charmm_inout_control_teminc'))

    x_charmm_inout_control_tstruc = Quantity(
        type=str,
        shape=[],
        description='''
        charmm running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_charmm_inout_control_tstruc'))

    x_charmm_inout_control_finalt = Quantity(
        type=str,
        shape=[],
        description='''
        charmm running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_charmm_inout_control_finalt'))

    x_charmm_inout_control_twindh = Quantity(
        type=str,
        shape=[],
        description='''
        charmm running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_charmm_inout_control_twindh'))

    x_charmm_inout_control_twindl = Quantity(
        type=str,
        shape=[],
        description='''
        charmm running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_charmm_inout_control_twindl'))

    x_charmm_inout_control_time_step = Quantity(
        type=str,
        shape=[],
        description='''
        charmm running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_charmm_inout_control_time_step'))

    x_charmm_inout_control_random_num_gen_seeds = Quantity(
        type=str,
        shape=[],
        description='''
        charmm running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_charmm_inout_control_random_num_gen_seeds'))

    x_charmm_inout_control_number_of_degrees_of_freedom = Quantity(
        type=str,
        shape=[],
        description='''
        charmm running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_charmm_inout_control_number_of_degrees_of_freedom'))

    x_charmm_inout_control_gaussian_option = Quantity(
        type=str,
        shape=[],
        description='''
        charmm running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_charmm_inout_control_gaussian_option'))

    x_charmm_inout_control_velocities_assigned_at_temperature = Quantity(
        type=str,
        shape=[],
        description='''
        charmm running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_charmm_inout_control_velocities_assigned_at_temperature'))

    x_charmm_inout_control_seeds = Quantity(
        type=str,
        shape=[],
        description='''
        charmm running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_charmm_inout_control_seeds'))

    x_charmm_inout_control_shake_tolerance = Quantity(
        type=str,
        shape=[],
        description='''
        charmm running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_charmm_inout_control_shake_tolerance'))

    x_charmm_inout_control_strt = Quantity(
        type=str,
        shape=[],
        description='''
        charmm running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_charmm_inout_control_strt'))

    x_charmm_inout_control_rest = Quantity(
        type=str,
        shape=[],
        description='''
        charmm running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_charmm_inout_control_rest'))

    x_charmm_inout_control_qref = Quantity(
        type=str,
        shape=[],
        description='''
        charmm running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_charmm_inout_control_qref'))

    x_charmm_inout_control_tref = Quantity(
        type=str,
        shape=[],
        description='''
        charmm running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_charmm_inout_control_tref'))

    x_charmm_inout_control_hoover = Quantity(
        type=str,
        shape=[],
        description='''
        charmm running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_charmm_inout_control_hoover'))

    x_charmm_inout_control_reft = Quantity(
        type=str,
        shape=[],
        description='''
        charmm running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_charmm_inout_control_reft'))

    x_charmm_inout_control_tmass = Quantity(
        type=str,
        shape=[],
        description='''
        charmm running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_charmm_inout_control_tmass'))

    x_charmm_inout_control_pcons = Quantity(
        type=str,
        shape=[],
        description='''
        charmm running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_charmm_inout_control_pcons'))

    x_charmm_inout_control_pmass = Quantity(
        type=str,
        shape=[],
        description='''
        charmm running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_charmm_inout_control_pmass'))

    x_charmm_inout_control_number_of_steps = Quantity(
        type=str,
        shape=[],
        description='''
        charmm running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_charmm_inout_control_number_of_steps'))

    x_charmm_inout_control_steps_per_cycle = Quantity(
        type=str,
        shape=[],
        description='''
        charmm running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_charmm_inout_control_steps_per_cycle'))

    x_charmm_inout_control_initial_temperature = Quantity(
        type=str,
        shape=[],
        description='''
        charmm running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_charmm_inout_control_initial_temperature'))

    x_charmm_inout_control_dielectric = Quantity(
        type=str,
        shape=[],
        description='''
        charmm running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_charmm_inout_control_dielectric'))

    x_charmm_inout_control_excluded_species_or_groups = Quantity(
        type=str,
        shape=[],
        description='''
        charmm running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_charmm_inout_control_excluded_species_or_groups'))

    x_charmm_inout_control_1_4_electrostatics_scale = Quantity(
        type=str,
        shape=[],
        description='''
        charmm running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_charmm_inout_control_1_4_electrostatics_scale'))

    x_charmm_inout_control_velocity_rescale_temp = Quantity(
        type=str,
        shape=[],
        description='''
        charmm running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_charmm_inout_control_velocity_rescale_temp'))

    x_charmm_inout_control_velocity_reassignment_freq = Quantity(
        type=str,
        shape=[],
        description='''
        charmm running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_charmm_inout_control_velocity_reassignment_freq'))

    x_charmm_inout_control_velocity_reassignment_temp = Quantity(
        type=str,
        shape=[],
        description='''
        charmm running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_charmm_inout_control_velocity_reassignment_temp'))

    x_charmm_inout_control_langevin_dynamics = Quantity(
        type=str,
        shape=[],
        description='''
        charmm running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_charmm_inout_control_langevin_dynamics'))

    x_charmm_inout_control_langevin_temperature = Quantity(
        type=str,
        shape=[],
        description='''
        charmm running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_charmm_inout_control_langevin_temperature'))

    x_charmm_inout_control_langevin_integrator = Quantity(
        type=str,
        shape=[],
        description='''
        charmm running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_charmm_inout_control_langevin_integrator'))

    x_charmm_inout_control_langevin_damping_coefficient_unit = Quantity(
        type=str,
        shape=[],
        description='''
        charmm running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_charmm_inout_control_langevin_damping_coefficient_unit'))

    x_charmm_inout_control_temperature_coupling = Quantity(
        type=str,
        shape=[],
        description='''
        charmm running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_charmm_inout_control_temperature_coupling'))

    x_charmm_inout_control_coupling_temperature = Quantity(
        type=str,
        shape=[],
        description='''
        charmm running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_charmm_inout_control_coupling_temperature'))

    x_charmm_inout_control_target_pressure = Quantity(
        type=str,
        shape=[],
        description='''
        charmm running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_charmm_inout_control_target_pressure'))

    x_charmm_inout_control_langevin_oscillation_period = Quantity(
        type=str,
        shape=[],
        description='''
        charmm running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_charmm_inout_control_langevin_oscillation_period'))

    x_charmm_inout_control_langevin_decay_time = Quantity(
        type=str,
        shape=[],
        description='''
        charmm running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_charmm_inout_control_langevin_decay_time'))

    x_charmm_inout_control_langevin_piston_temperature = Quantity(
        type=str,
        shape=[],
        description='''
        charmm running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_charmm_inout_control_langevin_piston_temperature'))

    x_charmm_inout_control_pressure_control = Quantity(
        type=str,
        shape=[],
        description='''
        charmm running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_charmm_inout_control_pressure_control'))

    x_charmm_inout_control_particle_mesh_ewald = Quantity(
        type=str,
        shape=[],
        description='''
        charmm running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_charmm_inout_control_particle_mesh_ewald'))

    x_charmm_inout_control_pme_tolerance = Quantity(
        type=str,
        shape=[],
        description='''
        charmm running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_charmm_inout_control_pme_tolerance'))

    x_charmm_inout_control_pme_ewald_coefficient = Quantity(
        type=str,
        shape=[],
        description='''
        charmm running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_charmm_inout_control_pme_ewald_coefficient'))

    x_charmm_inout_control_pme_interpolation_order = Quantity(
        type=str,
        shape=[],
        description='''
        charmm running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_charmm_inout_control_pme_interpolation_order'))

    x_charmm_inout_control_pme_grid_dimensions = Quantity(
        type=str,
        shape=[],
        description='''
        charmm running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_charmm_inout_control_pme_grid_dimensions'))

    x_charmm_inout_control_pme_maximum_grid_spacing = Quantity(
        type=str,
        shape=[],
        description='''
        charmm running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_charmm_inout_control_pme_maximum_grid_spacing'))

    x_charmm_inout_control_minimization = Quantity(
        type=str,
        shape=[],
        description='''
        charmm running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_charmm_inout_control_minimization'))

    x_charmm_inout_control_verlet_integrator = Quantity(
        type=str,
        shape=[],
        description='''
        charmm running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_charmm_inout_control_verlet_integrator'))

    x_charmm_inout_control_random_number_seed = Quantity(
        type=str,
        shape=[],
        description='''
        charmm running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_charmm_inout_control_random_number_seed'))

    x_charmm_inout_control_structure_file = Quantity(
        type=str,
        shape=[],
        description='''
        charmm running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_charmm_inout_control_structure_file'))

    x_charmm_inout_control_parameter_file = Quantity(
        type=str,
        shape=[],
        description='''
        charmm running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_charmm_inout_control_parameter_file'))

    x_charmm_inout_control_number_of_parameters = Quantity(
        type=np.dtype(np.int32),
        shape=[],
        description='''
        charmm running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_charmm_inout_control_number_of_parameters'))

    x_charmm_inout_control_parameters = Quantity(
        type=str,
        shape=['x_charmm_inout_control_number_of_parameters'],
        description='''
        charmm running environment and control parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_charmm_inout_control_parameters'))

    x_charmm_section_input_output_files = SubSection(
        sub_section=SectionProxy('x_charmm_section_input_output_files'),
        repeats=True,
        a_legacy=LegacyDefinition(name='x_charmm_section_input_output_files'))


class x_charmm_section_atom_to_atom_type_ref(MSection):
    '''
    Section to store atom label to atom type definition list
    '''

    m_def = Section(validate=False, a_legacy=LegacyDefinition(name='x_charmm_section_atom_to_atom_type_ref'))

    x_charmm_atom_to_atom_type_ref = Quantity(
        type=np.dtype(np.int64),
        shape=['number_of_atoms_per_type'],
        description='''
        Reference to the atoms of each atom type.
        ''',
        a_legacy=LegacyDefinition(name='x_charmm_atom_to_atom_type_ref'))


class x_charmm_section_single_configuration_calculation(MSection):
    '''
    section for gathering values for MD steps
    '''

    m_def = Section(validate=False, a_legacy=LegacyDefinition(name='x_charmm_section_single_configuration_calculation'))


class section_system(public.section_system):

    m_def = Section(validate=False, extends_base_section=True, a_legacy=LegacyDefinition(name='section_system'))

    x_charmm_atom_positions_image_index = Quantity(
        type=np.dtype(np.int32),
        shape=['number_of_atoms', 3],
        unit='dimensionless',
        description='''
        PBC image flag index.
        ''',
        a_legacy=LegacyDefinition(name='x_charmm_atom_positions_image_index'))

    x_charmm_atom_positions_scaled = Quantity(
        type=np.dtype(np.float64),
        shape=['number_of_atoms', 3],
        unit='dimensionless',
        description='''
        Position of the atoms in a scaled format [0, 1].
        ''',
        a_legacy=LegacyDefinition(name='x_charmm_atom_positions_scaled'))

    x_charmm_atom_positions_wrapped = Quantity(
        type=np.dtype(np.float64),
        shape=['number_of_atoms', 3],
        unit='meter',
        description='''
        Position of the atoms wrapped back to the periodic box.
        ''',
        a_legacy=LegacyDefinition(name='x_charmm_atom_positions_wrapped'))

    x_charmm_lattice_lengths = Quantity(
        type=np.dtype(np.float64),
        shape=[3],
        description='''
        Lattice dimensions in a vector. Vector includes [a, b, c] lengths.
        ''',
        categories=[public.configuration_core],
        a_legacy=LegacyDefinition(name='x_charmm_lattice_lengths'))

    x_charmm_lattice_angles = Quantity(
        type=np.dtype(np.float64),
        shape=[3],
        description='''
        Angles of lattice vectors. Vector includes [alpha, beta, gamma] in degrees.
        ''',
        categories=[public.configuration_core],
        a_legacy=LegacyDefinition(name='x_charmm_lattice_angles'))

    x_charmm_dummy = Quantity(
        type=str,
        shape=[],
        description='''
        dummy
        ''',
        a_legacy=LegacyDefinition(name='x_charmm_dummy'))

    x_charmm_mdin_finline = Quantity(
        type=str,
        shape=[],
        description='''
        finline in mdin
        ''',
        a_legacy=LegacyDefinition(name='x_charmm_mdin_finline'))

    x_charmm_traj_timestep_store = Quantity(
        type=str,
        shape=[],
        description='''
        tmp
        ''',
        a_legacy=LegacyDefinition(name='x_charmm_traj_timestep_store'))

    x_charmm_traj_number_of_atoms_store = Quantity(
        type=str,
        shape=[],
        description='''
        tmp
        ''',
        a_legacy=LegacyDefinition(name='x_charmm_traj_number_of_atoms_store'))

    x_charmm_traj_box_bound_store = Quantity(
        type=str,
        shape=[],
        description='''
        tmp
        ''',
        a_legacy=LegacyDefinition(name='x_charmm_traj_box_bound_store'))

    x_charmm_traj_box_bounds_store = Quantity(
        type=str,
        shape=[],
        description='''
        tmp
        ''',
        a_legacy=LegacyDefinition(name='x_charmm_traj_box_bounds_store'))

    x_charmm_traj_variables_store = Quantity(
        type=str,
        shape=[],
        description='''
        tmp
        ''',
        a_legacy=LegacyDefinition(name='x_charmm_traj_variables_store'))

    x_charmm_traj_atoms_store = Quantity(
        type=str,
        shape=[],
        description='''
        tmp
        ''',
        a_legacy=LegacyDefinition(name='x_charmm_traj_atoms_store'))


class section_sampling_method(public.section_sampling_method):

    m_def = Section(validate=False, extends_base_section=True, a_legacy=LegacyDefinition(name='section_sampling_method'))

    x_charmm_barostat_target_pressure = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        unit='pascal',
        description='''
        MD barostat target pressure.
        ''',
        categories=[public.settings_barostat, public.settings_sampling, public.settings_molecular_dynamics],
        a_legacy=LegacyDefinition(name='x_charmm_barostat_target_pressure'))

    x_charmm_barostat_tau = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        unit='second',
        description='''
        MD barostat relaxation time.
        ''',
        categories=[public.settings_barostat, public.settings_sampling, public.settings_molecular_dynamics],
        a_legacy=LegacyDefinition(name='x_charmm_barostat_tau'))

    x_charmm_barostat_type = Quantity(
        type=str,
        shape=[],
        description='''
        MD barostat type, valid values are defined in the barostat_type wiki page.
        ''',
        categories=[public.settings_barostat, public.settings_sampling, public.settings_molecular_dynamics],
        a_legacy=LegacyDefinition(name='x_charmm_barostat_type'))

    x_charmm_integrator_dt = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        unit='second',
        description='''
        MD integration time step.
        ''',
        categories=[public.settings_integrator, public.settings_sampling, public.settings_molecular_dynamics],
        a_legacy=LegacyDefinition(name='x_charmm_integrator_dt'))

    x_charmm_integrator_type = Quantity(
        type=str,
        shape=[],
        description='''
        MD integrator type, valid values are defined in the integrator_type wiki page.
        ''',
        categories=[public.settings_integrator, public.settings_sampling, public.settings_molecular_dynamics],
        a_legacy=LegacyDefinition(name='x_charmm_integrator_type'))

    x_charmm_periodicity_type = Quantity(
        type=str,
        shape=[],
        description='''
        Periodic boundary condition type in the sampling (non-PBC or PBC).
        ''',
        categories=[public.settings_integrator, public.settings_sampling, public.settings_molecular_dynamics],
        a_legacy=LegacyDefinition(name='x_charmm_periodicity_type'))

    x_charmm_langevin_gamma = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        unit='second',
        description='''
        Langevin thermostat damping factor.
        ''',
        categories=[public.settings_sampling, public.settings_molecular_dynamics, public.settings_thermostat],
        a_legacy=LegacyDefinition(name='x_charmm_langevin_gamma'))

    x_charmm_number_of_steps_requested = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        description='''
        Number of requested MD integration time steps.
        ''',
        categories=[public.settings_integrator, public.settings_sampling, public.settings_molecular_dynamics],
        a_legacy=LegacyDefinition(name='x_charmm_number_of_steps_requested'))

    x_charmm_thermostat_level = Quantity(
        type=str,
        shape=[],
        description='''
        MD thermostat level (see wiki: single, multiple, regional).
        ''',
        categories=[public.settings_sampling, public.settings_molecular_dynamics, public.settings_thermostat],
        a_legacy=LegacyDefinition(name='x_charmm_thermostat_level'))

    x_charmm_thermostat_target_temperature = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        unit='kelvin',
        description='''
        MD thermostat target temperature.
        ''',
        categories=[public.settings_sampling, public.settings_molecular_dynamics, public.settings_thermostat],
        a_legacy=LegacyDefinition(name='x_charmm_thermostat_target_temperature'))

    x_charmm_thermostat_tau = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        unit='second',
        description='''
        MD thermostat relaxation time.
        ''',
        categories=[public.settings_sampling, public.settings_molecular_dynamics, public.settings_thermostat],
        a_legacy=LegacyDefinition(name='x_charmm_thermostat_tau'))

    x_charmm_thermostat_type = Quantity(
        type=str,
        shape=[],
        description='''
        MD thermostat type, valid values are defined in the thermostat_type wiki page.
        ''',
        categories=[public.settings_sampling, public.settings_molecular_dynamics, public.settings_thermostat],
        a_legacy=LegacyDefinition(name='x_charmm_thermostat_type'))


class section_atom_type(common.section_atom_type):

    m_def = Section(validate=False, extends_base_section=True, a_legacy=LegacyDefinition(name='section_atom_type'))

    x_charmm_atom_name = Quantity(
        type=str,
        shape=[],
        description='''
        Atom name of an atom in topology definition.
        ''',
        a_legacy=LegacyDefinition(name='x_charmm_atom_name'))

    x_charmm_atom_type = Quantity(
        type=str,
        shape=[],
        description='''
        Atom type of an atom in topology definition.
        ''',
        a_legacy=LegacyDefinition(name='x_charmm_atom_type'))

    x_charmm_atom_element = Quantity(
        type=str,
        shape=[],
        description='''
        Atom type of an atom in topology definition.
        ''',
        a_legacy=LegacyDefinition(name='x_charmm_atom_element'))

    x_charmm_atom_type_element = Quantity(
        type=str,
        shape=[],
        description='''
        Element symbol of an atom type.
        ''',
        a_legacy=LegacyDefinition(name='x_charmm_atom_type_element'))

    x_charmm_atom_type_radius = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        description='''
        van der Waals radius of an atom type.
        ''',
        a_legacy=LegacyDefinition(name='x_charmm_atom_type_radius'))

    number_of_atoms_per_type = Quantity(
        type=int,
        shape=[],
        description='''
        Number of atoms involved in this type.
        ''',
        a_legacy=LegacyDefinition(name='number_of_atoms_per_type'))


class section_interaction(common.section_interaction):

    m_def = Section(validate=False, extends_base_section=True, a_legacy=LegacyDefinition(name='section_interaction'))

    x_charmm_interaction_atom_to_atom_type_ref = Quantity(
        type=common.section_atom_type,
        shape=['number_of_atoms_per_interaction'],
        description='''
        Reference to the atom type of each interaction atoms.
        ''',
        a_legacy=LegacyDefinition(name='x_charmm_interaction_atom_to_atom_type_ref'))

    x_charmm_number_of_defined_pair_interactions = Quantity(
        type=np.dtype(np.int32),
        shape=[],
        description='''
        Number of defined pair interactions (L-J pairs).
        ''',
        a_legacy=LegacyDefinition(name='x_charmm_number_of_defined_pair_interactions'))

    x_charmm_pair_interaction_atom_type_ref = Quantity(
        type=common.section_atom_type,
        shape=['x_charmm_number_of_defined_pair_interactions', 'number_of_atoms_per_interaction'],
        description='''
        Reference to the atom type for pair interactions.
        ''',
        a_legacy=LegacyDefinition(name='x_charmm_pair_interaction_atom_type_ref'))

    x_charmm_pair_interaction_parameters = Quantity(
        type=np.dtype(np.float64),
        shape=['x_charmm_number_of_defined_pair_interactions', 2],
        description='''
        Pair interactions parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_charmm_pair_interaction_parameters'))


class section_molecule_interaction(common.section_molecule_interaction):

    m_def = Section(validate=False, extends_base_section=True, a_legacy=LegacyDefinition(name='section_molecule_interaction'))

    x_charmm_molecule_interaction_atom_to_atom_type_ref = Quantity(
        type=common.section_atom_type,
        shape=['number_of_atoms_per_interaction'],
        description='''
        Reference to the atom type of each molecule interaction atoms.
        ''',
        a_legacy=LegacyDefinition(name='x_charmm_molecule_interaction_atom_to_atom_type_ref'))

    x_charmm_number_of_defined_molecule_pair_interactions = Quantity(
        type=np.dtype(np.int32),
        shape=[],
        description='''
        Number of defined pair interactions within a molecule (L-J pairs).
        ''',
        a_legacy=LegacyDefinition(name='x_charmm_number_of_defined_molecule_pair_interactions'))

    x_charmm_pair_molecule_interaction_parameters = Quantity(
        type=np.dtype(np.float64),
        shape=['number_of_defined_molecule_pair_interactions', 2],
        description='''
        Molecule pair interactions parameters.
        ''',
        a_legacy=LegacyDefinition(name='x_charmm_pair_molecule_interaction_parameters'))

    x_charmm_pair_molecule_interaction_to_atom_type_ref = Quantity(
        type=common.section_atom_type,
        shape=['x_charmm_number_of_defined_pair_interactions', 'number_of_atoms_per_interaction'],
        description='''
        Reference to the atom type for pair interactions within a molecule.
        ''',
        a_legacy=LegacyDefinition(name='x_charmm_pair_molecule_interaction_to_atom_type_ref'))


class section_run(public.section_run):

    m_def = Section(validate=False, extends_base_section=True, a_legacy=LegacyDefinition(name='section_run'))

    x_charmm_program_version_date = Quantity(
        type=str,
        shape=[],
        description='''
        Program version date.
        ''',
        a_legacy=LegacyDefinition(name='x_charmm_program_version_date'))

    x_charmm_parallel_task_nr = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        description='''
        Program task no.
        ''',
        a_legacy=LegacyDefinition(name='x_charmm_parallel_task_nr'))

    x_charmm_build_osarch = Quantity(
        type=str,
        shape=[],
        description='''
        Program Build OS/ARCH
        ''',
        a_legacy=LegacyDefinition(name='x_charmm_build_osarch'))

    x_charmm_output_created_by_user = Quantity(
        type=str,
        shape=[],
        description='''
        Output file creator
        ''',
        a_legacy=LegacyDefinition(name='x_charmm_output_created_by_user'))

    x_charmm_most_severe_warning_level = Quantity(
        type=str,
        shape=[],
        description='''
        Highest charmm warning level in the run.
        ''',
        a_legacy=LegacyDefinition(name='x_charmm_most_severe_warning_level'))

    x_charmm_program_build_date = Quantity(
        type=str,
        shape=[],
        description='''
        Program Build date
        ''',
        a_legacy=LegacyDefinition(name='x_charmm_program_build_date'))

    x_charmm_program_citation = Quantity(
        type=str,
        shape=[],
        description='''
        Program citations
        ''',
        a_legacy=LegacyDefinition(name='x_charmm_program_citation'))

    x_charmm_program_copyright = Quantity(
        type=str,
        shape=[],
        description='''
        Program copyright
        ''',
        a_legacy=LegacyDefinition(name='x_charmm_program_copyright'))

    x_charmm_number_of_tasks = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        description='''
        Number of tasks in parallel program (MPI).
        ''',
        a_legacy=LegacyDefinition(name='x_charmm_number_of_tasks'))

    x_charmm_program_module_version = Quantity(
        type=str,
        shape=[],
        description='''
        charmm program module version.
        ''',
        a_legacy=LegacyDefinition(name='x_charmm_program_module_version'))

    x_charmm_program_license = Quantity(
        type=str,
        shape=[],
        description='''
        charmm program license.
        ''',
        a_legacy=LegacyDefinition(name='x_charmm_program_license'))

    x_charmm_xlo_xhi = Quantity(
        type=str,
        shape=[],
        description='''
        test
        ''',
        a_legacy=LegacyDefinition(name='x_charmm_xlo_xhi'))

    x_charmm_data_file_store = Quantity(
        type=str,
        shape=[],
        description='''
        Filename of data file
        ''',
        a_legacy=LegacyDefinition(name='x_charmm_data_file_store'))

    x_charmm_program_working_path = Quantity(
        type=str,
        shape=[],
        description='''
        tmp
        ''',
        a_legacy=LegacyDefinition(name='x_charmm_program_working_path'))

    x_charmm_program_execution_host = Quantity(
        type=str,
        shape=[],
        description='''
        tmp
        ''',
        a_legacy=LegacyDefinition(name='x_charmm_program_execution_host'))

    x_charmm_program_execution_path = Quantity(
        type=str,
        shape=[],
        description='''
        tmp
        ''',
        a_legacy=LegacyDefinition(name='x_charmm_program_execution_path'))

    x_charmm_program_module = Quantity(
        type=str,
        shape=[],
        description='''
        tmp
        ''',
        a_legacy=LegacyDefinition(name='x_charmm_program_module'))

    x_charmm_program_execution_date = Quantity(
        type=str,
        shape=[],
        description='''
        tmp
        ''',
        a_legacy=LegacyDefinition(name='x_charmm_program_execution_date'))

    x_charmm_program_execution_time = Quantity(
        type=str,
        shape=[],
        description='''
        tmp
        ''',
        a_legacy=LegacyDefinition(name='x_charmm_program_execution_time'))

    x_charmm_mdin_header = Quantity(
        type=str,
        shape=[],
        description='''
        tmp
        ''',
        a_legacy=LegacyDefinition(name='x_charmm_mdin_header'))

    x_charmm_mdin_wt = Quantity(
        type=str,
        shape=[],
        description='''
        tmp
        ''',
        a_legacy=LegacyDefinition(name='x_charmm_mdin_wt'))

    x_charmm_section_control_parameters = SubSection(
        sub_section=SectionProxy('x_charmm_section_control_parameters'),
        repeats=True,
        a_legacy=LegacyDefinition(name='x_charmm_section_control_parameters'))


class section_topology(common.section_topology):

    m_def = Section(validate=False, extends_base_section=True, a_legacy=LegacyDefinition(name='section_topology'))

    x_charmm_input_units_store = Quantity(
        type=str,
        shape=[],
        description='''
        It determines the units of all quantities specified in the input script and data
        file, as well as quantities output to the screen, log file, and dump files.
        ''',
        a_legacy=LegacyDefinition(name='x_charmm_input_units_store'))

    x_charmm_data_bond_types_store = Quantity(
        type=np.dtype(np.int32),
        shape=[],
        description='''
        store temporarly
        ''',
        a_legacy=LegacyDefinition(name='x_charmm_data_bond_types_store'))

    x_charmm_data_bond_count_store = Quantity(
        type=np.dtype(np.int32),
        shape=[],
        description='''
        store temporarly
        ''',
        a_legacy=LegacyDefinition(name='x_charmm_data_bond_count_store'))

    x_charmm_data_angle_count_store = Quantity(
        type=np.dtype(np.int32),
        shape=[],
        description='''
        store temporarly
        ''',
        a_legacy=LegacyDefinition(name='x_charmm_data_angle_count_store'))

    x_charmm_data_atom_types_store = Quantity(
        type=np.dtype(np.int32),
        shape=[],
        description='''
        store temporarly
        ''',
        a_legacy=LegacyDefinition(name='x_charmm_data_atom_types_store'))

    x_charmm_data_dihedral_count_store = Quantity(
        type=np.dtype(np.int32),
        shape=[],
        description='''
        store temporarly
        ''',
        a_legacy=LegacyDefinition(name='x_charmm_data_dihedral_count_store'))

    x_charmm_data_angles_store = Quantity(
        type=str,
        shape=[],
        description='''
        store temporarly
        ''',
        a_legacy=LegacyDefinition(name='x_charmm_data_angles_store'))

    x_charmm_data_angle_list_store = Quantity(
        type=str,
        shape=[],
        description='''
        tmp
        ''',
        a_legacy=LegacyDefinition(name='x_charmm_data_angle_list_store'))

    x_charmm_data_bond_list_store = Quantity(
        type=str,
        shape=[],
        description='''
        tmp
        ''',
        a_legacy=LegacyDefinition(name='x_charmm_data_bond_list_store'))

    x_charmm_data_dihedral_list_store = Quantity(
        type=str,
        shape=[],
        description='''
        tmp
        ''',
        a_legacy=LegacyDefinition(name='x_charmm_data_dihedral_list_store'))

    x_charmm_data_dihedral_coeff_list_store = Quantity(
        type=str,
        shape=[],
        description='''
        tmp
        ''',
        a_legacy=LegacyDefinition(name='x_charmm_data_dihedral_coeff_list_store'))

    x_charmm_masses_store = Quantity(
        type=str,
        shape=[],
        description='''
        tmp
        ''',
        a_legacy=LegacyDefinition(name='x_charmm_masses_store'))

    x_charmm_data_topo_list_store = Quantity(
        type=str,
        shape=[],
        description='''
        tmp
        ''',
        a_legacy=LegacyDefinition(name='x_charmm_data_topo_list_store'))

    x_charmm_section_atom_to_atom_type_ref = SubSection(
        sub_section=SectionProxy('x_charmm_section_atom_to_atom_type_ref'),
        repeats=True,
        a_legacy=LegacyDefinition(name='x_charmm_section_atom_to_atom_type_ref'))


class section_frame_sequence(public.section_frame_sequence):

    m_def = Section(validate=False, extends_base_section=True, a_legacy=LegacyDefinition(name='section_frame_sequence'))

    x_charmm_number_of_volumes_in_sequence = Quantity(
        type=int,
        shape=[],
        description='''
        Gives the number of volumes in this sequence of frames, see
        x_charmm_frame_sequence_volume.
        ''',
        a_legacy=LegacyDefinition(name='x_charmm_number_of_volumes_in_sequence'))

    x_charmm_number_of_densities_in_sequence = Quantity(
        type=int,
        shape=[],
        description='''
        Gives the number of densities in this sequence of frames, see
        x_charmm_frame_sequence_density.
        ''',
        a_legacy=LegacyDefinition(name='x_charmm_number_of_densities_in_sequence'))

    x_charmm_number_of_bond_energies_in_sequence = Quantity(
        type=int,
        shape=[],
        description='''
        Gives the number of bond_energies in this sequence of frames, see
        x_charmm_frame_sequence_bond_energy.
        ''',
        a_legacy=LegacyDefinition(name='x_charmm_number_of_bond_energies_in_sequence'))

    x_charmm_number_of_urey_energies_in_sequence = Quantity(
        type=int,
        shape=[],
        description='''
        Gives the number of bond_energies in this sequence of frames, see
        x_charmm_frame_sequence_urey_energy.
        ''',
        a_legacy=LegacyDefinition(name='x_charmm_number_of_urey_energies_in_sequence'))

    x_charmm_number_of_high_frequency_correction_total_energies_in_sequence = Quantity(
        type=int,
        shape=[],
        description='''
        Gives the number of bond_energies in this sequence of frames, see
        x_charmm_frame_sequence_high_frequency_correction_total_energy.
        ''',
        a_legacy=LegacyDefinition(name='x_charmm_number_of_high_frequency_correction_total_energies_in_sequence'))

    x_charmm_number_of_high_frequency_correction_energies_in_sequence = Quantity(
        type=int,
        shape=[],
        description='''
        Gives the number of bond_energies in this sequence of frames, see
        x_charmm_frame_sequence_high_frequency_correction_energy.
        ''',
        a_legacy=LegacyDefinition(name='x_charmm_number_of_high_frequency_correction_energies_in_sequence'))

    x_charmm_number_of_high_frequency_correction_kinetic_energies_in_sequence = Quantity(
        type=int,
        shape=[],
        description='''
        Gives the number of bond_energies in this sequence of frames, see
        x_charmm_frame_sequence_high_frequency_correction_kinetic_energy.
        ''',
        a_legacy=LegacyDefinition(name='x_charmm_number_of_high_frequency_correction_kinetic_energies_in_sequence'))

    x_charmm_number_of_virial_kinetic_energies_in_sequence = Quantity(
        type=int,
        shape=[],
        description='''
        Gives the number of bond_energies in this sequence of frames, see
        x_charmm_frame_sequence_virial_kinetic_energy.
        ''',
        a_legacy=LegacyDefinition(name='x_charmm_number_of_virial_kinetic_energies_in_sequence'))

    x_charmm_number_of_angle_energies_in_sequence = Quantity(
        type=int,
        shape=[],
        description='''
        Gives the number of angle_energies in this sequence of frames, see
        x_charmm_frame_sequence_angle_energy.
        ''',
        a_legacy=LegacyDefinition(name='x_charmm_number_of_angle_energies_in_sequence'))

    x_charmm_number_of_proper_dihedral_energies_in_sequence = Quantity(
        type=int,
        shape=[],
        description='''
        Gives the number of proper_dihedral_energies in this sequence of frames, see
        x_charmm_frame_sequence_proper_dihedral_energy.
        ''',
        a_legacy=LegacyDefinition(name='x_charmm_number_of_proper_dihedral_energies_in_sequence'))

    x_charmm_number_of_improper_dihedral_energies_in_sequence = Quantity(
        type=int,
        shape=[],
        description='''
        Gives the number of improper_dihedral_energies in this sequence of frames, see
        x_charmm_frame_sequence_improper_dihedral_energy.
        ''',
        a_legacy=LegacyDefinition(name='x_charmm_number_of_improper_dihedral_energies_in_sequence'))

    x_charmm_number_of_cmap_dihedral_energies_in_sequence = Quantity(
        type=int,
        shape=[],
        description='''
        Gives the number of cmap_dihedral_energies in this sequence of frames, see
        x_charmm_frame_sequence_cmap_dihedral_energy.
        ''',
        a_legacy=LegacyDefinition(name='x_charmm_number_of_cmap_dihedral_energies_in_sequence'))

    x_charmm_number_of_vdw_energies_in_sequence = Quantity(
        type=int,
        shape=[],
        description='''
        Gives the number of vdw_energies in this sequence of frames, see
        x_charmm_frame_sequence_vdw_energy.
        ''',
        a_legacy=LegacyDefinition(name='x_charmm_number_of_vdw_energies_in_sequence'))

    x_charmm_number_of_boundary_energies_in_sequence = Quantity(
        type=int,
        shape=[],
        description='''
        Gives the number of boundary_energies in this sequence of frames, see
        x_charmm_frame_sequence_boundary_energy.
        ''',
        a_legacy=LegacyDefinition(name='x_charmm_number_of_boundary_energies_in_sequence'))

    x_charmm_number_of_electrostatic_energies_in_sequence = Quantity(
        type=int,
        shape=[],
        description='''
        Gives the number of electrostatic_energies in this sequence of frames, see
        x_charmm_frame_sequence_electrostatic_energy.
        ''',
        a_legacy=LegacyDefinition(name='x_charmm_number_of_electrostatic_energies_in_sequence'))

    x_charmm_number_of_total_energies_in_sequence = Quantity(
        type=int,
        shape=[],
        description='''
        Gives the number of total_energies in this sequence of frames, see
        x_charmm_frame_sequence_total_energy.
        ''',
        a_legacy=LegacyDefinition(name='x_charmm_number_of_total_energies_in_sequence'))

    x_charmm_number_of_total_kinetic_energies_in_sequence = Quantity(
        type=int,
        shape=[],
        description='''
        Gives the number of total_kinetic_energies in this sequence of frames, see
        x_charmm_frame_sequence_total_kinetic_energy_frames.
        ''',
        a_legacy=LegacyDefinition(name='x_charmm_number_of_total_kinetic_energies_in_sequence'))

    x_charmm_number_of_misc_energies_in_sequence = Quantity(
        type=int,
        shape=[],
        description='''
        Gives the number of misc_energies in this sequence of frames, see
        x_charmm_frame_sequence_misc_energy.
        ''',
        a_legacy=LegacyDefinition(name='x_charmm_number_of_misc_energies_in_sequence'))

    x_charmm_frame_sequence_density_frames = Quantity(
        type=np.dtype(np.int32),
        shape=['x_charmm_number_of_densities_in_sequence'],
        description='''
        Array containing the strictly increasing indices of the frames the
        x_charmm_frame_sequence_densities values refers to. If not given it defaults to
        the trivial mapping 0,1,...
        ''',
        a_legacy=LegacyDefinition(name='x_charmm_frame_sequence_density_frames'))

    x_charmm_frame_sequence_density = Quantity(
        type=np.dtype(np.float64),
        shape=['x_charmm_number_of_densities_in_sequence'],
        description='''
        Array containing the values of the density along this sequence of frames (i.e., a
        trajectory, a frame is one section_single_configuration_calculation). If not all
        frames have a value the indices of the frames that have a value are stored in
        frame_sequence_density_frames.
        ''',
        a_legacy=LegacyDefinition(name='x_charmm_frame_sequence_density'))

    x_charmm_frame_sequence_cmap_dihedral_energy_frames = Quantity(
        type=np.dtype(np.int32),
        shape=['x_charmm_number_of_cmap_dihedral_energy_in_sequence'],
        description='''
        Array containing the strictly increasing indices of the frames the
        x_charmm_frame_sequence_cmap_dihedral_energy values refers to. If not given it
        defaults to the trivial mapping 0,1,...
        ''',
        a_legacy=LegacyDefinition(name='x_charmm_frame_sequence_cmap_dihedral_energy_frames'))

    x_charmm_frame_sequence_cmap_dihedral_energy = Quantity(
        type=np.dtype(np.float64),
        shape=['x_charmm_number_of_cmap_dihedral_energy_in_sequence'],
        description='''
        Array containing the values of the cmap_dihedral_energy along this sequence of
        frames (i.e., a trajectory, a frame is one
        section_single_configuration_calculation). If not all frames have a value the
        indices of the frames that have a value are stored in
        frame_sequence_cmap_dihedral_energy_frames.
        ''',
        a_legacy=LegacyDefinition(name='x_charmm_frame_sequence_cmap_dihedral_energy'))

    x_charmm_frame_sequence_improper_dihedral_energy_frames = Quantity(
        type=np.dtype(np.int32),
        shape=['x_charmm_number_of_improper_dihedral_energy_in_sequence'],
        description='''
        Array containing the strictly increasing indices of the frames the
        x_charmm_frame_sequence_improper_dihedral_energy values refers to. If not given it
        defaults to the trivial mapping 0,1,...
        ''',
        a_legacy=LegacyDefinition(name='x_charmm_frame_sequence_improper_dihedral_energy_frames'))

    x_charmm_frame_sequence_improper_dihedral_energy = Quantity(
        type=np.dtype(np.float64),
        shape=['x_charmm_number_of_improper_dihedral_energy_in_sequence'],
        description='''
        Array containing the values of the improper_dihedral_energy along this sequence of
        frames (i.e., a trajectory, a frame is one
        section_single_configuration_calculation). If not all frames have a value the
        indices of the frames that have a value are stored in
        frame_sequence_improper_dihedral_energy_frames.
        ''',
        a_legacy=LegacyDefinition(name='x_charmm_frame_sequence_improper_dihedral_energy'))

    x_charmm_frame_sequence_proper_dihedral_energy_frames = Quantity(
        type=np.dtype(np.int32),
        shape=['x_charmm_number_of_proper_dihedral_energy_in_sequence'],
        description='''
        Array containing the strictly increasing indices of the frames the
        x_charmm_frame_sequence_proper_dihedral_energy values refers to. If not given it
        defaults to the trivial mapping 0,1,...
        ''',
        a_legacy=LegacyDefinition(name='x_charmm_frame_sequence_proper_dihedral_energy_frames'))

    x_charmm_frame_sequence_proper_dihedral_energy = Quantity(
        type=np.dtype(np.float64),
        shape=['x_charmm_number_of_proper_dihedral_energy_in_sequence'],
        description='''
        Array containing the values of the proper_dihedral_energy along this sequence of
        frames (i.e., a trajectory, a frame is one
        section_single_configuration_calculation). If not all frames have a value the
        indices of the frames that have a value are stored in
        frame_sequence_proper_dihedral_energy_frames.
        ''',
        a_legacy=LegacyDefinition(name='x_charmm_frame_sequence_proper_dihedral_energy'))

    x_charmm_frame_sequence_bond_energy_frames = Quantity(
        type=np.dtype(np.int32),
        shape=['x_charmm_number_of_bond_energies_in_sequence'],
        description='''
        Array containing the strictly increasing indices of the frames the
        x_charmm_frame_sequence_bond_energy values refers to. If not given it defaults to
        the trivial mapping 0,1,...
        ''',
        a_legacy=LegacyDefinition(name='x_charmm_frame_sequence_bond_energy_frames'))

    x_charmm_frame_sequence_urey_energy_frames = Quantity(
        type=np.dtype(np.int32),
        shape=['x_charmm_number_of_urey_energies_in_sequence'],
        description='''
        Array containing the strictly increasing indices of the frames the
        x_charmm_frame_sequence_urey_energy values refers to. If not given it defaults to
        the trivial mapping 0,1,...
        ''',
        a_legacy=LegacyDefinition(name='x_charmm_frame_sequence_urey_energy_frames'))

    x_charmm_frame_sequence_high_frequency_correction_total_energy_frames = Quantity(
        type=np.dtype(np.int32),
        shape=['x_charmm_number_of_high_frequency_correction_total_energies_in_sequence'],
        description='''
        Array containing the strictly increasing indices of the frames the
        x_charmm_frame_sequence_high_frequency_correction_total_energy values refers to.
        If not given it defaults to the trivial mapping 0,1,...
        ''',
        a_legacy=LegacyDefinition(name='x_charmm_frame_sequence_high_frequency_correction_total_energy_frames'))

    x_charmm_frame_sequence_high_frequency_correction_energy_frames = Quantity(
        type=np.dtype(np.int32),
        shape=['x_charmm_number_of_high_frequency_correction_energies_in_sequence'],
        description='''
        Array containing the strictly increasing indices of the frames the
        x_charmm_frame_sequence_high_frequency_correction_energy values refers to. If not
        given it defaults to the trivial mapping 0,1,...
        ''',
        a_legacy=LegacyDefinition(name='x_charmm_frame_sequence_high_frequency_correction_energy_frames'))

    x_charmm_frame_sequence_high_frequency_correction_kinetic_energy_frames = Quantity(
        type=np.dtype(np.int32),
        shape=['x_charmm_number_of_high_frequency_correction_kinetic_energies_in_sequence'],
        description='''
        Array containing the strictly increasing indices of the frames the
        x_charmm_frame_sequence_high_frequency_correction_kinetic_energy values refers to.
        If not given it defaults to the trivial mapping 0,1,...
        ''',
        a_legacy=LegacyDefinition(name='x_charmm_frame_sequence_high_frequency_correction_kinetic_energy_frames'))

    x_charmm_frame_sequence_virial_kinetic_energy_frames = Quantity(
        type=np.dtype(np.int32),
        shape=['x_charmm_number_of_virial_kinetic_energies_in_sequence'],
        description='''
        Array containing the strictly increasing indices of the frames the
        x_charmm_frame_sequence_virial_kinetic_energy values refers to. If not given it
        defaults to the trivial mapping 0,1,...
        ''',
        a_legacy=LegacyDefinition(name='x_charmm_frame_sequence_virial_kinetic_energy_frames'))

    x_charmm_frame_sequence_bond_energy = Quantity(
        type=np.dtype(np.float64),
        shape=['x_charmm_number_of_bond_energies_in_sequence'],
        description='''
        Array containing the values of the bond_energy along this sequence of frames
        (i.e., a trajectory, a frame is one section_single_configuration_calculation). If
        not all frames have a value the indices of the frames that have a value are stored
        in frame_sequence_bond_energy_frames.
        ''',
        a_legacy=LegacyDefinition(name='x_charmm_frame_sequence_bond_energy'))

    x_charmm_frame_sequence_urey_energy = Quantity(
        type=np.dtype(np.float64),
        shape=['x_charmm_number_of_urey_energies_in_sequence'],
        description='''
        Array containing the values of the urey_energy along this sequence of frames
        (i.e., a trajectory, a frame is one section_single_configuration_calculation). If
        not all frames have a value the indices of the frames that have a value are stored
        in frame_sequence_urey_energy_frames.
        ''',
        a_legacy=LegacyDefinition(name='x_charmm_frame_sequence_urey_energy'))

    x_charmm_frame_sequence_high_frequency_correction_total_energy = Quantity(
        type=np.dtype(np.float64),
        shape=['x_charmm_number_of_high_frequency_correction_total_energies_in_sequence'],
        description='''
        Array containing the values of the high_frequency_correction_total_energy along
        this sequence of frames (i.e., a trajectory, a frame is one
        section_single_configuration_calculation). If not all frames have a value the
        indices of the frames that have a value are stored in
        frame_sequence_high_frequency_correction_total_energy_frames.
        ''',
        a_legacy=LegacyDefinition(name='x_charmm_frame_sequence_high_frequency_correction_total_energy'))

    x_charmm_frame_sequence_high_frequency_correction_energy = Quantity(
        type=np.dtype(np.float64),
        shape=['x_charmm_number_of_high_frequency_correction_energies_in_sequence'],
        description='''
        Array containing the values of the high_frequency_correction_energy along this
        sequence of frames (i.e., a trajectory, a frame is one
        section_single_configuration_calculation). If not all frames have a value the
        indices of the frames that have a value are stored in
        frame_sequence_high_frequency_correction_energy_frames.
        ''',
        a_legacy=LegacyDefinition(name='x_charmm_frame_sequence_high_frequency_correction_energy'))

    x_charmm_frame_sequence_high_frequency_correction_kinetic_energy = Quantity(
        type=np.dtype(np.float64),
        shape=['x_charmm_number_of_high_frequency_correction_kinetic_energies_in_sequence'],
        description='''
        Array containing the values of the high_frequency_correction_kinetic_energy along
        this sequence of frames (i.e., a trajectory, a frame is one
        section_single_configuration_calculation). If not all frames have a value the
        indices of the frames that have a value are stored in
        frame_sequence_high_frequency_correction_kinetic_energy_frames.
        ''',
        a_legacy=LegacyDefinition(name='x_charmm_frame_sequence_high_frequency_correction_kinetic_energy'))

    x_charmm_frame_sequence_virial_kinetic_energy = Quantity(
        type=np.dtype(np.float64),
        shape=['x_charmm_number_of_virial_kinetic_energies_in_sequence'],
        description='''
        Array containing the values of the virial_kinetic_energy along this sequence of
        frames (i.e., a trajectory, a frame is one
        section_single_configuration_calculation). If not all frames have a value the
        indices of the frames that have a value are stored in
        frame_sequence_virial_kinetic_energy_frames.
        ''',
        a_legacy=LegacyDefinition(name='x_charmm_frame_sequence_virial_kinetic_energy'))

    x_charmm_frame_sequence_boundary_frames = Quantity(
        type=np.dtype(np.int32),
        shape=['x_charmm_number_of_boundary_energies_in_sequence'],
        description='''
        Array containing the strictly increasing indices of the frames the
        x_charmm_frame_sequence_boundary values refers to. If not given it defaults to the
        trivial mapping 0,1,...
        ''',
        a_legacy=LegacyDefinition(name='x_charmm_frame_sequence_boundary_frames'))

    x_charmm_frame_sequence_boundary = Quantity(
        type=np.dtype(np.float64),
        shape=['x_charmm_number_of_boundary_energies_in_sequence'],
        description='''
        Array containing the values of the boundary along this sequence of frames (i.e., a
        trajectory, a frame is one section_single_configuration_calculation). If not all
        frames have a value the indices of the frames that have a value are stored in
        frame_sequence_boundary_frames.
        ''',
        a_legacy=LegacyDefinition(name='x_charmm_frame_sequence_boundary'))

    x_charmm_frame_sequence_angle_energy_frames = Quantity(
        type=np.dtype(np.int32),
        shape=['x_charmm_number_of_angle_energies_in_sequence'],
        description='''
        Array containing the strictly increasing indices of the frames the
        x_charmm_frame_sequence_angle_energy values refers to. If not given it defaults to
        the trivial mapping 0,1,...
        ''',
        a_legacy=LegacyDefinition(name='x_charmm_frame_sequence_angle_energy_frames'))

    x_charmm_frame_sequence_angle_energy = Quantity(
        type=np.dtype(np.float64),
        shape=['x_charmm_number_of_angle_energies_in_sequence'],
        description='''
        Array containing the values of the angle_energy along this sequence of frames
        (i.e., a trajectory, a frame is one section_single_configuration_calculation). If
        not all frames have a value the indices of the frames that have a value are stored
        in frame_sequence_angle_energy_frames.
        ''',
        a_legacy=LegacyDefinition(name='x_charmm_frame_sequence_angle_energy'))

    x_charmm_frame_sequence_vdw_energy_frames = Quantity(
        type=np.dtype(np.int32),
        shape=['x_charmm_number_of_vdw_energies_in_sequence'],
        description='''
        Array containing the strictly increasing indices of the frames the
        x_charmm_frame_sequence_vdw_energy values refers to. If not given it defaults to
        the trivial mapping 0,1,...
        ''',
        a_legacy=LegacyDefinition(name='x_charmm_frame_sequence_vdw_energy_frames'))

    x_charmm_frame_sequence_vdw_energy = Quantity(
        type=np.dtype(np.float64),
        shape=['x_charmm_number_of_vdw_energies_in_sequence'],
        description='''
        Array containing the values of the vdw_energy along this sequence of frames (i.e.,
        a trajectory, a frame is one section_single_configuration_calculation). If not all
        frames have a value the indices of the frames that have a value are stored in
        frame_sequence_vdw_energy_frames.
        ''',
        a_legacy=LegacyDefinition(name='x_charmm_frame_sequence_vdw_energy'))

    x_charmm_frame_sequence_electrostatic_energy_frames = Quantity(
        type=np.dtype(np.int32),
        shape=['x_charmm_number_of_electrostatic_energies_in_sequence'],
        description='''
        Array containing the strictly increasing indices of the frames the
        x_charmm_frame_sequence_electrostatic_energy values refers to. If not given it
        defaults to the trivial mapping 0,1,...
        ''',
        a_legacy=LegacyDefinition(name='x_charmm_frame_sequence_electrostatic_energy_frames'))

    x_charmm_frame_sequence_electrostatic_energy = Quantity(
        type=np.dtype(np.float64),
        shape=['x_charmm_number_of_electrostatic_energies_in_sequence'],
        description='''
        Array containing the values of the electrostatic_energy along this sequence of
        frames (i.e., a trajectory, a frame is one
        section_single_configuration_calculation). If not all frames have a value the
        indices of the frames that have a value are stored in
        frame_sequence_electrostatic_energy_frames.
        ''',
        a_legacy=LegacyDefinition(name='x_charmm_frame_sequence_electrostatic_energy'))

    x_charmm_frame_sequence_total_energy_frames = Quantity(
        type=np.dtype(np.int32),
        shape=['x_charmm_number_of_total_energies_in_sequence'],
        description='''
        Array containing the strictly increasing indices of the frames the
        x_charmm_frame_sequence_total_energy values refers to. If not given it defaults to
        the trivial mapping 0,1,...
        ''',
        a_legacy=LegacyDefinition(name='x_charmm_frame_sequence_total_energy_frames'))

    x_charmm_frame_sequence_total_energy = Quantity(
        type=np.dtype(np.float64),
        shape=['x_charmm_number_of_total_energies_in_sequence'],
        description='''
        Array containing the values of the total_energy along this sequence of frames
        (i.e., a trajectory, a frame is one section_single_configuration_calculation). If
        not all frames have a value the indices of the frames that have a value are stored
        in frame_sequence_total_energy_frames.
        ''',
        a_legacy=LegacyDefinition(name='x_charmm_frame_sequence_total_energy'))

    x_charmm_frame_sequence_total_kinetic_energy_frames = Quantity(
        type=np.dtype(np.int32),
        shape=['x_charmm_number_of_total_kinetic_energies_in_sequence'],
        description='''
        Array containing the strictly increasing indices of the frames the
        x_charmm_frame_sequence_total_kinetic_energy values refers to. If not given it
        defaults to the trivial mapping 0,1,...
        ''',
        a_legacy=LegacyDefinition(name='x_charmm_frame_sequence_total_kinetic_energy_frames'))

    x_charmm_frame_sequence_total_kinetic_energy = Quantity(
        type=np.dtype(np.float64),
        shape=['x_charmm_number_of_total_kinetic_energies_in_sequence'],
        description='''
        Array containing the values of the total_kinetic_energy along this sequence of
        frames (i.e., a trajectory, a frame is one
        section_single_configuration_calculation). If not all frames have a value the
        indices of the frames that have a value are stored in
        frame_sequence_total_kinetic_energy_frames.
        ''',
        a_legacy=LegacyDefinition(name='x_charmm_frame_sequence_total_kinetic_energy'))

    x_charmm_frame_sequence_misc_energy_frames = Quantity(
        type=np.dtype(np.int32),
        shape=['x_charmm_number_of_misc_energies_in_sequence'],
        description='''
        Array containing the strictly increasing indices of the frames the
        x_charmm_frame_sequence_misc_energy values refers to. If not given it defaults to
        the trivial mapping 0,1,...
        ''',
        a_legacy=LegacyDefinition(name='x_charmm_frame_sequence_misc_energy_frames'))

    x_charmm_frame_sequence_misc_energy = Quantity(
        type=np.dtype(np.float64),
        shape=['x_charmm_number_of_misc_energies_in_sequence'],
        description='''
        Array containing the values of the misc_energy along this sequence of frames
        (i.e., a trajectory, a frame is one section_single_configuration_calculation). If
        not all frames have a value the indices of the frames that have a value are stored
        in frame_sequence_misc_energy_frames.
        ''',
        a_legacy=LegacyDefinition(name='x_charmm_frame_sequence_misc_energy'))

    x_charmm_frame_sequence_volume_frames = Quantity(
        type=np.dtype(np.int32),
        shape=['x_charmm_number_of_volumes_in_sequence'],
        description='''
        Array containing the strictly increasing indices of the frames the
        x_charmm_frame_sequence_volume values refers to. If not given it defaults to the
        trivial mapping 0,1,...
        ''',
        a_legacy=LegacyDefinition(name='x_charmm_frame_sequence_volume_frames'))

    x_charmm_frame_sequence_volume = Quantity(
        type=np.dtype(np.float64),
        shape=['x_charmm_number_of_volumes_in_sequence'],
        description='''
        Array containing the values of the volume along this sequence of frames (i.e., a
        trajectory, a frame is one section_single_configuration_calculation). If not all
        frames have a value the indices of the frames that have a value are stored in
        frame_sequence_volume_frames.
        ''',
        a_legacy=LegacyDefinition(name='x_charmm_frame_sequence_volume'))


class section_single_configuration_calculation(public.section_single_configuration_calculation):

    m_def = Section(validate=False, extends_base_section=True, a_legacy=LegacyDefinition(name='section_single_configuration_calculation'))

    x_charmm_section_single_configuration_calculation = SubSection(
        sub_section=SectionProxy('x_charmm_section_single_configuration_calculation'),
        repeats=True,
        a_legacy=LegacyDefinition(name='x_charmm_section_single_configuration_calculation'))


m_package.__init_metainfo__()
