# Copyright 2016-2018 Daria M. Tomecka, Fawzi Mohamed
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

################################################################
# This is the parser for the main output file of Fleur (out) - adapted for version fleur26e
################################################################

from builtins import object
from nomadcore.simple_parser import SimpleMatcher as SM
from nomadcore.simple_parser import mainFunction, AncillaryParser, CachingLevel
from nomadcore.local_meta_info import loadJsonFile, InfoKindEl
import os, sys, json, logging
import numpy as np
#import fleur_parser_inp
#import fleur_XML_parser


__author__ = "Daria M. Tomecka"
__maintainer__ = "Daria M. Tomecka"
__email__ = "tomeckadm@gmail.com;"
__date__ = "15/05/2017"

class FleurContext(object):
    """context for the fleur parser"""

    def __init__(self):
        self.parser = None
        self.rootSecMethodIndex = None
        self.secMethodIndex = None
        self.secSystemIndex = None

    def initialize_values(self):
        """allows to reset values if the same superContext is used to parse different files"""
       # pass

#        self.metaInfoEnv = self.parser.parserBuilder.metaInfoEnv

        self.rootSecMethodIndex = None
        self.secMethodIndex = None
        self.secSystemIndex = None
        self.scfIterNr = 0

        self.equiv_atom_labels = []
        self.equiv_atom_pos = []


    def startedParsing(self, path, parser):
        """called when parsing starts"""
        self.parser = parser
        self.metaInfoEnv = self.parser.parserBuilder.metaInfoEnv

        # allows to reset values if the same superContext is used to parse different files
        self.initialize_values()

    def onClose_x_fleur_header(self, backend, gIndex, section):
        backend.addValue("program_version",
                         section["x_fleur_version"][0])


    def onOpen_section_system(self, backend, gIndex, section):
        self.equiv_atom_labels = []
        self.equiv_atom_pos = []

        mainFile = self.parser.fIn.fIn.name
        fName = mainFile[:-4] + ".inp"
        if os.path.exists(fName):
            structSuperContext = fleur_parser_inp.FleurInpContext()
            structParser = AncillaryParser(
                fileDescription = fleur_parser_inp.buildStructureMatchers(),
                parser = self.parser,
                cachingLevelForMetaName = fleur_parser_inp.get_cachingLevelForMetaName(self.metaInfoEnv, CachingLevel.PreOpenedIgnore),
                superContext = inpSuperContext)

            with open(fName) as fIn:
                inpParser.parseFile(fIn)



        mainFile = self.parser.fIn.fIn.name
        fName = mainFile[:-4] + ".xml"
        if os.path.exists(fName):
            xmlSuperContext = fleur_parser_xml.FleurXmlContext()
            xmlParser = AncillaryParser(
                fileDescription = fleur_parser_xml.buildXmlMatchers(),
                parser = self.parser,
                cachingLevelForMetaName = fleur_parser_xml.get_cachingLevelForMetaName(self.metaInfoEnv, CachingLevel.PreOpenedIgnore),
                superContext = xmlSuperContext)

            with open(fName) as fIn:
                xmlParser.parseFile(fIn)


        #if self.secSystemIndex is None:
        self.secSystemIndex = gIndex
        #        self.secSystemIndex["single_configuration_calculation_to_system_ref"] = gIndex


    def onClose_section_single_configuration_calculation(self, backend, gIndex, section):
        """Trigger called when section_single_configuration_calculation is opened.
        """
        # write number of SCF iterations
        backend.addValue('number_of_scf_iterations', self.scfIterNr)

        # write the references to section_method and section_system
        #        method_index = self.secMethodIndex("single_configuration_to_calculation_method_ref")
        #        if method_index is not None:

        backend.addValue('single_configuration_to_calculation_method_ref', self.secMethodIndex)
        #        system_index = self.secSystemIndex("single_configuration_calculation_to_system_ref")
        #        if system_index is not None:

        backend.addValue('single_configuration_calculation_to_system_ref', self.secSystemIndex)


    def onOpen_section_method(self, backend, gIndex, section):
        #if self.secMethodIndex is None:
        if self.rootSecMethodIndex is None:
            self.rootSecMethodIndex = gIndex
        self.secMethodIndex = gIndex
