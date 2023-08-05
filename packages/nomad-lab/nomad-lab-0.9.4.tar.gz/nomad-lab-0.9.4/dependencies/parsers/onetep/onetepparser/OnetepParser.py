# Copyright 2016-2018 Martina Stella, Fawzi Mohamed
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

from __future__ import division
from builtins import str
from builtins import range
from builtins import object
import numpy as np
import math
import nomadcore.ActivateLogging
from nomadcore.caching_backend import CachingLevel
from nomadcore.simple_parser import AncillaryParser, mainFunction
from nomadcore.simple_parser import SimpleMatcher as SM
from .OnetepCommon import get_metaInfo
from . import OnetepCellParser, OnetepBandParser, OnetepMDParser, OnetepTSParser
import logging, os, re, sys


################################################################################################################################################################
################################################################################################################################################################
################################################################################################################################################################
######################  PARSER CONTEXT CLASS  ##################################################################################################################
################################################################################################################################################################
############################################################################ onetep.Parser Version 1.0 #########################################################
################################################################################################################################################################

logger = logging.getLogger("nomad.OnetepParser")

class OnetepParserContext(object):

    def __init__(self):
        """ Initialise variables used within the current superContext """
        self.secMethodIndex =[]
        self.secSystemDescriptionIndex =[]
        self.functionals                       = []
        self.func_total                        = []
        self.relativistic                      = []
        #self.dispersion                        = []
        self.cell                              = []
        self.at_nr                             = 0
        self.atom_type_mass                    = []
        self.atom_labels                       = []
        self.atom_optim_position = []
        self.onetep_optimised_atom_positions   = []
        self.onetep_atom_optim_label           = []
        self.atom_forces                       = []
        self.atom_forces_band                       = []
        self.stress_tensor_value               = []
        self.raman_tensor_value               = []
        self.onetep_atom_positions              = []
        self.atom_positions                     = []
        self.a                                 = []
        self.b                                 = []
        self.c                                 = []
        self.alpha                             = []
        self.beta                              = []
        self.gamma                             = []
        self.volume                            = 0
        self.time_calc                         = 0
        self.time_calculation                  = []
        self.energy_total_scf_iteration_list   = []
        self.scfIterNr                         = []
        self.functional_type                   = []
        self.functional_weight                 = None
        self.k_nr                              = 0
        self.e_nr                              = 0
        self.k_count_1                         = 0
        self.k_nr_1                            = 0
        self.e_nr_1                            = 0
        self.onetep_band_kpoints               = []
        self.onetep_band_energies              = []
        self.onetep_band_kpoints_1             = []
        self.onetep_band_energies_1            = []
        self.k_path_nr                         = 0
        self.band_en                           = []
        self.van_der_waals_name                = None
        self.e_spin_1                          = []
        self.e_spin_2                          = []
        self.optim_method                      = []
        self.disp_energy                       = []
        self.geoConvergence = None
        self.total_energy_corrected_for_finite_basis = []
        self.contr_s = []
        self.contr_p = []
        self.contr_d = []
        self.contr_f = []
        self.total_contribution = []
        self.total_charge = []
        self.frequencies = []
        self.ir_intens = []
        self.raman_act = []
        self.irr_repres = []
        self.nr_iter =[]
        self.onetep_atom_velocities = []
        self.time_0 = []
        self.frame_temp = []
        self.frame_press =[]
        self.frame_potential =[]
        self.frame_total_energy = []
        self.frame_hamiltonian = []
        self.frame_kinetic = []
        self.frame_atom_forces=[]
        self.frame_atom_lables =[]
        self.frame_stress_tensor =[]
        self.frame_position =[]
        self.frame_cell=[]
        self.energy_frame_gain = []
        self.frame_time=[]
        self.energy_frame =[]
        self.total_energy_frame = []
        self.frame_energies =[]
        self.secMethodIndex =[]
        self.scfgIndex=[]
        self.n_spin_channels = []
        self.n_spin_channels_bands = []
        self.energy_frame_free = []
        self.energy_frame_T0 = []
        self.scf_conv_thresh = []
        self.n_iteration = []
        self.wall_time_end =[]
        self.initial_scf_iter_time = []
        self.ts_total_energy = []
        self.ts_cell_vector = []
        self.ts_forces = []
        self.ts_positions = []
        self.ts_path =[]
        self.ts_total_energy_f = []
        self.ts_cell_vector_f = []
        self.ts_forces_f = []
        self.ts_positions_f = []
        self.ts_path_f =[]
        self.ts_total_energy_p = []
        self.ts_cell_vector_p = []
        self.ts_forces_p = []
        self.ts_positions_p = []
        self.ts_path_p =[]
        self.total_spin_mulliken = []
        self.kinetic = []
        self.local_pseudo = []
        self.nonlocal_pseudo = []
        self.pen =[]
        self.Hartree = []
        self.Exchangecorrelation = []
        self.Ewald = []
        self.DispersionCorrection =[]
        self.Integrateddensity = []
        self.step =[]
        self.excitations =[]
        self.gindexsis=[]
        self.oscill_str =[]
        self.life_time =[]
        self.tddft_energy =[]
        self.number_of_atoms =[]
        self.basis_set_kind = []
        self.basis_set_name=[]
    def onClose_x_onetep_section_tddft(self, backend, gIndex, section):
        energies =['x_onetep_tddft_energy_store']
        if energies:
            self.tddft_energy =[]
    def initialize_values(self):
        """ Initializes the values of variables in superContexts that are used to parse different files """
        self.pippo = None
        self.at_nr_opt = None
    def startedParsing(self, fInName, parser):
        """Function is called when the parsing starts.

        Get compiled parser, filename and metadata.

        Args:
            fInName: The file name on which the current parser is running.
            parser: The compiled parser. Is an object of the class SimpleParser in nomadcore.simple_parser.py.
        """
        self.parser = parser
        self.fName = fInName
        # save metadata
        self.metaInfoEnv = self.parser.parserBuilder.metaInfoEnv
        # allows to reset values if the same superContext is used to parse different files
        self.initialize_values()

    def onClose_section_topology(self, backend, gIndex, section):
    # Processing the atom masses and type
        #get cached values of onetep_store_atom_mass and type
        mass = section['x_onetep_store_atom_mass']
        name = section['x_onetep_store_atom_name']

        n_ngwf = section['x_onetep_n_ngwf_atom_store']
        radius = section['x_onetep_ngwf_radius_store']
        if mass:
            for i in range(len(mass)):
                #converting mass in Kg from AMU
                # mass[i] = float(mass[i]) * 1.66053904e-27

                backend.openSection('section_atom_type')
                backend.addValue('atom_type_mass', float(mass[i]))
                backend.addValue('atom_type_name', name[i])
                backend.closeSection('section_atom_type', gIndex+i)
                backend.addValue('x_onetep_n_ngwf_atom', n_ngwf[i])
                backend.addValue('x_onetep_ngwf_radius', radius[i])
# Translating the XC functional name to the NOMAD standard
    def onClose_x_onetep_section_functionals(self, backend, gIndex, section):
        """When all the functional definitions have been gathered, matches them
        with the nomad correspondents and combines into one single string which
        is put into the backend.
        """
        # Get the list of functional and relativistic names
        functional_names = section["x_onetep_functional_name"]

        #relativistic_names = section["onetep_relativity_treatment_scf"]


        functional_map = {
            "PBE": "GGA_C_PBE_GGA_X_PBE",
            "LDA": "LDA_C_PZ_LDA_X_PZ",
            "PW91": "GGA_C_PW91_GGA_X_PW91",
            "PW92": "GGA_C_PW92_GGA_X_PW92",
            "GGA": "GGA_X_PBE",
            "CAPZ": "LDA_C_PZ",
            "VWN": "LDA_C_VWN",
            "PBESOL": "GGA_X_PBE_SOL",
            "RPBE": "GGA_X_RPBE",
            "REVPBE":"GGA_X_PBE_R",
            "BLYP":"GGA_X_B88_GGA_C_LYP",
            "XLYP":"GGA_XC_XLYP",
            "OPTB88":"GGA_X_OPTB88_VDW_LDA_C_PZ",
            "OPTPBE":"GGA_X_OPTPBE_VDW_LDA_C_PZ",
            "VDWDF":"GGA_X_PBE_R_VDW_LDA_C_PZ",
            "VDWDF2":"GGA_X_RPW86_LDA_C_PZ",
            "VV10":"HYB_GGA_XC_LC_VV10",
            "AVV10S":"GGA_X_AM05_GGA_C_AM05_rVV10-sol",

        }


        # Match each onetep functional name and sort the matches into a list
        self.functionals = []

        for name in functional_names:
            match = functional_map.get(name)
            if match:
                self.functionals.append(match)

        # self.functionals = "_".join(sorted(self.functionals))



    def onClose_x_onetep_section_relativity_treatment(self, backend, gIndex, section):
        relativistic_names = section["x_onetep_relativity_treatment_scf"]

        # Define a mapping for the relativistic treatments
        relativistic_map = {
            " Koelling-Harmon": "scalar_relativistic"
        }
        self.relativistic = []

        for name in relativistic_names:
            match = relativistic_map.get(name)
            if match:
                self.relativistic.append(match)
        self.relativistic = "_".join(sorted(self.relativistic))
# Here we add info about the XC functional and relativistic treatment

    def onClose_x_onetep_section_geom_optimisation_method(self, backend, gIndex, section):
        self.optim_method = section["x_onetep_geometry_optim_method"]

    def onClose_x_onetep_section_kernel_parameters(self, backend, gIndex, section):
        self.diis_scheme_type = section["x_onetep_kernel_diis_type_store"]
        if self.diis_scheme_type is not None:
            diis_map = {
            "DKN_LINEAR": "linear mixing of density kernels",
            "HAM_LINEAR": "linear mixing of density kernels",
            "DKN_PULAY" : "Pulay mixing of density kernels",
            "HAM_PULAY" : "Pulay mixing of Hamiltonians",
            "DKN_LISTI": "LiSTi mixing of density kernels",
            "HAM_LISTI": "LiSTi mixing of Hamiltonians",
            "DKN_LISTB" : "LiSTb mixing of density kernels",
            "HAM_LISTB" : "LiSTb mixing of Hamiltonians",
            "DIAG" : "nomixing",
            }
            self.diis = []
            for name in self.diis_scheme_type:
                match = diis_map.get(name)
                if match:
                    self.diis.append(match)
            backend.addValue('x_onetep_kernel_diis_type',self.diis)


    def onClose_x_onetep_section_van_der_Waals_parameters(self, backend, gIndex, section):
        self.van_der_waals_name = section["x_onetep_disp_method_name_store"]
        self.dispersion = []

        if self.van_der_waals_name is not None:
            dispersion_map = {
            "1": "Elstner",
            "2": "First damping function from Wu and Yang",
            "3" : "Second damping function from Wu and Yang ",
            "4" : "D2 Grimme",
            }
            #self.dispersion = []
            for name in self.van_der_waals_name:
                match = dispersion_map.get(name)
                if match:
                    self.dispersion.append(match)
            self.dispersion = "_".join(sorted(self.dispersion))
            self.disp = str(self.dispersion)
            method_index = backend.openSection('section_method')
            backend.addValue('van_der_Waals_method',self.disp)
            backend.closeSection('section_method',method_index)


    def onClose_section_method(self, backend, gIndex, section):

        #self.disp1 = section['van_der_Waals_method']

        self.disp1= None
        if self.functional_weight is not None:
            self.func_and_weight = []
            for i in range(len(self.functional_types)):
                self.func_total.append(self.functionals[i]+'_'+self.functional_weight[i])
                xc_functionals_index = backend.openSection('section_XC_functionals')
                backend.addValue('XC_functional_name', self.functionals[i])
                backend.addValue('XC_functional_weight', self.functional_weight[i])
                backend.closeSection('section_XC_functionals', xc_functionals_index)
        # Push the functional string into the backend
        # Push the relativistic treatment string into the backend
            backend.addValue('XC_functional', "_".join(sorted(self.functionals)))
            # backend.addValue('relativity_method', self.relativistic)
        #if self.functional_weight = 0

            if self.disp1 is not None:

                backend.addValue('XC_method_current', ("_".join(sorted(self.func_total)))+'_'+self.disp1+'_'+self.relativistic)
            else:
                backend.addValue('XC_method_current', ("_".join(sorted(self.func_total)))+'_'+self.relativistic)
        else:
            for i in range(len(self.functionals)):
          #      self.func_total.append(self.functionals[i]+'_'+self.functional_weight[i])
                xc_functionals_index = backend.openSection('section_XC_functionals')
                backend.addValue('XC_functional_name', self.functionals[i])
         #       backend.addValue('XC_functional_weight', self.functional_weight[i])
                backend.closeSection('section_XC_functionals', xc_functionals_index)
            backend.addValue('XC_functional', "_".join(sorted(self.functionals)))
            # backend.addValue('relativity_method', self.relativistic)
            if self.disp1 is not None:
                backend.addValue('XC_method_current', ("_".join(sorted(self.functionals)))+'_'+self.disp1
                    +'_'+self.relativistic)
            else:
                backend.addValue('XC_method_current', ("_".join(sorted(self.functionals))))

        if self.n_spin_channels:
            backend.addValue('number_of_spin_channels', self.n_spin_channels[0])





# Here we add basis set name and kind for the plane wave code
    def onClose_section_basis_set_cell_dependent(self, backend, gIndex, section):
        ecut_str = section['x_onetep_basis_set_planewave_cutoff']
        self.ecut = float(ecut_str[0])
        eVtoRy = 0.073498618
        ecut_str_name = int(round(eVtoRy*self.ecut))

        self.basis_set_kind = 'psinc functions'
        self.basis_set_name = 'psinc functions'
        backend.addValue('basis_set_planewave_cutoff', self.ecut)
        backend.addValue('basis_set_cell_dependent_kind', self.basis_set_kind)
        backend.addValue('basis_set_cell_dependent_name', self.basis_set_name)

#     def onClose_x_onetep_section_cell_optim(self, backend, gIndex, section):
#         """trigger called when _onetep_section_cell is closed"""
#         # get cached values for onetep_cell_vector
#         vet = section['x_onetep_cell_vector_optim']

#         vet[0] = vet[0].split()
#         vet[0] = [float(i) for i in vet[0]]

#         vet[1] = vet[1].split()
#         vet[1] = [float(i) for i in vet[1]]

#         vet[2] = vet[2].split()
#         vet[2] = [float(i) for i in vet[2]]

#         self.cell.append(vet[0])
#         self.cell.append(vet[1])
#         self.cell.append(vet[2]) # Reconstructing the unit cell vector by vector


# # # Here we recover the unit cell dimensions (both magnitudes and angles) (useful to convert fractional coordinates to cartesian)
# #     def onClose_x_onetep_section_atom_positions(self, backend, gIndex, section):
# #         """trigger called when _onetep_section_atom_positions is closed"""
# #         # get cached values for cell magnitudes and angles
# #         self.a = section['x_onetep_cell_length_a']
# #         self.b = section['x_onetep_cell_length_b']
# #         self.c = section['x_onetep_cell_length_c']
# #         self.alpha = section['x_onetep_cell_angle_alpha']
# #         self.beta  = section['x_onetep_cell_angle_beta']
# #         self.gamma = section['x_onetep_cell_angle_gamma']
# #         self.volume = np.sqrt( 1 - math.cos(np.deg2rad(self.alpha[0]))**2
# #                                  - math.cos(np.deg2rad(self.beta[0]))**2
# #                                  - math.cos(np.deg2rad(self.gamma[0]))**2
# #                                  + 2 * math.cos(np.deg2rad(self.alpha[0]))
# #                                      * math.cos(np.deg2rad(self.beta[0]))
# #                                      * math.cos(np.deg2rad(self.gamma[0])) ) * self.a[0]*self.b[0]*self.c[0]

    def onClose_x_onetep_section_atom_positions_optim(self, backend, gIndex, section):
        """trigger called when _onetep_section_atom_positions is closed"""
        # get cached values for cell magnitudes and angles

        self.a = section['x_onetep_cell_length_a_optim']
        self.b = section['x_onetep_cell_length_b_optim']
        self.c = section['x_onetep_cell_length_c_optim']
        self.alpha = section['x_onetep_cell_angle_alpha_optim']
        self.beta  = section['x_onetep_cell_angle_beta_optim']
        self.gamma = section['x_onetep_cell_angle_gamma_optim']
        self.volume = np.sqrt( 1 - math.cos(np.deg2rad(self.alpha[0]))**2
                                 - math.cos(np.deg2rad(self.beta[0]))**2
                                 - math.cos(np.deg2rad(self.gamma[0]))**2
                                 + 2 * math.cos(np.deg2rad(self.alpha[0]))
                                     * math.cos(np.deg2rad(self.beta[0]))
                                     * math.cos(np.deg2rad(self.gamma[0])) ) * self.a[0]*self.b[0]*self.c[0]

