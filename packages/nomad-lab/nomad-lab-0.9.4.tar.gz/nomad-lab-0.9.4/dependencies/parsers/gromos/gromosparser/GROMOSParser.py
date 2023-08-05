# Copyright 2018-2018 Berk Onat
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
from nomadcore.smart_parser.SmartParserDictionary import isMetaStrInDict, setMetaStrInDict, copyMetaDictToDict
from .GROMOSDictionary import get_updateDictionary, set_Dictionaries
from .GROMOSCommon import PARSERNAME, PROGRAMNAME, PARSERVERSION, PARSERTAG, LOGGER
from .GROMOSCommon import PARSER_INFO_DEFAULT, META_INFO_PATH, set_excludeList, set_includeList
from nomadcore.md_data_access import MDDataAccess as MDDA
import argparse
import logging
import os
import re
import sys
import datetime
import io
import fnmatch
from nomadcore.simple_parser import mainFunction

############################################################
# This is the parser for the main file of GROMOS.
############################################################

#PRINTABLE = re.compile(r"\W+")

TEXTCHARS = bytearray({7,8,9,10,12,13,27} | set(range(0x20, 0x100)) - {0x7f})

def is_file_binary(fName, checkBytes=None):
    if checkBytes is None:
        checkBytes = 1024
    with open(fName, 'rb') as fin:
        testin = fin.read(checkBytes)
    if is_binary_string(testin):
        return True
    else:
        return False

def is_binary_string(inbytes):
    return bool(inbytes.translate(None, TEXTCHARS))