#        self.secMethodIndex["single_configuration_to_calculation_method_ref"] = gIndex

    def onClose_x_fleur_section_equiv_atoms(self, backend, gIndex, section):
        label = section["x_fleur_atom_name"][0]
        x = section["x_fleur_atom_pos_x"]
        y = section["x_fleur_atom_pos_y"]
        z = section["x_fleur_atom_pos_z"]
        if len(x) != len(y) or len(x) != len(z):
            raise Exception("incorrect parsing, different number of x,y,z components")
        groupPos = [[x[i], y[i], z[i]] for i in range(len(x))]
        nAt = len(groupPos)

        self.equiv_atom_labels += [label for i in range(nAt)]
        self.equiv_atom_pos += groupPos

    def onClose_section_system(self, backend, gIndex, section):

        #backend.addValue("smearing_kind", x_fleur_smearing_kind)
        smearing_kind = section['x_fleur_smearing_kind']
        if smearing_kind is not None:
        #    value = ''
            backend.addValue('x_fleur_smearing_kind', value)


        smearing_width = section['x_fleur_smearing_width']
        if smearing_width is not None:
        #    value = ''
            backend.addValue('x_fleur_smearing_width', value)



         #------1.atom_positions
        atom_pos = []
        for i in ['x', 'y', 'z']:
            api = section['x_fleur_atom_pos_' + i]
            if api is not None:
               atom_pos.append(api)
               logging.error("atom_pos: %s x %s y %s z %s",atom_pos, x, y, z)
        if atom_pos:
            # need to transpose array since its shape is [number_of_atoms,3] in the metadata
            backend.addArrayValues('atom_positions', np.transpose(np.asarray(atom_pos)), gIndex)
        elif len(self.equiv_atom_pos) > 0:
            backend.addArrayValues('atom_positions', np.asarray(self.equiv_atom_pos), gIndex)

         #------2.atom labels
        atom_labels = section['x_fleur_atom_name']
        if atom_labels is not None:
            backend.addArrayValues('atom_labels', np.asarray(atom_labels), gIndex)
        elif len(self.equiv_atom_labels) > 0:
            backend.addArrayValues('atom_labels', np.asarray(self.equiv_atom_labels), gIndex)

        #------3.atom force
        atom_force = []
        for i in ['x', 'y', 'z']:
            api = section['x_fleur_tot_for_' + i]
            if api is not None:
               atom_force.append(api)
        if atom_force:
            # need to transpose array since its shape is [number_of_atoms,3] in the metadata
           backend.addArrayValues('atom_forces', np.transpose(np.asarray(atom_force)))

        #----4. unit_cell
        unit_cell = []
        for i in ['x', 'y', 'z']:
            uci = section['x_fleur_lattice_vector_' + i]
            if uci is not None:
                unit_cell.append(uci)
        if unit_cell:
           backend.addArrayValues('simulation_cell', np.asarray(unit_cell))
           backend.addArrayValues("configuration_periodic_dimensions", np.ones(3, dtype=bool))


    def onClose_section_scf_iteration(self, backend, gIndex, section):
        #Trigger called when section_scf_iteration is closed.

        # count number of SCF iterations
        self.scfIterNr += 1

    def onClose_x_fleur_section_XC(self, backend, gIndex, section):
        xc_index = section["x_fleur_exch_pot"]
        logging.info("winsectxc: %s -> %s", section, xc_index)
        if not xc_index:
            xc_index = ["pbe"]
        xc_map_legend = {

            'pbe': ['GGA_X_PBE', 'GGA_C_PBE'],

            'rpbe': ['GGA_X_PBE', 'GGA_C_PBE'],

            'Rpbe': ['GGA_X_RPBE'],

            'pw91': ['GGA_X_PW91','GGA_C_PW91'],

            'l91': ['LDA_C_PW','LDA_C_PW_RPA','LDA_C_PW_MOD','LDA_C_OB_PW'],

            'vwn': ['LDA_C_VWN','LDA_C_VWN_1','LDA_C_VWN_2','LDA_C_VWN_3','LDA_C_VWN_4','LDA_C_VWN_RPA'],

            'bh': ['LDA_C_VBH'],

            'pz':['LDA_C_PZ'],

            'x-a': [],

            'mjw': [],

            'wign': [],

            'hl': [],

            'xal': [],

            'relativistic': ['---']
            #http://dx.doi.org/10.1088/0022-3719/12/15/007

        }

        # Push the functional string into the backend
        xc_map_legend = xc_map_legend.get(xc_index[0])
        if not xc_map_legend:
            raise Exception("Unhandled xc functional %s found" % xc_index)

        for xc_name in xc_map_legend:
            s = backend.openSection("section_XC_functionals")
            backend.addValue("XC_functional_name", xc_name)
            backend.closeSection("section_XC_functionals", s)