# Storing the total energy of each SCF iteration in an array


# Processing forces acting on atoms (final converged forces)
    def onClose_section_single_configuration_calculation(self, backend, gIndex, section):
        # self.energy_total_scf_iteration_list = []
        # backend.addValue('x_onetep_ts_index', gIndex)
        self.time_0 = section['x_onetep_frame_time_0']
        self.numb_iter = section['x_onetep_number_of_scf_iterations_store']
        self.initial_scf_iter_time = section['x_onetep_initial_scf_iteration_wall_time']
        hrbohr_to_N = float(8.238723e-8)
        hrang_to_N = float(4.359745e-8)
        f_st = section['x_onetep_store_atom_forces']
        f_ion = section['x_onetep_store_atom_ionforces']
        f_local=section['x_onetep_store_atom_localforces']
        f_nonlocal=section['x_onetep_store_atom_nonlocalforces']
        f_noself=section['x_onetep_store_atom_nonselfforces']
        f_correc=section['x_onetep_store_atom_corrforces']
        if f_st:# and self.at_nr_opt is not None:

            for i in range(0, len(f_st)):
                f_st[i] = f_st[i].split()
                f_st[i] = [float(j) for j in f_st[i]]

                f_st_int = f_st[i]
                if self.numb_iter:
                    f_st_int = [x * hrbohr_to_N for x in f_st_int]
                else:
                    f_st_int = [x * hrang_to_N for x in f_st_int]

                self.atom_forces.append(f_st_int)

                self.atom_forces = self.atom_forces[-self.number_of_atoms[0][0]:]

            backend.addArrayValues('atom_forces', np.asarray(self.atom_forces))

        if f_ion is not None:# and self.at_nr_opt is not None:
            for i in range(0, len(f_ion)):
                f_ion[i] = f_ion[i].split()
                f_ion[i] = [float(j) for j in f_ion[i]]
                f_ion_int = f_ion[i]
                f_ion_int = [x * hrang_to_N for x in f_ion_int]
                self.atom_forces_ion = []
                self.atom_forces_ion.extend(f_ion)

                self.atom_forces_ion = self.atom_forces_ion[-len(f_ion):]

            backend.addArrayValues('x_onetep_atom_ionforces', np.asarray(self.atom_forces_ion))
        if f_local is not None:# and self.at_nr_opt is not None:
            for i in range(0, len(f_local)):
                f_local[i] = f_local[i].split()
                f_local[i] = [float(j) for j in f_local[i]]
                f_local_int = f_local[i]
                f_local_int = [x * hrang_to_N for x in f_local_int]
                self.atom_forces_local = []
                self.atom_forces_local.extend(f_local)

                self.atom_forces_local = self.atom_forces_local[-len(f_local):]

            backend.addArrayValues('x_onetep_atom_local_potentialforces', np.asarray(self.atom_forces_local))
        if f_nonlocal is not None:# and self.at_nr_opt is not None:
            for i in range(0, len(f_nonlocal)):
                f_nonlocal[i] = f_nonlocal[i].split()
                f_nonlocal[i] = [float(j) for j in f_nonlocal[i]]
                f_nonlocal_int = f_nonlocal[i]
                f_nonlocal_int = [x * hrang_to_N for x in f_nonlocal_int]
                self.atom_forces_nonlocal = []
                self.atom_forces_nonlocal.extend(f_nonlocal)

                self.atom_forces_nonlocal = self.atom_forces_nonlocal[-len(f_nonlocal):]

            backend.addArrayValues('x_onetep_atom_nonlocal_potentialforces', np.asarray(self.atom_forces_nonlocal))

        if f_noself is not None:# and self.at_nr_opt is not None:
            for i in range(0, len(f_noself)):
                f_noself[i] = f_noself[i].split()
                f_noself[i] = [float(j) for j in f_noself[i]]
                f_noself_int = f_noself[i]
                f_noself_int = [x * hrang_to_N for x in f_noself_int]
                self.atom_forces_nonself = []
                self.atom_forces_nonself.extend(f_noself)

                self.atom_forces_nonself = self.atom_forces_nonself[-len(f_noself):]

            backend.addArrayValues('x_onetep_atom_nonself_forces',np.asarray(self.atom_forces_nonself))

        if f_correc is not None:# and self.at_nr_opt is not None:
            for i in range(0, len(f_correc)):
                f_correc[i] = f_correc[i].split()
                f_correc[i] = [float(j) for j in f_correc[i]]
                f_correc_int = f_correc[i]
                f_correc_int = [x * hrang_to_N for x in f_correc_int]
                self.atom_forces_correc = []
                self.atom_forces_correc.extend(f_correc)

                self.atom_forces_correc = self.atom_forces_correc[-len(f_correc):]

            backend.addArrayValues('x_onetep_atom_correction_forces',np.asarray(self.atom_forces_correc))

        for i in range(len(self.n_spin_channels)):
            if self.n_spin_channels[i]==1:

                backend.openSection('section_eigenvalues') # opening first section_eigenvalues
                backend.addArrayValues('eigenvalues_kpoints', np.asarray(self.k_points_scf))
                backend.addArrayValues('eigenvalues_values', np.asarray(self.e_spin_1))
                backend.addValue('number_of_eigenvalues_kpoints', self.k_nr_scf)
                backend.addValue('number_of_eigenvalues', self.e_nr_scf)
                backend.closeSection('section_eigenvalues', gIndex)

            if self.n_spin_channels[i]==2:
                # print self.n_spin_channels,'ciao'
                # self.e_spin_2.(self.e_spin_1)
                both_spin = [[self.e_spin_2],[self.e_spin_1]]
                #
                backend.openSection('section_eigenvalues') # opening the second section_eigenvalues (only for spin polarised calculations)
                backend.addArrayValues('eigenvalues_kpoints', np.asarray(self.k_points_scf))
                backend.addArrayValues('eigenvalues_values', np.asarray(both_spin))
                backend.addValue('number_of_eigenvalues_kpoints', self.k_nr_scf)
                backend.addValue('number_of_eigenvalues', self.e_nr_scf)

                backend.closeSection('section_eigenvalues', gIndex)


        #backend.openSection('section_stress_tensor')
        # if self.stress_tensor_value:
            # backend.addArrayValues('stress_tensor',np.asarray(self.stress_tensor_value))
        #backend.closeSection('section_stress_tensor', gIndex)
        #backend.addValue('time_calculation', self.time_calc)

        #######Total Dispersion energy recovered from totatl energy. ##############
        # if self.dispersion is not None:
        #     van_der_waals_energy = section['x_onetep_total_dispersion_corrected_energy']
        #     total_energy = section['energy_total']
        #     for i in range(len(total_energy)):
        #         self.disp_energy = abs(van_der_waals_energy[i] - total_energy[i])
        #     backend.addValue('energy_van_der_Waals', self.disp_energy)


        finite_basis_corr_energy = section['x_onetep_total_energy_corrected_for_finite_basis_store'] ###Conversion to Jule
        J_converter = 1.602176565e-19
        J_float = float(J_converter)

        if finite_basis_corr_energy:
            finite_basis_corr_energy[0] = float(finite_basis_corr_energy[0]) * J_float
            backend.addValue('x_onetep_total_energy_corrected_for_finite_basis', finite_basis_corr_energy[0])

        if self.secMethodIndex:
            backend.addValue('single_configuration_to_calculation_method_ref', self.secMethodIndex)
        elif self.gindexsis:
            backend.addValue('single_configuration_to_calculation_method_ref', self.gindexsis)
        if self.secSystemDescriptionIndex is not None:
            backend.addValue('single_configuration_calculation_to_system_ref', self.secSystemDescriptionIndex)
        # extFile = ".md"       # Find the file with extension .cell
        # dirName = os.path.dirname(os.path.abspath(self.fName))
        # cFile = str()
        # for file in os.listdir(dirName):
        #     if file.endswith(extFile):
        #         cFile = file
        # fName = os.path.normpath(os.path.join(dirName, cFile))



        #  # parsing *.cell file to get the k path segments
        # if file.endswith(extFile):
        #     pass
        # else:
        #     if self.numb_iter:
        #         backend.addValue('number_of_scf_iterations', self.numb_iter[-1])
        #     else:
        #         backend.addValue('number_of_scf_iterations', len(self.energy_total_scf_iteration_list))



        Hr_J_converter = float(4.35974e-18)

        if self.local_pseudo:
            backend.addValue('x_onetep_pseudo_local',self.local_pseudo[0]*Hr_J_converter)
        if self.kinetic:
            backend.addValue('electronic_kinetic_energy',self.kinetic[0]*Hr_J_converter)
        if self.nonlocal_pseudo:
            backend.addValue('x_onetep_pseudo_non_local',self.nonlocal_pseudo[0]*Hr_J_converter)
        if self.Hartree:
            backend.addValue('energy_correction_hartree',self.Hartree[0]*Hr_J_converter)
        if self.Exchangecorrelation:
            backend.addValue('energy_XC',self.Exchangecorrelation[0]*Hr_J_converter)
        if self.Ewald:
            backend.addValue('x_onetep_ewald_correction',self.Ewald[0]*Hr_J_converter)
        if self.DispersionCorrection:
            backend.addValue('x_onetep_dispersion_correction',self.DispersionCorrection[0]*Hr_J_converter)
        if self.Integrateddensity:
            backend.addValue('x_onetep_integrated_density',self.Integrateddensity[0])




    def onClose_section_scf_iteration(self, backend, gIndex, section):
        """trigger called when _section_scf_iteration is closed"""
        # get cached values for energy_total_scf_iteration

        ev = section['energy_total_scf_iteration']

        if ev:

            self.scfIterNr = len(ev)
            self.energy_total_scf_iteration_list.append(ev)



    def onClose_x_onetep_section_SCF_iteration_frame(self, backend, gIndex, section):

        self.frame_free_energy = section['x_onetep_frame_energy_free']
        self.frame_energies = section['x_onetep_SCF_frame_energy']
        self.frame_energies_gain = section['x_onetep_SCF_frame_energy_gain']
        self.frame_T0 = section ['x_onetep_frame_energy_total_T0']
        self.wall_time_store = section ['x_onetep_frame_time_scf_iteration_wall_end']

        frame_time = section['x_onetep_frame_time']


        if self.frame_energies:

            for i in range(len(self.frame_energies)):

                J_converter = float(1.602176565e-19)

                self.frame_energies[i]=self.frame_energies[i].split()
                self.frame_energies[i]=[float(j) for j in self.frame_energies[i]]

                self.frame_energies_gain[i]=self.frame_energies_gain[i].split()
                self.frame_energies_gain[i]=[float(j) for j in self.frame_energies_gain[i]]

                self.wall_time_store[i] = self.wall_time_store[i].split()
                self.wall_time_store[i]=[float(j) for j in self.wall_time_store[i]]
                wall_times = self.wall_time_store[i]

                energies = self.frame_energies[i] ###Conversion to Jule
                energies = [x * J_converter for x in energies]

                energies_gain = self.frame_energies_gain[i] ###Conversion to Jule
                energies_gain = [x * J_converter for x in energies_gain]

                self.energy_frame.extend(energies)

                self.energy_frame_gain.extend(energies_gain)

                self.wall_time_end.extend(wall_times)

            free_energies = self.frame_free_energy
            free_energies = [x * J_converter for x in free_energies]
            self.energy_frame_free.extend(free_energies)

            t0_energies = self.frame_T0
            t0_energies = [x * J_converter for x in t0_energies]
            self.energy_frame_T0.extend(t0_energies)


            if frame_time:
                for i in range(len(frame_time)):
                    self.time_0.extend(frame_time)

        #get cached values of onetep_store_atom_forces
# Recover SCF k points and eigenvalue from *.band file (ONLY FOR SINGLE POINT CALCULATIONS AT THIS STAGE)


    def onClose_x_onetep_section_raman_tensor(self, backend, gIndex, section):
     #get cached values for stress tensor
        ram_tens =[]
        ram_tens = section['x_onetep_store_raman_tensor']

        for i in range(len(ram_tens)):
            ram_tens[i] = ram_tens[i].split()
            ram_tens[i] = [float(j) for j in ram_tens[i]]
            ram_tens_int = ram_tens[i]
            self.raman_tensor_value.append(ram_tens_int)
        self.raman_tensor_value = self.raman_tensor_value[-3:]
        if self.raman_tensor_value:
            backend.addArrayValues('x_onetep_ramen_tensor',np.asarray(self.raman_tensor_value))



######################################################################################
################ Triggers on closure section_system ######################
######################################################################################

    def onClose_section_system(self, backend, gIndex, section):
        self.secSystemDescriptionIndex = gIndex
        self.number_of_atoms.append(section['x_onetep_number_of_atoms'])


       # = number_of_atoms[i].split()
        # self.at_nr = number_of_atoms[i]

    #     """trigger called when _section_system is closed"""
    #     cellSuperContext = OnetepCellParser.OnetepCellParserContext(False)
    #     cellParser = AncillaryParser(
    #         fileDescription = OnetepCellParser.build_OnetepCellFileSimpleMatcher(),
    #         parser = self.parser,
    #         cachingLevelForMetaName = OnetepCellParser.get_cachingLevelForMetaName(self.metaInfoEnv, CachingLevel.Ignore),
    #         superContext = cellSuperContext)

    #     extFile = ".dat"       # Find the file with extension .cell
    #     dirName = os.path.dirname(os.path.abspath(self.fName))
    #     cFile = str()
    #     for file in os.listdir(dirName):
    #         if file.endswith(extFile):
    #             cFile = file
    #         # else:
    #         #     print("ERROR: please provide .dat file to parse info about cell and positions")
    #     fName = os.path.normpath(os.path.join(dirName, cFile))
    #     for file in os.listdir(dirName):
    #         if file.endswith(extFile):
    #             with open(fName) as fIn:
    #                 cellParser.parseFile(fIn)  # parsing *.cell file to get the k path segments
    #             self.cell = cellSuperContext.cell_store  # recover k path segments coordinartes from *.cell file
    #             self.at_nr = cellSuperContext.at_nr
    #             self.atom_labels = cellSuperContext.atom_labels_store
    #             self.onetep_atom_positions = cellSuperContext.onetep_atom_positions_store
    # # Processing the atom positions in fractionary coordinates (as given in the onetep output)
    #             backend.addArrayValues('x_onetep_atom_positions', np.asarray(self.onetep_atom_positions))


    # # Backend add the total number of atoms in the simulation cell


    # # Processing the atom labels
    #         #get cached values of onetep_store_atom_labels

    #             backend.addArrayValues('atom_labels', np.asarray(self.atom_labels))

    #             backend.addValue('number_of_atoms', self.at_nr)

    #             backend.addArrayValues('simulation_cell', np.asarray(self.cell[-3:]))



# Converting the fractional atomic positions (x) to cartesian coordinates (X) ( X = M^-1 x )
        # for i in range(0, self.at_nr):

        #     pos_a = [   self.a[0] * self.onetep_atom_positions[i][0]
        #               + self.b[0] * math.cos(np.deg2rad(self.gamma[0])) * self.onetep_atom_positions[i][1]
        #               + self.c[0] * math.cos(np.deg2rad(self.beta[0])) * self.onetep_atom_positions[i][2],

        #                 self.b[0] * math.sin(self.gamma[0]) * self.onetep_atom_positions[i][1]
        #               + self.c[0] * self.onetep_atom_positions[i][2] * (( math.cos(np.deg2rad(self.alpha[0]))
        #               - math.cos(np.deg2rad(self.beta[0])) * math.cos(np.deg2rad(self.gamma[0])) ) / math.sin(np.deg2rad(self.gamma[0])) ),

        #                (self.volume / (self.a[0]*self.b[0] * math.sin(np.deg2rad(self.gamma[0])))) * self.onetep_atom_positions[i][2] ]

        #     self.atom_positions.append(pos_a)


        # backend.addValue('x_onetep_cell_volume', self.volume)
        # backend.addArrayValues('atom_positions', np.asarray(self.atom_positions))

#         vel = section['x_onetep_store_atom_ionic_velocities']
#         if vel:
#             for i in range(0, self.at_nr):
#                 vel[i] = vel[i].split()
#                 vel[i] = [float(j) for j in vel[i]]
#                 self.onetep_atom_velocities.append(vel[i])

#             backend.addArrayValues('x_onetep_atom_ionic_velocities', np.asarray(self.onetep_atom_velocities))

# # Backend add the simulation cell
        pos_opt = section['x_onetep_store_optimised_atom_positions']
        if pos_opt:

            # backend.addArrayValues('atom_labels', np.asarray(self.atom_labels[-self.at_nr:]))

            self.at_nr_opt = len(pos_opt)
            bohr_to_m = float(5.29177211e-11)
            for i in range(0, self.at_nr_opt):
                pos_opt[i] = pos_opt[i].split()
                pos_opt[i] = [float(j) for j in pos_opt[i]]
                pos_opt[i] = [ii * bohr_to_m  for ii in pos_opt[i]]
                self.onetep_optimised_atom_positions.append(pos_opt[i])
            backend.addArrayValues('atom_positions', np.asarray(self.onetep_optimised_atom_positions[-self.number_of_atoms[0][0]:]))
