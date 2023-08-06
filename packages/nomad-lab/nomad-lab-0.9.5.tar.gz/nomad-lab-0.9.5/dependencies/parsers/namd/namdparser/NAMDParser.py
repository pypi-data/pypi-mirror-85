# Copyright 2018-2018 Berk Onat, Fawzi Mohamed
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

from builtins import map
from builtins import range
from builtins import object
import numpy as np
import nomadcore.ActivateLogging
from nomadcore.caching_backend import CachingLevel
from nomadcore.simple_parser import SimpleMatcher as SM
from nomadcore.smart_parser import SmartParserCommon as SmartParser
from nomadcore.smart_parser.SmartParserCommon import get_metaInfo, conv_str, conv_int, conv_float, open_section
from nomadcore.smart_parser.SmartParserDictionary import getList_MetaStrInDict, getDict_MetaStrInDict
from nomadcore.smart_parser.SmartParserDictionary import isMetaStrInDict
from .NAMDDictionary import get_updateDictionary, set_Dictionaries
from .NAMDCommon import PARSERNAME, PROGRAMNAME, PARSERVERSION, PARSERTAG, LOGGER
from .NAMDCommon import PARSER_INFO_DEFAULT, META_INFO_PATH, set_excludeList, set_includeList
from nomadcore.md_data_access import MDDataAccess as MDDA
import argparse
import logging
import os
import re
import sys
import datetime
import io
from nomadcore.simple_parser import mainFunction

############################################################
# This is the parser for the main file of NAMD.
############################################################

#PRINTABLE = re.compile(r"\W+")

