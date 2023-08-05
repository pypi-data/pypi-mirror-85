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
from .TINKERDictionary import get_updateDictionary, set_Dictionaries
from .TINKERCommon import PARSERNAME, PROGRAMNAME, PARSERVERSION, PARSERTAG, LOGGER
from .TINKERCommon import PARSER_INFO_DEFAULT, META_INFO_PATH, set_excludeList, set_includeList
from nomadcore.md_data_access import MDDataAccess as MDDA
#from nomadcore.md_data_access.MDDataAccess import is_file_binary, is_binary_string
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
# This is the parser for the main file of TINKER.
############################################################

parser = None

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

class TINKERParser(SmartParser.ParserBase):
    """Context for parsing TINKER main file.

    This class keeps tracks of several TINKER settings to adjust the parsing to them.
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
        self.tinkerBaseName = None
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
        self.MDreadstep = 0
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
        self.MDreadstep = 0
        self.MDnextstep = 0
        self.cntrlparmstep = [-1]
        self.opencntrlstep = [-1]
        self.samplingstep = 0
        self.singleConfCalcs = []
        self.lastCalculationGIndex = None
        self.inputCntrlFile = None
        set_Dictionaries(self)
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
        the TINKER output from the parsed log output,
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

    def parameter_file_name(self, cntrldict, itemdict):
        """ Function to generate data for parameter files list
        """
        working_dir_name = os.path.dirname(os.path.normpath(os.path.abspath(self.fName)))
        parmmeta = isMetaStrInDict("parameters",self.cntrlDict)
        filename = []
        if parmmeta is not None:
            if self.cntrlDict[parmmeta].value is not None:
                fname = self.cntrlDict[parmmeta].value
                filename.append(fname.replace(working_dir_name, '.'+os.path.sep))
        if filename:
            return False, filename, itemdict
        else:
            return False, None, itemdict

    def tinker_input_output_files(self, backend, gIndex, section, call_level):
        """Called with onClose_x_tinker_section_control_parameters to setup
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

        #inputOK = self.findInputCmdFileAndRead(parser)


        # Here we update topology info
        # Check if topology files can be loaded
        self.newTopo = False
        self.newIncoord=False
        self.newOutcoord=False
        topoDone=False
        IncoordDone=False
        OutcoordDone=False
        topoFile = self.findFileInDir(parser, "topology file", "filecntrlDict")
        #confFile = self.findFileInDir(parser, "configuration file", "filecntrlDict")
        inconfFile = self.findFileInDir(parser, "initial configuration file", "filecntrlDict")
        outcoorFile = self.findFileInDir(parser, "restart file", "filecntrlDict")
        outconfFile = self.findFileInDir(parser, "final configuration file", "filecntrlDict")
        arcFile = self.findFileInDir(parser, "archive file", "filecntrlDict")
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
                self.newIncoord=True

        if inconfFile is not None:
            if inconfFile.upper() in self.filesInOutputDir:
                file_name = self.filesInOutputDir[inconfFile.upper()]
                self.fileDict[fKey+'input_coord'].value = file_name.replace(
                        working_dir_name+os.path.sep, '')
                self.fileDict[fKey+'input_coord'].fileName = file_name
                self.fileDict[fKey+'input_coord'].activeInfo = True
                self.fileDict[fKey+'input_coord'].fileSupplied = True
                atLeastOneFileExist = True
                IncoordDone = True
                self.newIncoord=True

        if outconfFile is not None:
            if outconfFile.upper() in self.filesInOutputDir:
                file_name = self.filesInOutputDir[outconfFile.upper()]
                self.fileDict[fKey+'output_coord'].value = file_name.replace(
                        working_dir_name+os.path.sep, '')
                self.fileDict[fKey+'output_coord'].fileName = file_name
                self.fileDict[fKey+'output_coord'].activeInfo = True
                self.fileDict[fKey+'output_coord'].fileSupplied = True
                atLeastOneFileExist = True
                OutcoordDone = True
                self.newOutcoord=True

        if OutcoordDone is False:
            if outcoorFile is not None:
                if outcoorFile.upper() in self.filesInOutputDir:
                    file_name = self.filesInOutputDir[outcoorFile.upper()]
                    self.fileDict[fKey+'output_coord'].value = file_name.replace(
                            working_dir_name+os.path.sep, '')
                    self.fileDict[fKey+'output_coord'].fileName = file_name
                    self.fileDict[fKey+'output_coord'].activeInfo = True
                    self.fileDict[fKey+'output_coord'].fileSupplied = True
                    atLeastOneFileExist = True
                    OutcoordDone = True
                    self.newOutcoord=True

        self.newTraj = False
        trajDone=False
        if arcFile is not None:
            file_name = arcFile
            self.fileDict[fKey+'trajectory'].value = file_name.replace(
                    working_dir_name+os.path.sep, '')
            self.fileDict[fKey+'trajectory'].fileName = file_name
            self.fileDict[fKey+'trajectory'].activeInfo = True
            self.fileDict[fKey+'trajectory'].fileSupplied = True
            atLeastOneFileExist = True
            trajDone = True
            self.newTraj = True

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
        if self.newOutcoord:
            if OutcoordDone and atLeastOneFileExist:
                self.MDData.initializeInputCoordinateFileHandlers(self)
                if self.outputcoords:
                    self.outputpositions = self.outputcoords.positions()
                    self.numatoms = len(self.outputpositions)
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
        return atLeastOneFileExist

    def onOpen_x_tinker_section_control_parameters(self, backend, gIndex, section):
        # keep track of the latest section
        if self.inputControlIndex is None:
            self.inputControlIndex = gIndex

    def onClose_x_tinker_section_control_parameters(self, backend, gIndex, section):
        # Find input and output files. Read input control parameters
        atLeastOneFileExist = self.tinker_input_output_files(backend, gIndex, section, "control")
        section_control_Dict = {}
        section_control_Dict.update(self.mdcntrlDict)
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

        #if atLeastOneFileExist:
        #    secIOGIndex = backend.openSection(PARSERTAG+'_section_input_output_files')
        #    updateFileDict = {
        #            'startSection'   : [[PARSERTAG+'_section_input_output_files']],
        #            'dictionary'     : self.fileDict
        #            }
        #    self.metaStorage.update(updateFileDict)
        #    self.metaStorage.updateBackend(backend.superBackend,
        #            startsection=[PARSERTAG+'_section_input_output_files'],
        #            autoopenclose=False)
        #    backend.closeSection(PARSERTAG+'_section_input_output_files', secIOGIndex)

        # TINKER prints the initial and final energies to the log file.
        if self.MDcurrentstep < 0:
            self.MDcurrentstep += 1
            self.MDcurrentstep = int(self.MDcurrentstep)
        self.stepcontrolDict.update({"MDcurrentstep" : int(self.MDcurrentstep)})
        nsteps = 0
        nlogsteps = 0
        nstructstep = 0
        ninputstep = 0
        noutputstep = 0
        ntrajsteps = 0
        nvelsteps = 0
        nforcesteps = 0
        filesteps = None
        filefreq = None
        numSecRun = str(self.secRunGIndex)

        if self.secRunGIndex in self.fileUnitDict:
            if 'filesteps' in self.fileUnitDict[self.secRunGIndex]:
                filesteps = self.fileUnitDict[self.secRunGIndex]['filesteps']
                if len(filesteps)>0:
                    filefreq = filesteps[0]

        nstructKey = isMetaStrInDict("topology file",self.filecntrlDict)
        ninputKey = isMetaStrInDict("initial configuration file",self.filecntrlDict)
        nxoutKey = isMetaStrInDict("archive file",self.filecntrlDict)
        if nxoutKey is None:
            nxoutKey = isMetaStrInDict("initial trajectory file",self.filecntrlDict)
        noutputKey = isMetaStrInDict("final configuration file",self.filecntrlDict)
        #nminstepKey = isMetaStrInDict("EMIN-NMIN", self.cntrlDict)
        nstepKey = isMetaStrInDict("NSTEP", self.cntrlDict)
        nlogKey = isMetaStrInDict("PRINTOUT", self.cntrlDict)
        if nstepKey is not None:
            if self.cntrlDict[nstepKey].activeInfo:
                nsteps = conv_int(self.cntrlDict[nstepKey].value, default=0)
            else:
                #nsteps = conv_int(self.cntrlDict[nstepKey].defaultValue, default=0)
                nsteps = 0
        #if nminstepKey is not None:
        #    if self.cntrlDict[nminstepKey].activeInfo:
        #        self.MD = False
        #        nsteps = conv_int(self.cntrlDict[nminstepKey].value, default=0)
        if nlogKey is not None:
            if self.cntrlDict[nlogKey].activeInfo:
                nlogsteps = conv_int(self.cntrlDict[nlogKey].value, default=1)
            else:
                nlogsteps = 1
        else:
            nlogsteps = 1
        #if nxoutKey is not None:
        #    if self.cntrlDict[nxoutKey].activeInfo:
        #        ntrajsteps = conv_int(self.cntrlDict[nxoutKey].value, default=0)
        if nstructKey is not None:
            if self.filecntrlDict[nstructKey].activeInfo:
                nstructstep = 1
        if ninputKey is not None:
            if self.filecntrlDict[ninputKey].activeInfo:
                ninputstep = 1
        if noutputKey is not None:
            if self.filecntrlDict[noutputKey].activeInfo:
                noutputstep = 1

        if nlogsteps>0:
            logsteps = [i for i in range(1, nsteps, nlogsteps)]
            logsteps.append(nsteps)
        else:
            logsteps = [1, nsteps]
            #logsteps.append(nsteps)
        trajsteps = []
        if filesteps is not None:
            if(ninputstep>0 or nstructstep>0):
                if 1 not in filesteps:
                    trajsteps.append(1)
                    rtn = setMetaStrInDict(self, 'mddataDict', 'InputCoordStep', int(1))
            for trjs in filesteps:
                trajsteps.append(trjs)
            if noutputstep>0:
                if nsteps not in filesteps:
                    trajsteps.append(nsteps)
                    rtn = setMetaStrInDict(self, 'mddataDict', 'OutputCoordStep', int(nsteps))
        else:
            if(ninputstep>0 or nstructstep>0):
                trajsteps.append(1)
                rtn = setMetaStrInDict(self, 'mddataDict', 'InputCoordStep', int(1))
            if noutputstep>0:
                trajsteps.append(nsteps)
                rtn = setMetaStrInDict(self, 'mddataDict', 'OutputCoordStep', int(nsteps))

        #if ntrajsteps>0:
        #    trajsteps = [i for i in range(1, nsteps, ntrajsteps)]
        #    trajsteps.append(nsteps)
        #else:
        #    trajsteps = []
        #    if(ninputstep>0 or nstructstep>0):
        #        trajsteps.append(0)
        #    if noutputstep>0:
        #        trajsteps.append(nsteps)
        if nvelsteps>0:
            velsteps = [i for i in range(1, nsteps, nvelsteps)]
            velsteps.append(nsteps)
        else:
            velsteps = []
            #velsteps.append(nsteps)
        if nforcesteps>0:
            forcesteps = [i for i in range(1, nsteps, nforcesteps)]
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
        for step in range(1,nsteps+1):
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
        parmmeta = isMetaStrInDict("parameters",self.cntrlDict)
        if parmmeta is not None:
            if self.cntrlDict[parmmeta].value is not None:
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

        # TINKER default unit vectors. If all are zeros than the simulation cell is not periodic.
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
            # TINKER Guide says: (See http://www.ks.uiuc.edu/Research/tinker/2.12/ug/node11.html)
            # Positions in PDB/TINKER binary/DCD files are stored in A.
            #pos_obj = getattr(self.trajectory, 'positions', None)
            #if callable(pos_obj):
            SloppyBackend.addArrayValues('atom_positions', np.transpose(np.asarray(
                self.metaStorage.convertUnits(positions, "nano-meter", self.unitDict))))
            if coordinates.velocities is not None:
                # Velocities in PDB files are stored in A/ps units.(PDB files are read for input
                #     coordinates, velocities, and forces)
                # Velocities in TINKER binary/DCD files are stored in TINKER internal units and must be multiplied
                #     by PDBVELFACTOR=20.45482706 to convert to A/ps. (These files are used for output trajectory)
                SloppyBackend.addArrayValues('atom_velocities', np.transpose(np.asarray(
                    self.metaStorage.convertUnits(
                        coordinates.velocities, "(nano-meter)/(pico-second)", self.unitDict))))
                # need to transpose array since its shape is [number_of_atoms,3] in the metadata

            if self.topology is not None:
                atom_labels = self.topoDict["atom_element_list"]
                numatoms = len(atom_labels)
                self.numatoms
                SloppyBackend.addArrayValues('atom_labels', np.asarray(atom_labels))
                pass
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
            #updateDictVDW = {
            #    'startSection' : [
            #        ['section_energy_van_der_Waals']],
            #    #'muteSections' : [['section_sampling_method']],
            #    'dictionary' : section_singlevdw_Dict
            #    }
            #self.secVDWGIndex = backend.superBackend.openSection("section_energy_van_der_Waals")
            #self.metaStorage.update(updateDictVDW)
            #self.metaStorage.updateBackend(backend.superBackend,
            #        startsection=['section_energy_van_der_Waals'],
            #        autoopenclose=False)
            #backend.superBackend.closeSection("section_energy_van_der_Waals", self.secVDWGIndex)
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
                # Forces in PDB/TINKER binary/DCD files are stored in kcal/mol/A
                SloppyBackend.addArrayValues('atom_forces', np.transpose(np.asarray(
                    self.metaStorage.convertUnits(
                        self.atompositions.velocities, "kilo-joule/(mol*nano-meter)", self.unitDict))))
                # need to transpose array since its shape is [number_of_atoms,3] in the metadata
        if(self.MDcurrentstep in trajsteps or
           self.MDcurrentstep in velsteps):
            trajfile = None
            if 'filetrajs' in self.fileUnitDict[self.secRunGIndex]:
                filetrajs = self.fileUnitDict[self.secRunGIndex]['filetrajs']
                if self.MDcurrentstep in filetrajs:
                    trajfile = filetrajs[self.MDcurrentstep]
            if trajfile is not None:
                rtn = setMetaStrInDict(self, 'filecntrlDict', 'archive file', trajfile)
                self.tinker_input_output_files(backend, gIndex, section, "traj")

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

    def trueToZero(self, fname, value):
        keyMapper = {
                "Molecular Dynamics" : "MDmainstep",
                "Optimization" : "MDmainstep",
                }
        if value is not None:
            for k,v in keyMapper.items():
                if fname in k:
                    return int(0)
        return value

    def convertInt(self, fname, value):
        keyMapper = {
                "MD Step"        : "MDcurrentstep",
                "Dynamics Steps" : "MDcurrentstep",
                "VM Iter"        : "MDcurrentstep",
                "TN Iter"        : "MDcurrentstep",
                "QN Iter"        : "MDcurrentstep",
                "CG Iter"        : "MDcurrentstep",
                }
        if value is not None:
            for k,v in keyMapper.items():
                if fname in k:
                    if isinstance(value, str):
                        if 'D' in value.upper():
                            value = value.replace('D', 'E').replace('d', 'E')
                    try:
                        return int(value)
                    except ValueError:
                        pass
        return value

    def convertFloat(self, fname, value):
        keyMapper = {
                "F Value"        : "E Potential",
                }
        if value is not None:
            for k,v in keyMapper.items():
                if fname in k:
                    if isinstance(value, str):
                        if 'D' in value.upper():
                            value = value.replace('D', 'E').replace('d', 'E')
                    try:
                        return float(value)
                    except ValueError:
                        pass
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

    def checkTinkerParam(self, cmdLine, prmName):
        try:
            prm = cmdLine.split()[-1]
            if "NONE" in prm.upper() or prmName.upper() in prm.upper():
                prm = None
            else:
                prm = ' '.join(cmdLine.split()[1:])
        except ValueError:
            prm = None
        return prm

    def readTinkerParameterFile(self, parser, fileName, cntrlDict):
        success = False
        emptyLine = re.compile(r"^\s*$")
        atom=[]
        vdw=[]
        bond=[]
        angle=[]
        dihedral=[]
        improper=[]
        ureybond=[]
        charge=[]
        mutate=[]
        if fileName is not None:
            with open(fileName, 'r') as fin:
                for line in fin:
                    prm = None
                    if emptyLine.findall(line):
                        continue
                    cmdLine = ' '.join([x for x in line.strip().split() if x])
                    cmdLineUp = cmdLine.upper()
                    if cmdLine.startswith('#') or cmdLine.startswith('echo'):
                        continue
                    elif cmdLineUp.startswith('PARAMETERS'):
                        prm = self.checkTinkerParam(cmdLine, 'parameters')
                        rtn = setMetaStrInDict(self, 'cntrlDict', 'parameters', prm)
                        success = rtn[0] if success is False else True
                        continue
                    elif cmdLineUp.startswith('VERBOSE'):
                        rtn = setMetaStrInDict(self, 'cntrlDict', 'verbose', True)
                        success = rtn[0] if success is False else True
                        continue
                    elif cmdLineUp.startswith('ARCHIVE'):
                        rtn = setMetaStrInDict(self, 'cntrlDict', 'archive', True)
                        success = rtn[0] if success is False else True
                        continue
                    elif cmdLineUp.startswith('LIGHTS'):
                        rtn = setMetaStrInDict(self, 'cntrlDict', 'lights', True)
                        success = rtn[0] if success is False else True
                        continue
                    elif cmdLineUp.startswith('SADDLEPOINT'):
                        rtn = setMetaStrInDict(self, 'cntrlDict', 'saddlepoint', True)
                        success = rtn[0] if success is False else True
                        continue
                    elif cmdLineUp.startswith('ENFORCE-CHIRALITY'):
                        rtn = setMetaStrInDict(self, 'cntrlDict', 'enforce-chirality', True)
                        success = rtn[0] if success is False else True
                        continue
                    elif cmdLineUp.startswith('NEIGHBOR-LIST'):
                        rtn = setMetaStrInDict(self, 'cntrlDict', 'neighbor-list', True)
                        success = rtn[0] if success is False else True
                        continue
                    elif cmdLineUp.startswith('PRINTOUT'):
                        prm = self.checkTinkerParam(cmdLine, 'printout')
                        rtn = setMetaStrInDict(self, 'cntrlDict', 'printout', prm)
                        success = rtn[0] if success is False else True
                        continue
                    elif cmdLineUp.startswith('DIGITS'):
                        prm = self.checkTinkerParam(cmdLine, 'digits')
                        rtn = setMetaStrInDict(self, 'cntrlDict', 'digit', prm)
                        success = rtn[0] if success is False else True
                        continue
                    elif cmdLineUp.startswith('SPACEGROUP'):
                        prm = self.checkTinkerParam(cmdLine, 'spacegroup')
                        rtn = setMetaStrInDict(self, 'cntrlDict', 'spacegroup', prm)
                        success = rtn[0] if success is False else True
                        continue
                    elif cmdLineUp.startswith('VDWTYPE'):
                        prm = self.checkTinkerParam(cmdLine, 'vdwtype')
                        rtn = setMetaStrInDict(self, 'cntrlDict', 'vdwtype', prm)
                        success = rtn[0] if success is False else True
                        continue
                    elif cmdLineUp.startswith('VDW-CUTOFF'):
                        prm = self.checkTinkerParam(cmdLine, 'vdw-cutoff')
                        rtn = setMetaStrInDict(self, 'cntrlDict', 'vdw-cutoff', prm)
                        success = rtn[0] if success is False else True
                        continue
                    elif cmdLineUp.startswith('VDW-CORRECTION'):
                        rtn = setMetaStrInDict(self, 'cntrlDict', 'vdw-correction', True)
                        success = rtn[0] if success is False else True
                        continue
                    elif cmdLineUp.startswith('EWALD'):
                        rtn = setMetaStrInDict(self, 'cntrlDict', 'ewald', True)
                        success = rtn[0] if success is False else True
                        continue
                    elif cmdLineUp.startswith('ANISO-PRESSURE'):
                        rtn = setMetaStrInDict(self, 'cntrlDict', 'aniso-pressure', True)
                        success = rtn[0] if success is False else True
                        continue
                    elif cmdLineUp.startswith('EWALD-CUTOFF'):
                        prm = self.checkTinkerParam(cmdLine, 'ewald-cutoff')
                        rtn = setMetaStrInDict(self, 'cntrlDict', 'ewald-cutoff', prm)
                        success = rtn[0] if success is False else True
                        continue
                    elif cmdLineUp.startswith('PME-GRID'):
                        prm = self.checkTinkerParam(cmdLine, 'pme-grid')
                        if prm is not None:
                            prm = ','.join(prm.split())
                        rtn = setMetaStrInDict(self, 'cntrlDict', 'pme-grid', prm)
                        success = rtn[0] if success is False else True
                        continue
                    elif cmdLineUp.startswith('PME-ORDER'):
                        prm = self.checkTinkerParam(cmdLine, 'pme-order')
                        rtn = setMetaStrInDict(self, 'cntrlDict', 'pme-order', prm)
                        success = rtn[0] if success is False else True
                        continue
                    elif cmdLineUp.startswith('RADIUSRULE'):
                        prm = self.checkTinkerParam(cmdLine, 'radiusrule')
                        rtn = setMetaStrInDict(self, 'cntrlDict', 'radiusrule', prm)
                        success = rtn[0] if success is False else True
                        continue
                    elif cmdLineUp.startswith('RADIUSRULE'):
                        prm = self.checkTinkerParam(cmdLine, 'radiusrule')
                        rtn = setMetaStrInDict(self, 'cntrlDict', 'radiusrule', prm)
                        success = rtn[0] if success is False else True
                        continue
                    elif cmdLineUp.startswith('RADIUSTYPE'):
                        prm = self.checkTinkerParam(cmdLine, 'radiustype')
                        rtn = setMetaStrInDict(self, 'cntrlDict', 'radiustype', prm)
                        success = rtn[0] if success is False else True
                        continue
                    elif cmdLineUp.startswith('RADIUSSIZE'):
                        prm = self.checkTinkerParam(cmdLine, 'radiussize')
                        rtn = setMetaStrInDict(self, 'cntrlDict', 'radiussize', prm)
                        success = rtn[0] if success is False else True
                        continue
                    elif cmdLineUp.startswith('EPSILONRULE'):
                        prm = self.checkTinkerParam(cmdLine, 'epsilonrule')
                        rtn = setMetaStrInDict(self, 'cntrlDict', 'epsilonrule', prm)
                        success = rtn[0] if success is False else True
                        continue
                    elif cmdLineUp.startswith('DIELECTRIC'):
                        prm = self.checkTinkerParam(cmdLine, 'dielectric')
                        rtn = setMetaStrInDict(self, 'cntrlDict', 'dielectric', prm)
                        success = rtn[0] if success is False else True
                        continue
                    elif cmdLineUp.startswith('A-AXIS'):
                        prm = self.checkTinkerParam(cmdLine, 'a-axis')
                        rtn = setMetaStrInDict(self, 'cntrlDict', 'a-axis', prm)
                        success = rtn[0] if success is False else True
                        continue
                    elif cmdLineUp.startswith('B-AXIS'):
                        prm = self.checkTinkerParam(cmdLine, 'b-axis')
                        rtn = setMetaStrInDict(self, 'cntrlDict', 'b-axis', prm)
                        success = rtn[0] if success is False else True
                        continue
                    elif cmdLineUp.startswith('C-AXIS'):
                        prm = self.checkTinkerParam(cmdLine, 'c-axis')
                        rtn = setMetaStrInDict(self, 'cntrlDict', 'c-axis', prm)
                        success = rtn[0] if success is False else True
                        continue
                    elif cmdLineUp.startswith('ALPHA'):
                        prm = self.checkTinkerParam(cmdLine, 'alpha')
                        rtn = setMetaStrInDict(self, 'cntrlDict', 'alpha', prm)
                        success = rtn[0] if success is False else True
                        continue
                    elif cmdLineUp.startswith('BETA'):
                        prm = self.checkTinkerParam(cmdLine, 'beta')
                        rtn = setMetaStrInDict(self, 'cntrlDict', 'beta', prm)
                        success = rtn[0] if success is False else True
                        continue
                    elif cmdLineUp.startswith('GAMMA'):
                        prm = self.checkTinkerParam(cmdLine, 'gamma')
                        rtn = setMetaStrInDict(self, 'cntrlDict', 'gamma', prm)
                        success = rtn[0] if success is False else True
                        continue
                    elif cmdLineUp.startswith('INTEGRATOR'):
                        prm = self.checkTinkerParam(cmdLine, 'integrator')
                        rtn = setMetaStrInDict(self, 'cntrlDict', 'integrator', prm)
                        success = rtn[0] if success is False else True
                        continue
                    elif cmdLineUp.startswith('BAROSTAT'):
                        prm = self.checkTinkerParam(cmdLine, 'barostat')
                        rtn = setMetaStrInDict(self, 'cntrlDict', 'barostat', prm)
                        success = rtn[0] if success is False else True
                        continue
                    elif cmdLineUp.startswith('TAU-PRESSURE'):
                        prm = self.checkTinkerParam(cmdLine, 'tau-pressure')
                        rtn = setMetaStrInDict(self, 'cntrlDict', 'tau-pressure', prm)
                        success = rtn[0] if success is False else True
                        continue
                    elif cmdLineUp.startswith('TAU-TEMPERATURE'):
                        prm = self.checkTinkerParam(cmdLine, 'tau-temperature')
                        rtn = setMetaStrInDict(self, 'cntrlDict', 'tau-temperature', prm)
                        success = rtn[0] if success is False else True
                        continue
                    elif cmdLineUp.startswith('RATTLE'):
                        prm = self.checkTinkerParam(cmdLine, 'rattle')
                        rtn = setMetaStrInDict(self, 'cntrlDict', 'rattle', prm)
                        success = rtn[0] if success is False else True
                        continue
                    elif cmdLineUp.startswith('LAMBDA'):
                        prm = self.checkTinkerParam(cmdLine, 'lambda')
                        rtn = setMetaStrInDict(self, 'cntrlDict', 'lambda', prm)
                        success = rtn[0] if success is False else True
                        continue
                    elif cmdLineUp.startswith('POLAR-EPS'):
                        prm = self.checkTinkerParam(cmdLine, 'polar-eps')
                        rtn = setMetaStrInDict(self, 'cntrlDict', 'polar-eps', prm)
                        success = rtn[0] if success is False else True
                        continue
                    elif cmdLineUp.startswith('VIB-ROOTS'):
                        prm = self.checkTinkerParam(cmdLine, 'vib-roots')
                        rtn = setMetaStrInDict(self, 'cntrlDict', 'vib-roots', prm)
                        success = rtn[0] if success is False else True
                        continue
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

    def generateARCfileFromSequenceFiles(self, parser, fileListInDir, arcname):
        xyzSeqList = []
        working_dir_name = os.path.dirname(os.path.abspath(self.fName))
        addfile = os.path.normpath(working_dir_name+os.path.sep+arcname)
        for fname in self.tinkerFiles:
            if('.arc' not in fname and
               '.xyz' not in fname and
               fname in fileListInDir):
                xyzSeqList.append(working_dir_name+os.path.sep+fname)
        anyFileExist=False
        for fname in xyzSeqList:
            with open(fname, 'rb') as fin:
                if fin.read():
                    anyFileExist=True
                    fin.close()
        if anyFileExist:
            with open(addfile, 'wb') as fout:
                for fname in xyzSeqList:
                    with open(fname, 'rb') as fin:
                        fout.write(fin.read())

    def fetchInfoFromInputOutput(self, parser):
        self.recordList.write('   #######################################   ')
        working_dir_name = os.path.dirname(os.path.abspath(self.fName))
        fileList = [x for x in os.walk(os.path.abspath(working_dir_name))]
        filesListInDir = []
        try:
            getattr(self, "filesInOutputDir")
        except AttributeError:
            self.filesInOutputDir = {}
            for fdir, fchilds, fnames in fileList:
                for fname in fnames:
                    fkeyname = os.path.normpath(os.path.join(fdir, fname))
                    self.filesInOutputDir.update({fkeyname.upper():fkeyname})
        for fdir, fchilds, fnames in fileList:
            for fname in fnames:
                filesListInDir.append(fname)
        self.tinkerRunFiles = {}
        self.tinkerFiles = []
        self.tinkerFileSteps = []
        self.tinkerFileTimes = []
        self.tinkerAveSteps = []
        self.tinkerAveTimes = []
        self.tinkerFirstStep = None
        self.tinkerRunMD = False
        fileFound = False
        textFiles = None
        self.tinkerKeyFile = None
        self.MDsteps = 0
        self.MDtimestep = None
        step = 0
        mdstart = 0
        mdend = 1
        self.recordList.seek(0)
        runnum=-1
        runstart = 0
        runend = 14
        header = False
        for li, line in enumerate(self.recordList):
            upLine = line.upper()
            if 'OPTIMIZATION' in upLine:
                mdstart = li
            if 'MOLECULAR DYNAMICS TRAJECTORY' in upLine:
                self.tinkerRunMD = True
                mdstart = li
            if 'ITER' in upLine and 'VALUE' in upLine and 'RMS' in upLine:
                mdstart = li
            if 'MD STEP' in upLine:
                self.tinkerRunMD = True
                mdstart = li
            if ''.join(line.strip().split()) == '':
                mdend = li
            if 'AVERAGE' in upLine and 'VALUES' in upLine:
                avestep = int(' '.join(line.strip().split()).split()[-3])
                if self.tinkerFirstStep is None:
                    self.tinkerFirstStep = avestep
                else:
                    if avestep<self.tinkerFirstStep:
                        self.tinkerFirstStep = avestep
                self.tinkerAveSteps.append(avestep)
            if 'SIMULATION' in upLine and 'TIME' in upLine:
                self.tinkerAveTimes.append(float(' '.join(line.strip().split()).split()[2]))
            if 'INSTANTANEOUS' in upLine and 'VALUES' in upLine:
                inststep = int(' '.join(line.strip().split()).split()[-3])
                if self.tinkerFirstStep is None:
                    self.tinkerFirstStep = inststep
                else:
                    if inststep<self.tinkerFirstStep:
                        self.tinkerFirstStep = inststep
                self.tinkerFileSteps.append(inststep)
            if 'CURRENT' in upLine and 'TIME' in upLine:
                self.tinkerFileTimes.append(float(' '.join(line.strip().split()).split()[2]))
            if 'COORDINATE' in upLine and 'FILE' in upLine:
                fileFound = True
                self.tinkerFiles.append(' '.join(line.strip().split()).split()[-1])
            if '#######' in line:
                break

        self.recordList.seek(0)
        mdstep=False
        avestep=False
        inststep=False
        for li, line in enumerate(self.recordList):
            if li >= mdstart and li <= mdend:
                upLine = line.upper()
                if 'MD STEP' in upLine or ('ITER' in upLine and 'VALUE' in upLine):
                    mdstep=True
                if 'AVERAGE VALUES' in upLine:
                    avestep=True
                if 'INSTANTANEOUS VALUES' in upLine:
                    inststep=True
                if mdstep:
                    sl = line.strip().split()
                    if len(sl)>3:
                        try:
                            step = int(sl[0])
                            if step> self.MDsteps:
                                self.MDsteps = step
                        except(ValueError, TypeError):
                            pass
                if avestep or inststep:
                    if 'DYNAMICS STEPS' in upLine:
                        sl = line.strip().split()
                        if len(sl)>3:
                            try:
                                step = int(sl[-3])
                                if step > self.MDsteps:
                                    self.MDsteps = step
                            except(ValueError, TypeError):
                                pass

        if self.MDsteps is not None:
            nstepKey = isMetaStrInDict("NSTEP", self.cntrlDict)
            if nstepKey is not None:
                self.cntrlDict[nstepKey].activeInfo = True
                self.cntrlDict[nstepKey].value = self.MDsteps

        if self.MDtimestep is None:
            if len(self.tinkerFileSteps)>0 and len(self.tinkerFileTimes)>0:
                self.MDtimestep = self.tinkerFileTimes[0]/self.tinkerFileSteps[0]
        if self.MDtimestep is None:
            if len(self.tinkerAveSteps)>0 and len(self.tinkerAveTimes)>0:
                self.MDtimestep = self.tinkerAveTimes[0]/self.tinkerAveSteps[0]

        if self.MDtimestep is not None:
            nstepKey = isMetaStrInDict("STEP-DT", self.cntrlDict)
            if nstepKey is not None:
                self.cntrlDict[nstepKey].activeInfo = True
                self.cntrlDict[nstepKey].value = self.MDtimestep

        # First find tinker run name from output files such as Coordinate File outputs
        # If there is no output file than
        # find all .key files in working dir
        # and try match the base names of these files with the output log file that
        # parser is working on.
        # If none of the above strategies work, use default key file name tinker.key
        # Finally, try readinf input key file if there is one
        if fileFound is True:
            coordfilename = os.path.basename(self.tinkerFiles[0])
            coordexts = MDDA.get_fileExtensions(coordfilename)
            if len(coordexts)>0:
                self.tinkerBaseName = coordexts[0]
                self.tinkerKeyFile = self.tinkerBaseName + '.key'
        if self.tinkerKeyFile is None:
            for tfile in filesListInDir:
                if '.KEY' in tfile.upper():
                    fname = os.path.basename(tfile)
                    fexts = MDDA.get_fileExtensions(fname)
                    if len(fexts)>0:
                        if fexts[0].upper() in os.path.basename(self.fName).upper():
                            coordfilename = os.path.basename(tfile)
                            coordexts = MDDA.get_fileExtensions(coordfilename)
                            self.tinkerBaseName = coordexts[0]
                            self.tinkerKeyFile = tfile
                            break
        if self.tinkerKeyFile is None and textFiles is not None:
            for tfile in filesListInDir:
                if 'TINKER.KEY' in tfile.upper():
                    coordfilename = os.path.basename(tfile)
                    coordexts = MDDA.get_fileExtensions(coordfilename)
                    self.tinkerBaseName = coordexts[0]
                    self.tinkerKeyFile = tfile
                    break
        if self.tinkerKeyFile is None and textFiles is not None:
            for tfile in filesListInDir:
                if '.KEY' in tfile.upper():
                    coordfilename = os.path.basename(tfile)
                    coordexts = MDDA.get_fileExtensions(coordfilename)
                    self.tinkerBaseName = coordexts[0]
                    self.tinkerKeyFile = tfile
                    break

        self.tinkerTrajSteps = []
        if fileFound is True:
            rtn = setMetaStrInDict(self, 'filecntrlDict', 'coordinate file list', ','.join(self.tinkerFiles))
            self.tinkerRunFiles.update({'coordinate file list' : ','.join(self.tinkerFiles)})
        if self.secRunGIndex<1:
            xyzfile = self.tinkerBaseName + '.xyz'
        elif self.secRunGIndex>0:
            xyzfile = self.tinkerBaseName + '.xyz_' + str(self.secRunGIndex+1)
        outxyzfile = self.tinkerBaseName + '.xyz_' + str(self.secRunGIndex+2)
        dynfile = self.tinkerBaseName + '.dyn'
        corfile = self.tinkerBaseName + '.001'
        arcfile = self.tinkerBaseName + '.arc'
        if xyzfile in filesListInDir:
            rtn = setMetaStrInDict(self, 'filecntrlDict', 'topology file', xyzfile)
            self.tinkerRunFiles.update({'topology file' : xyzfile})
            self.tinkerTrajSteps.append(1)
            if self.tinkerFirstStep not in self.tinkerTrajSteps:
                self.tinkerTrajSteps.append(self.tinkerFirstStep)
        if self.tinkerFileSteps:
            for trajst in self.tinkerFileSteps:
                if trajst not in self.tinkerTrajSteps:
                    self.tinkerTrajSteps.append(trajst)
        if outxyzfile in filesListInDir:
            rtn = setMetaStrInDict(self, 'filecntrlDict', 'final configuration file', outxyzfile)
            self.tinkerRunFiles.update({'final configuration file' : outxyzfile})
            if self.MDsteps not in self.tinkerTrajSteps:
                self.tinkerTrajSteps.append(self.MDsteps)
        if xyzfile in filesListInDir:
            rtn = setMetaStrInDict(self, 'filecntrlDict', 'initial configuration file', xyzfile)
            self.tinkerRunFiles.update({'initial configuration file' : xyzfile})
        if self.tinkerRunMD is True:
            if dynfile in filesListInDir:
                rtn = setMetaStrInDict(self, 'filecntrlDict', 'restart file', dynfile)
                self.tinkerRunFiles.update({'restart file' : dynfile})
                if self.MDsteps not in self.tinkerTrajSteps:
                    self.tinkerTrajSteps.append(self.MDsteps)
            if corfile in filesListInDir:
                rtn = setMetaStrInDict(self, 'filecntrlDict', 'initial trajectory file', corfile)
                self.tinkerRunFiles.update({'initial trajectory file' : corfile})
            if arcfile in filesListInDir and arcfile in self.tinkerFiles:
                rtn = setMetaStrInDict(self, 'filecntrlDict', 'archive file', arcfile)
                self.tinkerRunFiles.update({'archive file' : arcfile})

        self.tinkerXYZSeqList = {}
        if arcfile not in self.tinkerFiles:
            trajinstance = 0
            for fname in self.tinkerFiles:
                if('.arc' not in fname and
                   '.xyz' not in fname and
                   fname in filesListInDir):
                    self.tinkerXYZSeqList.update({
                        self.tinkerFileSteps[
                            trajinstance] : working_dir_name+os.path.sep+fname
                        })
                    trajinstance += 1
        #    self.generateARCfileFromSequenceFiles(parser, filesListInDir, arcfile)
        #    rtn = setMetaStrInDict(self, 'filecntrlDict', 'archive file', arcfile)
        #    self.tinkerRunFiles.update({'archive file' : arcfile})


        if self.tinkerKeyFile is not None:
            rtn = setMetaStrInDict(self, 'filecntrlDict', 'key file', self.tinkerKeyFile)
            self.findInputCmdFileAndRead(parser)
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

    def generateARCfileFromSequenceFiles(self, parser, fileListInDir, arcname):
        xyzSeqList = []
        working_dir_name = os.path.dirname(os.path.abspath(self.fName))
        addfile = os.path.normpath(working_dir_name+os.path.sep+arcname)
        for fname in self.tinkerFiles:
            if('.arc' not in fname and
               '.xyz' not in fname and
               fname in fileListInDir):
                xyzSeqList.append(working_dir_name+os.path.sep+fname)
        anyFileExist=False
        for fname in xyzSeqList:
            with open(fname, 'rb') as fin:
                if fin.read():
                    anyFileExist=True
                    fin.close()
        if anyFileExist:
            with open(addfile, 'wb') as fout:
                for fname in xyzSeqList:
                    with open(fname, 'rb') as fin:
                        fout.write(fin.read())

    def fetchInfoFromInputOutput(self, parser):
        self.recordList.write('   #######################################   ')
        working_dir_name = os.path.dirname(os.path.abspath(self.fName))
        fileList = [x for x in os.walk(os.path.abspath(working_dir_name))]
        filesListInDir = []
        try:
            getattr(self, "filesInOutputDir")
        except AttributeError:
            self.filesInOutputDir = {}
            for fdir, fchilds, fnames in fileList:
                for fname in fnames:
                    fkeyname = os.path.normpath(os.path.join(fdir, fname))
                    self.filesInOutputDir.update({fkeyname.upper():fkeyname})
        for fdir, fchilds, fnames in fileList:
            for fname in fnames:
                filesListInDir.append(fname)
        self.tinkerRunFiles = {}
        self.tinkerFiles = []
        self.tinkerFileSteps = []
        self.tinkerFileTimes = []
        self.tinkerAveSteps = []
        self.tinkerAveTimes = []
        self.tinkerFirstStep = None
        self.tinkerRunMD = False
        fileFound = False
        textFiles = None
        self.tinkerKeyFile = None
        self.MDsteps = 0
        self.MDtimestep = None
        step = 0
        mdstart = 0
        mdend = 1
        self.recordList.seek(0)
        runnum=-1
        runstart = 0
        runend = 14
        header = False
        for li, line in enumerate(self.recordList):
            upLine = line.upper()
            if 'OPTIMIZATION' in upLine:
                mdstart = li
            if 'MOLECULAR DYNAMICS TRAJECTORY' in upLine:
                self.tinkerRunMD = True
                mdstart = li
            if 'ITER' in upLine and 'VALUE' in upLine and 'RMS' in upLine:
                mdstart = li
            if 'MD STEP' in upLine:
                self.tinkerRunMD = True
                mdstart = li
            if ''.join(line.strip().split()) == '':
                mdend = li
            if 'AVERAGE' in upLine and 'VALUES' in upLine:
                avestep = int(' '.join(line.strip().split()).split()[-3])
                if self.tinkerFirstStep is None:
                    self.tinkerFirstStep = avestep
                else:
                    if avestep<self.tinkerFirstStep:
                        self.tinkerFirstStep = avestep
                self.tinkerAveSteps.append(avestep)
            if 'SIMULATION' in upLine and 'TIME' in upLine:
                self.tinkerAveTimes.append(float(' '.join(line.strip().split()).split()[2]))
            if 'INSTANTANEOUS' in upLine and 'VALUES' in upLine:
                inststep = int(' '.join(line.strip().split()).split()[-3])
                if self.tinkerFirstStep is None:
                    self.tinkerFirstStep = inststep
                else:
                    if inststep<self.tinkerFirstStep:
                        self.tinkerFirstStep = inststep
                self.tinkerFileSteps.append(inststep)
            if 'CURRENT' in upLine and 'TIME' in upLine:
                self.tinkerFileTimes.append(float(' '.join(line.strip().split()).split()[2]))
            if 'COORDINATE' in upLine and 'FILE' in upLine:
                fileFound = True
                self.tinkerFiles.append(' '.join(line.strip().split()).split()[-1])
            if '#######' in line:
                break

        self.recordList.seek(0)
        mdstep=False
        avestep=False
        inststep=False
        for li, line in enumerate(self.recordList):
            if li >= mdstart and li <= mdend:
                upLine = line.upper()
                if 'MD STEP' in upLine or ('ITER' in upLine and 'VALUE' in upLine):
                    mdstep=True
                if 'AVERAGE VALUES' in upLine:
                    avestep=True
                if 'INSTANTANEOUS VALUES' in upLine:
                    inststep=True
                if mdstep:
                    sl = line.strip().split()
                    if len(sl)>3:
                        try:
                            step = int(sl[0])
                            if step> self.MDsteps:
                                self.MDsteps = step
                        except(ValueError, TypeError):
                            pass
                if avestep or inststep:
                    if 'DYNAMICS STEPS' in upLine:
                        sl = line.strip().split()
                        if len(sl)>3:
                            try:
                                step = int(sl[-3])
                                if step > self.MDsteps:
                                    self.MDsteps = step
                            except(ValueError, TypeError):
                                pass

        if self.MDsteps is not None:
            nstepKey = isMetaStrInDict("NSTEP", self.cntrlDict)
            if nstepKey is not None:
                self.cntrlDict[nstepKey].activeInfo = True
                self.cntrlDict[nstepKey].value = self.MDsteps

        if self.MDtimestep is None:
            if len(self.tinkerFileSteps)>0 and len(self.tinkerFileTimes)>0:
                self.MDtimestep = self.tinkerFileTimes[0]/self.tinkerFileSteps[0]
        if self.MDtimestep is None:
            if len(self.tinkerAveSteps)>0 and len(self.tinkerAveTimes)>0:
                self.MDtimestep = self.tinkerAveTimes[0]/self.tinkerAveSteps[0]

        if self.MDtimestep is not None:
            nstepKey = isMetaStrInDict("STEP-DT", self.cntrlDict)
            if nstepKey is not None:
                self.cntrlDict[nstepKey].activeInfo = True
                self.cntrlDict[nstepKey].value = self.MDtimestep

        # First find tinker run name from output files such as Coordinate File outputs
        # If there is no output file than
        # find all .key files in working dir
        # and try match the base names of these files with the output log file that
        # parser is working on.
        # If none of the above strategies work, use default key file name tinker.key
        # Finally, try readinf input key file if there is one
        if fileFound is True:
            coordfilename = os.path.basename(self.tinkerFiles[0])
            coordexts = MDDA.get_fileExtensions(coordfilename)
            if len(coordexts)>0:
                self.tinkerBaseName = coordexts[0]
                self.tinkerKeyFile = self.tinkerBaseName + '.key'
        if self.tinkerKeyFile is None:
            for tfile in filesListInDir:
                if '.KEY' in tfile.upper():
                    fname = os.path.basename(tfile)
                    fexts = MDDA.get_fileExtensions(fname)
                    if len(fexts)>0:
                        if fexts[0].upper() in os.path.basename(self.fName).upper():
                            coordfilename = os.path.basename(tfile)
                            coordexts = MDDA.get_fileExtensions(coordfilename)
                            self.tinkerBaseName = coordexts[0]
                            self.tinkerKeyFile = tfile
                            break
        if self.tinkerKeyFile is None and textFiles is not None:
            for tfile in filesListInDir:
                if 'TINKER.KEY' in tfile.upper():
                    coordfilename = os.path.basename(tfile)
                    coordexts = MDDA.get_fileExtensions(coordfilename)
                    self.tinkerBaseName = coordexts[0]
                    self.tinkerKeyFile = tfile
                    break
        if self.tinkerKeyFile is None and textFiles is not None:
            for tfile in filesListInDir:
                if '.KEY' in tfile.upper():
                    coordfilename = os.path.basename(tfile)
                    coordexts = MDDA.get_fileExtensions(coordfilename)
                    self.tinkerBaseName = coordexts[0]
                    self.tinkerKeyFile = tfile
                    break

        self.tinkerTrajSteps = []
        if fileFound is True:
            rtn = setMetaStrInDict(self, 'filecntrlDict', 'coordinate file list', ','.join(self.tinkerFiles))
            self.tinkerRunFiles.update({'coordinate file list' : ','.join(self.tinkerFiles)})
        if self.secRunGIndex<1:
            xyzfile = self.tinkerBaseName + '.xyz'
        elif self.secRunGIndex>0:
            xyzfile = self.tinkerBaseName + '.xyz_' + str(self.secRunGIndex+1)
        outxyzfile = self.tinkerBaseName + '.xyz_' + str(self.secRunGIndex+2)
        dynfile = self.tinkerBaseName + '.dyn'
        corfile = self.tinkerBaseName + '.001'
        arcfile = self.tinkerBaseName + '.arc'
        if xyzfile in filesListInDir:
            rtn = setMetaStrInDict(self, 'filecntrlDict', 'topology file', xyzfile)
            self.tinkerRunFiles.update({'topology file' : xyzfile})
            self.tinkerTrajSteps.append(1)
            if self.tinkerFirstStep not in self.tinkerTrajSteps:
                self.tinkerTrajSteps.append(self.tinkerFirstStep)
        if self.tinkerFileSteps:
            for trajst in self.tinkerFileSteps:
                if trajst not in self.tinkerTrajSteps:
                    self.tinkerTrajSteps.append(trajst)
        if outxyzfile in filesListInDir:
            rtn = setMetaStrInDict(self, 'filecntrlDict', 'final configuration file', outxyzfile)
            self.tinkerRunFiles.update({'final configuration file' : outxyzfile})
            if self.MDsteps not in self.tinkerTrajSteps:
                self.tinkerTrajSteps.append(self.MDsteps)
        if xyzfile in filesListInDir:
            rtn = setMetaStrInDict(self, 'filecntrlDict', 'initial configuration file', xyzfile)
            self.tinkerRunFiles.update({'initial configuration file' : xyzfile})
        if self.tinkerRunMD is True:
            if dynfile in filesListInDir:
                rtn = setMetaStrInDict(self, 'filecntrlDict', 'restart file', dynfile)
                self.tinkerRunFiles.update({'restart file' : dynfile})
                if self.MDsteps not in self.tinkerTrajSteps:
                    self.tinkerTrajSteps.append(self.MDsteps)
            if corfile in filesListInDir:
                rtn = setMetaStrInDict(self, 'filecntrlDict', 'initial trajectory file', corfile)
                self.tinkerRunFiles.update({'initial trajectory file' : corfile})
            if arcfile in filesListInDir and arcfile in self.tinkerFiles:
                rtn = setMetaStrInDict(self, 'filecntrlDict', 'archive file', arcfile)
                self.tinkerRunFiles.update({'archive file' : arcfile})

        self.tinkerXYZSeqList = {}
        if arcfile not in self.tinkerFiles:
            trajinstance = 0
            for fname in self.tinkerFiles:
                if('.arc' not in fname and
                   '.xyz' not in fname and
                   fname in filesListInDir):
                    self.tinkerXYZSeqList.update({
                        self.tinkerFileSteps[
                            trajinstance] : working_dir_name+os.path.sep+fname
                        })
                    trajinstance += 1
        #    self.generateARCfileFromSequenceFiles(parser, filesListInDir, arcfile)
        #    rtn = setMetaStrInDict(self, 'filecntrlDict', 'archive file', arcfile)
        #    self.tinkerRunFiles.update({'archive file' : arcfile})


        if self.tinkerKeyFile is not None:
            rtn = setMetaStrInDict(self, 'filecntrlDict', 'key file', self.tinkerKeyFile)
            #self.findInputCmdFileAndRead(parser)

        self.tinkerRunFiles.update({'filesteps' : self.tinkerTrajSteps})
        self.tinkerRunFiles.update({'filetrajs' : self.tinkerXYZSeqList})

        self.fileUnitDict.update({self.secRunGIndex : self.tinkerRunFiles})

        return True

    def findInputCmdFileAndRead(self, parser):
        success = None
        tkeyFile = self.findFileInDir(parser, "key file", "filecntrlDict")
        if tkeyFile is not None:
            self.inputCntrlFile = tkeyFile
            success = self.readTinkerParameterFile(parser, tkeyFile, 'cntrlDict')
        return success

    def build_subMatchers(self):
        """Builds the sub matchers to parse the main output file.
        """
        mddataNameList=getList_MetaStrInDict(self.mddataDict)

        self.mdStepHeaderDict={
                'MD Step':0,
                'E Total':1,
                'E Potential':2,
                'E Kinetic':3,
                'Temp':4,
                'Pres':5,
                }

        #self.minStepHeaderDict={
        #        'MIN Iter' : 0,
        #        'F Value' : 1,
        #        'G RMS' : 2,
        #        'F Move' : 3,
        #        'X Move' : 4,
        #        'Angle' : 5,
        #        'FG Call' : 6,
        #        'Comment' : 7
        #        }

        cntrlNameList=getList_MetaStrInDict(self.metaDicts['cntrl'])
        filecntrlNameList=getList_MetaStrInDict(self.metaDicts['filecntrl'])
        fileNameList=getList_MetaStrInDict(self.metaDicts['file'])
        extraNameList=getList_MetaStrInDict(self.metaDicts['extra'])

        self.minOutputSubParsers = [
            # Optimization reader
            { "startReStr"        : r"\s*Optimization\s*",
              "parser"            : "namelist_parser",
              "parsername"        : "min_init_parser",
              "waitlist"          : None,
              "stopOnMatchStr"    : r"\s*(?:QN|TN|CG|VM)\s+Iter\s*",
              "quitOnMatchStr"    : r"\s*(?:QN|TN|CG|VM)\s+Iter\s*",
              "metaNameStart"     : PARSERTAG + "_inout_control",
              "matchNameList"     : cntrlNameList,
              "matchNameDict"     : "mdcntrlDict",
              "updateMatchDict"   : True,
              "onlyCaseSensitive" : False,
              "stopOnFirstLine"   : False,
              "parserOptions"     : {
                  "lineFilter"       : None,
                  "controlsections"  : ["x_tinker_section_control_parameters"],
                  "controlsave"      : "sectioncontrol",
                  "controldict"      : "stepcontrolDict",
                  }
              },
            # Optimization end reader
            { "startReStr"        : r"\s*[A-Z]+\s+--\s*",
              "parser"            : "namelist_parser",
              "parsername"        : "min_end_parser",
              "waitlist"          : None,
              "stopOnMatchStr"    : r"^\s*$",
              "quitOnMatchStr"    : r"^\s*$",
              "metaNameStart"     : PARSERTAG + "_inout_control",
              "matchNameList"     : cntrlNameList,
              "matchNameDict"     : "mdcntrlDict",
              "updateMatchDict"   : True,
              "onlyCaseSensitive" : False,
              "stopOnFirstLine"   : True,
              "parserOptions"     : {
                  "lineFilter"       : None,
                  #"controlsections"  : ["x_tinker_section_control_parameters"],
                  #"controlsave"      : "sectioncontrol",
                  #"controldict"      : "stepcontrolDict",
                  }
              },
            # Optimization end reader
            { "startReStr"        : r"\s*Final\s*",
              "parser"            : "namelist_parser",
              "parsername"        : "min_final_parser",
              "waitlist"          : None,
              "stopOnMatchStr"    : r"^\s*$",
              "quitOnMatchStr"    : r"^\s*$",
              "metaNameStart"     : PARSERTAG + "_inout_control",
              "matchNameList"     : cntrlNameList,
              "matchNameDict"     : "mdcntrlDict",
              "updateMatchDict"   : True,
              "onlyCaseSensitive" : False,
              "stopOnFirstLine"   : False,
              "parserOptions"     : {
                  "lineFilter"       : None,
                  #"controlsections"  : ["x_tinker_section_control_parameters"],
                  #"controlsave"      : "sectioncontrol",
                  #"controldict"      : "stepcontrolDict",
                  }
              },
            # Section Control Parser
            { "startReStr"        : "AlwaysRun",
              "parser"            : "section_control_parser",
              "parsername"        : "control_section_parser",
              "waitlist"          : [["min_init_parser"]],
              "stopOnMatchStr"    : "AlwaysStop",
              "quitOnMatchStr"    : "AlwaysStop",
              "metaNameStart"     : None,
              "matchNameList"     : None,
              "matchNameDict"     : None,
              "updateMatchDict"   : False,
              "onlyCaseSensitive" : False,
              "stopOnFirstLine"   : False,
              "parserOptions"     : {
                  "sectionname"      : "x_tinker_section_control_parameters",
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
            # Optimization Step header reader
            { "startReStr"        : r"\s*(?:QN|TN|CG|VM)\s+Iter\s*",
              "parser"            : "table_parser",
              "parsername"        : "min_header_parser",
              "waitlist"          : None,
              #"waitlist"          : [["min_init_parser"]],
              "stopOnMatchStr"    : r"^\s*$",
              "quitOnMatchStr"    : r"^\s*$",
              "metaNameStart"     : PARSERTAG + "_mdout_",
              "matchNameList"     : mddataNameList,
              "matchNameDict"     : "mddataDict",
              "updateMatchDict"   : True,
              "onlyCaseSensitive" : False,
              "stopOnFirstLine"   : False,
              "parserOptions"     : {
                  "header"           : True,
                  "headersave"       : "minStepHeaderDict",
                  "wrap"             : False,
                  "tablelines"       : 0,
                  "tablestartsat"    : r"\s*(?:QN|TN|CG|VM)\s*Iter",
                  "tableendsat"      : r"^\s*$",
                  "lineFilter"       : {
                      'QN Iter' : 'ITER1',
                      'TN Iter' : 'ITER2',
                      'VM Iter' : 'ITER3',
                      'CG Iter' : 'ITER4',
                      'F Value' : 'FVALUE',
                      'G RMS'   : 'GRMS1',
                      'RMS G'   : 'GRMS2',
                      'F Move'  : 'FMove',
                      'X Move'  : 'XMove',
                      'FG Call' : 'FGCall'
                      },
                  "movetostopline"   : True,
                  #"parsercntrlattr"  : "MDcurrentstep",
                  #"parsercntrlin"    : "steps",
                  #"lookupdict"       : "stepcontrolDict"
                  }
              },
            # Optim output cycles reader
            { "startReStr"        : r"^\s*[0-9]+\s*",
              "parser"            : "table_parser",
              "parsername"        : "min_step_parser",
              "waitlist"          : None,
              #"waitlist"          : [["min_init_parser"]],
              "stopOnMatchStr"    : r"^\s*$",
              "quitOnMatchStr"    : r"^\s*$",
              #"stopOnMatchStr"    : r"\s*(?:MD\s*Step|"
              #                       "Average\s*Values|"
              #                       "Instantaneous\s*Values)\s*",
              #"quitOnMatchStr"    : r"\s*(?:MD\s*Step|"
              #                       "Average\s*Values|"
              #                       "Instantaneous\s*Values)\s*",
              "metaNameStart"     : PARSERTAG + "_mdout_",
              "matchNameList"     : mddataNameList,
              "matchNameDict"     : "mddataDict",
              "updateMatchDict"   : True,
              "onlyCaseSensitive" : False,
              "stopOnFirstLine"   : True,
              "parserOptions"     : {
                  "header"           : False,
                  "headerList"       : "minStepHeaderDict",
                  "wrap"             : False,
                  "tablelines"       : 0,
                  "maxtablelines"    : 1,
                  "tablestartsat"    : r"\s*[0-9]+\s*",
                  "tableendsat"      : r"^\s*$",
                  "lineFilter"       : None,
                  "movetostopline"   : True,
                  "controlsections"  : ["section_single_configuration_calculation"],
                  "controlsave"      : "sectioncontrol",
                  "controldict"      : "stepcontrolDict",
                  #"parsercntrlattr"  : "MDcurrentstep",
                  #"parsercntrlin"    : "logsteps",
                  #"lookupdict"       : "stepcontrolDict"
                  }
              },
            # energy save Parser
            { "startReStr"        : "AlwaysRun",
              "parser"            : "dictionary_parser",
              "parsername"        : "min_energies_parser",
              "waitlist"          : None,
              #"waitlist"          : [["md_step_parser"]],
              "stopOnMatchStr"    : "AlwaysStop",
              "quitOnMatchStr"    : "AlwaysStop",
              "metaNameStart"     : PARSERTAG + "_mdout_",
              "matchNameList"     : mddataNameList,
              "matchNameDict"     : "mddataDict",
              "updateMatchDict"   : False,
              "onlyCaseSensitive" : False,
              "stopOnFirstLine"   : False,
              "parserOptions"     : {
                  "dictionary"       : "mddataDict",
                  "dicttype"         : "smartparser", # (standard or smartparser)
                  "readwritedict"    : "write",
                  "keyMapper"        : {"F Value" : "E Potential"},
                  #"preprocess"       : self.convertFloat,
                  #"postprocess"      : self.convertFloat,
                  #"parsercntrlattr"  : "MDcurrentstep",
                  #"parsercntrlin"    : "steps",
                  #"lookupdict"       : "stepcontrolDict"
                  }
              },
            # thermostat save Parser
            { "startReStr"        : "AlwaysRun",
              "parser"            : "dictionary_parser",
              "parsername"        : "min_frameseq_step_parser",
              "waitlist"          : None,
              #"waitlist"          : [["md_step_parser"]],
              "stopOnMatchStr"    : "AlwaysStop",
              "quitOnMatchStr"    : "AlwaysStop",
              "metaNameStart"     : PARSERTAG + "_mdout_",
              "matchNameList"     : mddataNameList,
              "matchNameDict"     : "mddataDict",
              "updateMatchDict"   : False,
              "onlyCaseSensitive" : False,
              "stopOnFirstLine"   : False,
              "parserOptions"     : {
                  "dictionary"       : "stepcontrolDict",
                  "dicttype"         : "standard", # (standard or smartparser)
                  "readwritedict"    : "write",
                  "keyMapper"        : {"MD Step"         : "MDcurrentstep",
                                        "Dynamics Steps"  : "MDcurrentstep",
                                        #"InputCoordStep"  : "MDcurrentstep",
                                        #"OutputCoordStep" : "MDcurrentstep",
                                        "VM Iter"         : "MDcurrentstep",
                                        "TN Iter"         : "MDcurrentstep",
                                        "QN Iter"         : "MDcurrentstep",
                                        "CG Iter"         : "MDcurrentstep"},
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
              "parsername"        : "min_section_parser",
              #"waitlist"          : [["md_step_parser"]],
              "waitlist"          : None,
              "stopOnMatchStr"    : "EOFEOF\s*",
              "quitOnMatchStr"    : "EOFEOF\s*",
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
              "parsername"        : "min_readline_parser",
              #"waitlist"          : [["md_step_parser"]],
              #"waitlist"          : None,
              "waitlist"          : [["min_init_parser"]],
              "stopOnMatchStr"    : "EOFEOF\s*",
              "quitOnMatchStr"    : "EOFEOF\s*",
              "metaNameStart"     : None,
              "matchNameList"     : None,
              "matchNameDict"     : None,
              "updateMatchDict"   : False,
              "onlyCaseSensitive" : True,
              "stopOnFirstLine"   : False,
              "parserOptions"     : {
                  "peeklineFirst"    : False,
                  "waitatlineStr"    : r"^\s*",
                  "controlwait"      : None,
                  "controlattr"      : "MDcurrentstep",
                  #"controlnextattr"  : "MDnextstep",
                  #"controllast"      : -1,
                  #"controlskip"      : [0],
                  "controlin"        : "steps",
                  "controlcounter"   : "targetstep",
                  "controldict"      : "stepcontrolDict",
                  "lookupdict"       : "stepcontrolDict"
                  }
              },
            ]

        self.mdOutputSubParsers = [
            # MD reader
            { "startReStr"        : r"\s*Molecular\s+Dynamics\s*",
              "parser"            : "namelist_parser",
              "parsername"        : "md_init_parser",
              "waitlist"          : None,
              "stopOnMatchStr"    : r"\s*(?:MD\s+Step|"
                                     "Average\s+Values|"
                                     "Instantaneous\s+Values)\s*",
              "quitOnMatchStr"    : r"\s*(?:MD\s+Step|"
                                     "Average\s+Values|"
                                     "Instantaneous\s+Values)\s*",
              "metaNameStart"     : PARSERTAG + "_inout_control",
              "matchNameList"     : cntrlNameList,
              "matchNameDict"     : "mdcntrlDict",
              "updateMatchDict"   : False,
              "onlyCaseSensitive" : False,
              "stopOnFirstLine"   : False,
              "parserOptions"     : {
                  #"lineFilter"       : None,
                  #"movetostopline"   : True,
                  "controlsections"  : ["x_tinker_section_control_parameters"],
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
              "onlyCaseSensitive" : False,
              "stopOnFirstLine"   : False,
              "parserOptions"     : {
                  "sectionname"      : "x_tinker_section_control_parameters",
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
            # MD output average values reader
            { "startReStr"        : r"^\s*Average\s*Values\s*",
              "parser"            : "namelist_parser",
              "parsername"        : "md_average_parser",
              "waitlist"          : None,
              "stopOnMatchStr"    : r"^\s*Density\s*",
              "quitOnMatchStr"    : r"^\s*Density\s*",
              "metaNameStart"     : PARSERTAG + "_mdout_",
              "matchNameList"     : mddataNameList,
              "matchNameDict"     : "mddataDict",
              "updateMatchDict"   : True,
              "onlyCaseSensitive" : False,
              "stopOnFirstLine"   : False,
              "parserOptions"     : {
                  #"lineFilter"       : None,
                  "movetostopline"   : True,
                  #"controlsections"  : ["section_single_configuration_calculation"],
                  #"controlsave"      : "sectioncontrol",
                  #"controldict"      : "stepcontrolDict",
                  }
              },
            # MD output insta values reader
            { "startReStr"        : r"^\s*Instantaneous\s*Values\s*",
              "parser"            : "namelist_parser",
              "parsername"        : "md_insta_parser",
              "waitlist"          : None,
              "stopOnMatchStr"    : r"^\s*Coordinate\s*File\s*",
              "quitOnMatchStr"    : r"^\s*Coordinate\s*File\s*",
              "metaNameStart"     : PARSERTAG + "_mdout_",
              "matchNameList"     : mddataNameList,
              "matchNameDict"     : "mddataDict",
              "updateMatchDict"   : True,
              "onlyCaseSensitive" : False,
              "stopOnFirstLine"   : False,
              "parserOptions"     : {
                  "movetostopline"   : True,
                  #"controlsections"  : ["section_single_configuration_calculation"],
                  #"controlsave"      : "sectioncontrol",
                  #"controldict"      : "stepcontrolDict",
                  }
              },
            # MD output coordinate reader
            { "startReStr"        : r"^\s*Coordinate\s*File\s*",
              "parser"            : "namelist_parser",
              "parsername"        : "md_coord_parser",
              "waitlist"          : None,
              "stopOnMatchStr"    : r"^\s*$",
              "quitOnMatchStr"    : r"^\s*$",
              "metaNameStart"     : PARSERTAG + "_mdout_",
              "matchNameList"     : mddataNameList,
              "matchNameDict"     : "mddataDict",
              "updateMatchDict"   : True,
              "onlyCaseSensitive" : False,
              "stopOnFirstLine"   : False,
              "parserOptions"     : {
                  "movetostopline"   : True,
                  #"controlsections"  : ["section_single_configuration_calculation"],
                  #"controlsave"      : "sectioncontrol",
                  #"controldict"      : "stepcontrolDict",
                  }
              },
            # energy save Parser
            { "startReStr"        : "AlwaysRun",
              "parser"            : "dictionary_parser",
              "parsername"        : "md_energies_parser",
              #"waitlist"          : None,
              "waitlist"          : [["md_average_parser"],
                                     ["md_insta_parser"]],
              "stopOnMatchStr"    : "AlwaysStop",
              "quitOnMatchStr"    : "AlwaysStop",
              "metaNameStart"     : PARSERTAG + "_mdout_",
              "matchNameList"     : mddataNameList,
              "matchNameDict"     : "mddataDict",
              "updateMatchDict"   : False,
              "onlyCaseSensitive" : False,
              "stopOnFirstLine"   : False,
              "parserOptions"     : {
                  "dictionary"       : "mddataDict",
                  "dicttype"         : "smartparser", # (standard or smartparser)
                  "readwritedict"    : "write",
                  "keyMapper"        : {"Total Energy" : "E Total",
                                        "Potential Energy" : "E Potential",
                                        "Kinetic Energy" : "E Kinetic",
                                        "Temperature" : "Temp",
                                        "Pressure" : "Pres"},
                  #"preprocess"       : self.convertFloat,
                  #"postprocess"      : self.convertFloat,
                  #"parsercntrlattr"  : "MDcurrentstep",
                  #"parsercntrlin"    : "steps",
                  #"lookupdict"       : "stepcontrolDict"
                  }
              },
            # MD STEP header reader
            { "startReStr"        : r"\s*MD\s+Step\s*",
              "parser"            : "table_parser",
              "parsername"        : "md_header_parser",
              "waitlist"          : None,
              "stopOnMatchStr"    : r"^\s*$",
              "quitOnMatchStr"    : r"^\s*$",
              "metaNameStart"     : PARSERTAG + "_mdout_",
              "matchNameList"     : mddataNameList,
              "matchNameDict"     : "mddataDict",
              "updateMatchDict"   : True,
              "onlyCaseSensitive" : False,
              "stopOnFirstLine"   : False,
              "parserOptions"     : {
                  "header"           : True,
                  "headersave"       : "mdStepHeaderDict",
                  "wrap"             : False,
                  "tablelines"       : 0,
                  "tablestartsat"    : r"\s*MD\s*Step",
                  "tableendsat"      : r"^\s*$",
                  "lineFilter"       : {
                      'MD Step': 'MD-Step',
                      'E Total': 'TOTAL',
                      'E Potential': 'POTENTIAL',
                      'E Kinetic': 'KINETIC',
                      'Temp': 'TEMP',
                      'Pres': 'PRESS'
                      },
                  "movetostopline"   : True,
                  #"parsercntrlattr"  : "MDcurrentstep",
                  #"parsercntrlin"    : "steps",
                  #"lookupdict"       : "stepcontrolDict"
                  }
              },
            # MD output cycles reader
            { "startReStr"        : r"^\s*[0-9]+\s*",
              "parser"            : "table_parser",
              "parsername"        : "md_step_parser",
              "waitlist"          : None,
              #"waitlist"          : [["md_header_parser"]],
              "stopOnMatchStr"    : r"\s*(?:MD\s*Step|"
                                     "Average\s*Values|"
                                     "Instantaneous\s*Values)\s*",
              "quitOnMatchStr"    : r"\s*(?:MD\s*Step|"
                                     "Average\s*Values|"
                                     "Instantaneous\s*Values)\s*",
              "metaNameStart"     : PARSERTAG + "_mdout_",
              "matchNameList"     : mddataNameList,
              "matchNameDict"     : "mddataDict",
              "updateMatchDict"   : True,
              "onlyCaseSensitive" : False,
              "stopOnFirstLine"   : True,
              "parserOptions"     : {
                  "header"           : False,
                  "headerList"       : "mdStepHeaderDict",
                  "wrap"             : False,
                  "tablelines"       : 0,
                  "maxtablelines"    : 1,
                  "tablestartsat"    : r"\s*[0-9]+\s*",
                  "tableendsat"      : r"^\s*$",
                  "lineFilter"       : None,
                  "movetostopline"   : True,
                  "controlsections"  : ["section_single_configuration_calculation"],
                  "controlsave"      : "sectioncontrol",
                  "controldict"      : "stepcontrolDict",
                  #"parsercntrlattr"  : "MDcurrentstep",
                  #"parsercntrlin"    : "logsteps",
                  #"lookupdict"       : "stepcontrolDict"
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
              "updateMatchDict"   : False,
              "onlyCaseSensitive" : False,
              "stopOnFirstLine"   : False,
              "parserOptions"     : {
                  "dictionary"       : "stepcontrolDict",
                  "dicttype"         : "standard", # (standard or smartparser)
                  "readwritedict"    : "write",
                  "keyMapper"        : {"MD Step"         : "MDcurrentstep",
                                        "Dynamics Steps"  : "MDcurrentstep",
                                        #"InputCoordStep"  : "MDcurrentstep",
                                        #"OutputCoordStep" : "MDcurrentstep",
                                        "VM Iter"         : "MDcurrentstep",
                                        "TN Iter"         : "MDcurrentstep",
                                        "QN Iter"         : "MDcurrentstep",
                                        "CG Iter"         : "MDcurrentstep"},
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
              "parsername"        : "md_section_parser",
              #"waitlist"          : [["md_step_parser"]],
              "waitlist"          : None,
              "stopOnMatchStr"    : "EOFEOF\s*",
              "quitOnMatchStr"    : "EOFEOF\s*",
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
              "parsername"        : "md_readline_parser",
              #"waitlist"          : [["md_step_parser"]],
              #"waitlist"          : None,
              "waitlist"          : [["md_init_parser"]],
              "stopOnMatchStr"    : "EOFEOF\s*",
              "quitOnMatchStr"    : "EOFEOF\s*",
              "metaNameStart"     : None,
              "matchNameList"     : None,
              "matchNameDict"     : None,
              "updateMatchDict"   : False,
              "onlyCaseSensitive" : True,
              "stopOnFirstLine"   : False,
              "parserOptions"     : {
                  "peeklineFirst"    : False,
                  "waitatlineStr"    : r"^\s*",
                  "controlwait"      : None,
                  "controlattr"      : "MDcurrentstep",
                  #"controlnextattr"  : "MDnextstep",
                  #"controllast"      : -1,
                  #"controlskip"      : [0],
                  "controlin"        : "steps",
                  "controlcounter"   : "targetstep",
                  "controldict"      : "stepcontrolDict",
                  "lookupdict"       : "stepcontrolDict"
                  }
              },
            ]

        outputSubParsers = [
            # MD LOOP Parser Caller
            { "startReStr"        : r"\s*(?:Molecular\s+Dynamics|Optimization)\s*",
                                     #"Numbers\s+of\s+First\s+and\s+Last\s+File\s+to)\s*",
              #"startReStr"        : r"^\s*.*",
              "parser"            : "subparser_caller",
              "parsername"        : "command_subparser",
              "waitlist"          : None,
              #"waitlist"          : [["control_section_parser"]],
              #"stopOnMatchStr"    : r"\s*(?:Molecular\s+Dynamics|Optimization)\s*",
              #"quitOnMatchStr"    : r"\s*(?:Molecular\s+Dynamics|Optimization)\s*",
              "stopOnMatchStr"    : r"^\s*######+$",
              "quitOnMatchStr"    : r"^\s*######+$",
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
                      "Molecular Dynamics"   : "mdOutputSubParsers",
                      "Optimization"         : "minOutputSubParsers",
                      #"Analyze"              : "analyzeOutputSubParsers",
                      },
                  #"subparserSection" : {
                  #    "MD Step"    : ["section_run", "auto", "secRunOpen", "secRunGIndex"],
                  #    },
                  }
              },
            # Readline Control Parser
            { "startReStr"        : "AlwaysRun",
              "parser"            : "readline_control_parser",
              "parsername"        : "readline_parser",
              "waitlist"          : None,
              "stopOnMatchStr"    : r"^\s*######+$",
              "quitOnMatchStr"    : r"^\s*######+$",
              "metaNameStart"     : None,
              "matchNameList"     : None,
              "matchNameDict"     : None,
              "updateMatchDict"   : False,
              "onlyCaseSensitive" : False,
              "stopOnFirstLine"   : False,
              "parserOptions"     : {
                  "peeklineFirst"    : True,
                  #"waitatlineStr"    : "^\s*######+\s*$",
                  "waitatlineStr"    : None,
                  "controlwait"      : None,
                  "controlattr"      : "MDcurrentstep",
                  #"controlnextattr"  : "MDnextstep",
                  #"controllast"      : -1,
                  "controlskip"      : [-1],
                  "controlin"        : "opencntrlstep",
                  #"controlin"        : "steps",
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
                startReStr=r"^\s*#+\s*TINKER\s*---\s*Software\s*Tools\s*for\s*Molecular\s*Design\s*#+\s*$",
                #endReStr=r"\s*TINKER\s*-+\s*Software\s*Tools\s*for\s*Molecular\s*Design\s*",
                repeats=True,
                required=True,
                #forwardMatch=True,
                sections=['section_run'],
                fixedStartValues={'program_name': PROGRAMNAME},
                subMatchers=[
                    SM(name='ProgramInfo',
                        startReStr=r"^\s*#+\s*Version\s*"
                                   "(?P<"+PARSERTAG+"_mdin_finline>[a-zA-Z0-9:., ]+)\s*#+",
                       adHoc=lambda p: p.backend.addValue(
                           "program_version",
                           ' '.join(p.lastMatch[
                               PARSERTAG+"_mdin_finline"
                               ].replace('\n', ' ').strip().split()))),
                    SM(name='copyright',
                       startReStr=r"^\s*#+\s*Copyright\s*\(c\)\s*",
                       coverageIgnore=True,
                       adHoc=lambda p:
                       self.adHoc_read_store_text_stop_parsing(p,
                           stopOnMatchStr=r"^\s*#+\s*#+\s*$",
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
                                   ].replace('\n', ' ').replace('#', '').strip().split())
                               )
                           )
                       ),
                    SM(name='newRun',
                       startReStr=r"^\s*$",
                       #endReStr=r"^\s*$",
                       #forwardMatch=True,
                       adHoc=lambda p:
                       self.adHoc_takingover_parsing(p,
                           stopOnMatchStr=r"^\s*#####+\s*$",
                           quitOnMatchStr=r"^\s*#####+\s*$",
                           #onStartRunFunction=self.textFileFoundInDir,
                           stopControl="stopControl", # if None or True, stop with quitMatch, else wait
                           onStartReplayRunFunction={1:"fetchInfoFromInputOutput"},
                           record=True, # if False or None, no record, no replay
                           replay=1, # if 0 or None= no replay, if <0 infinite replay
                           parseOnlyRecorded=True, # if True, parsers only work on record
                           ordered=False,
                           onlySubParsersReadLine=True,
                           subParsers=outputSubParsers)),
                ]) # END MainRun
            ]


class TINKERParserInterface():
   """ A proper class envolop for running this parser from within python. """
   def __init__(self, backend, **kwargs):
       self.backend_factory = backend

   def parse(self, mainfile):
        from unittest.mock import patch
        logging.info('tinker parser started')
        logging.getLogger('nomadcore').setLevel(logging.WARNING)
        backend = self.backend_factory("tinker.nomadmetainfo.json")
        parserInfo = {'name': 'tinker-parser', 'version': '1.0'}
        context = TINKERParser()
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