#         # #     print pos_opt[i]

# # Converting the fractional atomic positions (x) to cartesian coordinates (X) ( X = M^-1 x )
#             for i in range(0, self.at_nr_opt):

#                 pos_opt_a = [   self.a[0] * self.onetep_optimised_atom_positions[i][0]
#                       + self.b[0] * math.cos(np.deg2rad(self.gamma[0])) * self.onetep_optimised_atom_positions[i][1]
#                       + self.c[0] * math.cos(np.deg2rad(self.beta[0])) * self.onetep_optimised_atom_positions[i][2],

#                         self.b[0] * math.sin(self.gamma[0]) * self.onetep_optimised_atom_positions[i][1]
#                       + self.c[0] * self.onetep_optimised_atom_positions[i][2] * (( math.cos(np.deg2rad(self.alpha[0]))
#                       - math.cos(np.deg2rad(self.beta[0])) * math.cos(np.deg2rad(self.gamma[0])) ) / math.sin(np.deg2rad(self.gamma[0])) ),

#                        (self.volume / (self.a[0]*self.b[0] * math.sin(np.deg2rad(self.gamma[0])))) * self.onetep_optimised_atom_positions[i][2] ]

#                 self.atom_optim_position.append(pos_opt_a)

#             backend.addArrayValues('simulation_cell', np.asarray(self.cell[-3:]))
#             backend.addArrayValues('atom_positions', np.asarray(self.atom_optim_position[-self.at_nr:]))
#             backend.addValue('x_onetep_cell_volume', self.volume)
#         else:
#             pass


    def onClose_x_onetep_section_vibrational_frequencies(self, backend, gIndex, section):
        frequ = section['x_onetep_vibrationl_frequencies_store']
        ##### in this case the name x_onetep_ir_store sands for irreducible representation in the point group.
        irr_rep = section ['x_onetep_ir_store']
        ##### in this case the name x_onetep_ir_intesities_store sands for Infra-red intensities.
        ir_intensities = section['x_onetep_ir_intensity_store']

        self.nr_iter =section['x_onetep_n_iterations_phonons']

        raman_activity = section['x_onetep_raman_activity_store']

        #raman_act = section['onetep_raman_active_store']

        if frequ and ir_intensities and raman_activity:
                for i in range(0,len(frequ)):
                    frequ[i] = frequ[i].split()
                    frequ[i] = [float(j) for j in frequ[i]]
                    frequ_list = frequ[i]
                    self.frequencies.extend(frequ_list)

                    irr_rep[i] = irr_rep[i].split()
                    irr_rep_list = irr_rep[i]
                    self.irr_repres.extend(irr_rep_list)

                    ir_intensities[i] = ir_intensities[i].split()
                    ir_intensities[i] = [float(j) for j in ir_intensities[i]]
                    ir_intens_list = ir_intensities[i]
                    self.ir_intens.extend(ir_intens_list)

                    raman_activity[i] = raman_activity[i].split()
                    raman_activity[i] = [float(j) for j in raman_activity[i]]
                    raman_list = raman_activity[i]
                    self.raman_act.extend(raman_list)


                backend.addArrayValues('x_onetep_ir_intensity', np.asarray(self.ir_intens[-len(self.nr_iter):]))
                backend.addArrayValues('x_onetep_vibrationl_frequencies', np.asarray(self.frequencies[-len(self.nr_iter):]))
                backend.addArrayValues('x_onetep_ir', np.asarray(self.irr_repres[-len(self.nr_iter):]))
                backend.addArrayValues('x_onetep_raman_activity', np.asarray(self.raman_act[-len(self.nr_iter):]))

        elif frequ and ir_intensities:
                for i in range(0,len(frequ)):
                    frequ[i] = frequ[i].split()
                    frequ[i] = [float(j) for j in frequ[i]]
                    frequ_list = frequ[i]
                    self.frequencies.extend(frequ_list)
                    irr_rep[i] = irr_rep[i].split()
                    irr_rep_list = irr_rep[i]
                    self.irr_repres.extend(irr_rep_list)

                    ir_intensities[i] = ir_intensities[i].split()
                    ir_intensities[i] = [float(j) for j in ir_intensities[i]]
                    ir_intens_list = ir_intensities[i]
                    self.ir_intens.extend(ir_intens_list)

                backend.addArrayValues('x_onetep_ir_intensity', np.asarray(self.ir_intens[-len(self.nr_iter):]))
                backend.addArrayValues('x_onetep_vibrationl_frequencies', np.asarray(self.frequencies[-len(self.nr_iter):]))
                backend.addArrayValues('x_onetep_ir', np.asarray(self.irr_repres[-len(self.nr_iter):]))

        elif frequ:
                for i in range(0,len(frequ)):
                    frequ[i] = frequ[i].split()
                    frequ[i] = [float(j) for j in frequ[i]]
                    frequ_list = frequ[i]
                    self.frequencies.extend(frequ_list)
                    irr_rep[i] = irr_rep[i].split()
                    irr_rep_list = irr_rep[i]
                    self.irr_repres.extend(irr_rep_list)

                backend.addArrayValues('x_onetep_vibrationl_frequencies', np.asarray(self.frequencies[-len(self.nr_iter):]))
                backend.addArrayValues('x_onetep_ir', np.asarray(self.irr_repres[-len(self.nr_iter):]))

    def onClose_x_onetep_section_nbo_population_analysis(self, backend, gIndex, section):
        atom_labels_nbo= section['x_onetep_nbo_atom_label_store']
        population_nbo=section['x_onetep_total_nbo_population_store']
        partial_charges=section['x_onetep_nbo_partial_charge_store']
        self.atoms_lables_nbo = []
        if atom_labels_nbo:
            self.atoms_lables_nbo.extend(atom_labels_nbo)
            backend.addArrayValues('x_onetep_nbo_atom_labels',np.asarray(self.atoms_lables_nbo))
        self.nbo_populations = []
        if population_nbo:
            self.nbo_populations.extend(population_nbo)
            backend.addArrayValues('x_onetep_total_nbo_population', np.asarray(self.nbo_populations))
        self.nbo_charges = []
        if partial_charges:
            self.nbo_charges.extend(partial_charges)
            backend.addArrayValues('x_onetep_nbo_partial_charge',np.asarray(self.nbo_charges))

    def onClose_x_onetep_section_mulliken_population_analysis(self, backend, gIndex, section):
        orb_contr = section['x_onetep_total_orbital_store']
        tot_charge = section ['x_onetep_mulliken_charge_store']
        spin = section['x_onetep_spin_store']
        if orb_contr:
            self.total_contribution.extend(orb_contr)

            backend.addArrayValues('x_onetep_total_orbital',np.asarray(self.total_contribution))

        if tot_charge:
            self.total_charge.extend(tot_charge)
            backend.addArrayValues('x_onetep_mulliken_charge', np.asarray(self.total_charge))

        if spin:
            self.total_spin_mulliken.extend(spin)

            backend.addArrayValues('x_onetep_spin',np.asarray(self.total_spin_mulliken))



    def onClose_x_onetep_section_dipole(self, backend, gIndex, section):
        electronic=section['x_onetep_electronic_dipole_moment_store']
        ionic=section['x_onetep_ionic_dipole_moment_store']
        total=section['x_onetep_total_dipole_moment_store']
        if electronic:
            self.electronic_dipole =[]
            self.electronic_dipole.extend(electronic)

            backend.addArrayValues('x_onetep_electronic_dipole_moment',np.asarray(self.electronic_dipole))
        if ionic:
            self.ionic_dipole =[]
            self.ionic_dipole.extend(ionic)

            backend.addArrayValues('x_onetep_ionic_dipole_moment',np.asarray(self.ionic_dipole))
        if total:
            self.total_dipole =[]
            self.total_dipole.extend(total)

            backend.addArrayValues('x_onetep_total_dipole_moment',np.asarray(self.total_dipole))

    def onClose_x_onetep_section_energy_components(self, backend, gIndex, section):
        ######### Caching energy components #######

        self.kinetic = section['x_onetep_electronic_kinetic_energy']


        self.local_pseudo = section['x_onetep_pseudo_local_store']
        self.nonlocal_pseudo = section['x_onetep_pseudo_non_local_store']

        self.Hartree = section['x_onetep_energy_correction_hartree_store']
        self.Exchangecorrelation = section['x_onetep_energy_XC_store']
        self.Ewald = section['x_onetep_ewald_correction_store']
        self.DispersionCorrection =section['x_onetep_dispersion_correction_store']
        self.Integrateddensity = section['x_onetep_integrated_density_store']

    def onClose_x_onetep_section_orbital_information(self, backend, gIndex, section):
        number=section['x_onetep_orbital_number_store']
        energy=section['x_onetep_orbital_energy_store']
        occupancy=section['x_onetep_orbital_occupancy_store']
        if number:
            self.orb_number =[]
            self.orb_number.extend(number)

            backend.addArrayValues('x_onetep_orbital_number',np.asarray(self.orb_number))
        if energy:
            self.orb_energy =[]
            self.orb_energy.extend(energy)

            backend.addArrayValues('x_onetep_orbital_energy',np.asarray(self.orb_energy))
        if occupancy:
            self.orb_occ =[]
            self.orb_occ.extend(occupancy)

            backend.addArrayValues('x_onetep_orbital_occupancy',np.asarray(self.orb_occ))

    def onClose_x_onetep_section_tddft_iterations(self, backend, gIndex, section):
        penalties =section['x_onetep_tddft_penalties_store']
        step =section['x_onetep_tddft_step_store']
        energies =section['x_onetep_tddft_energy_store']

        if energies:
            self.tddft_energy.extend(energies)
        if penalties:
            self.pen.extend(penalties)
        if step:
            self.step.extend(step)

    def onClose_x_onetep_section_tddft_excitations(self, backend, gIndex, section):

        ex_energies =section['x_onetep_tddft_excit_energy_store']
        oscill =section['x_onetep_tddft_excit_oscill_str_store']
        life = section['x_onetep_tddft_excit_lifetime_store']
        if ex_energies:

            self.excitations.extend(ex_energies)
        if oscill:

            self.oscill_str.extend(oscill)
        if life:

            self.life_time.extend(life)

    def onClose_x_onetep_section_edft_parameters(self, backend, gIndex, section):
        if section['x_onetep_edft_smearing_kind'] and section['x_onetep_edft_smearing_width']:
            sm_kind = section['x_onetep_edft_smearing_kind']
            sm_width = section['x_onetep_edft_smearing_width']
            self.gindexsis =  backend.openSection('section_method')
            backend.addValue('smearing_kind', sm_kind[0])
            backend.addValue('smearing_width', sm_width[0])
            backend.closeSection('section_method',self.gindexsis)

    def onClose_x_onetep_section_tddft(self, backend, gIndex, section):

        if self.tddft_energy:
            backend.addArrayValues('x_onetep_tddft_energies',np.asarray(self.tddft_energy))
        if self.pen:
            backend.addArrayValues('x_onetep_tddft_penalties',np.asarray(self.pen))
        if self.step:
            backend.addArrayValues('x_onetep_tddft_steps',np.asarray(self.step))
        if self.excitations:
            backend.addArrayValues('x_onetep_tddft_excit_energies',np.asarray(self.excitations))
        if self.oscill_str:
            backend.addArrayValues('x_onetep_tddft_excit_oscill_str',np.asarray(self.oscill_str))
        if self.life_time:
            backend.addArrayValues('x_onetep_tddft_excit_lifetime',np.asarray(self.life_time))

    def onClose_section_run(self, backend, gIndex, section):
        #backend.addValue('program_basis_set_type', self.basis_set_kind)
        if section['x_onetep_is_smearing'] or section['x_onetep_pbc_cutoff']:
            gindexsis =  backend.openSection('section_system')
            backend.addArrayValues('configuration_periodic_dimensions', np.asarray([False, False, False]))
            backend.closeSection('section_system',gindexsis)
        else:
            gindexsis =  backend.openSection('section_system')
            backend.addArrayValues('configuration_periodic_dimensions', np.asarray([True, True, True]))
            backend.closeSection('section_system',gindexsis)

        f_st_band = section['x_onetep_store_atom_forces_band']

       # if f_st_band:
        #     gindex_band = 1
        #     for i in range(0, self.at_nr):
        #         f_st_band[i] = f_st_band[i].split()
        #         f_st_band[i] = [float(j) for j in f_st_band[i]]

        #         f_st_int_band = f_st_band[i]

        #         self.atom_forces_band.append(f_st_int_band)
        #         self.atom_forces_band = self.atom_forces_band[-self.at_nr:]
        #     backend.addArrayValues('x_onetep_atom_forces', np.asarray(self.atom_forces_band))

        cellSuperContext = OnetepCellParser.OnetepCellParserContext(False)
        cellParser = AncillaryParser(
            fileDescription = OnetepCellParser.build_OnetepCellFileSimpleMatcher(),
            parser = self.parser,
            cachingLevelForMetaName = OnetepCellParser.get_cachingLevelForMetaName(self.metaInfoEnv, CachingLevel.Ignore),
            superContext = cellSuperContext)

        extFile = ".dat"       # Find the file with extension .cell
        dirName = os.path.dirname(os.path.abspath(self.fName))
        cFile = str()
        for file in os.listdir(dirName):
            if file.endswith(extFile):
                cFile = file
            # else:
            #     print("ERROR: please provide .dat file to parse info about cell and positions")
        fName = os.path.normpath(os.path.join(dirName, cFile))
        for file in os.listdir(dirName):
            if file.endswith(extFile):
                with open(fName) as fIn:
                    cellParser.parseFile(fIn)  # parsing *.cell file to get the k path segments
                self.cell = cellSuperContext.cell_store  # recover k path segments coordinartes from *.cell file
                self.at_nr = cellSuperContext.at_nr
                self.atom_labels = cellSuperContext.atom_labels_store
                self.onetep_atom_positions = cellSuperContext.onetep_atom_positions_store

    #             for i in range(0, self.at_nr):

    #             pos_a = [   self.a[0] * self.onetep_atom_positions[i][0]
    #                   + self.b[0] * math.cos(np.deg2rad(self.gamma[0])) * self.onetep_atom_positions[i][1]
    #                   + self.c[0] * math.cos(np.deg2rad(self.beta[0])) * self.onetep_atom_positions[i][2],

    #                     self.b[0] * math.sin(self.gamma[0]) * self.onetep_atom_positions[i][1]
    #                   + self.c[0] * self.onetep_atom_positions[i][2] * (( math.cos(np.deg2rad(self.alpha[0]))
    #                   - math.cos(np.deg2rad(self.beta[0])) * math.cos(np.deg2rad(self.gamma[0])) ) / math.sin(np.deg2rad(self.gamma[0])) ),

    #                    (self.volume / (self.a[0]*self.b[0] * math.sin(np.deg2rad(self.gamma[0])))) * self.onetep_atom_positions[i][2] ]

    #             self.atom_positions.append(pos_a)

    #         # backend.addArrayValues('simulation_cell', np.asarray(self.cell[-3:]))
    #         # backend.addValue('x_castep_cell_volume', self.volume)
    #         # backend.addArrayValues('atom_positions', np.asarray(self.atom_positions))
    # # Processing the atom positions in fractionary coordinates (as given in the onetep output)
                i = backend.openSection('section_system')

                # backend.addArrayValues('x_onetep_atom_positions', np.asarray(self.onetep_atom_positions))

                backend.addArrayValues('atom_positions', np.asarray(self.onetep_atom_positions))

                backend.addArrayValues('atom_labels', np.asarray(self.atom_labels))

                backend.addValue('number_of_atoms', len(self.atom_labels))

                backend.addArrayValues('lattice_vectors', np.asarray(self.cell[-3:]))

                backend.closeSection('section_system', i )


        # time_list = self.time_0

        if section['x_onetep_geom_converged'] is not None:
            if section['x_onetep_geom_converged'][-1] == 'successfully':
                self.geoConvergence = True
            else:
                self.geoConvergence = False
        if self.geoConvergence is not None:
            backend.openSection('section_frame_sequence')
            backend.addValue('geometry_optimization_converged', self.geoConvergence)
            backend.closeSection('section_frame_sequence',gIndex)

        TSSuperContext = OnetepTSParser.OnetepTSParserContext(False)
        TSParser = AncillaryParser(
            fileDescription = OnetepTSParser.build_OnetepTSFileSimpleMatcher(),
            parser = self.parser,
            cachingLevelForMetaName = OnetepTSParser.get_cachingLevelForMetaName(self.metaInfoEnv, CachingLevel.Ignore),
            superContext = TSSuperContext)

        extFile = ".ts"       # Find the file with extension .cell
        dirName = os.path.dirname(os.path.abspath(self.fName))
        cFile = str()
        for file in os.listdir(dirName):
            if file.endswith(extFile):
                cFile = file
            fName = os.path.normpath(os.path.join(dirName, cFile))
            if file.endswith(".ts"):
                with open(fName) as fIn:
                    TSParser.parseFile(fIn)

                    self.ts_total_energy = TSSuperContext.total_energy
                    self.ts_cell_vector = TSSuperContext.frame_cell
                    self.ts_forces = TSSuperContext.total_forces
                    self.ts_position = TSSuperContext.total_positions

                    self.ts_path = TSSuperContext.path_ts
                    if TSSuperContext.total_energy_final:
                        self.ts_total_energy_f = TSSuperContext.total_energy_final

                        self.ts_forces_f = TSSuperContext.md_forces_final
                        self.ts_cell_vector_f = TSSuperContext.cell_final
                        self.ts_positions_f = TSSuperContext.atomf_position
                        self.ts_path_f =TSSuperContext.path_final

                    self.ts_total_energy_p = TSSuperContext.total_energy_pro
                    self.ts_forces_p = TSSuperContext.md_forces_pro
                    self.ts_cell_vector_p = TSSuperContext.cell_pro
                    self.ts_positions_p = TSSuperContext.atomp_position
                    self.ts_path_p =TSSuperContext.path_pro
                    for i in range(len(self.ts_total_energy)):
                        backend.openSection('x_onetep_section_ts')
                        backend.addValue('x_onetep_ts_path', self.ts_path[i])
                        backend.addValue('x_onetep_ts_energy_total', self.ts_total_energy[i])
                        backend.addArrayValues('x_onetep_ts_cell_vectors', np.asarray(self.ts_cell_vector[i]))
                        backend.addArrayValues('x_onetep_ts_forces', np.asarray(self.ts_forces[i]))
                        backend.addArrayValues('x_onetep_ts_positions', np.asarray(self.ts_position[i]))

                        backend.closeSection('x_onetep_section_ts',i)

                    if TSSuperContext.total_energy_final:
                        backend.openSection('x_onetep_section_ts_final')
                        backend.addValue('x_onetep_ts_energy_final', self.ts_total_energy_f)
                        backend.addArrayValues('x_onetep_ts_cell_vectors_final', np.asarray(self.ts_cell_vector_f))
                        backend.addArrayValues('x_onetep_ts_positions_final', np.asarray(self.ts_positions_f))
                        backend.addArrayValues('x_onetep_ts_forces_final', np.asarray(self.ts_forces_f))
                        backend.addValue('x_onetep_ts_path_ts_final', self.ts_path_f)
                        backend.closeSection('x_onetep_section_ts_final',gIndex)


                    backend.openSection('x_onetep_section_ts_product')
                    backend.addValue('x_onetep_ts_energy_product', self.ts_total_energy_p)
                    backend.addArrayValues('x_onetep_ts_cell_vectors_product', np.asarray(self.ts_cell_vector_p))
                    backend.addArrayValues('x_onetep_ts_positions_product', np.asarray(self.ts_positions_p))
                    backend.addArrayValues('x_onetep_ts_forces_product', np.asarray(self.ts_forces_p))
                    backend.addValue('x_onetep_ts_path_product', self.ts_path_p)
                    backend.closeSection('x_onetep_section_ts_product',gIndex)

        if self.ts_total_energy is None:
            backend.addValue('program_basis_set_type', self.basis_set_kind)
        else:
            basis_set_kind_ts = 'psinc functions'
            backend.addValue('program_basis_set_type', basis_set_kind_ts)
        # MDSuperContext = OnetepMDParser.OnetepMDParserContext(False)
        # MDParser = AncillaryParser(
        #     fileDescription = OnetepMDParser.build_OnetepMDFileSimpleMatcher(),
        #     parser = self.parser,
        #     cachingLevelForMetaName = OnetepMDParser.get_cachingLevelForMetaName(self.metaInfoEnv, CachingLevel.Ignore),
        #     superContext = MDSuperContext)

        # extFile = ".md"       # Find the file with extension .cell
        # dirName = os.path.dirname(os.path.abspath(self.fName))
        # cFile = str()
        # for file in os.listdir(dirName):
        #     if file.endswith(extFile):
        #         cFile = file
        # fName = os.path.normpath(os.path.join(dirName, cFile))

        #  # parsing *.cell file to get the k path segments
        # if file.endswith(extFile):
        #     with open(fName) as fIn:
        #         MDParser.parseFile(fIn)

        #     self.frame_temp = MDSuperContext.frame_temperature  # recover k path segments coordinartes from *.cell file
        #     self.frame_press= MDSuperContext.frame_pressure
        #     self.frame_kinetic = MDSuperContext.kinetic
        #     self.frame_potential = MDSuperContext.hamiltonian
        #     self.frame_atom_forces = MDSuperContext.total_forces
        #     self.frame_atom_veloc = MDSuperContext.total_velocities
        #     self.frame_stress_tensor = MDSuperContext.frame_stress_tensor
        #     self.frame_position =MDSuperContext.total_positions
        #     self.frame_cell=MDSuperContext.frame_cell
        #     self.frame_vet_velocities =MDSuperContext.vector_velocities



        #     if self.frame_temp:

        #         gIndexGroupscf = backend.openSection('section_scf_iteration')
        #         for i in range(len(self.frame_atom_forces)):

        #             backend.openSection('section_system')
        #             backend.addArrayValues('atom_velocities', np.asarray(self.frame_atom_veloc[i]))
        #             backend.addArrayValues('atom_labels', np.asarray(self.atom_labels))
        #             backend.addArrayValues('atom_positions', np.asarray(self.frame_position[i]))
        #             backend.addArrayValues('simulation_cell', np.asarray(self.frame_cell[i]))
        #             backend.addArrayValues('x_onetep_velocities_cell_vector',np.asarray(self.frame_vet_velocities[i]))
        #             backend.closeSection('section_system',i+2)

        #             backend.openSection('section_single_configuration_calculation')
        #             backend.addArrayValues('atom_forces', np.asarray(self.frame_atom_forces[i]))
        #             backend.addArrayValues('stress_tensor',np.asarray(self.frame_stress_tensor[i]))
        #             backend.addValue('number_of_scf_iterations', len(self.frame_energies))
        #             if i > 0:

        #                 backend.addValue('energy_free', self.energy_frame_free[i-1])
        #                 backend.addValue('energy_total_T0',self.energy_frame_T0[i-1])

        #             if i > 0:
        #                 for j in range(len(self.frame_energies)):
        #                     s = j + i*len(self.frame_energies) - len(self.frame_energies)

        #                     backend.openSection('section_scf_iteration')
        #                     backend.addValue('energy_total_scf_iteration', self.energy_frame[s])
        #                     backend.addValue('energy_change_scf_iteration', self.energy_frame_gain[s])
        #                     backend.addValue('time_scf_iteration_wall_end',  self.wall_time_end[s])
        #                     backend.closeSection('section_scf_iteration',s+gIndexGroupscf)

        #             backend.closeSection('section_single_configuration_calculation',i+1)

        #         backend.openSection('section_frame_sequence')
        #         backend.addValue('number_of_frames_in_sequence',(len(self.frame_potential)))
        #         backend.addArrayValues('frame_sequence_temperature', np.asarray(self.frame_temp))
        #         backend.addArrayValues('frame_sequence_pressure', np.asarray(self.frame_press))
        #         backend.addArrayValues('frame_sequence_kinetic_energy', np.asarray(self.frame_kinetic))
        #         backend.addArrayValues('frame_sequence_potential_energy', np.asarray(self.frame_potential))
        #         backend.addArrayValues('frame_sequence_time', np.asarray(time_list))
        #         backend.closeSection('section_frame_sequence',gIndex)

        #     else:
        #         pass

        # else:
        #     pass