class GROMOSParser(SmartParser.ParserBase):
    """Context for parsing GROMOS main file.

    This class keeps tracks of several GROMOS settings to adjust the parsing to them.
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
            parserinfodef=PARSER_INFO_DEFAULT, recorderOn=True)

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
        self.fileUnitDict = {}
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
        self.newTopo = False
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
        self.cntrlparmstep = [-1]
        self.opencntrlstep = [-1]
        self.samplingstep = 0
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
        self.recordList = None
        self.stopControl = None
        self.numatoms = None
        self.secOpen = open_section
        self.superP = self.parser.backend.superBackend
        self.MDData = MDDA.MDDataAccess()
        self.inputCntrlFile = None
        if self.recordList:
            self.recordList.close()
        self.recordList = io.StringIO()

    def reset_values(self):
        self.minConverged = None
        self.trajectory = None
        self.newTopo = False
        self.newTraj = False
        self.newIncoord = False
        #self.secMethodGIndex = 0
        self.secSystemGIndex = 0
        #self.secTopologyGIndex = 0
        self.secSamplingGIndex = 0
        self.secSingleGIndex = 0
        self.secVDWGIndex = 0
        self.secAtomType = 0
        self.inputMethodIndex = 0
        self.inputControlIndex = 0
        self.mainMethodIndex = 0
        self.mainCalcIndex = 0
        self.MD = True
        self.MDiter = -1
        self.MDstep = 1
        self.MDcurrentstep = -1
        self.MDnextstep = 0
        self.cntrlparmstep = [-1]
        self.opencntrlstep = [-1]
        self.samplingstep = 0
        self.singleConfCalcs = []
        self.lastCalculationGIndex = None
        self.inputCntrlFile = None
        set_Dictionaries(self)

    def startedParsing(self, fInName, parser):
        """Function is called when the parsing starts.

        Get compiled parser, filename and metadata.

        Args:
            fInName: The file name on which the current parser is running.
            parser: The compiled parser. Is an object of the class SimpleParser in nomadcore.simple_parser.py.
        """
        self.parser = parser
        self.fName = fInName
        self.working_dir_name = os.path.dirname(os.path.abspath(self.fName))
        # save metadata
        self.metaInfoEnv = self.parser.parserBuilder.metaInfoEnv
        # allows to reset values if the same superContext is used to parse different files
        self.initialize_values()

#    def peekline(self, parser):
#        pos = parser.fIn.fIn.tell()
#        line = parser.fIn.fIn.readline()
#        parser.fIn.fIn.seek(pos)
#        return line

    def onOpen_section_run(self, backend, gIndex, section):
        # keep track of the latest section
        self.secRunGIndex = gIndex
        self.secRunOpen = True

    def onClose_section_run(self, backend, gIndex, section):
        """Trigger called when section_run is closed.

        Write the keywords from control parametres and
        the GROMOS output from the parsed log output,
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
        #self.initialize_values()
        self.secRunOpen = False
        self.metaStorage.reset({'startSection' : [['section_run']]})
        self.metaStorageRestrict.reset({'startSection' : [['section_restricted_uri']]})
        self.reset_values()

    def parameter_file_name(self, filedict, itemdict):
        """ Function to generate data for parameter files list
        """
        working_dir_name = os.path.dirname(os.path.normpath(os.path.abspath(self.fName)))
        parmmeta = isMetaStrInDict("structure",self.fileDict)
        filename = []
        if parmmeta is not None:
            if self.fileDict[parmmeta].value is not None:
                fname = self.fileDict[parmmeta].value
                filename.append(fname.replace(working_dir_name, '.'+os.path.sep))
        if filename:
            return False, filename, itemdict
        else:
            return False, None, itemdict
    def gromos_input_output_files(self, backend, gIndex, section):
        """Called with onClose_x_gromos_section_control_parameters to setup
            topology and trajectory inputs/outputs

        Determine whether topology, trajectory and input coordinate files are
        supplied to the parser

        Initiates topology and trajectory file handles.

        Captures topology, atomic positions, atom labels, lattice vectors and
        stores them before section_system and
        section_single_configuration_calculation are encountered.
        """
        # Checking whether topology, input
        # coordinates and trajectory files exist
        fileList=None
        fKey = PARSERTAG + '_inout_file_'
        working_dir_name = os.path.dirname(os.path.abspath(self.fName))
        try:
            getattr(self, "filesInOutputDir")
        except AttributeError:
            self.filesInOutputDir = {}
            fileList = [x for x in os.walk(os.path.abspath(working_dir_name))]
            for fdir, fchilds, fnames in fileList:
                for fname in fnames:
                    fkeyname = os.path.normpath(os.path.join(fdir, fname))
                    self.filesInOutputDir.update({fkeyname.upper():fkeyname})

        # Reset all file definitions to None and inactive
        atLeastOneFileExist = False # also be used to check any updates
        for k,v in self.fileDict.items():
            if k.startswith(fKey):
                self.fileDict[k].value = None
                self.fileDict[k].activeInfo = False
                self.fileDict[k].fileSupplied = False

        inputOK = self.findInputCmdFileAndRead(parser)

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

        # Here we update topology info
        # Check if topology files can be loaded
        self.newTopo = False
        self.newIncoord=False
        topoDone=False
        IncoordDone=False
        topoFile = self.findFileInDir(parser, "topology read from", "filecntrlDict")
        confFile = self.findFileInDir(parser, "configuration read from", "filecntrlDict")
        if topoFile is not None:
            if topoFile.upper() in self.filesInOutputDir:
                file_name = self.filesInOutputDir[topoFile.upper()]
                self.fileDict[fKey+'structure'].value = file_name.replace(
                        working_dir_name+os.path.sep, '')
                self.fileDict[fKey+'structure'].fileName = file_name
                self.fileDict[fKey+'structure'].activeInfo = True
                self.fileDict[fKey+'structure'].fileSupplied = True
                atLeastOneFileExist = True
                topoDone = True
                self.newTopo = True

        if confFile is not None:
            if confFile.upper() in self.filesInOutputDir:
                file_name = self.filesInOutputDir[confFile.upper()]
                self.fileDict[fKey+'input_coord'].value = file_name.replace(
                        working_dir_name+os.path.sep, '')
                self.fileDict[fKey+'input_coord'].fileName = file_name
                self.fileDict[fKey+'input_coord'].activeInfo = True
                self.fileDict[fKey+'input_coord'].fileSupplied = True
                atLeastOneFileExist = True
                IncoordDone = True
                self.newIncoord=True

        self.newTraj = False
        trajDone=False
        outLogFile = os.path.normpath(os.path.abspath(self.fName))
        baseOutLog = os.path.basename(self.fName)
        extsOutLog = MDDA.get_fileExtensions(baseOutLog)
        guessOutExt = '.'+extsOutLog[-1]
        trcFound = None
        guessTRCfile = outLogFile.replace(guessOutExt, '.trc')
        if guessTRCfile.upper() in self.filesInOutputDir:
            trcFound = self.filesInOutputDir[guessTRCfile.upper()]
        if trcFound is None:
            guessTRCfile = outLogFile.replace(guessOutExt, '.trc.gz')
            if guessTRCfile.upper() in self.filesInOutputDir:
                trcFound = self.filesInOutputDir[guessTRCfile.upper()]
        if trcFound is None:
            guessTRCfile = outLogFile.replace(guessOutExt, '.trc.zip')
            if guessTRCfile.upper() in self.filesInOutputDir:
                trcFound = self.filesInOutputDir[guessTRCfile.upper()]
        if trcFound is not None:
            file_name = trcFound
            self.fileDict[fKey+'trajectory'].value = file_name.replace(
                    working_dir_name+os.path.sep, '')
            self.fileDict[fKey+'trajectory'].fileName = file_name
            self.fileDict[fKey+'trajectory'].activeInfo = True
            self.fileDict[fKey+'trajectory'].fileSupplied = True
            atLeastOneFileExist = True
            trajDone = True
            self.newTraj = True

        if atLeastOneFileExist:
        #    updateDict = {
        #            'startSection'   : [[PARSERTAG+'_section_input_output_files']],
        #            'dictionary'     : self.fileDict
        #            }
        #    self.metaStorage.update(updateDict)
        #    self.metaStorage.updateBackend(backend.superBackend,
        #            startsection=[PARSERTAG+'_section_input_output_files'],
        #            autoopenclose=False)
            self.secRestrictGIndex = backend.superBackend.openSection("section_restricted_uri")
            restrictionsDict = get_updateDictionary(self, 'restrictions')
            updateDict = {
                    'startSection' : [['section_restricted_uri']],
                    'dictionary' : restrictionsDict
                    }
            self.metaStorageRestrict.update(updateDict)
            self.metaStorageRestrict.updateBackend(backend.superBackend,
                    startsection=['section_restricted_uri'],
                    autoopenclose=False)
            backend.superBackend.closeSection("section_restricted_uri", self.secRestrictGIndex)

        if self.newTopo:
            if topoDone and atLeastOneFileExist:
                self.MDData.initializeTopologyFileHandlers(self)
                if self.topology:
                    self.topoDict = self.topology.topoDict
        if self.newTraj:
            if trajDone and atLeastOneFileExist:
                self.MDData.initializeTrajectoryFileHandlers(self)
                if self.trajectory:
                    self.atompositions = self.trajectory.positions()
        if self.newIncoord:
            if IncoordDone and atLeastOneFileExist:
                self.MDData.initializeInputCoordinateFileHandlers(self)
                if self.inputcoords:
                    self.inputpositions = self.inputcoords.positions()
                    self.numatoms = len(self.inputpositions)
        if self.topology:
            if self.topology.n_atoms is not None:
                if self.atompositions:
                    self.topology.n_atoms = len(self.atompositions)
                elif self.inputpositions:
                    self.topology.n_atoms = len(self.inputpositions)
                elif self.numatoms:
                    self.topology.n_atoms = self.numatoms
                #self.MDData.initializeOutputCoordinateFileHandlers(self)
                #self.MDData.initializeFileHandlers(self)
                #if self.outputcoords:
                #    self.outputpositions = self.outputcoords.positions()
                #self.MDiter += self.MDstep
                #self.MDiter += 1
                #self.MDcurrentstep = int(self.MDiter)
                #self.stepcontrolDict.update({"MDcurrentstep" : int(self.MDcurrentstep)})
                #pass

    def onOpen_x_gromos_section_control_parameters(self, backend, gIndex, section):
        # keep track of the latest section
        if self.inputControlIndex is None:
            self.inputControlIndex = gIndex

    def onClose_x_gromos_section_control_parameters(self, backend, gIndex, section):
        section_control_Dict = {}
        section_control_Dict.update(self.topocntrlDict)
        section_control_Dict.update(self.ffcntrlDict)
        section_control_Dict.update(self.filecntrlDict)
        section_control_Dict.update(self.cntrlDict)
        updateDict = {
            'startSection' : [[PARSERTAG+'_section_control_parameters']],
            'dictionary'   : section_control_Dict
            }
        self.metaStorage.update(updateDict)
        self.metaStorage.updateBackend(backend.superBackend,
                startsection=[PARSERTAG+'_section_control_parameters'],
                autoopenclose=False)

        # Find input and output files. Read input control parameters
        self.gromos_input_output_files(backend, gIndex, section)

        # GROMOS prints the initial and final energies to the log file.
        self.MDcurrentstep += 1
        self.stepcontrolDict.update({"MDcurrentstep" : int(self.MDcurrentstep)})
        nsteps = 0
        nlogsteps = 0
        nstructstep = 0
        ninputstep = 0
        noutputstep = 0
        ntrajsteps = 0
        nvelsteps = 0
        nforcesteps = 0

        nstructKey = isMetaStrInDict("topology read from",self.filecntrlDict)
        ninputKey = isMetaStrInDict("configuration read from",self.filecntrlDict)
        nminstepKey = isMetaStrInDict("EMIN-NMIN", self.cntrlDict)
        nstepKey = isMetaStrInDict("STEP-NSTLIM", self.cntrlDict)
        nlogKey = isMetaStrInDict("PRNT-NTPR", self.cntrlDict)
        nxoutKey = isMetaStrInDict("WRIT-NTWX", self.cntrlDict)
        nvoutKey = isMetaStrInDict("WRIT-NTWV", self.cntrlDict)
        nfoutKey = isMetaStrInDict("WRIT-NTWF", self.cntrlDict)
        if nstepKey is not None:
            if self.cntrlDict[nstepKey].activeInfo:
                nsteps = conv_int(self.cntrlDict[nstepKey].value, default=0)
            else:
                #nsteps = conv_int(self.cntrlDict[nstepKey].defaultValue, default=0)
                nsteps = 0
        if nminstepKey is not None:
            if self.cntrlDict[nminstepKey].activeInfo:
                self.MD = False
                nsteps = conv_int(self.cntrlDict[nminstepKey].value, default=0)
        if nlogKey is not None:
            if self.cntrlDict[nlogKey].activeInfo:
                nlogsteps = conv_int(self.cntrlDict[nlogKey].value, default=1)
            else:
                if self.cntrlDict[nlogKey].defaultValue is not None:
                    nlogsteps = conv_int(self.cntrlDict[nlogKey].defaultValue, default=1)
                else:
                    nlogsteps = -1
        if nxoutKey is not None:
            if self.cntrlDict[nxoutKey].activeInfo:
                ntrajsteps = conv_int(self.cntrlDict[nxoutKey].value, default=0)
        if nstructKey is not None:
            if self.filecntrlDict[nstructKey].activeInfo:
                nstructstep = 1
        if ninputKey is not None:
            if self.filecntrlDict[ninputKey].activeInfo:
                ninputstep = 1
        #if noutputKey is not None:
        #    if self.cntrlDict[noutputKey].activeInfo:
        #        noutputstep = 1
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
            logsteps = [0, nsteps]
            #logsteps.append(nsteps)
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
        self.onOpen_section_sampling_method(backend, None, None)
        self.onClose_section_sampling_method(backend, None, None)
        if self.topology:
            if self.newTopo:
                section_file_Dict = {}
                section_file_Dict.update(self.fileDict)
                updateDict = {
                        'startSection' : [[PARSERTAG+'_section_control_parameters']],
                        'dictionary'   : section_file_Dict
                        }
                self.metaStorage.update(updateDict)
                self.metaStorage.updateBackend(backend.superBackend,
                        startsection=[PARSERTAG+'_section_control_parameters'],
                        autoopenclose=False)

                self.secRestrictGIndex = backend.superBackend.openSection("section_restricted_uri")
                restrictionsDict = get_updateDictionary(self, 'restrictions')
                updateDict = {
                        'startSection' : [['section_restricted_uri']],
                        'dictionary' : restrictionsDict
                        }
                self.metaStorageRestrict.update(updateDict)
                self.metaStorageRestrict.updateBackend(backend.superBackend,
                        startsection=['section_restricted_uri'],
                        autoopenclose=False)
                backend.superBackend.closeSection("section_restricted_uri", self.secRestrictGIndex)

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
        if (gIndex is None or gIndex == -1 or gIndex == "-1"):
            self.secSamplingGIndex = backend.superBackend.openSection("section_sampling_method")
        else:
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
        if (gIndex is None or gIndex == -1 or gIndex == "-1"):
            backend.superBackend.closeSection("section_sampling_method", self.secSamplingGIndex)

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
        if self.numatoms is not None:
            numatoms = self.numatoms

        # GROMOS default unit vectors. If all are zeros than the simulation cell is not periodic.
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
            if self.newTopo:
#            if (self.secTopologyGIndex is None or
#                (self.secTopologyGIndex == -1 or
#                self.secTopologyGIndex == "-1")):
                self.onOpen_section_topology(backend, None, None)
                self.onClose_section_topology(backend, None, None)
                self.newTopo=False
        if self.secTopologyGIndex is not None:
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
                    coordinates.unitcell_vectors, "nano-meter", self.unitDict))
                SloppyBackend.addArrayValues('simulation_cell', unit_cell)
                SloppyBackend.addArrayValues('lattice_vectors', unit_cell)
            if coordinates.unitcell_lengths is not None:
                SloppyBackend.addArrayValues(PARSERTAG + '_lattice_lengths', coordinates.unitcell_lengths)
            if coordinates.unitcell_angles is not None:
                SloppyBackend.addArrayValues(PARSERTAG + '_lattice_angles', coordinates.unitcell_angles)
            # GROMOS Guide says: (See http://www.ks.uiuc.edu/Research/gromos/2.12/ug/node11.html)
            # Positions in PDB/GROMOS binary/DCD files are stored in A.
            #pos_obj = getattr(self.trajectory, 'positions', None)
            #if callable(pos_obj):
            SloppyBackend.addArrayValues('atom_positions', np.transpose(np.asarray(
                self.metaStorage.convertUnits(positions, "nano-meter", self.unitDict))))
            if coordinates.velocities is not None:
                # Velocities in PDB files are stored in A/ps units.(PDB files are read for input
                #     coordinates, velocities, and forces)
                # Velocities in GROMOS binary/DCD files are stored in GROMOS internal units and must be multiplied
                #     by PDBVELFACTOR=20.45482706 to convert to A/ps. (These files are used for output trajectory)
                SloppyBackend.addArrayValues('atom_velocities', np.transpose(np.asarray(
                    self.metaStorage.convertUnits(
                        coordinates.velocities, "(nano-meter)/(pico-second)", self.unitDict))))
                # need to transpose array since its shape is [number_of_atoms,3] in the metadata

            if self.topology is not None:
                if "atom_element_list" in self.topoDict:
                    atom_labels = self.topoDict["atom_element_list"]
                    numatoms = len(atom_labels)
                    self.numatoms
                    SloppyBackend.addArrayValues('atom_labels', np.asarray(atom_labels))
        else:
            if unit_vectors is not None:
                unit_cell = np.asarray(self.metaStorage.convertUnits(
                    unit_vectors, "nano-meter", self.unitDict))
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

        if self.topology is not None:
            self.topology_system_name(backend, gIndex)

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
        try:
            self.MDcurrentstep = int(self.stepcontrolDict["MDcurrentstep"])
        except KeyError:
            self.stepcontrolDict.update({"MDcurrentstep" : int(self.MDcurrentstep)})
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
                # Forces in PDB/GROMOS binary/DCD files are stored in kcal/mol/A
                SloppyBackend.addArrayValues('atom_forces', np.transpose(np.asarray(
                    self.metaStorage.convertUnits(
                        self.atompositions.velocities, "kilo-joule/(mol*nano-meter)", self.unitDict))))
                # need to transpose array since its shape is [number_of_atoms,3] in the metadata

        if(self.MDcurrentstep in trajsteps or
           self.MDcurrentstep in velsteps):
            self.onOpen_section_system(backend, None, None)
            self.onClose_section_system(backend, None, None)
            backend.addValue('single_configuration_calculation_to_system_ref', self.secSystemGIndex)
            self.MDiter += 1
        else:
            if(self.MDcurrentstep in logsteps or
               self.MDcurrentstep in forcesteps):
                self.MDiter += 1
            if(self.inputcoords is not None and
               self.MDcurrentstep == steps[0] and
               self.inputpositions is not None):
                self.onOpen_section_system(backend, None, None)
                self.onClose_section_system(backend, None, None)
                backend.addValue('single_configuration_calculation_to_system_ref', self.secSystemGIndex)
                self.MDiter += 1
            if(self.outputcoords is not None and
               self.MDcurrentstep == steps[-1] and
               self.outputpositions is not None):
                self.onOpen_section_system(backend, None, None)
                self.onClose_section_system(backend, None, None)
                backend.addValue('single_configuration_calculation_to_system_ref', self.secSystemGIndex)
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
        backend.superBackend.closeSection("section_single_configuration_calculation", self.secSingleGIndex)

    def setStartingPointCalculation(self, parser):
        backend = parser.backend
        backend.openSection('section_calculation_to_calculation_refs')
        if self.lastCalculationGIndex:
            backend.addValue('calculation_to_calculation_ref', self.lastCalculationGIndex)
            backend.closeSection('section_calculation_to_calculation_refs')
        return None

    def fileNameTrans(self, fname, value):
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
                "STEP" : "MDcurrentstep",
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
        istimestep = isMetaStrInDict("STEP-DT",self.cntrlDict)
        if istimestep is not None:
            if self.cntrlDict[istimestep].value is not None:
                timestep = float(self.cntrlDict[istimestep].value)
        if value is not None:
            for k,v in keyMapper.items():
                if fname in k:
                    return value*timestep
        return value

    def filesFoundInDir(self, parser):
        fileList = []
        working_dir_name = os.path.dirname(os.path.abspath(self.fName))
        for afile in os.listdir(working_dir_name):
            if os.path.isfile(os.path.normpath(os.path.join(working_dir_name,afile))):
                fileList.append(afile)
                #fileList.append(os.path.normpath(os.path.join(working_dir_name,afile)))
        if fileList:
            return fileList
        else:
            return None

    def textFileFoundInDir(self, parser):
        fileList = self.filesFoundInDir(parser)
        if fileList is None:
            fileList=[]
        foundList = []
        working_dir_name = os.path.dirname(os.path.abspath(self.fName))
        for afile in fileList:
            if is_file_binary(os.path.normpath(os.path.join(working_dir_name,afile))) is False:
                foundList.append(os.path.normpath(os.path.join(working_dir_name,afile)))
        if foundList:
            return foundList
        else:
            return None

    def matchStrInTextFile(self, parser, file_name, matchReStr):
        matched = False
        matchRe = re.compile(matchReStr)
        with open(file_name, 'r') as fin:
            for line in fin:
               if matchRe.findall(line):
                   matched = True
                   break
        return matched

    def checkTextFilesMatchStr(self, parser, fileList, includeReStrList=None, excludeReStrList=None):
        includedList = []
        excludedList = []
        if includeReStrList is None:
            includeReStrList = []
        if excludeReStrList is None:
            excludeReStrList = []
        # If a match string list is given,
        # find the files have macth Re in the list
        if includeReStrList:
            for fName in fileList:
                for reStr in includeReStrList:
                    if self.matchStrInTextFile(parser,fName,reStr):
                        includedList.append(fName)
        else:
            includedList = fileList
        # If and exclude list is given,
        # remove the files from list that
        # includes these Regular expression matches
        if excludeReStrList:
            for fName in includedList:
                for reStr in excludeReStrList:
                    if not self.matchStrInTextFile(parser,fName,reStr):
                        excludedList.append(fName)
        else:
            excludedList = includedList
        return excludedList

    def storeTextFile(self, parser, textDict, storeName, textFile):
        if textDict:
            recordText = []
            with io.open(textFile) as fin:
                recordText.append(fin.readline())
            textDict.update({storeName:recordText})
            return textDict
        else:
            return None

    def prune_list(self, iList):
        oList = []
        for item in iList:
            if item:
                if isinstance(item, (list, tuple)):
                    item = self.prune_list(item)
                oList.append(item)
        return oList

    def readGromosParameterFile(self, parser, fileName, cntrlDict):
        success = False
        emptyLine = re.compile(r"^\s*$")
        if fileName is not None:
            with open(fileName, 'r') as fin:
                section = None
                enid = 0 # energymin input id
                syid = 0 # system inout id
                inid = 0 # initilise
                stid = 0 # step
                bcid = 0 # boundcond
                prid = 0 # printout
                csid = 0 # constraint
                frid = 0 # force
                plid = 0 # pairlist
                nbid = 0 # nonbonded
                mbid = 0 # multibath
                psid = 0 # pressurescale
                cfid = 0 # covalentform
                ctid = 0 # comtransrot
                wtid = 0 # writetraj
                bathalg = 0
                numbaths = 1
                dofset = 1
                temp = None
                tau = None
                last = None
                combath = None
                irbath = None
                aniso = None
                pres0 = None
                for line in fin:
                    if emptyLine.findall(line):
                        continue
                    cmdLine = ' '.join([x for x in line.strip().split() if x]).upper()
                    if cmdLine.startswith('#'):
                        continue
                    if cmdLine.startswith('END'):
                        section = None
                        enid = 0
                        syid = 0
                        inid = 0
                        stid = 0
                        bcid = 0
                        prid = 0
                        csid = 0
                        frid = 0
                        plid = 0
                        nbid = 0
                        mbid = 0
                        psid = 0
                        cfid = 0
                        ctid = 0
                        wtid = 0
                        bathalg = 0
                        numbaths = 1
                        dofset = 1
                        temp = None
                        tau = None
                        last = None
                        combath = None
                        irbath = None
                        aniso = None
                        pres0 = None
                        continue
                    elif cmdLine.startswith('TITLE'):
                        section = 'TITLE'
                        continue
                    elif cmdLine.startswith('ENERGYMIN'):
                        section = 'ENERGYMIN'
                        continue
                    elif cmdLine.startswith('SYSTEM'):
                        section = 'SYSTEM'
                        continue
                    elif cmdLine.startswith('INITIALISE'):
                        section = 'INITIALISE'
                        continue
                    elif cmdLine.startswith('STEP'):
                        section = 'STEP'
                        continue
                    elif cmdLine.startswith('BOUNDCOND'):
                        section = 'BOUNDCOND'
                        continue
                    elif cmdLine.startswith('MULTIBATH'):
                        section = 'MULTIBATH'
                        continue
                    elif cmdLine.startswith('PRESSURESCALE'):
                        section = 'PRESSURESCALE'
                        continue
                    elif cmdLine.startswith('COVALENTFORM'):
                        section = 'COVALENTFORM'
                        continue
                    elif cmdLine.startswith('COMTRANSROT'):
                        section = 'COMTRANSROT'
                        continue
                    elif cmdLine.startswith('PRINTOUT'):
                        section = 'PRINTOUT'
                        continue
                    elif cmdLine.startswith('WRITETRAJ'):
                        section = 'WRITETRAJ'
                        continue
                    elif cmdLine.startswith('CONSTRAINT'):
                        section = 'CONSTRAINT'
                        continue
                    elif cmdLine.startswith('FORCE'):
                        section = 'FORCE'
                        continue
                    elif cmdLine.startswith('PAIRLIST'):
                        section = 'PAIRLIST'
                        continue
                    elif cmdLine.startswith('NONBONDED'):
                        section = 'NONBONDED'
                        continue
                    if section == 'TITLE':
                        rtn = setMetaStrInDict(self, 'cntrlDict', 'TITLE', line.strip())
                        success = rtn[0] if success is False else True
                    elif section == 'ENERGYMIN':
                        for item in cmdLine.split():
                            addok = False
                            if enid == 0:
                                addok = True
                                rtn = setMetaStrInDict(self, 'cntrlDict', 'EMIN-NTEM', item)
                            elif enid == 1:
                                addok = True
                                rtn = setMetaStrInDict(self, 'cntrlDict', 'EMIN-NCYC', item)
                            elif enid == 2:
                                addok = True
                                rtn = setMetaStrInDict(self, 'cntrlDict', 'EMIN-DELE', item)
                            elif enid == 3:
                                addok = True
                                rtn = setMetaStrInDict(self, 'cntrlDict', 'EMIN-DX0', item)
                            elif enid == 4:
                                addok = True
                                rtn = setMetaStrInDict(self, 'cntrlDict', 'EMIN-DXM', item)
                            elif enid == 5:
                                addok = True
                                rtn = setMetaStrInDict(self, 'cntrlDict', 'EMIN-NMIN', item)
                            elif enid == 6:
                                addok = True
                                rtn = setMetaStrInDict(self, 'cntrlDict', 'EMIN-FLIM', item)
                            if addok:
                                enid += 1
                                success = rtn[0] if success is False else True
                    elif section == 'SYSTEM':
                        for item in cmdLine.split():
                            addok = False
                            if syid == 0:
                                addok = True
                                rtn = setMetaStrInDict(self, 'cntrlDict', 'SYS-NPM', item)
                            elif syid == 1:
                                addok = True
                                rtn = setMetaStrInDict(self, 'cntrlDict', 'SYS-NSM', item)
                            if addok:
                                syid += 1
                                success = rtn[0] if success is False else True
                    elif section == 'STEP':
                        for item in cmdLine.split():
                            addok = False
                            if stid == 0:
                                addok = True
                                rtn = setMetaStrInDict(self, 'cntrlDict', 'STEP-NSTLIM', item)
                            elif stid == 1:
                                addok = True
                                rtn = setMetaStrInDict(self, 'cntrlDict', 'STEP-T', item)
                            elif stid == 2:
                                addok = True
                                rtn = setMetaStrInDict(self, 'cntrlDict', 'STEP-DT', item)
                            if addok:
                                stid += 1
                                success = rtn[0] if success is False else True
                    elif section == 'MULTIBATH':
                        for item in cmdLine.split():
                            addok = False
                            if mbid == 0:
                                addok = True
                                rtn = setMetaStrInDict(self, 'cntrlDict', 'BATH-ALG', item)
                                try:
                                    bathalg=int(item)
                                except (ValueError, TypeError):
                                    pass
                            elif(mbid == 1 and bathalg>1):
                                addok = True
                                rtn = setMetaStrInDict(self, 'cntrlDict', 'BATH-NUM', item)
                            elif((mbid == 1 and bathalg<2) or (mbid == 2 and bathalg>1)):
                                addok = True
                                rtn = setMetaStrInDict(self, 'cntrlDict', 'BATH-NBATHS', item)
                                numbaths=int(item)
                            elif((mbid >= 2 and mbid < 2+(2*numbaths) and bathalg<2) or
                                 (mbid >= 3 and mbid < 3+(2*numbaths) and bathalg>1)):
                                addok = True
                                if(((mbid-1)%2==1 and bathalg<2) or
                                   ((mbid-2)%2==1 and bathalg>1)):
                                    if temp == None:
                                        temp = item
                                    else:
                                        temp = temp + ', ' + item
                                    rtn = setMetaStrInDict(self, 'cntrlDict', 'BATH-TEMP', temp)
                                elif(((mbid-1)%2==0 and bathalg<2) or
                                     ((mbid-2)%2==0 and bathalg>1)):
                                    if tau == None:
                                        tau = item
                                    else:
                                        tau = tau + ', ' + item
                                    rtn = setMetaStrInDict(self, 'cntrlDict', 'BATH-TAU', tau)
                            elif((mbid == 2+(2*numbaths) and bathalg<2) or
                                 (mbid == 3+(2*numbaths) and bathalg>1)):
                                addok = True
                                rtn = setMetaStrInDict(self, 'cntrlDict', 'BATH-DOFSET', item)
                                try:
                                    dofset=int(item)
                                except (ValueError, TypeError):
                                    pass
                            elif((mbid >= 3+(2*numbaths) and mbid < 3+(2*numbaths)+dofset and bathalg<2) or
                                 (mbid >= 4+(2*numbaths) and mbid < 4+(2*numbaths)+dofset and bathalg>1)):
                                addok = True
                                if last == None:
                                    last = item
                                else:
                                    last = last + ', ' + item
                                rtn = setMetaStrInDict(self, 'cntrlDict', 'BATH-LAST', last)
                            elif((mbid >= 3+(2*numbaths)+dofset and mbid < 3+(2*numbaths)+(2*dofset) and bathalg<2) or
                                 (mbid >= 4+(2*numbaths)+dofset and mbid < 4+(2*numbaths)+(2*dofset) and bathalg>1)):
                                addok = True
                                if combath == None:
                                    combath = item
                                else:
                                    combath = combath + ', ' + item
                                rtn = setMetaStrInDict(self, 'cntrlDict', 'BATH-COMBATH', combath)
                            elif((mbid >= 3+(2*numbaths)+(2*dofset) and mbid < 3+(2*numbaths)+(3*dofset) and bathalg<2) or
                                 (mbid >= 4+(2*numbaths)+(2*dofset) and mbid < 4+(2*numbaths)+(3*dofset) and bathalg>1)):
                                addok = True
                                if irbath == None:
                                    irbath = item
                                else:
                                    irbath = irbath + ', ' + item
                                rtn = setMetaStrInDict(self, 'cntrlDict', 'BATH-IRBATH', irbath)
                            if addok:
                                mbid += 1
                                success = rtn[0] if success is False else True
                    elif section == 'PRESSURESCALE':
                        for item in cmdLine.split():
                            addok = False
                            if psid == 0:
                                addok = True
                                rtn = setMetaStrInDict(self, 'cntrlDict', 'PRES-COUPLE', item)
                            elif psid == 1:
                                addok = True
                                rtn = setMetaStrInDict(self, 'cntrlDict', 'PRES-SCALE', item)
                            elif psid == 2:
                                addok = True
                                rtn = setMetaStrInDict(self, 'cntrlDict', 'PRES-COMP', item)
                            elif psid == 3:
                                addok = True
                                rtn = setMetaStrInDict(self, 'cntrlDict', 'PRES-TAUP', item)
                            elif psid == 4:
                                addok = True
                                rtn = setMetaStrInDict(self, 'cntrlDict', 'PRES-VIRIAL', item)
                            elif psid >= 5 and psid <= 7:
                                addok = True
                                if aniso is None:
                                    aniso = item
                                else:
                                    aniso = aniso + ', ' + item
                                rtn = setMetaStrInDict(self, 'cntrlDict', 'PRES-ANISO', aniso)
                            elif psid >= 8 and psid <= 16:
                                addok = True
                                if pres0 is None:
                                    pres0 = item
                                else:
                                    pres0 = pres0 + ', ' + item
                                rtn = setMetaStrInDict(self, 'cntrlDict', 'PRES-INIT0', pres0)
                            if addok:
                                psid += 1
                                success = rtn[0] if success is False else True
                    elif section == 'INITIALISE':
                        for item in cmdLine.split():
                            addok = False
                            if inid == 0:
                                addok = True
                                rtn = setMetaStrInDict(self, 'cntrlDict', 'INIT-NTIVEL', item)
                            elif inid == 1:
                                addok = True
                                rtn = setMetaStrInDict(self, 'cntrlDict', 'INIT-NTISHK', item)
                            elif inid == 2:
                                addok = True
                                rtn = setMetaStrInDict(self, 'cntrlDict', 'INIT-NTINHT', item)
                            elif inid == 3:
                                addok = True
                                rtn = setMetaStrInDict(self, 'cntrlDict', 'INIT-NTINHB', item)
                            elif inid == 4:
                                addok = True
                                rtn = setMetaStrInDict(self, 'cntrlDict', 'INIT-NTISHI', item)
                            elif inid == 5:
                                addok = True
                                rtn = setMetaStrInDict(self, 'cntrlDict', 'INIT-NTIRTC', item)
                            elif inid == 6:
                                addok = True
                                rtn = setMetaStrInDict(self, 'cntrlDict', 'INIT-NTICOM', item)
                            elif inid == 7:
                                addok = True
                                rtn = setMetaStrInDict(self, 'cntrlDict', 'INIT-NTISTI', item)
                            elif inid == 8:
                                addok = True
                                rtn = setMetaStrInDict(self, 'cntrlDict', 'INIT-IG', item)
                            elif inid == 9:
                                addok = True
                                rtn = setMetaStrInDict(self, 'cntrlDict', 'INIT-TEMPI', item)
                            if addok:
                                inid += 1
                                success = rtn[0] if success is False else True
                    elif section == 'BOUNDCOND':
                        for item in cmdLine.split():
                            addok = False
                            if bcid == 0:
                                addok = True
                                rtn = setMetaStrInDict(self, 'cntrlDict', 'BCND-NTB', item)
                            elif bcid == 1:
                                addok = True
                                rtn = setMetaStrInDict(self, 'cntrlDict', 'BCND-NDFMIN', item)
                            if addok:
                                bcid += 1
                                success = rtn[0] if success is False else True
                    elif section == 'PRINTOUT':
                        for item in cmdLine.split():
                            addok = False
                            if prid == 0:
                                addok = True
                                rtn = setMetaStrInDict(self, 'cntrlDict', 'PRNT-NTPR', item)
                            elif prid == 1:
                                addok = True
                                rtn = setMetaStrInDict(self, 'cntrlDict', 'PRNT-NTPP', item)
                            if addok:
                                prid += 1
                                success = rtn[0] if success is False else True
                    elif section == 'WRITETRAJ':
                        for item in cmdLine.split():
                            addok = False
                            if wtid == 0:
                                addok = True
                                rtn = setMetaStrInDict(self, 'cntrlDict', 'WRIT-NTWX', item)
                            elif wtid == 1:
                                addok = True
                                rtn = setMetaStrInDict(self, 'cntrlDict', 'WRIT-NTWSE', item)
                            elif wtid == 2:
                                addok = True
                                rtn = setMetaStrInDict(self, 'cntrlDict', 'WRIT-NTWV', item)
                            elif wtid == 3:
                                addok = True
                                rtn = setMetaStrInDict(self, 'cntrlDict', 'WRIT-NTWF', item)
                            elif wtid == 4:
                                addok = True
                                rtn = setMetaStrInDict(self, 'cntrlDict', 'WRIT-NTWE', item)
                            elif wtid == 5:
                                addok = True
                                rtn = setMetaStrInDict(self, 'cntrlDict', 'WRIT-NTWG', item)
                            elif wtid == 6:
                                addok = True
                                rtn = setMetaStrInDict(self, 'cntrlDict', 'WRIT-NTWB', item)
                            if addok:
                                wtid += 1
                                success = rtn[0] if success is False else True
        return success

    def findFileInDir(self, parser, fileMetaName, cntrlDictName):
        filecntrlDict = getattr(self, cntrlDictName)
        if filecntrlDict is not None:
            infileKey = isMetaStrInDict(fileMetaName, filecntrlDict)
        infile = None
        paramFile = None
        if infileKey is not None:
            if filecntrlDict[infileKey].value is not None:
                infile = filecntrlDict[infileKey].value
        if infile is not None:
            #self.working_dir_name
            #working_dir_name = os.path.dirname(os.path.abspath(os.getcwd()))
            thisfile=os.path.normpath(infile)
            findfile=os.path.basename(thisfile)
            dirlisti=thisfile.split(os.path.sep)
            dirlist=self.prune_list(dirlisti)
            sepp=os.path.sep

            subdirlist = [sepp.join(dirlist[dr:-1]) for dr in range(len(dirlist))]
            for sid, sdir in enumerate(subdirlist):
                if sdir == '':
                    subdirlist[sid] = os.curdir

            matchdirs = []
            for root, dirnames, filenames in os.walk(self.working_dir_name):
                for possubdir in subdirlist:
                    for subdir in fnmatch.filter(dirnames, possubdir):
                        matchdirs.append(os.path.join(root, subdir))
            if matchdirs:
                pass
            else:
                matchdirs.append(self.working_dir_name)

            matches = []
            for root, dirnames, filenames in os.walk(self.working_dir_name):
                if root == self.working_dir_name:
                    for filename in fnmatch.filter(filenames, findfile):
                        matches.append(os.path.join(root, filename))
                        break
            if matches:
                pass
            else:
                for root, dirnames, filenames in os.walk(self.working_dir_name):
                    for mdir in matchdirs:
                        if mdir+sepp+findfile == root+sepp+findfile:
                            for filename in fnmatch.filter(filenames, findfile):
                                matches.append(os.path.join(root, filename))
                                break

            inputFile = None
            if matches:
                inputFile = matches[0]

            if inputFile is not None:
                paramFile = os.path.normpath(os.path.abspath(inputFile))

        return paramFile

    def findInputCmdFileAndRead(self, parser):
        paramFile = self.findFileInDir(parser, "parameter read from", "filecntrlDict")
        if paramFile is not None:
            self.inputCntrlFile = paramFile
            success = self.readGromosParameterFile(parser, paramFile, 'cntrlDict')

        return success

    def build_subMatchers(self):
        """Builds the sub matchers to parse the main output file.
        """
        mddataNameList=getList_MetaStrInDict(self.mddataDict)

        self.mdTempHeaderDict={'BATH':0, 'EKIN':1, 'EKIN-MOL-TR':2,
                               'EKIN-MOL-IR':3, 'T':4, 'T-MOL-TR':5,
                               'T-MOL-IR':6, 'SCALE':7}
        self.mdStepHeaderDict={'STEP':0, 'TIME':1}

        cntrlNameList=getList_MetaStrInDict(self.metaDicts['cntrl'])
        filecntrlNameList=getList_MetaStrInDict(self.metaDicts['filecntrl'])
        fileNameList=getList_MetaStrInDict(self.metaDicts['file'])
        extraNameList=getList_MetaStrInDict(self.metaDicts['extra'])

        self.mdOutputSubParsers = [
            # MD TIMESTEP reader
            { "startReStr"        : r"^TIMESTEP\s*",
              "parser"            : "namelist_parser",
              "parsername"        : "md_step_parser",
              "waitlist"          : None,
              "stopOnMatchStr"    : r"^END\s*",
              "quitOnMatchStr"    : r"^END\s*",
              "metaNameStart"     : PARSERTAG + "_inout_control",
              "matchNameList"     : cntrlNameList,
              "matchNameDict"     : "mddataDict",
              "updateMatchDict"   : False,
              "onlyCaseSensitive" : False,
              "stopOnFirstLine"   : False,
              "parserOptions"     : {
                  #"lineFilter"       : None,
                  "makeOneLinerBetween" : [
                      [r"^TIMESTEP", r"^END", [["\n"], ["END"], ["TIMESTEP", "STEP TIME"]]]
                      ],
                  #"controlsections"  : ["section_single_configuration_calculation"],
                  #"controlsave"      : "sectioncontrol",
                  #"controldict"      : "stepcontrolDict",
                  }
              },
            # MD ENERGIES reader
            { "startReStr"        : r"^ENERGIES\s*",
              "parser"            : "namelist_parser",
              "parsername"        : "md_energy_parser",
              "waitlist"          : None,
              "stopOnMatchStr"    : r"^END\s*",
              "quitOnMatchStr"    : r"^END\s*",
              "metaNameStart"     : PARSERTAG + "_inout_control",
              "matchNameList"     : cntrlNameList,
              "matchNameDict"     : "mddataDict",
              "updateMatchDict"   : False,
              "onlyCaseSensitive" : False,
              "stopOnFirstLine"   : False,
              "parserOptions"     : {
                  "lineFilter"       : None,
                  #"controlsections"  : ["section_single_configuration_calculation"],
                  #"controlsave"      : "sectioncontrol",
                  #"controldict"      : "stepcontrolDict",
                  }
              },
            # MD TEMPERATURES reader
            { "startReStr"        : r"^TEMPERATURES\s*",
              "parser"            : "table_parser",
              "parsername"        : "md_temp_parser",
              "waitlist"          : [["md_energy_parser"]],
              "stopOnMatchStr"    : r"(?:^END|\s*-------------------)",
              "quitOnMatchStr"    : r"(?:^END|\s*-------------------)",
              "metaNameStart"     : PARSERTAG + "_mdout_",
              "matchNameList"     : mddataNameList,
              "matchNameDict"     : "mddataDict",
              "updateMatchDict"   : True,
              "onlyCaseSensitive" : False,
              "stopOnFirstLine"   : False,
              "parserOptions"     : {
                  "header"           : True,
                  "headerList"       : "mdTempHeaderDict",
                  "wrap"             : False,
                  "tablelines"       : 1,
                  "tablestartsat"    : r"\s*BATH\s*EKIN\s*",
                  "tableendsat"      : r"\s*--------------------",
                  "lineFilter"       : None,
                  "movetostopline"   : False,
                  "parsercntrlattr"  : "MDcurrentstep",
                  "parsercntrlin"    : "logsteps",
                  "lookupdict"       : "stepcontrolDict"
                  }
              },
            # thermostat save Parser
            { "startReStr"        : "AlwaysRun",
              "parser"            : "dictionary_parser",
              "parsername"        : "md_frameseq_step_parser",
              "waitlist"          : None,
              #"waitlist"          : [["md_step_parser"]],
              "stopOnMatchStr"    : "AlwaysStop",
              "quitOnMatchStr"    : "AlwaysStop",
              "metaNameStart"     : PARSERTAG + "_mdout_",
              "matchNameList"     : mddataNameList,
              "matchNameDict"     : "mddataDict",
              "updateMatchDict"   : True,
              "onlyCaseSensitive" : False,
              "stopOnFirstLine"   : False,
              "parserOptions"     : {
                  "dictionary"       : "stepcontrolDict",
                  "dicttype"         : "standard", # (standard or smartparser)
                  "readwritedict"    : "write",
                  "keyMapper"        : {"STEP" : "MDcurrentstep"},
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
            # Section Control Parser
            { "startReStr"        : "AlwaysRun",
              "parser"            : "section_control_parser",
              "parsername"        : "section_parser",
              "waitlist"          : [["md_step_parser"]],
              "stopOnMatchStr"    : "\s*FINAL\s*DATA\s*",
              "quitOnMatchStr"    : "\s*FINAL\s*DATA\s*",
              "metaNameStart"     : None,
              "matchNameList"     : None,
              "matchNameDict"     : None,
              "updateMatchDict"   : False,
              "onlyCaseSensitive" : True,
              "stopOnFirstLine"   : False,
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
            # Readline Control Parser
            { "startReStr"        : "AlwaysRun",
              "parser"            : "readline_control_parser",
              "parsername"        : "readline_parser",
              "waitlist"          : None,
              "stopOnMatchStr"    : "\s*FINAL\s*DATA\s*",
              "quitOnMatchStr"    : "\s*FINAL\s*DATA\s*",
              "metaNameStart"     : None,
              "matchNameList"     : None,
              "matchNameDict"     : None,
              "updateMatchDict"   : False,
              "onlyCaseSensitive" : True,
              "stopOnFirstLine"   : False,
              "parserOptions"     : {
                  "peeklineFirst"    : True,
                  "waitatlineStr"    : r"\s*TIMESTEP\s*",
                  "controlwait"      : None,
                  "controlattr"      : "MDcurrentstep",
                  "controlnextattr"  : "MDnextstep",
                  #"controllast"      : -1,
                  "controlskip"      : [],
                  "controlin"        : "steps",
                  "controlcounter"   : "targetstep",
                  "controldict"      : "stepcontrolDict",
                  "lookupdict"       : "stepcontrolDict"
                  }
              },
            ]

        outputSubParsers = [
            # MD++ header until topology reader
            { "startReStr"        : r"^(?:TITLE|output\s*file)\s*",
              "parser"            : "namelist_parser",
              "parsername"        : "md_title_parser",
              "waitlist"          : None,
              "stopOnMatchStr"    : r"^TOPOLOGY\s*",
              "quitOnMatchStr"    : r"^TOPOLOGY\s*",
              "metaNameStart"     : PARSERTAG + "_inout_control",
              "matchNameList"     : cntrlNameList,
              "matchNameDict"     : "topocntrlDict",
              "updateMatchDict"   : False,
              "onlyCaseSensitive" : False,
              "stopOnFirstLine"   : False,
              "parserOptions"     : {
                  "controlsections"  : ["x_gromos_section_control_parameters"],
                  "controlsave"      : "sectioncontrol",
                  "controldict"      : "stepcontrolDict",
                  }
              },
            # MD++ TOPOLOGY info reader
            { "startReStr"        : r"^TOPOLOGY\s*",
              "parser"            : "namelist_parser",
              "parsername"        : "md_topo_parser",
              "waitlist"          : None,
              "stopOnMatchStr"    : r"^END\s*",
              "quitOnMatchStr"    : r"^END\s*",
              "metaNameStart"     : PARSERTAG + "_inout_control",
              "matchNameList"     : cntrlNameList,
              "matchNameDict"     : "topocntrlDict",
              "updateMatchDict"   : False,
              "onlyCaseSensitive" : False,
              "stopOnFirstLine"   : False,
              "parserOptions"     : {
                  "makeOneLinerBetween" : [
                      [r"^MAKE_TOP\s*", r"^(?:Force-field\s*code|\s*RESNAME)\s*",
                          [["\n", " "]]],
                      [r"^COM_TOP\s*", r"^(?:Parameters\s*from|\s*RESNAME)\s*",
                          [["\n", " "]]],
                      [r"^\s*RESNAME", r"^\s*(?:END|ATOMTYPENAME|SOLUTEATOM)\s*",
                          [["\n", " "]]],
                      [r"^\s*ATOMTYPENAME", r"^\s*(?:END|SOLUTEATOM|CGSOLUTE)\s*",
                          [["\n", " "]]],
                      [r"^\s*SOLUTEATOM", r"^\s*(?:END|CGSOLUTE|LJEXCEPTIONS)\s*",
                          [["\n", " "]]],
                      [r"^\s*CGSOLUTE", r"^\s*(?:END|LJEXCEPTIONS|BOND)\s*",
                          [["\n", " "]]],
                      [r"^\s*LJEXCEPTIONS", r"^\s*(?:END|BOND)\s*",
                          [["\n", " "]]],
                      [r"^\s*BONDDP", r"^\s*(?:END|BONDANGLE|IMPDIHEDRAL)\s*",
                          [["\n", " "]]],
                      [r"^\s*BONDANGLE", r"^\s*(?:END|IMPDIHEDRAL|DIHEDRAL)\s*",
                          [["\n", " "]]],
                      [r"^\s*BOND", r"^\s*(?:END|BONDDP|BONDANGLE)\s*",
                          [["\n", " "]]],
                      [r"^\s*IMPDIHEDRAL", r"^\s*(?:END|DIHEDRAL|CROSSDIHEDRAL)\s*",
                          [["\n", " "]]],
                      [r"^\s*CROSSDIHEDRAL", r"^\s*(?:END|SOLVENT)\s*",
                          [["\n", " "]]],
                      [r"^\s*DIHEDRAL", r"^\s*(?:END|CROSSDIHEDRAL|SOLVENT)\s*",
                          [["\n", " "],["dihedrals", "propdihedrals"]]],
                      [r"^\s*SOLVENT", r"^\s*(?:END|SOLUTE)\s*",
                          [["\n", " "]]],
                      ],
                  "controlsections"  : ["x_gromos_section_control_parameters"],
                  "controlsave"      : "sectioncontrol",
                  "controldict"      : "stepcontrolDict",
                  }
              },
            # MD++ FORCEFIELD info reader
            { "startReStr"        : r"^FORCEFIELD\s*",
              "parser"            : "namelist_parser",
              "parsername"        : "md_ff_parser",
              "waitlist"          : None,
              "stopOnMatchStr"    : r"^END\s*",
              "quitOnMatchStr"    : r"^END\s*",
              "metaNameStart"     : PARSERTAG + "_inout_control",
              "matchNameList"     : cntrlNameList,
              "matchNameDict"     : "ffcntrlDict",
              "updateMatchDict"   : False,
              "onlyCaseSensitive" : False,
              "stopOnFirstLine"   : False,
              "parserOptions"     : {
                  "makeOneLinerBetween" : [
                      [r"^FORCEFIELD", r"^\s*(?:nonbonded\s*force|Pairlist\s*Algorithm)\s*",
                          [["\n", " "],
                           ["improper dihedral inter", "improper-dihedral-inter"],
                           ["dihedral interaction", "propdihedral_interaction"]]
                          ],
                      [r"^\s*cutoff", r"^\s*(?:pairlist\s*creation|REACTION\s*FIELD)\s*",
                          [["\n", " "],
                           ["shortrange cutoff      :", "shortrange-cutoff- :"],
                           ["longrange cutoff       :", "longrange-cutoff- :"]]
                          ],
                      [r"^\s*reactionfield\s*cutoff", r"^(?:\s*perturbation|END)\s*",
                          [["\n", " "],
                           ["reactionfield cutoff   :", "reactionfield-cutoff- :"],
                           ["reactionfield epsilon  :", "reactionfield-epsilon- :"]]
                          ],
                      ],
                  "controlsections"  : ["x_gromos_section_control_parameters"],
                  "controlsave"      : "sectioncontrol",
                  "controldict"      : "stepcontrolDict",
                  }
              },
            # MD++ header until topology reader
            { "startReStr"        : r"^MESSAGES\s*FROM\s*INITIALISATION\s*",
              "parser"            : "namelist_parser",
              "parsername"        : "md_init_parser",
              "waitlist"          : None,
              "stopOnMatchStr"    : r"^enter\s*the\s*next\s*level\s*",
              "quitOnMatchStr"    : r"^enter\s*the\s*next\s*level\s*",
              "metaNameStart"     : PARSERTAG + "_inout_control",
              "matchNameList"     : cntrlNameList,
              "matchNameDict"     : "filecntrlDict",
              "updateMatchDict"   : False,
              "onlyCaseSensitive" : False,
              "stopOnFirstLine"   : False,
              "parserOptions"     : {
                  "controlsections"  : ["x_gromos_section_control_parameters"],
                  "controlsave"      : "sectioncontrol",
                  "controldict"      : "stepcontrolDict",
                  }
              },
            # Section Control Parser
            { "startReStr"        : "AlwaysRun",
              "parser"            : "section_control_parser",
              "parsername"        : "control_section_parser",
              "waitlist"          : [["md_init_parser"]],
              "stopOnMatchStr"    : "AlwaysStop",
              "quitOnMatchStr"    : "AlwaysStop",
              "metaNameStart"     : None,
              "matchNameList"     : None,
              "matchNameDict"     : None,
              "updateMatchDict"   : False,
              "onlyCaseSensitive" : True,
              "stopOnFirstLine"   : False,
              "parserOptions"     : {
                  "sectionname"      : "x_gromos_section_control_parameters",
                  "sectionopen"      : True,
                  "sectionopenattr"  : "MDcurrentstep",
                  "sectionopenin"    : "cntrlparmstep",
                  "sectionclose"     : True,
                  "sectioncloseattr" : "MDcurrentstep",
                  "sectionclosein"   : "cntrlparmstep",
                  "activatesection"  : "sectioncontrol",
                  "lookupdict"       : "stepcontrolDict"
                  }
              },
            # MD LOOP Parser Caller
            { "startReStr"        : r"\s*MAIN\s*MD\s*LOOP\s*",
              "parser"            : "subparser_caller",
              "parsername"        : "command_subparser",
              "waitlist"          : None,
              "stopOnMatchStr"    : r"\s*FINAL\s*DATA\s*",
              "quitOnMatchStr"    : r"\s*FINAL\s*DATA\s*",
              "metaNameStart"     : None,
              "matchNameList"     : None,
              "matchNameDict"     : None,
              "updateMatchDict"   : False,
              "onlyCaseSensitive" : False,
              "stopOnFirstLine"   : False,
              "parserOptions"     : {
                  "onStartRunFunction" : None,
                  "onQuitRunFunction" : None,
                  "onlySubParsersReadLine" : True,
                  "waitFirstCycle" : True,
                  "subparserMapper"  : {
                      "MAIN MD LOOP"    : "mdOutputSubParsers",
                      },
                  "subparserSection" : {
                      "MAIN MD LOOP"    : ["section_run", "auto", "secRunOpen", "secRunGIndex"],
                      },
                  }
              },
            # Readline Control Parser
            { "startReStr"        : "AlwaysRun",
              "parser"            : "readline_control_parser",
              "parsername"        : "readline_parser",
              "waitlist"          : None,
              #"stopOnMatchStr"    : "\s*GROMOS>\s*",
              #"quitOnMatchStr"    : "\s*GROMOS>\s*",
              "stopOnMatchStr"    : r"\s*(?:TIMING|Overall\s*time\s*used:)\s*",
              "quitOnMatchStr"    : r"\s*(?:TIMING|Overall\s*time\s*used:)\s*",
              "metaNameStart"     : None,
              "matchNameList"     : None,
              "matchNameDict"     : None,
              "updateMatchDict"   : False,
              "onlyCaseSensitive" : False,
              "stopOnFirstLine"   : False,
              "parserOptions"     : {
                  "peeklineFirst"    : True,
                  "waitatlineStr"    : "\s*TIMESTEP\s*",
                  "controlwait"      : None,
                  "controlattr"      : "MDcurrentstep",
                  #"controlnextattr"  : "MDnextstep",
                  #"controllast"      : -1,
                  "controlskip"      : [-1],
                  "controlin"        : "opencntrlstep",
                  #"controlcounter"   : "targetstep",
                  #"controldict"      : "stepcontrolDict",
                  #"lookupdict"       : "stepcontrolDict"
                  }
              },
            ]

        ########################################
        # return main Parser
        return [
            SM(name='MainRun',
                startReStr=r"^MD\+\+\s*",
                endReStr=r"^MD\+\+\s*finished\s*",
                repeats=True,
                required=True,
                #forwardMatch=True,
                sections=['section_run'],
                fixedStartValues={'program_name': PROGRAMNAME},
                subMatchers=[
                    SM(name='ProgramInfo',
                        startReStr=r"\s*version\s*:\s*"
                                   "(?P<"+PARSERTAG+"_mdin_finline>[a-zA-Z0-9:., ]+)\s*",
                       adHoc=lambda p: p.backend.addValue(
                           "program_version",
                           ' '.join(p.lastMatch[
                               PARSERTAG+"_mdin_finline"
                               ].replace('\n', ' ').strip().split()))),
                    #SM(name='logruninfo',
                    #    startReStr=r"\s*build\s*date\s*:\s*"
                    #               "(?P<"+PARSERTAG+"_mdin_finline>"
                    #               "[a-zA-Z0-9/:. ]+)\s*",
                    #   adHoc=lambda p: p.backend.addValue(
                    #       "time_run_date_start", datetime.datetime.strptime(
                    #           p.lastMatch[PARSERTAG+"_mdin_finline"].strip(),
                    #           '%a %b %d %H:%M:%S %Z %Y').timestamp())),
                    SM(startReStr=r"\s*Debugging\s*is\s*(?:disabled|enabled)\s*"),
                    SM(name='license',
                       startReStr=r"\s*Gruppe\s*fuer\s*",
                       coverageIgnore=True,
                       adHoc=lambda p:
                       self.adHoc_read_store_text_stop_parsing(p,
                           stopOnMatchStr=r"\s*(?:Bugreports|Running)\s*",
                           quitOnMatchStr=None,
                           metaNameStart=PARSERTAG+"_",
                           metaNameStore=PARSERTAG+"_program_copyright",
                           matchNameList=None,
                           matchNameDict=None,
                           onlyCaseSensitive=True,
                           stopOnFirstLine=False,
                           storeFirstLine=True,
                           storeStopQuitLine=True,
                           onQuitRunFunction=lambda p: p.backend.addValue(
                               PARSERTAG+"_program_copyright",
                               ' '.join(p.lastMatch[
                                   PARSERTAG+"_program_copyright"
                                   ].replace('\n', ' ').strip().split())
                               )
                           )
                       ),
                    SM(name='loghostinfo',
                       startReStr=r"\s*Running\s*on\s*"
                                   "(?P<"+PARSERTAG+"_mdin_finline>.*)\s*",
                       adHoc=lambda p: p.backend.addValue(
                           PARSERTAG+"_build_osarch",
                           ' '.join(p.lastMatch[
                               PARSERTAG+"_mdin_finline"
                               ].replace('\n', ' ').strip().split()))),
                    SM(name='newRun',
                       startReStr=r"\s*(?:TITLE|output\s*file)\s*",
                       endReStr=r"\s*(?:TIMING|Overall\s*time\s*used:)\s*",
                       forwardMatch=True,
                       adHoc=lambda p:
                       self.adHoc_takingover_parsing(p,
                           stopOnMatchStr=r"\s*(?:TIMING|Overall\s*time\s*used:)\s*",
                           quitOnMatchStr=r"\s*(?:TIMING|Overall\s*time\s*used:)\s*",
                           #onStartRunFunction=self.saveInputControlFiles(p),
                           #onStartRunFunction=self.textFileFoundInDir,
                           #onStartRunFunction=self.findInputCmdFile,
                           stopControl="stopControl", # if None or True, stop with quitMatch, else wait
                           record=False, # if False or None, no record, no replay
                           replay=0, # if 0 or None= no replay, if <0 infinite replay
                           #onStartReplayRunFunction={1:"guessInputCmdsFromOutput"},
                           #onStartReplayRunFunction={1:"findInputCmdFile"},
                           #onQuitReplayRunFunction={1:self.textFileFoundInDir},
                           parseOnlyRecorded=False, # if True, parsers only work on record
                           ordered=False,
                           onlySubParsersReadLine=True,
                           subParsers=outputSubParsers)),
                           #onQuitRunFunction=self.guessInputCmdsFromOutput,
                           #onQuitRunFunction=lambda p: [
                           #    sys.stdout.write(
                           #        "Line %d: %s" % (i, line.replace('GROMOS>', ''))
                           #        ) for i,line in enumerate(self.recordList) if 'GROMOS>' in line
                           #    ],
                           #onQuitRunFunction=lambda p: [sys.stdout.write("%s" % (line)) for i,line in enumerate(self.recordList)])),
                           #onQuitRunFunction=lambda p: [sys.stdout.write("Line %d: %s" % (i, line)) for i,line in enumerate(self.recordList)])),
                    SM(name='CPUtime',
                       startReStr=r"\s*Overall\s*time\s*used:\s*(?P<time_run_cpu1_end>[0-9:.eEdD]+)"),
                    #SM(name='Walldate',
                    #   startReStr=r"^\(initialisation\s*took\s*",
                    #   coverageIgnore=True,
                    #   adHoc=lambda p:
                    #   self.adHoc_read_store_text_stop_parsing(p,
                    #       stopOnMatchStr=r"^[MTWFS]+.*[0-9]+$",
                    #       quitOnMatchStr=r"^[MTWFS]+.*[0-9]+$",
                    #       metaNameStart=PARSERTAG+"_",
                    #       metaNameStore=PARSERTAG+"_mdin_finline",
                    #       matchNameList=None,
                    #       matchNameDict=None,
                    #       onlyCaseSensitive=True,
                    #       stopOnFirstLine=False,
                    #       storeFirstLine=True,
                    #       storeStopQuitLine=True,
                    #       onQuitRunFunction=lambda p: p.backend.addValue(
                    #           "time_run_wall_end",
                    #           datetime.datetime.strptime(
                    #           ' '.join(p.lastMatch[
                    #               PARSERTAG+"_mdin_finline"
                    #               ].replace('\n', ' ').strip().split()[-5:]),
                    #           '%a %b %d %H:%M:%S %Y').timestamp()
                    #           )
                    #       )
                    #   ),
                    SM(name='end_run',
                       startReStr=r"\s*MD\+\+\s*finished\s*successfully\s*",
                       adHoc=lambda p: p.backend.addValue("run_clean_end",True)),
                    # END Timings
                ]) # END MainRun
            ]


class GromacsParserInterface():
   """ A proper class envolop for running this parser from within python. """
   def __init__(self, backend, **kwargs):
       self.backend_factory = backend

   def parse(self, mainfile):
        from unittest.mock import patch
        logging.info('gromos parser started')
        logging.getLogger('nomadcore').setLevel(logging.WARNING)
        backend = self.backend_factory("gromos.nomadmetainfo.json")
        parserInfo = {'name': 'gromos-parser', 'version': '1.0'}
        context = GROMOSParser()
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
    parser = GROMOSParser()
    parser.parse()