#*

#    def onClose_section_run(self, backend, gIndex, section):
#        """Trigger called when section_run is closed.
#        """
        # reset all variables
#        self.initialize_values()
#        backend.addValue("energy_total", energy_total)
#        # frame sequence
#        sampling_method = "geometry_optimization"

#        samplingGIndex = backend.openSection("section_sampling_method")
#        backend.addValue("sampling_method", sampling_method)
#        backend.closeSection("section_sampling_method", samplingGIndex)
#        frameSequenceGIndex = backend.openSection("section_frame_sequence")
#        backend.addValue("frame_sequence_to_sampling_ref", samplingGIndex)
#        backend.addArrayValues("frame_sequence_local_frames_ref", np.asarray(self.singleConfCalcs))
#        backend.closeSection("section_frame_sequence", frameSequenceGIndex)



"""    def onClose_x_fleur_section_xml_file(self, backend, gIndex, section):

        x_fleur_loading_xml_file_list = section['x_fleur_loading_xml_file']

        xml_file = x_fleur_loading_xml_file_list[-1]

        if xml_file is not None:
           logger.warning("This output showed this calculation need to load xml file, so we need this xml file ('%s') to read geometry information" % os.path.normpath(xml_file) )
           fName = os.path.normpath(xml_file)

           xmlSuperContext = FleurXMLParser.FleurXMLParserContext(False)
           xmlParser = AncillaryParser(
                fileDescription = FleurXMLParser.build_FleurXMLFileSimpleMatcher(),
                parser = self.parser,
                cachingLevelForMetaName = FleurXMLParser.get_cachingLevelForMetaName(self.metaInfoEnv, CachingLevel.Ignore),
                superContext = xmlSuperContext)

           try:
                with open(fName) as fxml:
                     xmlParser.parseFile(fxml)

           except IOError:
                logger.warning("Could not find xml file in directory '%s'. " % os.path.dirname(os.path.abspath(self.fName)))
"""

#####################################################################################################
#                                          description of the input                                 #
#####################################################################################################