################################################################################################################################################################
################################################################################################################################################################
################################################################################################################################################################
######################  MAIN PARSER STARTS HERE  ###############################################################################################################
################################################################################################################################################################
############################################################################ onetep.Parser Version 1.0 #########################################################
################################################################################################################################################################


def build_onetepMainFileSimpleMatcher():
    """Builds the SimpleMatcher to parse the main file of onetep.

    First, several subMatchers are defined, which are then used to piece together
    the final SimpleMatcher.

    Returns:
       SimpleMatcher that parses main file of onetep.
    """

    ########################################

    ########################################
    # submatcher for
    scfEigenvaluesSubMatcher = SM(name = 'scfEigenvalues',
       startReStr = r"\stype\sof\scalculation\s*\:\ssingle\spoint\senergy\s*",
       sections = ["x_onetep_section_collect_scf_eigenvalues"]

       ) # CLOSING SM scfEigenvalues


    ########################################
    # submatcher for section method



    ########################################
    # submatcher for section_basis_set_cell_dependent

    basisSetCellAssociatedSubMatcher = SM(name = 'planeWaveBasisSet',
        startReStr = r"cutoff_energy+",
        subFlags = SM.SubFlags.Unordered,
        forwardMatch = True,
        sections = ["section_basis_set_cell_dependent"],
        subMatchers = [

            SM(r"cutoff\_energy\s+(?P<x_onetep_basis_set_planewave_cutoff>[0-9.]+)"),

            SM(r"cutoff\_energy\s*\:\s*(?P<x_onetep_basis_set_planewave_cutoff>[0-9.]+)"),

            SM(r"cutoff\_energy\:\s*(?P<x_onetep_basis_set_planewave_cutoff>[0-9.]+)"),

                      ]) # CLOSING SM planeWaveBasisSet

    calculationMethodSubMatcher = SM(name = 'calculationMethods',
        startReStr = r"xc\_functional+",
        forwardMatch = True,
        sections = ["section_method"],
        subMatchers = [

            SM(name = "onetepXC",
               startReStr = r"xc\_functional+",
               subFlags = SM.SubFlags.Unordered,
               forwardMatch = True,
               sections = ["x_onetep_section_functionals"],
               subMatchers = [
                 SM(r"xc\_functional\s*\:\s(?P<x_onetep_functional_name>[A-Za-z0-9()]+)"),
                 SM(r"xc\_functional\:\s*(?P<x_onetep_functional_name>[A-Za-z0-9()]+)"),
                 SM(r"xc\_functional\s*(?P<x_onetep_functional_name>[A-Za-z0-9()]+)") ,
                 SM(r"xc\_functional\s*\:\s*(?P<x_onetep_functional_name>[A-Za-z0-9()]+)"),

                             ]), # CLOSING onetep_section_functionals
            ])

    #        # SM(name = "onetepXC_definition",
    #        #    startReStr = r"\susing custom XC functional definition\:",
    #        #    #endReStr = r"\srelativistic treatment\s*\:\s*",
    #        #    forwardMatch = True,
    #        #    sections = ["x_onetep_section_functional_definition"],
    #        #    subMatchers = [
    #        #       SM(r"\s*(?P<x_onetep_functional_type>[A-Za-z0-9]+)\s*(?P<x_onetep_functional_weight>[0-9.]+)",
    #        #              repeats = True),
    #        #       #SM(r"\srelativistic treatment\s*\: *(?P<onetep_relativity_treatment_scf> [A-Za-z0-9() -]*)")
    #        #                    ]), # CLOSING onetep_section_functional_definition

    #        # SM(name = "onetep_relativ",
    #        #    startReStr = r"\srelativistic treatment\s*\:\s*",
    #        #    forwardMatch = True,
    #        #    sections = ["x_onetep_section_relativity_treatment"],
    #        #    subMatchers = [
    #        #       SM(r"\srelativistic treatment\s*\: *(?P<x_onetep_relativity_treatment_scf> [A-Za-z0-9() -]+)")
    #        #                   ]), # CLOSING onetep_section_relativistic_treatment

    #        #  SM(name = "van der Waals",
    #        #     startReStr = r"\sDFT\+D: Semi-empirical dispersion correction\s*\:\s*",
    #        #     #forwardMatch = True,
    #        #     #sections = ["onetep_section_relativity_treatment"],
    #        #     subMatchers = [
    #        #       SM(r"\sSEDC with\s*\: *(?P<van_der_Waals_method> [A-Za-z0-9() -]+)"),
    #        #                   ]), # CLOSING van der waals




    #           ]), # CLOSING SM calculationMethods

    # phononCalculationSubMatcher = SM(name = 'phonon_calculation',
    #     sections = ["x_onetep_section_phonons"],
    #     startReStr = r"\s\*\*\** Phonon Parameters \*\*\**\s*",
    #     subMatchers = [
    #         SM(r"\sphonon calculation method\s*\:\s*(?P<x_onetep_phonon_method>[a-zA-Z]+\s[a-zA-Z]+)"),
    #         SM(r"\sphonon convergence tolerance\s*\:\s*(?P<x_onetep_phonon_tolerance>[-+0-9.eEd]+)"),
    #         SM(r"\smax\. number of phonon cycles\s*\:\s*(?P<x_onetep_phonon_cycles>[0-9.]+)"),
    #         SM(r"\sDFPT solver method\s*\:\s*(?P<x_onetep_DFPT_solver_method>[a-zA-Z0-9.() ]+)"),
    #         SM(r"\sband convergence tolerance\s*\:\s*(?P<x_onetep_band_tolerance>[-+0-9.eEd]+)"),
    #                       ])
    edftCalculationSubMatcher = SM(name = 'phonon_calculation',
        sections = ["x_onetep_section_edft_parameters"],
        forwardMatch = True,
        startReStr = r"edft\_",
        subMatchers = [
            SM(r"edft\_commutator\_thres\s*\:\s*(?P<x_onetep_edft_commutator_thres>[-+0-9.eEd]+)"),
            SM(r"edft\_commutator\_thres\s*(?P<x_onetep_edft_commutator_thres>[-+0-9.eEd]+)"),
            SM(r"edft\_energy\_thres\s*\:\s*(?P<x_onetep_edft_energy_thres>[-+0-9.eEd]+)"),
            SM(r"edft\_energy\_thres\s*(?P<x_onetep_edft_energy_thres>[-+0-9.eEd]+)"),
            SM(r"edft\_entropy\_thres\s*\:\s*(?P<x_onetep_edft_entropy_thres>[-+0-9.eEd]+)"),
            SM(r"edft\_entropy\_thres\s*(?P<x_onetep_edft_entropy_thres>[-+0-9.eEd]+)"),
            SM(r"edft\_fermi\_thres\s*\:\s*(?P<x_onetep_edft_fermi_thres>[-+0-9.eEd]+)"),
            SM(r"edft\_fermi\_thres\s*(?P<x_onetep_edft_fermi_thres>[-+0-9.eEd]+)"),
            SM(r"edft\_free\_energy\_thres\s*\:\s*(?P<x_onetep_edft_free_energy_thres>[-+0-9.eEd]+)"),
            SM(r"edft\_free\_energy\_thres\s*(?P<x_onetep_edft_free_energy_thres>[-+0-9.eEd]+)"),
            SM(r"edft\_extra\_bands\s*\:\s*(?P<x_onetep_edft_extra_bands>[0-9.]+)"),
            SM(r"edft\_extra\_bandst\s*(?P<x_onetep_edft_extra_bands>[0-9.]+)"),
            SM(r"edft\_maxit\s*\:\s*(?P<x_onetep_edft_maxit>[0-9.]+)"),
            SM(r"edft\_maxit\s*(?P<x_onetep_edft_maxit>[0-9.]+)"),
            SM(r"edft\_rms\_gradient\_thres\s*(?P<x_onetep_edft_rms_gradient_thres>[-+0-9.eEd]+)"),
            SM(r"edft\_rms\_gradient\_thres\s*\:\s*(?P<x_onetep_edft_rms_gradient_thres>[-+0-9.eEd]+)"),
            SM(r"edft\_smearing\_width\s*(?P<x_onetep_edft_smearing_width>[-+0-9.eEd]+)"),
            SM(r"edft\_smearing\_width\s*\:\s*(?P<x_onetep_edft_smearing_width>[-+0-9.eEd]+)"),
                          ])

    GeomOptimParameterSubMatcher = SM(name = 'optimistation_parameters',
        sections = ["section_sampling_method"],
        # sections = ["x_onetep_section_geom_optimisation_method"],
        forwardMatch = True,
        subFlags = SM.SubFlags.Unordered,
        startReStr = r"geom\_",
        subMatchers = [

            SM(r"geom\_frequency\_est\s*\:\s*(?P<geometry_optimization_frequency_tol>[-+0-9.eEd]+)"),
            SM(r"geom\_frequency\_est\s*(?P<geometry_optimization_frequency_tol>[-+0-9.eEd]+)"),
            SM(r"geom\_method\s*\:\s*(?P<geometry_optimization_method>[a-zA-Z ()]+)"),
            SM(r"geom\_method\s*(?P<geometry_optimization_method>[a-zA-Z ()]+)"),
            SM(r"geom\_energy\_tol\s*\:\s*(?P<geometry_optimization_energy_change>[-+0-9.eEd]+)"),
            SM(r"geom\_energy\_tol\s*(?P<geometry_optimization_energy_change>[-+0-9.eEd]+)"),
            SM(r"geom\_max\_iter\s*\:\s*(?P<x_onetep_max_number_of_steps>[0-9.]+)"),
            SM(r"geom\_max\_iter\s*(?P<x_onetep_max_number_of_steps>[0-9.]+)"),
            SM(r"geom\_force\_tol\s*\:\s*(?P<geometry_optimization_threshold_force>[-+0-9.eEd]+)"),
            SM(r"geom\_force\_tol\s*(?P<geometry_optimization_threshold_force>[-+0-9.eEd]+)"),
            SM(r"geom\_disp\_tol\s*\:\s*(?P<geometry_optimization_geometry_change>[-+0-9.eEd]+)"),
            SM(r"geom\_disp\_tol\s*(?P<geometry_optimization_geometry_change>[-+0-9.eEd]+)"),
            SM(r"geom\_convergence\_win\s*\:\s*(?P<geometry_optimization_geometry_conv_win>[0-9.]+)"),
            SM(r"geom\_convergence\_win\s*(?P<geometry_optimization_geometry_conv_win>[0-9.]+)"),
                                            ]) # CLOSING converged optmisation

    KernelParameterSubMatcher = SM(name = 'kernel',
        sections = ["x_onetep_section_kernel_parameters"],
        # sections = ["x_onetep_section_geom_optimisation_method"],
        forwardMatch = True,
        subFlags = SM.SubFlags.Unordered,
        startReStr = r"kernel\_",
        subMatchers = [

            SM(r"kernel\_cutoff\s*\:\s*(?P<x_onetep_kernel_cutoff>[-+0-9.eEd]+)"),
            SM(r"kernel\_cutoff\s*(?P<x_onetep_kernel_cutoff>[-+0-9.eEd]+)"),
            SM(r"kernel\_diis\_maxit\s*\:\s*(?P<x_onetep_kernel_diis_maxit>[0-9.]+)"),
            SM(r"kernel\_diis\_maxit\s*(?P<x_onetep_kernel_diis_maxit>[0-9.]+)"),
            SM(r"kernel\_diis\_coeff\s*\:\s*(?P<x_onetep_kernel_diis_coeff>[-+0-9.eEd]+)"),
            SM(r"kernel\_diis\_coeff\s*(?P<x_onetep_kernel_diis_coeff>[-+0-9.eEd]+)"),
            SM(r"kernel\_diis\_thershold\s*\:\s*(?P<x_onetep_kernel_diis_thershold>[-+0-9.eEd]+)"),
            SM(r"kernel\_diis\_thershold\s*(?P<x_onetep_kernel_diis_thershold>[-+0-9.eEd]+)"),
            SM(r"kernel\_diis\_size\s*\:\s*(?P<x_onetep_kernel_diis_size>[-+0-9.eEd]+)"),
            SM(r"kernel\_diis\_size\s*(?P<x_onetep_kernel_diis_size>[-+0-9.eEd]+)"),
            SM(r"kernel\_diis\_scheme\s*\:\s*(?P<x_onetep_kernel_diis_type_store>[A-Z\-]+)"),
            SM(r"kernel\_diis\_scheme\s*(?P<x_onetep_kernel_diis_type_store>[A-Z\-]+)"),
            SM(r"kernel\_diis\_lshift\s*\:\s*(?P<x_onetep_kernel_diis_lshift>[-+0-9.eEd]+)"),
            SM(r"kernel\_diis\_lshift\s*(?P<x_onetep_kernel_diis_lshift>[-+0-9.eEd]+)"),
            SM(r"kernel\_diis\_ls\_iter\s*\:\s*(?P<x_onetep_kernel_diis_linear_iter>[0-9.]+)"),
            SM(r"kernel\_diis\_ls\_iter\s*(?P<x_onetep_kernel_diis_linear_iter>[0-9.]+)"),
            ])

    ElectronicMinimisParameterSubMatcher = SM(name = 'Elec_min_parameters' ,
        sections = ["x_onetep_section_scf_parameters"],
        forwardMatch = True,
        subFlags = SM.SubFlags.Unordered,
        startReStr = r"elec\_",
        subMatchers = [
            SM(r"elec\_energy\_tol\s*\:\s*(?P<x_onetep_energy_threshold_store>[-+0-9.eEd]+)"),
            SM(r"elec\_energy\_tol\s*(?P<x_onetep_energy_threshold_store>[-+0-9.eEd]+)"),
            SM(r"elec\_cg\_max\s*\:\s*(?P<x_onetep_elec_cg_max>[-+0-9.eEd]+)"),
            SM(r"elec\_cg\_max\s*(?P<x_onetep_elec_cg_max>[-+0-9.eEd]+)"),
            SM(r"elec\_force\_tol\s*\:\s*(?P<x_onetep_elec_force_tol>[-+0-9.eEd]+)"),
            SM(r"elec\_force\_tol\s*(?P<x_onetep_elec_force_tol>[-+0-9.eEd]+)"),

            ])

    LRTDDFT_parametersSubMatcher = SM(name = 'LRTDDFT' ,
        sections = ["x_onetep_section_tddft_parameters"],
        forwardMatch = True,
        subFlags = SM.SubFlags.Unordered,
        startReStr = r"lr\_tddft\_",
        subMatchers = [
            SM(r"lr\_tddft\_cg_threshold\s*\:\s*(?P<x_onetep_lr_tddft_cg_threshold>[-+0-9.eEd]+)"),
            SM(r"lr\_tddft\_cg_threshold\s*(?P<x_onetep_lr_tddft_cg_threshold>[-+0-9.eEd]+)"),
            SM(r"lr\_tddft\_kernel\_cutoff\s*\:\s*(?P<x_onetep_lr_tddft_kernel_cutoff>[-+0-9.eEd]+)"),
            SM(r"lr\_tddft\_kernel\_cutoff\s*(?P<x_onetep_lr_tddft_kernel_cutoff>[-+0-9.eEd]+)"),
            SM(r"lr\_tddft\_maxit\_cg\s*\:\s*(?P<x_onetep_lr_tddft_maxit_cg>[0-9.]+)"),
            SM(r"lr\_tddft\_maxit\_cg\s*(?P<x_onetep_lr_tddft_maxit_cg>[0-9.]+)"),
            SM(r"lr\_tddft\_maxit\_pen\s*\:\s*(?P<x_onetep_lr_tddft_maxit_pen>[0-9.]+)"),
            SM(r"lr\_tddft\_maxit\_pen\s*(?P<x_onetep_lr_tddft_maxit_pen>[0-9.]+)"),
            SM(r"lr\_tddft\_num\_states\s*\:\s*(?P<x_onetep_lr_tddft_num_states>[0-9.]+)"),
            SM(r"lr\_tddft\_num\_states\s*(?P<x_onetep_lr_tddft_num_states>[0-9.]+)"),
            SM(r"lr\_tddft\_penalty\_tol\s*\:\s*(?P<x_onetep_lr_tddft_penalty_tol>[-+0-9.eEd]+)"),
            SM(r"lr\_tddft\_penalty\_tol\s*(?P<x_onetep_lr_tddft_penalty_tol>[-+0-9.eEd]+)"),
            ])

    NGWFSubMatcher = SM(name = 'ngwf' ,
        sections = ["x_onetep_section_ngwf_parameters"],
        forwardMatch = True,
        subFlags = SM.SubFlags.Unordered,
        startReStr = r"ngwf\_",
        subMatchers = [
            SM(r"ngwf\_cg\_max\_step\s*\:\s*(?P<x_onetep_ngwf_cg_max_step>[0-9]+)"),
            SM(r"ngwf\_cg\_max\_step\s*(?P<x_onetep_ngwf_cg_max_step>[0-9]+)"),
            SM(r"ngwf\_cg\_type\s*\:\s*(?P<x_onetep_ngwf_cg_type>[A_Z\_]+)"),
            SM(r"ngwf\_cg\_type\s*(?P<x_onetep_ngwf_cg_type>[A_Z\_]+)"),
            SM(r"ngwf\_halo\s*\:\s*(?P<x_onetep_ngwf_halo>[-+0-9.eEd]+)"),
            SM(r"ngwf\_halo\s*(?P<x_onetep_ngwf_halo>[-+0-9.eEd]+)"),
            SM(r"ngwf\_max\_grad\s*\:\s*(?P<x_onetep_ngwf_max_grad>[-+0-9.eEd]+)"),
            SM(r"ngwf\_max\_grad\s*(?P<x_onetep_ngwf_max_grad>[-+0-9.eEd]+)"),
            SM(r"ngwf\_threshold\_orig\s*\:\s*(?P<x_onetep_ngwf_threshold_orig>[-+0-9.eEd]+)"),
            SM(r"ngwf\_threshold\_orig\s*(?P<x_onetep_ngwf_threshold_orig>[-+0-9.eEd]+)"),
            ])

    ElectronicParameterSubMatcher = SM(name = 'Elec_parameters' ,
        sections = ["section_system"],
        startReStr = r"\-*\sAtom counting information\s\-*\s*",
        subMatchers = [

            SM(r"Totals\:\s*(?P<x_onetep_number_of_atoms>[0-9]+)\s*(?P<x_onetep_number_of_ngwf>[0-9]+)\s*(?P<x_onetep_number_of_projectors>[0-9]+)",repeats=True),
            ])




    PopulationAnalysisParameterSubMatcher = SM(name = 'Pop_analysis' ,
        sections = ["x_onetep_section_population_analysis_parameters"],
        startReStr = r"popn\_",
        forwardMatch = True,
        subFlags = SM.SubFlags.Unordered,
        subMatchers = [
            SM(r"popn\_bond\_cutoff\s*\:\s*(?P<x_onetep_population_analysis_cutoff>[-+0-9.eEd]+)"),
            SM(r"popn\_bond\_cutoff\s*(?P<x_onetep_population_analysis_cutoff>[-+0-9.eEd]+)"),
            ])

    VanderWaalsParameterSubMatcher = SM(name = 'dispersion' ,
        sections = ["x_onetep_section_van_der_Waals_parameters"],
        forwardMatch = True,
        subFlags = SM.SubFlags.Unordered,
        startReStr = r"dispersion",
        subMatchers = [
            SM(r"dispersion\s*\:\s*(?P<x_onetep_disp_method_name_store>[0-9.]+)"),
            SM(r"dispersion\s*(?P<x_onetep_disp_method_name_store>[0-9.]+)"),
            SM(r"dispersion\:\s*(?P<x_onetep_disp_method_name_store>[0-9.]+)"),
            ])

    TSParameterSubMatcher = SM(name = 'TS_parameters' ,
        sections = ["x_onetep_section_ts_parameters"],
        subFlags = SM.SubFlags.Unordered,
        forwardMatch = True,
        startReStr = r"tssearch\_",
        subMatchers = [
            SM(r"tssearch\_cg\_max\_iter\s*(?P<x_onetep_ts_number_cg>[0-9]+)"),
            SM(r"tssearch\_method\s*\:\s*(?P<x_onetep_ts_method>[A-Za-z]+)"),
            SM(r"tssearch\_method\s*(?P<x_onetep_ts_method>[A-Za-z]+)"),
            SM(r"tssearch\_lstqst\_protocol\s*(?P<x_onetep_ts_protocol>[A-Za-z]+)"),
            SM(r"tssearch\_lstqst\_protocol\s*\:\s*(?P<x_onetep_ts_protocol>[A-Za-z]+)"),
            SM(r"tssearch\_qst\_max\_iter\s*\:\s*(?P<x_onetep_ts_qst_iter>[0-9.]+)"),
            SM(r"tssearch\_qst\_max\_iter\s*(?P<x_onetep_ts_qst_iter>[0-9.]+)"),
            SM(r"tssearch\_cg\_max\_iter\s*\:\s*(?P<x_onetep_ts_number_cg>[0-9.]+)"),
            SM(r"tssearch\_force\_tol\s*\:\s*(?P<x_onetep_ts_force_tolerance>[-+0-9.eEd]+)"),
            SM(r"tssearch\_force\_tol\s*(?P<x_onetep_ts_force_tolerance>[-+0-9.eEd]+)"),
            SM(r"tssearch\_disp\_tol\s*\:\s*(?P<x_onetep_ts_displacement_tolerance>[-+0-9.eEd]+)"),
            SM(r"tssearch\_disp\_tol\s*(?P<x_onetep_ts_displacement_tolerance>[-+0-9.eEd]+)"),
            ])

    MDParameterSubMatcher = SM(name = 'MD_parameters' ,
        sections = ["section_sampling_method"],
        forwardMatch = True,
        subFlags = SM.SubFlags.Unordered,
        startReStr = r"md\_",
        subMatchers = [
            SM(r"md\_delta\_t\s*\:\s*(?P<x_onetep_integrator_dt>[-+0-9.eEdD]+)"),
            SM(r"md\_delta\_t\s*(?P<x_onetep_integrator_dt>[-+0-9.eEdD]+)"),
            SM(r"md\_num\_iter\s*\:\s*(?P<x_onetep_number_of_steps_requested>[0-9]+)"),
            SM(r"md\_num\_iter\s*(?P<x_onetep_number_of_steps_requested>[0-9]+)"),

            ])

    # OpticsParameterSubMatcher = SM(name = 'optics_parameters' ,
    #     sections = ["x_onetep_section_optics_parameters"],
    #     startReStr = r"\s\*\*\** Optics Parameters \*\*\**\s*",
    #     subMatchers = [
    #         SM(r"\s*search method\s*\:\s*(?P<x_onetep_optics_n_bands>[0-9.]+)"),
    #         SM(r"\s*band convergence tolerance\s*\:\s*(?P<x_onetep_optics_tolerance>[-+0-9.eEd]+)"),


    #         ])

    # ElecSpecParameterSubMatcher = SM(name = 'electronic_spectroscopy_parameters' ,
    #     sections = ["x_onetep_section_electronic_spectroscpy_parameters"],
    #     startReStr = r"\s\*\*\** Electronic Spectroscopy Parameters \*\*\**\s*",
    #     subMatchers = [
    #         SM(r"\s*electronic spectroscopy with theory level\s*\:\s*(?P<x_onetep_theory_level>[A-Z]+)"),
    #         SM(r"\s*spectroscopy calculation\s*\:\s*(?P<x_onetep_spectroscopy_calculation>[A-Za-z0-9 + A-Za-z0-9 ]+)"),
    #         SM(r"\s*max\. number of iterations \s*\:\s*(?P<x_onetep_spec_max_iter>[0-9.]+)"),
    #         SM(r"\s*max\. steps per iteration\s*\:\s*(?P<x_onetep_spec_max_steps>[0-9.]+)"),
    #         SM(r"\s*number of bands \/ k-point\s*\:\s*(?P<x_onetep_spec_max_bands>[0-9.]+)"),
    #         SM(r"\s*band convergence tolerance\s*\:\s*(?P<x_onetep_spec_tolerance>[-+0-9.eEd]+)"),
    #         ])


    KernelOptimSubMatcher_edft = SM(name= 'kernel',
                                    startReStr = r"\>\>\> Density kernel optimised for the current NGWF basis\:",
                                    sections = ['x_onetep_section_kernel_optimisation'],

                                    repeats = True,

                subMatchers = [
                    SM(r"\s*Total free energy\s*\=\s*(?P<x_onetep_total_free_energy__hartree>[-+0-9.eEdD]*)\s*"),
                    SM(r"\s*Total energy\s*\=\s*(?P<x_onetep_total_energy__hartree>[-+0-9.eEdD]*)\s*"), # matching final converged total energy
                    SM(r"\s*Estimated bandgap\s*\=\s*(?P<x_onetep_band_gap__hartree>[-+0-9.eEdD]*)\s*"),
                    SM(r"\s*RMS occupancy error\s*\=\s*(?P<x_onetep_rms_occupancy_error__hartree>[-+0-9.eEdD]*)\s*"),
                    SM(r"\s*\[H\,K\] commutator\s*\=\s*(?P<x_onetep_commutator__hartree>[-+0-9.eEdD]*)\s*"),
                    ])

    KernelOptimSubMatcher = SM(name= 'kernel',
                                    startReStr = r"\>\>\> Density kernel optimised for the current NGWF basis\:",
                                    sections = ['x_onetep_section_kernel_optimisation'],
                                    endReStr = r"           \|         \*\*\* NGWF optimisation converged \*\*\*          \|",
                                    repeats = True,

                subMatchers = [
                    SM(r"\s*Total free energy\s*\=\s*(?P<x_onetep_total_free_energy__hartree>[-+0-9.eEdD]*)\s*"),
                    SM(r"\s*Total energy\s*\=\s*(?P<x_onetep_total_energy__hartree>[-+0-9.eEdD]*)\s*"), # matching final converged total energy
                    SM(r"\s*Estimated bandgap\s*\=\s*(?P<x_onetep_band_gap__hartree>[-+0-9.eEdD]*)\s*"),
                    SM(r"\s*RMS occupancy error\s*\=\s*(?P<x_onetep_rms_occupancy_error__hartree>[-+0-9.eEdD]*)\s*"),
                    SM(r"\s*\[H\,K\] commutator\s*\=\s*(?P<x_onetep_commutator__hartree>[-+0-9.eEdD]*)\s*"),
                    ])


    energycomponentsSubMatcher = SM(name= 'energy_components',
                                    startReStr = r"\s*\-\-\-\-\-\-\-\-\-\-* ENERGY COMPONENTS \(Eh\) \-\-\-\-\-\-\-\-\-\-\-*",
                                    weak = True,
                                    forwardMatch = True,
                                    sections = ['x_onetep_section_energy_components'],
                                    # endReStr = r"\s*Integrated density\s*\:\s*[+0-9.eEdD]+",


                subMatchers = [

                    SM(r"\s*\| Kinetic\s*\:\s*(?P<x_onetep_electronic_kinetic_energy>[-+0-9.eEdD]*)\s\|\s*"), # matching final converged total energy
                    SM(r"\s*\| Pseudopotential \(local\)\s*\:\s*(?P<x_onetep_pseudo_local_store>[-+0-9.eEdD]*)\s\|\s*"),
                    SM(r"\s*\| Pseudopotential \(non\-local\)\s*\:\s*(?P<x_onetep_pseudo_non_local_store>[-+0-9.eEdD]*)\s\|\s*"),
                    SM(r"\s*\| Hartree\s*\:\s*(?P<x_onetep_energy_correction_hartree_store>[-+0-9.eEdD]*)\s\|\s*"),
                    SM(r"\s*\| Exchange\-correlation\s*\:\s*(?P<x_onetep_energy_XC_store>[-+0-9.eEdD]*)\s\|\s*"),
                    SM(r"\s*\| Ewald\s*\:\s*(?P<x_onetep_ewald_correction_store>[-+0-9.eEdD]*)\s\|\s*"),
                    SM(r"\s*\| Dispersion Correction\s*\:\s*(?P<x_onetep_dispersion_correction_store>[-+0-9.eEdD]*)\s\|\s*"),
                    SM(r"\s*Integrated density\s*\:\s*(?P<x_onetep_integrated_density_store>[-+0-9.eEdD]*)\s*"),

                    ])

    edft_SubMatcher = SM (name = 'EDFT submatcher',
            sections = ['x_onetep_section_edft'],
            startReStr = r"\-\-\-\-* Ensemble\-DFT optimisation \-\-\-\-*",
            repeats = True,
            # endReStr = r"\-*\s*",
            subMatchers = [
                SM (name = 'EDFT submatcher',
                sections = ['x_onetep_section_edft_iterations'],
                startReStr = r"\#\s*(?P<x_onetep_edft_iteration>[0-9]+)\s*(?P<x_onetep_edft_rms_gradient>[-\d\.]+)\s*(?P<x_onetep_edft_commutator>[\d\.]+)\s*(?P<x_onetep_edft_free_energy>[\d\.]+)",
                repeats = True,
                # endReStr = r"\-*\s*",
                    subMatchers = [
                        SM(r"\#\s*(?P<x_onetep_edft_iteration>[0-9]+)\s*(?P<x_onetep_edft_rms_gradient>[-\d\.]+)\s*(?P<x_onetep_edft_commutator>[\d\.]+)\s*(?P<x_onetep_edft_free_energy>[\d\.]+)"),
                        SM(r"Step\s*\=\s*(?P<x_onetep_edft_step>[\d\.]+)\s*"),
                        SM(r"Energy\s*\=\s*(?P<x_onetep_edft_energy>[\d\.]+)\s*"),
                        SM(r"Est\. 0K Energy 0\.5\*\(E\+A\)\s*\=\s*(?P<x_onetep_edft_0K>[\d\.]+)\s*"),
                        SM(r"Residual Non\-orthogonality \=\s*(?P<x_onetep_residual_nonorthog>[\d\.]+)\s*"),
                        SM(r"Residual N\_electrons\s*\=\s*(?P<x_onetep_residual_n_elec>[\d\.]+)\s*"),
                        SM (name = 'EDFT submatcher',
                            sections = ['x_onetep_section_edft_spin'],
                            startReStr = r"\s*(?P<x_onetep_edft_spin_type>[0-9]+)\s*(?P<x_onetep_edft_n_electrons>[\d\.]+)\s*(?P<x_onetep_edft_fermi_level>[-\d\.]+)\s*(?P<x_onetep_edft_fermi_level_delta>[-\d\.]+)",
                            repeats = True,
                            # endReStr = r"\s*\-\-\-\-\-\-\s*",
                            subMatchers = [
                                     SM (name = 'EDFT submatcher',
                                        sections = ['x_onetep_section_edft_spin_iterations'],
                                        startReStr = r"\s*(?P<x_onetep_edft_orbital_iteration_spin>[0-9]+)\s\|\s*(?P<x_onetep_edft_eigenvalue>[-\d\.]+)\s*(?P<x_onetep_edft_occupancy>[-\d\.]+)\s\|",
                                        repeats = True,

                                            )]),
                        KernelOptimSubMatcher_edft,

                     ]) ])

    KernelOptimSubMatcher_frame = SM(name= 'energy_components',
                                    startReStr = r"\>\>\> Density kernel optimised for the current NGWF basis\:",
                                    sections = ['x_onetep_section_kernel_optimisation'],

                                    repeats = True,

                subMatchers = [
                    SM(r"\s*Total free energy\s*\=\s*(?P<x_onetep_total_free_energy__hartree>[-+0-9.eEdD]*)\s*"),
                    SM(r"\s*Total energy\s*\=\s*(?P<x_onetep_total_energy__hartree>[-+0-9.eEdD]*)\s*"), # matching final converged total energy
                    SM(r"\s*Estimated bandgap\s*\=\s*(?P<x_onetep_band_gap__hartree>[-+0-9.eEdD]*)\s*"),
                    SM(r"\s*RMS occupancy error\s*\=\s*(?P<x_onetep_rms_occupancy_error__hartree>[-+0-9.eEdD]*)\s*"),
                    SM(r"\s*\[H\,K\] commutator\s*\=\s*(?P<x_onetep_commutator__hartree>[-+0-9.eEdD]*)\s*"), ])


    energycomponentsSubMatcher_frame = SM(name= 'energy_components',
                                    startReStr = r"\s*\-\-\-\-\-\-\-\-\-\-* ENERGY COMPONENTS \(Eh\) \-\-\-\-\-\-\-\-\-\-\-*",
                                    # endReStr = r"\sBFGS\:\sfinished iteration\s*\0\s*",
                                    sections = ['x_onetep_section_energy_components'],
                                    forwardMatch = True,

                subMatchers = [

                    SM(r"\s*\| Kinetic\s*\:\s*(?P<x_onetep_electronic_kinetic_energy__hartree>[-+0-9.eEdD]*)\s\|\s*"), # matching final converged total energy
                    SM(r"\s*\| Pseudopotential \(local\)\s*\:\s*(?P<x_onetep_pseudo_local_store>[-+0-9.eEdD]*)\s\|\s*"),
                    SM(r"\s*\| Pseudopotential \(non\-local\)\s*\:\s*(?P<x_onetep_pseudo_non_local_store>[-+0-9.eEdD]*)\s\|\s*"),
                    SM(r"\s*\| Hartree\s*\:\s*(?P<x_onetep_energy_correction_hartree_store>[-+0-9.eEdD]*)\s\|\s*"),
                    SM(r"\s*\| Exchange\-correlation\s*\:\s*(?P<x_onetep_energy_XC_store>[-+0-9.eEdD]*)\s\|\s*"),
                    SM(r"\s*\| Ewald\s*\:\s*(?P<x_onetep_ewald_correction_store>[-+0-9.eEdD]*)\s\|\s*"),
                    SM(r"\s*\| Dispersion Correction\s*\:\s*(?P<x_onetep_dispersion_correction_store>[-+0-9.eEdD]*)\s\|\s*"),
                    SM(r"\s*Integrated density\s*\:\s*(?P<x_onetep_integrated_density_store>[-+0-9.eEdD]*)\s*"),

                    ])
    KernelOptimSubMatcher_ts = SM(name= 'kernel optimisation',
                                startReStr = r"\>\>\> Density kernel optimised for the current NGWF basis\:",
                                sections = ['x_onetep_section_kernel_optimisation'],
                                repeats = True,

                subMatchers = [
                    SM(r"\s*Total free energy\s*\=\s*(?P<x_onetep_total_free_energy__hartree>[-+0-9.eEdD]*)\s*"),
                    SM(r"\s*Total energy\s*\=\s*(?P<x_onetep_total_energy__hartree>[-+0-9.eEdD]*)\s*"), # matching final converged total energy
                    SM(r"\s*Estimated bandgap\s*\=\s*(?P<x_onetep_band_gap__hartree>[-+0-9.eEdD]*)\s*"),
                    SM(r"\s*RMS occupancy error\s*\=\s*(?P<x_onetep_rms_occupancy_error__hartree>[-+0-9.eEdD]*)\s*"),
                    SM(r"\s*\[H\,K\] commutator\s*\=\s*(?P<x_onetep_commutator__hartree>[-+0-9.eEdD]*)\s*"),
                    ])


    energycomponentsSubMatcher_ts = SM(name= 'energy_components',
                                    startReStr = r"\s*\-\-\-\-\-\-\-\-\-\-* ENERGY COMPONENTS \(Eh\) \-\-\-\-\-\-\-\-\-\-\-*",
                                    forwardMatch = True,
                                    # endReStr = r"\sBFGS\:\sfinished iteration\s*\0\s*",
                                    sections = ['x_onetep_section_energy_components'],


                subMatchers = [

                    SM(r"\s*\| Kinetic\s*\:\s*(?P<x_onetep_electronic_kinetic_energy__hartree>[-+0-9.eEdD]*)\s\|\s*"), # matching final converged total energy
                    SM(r"\s*\| Pseudopotential \(local\)\s*\:\s*(?P<x_onetep_pseudo_local_store>[-+0-9.eEdD]*)\s\|\s*"),
                    SM(r"\s*\| Pseudopotential \(non\-local\)\s*\:\s*(?P<x_onetep_pseudo_non_local_store>[-+0-9.eEdD]*)\s\|\s*"),
                    SM(r"\s*\| Hartree\s*\:\s*(?P<x_onetep_energy_correction_hartree_store>[-+0-9.eEdD]*)\s\|\s*"),
                    SM(r"\s*\| Exchange\-correlation\s*\:\s*(?P<x_onetep_energy_XC_store>[-+0-9.eEdD]*)\s\|\s*"),
                    SM(r"\s*\| Ewald\s*\:\s*(?P<x_onetep_ewald_correction_store>[-+0-9.eEdD]*)\s\|\s*"),
                    SM(r"\s*\| Dispersion Correction\s*\:\s*(?P<x_onetep_dispersion_correction_store>[-+0-9.eEdD]*)\s\|\s*"),
                    SM(r"\s*Integrated density\s*\:\s*(?P<x_onetep_integrated_density_store>[-+0-9.eEdD]*)\s*"),

                    ])

    geomOptim_finalSubMatcher = SM (name = 'geometry_optimisation_final_configuration',
            startReStr = r"\sBFGS\s\:\sFinal Configuration\:\s*",
            # sections = ['section_single_configuration_calculation','section_system'],
            forwardMatch = True,
            subMatchers = [

                            SM(r"\s*x\s*(?P<x_onetep_store_optimised_atom_labels>[A-Za-z]+\s*[0-9]+)\s*(?P<x_onetep_store_optimised_atom_positions>[-\d\.]+\s*[-\d\.]+\s*[-\d\.]+)",
                                    endReStr = "\n",
                                    repeats = True),
                            SM(r"\sBFGS\s\:\sFinal Enthalpy\s*\=\s(?P<x_onetep_enthalpy__hartree>[-+0-9.eEdD]+)"),
                            ])

    geomOptimSubMatcher =  SM (name = 'geometry_optimisation',
            startReStr = r"\sStarting BFGS iteration\s*(?P<x_onetep_geom_iteration_index>[0-9.]+)\s\.\.\.\s*",
            # sections = ['section_single_configuration_calculation','section_system'],
            endReStr = r"\sBFGS\s\:\sFinal Configuration\:\s",
            # required = True,
            repeats = True,
            subMatchers = [


                        SM(r"\s*x\s*(?P<x_onetep_store_optimised_atom_labels>[A-Za-z]+\s*[0-9]+)\s*(?P<x_onetep_store_optimised_atom_positions>[-\d\.]+\s*[-\d\.]+\s*[-\d\.]+)",
                            endReStr = "\n",
                            repeats = True),

                        KernelOptimSubMatcher_frame,

                        energycomponentsSubMatcher_frame,
                        SM(sections = ['section_scf_iteration'],
                            startReStr = r"\s*(?P<x_onetep_number_of_scf_iterations_store>[0-9]+)\s*(?P<x_onetep_scf_rms_gradient>[+0-9.eEdD]+)\s*(?P<energy_total_scf_iteration__hartree>[-+0-9.eEdD]*)\s*(?P<energy_change_scf_iteration__hartree>[-+0-9.eEdD]*)\s*[-+0-9.eEdD]*\s*",repeats = True,
                            endReStr = r"\s*[0-9]+\s*[+0-9.eEdD]+\s*[-+0-9.eEdD]*\s*\<\-\-\sCG\s*"),

                        SM(r"\<QC\>\s*\[NGWF iterations]\:\s*(?P<x_onetep_n_ngwf_iterations>[0-9]*)\s*"),
                        SM(r"\<QC\>\s*\[total\_energy\]\:\s*(?P<x_onetep_geom_optim_energy_total__hartree>[-+0-9.eEdD]*)\s*"), # matching final converged total energy
                        SM(r"\<QC\>\s*\[rms\_gradient\]\:\s*(?P<x_onetep_final_rms_gradient>[-+0-9.eEdD]*)\s*"),

                        # geomOptimSubMatcher_improving_cycle,


                        SM(startReStr = r"\*\*\*\*\** Forces \*\*\*\*\**\s*",
                            subMatchers = [
                                    SM(r"\*\s*[A-Za-z]+\s*[0-9]+\s*(?P<x_onetep_store_atom_forces>[-\d\.]+\s+[-\d\.]+\s+[-\d\.]+)\s\*",
                                        repeats = True)
                         ]),


                        # SM(r"\sBFGS\s\:\sGeometry optimization (?P<x_onetep_geom_converged>[a-z]+) to converge after\s*"),
                        # SM(r"\s[A-Za-z]+\:\sGeometry\soptimization\scompleted\s(?P<x_onetep_geom_converged>[a-z]+)\.\s*"),

                        # geomOptim_finalSubMatcher,
                        ])

    TSSubMatcher = SM(name = 'TS submatcher',
                    startReStr = r"\<\<\<\<\<* Starting ONETEP Transition State Search \>\>\>\>\>*",
                    subMatchers = [

                        SM(startReStr = r"Calculating Ewald energy\s\.\.\.\s*(?P<x_onetep_ewald_correction__hartree>[-+0-9.eEdD]+)\sHartree",
                            repeats = True,
                            endReStr = r"Determining parallel strategy\s.\.\.\.\.\.\sdone",
                            sections = ["section_single_configuration_calculation","section_system"],
                            subMatchers = [

                                    KernelOptimSubMatcher_ts,
                                    energycomponentsSubMatcher_ts,
                                    SM(sections = ['section_scf_iteration'],
                                        startReStr = r"\s*(?P<x_onetep_number_of_scf_iterations_store>[0-9]+)\s*(?P<x_onetep_scf_rms_gradient__hartree>[+0-9.eEdD]+)\s*(?P<energy_total_scf_iteration__hartree>[-+0-9.eEdD]*)\s*\<\-\-\sCG\s*"),
                                        # endReStr = r"\s*[0-9]+\s*(?P<x_onetep_scf_rms_gradient>[+0-9.eEdD]+)\s*(?P<energy_total_scf_iteration>[-+0-9.eEdD]*)\s*\<\-\-\sCG\s*",
                                        # endReStr = r"\s*[0-9]+\s*[+0-9.eEdD]+\s*[-+0-9.eEdD]*\s*\<\-\-\sCG\s*",
                                        # subMatchers = [
                                        #     SM(r"\s*[0-9]+\s*(?P<x_onetep_scf_rms_gradient>[+0-9.eEdD]+)\s*(?P<energy_total_scf_iteration>[-+0-9.eEdD]*)\s*\<\-\-\sCG\s*",
                                        #     repeats = True)]),

                                    SM(sections = ['section_scf_iteration'],
                                        startReStr = r"\s*(?P<x_onetep_number_of_scf_iterations_store>[0-9]+)\s*(?P<x_onetep_scf_rms_gradient__hartree>[+0-9.eEdD]+)\s*(?P<energy_total_scf_iteration__hartree>[-+0-9.eEdD]*)\s*(?P<energy_change_scf_iteration__hartree>[-+0-9.eEdD]*)\s*[-+0-9.eEdD]*\s*",repeats = True,
                                        # endReStr = r"\s*[0-9]+\s*(?P<x_onetep_scf_rms_gradient>[+0-9.eEdD]+)\s*(?P<energy_total_scf_iteration>[-+0-9.eEdD]*)\s*\<\-\-\sCG\s*",
                                        endReStr = r"\s*[0-9]+\s*[+0-9.eEdD]+\s*[-+0-9.eEdD]*\s*\<\-\-\sCG\s*",
                                        # subMatchers = [
                                        #     SM(r"\s*[0-9]+\s*(?P<x_onetep_scf_rms_gradient>[+0-9.eEdD]+)\s*(?P<energy_total_scf_iteration>[-+0-9.eEdD]*)\s*\<\-\-\sCG\s*",
                                        #     repeats = True)]),
                                          ),

                                    SM(r"\sPath coordinate\:\s*(?P<x_onetep_ts_coordinate_path>[-+0-9.eEdD]*)\s*"),
                                    SM(r"\sEnergy\:\s*(?P<x_onetep_energy_lst_max__hartree>[-+0-9.eEdD]*)"),
                                    SM(r"\sEnergy of reactant\:\s*(?P<x_onetep_energy_reac__hartree>[-+0-9.eEdD]*)\s*"),
                                    SM(r"\sEnergy of product\:\s*(?P<x_onetep_energy_prod__hartree>[-+0-9.eEdD]*)\s*"),
                                    SM(r"\sEnergy of LST maximum\:\s*(?P<x_onetep_energy_lst_max__hartree>[-+0-9.eEdD]*)\s*"),
                                    SM(r"\sLocation of LST maximum\:\s*(?P<x_onetep_location_lst_max__hartree>[-+0-9.eEdD]*)\s*"),
                                    SM(r"\sBarrier from reactant\:\s*(?P<x_onetep_barrier_reac__hartree>[-+0-9.eEdD]*)\s*"),
                                    SM(r"\sBarrier from product\:\s*(?P<x_onetep_barrier_prod__hartree>[-+0-9.eEdD]*)\s*"),
                                    SM(r"\sEnergy of reaction\:\s*(?P<x_onetep_reaction_energy__hartree>[-+0-9.eEdD]*)\s*"),


                                    SM(startReStr = r"\s*Forces\: Cartesian components\: Ha\/Bohr\s*",
                                         subMatchers = [

                                                    SM(r"\s*\+\s*[A-Za-z]+\s*[0-9]+\s*(?P<x_onetep_store_atom_forces>[-\d\.]+\s+[-\d\.]+\s+[-\d\.]+)\s*\+",
                                                        repeats = True)
                                                ]),
                            ]),
        ])
    pdos = SM (name = 'pdos',
            startReStr = r"\s\=\>\sComputing Gaussian smeared pDOS\s\<\=\s*",
            sections = ["section_dos"],
            repeats = True,
            # endReStr = r"\=*\s*",
            # endReStr =r"\s*\.\.\.\.\.\.\.\s*\-\-\- gap \-\-\s*\.\.\.\.\.\.\.\.\.\s*",

            subMatchers = [
                SM(r"\<QC\>\s*\[pdoswts\(.*\)\]\:\s*(?P<dos_energies>[-\d\.]+)\s*",repeats=True),
                 ])

    singlepointSubMatcher = SM(name = 'single_point',
                # startReStr = r"\s*\<\<\<\<\< CALCULATION SUMMARY \>\>\>\>\>\s*",
                startReStr = r"\>\>\> Density kernel optimised for the current NGWF basis\:",
                # required = True,
                # weak = True,
                # startReStr = r"\s*\<* CALCULATION SUMMARY \>*\s*",
                forwardMatch = True,
                endReStr = r"\sStarting BFGS iteration\s1\s\.\.\.",
                sections = ["section_single_configuration_calculation","section_system"],
                subMatchers = [

                    KernelOptimSubMatcher,
                    energycomponentsSubMatcher,

                    SM(sections = ['section_scf_iteration'],
                        startReStr = r"\s*[0-9]+\s*(?P<x_onetep_scf_rms_gradient__hartree>[+0-9.eEdD]+)\s*(?P<energy_total_scf_iteration__hartree>[-+0-9.eEdD]*)\s*\<\-\-\sCG\s*"),
                        # endReStr = r"\s*[0-9]+\s*(?P<x_onetep_scf_rms_gradient>[+0-9.eEdD]+)\s*(?P<energy_total_scf_iteration>[-+0-9.eEdD]*)\s*\<\-\-\sCG\s*",
                        # endReStr = r"\s*[0-9]+\s*[+0-9.eEdD]+\s*[-+0-9.eEdD]*\s*\<\-\-\sCG\s*",
                        # subMatchers = [
                        #     SM(r"\s*[0-9]+\s*(?P<x_onetep_scf_rms_gradient>[+0-9.eEdD]+)\s*(?P<energy_total_scf_iteration>[-+0-9.eEdD]*)\s*\<\-\-\sCG\s*",
                        #     repeats = True)]),

                    SM(sections = ['section_scf_iteration'],
                        startReStr = r"\s*[0-9]+\s*(?P<x_onetep_scf_rms_gradient__hartree>[+0-9.eEdD]+)\s*(?P<energy_total_scf_iteration__hartree>[-+0-9.eEdD]*)\s*(?P<energy_change_scf_iteration__hartree>[-+0-9.eEdD]*)\s*[-+0-9.eEdD]*\s*",repeats = True,
                        # endReStr = r"\s*[0-9]+\s*(?P<x_onetep_scf_rms_gradient>[+0-9.eEdD]+)\s*(?P<energy_total_scf_iteration>[-+0-9.eEdD]*)\s*\<\-\-\sCG\s*",
                        endReStr = r"\s*[0-9]+\s*[+0-9.eEdD]+\s*[-+0-9.eEdD]*\s*\<\-\-\sCG\s*",
                        # subMatchers = [
                        #     SM(r"\s*[0-9]+\s*(?P<x_onetep_scf_rms_gradient>[+0-9.eEdD]+)\s*(?P<energy_total_scf_iteration>[-+0-9.eEdD]*)\s*\<\-\-\sCG\s*",
                        #     repeats = True)]),
                          ),
                    SM(r"\<QC\>\s*\[NGWF iterations]\:\s*(?P<x_onetep_n_ngwf_iterations>[0-9]*)\s*"),
                    SM(r"\<QC\>\s*\[total\_energy\]\:\s*(?P<energy_total__hartree>[-+0-9.eEdD]*)\s*"), # matching final converged total energy
                    SM(r"\<QC\>\s*\[rms\_gradient\]\:\s*(?P<x_onetep_final_rms_gradient__hartree>[-+0-9.eEdD]*)\s*"),
                    SM(r"\sPath coordinate\:\s*(?P<x_onetep_ts_coordinate_path>[-+0-9.eEdD]*)\s*"),
                    SM(r"\sEnergy of reactant\:\s*(?P<x_onetep_energy_reac__hartree>[-+0-9.eEdD]*)\s*"),
                    SM(r"\sEnergy of product\:\s*(?P<x_onetep_energy_prod__hartree>[-+0-9.eEdD]*)\s*"),
                    SM(r"\sEnergy of LST maximum\:\s*(?P<x_onetep_energy_lst_max__hartree>[-+0-9.eEdD]*)\s*"),
                    SM(r"\sLocation of LST maximum\:\s*(?P<x_onetep_location_lst_max__hartree>[-+0-9.eEdD]*)\s*"),
                    SM(r"\sBarrier from reactant\:\s*(?P<x_onetep_barrier_reac__hartree>[-+0-9.eEdD]*)\s*"),
                    SM(r"\sBarrier from product\:\s*(?P<x_onetep_barrier_prod__hartree>[-+0-9.eEdD]*)\s*"),
                    SM(r"\sEnergy of reaction\:\s*(?P<x_onetep_reaction_energy__hartree>[-+0-9.eEdD]*)\s*"),
                    SM(startReStr = r"\*\*\*\*\**\sIon\-Ion forces\s*\*\*\*\*\**\s*",
                         endReStr = r"TOTAL\:\s*",
                         subMatchers = [

                                    SM(r"\*\s*[A-Za-z]+\s*[0-9]+\s*(?P<x_onetep_store_atom_ionforces>[-\d\.]+\s+[-\d\.]+\s+[-\d\.]+)\s\*",
                                        repeats = True)
                         ]),
                    SM(startReStr = r"\*\*\*\*\** Local potential forces \*\*\*\*\**\s*",
                         endReStr = r"TOTAL\:\s*",
                         subMatchers = [

                                    SM(r"\*\s*[A-Za-z]+\s*[0-9]+\s*(?P<x_onetep_store_atom_localforces>[-\d\.]+\s+[-\d\.]+\s+[-\d\.]+)\s\*",
                                        repeats = True)
                         ]),
                    SM(startReStr = r"\*\*\*\*\** Non\-Local potential forces \*\*\*\*\**\s*",
                         endReStr = r"TOTAL\:\s*",
                         subMatchers = [

                                    SM(r"\*\s*[A-Za-z]+\s*[0-9]+\s*(?P<x_onetep_store_atom_nonlocalforces>[-\d\.]+\s+[-\d\.]+\s+[-\d\.]+)\s\*",
                                        repeats = True)
                         ]),
                     SM(startReStr = r"\*\*\*\*\** NGWF non self\-consistent forces \*\*\*\*\**\s*",
                         endReStr = r"TOTAL\:\s*",
                         subMatchers = [

                                    SM(r"\*\s*[A-Za-z]+\s*[0-9]+\s*(?P<x_onetep_store_atom_nonselfforces>[-\d\.]+\s+[-\d\.]+\s+[-\d\.]+)\s\*",
                                        repeats = True)
                         ]),
                    SM(startReStr = r"\*\*\** Correction to ensure the total force is zero \*\*\**\s*",
                         endReStr = r"TOTAL\:\s*",
                         subMatchers = [

                                    SM(r"\*\s*[A-Za-z]+\s*[0-9]+\s*(?P<x_onetep_store_atom_corrforces>[-\d\.]+\s+[-\d\.]+\s+[-\d\.]+)\s\*",
                                        repeats = True)
                         ]),
                    SM(startReStr = r"\*\*\*\*\** Forces \*\*\*\*\**\s*",
                         subMatchers = [

                                    SM(r"\*\s*[A-Za-z]+\s*[0-9]+\s*(?P<x_onetep_store_atom_forces>[-\d\.]+\s+[-\d\.]+\s+[-\d\.]+)\s\*",
                                        repeats = True)
                         ]),
                    SM(startReStr = r"\s*Forces\: Cartesian components\: Ha\/Bohr\s*",
                         subMatchers = [

                                    SM(r"\s*\+\s*[A-Za-z]+\s*[0-9]+\s*(?P<x_onetep_store_atom_forces>[-\d\.]+\s+[-\d\.]+\s+[-\d\.]+)\s*\+",
                                        repeats = True)
                         ]),

                    geomOptimSubMatcher,
                    SM(r"\sBFGS\s\:\sGeometry optimization (?P<x_onetep_geom_converged>[a-z]+) to converge after\s*"),
                    SM(r"\s[A-Za-z]+\:\sGeometry\soptimization\scompleted\s(?P<x_onetep_geom_converged>[a-z]+)\.\s*"),
                    geomOptim_finalSubMatcher,

        ])


    LRTDDFTSubMatcher = SM(name = 'LRTDDFT',
                startReStr = r"\s*\|\s*LR\-TDDFT energy\s*\=\s*[+0-9.eEdD]+\s*\|",
                # startReStr = r"\#* LR\_TDDFT CG iteration\s*[0-9]+\s\#*",
                sections = ["x_onetep_section_tddft"],
                # repeats =True,
                subMatchers = [
                    # SM(r"\s*\|\s*LR\-TDDFT energy\s*\=\s*(?P<x_onetep_tddft_energy_store>[+0-9.eEdD]+)\s*\|"), # matching final converged total free energy
                    SM(r"\s*\|\s*Change in omega\s*\=\s*(?P<x_onetep_tddft_omega_change>[-+0-9.eEdD]*)"),  # 0K corrected final SCF energy
                    SM(r"\s*\|\s*RMS gradient\s*\=\s*(?P<x_onetep_tddft_rms_gradient>[+-0-9.eEdD]*)"),
                    SM(r"\*+ Number of newly converged states\:\s*(?P<x_onetep_tddft_number_conv_states>[0-9.]*)\*+"),

                    SM(startReStr = r"\s*\|ITER\|\s*Total Energy\s*\|\s*Penalty value\s*\|\s*step",
                       sections = ["x_onetep_section_tddft_iterations"],
                       subMatchers = [
                           SM(r"\s*[0-9.]+\s*(?P<x_onetep_tddft_energy_store>[+0-9.eEdD]+)+\s*(?P<x_onetep_tddft_penalties_store>[+0-9.eEdD]+)\s*(?P<x_onetep_tddft_step_store>[\d.]+)",repeats = True),
                        ]),
                    SM(startReStr = r"   \|Excitation\|    Energy \(in Ha\)   \|     Oscillator Str\.  \| Lifetime \(in ns\)",
                       sections = ["x_onetep_section_tddft_excitations"],
                       subMatchers = [
                           SM(r"\s*[0-9.]+\s*(?P<x_onetep_tddft_excit_energy_store>[+0-9.eEdD]+)\s*(?P<x_onetep_tddft_excit_oscill_str_store>[\d.]+)\s*(?P<x_onetep_tddft_excit_lifetime_store>[\d.]+)",repeats = True,endReStr = "\n"),
                        ]),

                    ])

    MDSubMatcher = SM(name = 'MD',
                startReStr = r"\sStarting MD iteration\s*[0-9.]+\s\.\.\.\s*",
                #endReStr = r"BFGS\: finished iteration     0 with enthalpy\= \-2\.14201700E\+002 eV",
                sections = ["x_onetep_section_SCF_iteration_frame"],
                # sections = ["section_single_configuration_calculation"],
                endReStr = r"\s\.\.\.\sfinished MD iteration\s*[0-9.]+\s*",
                repeats =True,
                subMatchers = [
                    # SM(r"\s*[0-9]+\s*(?P<onetep_SCF_frame_energy>[-+0-9.eEdD]*)\s*[-+0-9.eEdD]*\s*[0-9.]*\s*\<\-\-\sSCF\s*",
                    #     endReStr = "\n",
                    #     repeats = True),
                    SM(r"\s*[0-9]+\s*(?P<x_onetep_SCF_frame_energy>[-+0-9.eEdD]*)\s*[-+0-9.eEdD]*\s*(?P<x_onetep_SCF_frame_energy_gain>[-+0-9.eEdD]*)\s*(?P<x_onetep_frame_time_scf_iteration_wall_end>[0-9.]*)\s*\<\-\-\sSCF\s*",
                        endReStr = "\n",
                        repeats = True),
                    SM(r"Final free energy\s*\(E\-TS\)\s*= *(?P<x_onetep_frame_energy_free>[-+0-9.eEdD]*)"), # matching final converged total free energy
                    SM(r"NB est\. 0K energy\s*\(E\-0\.5TS\)\s*= *(?P<x_onetep_frame_energy_total_T0>[-+0-9.eEdD]*)"), # 0K corrected final SCF energy
                    SM(startReStr = r"\s*x\s*MD\sData\:\s*x",
                         subMatchers = [
                            SM(r"\s*x\s*time\s*\:\s*(?P<x_onetep_frame_time>[+0-9.eEdD]+)\s*ps\s*x\s*"),
                         ]),


                    ])
    ########################################
    # Sub matcher for geometry optimisation
    ########################################




    Mulliken_SubMatcher = SM (name = 'Mulliken population analysis',
            startReStr = r"\s*Mulliken Atomic Populations\s*",
            sections = ['x_onetep_section_mulliken_population_analysis'],
            endReStr = r"\s*Bond\s*Population\s*Spin\s*Length\s\(bohr\)\s*",
            #endReStr = r"\s*Bond\s*Population\s*Length\s\(A\)\s*",
            repeats = True,
            subMatchers = [
                SM(r"\s*[a-zA-Z]+\s*[0-9.]+\s*(?P<x_onetep_total_orbital_store>[0-9.]+)\s*(?P<x_onetep_mulliken_charge_store>[0-9.]+)\s*", repeats = True),
                SM(r"\s*[a-zA-Z]+\s*[0-9.]+\s*(?P<x_onetep_total_orbital_store>[0-9.]+)\s*(?P<x_onetep_mulliken_charge_store>[0-9.]+)\s*(?P<x_onetep_spin_store>[0-9.]+)\s*",

                    repeats = True),
                 ])
    Natural_SubMatcher = SM (name = 'Natural population analysis',
            startReStr = r"\s*Natural Population\s*",
            sections = ['x_onetep_section_nbo_population_analysis'],
            endReStr = r"\=\=\=\=\=\=*\s*",
            repeats = True,
            subMatchers = [
                SM(r"\s(?P<x_onetep_nbo_atom_label_store>[a-zA-Z-0-9]+)\s*[0-9.]+\s*(?P<x_onetep_total_nbo_population_store>[\d\.]+)\s*(?P<x_onetep_nbo_partial_charge_store>[-\d\.]+)\s*", repeats = True),
                SM(r"\sTotal charge \(e\)\:\s*(?P<x_onetep_nbo_total_charge>[\d\.]+)\s*",

                    repeats = True),
                 ])



    Orbital_SubMatcher_2 = SM (name = 'Orbital Information',
            startReStr = r"\s*\.\.\.\.\.\.\.\s*\-\-\- gap \-\-\s*\.\.\.\.\.\.\.\.\.\s*",
            # sections  =[''],
            # sections = ['x_onetep_section_orbital_information'],
            forwardMatch = True,
            endReStr = r"\s*\.\.\.\.\.\.\.\s*\.*\s*\.\.\.\.\.\.\.\.\.\s*",
            # endReStr =r"\s*\.\.\.\.\.\.\.\s*\-\-\- gap \-\-\s*\.\.\.\.\.\.\.\.\.\s*",

            subMatchers = [
                SM(r"\s*(?P<x_onetep_orbital_number_store>[0-9]+)\s*(?P<x_onetep_orbital_energy_store>[-\d\.]+)\s*(?P<x_onetep_orbital_occupancy_store>[\d\.]+)\s*",repeats=True),
                 ])
    Orbital_SubMatcher_3 = SM (name = 'Orbital Information',
            startReStr = r"\s*\.\.\.\.\.\.\.\s*\.*\s*\.\.\.\.\.\.\.\.\.\s*",
            # sections = ['x_onetep_section_orbital_information'],
            # sections = [''],
            endReStr = "\n",
            # endReStr =r"\s*\.\.\.\.\.\.\.\s*\-\-\- gap \-\-\s*\.\.\.\.\.\.\.\.\.\s*",

            subMatchers = [
                SM(r"\s*(?P<x_onetep_orbital_number_store>[0-9]+)\s*(?P<x_onetep_orbital_energy_store>[-\d\.]+)\s*(?P<x_onetep_orbital_occupancy_store>[\d\.]+)\s*",repeats=True),
                 ])
    Orbital_SubMatcher = SM (name = 'Orbital Information',
            startReStr = r"\=\=\=\=\=\=\=\=\=\=\=\=\=\=\=\=\=\=\= Orbital energy and occupancy information \=\=\=\=\=\=\=\=\=\=\=\=\=\=\=\=\=\=\=\s*",
            sections = ['x_onetep_section_orbital_information'],
            forwardMatch = True,
            # endReStr = "\n",
            endReStr =r"\s*\.\.\.\.\.\.\.\s*\-\-\- gap \-\-\s*\.\.\.\.\.\.\.\.\.\s*",

            subMatchers = [
                SM(r"\s*Total number of orbitals\:\s*(?P<x_onetep_total_number_orbitals>[0-9]+)\s*"),
                SM(r"\s*Number of occupied orbitals\:\s*(?P<x_onetep_total_number_occ_orbitals>[0-9]+)\s*"),
                SM(r"\s*Occupancy sum\:\s*(?P<x_onetep_occupancy_sum>[\d\.]+)\s*"),
                SM(r"\s*HOMO\-LUMO gap\:\s*(?P<x_onetep_homo_lumo_gap__hartree>[\d\.]+)\s*"),
                SM(r"\s*Mid\-gap level\:\s*(?P<x_onetep_mid_gap__hartree>[\d\.]+)\s*"),
                SM(r"\s*(?P<x_onetep_orbital_number_store>[0-9]+)\s*(?P<x_onetep_orbital_energy_store>[-\d\.]+)\s*(?P<x_onetep_orbital_occupancy_store>[\d\.]+)\s*",repeats=True),
                Orbital_SubMatcher_2 ,

                Orbital_SubMatcher_3,
                 ])


    Dipole_moments = SM (name = 'Dipole moments',
            startReStr = r"\=\=\=\=\=*\s* Dipole Moment Calculation \=\=\=\=\=*\s*",
            sections = ['x_onetep_section_dipole'],

            # endReStr = r"\=*\s*",
            # endReStr =r"\s*\.\.\.\.\.\.\.\s*\-\-\- gap \-\-\s*\.\.\.\.\.\.\.\.\.\s*",

            subMatchers = [
                SM(r"Electronic dipole moment \(e\.bohr\)\:\s*dx\s\=\s*(?P<x_onetep_electronic_dipole_moment_store>[-\d\.]+)\s*"),
                SM(r"\s*dy\s\=\s*(?P<x_onetep_electronic_dipole_moment_store>[-\d\.]+)\s*") ,
                SM(r"\s*dz\s\=\s*(?P<x_onetep_electronic_dipole_moment_store>[-\d\.]+)\s*"),
                SM(r"\s*Magnitude\s\(e\.bohr\)\:\s*(?P<x_onetep_electronic_dipole_moment_magnitude>[-\d\.]+)\s*"),
                SM(r"\s*Ionic dipole moment \(e\.bohr\)\:\s*dx\s\=\s*(?P<x_onetep_ionic_dipole_moment_store>[-\d\.]+)\s*"),
                SM(r"\s*dy\s\=\s*(?P<x_onetep_ionic_dipole_moment_store>[-\d\.]+)\s*") ,
                SM(r"\s*dz\s\=\s*(?P<x_onetep_ionic_dipole_moment_store>[-\d\.]+)\s*"),
                SM(r"\s*Magnitude\s\(e\.bohr\)\:\s*(?P<x_onetep_ionic_dipole_moment_magnitude>[-\d\.]+)\s*"),
                SM(r"\s*Total dipole moment \(e\.bohr\)\:\s*dx\s\=\s*(?P<x_onetep_total_dipole_moment_store>[-\d\.]+)\s*"),
                SM(r"\s*dy\s\=\s*(?P<x_onetep_total_dipole_moment_store>[-\d\.]+)\s*"),
                SM(r"\s*dz\s\=\s*(?P<x_onetep_total_dipole_moment_store>[-\d\.]+)\s*"),
                SM(r"\s*Magnitude\s\(e\.bohr\)\:\s*(?P<x_onetep_total_dipole_moment_magnitude>[-\d\.]+)\s*"),
                 ])


    ########################################
    # return main Parser ###################
    ########################################
    return SM (name = 'Root',
        startReStr = "",
        forwardMatch = True,
        weak = True,
        subMatchers = [
        SM (name = 'NewRun',
            startReStr = r"\s\|\s*Linear-Scaling Ab Initio Total Energy Program\s*\|\s*",
            required = True,
            forwardMatch = True,
            sections = ['section_run'],
            subMatchers = [



                SM(name = 'ProgramHeader',
                  startReStr = r"\s\|\s*Linear-Scaling Ab Initio Total Energy Program\s*\|\s*",
                  subMatchers = [

                     SM(r"\s\|\s*Version\s(?P<program_version>[0-9a-zA-Z_.]*)"),
                     #SM(r"\s\|\s*in all publications arising from your use of (?P<program_name>[a-zA-Z]+)*"),
                     SM(r"\s\|\s*(?P<program_name>[a-zA-Z]+)\sis based on developments described in the following\s*\|\s*"),
                     SM(r"\s*Default threads\:\s(?P<x_onetep_number_of_processors>[0-9.]*)"),


                                  ]), # CLOSING SM ProgramHeader

                SM(name = 'input',
                  startReStr = r"\-\-\-\-\-* INPUT FILE \-\-\-\-\-*",
                  subFlags = SM.SubFlags.Unordered,
                  endReStr = r"\-\-\-\-\-* END INPUT FILE \-\-\-\-\-*",
                  subMatchers = [

                        SM(r"is\_smeared\_ion\_rep*(?P<x_onetep_is_smearing>[a-zA-Z]+)"),
                        SM(r"pbc\_correction\_cutoff*(?P<x_onetep_pbc_cutoff>[0-9a-zA-Z_.]*)"),
                        TSParameterSubMatcher,
                        LRTDDFT_parametersSubMatcher,
                        NGWFSubMatcher,
                        VanderWaalsParameterSubMatcher,
                        edftCalculationSubMatcher,
                        ElectronicMinimisParameterSubMatcher,
                        GeomOptimParameterSubMatcher,
                        calculationMethodSubMatcher,

                        basisSetCellAssociatedSubMatcher,

                        SM(name = 'Atom_topology',
                          startReStr = r"\%block\s*species\s*",

                          # endReStr = r"\%endblock species\s*",
                          #forwardMatch = True,
                          sections = ['section_topology'],
                          subMatchers = [

                              SM(r"[0-9a-zA-Z]+\s*(?P<x_onetep_store_atom_name>[a-zA-Z]+)\s*(?P<x_onetep_store_atom_mass>[0-9.]+)\s*(?P<x_onetep_n_ngwf_atom_store>[0-9.]+)\s*(?P<x_onetep_ngwf_radius_store>[\d\.]+)\s*",
                                #endReStr = "\n",
                                repeats = True),
                             ]) # CLOSI

                    ]),


                ElectronicParameterSubMatcher,
                LRTDDFTSubMatcher,
                edft_SubMatcher,
                TSSubMatcher,
                # KernelOptimSubMatcher,
                # energycomponentsSubMatcher,
                singlepointSubMatcher,

                Dipole_moments,
                Mulliken_SubMatcher,
                Natural_SubMatcher,

                Orbital_SubMatcher,


                #pdos,
                SM(name = 'calc_time',
                    startReStr = r"\-\-\-*\sTIMING INFORMATION\s\-\-\-*",
                    #sections = ['x_onetep_section_time'],
                    subMatchers = [
                        SM(r"AVERAGE TIME\:\s*(?P<x_onetep_avarage_time>[0-9.]*)"), # matching final converged total energy
                        SM(r"TOTAL TIME\:\s*(?P<time_run_wall_end>[0-9.]*)"),
                        SM(r"Job completed\:\s*(?P<x_onetep_final_date>[0-9.-]*)(?P<x_onetep_final_time>[0-9.:]*)"),
                                      ]), # CLOSING section_onetep_time


                ])



        ]) # CLOSING SM NewRun