class NAMDParser(SmartParser.ParserBase):
    """Context for parsing NAMD main file.

    This class keeps tracks of several NAMD settings to adjust the parsing to them.
    The onClose_ functions allow processing and writing of cached values after a section is closed.
    They take the following arguments:
        backend: Class that takes care of writing and caching of metadata.
        gIndex: Index of the section that is closed.
        section: The cached values and sections that were found in the section that is closed.
    """
    def __init__(self):
        # dictionary of energy values, which are tracked between SCF iterations and written after convergence
        self.totalEnergyList = {
                                'energy_electrostatic': None,
                                'energy_total_T0_per_atom': None,
                                'energy_free_per_atom': None,
                               }
        SmartParser.ParserBase.__init__(
            self, re_program_name=re.compile(r"\s*"+PROGRAMNAME+"$"),
            parsertag=PARSERTAG, metainfopath=META_INFO_PATH,
            parserinfodef=PARSER_INFO_DEFAULT)

        set_Dictionaries(self)
        self.metaInfoEnv = get_metaInfo(self)
        self.secGIndexDict = {}

        self.cachingLevelForMetaName = {
                               PARSERTAG + '_trajectory_file_detect': CachingLevel.Cache,
                               PARSERTAG + '_geometry_optimization_cdetect': CachingLevel.Cache,
                               PARSERTAG + '_mdin_finline': CachingLevel.Ignore,
                               #PARSERTAG + '_section_input_output_files': CachingLevel.Ignore,
                               PARSERTAG + '_single_configuration_calculation_detect': CachingLevel.Cache,
                              }
        for name in self.metaInfoEnv.infoKinds:
            metaInfo = self.metaInfoEnv.infoKinds[name]
            if (name.startswith(PARSERTAG + '_mdin_') and
                metaInfo.kindStr == "type_document_content" and
                (PARSERTAG + "_mdin_method" in metaInfo.superNames or
                 PARSERTAG + "_mdin_run" in metaInfo.superNames or
                 PARSERTAG + "_mdin_system" in metaInfo.superNames) or
                name.startswith(PARSERTAG + '_parm_') and
                metaInfo.kindStr == "type_document_content" and
                (PARSERTAG + "_mdin_method" in metaInfo.superNames or
                 PARSERTAG + "_mdin_run" in metaInfo.superNames or
                 PARSERTAG + "_mdin_system" in metaInfo.superNames) or
                #name.startswith(PARSERTAG + '_mdin_file_') and
                name.startswith(PARSERTAG + '_inout_file_') or
                #metaInfo.kindStr == "type_document_content" and
                #(PARSERTAG + "_section_input_output_files" in metaInfo.superNames or
                # "section_run" in metaInfo.superNames) or
                name.startswith(PARSERTAG + '_inout_control_') or
                #(PARSERTAG + "_section_control_parameters" in metaInfo.superNames) or
                #name.startswith(PARSERTAG + '_mdin_') and
                #(PARSERTAG + "_section_control_parameters" in metaInfo.superNames) or
                name.startswith(PARSERTAG + '_mdout_') or
                name.startswith(PARSERTAG + '_mdout_') and
                #metaInfo.kindStr == "type_document_content" and
                (PARSERTAG + "_mdout_method" in metaInfo.superNames or
                 PARSERTAG + "_mdout_system" in metaInfo.superNames or
                 "section_run" in metaInfo.superNames or
                 PARSERTAG + "_mdout_single_configuration_calculation" in metaInfo.superNames)
                or name.startswith('section_single_configuration_calculation')
                or PARSERTAG + '_mdout' in metaInfo.superNames
                or 'section_sampling_method' in metaInfo.superNames
                or 'section_single_configuration_calculation' in metaInfo.superNames
               ):
                self.cachingLevelForMetaName[name] = CachingLevel.Cache
            if name in self.extraDict.keys():
                self.cachingLevelForMetaName[name] = CachingLevel.Ignore


    def initialize_values(self):
        """Initializes the values of certain variables.

        This allows a consistent setting and resetting of the variables,
        when the parsing starts and when a section_run closes.
        """
        set_Dictionaries(self)
        self.secGIndexDict.clear()
        self.secMethodGIndex = None
        self.secSystemGIndex = None
        self.secTopologyGIndex = None
        self.secSamplingGIndex = None
        self.secSingleGIndex = None
        self.secVDWGIndex = None
        self.secAtomType = None
        self.inputMethodIndex = None
        self.inputControlIndex = None
        self.mainMethodIndex = None
        self.mainCalcIndex = None
        self.MD = True
        self.topoDict = None
        self.topologyTable = None
        self.topologyBonds = None
        self.topology = None
        self.topologyFormat = None
        self.topologyFile = None
        self.trajectory = None
        self.trajectoryFormat = None
        self.trajectoryFile = None
        self.readChunk = 300
        self.boxlengths = None
        self.latticevectors = None
        self.atompositions = None
        self.inputcoords = None
        self.inputpositions = None
        self.outputcoords = None
        self.outputpositions = None
        # start with -1 since zeroth iteration is the initialization
        self.MDiter = -1
        self.MDstep = 1
        self.MDcurrentstep = -1
        self.MDnextstep = 0
        self.singleConfCalcs = []
        self.minConverged = None
        self.parsedLogFile = False
        self.LogSuperContext = None
        self.forces_raw = []
        self.ffparams = []
        self.lastCalculationGIndex = None
        self.logFileName = None
        self.lastfInLine = None
        self.lastfInMatcher = None
        self.secOpen = open_section
        self.superP = self.parser.backend.superBackend
        self.MDData = MDDA.MDDataAccess()
        if self.recordList:
            self.recordList.close()
        self.recordList = io.StringIO()

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

    #def peekline(self, parser):
    #    pos = parser.fIn.fIn.tell()
    #    line = parser.fIn.fIn.readline()
    #    parser.fIn.fIn.seek(pos)
    #    return line

    def onClose_section_run(self, backend, gIndex, section):
        """Trigger called when section_run is closed.

        Write the keywords from control parametres and
        the NAMD output from the parsed log output,
        which belong to settings_run.
        Variables are reset to ensure clean start for new run.
        """
        frameSequenceGIndex = backend.openSection("section_frame_sequence")
        section_frameseq_Dict = get_updateDictionary(self, 'frameseqend')
        updateFrameDict = {
                'startSection' : [
                    ['section_frame_sequence']],
                #'muteSections' : [['section_sampling_method']],
                'dictionary' : section_frameseq_Dict
                }
        self.metaStorage.update(updateFrameDict)
        self.metaStorage.updateBackend(backend.superBackend,
                startsection=['section_frame_sequence'],
                autoopenclose=False)
        backend.addValue("frame_sequence_to_sampling_ref", self.secSamplingGIndex)
        backend.addArrayValues("frame_sequence_local_frames_ref", np.asarray(self.singleConfCalcs))
        backend.closeSection("section_frame_sequence", frameSequenceGIndex)

        # reset all variables
        self.initialize_values()

    def onClose_x_namd_section_input_output_files(self, backend, gIndex, section):
        """Trigger called when x_namd_section_input_output_files is closed.

        Determine whether topology, trajectory and input coordinate files are
        supplied to the parser

        Initiates topology and trajectory file handles.

        Captures topology, atomic positions, atom labels, lattice vectors and
        stores them before section_system and
        section_single_configuration_calculation are encountered.
        """
        # Checking whether topology, input
        # coordinates and trajectory files exist
        atLeastOneFileExist = False
        working_dir_name = os.path.dirname(os.path.abspath(self.fName))
        for k,v in self.fileDict.items():
            if k.startswith(PARSERTAG + '_inout_file'):
                if v.value:
                    file_name = os.path.normpath(os.path.join(working_dir_name, v.value))
                    self.fileDict[k].fileSupplied = os.path.isfile(file_name)
                    self.fileDict[k].activeInfo = False
                    if self.fileDict[k].fileSupplied:
                        self.fileDict[k].fileName = file_name
                        self.fileDict[k].activeInfo = True
                        if self.fileDict[k].activeInfo:
                            atLeastOneFileExist = True
                    else:
                        self.fileDict[k].value = None
        updateDict = {
            'startSection'   : [[PARSERTAG+'_section_input_output_files']],
            'dictionary'     : self.fileDict
            }
        self.metaStorage.update(updateDict)
        self.metaStorage.updateBackend(backend.superBackend,
                startsection=[PARSERTAG+'_section_input_output_files'],
                autoopenclose=False)
        if atLeastOneFileExist:
            self.MDData.initializeFileHandlers(self)
            if self.topology:
                self.topoDict = self.topology.topoDict
            if self.trajectory:
                self.atompositions = self.trajectory.positions()
            if self.inputcoords:
                self.inputpositions = self.inputcoords.positions()
            if self.outputcoords:
                self.outputpositions = self.outputcoords.positions()
        #self.MDiter += self.MDstep
        self.MDiter += 1
        self.MDcurrentstep = int(self.MDiter)
        self.stepcontrolDict.update({"MDcurrentstep" : int(self.MDcurrentstep)})
            #pass

    def onOpen_x_namd_section_control_parameters(self, backend, gIndex, section):
        # keep track of the latest section
        if self.inputControlIndex is None:
            self.inputControlIndex = gIndex

    def onClose_x_namd_section_control_parameters(self, backend, gIndex, section):
        section_control_Dict = {}
        section_control_Dict.update(self.cntrlDict)
        updateDict = {
            'startSection' : [[PARSERTAG+'_section_control_parameters']],
            'dictionary'   : section_control_Dict
            }
        self.metaStorage.update(updateDict)
        self.metaStorage.updateBackend(backend.superBackend,
                startsection=[PARSERTAG+'_section_control_parameters'],
                autoopenclose=False)
        nparms = 0
        nparmKey = isMetaStrInDict("PARAMETERS",self.cntrlDict)
        if nparmKey is not None:
            if self.cntrlDict[nparmKey].activeInfo:
                nparms = np.array(self.cntrlDict[nparmKey].value).shape[0]
        if nparms>0:
            backend.superBackend.addValue(PARSERTAG+"_inout_control_number_of_parameters", int(nparms))
        # NAMD prints the initial and final energies to the log file.
        # The total number of MD steps in NAMD is nsteps irrelevant
        # to the number of steps in log file of energy file (.edr)
        nsteps = 0
        nlogsteps = 0
        nstructstep = 0
        ninputstep = 0
        noutputstep = 0
        nbinsteps = 0
        ntrajsteps = 0
        nvelsteps = 0
        nforcesteps = 0
        nstructKey = isMetaStrInDict("STRUCTURE FILE",self.cntrlDict)
        ninputKey = isMetaStrInDict("COORDINATE PDB",self.cntrlDict)
        noutputKey = isMetaStrInDict("OUTPUT FILENAME",self.cntrlDict)
        nstepKey = isMetaStrInDict("NUMBER OF STEPS", self.cntrlDict)
        nlogKey = isMetaStrInDict("ENERGY OUTPUT STEPS", self.cntrlDict)
        nxoutKey = isMetaStrInDict("DCD FREQUENCY", self.cntrlDict)
        nvoutKey = isMetaStrInDict("VELOCITY DCD FREQUENCY", self.cntrlDict)
        nfoutKey = isMetaStrInDict("FORCE DCD FREQUENCY", self.cntrlDict)
        nbinoutKey = isMetaStrInDict("BINARY OUTPUT", self.cntrlDict)
        if nstepKey is not None:
            if self.cntrlDict[nstepKey].activeInfo:
                nsteps = conv_int(self.cntrlDict[nstepKey].value, default=0)
            else:
                nsteps = conv_int(self.cntrlDict[nstepKey].defaultValue, default=0)
        if nlogKey is not None:
            if self.cntrlDict[nlogKey].activeInfo:
                nlogsteps = conv_int(self.cntrlDict[nlogKey].value, default=1)
            else:
                nlogsteps = conv_int(self.cntrlDict[nlogKey].defaultValue, default=1)
        if nbinoutKey is not None:
            if self.cntrlDict[nbinoutKey].activeInfo:
                binsteps = [nsteps] if self.cntrlDict[
                        nbinoutKey].value == "FILES WILL BE USED" else []
            else:
                binsteps = []
        else:
            binsteps = []
        if nxoutKey is not None:
            if self.cntrlDict[nxoutKey].activeInfo:
                ntrajsteps = conv_int(self.cntrlDict[nxoutKey].value, default=0)
        if nstructKey is not None:
            if self.cntrlDict[nstructKey].activeInfo:
                nstructstep = 1
        if ninputKey is not None:
            if self.cntrlDict[ninputKey].activeInfo:
                ninputstep = 1
        if noutputKey is not None:
            if self.cntrlDict[noutputKey].activeInfo:
                noutputstep = 1
        if nvoutKey is not None:
            if self.cntrlDict[nvoutKey].activeInfo:
                nvelsteps = conv_int(self.cntrlDict[nvoutKey].value, default=0)
        if nfoutKey is not None:
            if self.cntrlDict[nfoutKey].activeInfo:
                nforcesteps = conv_int(self.cntrlDict[nfoutKey].value, default=0)

        if nlogsteps>0:
            logsteps = [i for i in range(0, nsteps, nlogsteps)]
            logsteps.append(nsteps)
        else:
            logsteps = [i for i in range(0, nsteps)]
            logsteps.append(nsteps)
        if ntrajsteps>0:
            trajsteps = [i for i in range(0, nsteps, ntrajsteps)]
            trajsteps.append(nsteps)
        else:
            trajsteps = []
            if(ninputstep>0 or nstructstep>0):
                trajsteps.append(0)
            if noutputstep>0:
                trajsteps.append(nsteps)
        if nvelsteps>0:
            velsteps = [i for i in range(0, nsteps, nvelsteps)]
            velsteps.append(nsteps)
        else:
            velsteps = []
            #velsteps.append(nsteps)
        if nforcesteps>0:
            forcesteps = [i for i in range(0, nsteps, nforcesteps)]
            forcesteps.append(nsteps)
        else:
            forcesteps = []
            #forcesteps.append(nsteps)
        self.stepcontrolDict.update({"logsteps"     : logsteps})
        self.stepcontrolDict.update({"nextlogsteps" : logsteps})
        self.stepcontrolDict.update({"trajsteps"    : trajsteps})
        self.stepcontrolDict.update({"velsteps"     : velsteps})
        self.stepcontrolDict.update({"forcesteps"   : forcesteps})
        self.stepcontrolDict.update({"binsteps"     : binsteps})
        steps = []
        for step in range(0,nsteps+1):
            if(step in logsteps or
               step in trajsteps or
               step in velsteps or
               step in forcesteps):
               steps.append(step)
        #steps = logsteps if len(logsteps)>len(trajsteps) else trajsteps
        #followsteps = "log" if len(logsteps)>len(trajsteps) else "traj"
        #steps = steps if len(steps)>len(velsteps) else velsteps
        #followsteps = followsteps if len(steps)>len(velsteps) else "vel"
        #self.stepcontrolDict.update({"steps"  : steps if len(steps)>len(forcesteps) else forcesteps})
        #self.stepcontrolDict.update({"follow" : followsteps if len(steps)>len(enersteps) else "force"})
        self.stepcontrolDict.update({"steps"  : steps})
        #self.stepcontrolDict.update({"follow" : followsteps})

    def onOpen_section_method(self, backend, gIndex, section):
        # keep track of the latest method section
        self.secMethodGIndex = gIndex
        if self.inputMethodIndex is None:
            self.inputMethodIndex = gIndex
        else:
            backend.openNonOverlappingSection("section_method_to_method_refs")
            backend.addValue("method_to_method_kind", "core_settings")
            backend.addValue("method_to_method_ref", self.inputMethodIndex)
            backend.closeNonOverlappingSection("section_method_to_method_refs")
        if self.mainMethodIndex is None:
            self.mainMethodIndex = gIndex

    def onClose_section_method(self, backend, gIndex, section):
        """Trigger called when section_method is closed.
        """
        # input method
        pass

    def onOpen_section_sampling_method(self, backend, gIndex, section):
        # keep track of the latest sampling description section
        self.secSamplingGIndex = gIndex
        #self.inputControlIndex = backend.superBackend.openSection(PARSERTAG + '_section_control_parameters')

    def onClose_section_sampling_method(self, backend, gIndex, section):
        """Trigger called when section_sampling_method is closed.

        Writes sampling method details for minimization and molecular dynamics.
        """
        # check control keywords were found throguh dictionary support
        #backend.superBackend.closeSection(PARSERTAG + '_section_control_parameters', self.inputControlIndex)
        section_sampling_Dict = get_updateDictionary(self, 'sampling')
        updateDict = {
            #'startSection' : [['section_sampling_method']],
            'startSection' : [['section_run']],
            'dictionary' : section_sampling_Dict
            }
        self.metaStorage.update(updateDict)
        self.metaStorage.updateBackend(backend.superBackend,
                startsection=['section_run'],
                #startsection=['section_sampling_method'],
                autoopenclose=False)

    def onOpen_section_topology(self, backend, gIndex, section):
        # keep track of the latest topology description section
        if (gIndex is None or gIndex == -1 or gIndex == "-1"):
            self.secTopologyGIndex = backend.superBackend.openSection("section_topology")
        else:
            self.secTopologyGIndex = gIndex

    def onClose_section_topology(self, backend, gIndex, section):
        """Trigger called when section_topology is closed.
        """
        section_topology_Dict = get_updateDictionary(self, 'topology')
        updateDict = {
            'startSection' : [
                ['section_topology']],
            #'muteSections' : [['section_sampling_method']],
            'dictionary' : section_topology_Dict
            }
        self.metaStorage.update(updateDict)
        self.metaStorage.updateBackend(backend.superBackend,
                startsection=['section_topology'],
                autoopenclose=False)
        self.topology_atom_type_and_interactions(backend, gIndex)

        if (gIndex is None or gIndex == -1 or gIndex == "-1"):
            backend.superBackend.closeSection("section_topology", self.secTopologyGIndex)

    def onOpen_section_system(self, backend, gIndex, section):
        # keep track of the latest system description section
        if (gIndex is None or gIndex == -1 or gIndex == "-1"):
            self.secSystemGIndex = backend.superBackend.openSection("section_system")
        else:
            self.secSystemGIndex = gIndex

    def onClose_section_system(self, backend, gIndex, section):
        """Trigger called when section_system is closed.

        Writes atomic positions, atom labels and lattice vectors.
        """
        # Our special recipe for the confused backend and more
        # See our other recipes at the back of this parser: MetaInfoStorage! :)
        if (gIndex is None or gIndex == -1 or gIndex == "-1"):
            SloppyBackend = backend.superBackend
        else:
            SloppyBackend = backend

        numatoms = None

        # NAMD default unit vectors. If all are zeros than the simulation cell is not periodic.
        unit_vectors = np.asarray(
                [[0.0,0.0,0.0],
                 [0.0,0.0,0.0],
                 [0.0,0.0,0.0]]
                )
        vaKey = isMetaStrInDict("PERIODIC CELL BASIS 1",self.cntrlDict)
        vbKey = isMetaStrInDict("PERIODIC CELL BASIS 2",self.cntrlDict)
        vcKey = isMetaStrInDict("PERIODIC CELL BASIS 3",self.cntrlDict)
        if vaKey is not None:
            if self.cntrlDict[vaKey].value is not None:
                unit_vectors[:,0]=np.asarray([ float(i) for i in self.cntrlDict[vaKey].value.split()])
        if vbKey is not None:
            if self.cntrlDict[vbKey].value is not None:
                unit_vectors[:,1]=np.asarray([ float(i) for i in self.cntrlDict[vbKey].value.split()])
        if vcKey is not None:
            if self.cntrlDict[vcKey].value is not None:
                unit_vectors[:,2]=np.asarray([ float(i) for i in self.cntrlDict[vcKey].value.split()])
        if self.trajectory is not None:
            if self.trajectory.unitcell_vectors is None:
                self.trajectory.unitcell_vectors = unit_vectors

        if self.topology:
            if (self.secTopologyGIndex is None or
                (self.secTopologyGIndex == -1 or
                self.secTopologyGIndex == "-1")):
                self.onOpen_section_topology(backend, None, None)
                self.onClose_section_topology(backend, None, None)
            SloppyBackend.addValue("topology_ref", self.secTopologyGIndex)

        coordinates=None
        steps = self.stepcontrolDict["steps"]
        if self.trajectory is not None:
            coordinates=self.trajectory
            positions=self.atompositions
        elif(self.inputcoords is not None and
             self.MDcurrentstep == steps[0]):
            coordinates=self.inputcoords
            positions=self.inputpositions
        elif(self.outputcoords is not None and
             self.MDcurrentstep == steps[-1]):
            coordinates=self.outputcoords
            positions=self.outputpositions

        if(coordinates is not None and positions is not None):
            self.trajRefSingleConfigurationCalculation = gIndex
            if coordinates.unitcell_vectors is not None:
                unit_cell = np.asarray(self.metaStorage.convertUnits(
                    coordinates.unitcell_vectors, "Angstrom", self.unitDict))
                SloppyBackend.addArrayValues('simulation_cell', unit_cell)
                SloppyBackend.addArrayValues('lattice_vectors', unit_cell)
            if coordinates.unitcell_lengths is not None:
                SloppyBackend.addArrayValues(PARSERTAG + '_lattice_lengths', coordinates.unitcell_lengths)
            if coordinates.unitcell_angles is not None:
                SloppyBackend.addArrayValues(PARSERTAG + '_lattice_angles', coordinates.unitcell_angles)
            # NAMD Guide says: (See http://www.ks.uiuc.edu/Research/namd/2.12/ug/node11.html)
            # Positions in PDB/NAMD binary/DCD files are stored in A.
            #pos_obj = getattr(self.trajectory, 'positions', None)
            #if callable(pos_obj):
            if(isinstance(positions, np.ndarray) or isinstance(positions, (tuple, list))):
                SloppyBackend.addArrayValues('atom_positions', np.transpose(np.asarray(
                    self.metaStorage.convertUnits(positions, "Angstrom", self.unitDict))))
            if coordinates.velocities is not None:
                # Velocities in PDB files are stored in A/ps units.(PDB files are read for input
                #     coordinates, velocities, and forces)
                # Velocities in NAMD binary/DCD files are stored in NAMD internal units and must be multiplied
                #     by PDBVELFACTOR=20.45482706 to convert to A/ps. (These files are used for output trajectory)
                SloppyBackend.addArrayValues('atom_velocities', np.transpose(np.asarray(
                    self.metaStorage.convertUnits(
                        coordinates.velocities, "20.45482706*Angstrom/(pico-second)", self.unitDict))))
                # need to transpose array since its shape is [number_of_atoms,3] in the metadata

            if self.topology is not None:
                atom_labels = self.topoDict["atom_element_list"]
                numatoms = len(atom_labels)
                SloppyBackend.addArrayValues('atom_labels', np.asarray(atom_labels))
                pass
        else:
            if unit_vectors is not None:
                unit_cell = np.asarray(self.metaStorage.convertUnits(
                    unit_vectors, "Angstrom", self.unitDict))
                SloppyBackend.addArrayValues('simulation_cell', unit_cell)
                SloppyBackend.addArrayValues('lattice_vectors', unit_cell)

        if self.trajectory is not None:
            # Read the next step at trajectory in advance
            # If iread returns None, it will be the last step
            try:
                self.atompositions = self.trajectory.positions()
                if self.atompositions is not None:
                    numatoms = len(self.atompositions)
                #self.MDiter += self.MDstep
                #self.MDiter += 1
            except AttributeError:
                self.atompositions = None
                pass

        if unit_vectors is not None:
            unit_periodicity=np.asarray([False,False,False])
            if np.linalg.norm(unit_vectors[0])>0.0:
                unit_periodicity[0]=True
            if np.linalg.norm(unit_vectors[1])>0.0:
                unit_periodicity[1]=True
            if np.linalg.norm(unit_vectors[2])>0.0:
                unit_periodicity[2]=True
            SloppyBackend.addArrayValues('configuration_periodic_dimensions', unit_periodicity)

        if numatoms:
            SloppyBackend.addValue("number_of_atoms", numatoms)

        if (gIndex is None or gIndex == -1 or gIndex == "-1"):
            SloppyBackend.closeSection("section_system", self.secSystemGIndex)

    def onOpen_section_single_configuration_calculation(self, backend, gIndex, section):
        # write the references to section_method and section_system
        self.singleConfCalcs.append(gIndex)
        self.secSingleGIndex = backend.superBackend.openSection("section_single_configuration_calculation")

    def onClose_section_single_configuration_calculation(self, backend, gIndex, section):
        """Trigger called when section_single_configuration_calculation is closed.

        Write number of steps in MD or Minimization.
        Check for convergence of geometry optimization.
        Write energy values at MD and with error in Minimization.
        Write reference to section_method and section_system
        """

        self.lastCalculationGIndex = gIndex
        steps = self.stepcontrolDict["steps"]
        logsteps = self.stepcontrolDict["logsteps"]
        velsteps = self.stepcontrolDict["velsteps"]
        forcesteps = self.stepcontrolDict["forcesteps"]
        trajsteps = self.stepcontrolDict["trajsteps"]
        #print("PRINTING steps:",steps)
        #print("PRINTING logsteps:",logsteps)
        #print("PRINTING velsteps:",velsteps)
        #print("PRINTING forcesteps:",forcesteps)
        #print("PRINTING trajsteps:",trajsteps)
        #if len(steps)>1:
        #    self.MDstep = steps[1]-steps[0]
        #if self.MDiter<len(steps):
        #    self.MDcurrentstep = steps[self.MDiter]
        #else:
        #    self.MDcurrentstep += 1
        #if self.MDiter+1<len(steps):
        #    self.MDnextstep = steps[self.MDiter+1]
        #    self.stepcontrolDict.update({"nextlogsteps":logsteps[self.MDiter+1:]})
        #else:
        #    self.MDnextstep = steps[-1] + 1
        #self.stepcontrolDict.update({"MDcurrentstep" : self.MDcurrentstep})

        if self.MDcurrentstep in logsteps:
            section_frameseq_Dict = get_updateDictionary(self, 'frameseq')
            updateFrameDict = {
                'startSection' : [
                    ['section_frame_sequence']],
                #'muteSections' : [['section_sampling_method']],
                'dictionary' : section_frameseq_Dict
                }
            self.metaStorage.update(updateFrameDict)
            section_singlevdw_Dict = get_updateDictionary(self, 'singlevdw')
            updateDictVDW = {
                'startSection' : [
                    ['section_energy_van_der_Waals']],
                #'muteSections' : [['section_sampling_method']],
                'dictionary' : section_singlevdw_Dict
                }
            self.secVDWGIndex = backend.superBackend.openSection("section_energy_van_der_Waals")
            self.metaStorage.update(updateDictVDW)
            self.metaStorage.updateBackend(backend.superBackend,
                    startsection=['section_energy_van_der_Waals'],
                    autoopenclose=False)
            backend.superBackend.closeSection("section_energy_van_der_Waals", self.secVDWGIndex)
            section_singlecalc_Dict = get_updateDictionary(self, 'singleconfcalc')
            updateDict = {
                'startSection' : [
                    ['section_single_configuration_calculation']],
                #'muteSections' : [['section_sampling_method']],
                'dictionary' : section_singlecalc_Dict
                }
            self.metaStorage.update(updateDict)
            self.metaStorage.updateBackend(backend.superBackend,
                    startsection=['section_single_configuration_calculation'],
                    autoopenclose=False)
        if self.MDcurrentstep in forcesteps:
            pos_obj = getattr(self.trajectory, 'positions', None)
            #if callable(pos_obj):
            if self.trajectory.forces is not None:
                # Forces in PDB/NAMD binary/DCD files are stored in kcal/mol/A
                SloppyBackend.addArrayValues('atom_forces', np.transpose(np.asarray(
                    self.metaStorage.convertUnits(
                        self.atompositions.velocities, "kcal/(mol*Angstrom)", self.unitDict))))
                # need to transpose array since its shape is [number_of_atoms,3] in the metadata

        if(self.MDcurrentstep in trajsteps or
           self.MDcurrentstep in velsteps):
            #print("PRINTING traj steps:",self.MDcurrentstep,trajsteps)
            self.onOpen_section_system(backend, None, None)
            self.onClose_section_system(backend, None, None)
            backend.addValue('single_configuration_calculation_to_system_ref', self.secSystemGIndex)
            self.MDiter += 1
        else:
            if(self.MDcurrentstep in logsteps or
               self.MDcurrentstep in forcesteps):
                self.MDiter += 1
            #if((self.MDcurrentstep in logsteps and
            #    self.MDiter+1 in steps) or
            #    (self.MDcurrentstep in forcesteps and
            #    self.MDiter+1 in steps)):
            #    self.MDiter += 1
        #if self.MDiter<len(steps):
        #    self.MDcurrentstep = steps[self.MDiter]
        #else:
        #    self.MDcurrentstep += 1
        if self.MDiter+1<len(steps):
            self.MDnextstep = int(steps[self.MDiter])
            self.stepcontrolDict.update({"nextlogsteps":logsteps[self.MDiter:]})
        else:
            self.MDnextstep = int(steps[-1] + 1)
        self.stepcontrolDict.update({"MDcurrentstep" : int(self.MDcurrentstep)})
        #print("PRINTING section single MDiter:",self.MDiter)
        backend.superBackend.closeSection("section_single_configuration_calculation", self.secSingleGIndex)

    def setStartingPointCalculation(self, parser):
        backend = parser.backend
        backend.openSection('section_calculation_to_calculation_refs')
        if self.lastCalculationGIndex:
            backend.addValue('calculation_to_calculation_ref', self.lastCalculationGIndex)
            backend.closeSection('section_calculation_to_calculation_refs')
        return None

    def fileNameTrans(self, fname, value):
        fileNameTrans = {
                "output_coord" : ".coor",
                "output_vel"   : ".vel",
                "output_xsc"   : ".xsc",
                }
        for k,v in fileNameTrans.items():
            if fname in k:
                return value+v
        return value

    def mdInfoTrans(self, fname, value):
        mdInfoDict = {
                "minimization" : [],
                "thermostat"   : [],
                "barostat"     : []
                }
        cgmin = isMetaStrInDict("MINIMIZATION",self.cntrlDict)
        quench = isMetaStrInDict("VELOCITY QUENCHING",self.cntrlDict)
        tcouple = isMetaStrInDict("TEMPERATURE COUPLING",self.cntrlDict)
        trescale = isMetaStrInDict("VELOCITY RESCALE FREQ",self.cntrlDict)
        treassign = isMetaStrInDict("VELOCITY REASSIGNMENT FREQ",self.cntrlDict)
        tandersen = isMetaStrInDict("LOWE-ANDERSEN DYNAMICS",self.cntrlDict)
        tlangevin = isMetaStrInDict("LANGEVIN DYNAMICS",self.cntrlDict)
        pberendsen = isMetaStrInDict("BERENDSEN PRESSURE COUPLING",self.cntrlDict)
        plangevin = isMetaStrInDict("LANGEVIN PISTON PRESSURE CONTROL",self.cntrlDict)
        mini = None
        thermo = None
        baro = None
        if cgmin is not None:
            if self.cntrlDict[cgmin].value is not None:
                mini = 'cg'
        if quench is not None:
            if self.cntrlDict[quench].value is not None:
                mini = 'quench'
        if tcouple is not None:
            if self.cntrlDict[tcouple].value is not None:
                thermo = 'tcouple'
        if trescale is not None:
            if self.cntrlDict[trescale].value is not None:
                thermo = 'rescale'
        if treassign is not None:
            if self.cntrlDict[treassign].value is not None:
                thermo = 'reassign'
        if tandersen is not None:
            if self.cntrlDict[tandersen].value is not None:
                thermo = 'andersen'
        if tlangevin is not None:
            if self.cntrlDict[tlangevin].value is not None:
                thermo = 'langevin'
        if pberendsen is not None:
            if self.cntrlDict[pberendsen].value is not None:
                baro = 'berendsen'
        if plangevin is not None:
            if self.cntrlDict[plangevin].value is not None:
                baro = 'langevin'
        for k,v in mdInfoDict.items():
            if fname in k:
                if 'thermostat' in fname:
                    return thermo
                elif 'barostat' in fname:
                    return baro
                elif 'minimization' in fname:
                    return mini
                else:
                    return value
        return value

    def convertInt(self, fname, value):
        keyMapper = {
                "TS" : "MDcurrentstep",
                "DCDSTEP" : "MDcurrentstep",
                "VELSTEP" : "MDcurrentstep",
                "FORCESTEP" : "MDcurrentstep"
                }
        if value is not None:
            for k,v in keyMapper.items():
                if fname in k:
                    return int(value)
        return value

    def updateTime(self, fname, value):
        keyMapper = {
                "TIME" : "MDcurrentstep",
                }
        timestep = 1.0
        istimestep = isMetaStrInDict("TIMESTEP",self.cntrlDict)
        if istimestep is not None:
            if self.cntrlDict[istimestep].value is not None:
                timestep = float(self.cntrlDict[istimestep].value)
        if value is not None:
            for k,v in keyMapper.items():
                if fname in k:
                    return float(value)*timestep
        return value

    def build_subMatchers(self):
        """Builds the sub matchers to parse the main output file.
        """
        mddataNameList=getList_MetaStrInDict(self.mddataDict)

        mdoutSubParsers = [
            # timestep header Parser
            { "startReStr"        : r"\s*ETITLE:\s*",
              "parser"            : "table_parser",
              "parsername"        : "header_parser",
              "waitlist"          : None,
              "stopOnMatchStr"    : r"(?:^\s*$|\s*ENERGY:\s*)",
              "quitOnMatchStr"    : r"^====================================================",
              "metaNameStart"     : PARSERTAG + "_mdout_",
              "matchNameList"     : mddataNameList,
              "matchNameDict"     : "mddataDict",
              "updateMatchDict"   : True,
              "onlyCaseSensitive" : True,
              "stopOnFirstLine"   : False,
              "parserOptions"     : {
                  "header"           : True,
                  "headersave"       : "mdoutHeaderDict",
                  "wrap"             : False,
                  "tablelines"       : 0,
                  "tablestartsat"    : r"\s*ETITLE:\s*",
                  "tableendsat"      : r"^\s*$",
                  "lineFilter"       : None,
                  "movetostopline"   : False,
                  "parsercntrlattr"  : "MDcurrentstep",
                  "parsercntrlin"    : "logsteps",
                  "lookupdict"       : "stepcontrolDict"
                  }
              },
            # timestep energy outputs Parser
            { "startReStr"        : r"\s*ENERGY:\s*",
              "parser"            : "table_parser",
              "parsername"        : "log_step_parser",
              "waitlist"          : None,
              "stopOnMatchStr"    : r"(?:^\s*$|\s*ENERGY:\s*)",
              "quitOnMatchStr"    : r"^====================================================",
              "metaNameStart"     : PARSERTAG + "_mdout_",
              "matchNameList"     : mddataNameList,
              "matchNameDict"     : "mddataDict",
              "updateMatchDict"   : True,
              "onlyCaseSensitive" : True,
              "stopOnFirstLine"   : False,
              "parserOptions"     : {
                  "header"           : False,
                  "headerList"       : "mdoutHeaderDict",
                  "wrap"             : False,
                  "tablelines"       : 0,
                  "tablestartsat"    : r"\s*ENERGY:\s*",
                  "tableendsat"      : r"^\s*$",
                  "lineFilter"       : None,
                  "movetostopline"   : False,
                  "parsercntrlattr"  : "MDcurrentstep",
                  "parsercntrlin"    : "logsteps",
                  "lookupdict"       : "stepcontrolDict"
                  }
              },
            # trajectory Parser
            { "startReStr"        : r"\s*WRITING\s*COORDINATES\s*TO\s*DCD\s*FILE\s*",
              "parser"            : "namelist_parser",
              "parsername"        : "dcd_parser",
              "stopOnMatchStr"    : r"\s*(?:ENERGY|TIMING|FINISHED|OPENING|The last)\s*",
              "quitOnMatchStr"    : r"\s*(?:ENERGY|TIMING|FINISHED|OPENING|The last)\s*",
              "metaNameStart"     : PARSERTAG + "_mdout_",
              "matchNameList"     : mddataNameList,
              "matchNameDict"     : "mddataDict",
              "updateMatchDict"   : False,
              "onlyCaseSensitive" : True,
              "stopOnFirstLine"   : True,
              "parserOptions"     : {
                  "controlsections"  : ["section_single_configuration_calculation"],
                  "controlsave"      : "sectioncontrol",
                  "controldict"      : "stepcontrolDict",
                  }
              },
            # velocities Parser
            { "startReStr"        : r"\s*WRITING\s*VELOCITIES\s*TO\s*DCD\s*FILE\s*",
              "parser"            : "namelist_parser",
              "parsername"        : "veldcd_parser",
              "stopOnMatchStr"    : r"\s*(?:ENERGY|TIMING|FINISHED|OPENING|The last)\s*",
              "quitOnMatchStr"    : r"\s*(?:ENERGY|TIMING|FINISHED|OPENING|The last)\s*",
              "metaNameStart"     : PARSERTAG + "_mdout_",
              "matchNameList"     : mddataNameList,
              "matchNameDict"     : "mddataDict",
              "updateMatchDict"   : False,
              "onlyCaseSensitive" : True,
              "stopOnFirstLine"   : True,
              "parserOptions"     : {
                  "controlsections"  : ["section_single_configuration_calculation"],
                  "controlsave"      : "sectioncontrol",
                  "controldict"      : "stepcontrolDict",
                  }
              },
            # forces Parser
            { "startReStr"        : r"\s*WRITING\s*FORCES\s*TO\s*DCD\s*FILE\s*",
              "parser"            : "namelist_parser",
              "parsername"        : "forcedcd_parser",
              "stopOnMatchStr"    : r"\s*(?:ENERGY|TIMING|FINISHED|OPENING|The last)\s*",
              "quitOnMatchStr"    : r"\s*(?:ENERGY|TIMING|FINISHED|OPENING|The last)\s*",
              "metaNameStart"     : PARSERTAG + "_mdout_",
              "matchNameList"     : mddataNameList,
              "matchNameDict"     : "mddataDict",
              "updateMatchDict"   : False,
              "onlyCaseSensitive" : True,
              "stopOnFirstLine"   : True,
              "parserOptions"     : {
                  "controlsections"  : ["section_single_configuration_calculation"],
                  "controlsave"      : "sectioncontrol",
                  "controldict"      : "stepcontrolDict",
                  }
              },
            # thermostat save Parser
            { "startReStr"        : "AlwaysRun",
              "parser"            : "dictionary_parser",
              "parsername"        : "frameseq_step_parser",
              "waitlist"          : None,
              "stopOnMatchStr"    : "AlwaysStop",
              "quitOnMatchStr"    : "AlwaysStop",
              "metaNameStart"     : PARSERTAG + "_mdout_",
              "matchNameList"     : mddataNameList,
              "matchNameDict"     : "mddataDict",
              "updateMatchDict"   : True,
              "onlyCaseSensitive" : True,
              "stopOnFirstLine"   : True,
              "parserOptions"     : {
                  "dictionary"       : "stepcontrolDict",
                  "dicttype"         : "standard", # (standard or smartparser)
                  "readwritedict"    : "write",
                  "keyMapper"        : {"TS" : "MDcurrentstep",
                                        "DCDSTEP" : "MDcurrentstep",
                                        "VELSTEP" : "MDcurrentstep",
                                        "FORCESTEP" : "MDcurrentstep"},
                  "updatefunc"       : "max",
                  "updateattrs"      : ["MDcurrentstep"],
                  "controlsections"  : ["section_single_configuration_calculation"],
                  "controlsave"      : "sectioncontrol",
                  "controldict"      : "stepcontrolDict",
                  "controlattrs"     : ["MDcurrentstep"],
                  "preprocess"       : self.convertInt,
                  "postprocess"      : self.convertInt,
                  #"parsercntrlattr"  : "MDcurrentstep",
                  #"parsercntrlin"    : "steps",
                  #"lookupdict"       : "stepcontrolDict"
                  }
              },
            # time save Parser
            { "startReStr"        : "AlwaysRun",
              "parser"            : "dictionary_parser",
              "parsername"        : "frameseq_step_parser",
              "waitlist"          : None,
              "stopOnMatchStr"    : "AlwaysStop",
              "quitOnMatchStr"    : "AlwaysStop",
              "metaNameStart"     : PARSERTAG + "_mdout_",
              "matchNameList"     : mddataNameList,
              "matchNameDict"     : "mddataDict",
              "updateMatchDict"   : True,
              "onlyCaseSensitive" : True,
              "stopOnFirstLine"   : True,
              "parserOptions"     : {
                  "dictionary"       : "mddataDict",
                  "dicttype"         : "smartparser", # (standard or smartparser)
                  "readwritedict"    : "read",
                  "keyMapper"        : {"TIME" : "TS"},
                  "preprocess"       : self.convertInt,
                  "postprocess"      : self.updateTime,
                  }
              },
            # Section Control Parser
            { "startReStr"        : "AlwaysRun",
              "parser"            : "section_control_parser",
              "parsername"        : "section_parser",
              "waitlist"          : [["log_step_parser"],
                                     ["forcedcd_parser"],
                                     ["veldcd_parser"],
                                     ["dcd_parser"]],
              "stopOnMatchStr"    : r"\s*ENERGY:\s*",
              "quitOnMatchStr"    : r"\s*ENERGY:\s*",
              "metaNameStart"     : None,
              "matchNameList"     : None,
              "matchNameDict"     : None,
              "updateMatchDict"   : False,
              "onlyCaseSensitive" : True,
              "stopOnFirstLine"   : True,
              "parserOptions"     : {
                  "sectionname"      : "section_single_configuration_calculation",
                  "sectionopen"      : True,
                  "sectionopenattr"  : "MDcurrentstep",
                  "sectionopenin"    : "steps",
                  "sectionclose"     : True,
                  "sectioncloseattr" : "MDcurrentstep",
                  "sectionclosein"   : "steps",
                  "activatesection"  : "sectioncontrol",
                  "lookupdict"       : "stepcontrolDict"
                  }
              },
            # Step Control Parser
            { "startReStr"        : "AlwaysRun",
              "parser"            : "readline_control_parser",
              "parsername"        : "readline_parser",
              "waitlist"          : None,
              "stopOnMatchStr"    : "AlwaysStop",
              "quitOnMatchStr"    : "AlwaysStop",
              "metaNameStart"     : None,
              "matchNameList"     : None,
              "matchNameDict"     : None,
              "updateMatchDict"   : False,
              "onlyCaseSensitive" : True,
              "stopOnFirstLine"   : True,
              "parserOptions"     : {
                  "waitatlineStr"    : r"\s*ENERGY:\s*",
                  "controlwait"      : None,
                  #"controlwait"      : "nextlogsteps",
                  "controlattr"      : "MDcurrentstep",
                  "controlnextattr"  : "MDnextstep",
                  "controllast"      : -1,
                  "controlskip"      : [],
                  "controlin"        : "steps",
                  "controlcounter"   : "targetstep",
                  "controldict"      : "stepcontrolDict",
                  "lookupdict"       : "stepcontrolDict"
                  }
              }
            ]

        cntrlNameList=getList_MetaStrInDict(self.metaDicts['cntrl'])
        fileNameList=getList_MetaStrInDict(self.metaDicts['file'])
        extraNameList=getList_MetaStrInDict(self.metaDicts['extra'])

        mdinoutSubParsers = [
            # cntrl Parser
            { "startReStr"        : r"\s*Info:\s*SIMULATION\s*PARAMETERS:\s*",
              "parser"            : "namelist_parser",
              "parsername"        : "cntrl_parser",
              "stopOnMatchStr"    : r"\s*Info:\s*(?:SUMMARY\s*OF\s*PARAMETERS:|"
                                     "STRUCTURE\s*SUMMARY:)",
              "quitOnMatchStr"    : None,
              "metaNameStart"     : PARSERTAG + "_inout_control_",
              "matchNameList"     : cntrlNameList,
              "matchNameDict"     : "cntrlDict",
              "updateMatchDict"   : True,
              "onlyCaseSensitive" : True,
              "stopOnFirstLine"   : False,
              "parserOptions"     : { "lineFilter" : None }
              },
            # simplify md info Parser
            { "startReStr"        : r"\s*Info:\s*(?:SUMMARY\s*OF\s*PARAMETERS:|"
                                     "STRUCTURE\s*SUMMARY:)",
              "parser"            : "dictionary_parser",
              "parsername"        : "info_add_parser",
              "quitOnMatchStr"    : None,
              "stopOnMatchStr"    : "AlwaysStop",
              "quitOnMatchStr"    : "AlwaysStop",
              "metaNameStart"     : PARSERTAG + "_mdin_method_",
              "matchNameList"     : extraNameList,
              "matchNameDict"     : "extraDict",
              "updateMatchDict"   : True,
              "onlyCaseSensitive" : True,
              "stopOnFirstLine"   : True,
              "parserOptions"     : {
                  "dictionary"       : "cntrlDict",
                  "dicttype"         : "smartparser", # (standard or smartparser)
                  "readwritedict"    : "read",
                  "keyMapper"        : {
                      "minimization" : "MINIMIZATION",
                      "minimization" : "VELOCITY QUENCHING",
                      "integrator"   : "VERLET INTEGRATOR",
                      "thermostat"   : "TEMPERATURE COUPLING",
                      "thermostat"   : "VELOCITY RESCALE FREQ",
                      "thermostat"   : "VELOCITY REASSIGNMENT FREQ",
                      "thermostat"   : "LOWE-ANDERSEN DYNAMICS",
                      "thermostat"   : "LANGEVIN DYNAMICS",
                      "barostat"     : "BERENDSEN PRESSURE COUPLING",
                      "barostat"     : "LANGEVIN PISTON PRESSURE CONTROL"
                      },
                  "preprocess"       : self.mdInfoTrans,
                  "postprocess"      : self.mdInfoTrans
                  }
              }
            ]

        fileinSubParsers = [
            # file Parser
            { "startReStr"        : "AlwaysRun",
              "parser"            : "dictionary_parser",
              "parsername"        : "file_parser",
              "waitlist"          : None,
              "stopOnMatchStr"    : "AlwaysStop",
              "quitOnMatchStr"    : "AlwaysStop",
              "metaNameStart"     : PARSERTAG + "_inout_file",
              "matchNameList"     : fileNameList,
              "matchNameDict"     : "fileDict",
              "updateMatchDict"   : True,
              "onlyCaseSensitive" : True,
              "stopOnFirstLine"   : True,
              "parserOptions"     : {
                  "dictionary"       : "cntrlDict",
                  "dicttype"         : "smartparser", # (standard or smartparser)
                  "readwritedict"    : "read",
                  "keyMapper"        : {
                      "structure"    : "STRUCTURE FILE",
                      "traj_coord"   : "Info: DCD FILENAME",
                      "traj_vel"     : "VELOCITY DCD FILENAME",
                      "traj_force"   : "FORCE DCD FILENAME",
                      "input_coord"  : "COORDINATE PDB",
                      "output_coord" : "OUTPUT FILENAME",
                      },
                  "preprocess"       : self.fileNameTrans
                  }
              }
            ]

        ########################################
        # return main Parser
        return [
            SM(name='NewRun',
                startReStr=r"\s*Info:\s*NAMD\s*[0-9.]+\s*for\s*",
                endReStr=r"\s*End\s*of\s*program\s*",
                repeats=True,
                required=True,
                forwardMatch=True,
                sections=['section_run'],
                fixedStartValues={'program_name': PROGRAMNAME},
                subMatchers=[
                    SM(name='ProgramInfo',
                       startReStr=r"\s*Info:\s*NAMD\s*"
                                   "(?P<program_version>[0-9.]+)\s*for\s*"
                                   "(?P<"+PARSERTAG+"_build_osarch>.+)\s*"),
                    SM(name='license',
                       startReStr=r"\s*Info:\s*Please\s*visit\s*",
                       coverageIgnore=True,
                       adHoc=lambda p:
                       self.adHoc_read_store_text_stop_parsing(p,
                           stopOnMatchStr=r"\s*Info:\s*(?:Info:Based|"
                                           "Built|Running|Configuration)\s*",
                           quitOnMatchStr=None,
                           metaNameStart=PARSERTAG+"_",
                           metaNameStore=PARSERTAG+"_program_citation",
                           matchNameList=None,
                           matchNameDict=None,
                           onlyCaseSensitive=True,
                           stopOnFirstLine=False,
                           storeFirstLine=True,
                           storeStopQuitLine=True,
                           onQuitRunFunction=lambda p: p.backend.addValue(
                               PARSERTAG+"_program_citation",
                               p.lastMatch[
                                   PARSERTAG+"_program_citation"
                                   ].replace('\n', ' ').replace('Info:', ' ')
                               )
                           )
                       ),
                    SM(name='loghostinfo',
                       startReStr=r"\s*Info:\s*Built\s*"
                                   "(?P<"+PARSERTAG+"_program_build_date>"
                                   "[a-zA-Z0-9:. ]+)\s*by"),
                    SM(name='SectionControlParm',
                       startReStr=r"\s*Info:\s*SIMULATION\s*PARAMETERS\s*",
                       endReStr=r"\s*Info:\s*(?:SUMMARY\s*OF\s*PARAMETERS|"
                                 "STRUCTURE\s*SUMMARY|Entering\s*startup)\s*",
                       forwardMatch=True,
                       sections=['section_sampling_method', PARSERTAG + '_section_control_parameters'],
                       adHoc=lambda p:
                       self.adHoc_takingover_parsing(p,
                           stopOnMatchStr=r"\s*Info:\s*(?:SUMMARY\s*OF\s*PARAMETERS|"
                                           "STRUCTURE\s*SUMMARY|Entering\s*startup)",
                           quitOnMatchStr=None,
                           stopControl="stopControl", # if None or True, stop with quitMatch, else wait
                           record=False, # if False or None, no record, no replay
                           replay=0, # if 0 or None= no replay, if <0 infinite replay
                           parseOnlyRecorded=False, # if True, parsers only work on record
                           ordered=False,
                           subParsers=mdinoutSubParsers)
                       ), # END SectionControlParm
                    SM(name='FileNameCopy',
                       startReStr=r"\s*Info:\s*Finished\s*startup",
                       forwardMatch=True,
                       sections=[PARSERTAG+'_section_input_output_files'],
                       coverageIgnore=True,
                       adHoc=lambda p:
                       self.adHoc_takingover_parsing(p,
                           stopOnMatchStr=r"^\s*$",
                           quitOnMatchStr=r"^\s*$",
                           stopControl="stopControl", # if None or True, stop with quitMatch, else wait
                           record=False, # if False or None, no record, no replay
                           replay=0, # if 0 or None= no replay, if <0 infinite replay
                           parseOnlyRecorded=False, # if True, parsers only work on record
                           ordered=False,
                           subParsers=fileinSubParsers),
                       ),
                    SM(name='SingleConfigurationCalculationWithSystemDescription',
                       startReStr=r"\s*ETITLE:\s*TS\s*",
                       endReStr=r"(?:^===================================================="
                                 "|WallClock:|End\s*of\s*program)\s*",
                       forwardMatch=True,
                       subMatchers=[
                           # the actual section for a single configuration calculation starts here
                           SM(name='SingleConfigurationCalculation',
                              startReStr=r"\s*ETITLE:\s*TS\s*",
                              endReStr=r"(?:^===================================================="
                                        "|^WallClock:|End\s*of\s*program)\s*",
                              repeats=True,
                              forwardMatch=True,
                              #sections=['section_single_configuration_calculation'],
                              subMatchers=[
                                  SM(name='MDStep',
                                     startReStr=r"\s*ETITLE:\s*TS\s*"
                                                 "(?P<"+PARSERTAG+"_mdin_finline>.*)(?:'|\")?\s*,?",
                                     forwardMatch=True,
                                     adHoc=lambda p:
                                     self.adHoc_takingover_parsing(p,
                                         stopOnMatchStr=r"^====================================================",
                                         quitOnMatchStr=r"^====================================================",
                                         stopControl="stopControl", # if None or True, stop with quitMatch, else wait
                                         record=False, # if False or None, no record, no replay
                                         replay=0, # if 0 or None= no replay, if <0 infinite replay
                                         parseOnlyRecorded=False, # if True, parsers only work on record
                                         ordered=False,
                                         onlySubParsersReadLine=True,
                                         subParsers=mdoutSubParsers)
                                     )]
                              ) # END SingleConfigurationCalculation
                       ]), # END SingleConfigurationCalculationWithSystemDescription
                    # summary of computation
                    SM(name='ComputationTimings',
                       startReStr=r"^WallClock:",
                       subMatchers=[
                           SM(r"^WallClock:\s*[0-9:.eEdD]+\s*CPUTime:\s*[0-9.:eEdD]+\s*Memory:\s*[0-9:.KMGTB ]+"),
                       ]), # END Computation
                    SM(name='end_run',
                       startReStr=r"\s*End\s*of\s*program\s*"),
                ]) # END NewRun
            ]


class NamdParserInterface():
   """ A proper class envolop for running this parser from within python. """
   def __init__(self, backend, **kwargs):
       self.backend_factory = backend

   def parse(self, mainfile):
        from unittest.mock import patch
        logging.info('namd parser started')
        logging.getLogger('nomadcore').setLevel(logging.WARNING)
        backend = self.backend_factory("namd.nomadmetainfo.json")
        parserInfo = {'name': 'namd-parser', 'version': '1.0'}
        context = NAMDParser()
        context.coverageIgnore = re.compile(r"^(?:" + r"|".join(context.coverageIgnoreList) + r")$")
        with patch.object(sys, 'argv', ['<exe>', '--uri', 'nmd://uri', mainfile]):
            mainFunction(
                mainFileDescription=context.mainFileDescription(),
                metaInfoEnv=None,
                parserInfo=parserInfo,
                cachingLevelForMetaName=context.cachingLevelForMetaName,
                superContext=context,
                superBackend=backend)
        return backend


if __name__ == "__main__":
    parser = NAMDParser()
    parser.parse()