mainFileDescription = SM(
              name = 'root',
              weak = True,
              startReStr = "",
              subMatchers = [
                SM(name = 'newRun',
                startReStr = r"\s* This output is generated by\s*[\w*.]+\s*\w*\*\s\*",
                repeats = True,
                required = True,
                forwardMatch = True,
                sections   = ['section_run','section_method', 'section_system', 'section_single_configuration_calculation'],
                subMatchers = [
### header ###
                    SM(name = 'header',
                    startReStr = r"\s* This output is generated by\s*(?P<x_fleur_version>[\w*.]+)\s*\w*\*\s\*",
                    sections=["x_fleur_header"],
                    fixedStartValues={'program_name': 'fleur', 'program_basis_set_type': '(L)APW+lo' }
                   ),

                    SM(name = 'systemName',
                    #startReStr = r"\s*-{11}fl7para file ends here-{11}\s*",#L112
                    startReStr = r"\s*[0-9]*\s*f l a p w  version\s[\w].*",
                    sections = ["section_system"],
                    subMatchers=[
                     #   SM(r"\s*[0-9]*\s*f l a p w  version\s[\w].*"),
                        SM(r"\s{4}(?P<x_fleur_system_name>[\w*\s*]+)\n"),#L117
                        SM(r"\s*name of space group=(?P<x_fleur_space_group>.*)"),#L121

                        SM(name = 'unit cell',
                        startReStr = r"\sbravais matrices of real and reciprocal lattices",
                        subMatchers=[
                            SM(r"\s*(?P<x_fleur_lattice_vector_x__bohr>[-+0-9.]+)\s+(?P<x_fleur_lattice_vector_y__bohr>[-+0-9.]+)\s+(?P<x_fleur_lattice_vector_z__bohr>[-+0-9.]+)\s*(?P<x_fleur_rec_lattice_vector_x__bohr>[-+0-9.]+)\s+(?P<x_fleur_rec_lattice_vector_y__bohr>[-+0-9.]+)\s+(?P<x_fleur_rec_lattice_vector_z__bohr>[-+0-9.]+)",#L131-5
                            repeats = True
                           )
                        ]),

                        SM(r"\s*the volume of the unit cell omega-tilda=\s*(?P<x_fleur_unit_cell_volume>[0-9.]+)"),#L137
                        SM(r"\s*the volume of the unit cell omega=\s*(?P<x_fleur_unit_cell_volume_omega>[0-9.]+)"), #L138

                        # SM(r"\s*exchange-correlation:\s*(?P<x_fleur_exch_pot>\w*\s*.*)",sections = ['x_fleur_section_XC']), #L140
                        SM(r"\s*exchange-correlation:\s*(?P<x_fleur_exch_pot>\w*)\s*(?P<x_fleur_xc_correction>\w*\s*.*)",sections = ['x_fleur_section_XC']), #L140

                        SM(name = 'atomPositions',
                        startReStr = r"\s*(?P<x_fleur_atom_name>\w*)\s+(?P<x_fleur_nuclear_number>[0-9]+)\s+(?P<x_fleur_number_of_core_levels>[0-9]+)\s+(?P<x_fleur_lexpansion_cutoff>[0-9.]+)\s+(?P<x_fleur_mt_gridpoints>[0-9.]+)\s+(?P<x_fleur_mt_radius>[0-9.]+)\s+(?P<x_fleur_logarythmic_increment>[0-9.]+)",
                           sections=["x_fleur_section_equiv_atoms"],
                        repeats = True,
                           subMatchers=[
                               SM(name = 'equiv atoms',
                               startReStr = r"\s*(?P<x_fleur_atom_pos_x__bohr>[-+0-9.]+)\s+(?P<x_fleur_atom_pos_y__bohr>[-+0-9.]+)\s+(?P<x_fleur_atom_pos_z__bohr>[-+0-9.]+)\s+(?P<x_fleur_atom_coord_scale>[-+0-9.]*)",
                        #       sections=["x_fleur_section_equiv_atoms"],
                                  subMatchers = [
                                      SM(r"\s*(?P<x_fleur_atom_pos_x__bohr>[-+0-9.]+)\s+(?P<x_fleur_atom_pos_y__bohr>[-+0-9.]+)\s+(?P<x_fleur_atom_pos_z__bohr>[-+0-9.]+)\s+(?P<x_fleur_atom_coord_scale>[-+0-9.]*)",#L145
                                      repeats = True
                                     )
                                  ]
                              )
                           ]),


                        SM(r"\s* Suggested values for input:"),
                        SM(r"\s*k_max\s=\s*(?P<x_fleur_k_max>.*)"),#L154
                        SM(r"\s*G_max\s=\s*(?P<x_fleur_G_max>.*)"),#L155
                        SM(r"\s*volume of interstitial region=\s*(?P<x_fleur_vol_interstitial>[0-9.]+)"),#L157
                        SM(r"\s*number of atom types=\s*(?P<x_fleur_nr_of_atom_types>[0-9]+)"),#L160
                        SM(r"\s*total number of atoms=\s*(?P<x_fleur_total_atoms>[0-9]+)"),

                        SM(r"\s*(?P<x_fleur_smearing_kind>\w*)-integration is used\s*.*"),#L187
                        SM(r"\s*gaussian half width\s*=\s*(?P<x_fleur_smearing_width__hartree>[0-9.]+)"),#188
                        SM(r"\s*number of valence electrons=\s*(?P<x_fleur_nr_of_valence_electrons>[0-9.]+)"),#190
                        SM(r"\s*temperature broadening\s*=\s*(?P<x_fleur_smearing_temperature>[0-9.]+)"),#191

                        SM(r"\s*number of k-points for this window =\s*(?P<x_fleur_nkptd>[0-9]*)"), #723
                        SM(name = 'k-point',
                           startReStr = r"\s{11}coordinates\s{11}weights",
                           subMatchers = [
                               SM(r"\s+(?P<x_fleur_k_point_x>[-+0-9.]+)\s+(?P<x_fleur_k_point_y>[-+0-9.]+)\s+(?P<x_fleur_k_point_z>[-+0-9.]+)\s+(?P<x_fleur_k_point_weight>[-+0-9.]+)", repeats = True   #L725
                              )
                           ]),
                        SM(r"\s*total electronic charge   =\s*(?P<x_fleur_tot_elec_charge>.*)"),#L1107
                        SM(r"\s*total nuclear charge      =\s*(?P<x_fleur_tot_nucl_charge>.*)") #L1108

                    ]),
                    #Check problematic SM
                    SM(name = "scf iteration",
                       startReStr = r"\s*it=\s*(?P<x_fleur_iteration_number>[0-9]+)",
                       sections=["section_scf_iteration"],
                       repeats = True,
                       subMatchers=[
                           SM(r"\s*---->\s*total energy=\s*(?P<x_fleur_energy_total__hartree>[-+0-9.]+)\s*htr"),


                           SM(startReStr = r"\s*\W{5}\s+TOTAL FORCES ON ATOMS\s+\W{5}",
                              subMatchers = [
                                  SM(r"\sTOTAL FORCE FOR ATOM TYPE=\s*[0-9]\s+X=\s+(?P<x_fleur_tot_for_x>[0-9.]+)\s+Y=\s+(?P<x_fleur_tot_for_y>[0-9.]+)\s+Z=\s+(?P<x_fleur_tot_for_z>[0-9.]+)", repeats = True),#L3825 first
                                  SM(r"\s*FX_TOT=(?P<x_fleur_tot_for_fx>[-+0-9.]+)\sFY_TOT=(?P<x_fleur_tot_for_fy>[-+0-9.]+)\sFZ_TOT=(?P<x_fleur_tot_for_fz>[-+0-9.]+)", repeats = True)
                              ], repeats = True),


                           SM(r"\s*---->\s*.*tkb\*entropy.*=\s*(?P<x_fleur_entropy__hartree>[-+0-9.]+)\shtr"),
                           SM(r"\s*---->\s*free energy=\s*(?P<x_fleur_free_energy__hartree>[-+0-9.]+)\shtr")
                       ]
                   )
                ])
              ])

# which values to cache or forward (mapping meta name -> CachingLevel)

cachingLevelForMetaName = {

    "XC_functional_name": CachingLevel.ForwardAndCache,
#    "energy_total": CachingLevel.ForwardAndCache,


 }
# loading metadata from nomad-meta-info/meta_info/nomad_meta_info/fleur.nomadmetainfo.json

parserInfo = {
  "name": "Fleur_parser",
  "version": "1.0"
}

class FleurParser():
    """ A proper class envolop for running this parser from within python. """
    def __init__(self, backend, **kwargs):
        self.backend_factory = backend

    def parse(self, mainfile):
        from unittest.mock import patch
        logging.debug('fleur parser started')
        logging.getLogger('nomadcore').setLevel(logging.WARNING)
        backend = self.backend_factory("fleur.nomadmetainfo.json")
        with patch.object(sys, 'argv', ['<exe>', '--uri', 'nmd://uri', mainfile]):
            mainFunction(
                mainFileDescription=mainFileDescription,
                metaInfoEnv=None,
                parserInfo=parserInfo,
                superContext=FleurContext(),
                superBackend=backend)

        return backend