def get_cachingLevelForMetaName(metaInfoEnv):
    """Sets the caching level for the metadata.

    Args:
        metaInfoEnv: metadata which is an object of the class InfoKindEnv in nomadcore.local_meta_info.py.

    Returns:
        Dictionary with metaname as key and caching level as value.
    """
    # manually adjust caching of metadata
    cachingLevelForMetaName = { 'x_onetep_ir_intensity_store' : CachingLevel.Cache,
                                'x_onetep_ir_store' : CachingLevel.Cache,
                                'x_onetep_vibrationl_frequencies_store' : CachingLevel.Cache,
                                'x_onetep_n_iterations_phonons' : CachingLevel.Cache,
                                'x_onetep_mulliken_charge_store' : CachingLevel.Cache,
                                'x_onetep_orbital_contributions' : CachingLevel.Cache,
                                # 'x_onetep_section_cell_optim': CachingLevel.Cache,
                                'x_onetep_section_atom_positions_optim' : CachingLevel.Cache,
                                'x_onetep_section_eigenvalues':CachingLevel.Cache,
                                'x_onetep_section_k_points':CachingLevel.Cache,
                                'x_onetep_section_k_band':CachingLevel.Cache,
                                'x_onetep_tddft_penalties_store':CachingLevel.Cache,
                                'x_onetep_tddft_energy_store':CachingLevel.Cache,
                                'x_onetep_tddft_step_store':CachingLevel.Cache,
                                'x_onetep_tddft_excit_energy_store':CachingLevel.Cache,
                                "x_onetep_tddft_excit_oscill_str_store":CachingLevel.Cache,
                                'x_onetep_section_tddft_iterations':CachingLevel.Cache,
                                'x_onetep_section_tddft_excitations':CachingLevel.Cache,
                                # 'band_energies' : CachingLevel.Cache,
                                # 'band_k_points' : CachingLevel.Cache,
                                'x_onetep_basis_set_planewave_cutoff' : CachingLevel.Cache,
                                # 'eigenvalues_values': CachingLevel.Cache,
                                # 'eigenvalues_kpoints':CachingLevel.Cache,
                                'x_onetep_number_of_scf_iterations_store':CachingLevel.Cache,
                                'x_onetep_tddft_excit_lifetime_store':CachingLevel.Cache,
                                "x_onetep_disp_method_name_store":CachingLevel.Cache,
                                'x_onetep_total_energy_corrected_for_finite_basis_store': CachingLevel.Cache,
                                'x_onetep_frame_time':CachingLevel.Cache,
                                'x_onetep_section_SCF_iteration_frame':CachingLevel.Cache,
                                'x_onetep_raman_activity_store': CachingLevel.Cache,
                                'x_onetep_SCF_frame_energy_gain':CachingLevel.Cache,
                                'x_onetep_frame_energy_free':CachingLevel.Cache,
                                'x_onetep_frame_energy_total_T0':CachingLevel.Cache,
                                'x_onetep_frame_time_scf_iteration_wall_end':CachingLevel.Cache,
                                'x_onetep_total_orbital_store':CachingLevel.Cache,
                                'x_onetep_mulliken_charge_store':CachingLevel.Cache,
                                'x_onetep_spin_store':CachingLevel.Cache,
                                'x_onetep_ngwf_radius_store':CachingLevel.Cache,
                                'x_onetep_n_ngwf_atom_store':CachingLevel.Cache,
                                'x_onetep_section_energy_components':CachingLevel.Cache,
                                'x_onetep_SCF_frame_energy':CachingLevel.Cache,
                                'x_onetep_electronic_kinetic_energy':CachingLevel.Cache,
                                'x_onetep_pseudo_local_store' :CachingLevel.Cache,
                                'x_onetep_pseudo_non_local_store':CachingLevel.Cache,
                                'x_onetep_nbo_atom_label_store':CachingLevel.Cache,
                                'x_onetep_total_nbo_population_store':CachingLevel.Cache,
                                'x_onetep_nbo_partial_charge_store':CachingLevel.Cache,
                                'x_onetep_energy_correction_hartree_store':CachingLevel.Cache,
                                'x_onetep_energy_XC_store':CachingLevel.Cache,
                                'x_onetep_ewald_correction_store':CachingLevel.Cache,
                                'x_onetep_electronic_dipole_moment_store':CachingLevel.Cache,
                                'x_onetep_ionic_dipole_moment_store':CachingLevel.Cache,
                                'x_onetep_total_dipole_moment_store' :CachingLevel.Cache,
                                'x_onetep_orbital_occupancy_store':CachingLevel.Cache,
                                'x_onetep_orbital_number_store':CachingLevel.Cache,
                                'x_onetep_orbital_energy_store':CachingLevel.Cache,
                                'x_onetep_dispersion_correction_store' :CachingLevel.Cache,
                                'x_onetep_integrated_density_store':CachingLevel.Cache,
                                }

    # Set caching for temparary storage variables
    for name in metaInfoEnv.infoKinds:
        if (   name.startswith('x_onetep_store_')
            or name.startswith('x_onetep_cell_')):
            cachingLevelForMetaName[name] = CachingLevel.Cache
    return cachingLevelForMetaName


# get main file description
onetepMainFileSimpleMatcher = build_onetepMainFileSimpleMatcher()


class OnetepParser():
    """ A proper class envolop for running this parser from within python. """
    def __init__(self, backend, **kwargs):
        self.backend_factory = backend

    def parse(self, mainfile):
        from unittest.mock import patch
        logging.debug('dmol3 parser started')
        logging.getLogger('nomadcore').setLevel(logging.WARNING)
        backend = self.backend_factory("onetep.nomadmetainfo.json")
        with patch.object(sys, 'argv', ['<exe>', '--uri', 'nmd://uri', mainfile]):
            mainFunction(
                mainFileDescription=onetepMainFileSimpleMatcher,
                metaInfoEnv=None,
                parserInfo={'name':'onetep-parser', 'version': '1.0'},
                cachingLevelForMetaName=get_cachingLevelForMetaName(backend.metaInfoEnv()),
                superContext=OnetepParserContext(),
                defaultSectionCachingLevel = True,
                superBackend=backend)

        return backend
