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
from .CHARMMDictionary import get_updateDictionary, set_Dictionaries
from .CHARMMCommon import PARSERNAME, PROGRAMNAME, PARSERVERSION, PARSERTAG, LOGGER
from .CHARMMCommon import PARSER_INFO_DEFAULT, META_INFO_PATH, set_excludeList, set_includeList
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
# This is the parser for the main file of CHARMM.
############################################################

parser = None

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

class CHARMMParser(SmartParser.ParserBase):
    """Context for parsing CHARMM main file.

    This class keeps tracks of several CHARMM settings to adjust the parsing to them.
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
                                'energy_total_t0_per_atom': None,
                                'energy_free_per_atom': None,
                               }
        SmartParser.ParserBase.__init__(
            self, re_program_name=re.compile(r"\s*"+PROGRAMNAME+"$"),
            parsertag=PARSERTAG, metainfopath=META_INFO_PATH,
            parserinfodef=PARSER_INFO_DEFAULT, recorderOn=True)

        set_Dictionaries(self)
        self.metaInfoEnv = get_metaInfo(self)
        self.secGIndexDict = {}
        #self.metaStorageRestrict = mStore.Container('section_restricted_uri')
        #self.metaStorageRestrict.build(jsonmetadata, 'section_restricted_uri', {})

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
        if self.recordList:
            self.recordList.close()
        self.recordList = io.StringIO()

    def reset_values(self):
        self.minConverged = None
        self.trajectory = None
        self.newTopo = False
        self.newTraj = False
        self.newIncoord = False
        self.secSystemGIndex = 0
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

    def onOpen_section_run(self, backend, gIndex, section):
        # keep track of the latest section
        self.secRunGIndex = gIndex
        self.secRunOpen = True

    def onClose_section_run(self, backend, gIndex, section):
        """Trigger called when section_run is closed.

        Write the keywords from control parametres and
        the CHARMM output from the parsed log output,
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
        if self.secSamplingGIndex is not None:
            backend.addValue("frame_sequence_to_sampling_method_ref", self.secSamplingGIndex)
        backend.addArrayValues("frame_sequence_to_frames_ref", np.asarray(self.singleConfCalcs))
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
        parmmeta = isMetaStrInDict("prm_file",self.fileDict)
        filename = []
        if parmmeta is not None:
            if self.fileDict[parmmeta].value is not None:
                fname = self.fileDict[parmmeta].value
                filename.append(fname.replace(working_dir_name, '.'+os.path.sep))
        if filename:
            return False, filename, itemdict
        else:
            return False, None, itemdict


    def findUnitFileInIODict(self, theUnit):
        theUnitList=[]
        for secRun, secList in self.inputOutputCards.items():
            if 'open_read' in secList:
                for orunit in secList['open_read']:
                    oreadCmdNo = orunit[0]
                    oreadUnit = orunit[1][0]
                    oreadFile = orunit[1][1]
                    if '@' not in oreadUnit:
                        if int(theUnit) == int(oreadUnit):
                            theUnitList.append((secRun, 'r', oreadCmdNo, oreadFile))
                    else:
                        unitRe = re.compile(oreadUnit.replace('@','[0-9]'))
                        if unitRe.findall(str(theUnit)):
                            theUnitList.append((secRun, 'r', oreadCmdNo, oreadFile))
            if 'open_write' in secList:
                for owunit in secList['open_write']:
                    owriteCmdNo = owunit[0]
                    owriteUnit = owunit[1][0]
                    owriteFile = owunit[1][1]
                    if '@' not in owriteUnit:
                        if int(theUnit) == int(owriteUnit):
                            theUnitList.append((secRun, 'w', owriteCmdNo, owriteFile))
                    else:
                        unitRe = re.compile(owriteUnit.replace('@','[0-9]'))
                        if unitRe.findall(str(theUnit)):
                            theUnitList.append((secRun, 'w', owriteCmdNo, owriteFile))
        if theUnitList:
            return theUnitList
        else:
            return None

    def findTopoFileInIODict(self, parser, theUnit, cmdNo, topoType):
        newTopo = False
        if self.secRunGIndex in self.inputOutputCards:
            if 'open_read' in self.inputOutputCards[self.secRunGIndex]:
                for orunit in self.inputOutputCards[self.secRunGIndex]['open_read']:
                    oreadCmdNo = orunit[0]
                    oreadUnit = orunit[1][0]
                    oreadFile = orunit[1][1]
                    if '@' not in oreadUnit:
                        if int(theUnit) == int(oreadUnit):
                            if 'psf' in topoType:
                                if int(cmdNo) > self.latestTopoFile['psfUnitCmdNo']:
                                    updateTopo = False
                                    if self.latestTopoFile['topoPsfFile'] is None:
                                        updateTopo = True
                                    else:
                                        if oreadFile not in self.latestTopoFile['topoPsfFile']:
                                            updateTopo = True
                                    if updateTopo:
                                        newTopo = True
                                        self.latestTopoFile.update({
                                            'topoPsfFile' : oreadFile,
                                            'topoPsfUnit' : int(theUnit),
                                            'psfUnitCmdNo' : cmdNo,
                                            })
                            if 'rtf' in topoType:
                                if int(cmdNo) > self.latestTopoFile['rtfUnitCmdNo']:
                                    updateTopo = False
                                    if self.latestTopoFile['topoRtfFile'] is None:
                                        updateTopo = True
                                    else:
                                        if oreadFile not in self.latestTopoFile['topoRtfFile']:
                                            updateTopo = True
                                    if updateTopo:
                                        newTopo = True
                                        self.latestTopoFile.update({
                                            'topoRtfFile' : oreadFile,
                                            'topoRtfUnit' : int(theUnit),
                                            'rtfUnitCmdNo' : cmdNo,
                                            })
                            if 'par' in topoType:
                                if int(cmdNo) > self.latestTopoFile['parUnitCmdNo']:
                                    updateTopo = False
                                    if self.latestTopoFile['topoParFile'] is None:
                                        updateTopo = True
                                    else:
                                        if oreadFile not in self.latestTopoFile['topoParFile']:
                                            updateTopo = True
                                    if updateTopo:
                                        newTopo = True
                                        self.latestTopoFile.update({
                                            'topoParFile' : oreadFile,
                                            'topoParUnit' : int(theUnit),
                                            'parUnitCmdNo' : cmdNo,
                                            })
                            if 'cor' in topoType:
                                if int(cmdNo) > self.latestTopoFile['corUnitCmdNo']:
                                    updateTopo = False
                                    if self.latestTopoFile['topoCorFile'] is None:
                                        updateTopo = True
                                    else:
                                        if oreadFile not in self.latestTopoFile['topoCorFile']:
                                            updateTopo = True
                                    if updateTopo:
                                        newTopo = True
                                        self.latestTopoFile.update({
                                            'topoCorFile' : oreadFile,
                                            'topoCorUnit' : int(theUnit),
                                            'corUnitCmdNo' : cmdNo,
                                            })
            if 'open_write' in self.inputOutputCards[self.secRunGIndex]:
                for owunit in self.inputOutputCards[self.secRunGIndex]['open_write']:
                    owriteCmdNo = owunit[0]
                    owriteUnit = owunit[1][0]
                    owriteFile = owunit[1][1]
                    if '@' not in owriteUnit:
                        if int(theUnit) == int(owriteUnit):
                            if 'psf' in topoType:
                                if int(cmdNo) > self.latestTopoFile['psfUnitCmdNo']:
                                    update=False
                                    if self.latestTopoFile['topoPsfFile'] is not None:
                                        if owriteFile not in self.latestTopoFile['topoPsfFile']:
                                            update=True
                                    else:
                                        update=True
                                    if update:
                                        newTopo = True
                                        self.latestTopoFile.update({
                                            'topoPsfFile' : owriteFile,
                                            'topoPsfUnit' : int(theUnit),
                                            'psfUnitCmdNo' : cmdNo,
                                            })
                            if 'rtf' in topoType:
                                if int(cmdNo) > self.latestTopoFile['rtfUnitCmdNo']:
                                    update=False
                                    if self.latestTopoFile['topoRtfFile'] is not None:
                                        if owriteFile not in self.latestTopoFile['topoRtfFile']:
                                            update=True
                                    else:
                                        update=True
                                    if update:
                                        newTopo = True
                                        self.latestTopoFile.update({
                                            'topoRtfFile' : owriteFile,
                                            'topoRtfUnit' : int(theUnit),
                                            'rtfUnitCmdNo' : cmdNo,
                                            })
                            if 'par' in topoType:
                                if int(cmdNo) > self.latestTopoFile['parUnitCmdNo']:
                                    update=False
                                    if self.latestTopoFile['topoParFile'] is not None:
                                        if owriteFile not in self.latestTopoFile['topoParFile']:
                                            update=True
                                    else:
                                        update=True
                                    if update:
                                        newTopo = True
                                        self.latestTopoFile.update({
                                            'topoParFile' : owriteFile,
                                            'topoParUnit' : int(theUnit),
                                            'parUnitCmdNo' : cmdNo,
                                            })
                            if 'cor' in topoType:
                                if int(cmdNo) > self.latestTopoFile['corUnitCmdNo']:
                                    update=False
                                    if self.latestTopoFile['topoCorFile'] is not None:
                                        if owriteFile not in self.latestTopoFile['topoCorFile']:
                                            update=True
                                    else:
                                        update=True
                                    if update:
                                        newTopo = True
                                        self.latestTopoFile.update({
                                            'topoCorFile' : owriteFile,
                                            'topoCorUnit' : int(theUnit),
                                            'corUnitCmdNo' : cmdNo,
                                            })
        return newTopo

    def charmm_input_output_files(self, backend, gIndex, section):
        """Called with onClose_x_charmm_section_control_parameters to setup
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
            if k.startswith(PARSERTAG + '_inout_file'):
                self.fileDict[k].value = None
                self.fileDict[k].activeInfo = False
                self.fileDict[k].fileSupplied = False

        topoData = [(
            x, self.latestTopoFile[x]
            ) for x in self.latestTopoFile if(
                'CmdNo' in x and self.latestTopoFile[x]>-1
                )]
        topoData.sort(reverse=True, key=lambda tup: tup[1])

        if self.newTopo:
            # Here we go updating topology info
            # Check list from most recent PSF file
            fKey = PARSERTAG + '_inout_file_'
            topoDone=False
            topoPsf=False
            topoPar=False
            topoRtf=False
            topoCor=False
            if topoData:
                for topoCmd in topoData:
                    if 'psf' in topoCmd[0]:
                        topoFile = self.latestTopoFile['topoPsfFile'].upper()
                        if topoFile in self.filesInOutputDir:
                            file_name = self.filesInOutputDir[topoFile]
                            self.fileDict[fKey+'structure'].value = file_name.replace(working_dir_name+'/', '')
                            self.fileDict[fKey+'structure'].fileName = file_name
                            self.fileDict[fKey+'structure'].activeInfo = True
                            self.fileDict[fKey+'structure'].fileSupplied = True
                            atLeastOneFileExist = True
                            topoDone = True
                            topoPsf=True
                    if 'par' in topoCmd[0]:
                        if 'Unit' in topoCmd[0]:
                            topoFile = self.latestTopoFile['topoParFile'].upper()
                            if topoFile in self.filesInOutputDir:
                                file_name = self.filesInOutputDir[topoFile]
                                self.fileDict[fKey+'prm_file'].value = file_name.replace(working_dir_name+'/', '')
                                self.fileDict[fKey+'prm_file'].fileName = file_name
                                self.fileDict[fKey+'prm_file'].activeInfo = True
                                self.fileDict[fKey+'prm_file'].fileSupplied = True
                                atLeastOneFileExist = True
                                topoDone = True
                                topoPar=True
                        elif 'Str' in topoCmd[0]:
                            if self.fileDict[fKey+'stream'].value is None:
                                self.fileDict[fKey+'stream'].value = 'input parameter card'
                            else:
                                self.fileDict[fKey+'stream'].value = self.fileDict[
                                        fKey+'stream'].value + ', input parameter card'
                            if self.fileDict[fKey+'stream'].strDict is None:
                                self.fileDict[fKey+'stream'].strDict = self.latestTopoFile['topoStrDict']
                            else:
                                self.fileDict[fKey+'stream'].strDict.update(self.latestTopoFile['topoStrDict'])
                            self.fileDict[fKey+'stream'].fileName = None
                            self.fileDict[fKey+'stream'].activeInfo = True
                            self.fileDict[fKey+'stream'].fileSupplied = True
                            atLeastOneFileExist = True
                            topoDone = True
                            topoPar=True
                    if 'rtf' in topoCmd[0]:
                        if 'Unit' in topoCmd[0]:
                            topoFile = self.latestTopoFile['topoRtfFile'].upper()
                            if topoFile in self.filesInOutputDir:
                                file_name = self.filesInOutputDir[topoFile]
                                self.fileDict[fKey+'rtf_file'].value = file_name.replace(working_dir_name+'/', '')
                                self.fileDict[fKey+'rtf_file'].fileName = file_name
                                self.fileDict[fKey+'rtf_file'].activeInfo = True
                                self.fileDict[fKey+'rtf_file'].fileSupplied = True
                                atLeastOneFileExist = True
                                topoDone = True
                                topoRtf=True
                        elif 'Str' in topoCmd[0]:
                            if self.fileDict[fKey+'stream'].value is None:
                                self.fileDict[fKey+'stream'].value = 'input rtf card'
                            else:
                                self.fileDict[fKey+'stream'].value = self.fileDict[
                                        fKey+'stream'].value + ', input rtf card'
                            if self.fileDict[fKey+'stream'].strDict is None:
                                self.fileDict[fKey+'stream'].strDict = self.latestTopoFile['topoStrDict']
                            else:
                                self.fileDict[fKey+'stream'].strDict.update(self.latestTopoFile['topoStrDict'])
                            self.fileDict[fKey+'stream'].fileName = None
                            self.fileDict[fKey+'stream'].activeInfo = True
                            self.fileDict[fKey+'stream'].fileSupplied = True
                            atLeastOneFileExist = True
                            topoDone = True
                            topoRtf=True
                    if 'cor' in topoCmd[0]:
                        if 'Unit' in topoCmd[0]:
                            topoFile = self.latestTopoFile['topoCorFile'].upper()
                            if topoFile in self.filesInOutputDir:
                                file_name = self.filesInOutputDir[topoFile]
                                self.fileDict[fKey+'cor_file'].value = file_name.replace(working_dir_name+'/', '')
                                self.fileDict[fKey+'cor_file'].fileName = file_name
                                self.fileDict[fKey+'cor_file'].activeInfo = True
                                self.fileDict[fKey+'cor_file'].fileSupplied = True
                                atLeastOneFileExist = True
                                topoDone = True
                                topoCor=True
                        elif 'Str' in topoCmd[0]:
                            if self.fileDict[fKey+'stream'].value is None:
                                self.fileDict[fKey+'stream'].value = 'input coor card'
                            else:
                                self.fileDict[fKey+'stream'].value = self.fileDict[
                                        fKey+'stream'].value + ', input coor card'
                            if self.fileDict[fKey+'stream'].strDict is None:
                                self.fileDict[fKey+'stream'].strDict = self.latestTopoFile['topoStrDict']
                            else:
                                self.fileDict[fKey+'stream'].strDict.update(self.latestTopoFile['topoStrDict'])
                            self.fileDict[fKey+'stream'].fileName = None
                            self.fileDict[fKey+'stream'].activeInfo = True
                            self.fileDict[fKey+'stream'].fileSupplied = True
                            atLeastOneFileExist = True
                            topoDone = True
                            topoCor=True
                    elif 'corprint' in topoCmd[0]:
                        if 'Str' in topoCmd[0]:
                            if self.fileDict[fKey+'stream'].value is None:
                                self.fileDict[fKey+'stream'].value = 'print coor card'
                            else:
                                self.fileDict[fKey+'stream'].value = self.fileDict[
                                        fKey+'stream'].value + ', print coor card'
                            if self.fileDict[fKey+'stream'].strDict is None:
                                self.fileDict[fKey+'stream'].strDict = self.latestTopoFile['topoStrDict']
                            else:
                                self.fileDict[fKey+'stream'].strDict.update(self.latestTopoFile['topoStrDict'])
                            self.fileDict[fKey+'stream'].fileName = None
                            self.fileDict[fKey+'stream'].activeInfo = True
                            self.fileDict[fKey+'stream'].fileSupplied = True
                            atLeastOneFileExist = True
                            topoDone = True
                            topoCor=True
                    if topoPar and topoRtf and topoPsf:
                        break
                    elif topoPar and topoRtf and topoCor:
                        break


        if self.newIncoord is False:
            fKey = PARSERTAG + '_inout_file_'
            if topoData is not None:
                for topoCmd in topoData:
                    if 'cor' in topoCmd[0]:
                        if 'Unit' in topoCmd[0]:
                            topoFile = self.latestTopoFile['topoCorFile'].upper()
                            if topoFile in self.filesInOutputDir:
                                file_name = self.filesInOutputDir[topoFile]
                                self.latestTrajFile['incoordFile']=topoFile
                                self.fileDict[fKey+'cor_file'].value = file_name.replace(working_dir_name+'/', '')
                                self.fileDict[fKey+'cor_file'].fileName = file_name
                                self.fileDict[fKey+'cor_file'].activeInfo = True
                                self.fileDict[fKey+'cor_file'].fileSupplied = True
                                atLeastOneFileExist = True
                                self.newIncoord = True
                                break
                        elif 'Str' in topoCmd[0]:
                            if self.latestTopoFile['topoStrDict'] is not None:
                                if 'cor' in self.latestTopoFile['topoStrDict']:
                                    self.latestTrajFile['incoordStr']={'cor' : self.latestTopoFile['topoStrDict']['cor']}
                            if self.fileDict[fKey+'stream'].strDict is None:
                                self.fileDict[fKey+'stream'].strDict = self.latestTopoFile['topoStrDict']
                            else:
                                self.fileDict[fKey+'stream'].strDict.update(self.latestTopoFile['topoStrDict'])
                            if self.fileDict[fKey+'stream'].value is None:
                                self.fileDict[fKey+'stream'].value = 'input coor card'
                            else:
                                self.fileDict[fKey+'stream'].value = self.fileDict[
                                        fKey+'stream'].value + ', input coor card'
                            self.fileDict[fKey+'stream'].fileName = None
                            self.fileDict[fKey+'stream'].activeInfo = True
                            self.fileDict[fKey+'stream'].fileSupplied = True
                            atLeastOneFileExist = True
                            self.newIncoord = True
                            break
                    elif 'corprint' in topoCmd[0]:
                        if 'Str' in topoCmd[0]:
                            if self.latestTopoFile['topoStrDict'] is not None:
                                if 'cor_print' in self.latestTopoFile['topoStrDict']:
                                    self.latestTrajFile['incoordStr']={'cor' : self.latestTopoFile['topoStrDict']['cor_print']}
                            if self.fileDict[fKey+'stream'].strDict is None:
                                self.fileDict[fKey+'stream'].strDict = self.latestTopoFile['topoStrDict']
                            else:
                                self.fileDict[fKey+'stream'].strDict.update(self.latestTopoFile['topoStrDict'])
                            if self.fileDict[fKey+'stream'].value is None:
                                self.fileDict[fKey+'stream'].value = 'print coor card'
                            else:
                                self.fileDict[fKey+'stream'].value = self.fileDict[
                                        fKey+'stream'].value + 'print coor card'
                            self.fileDict[fKey+'stream'].fileName = None
                            self.fileDict[fKey+'stream'].activeInfo = True
                            self.fileDict[fKey+'stream'].fileSupplied = True
                            atLeastOneFileExist = True
                            topoDone = True
                            topoCor=True

        if self.newIncoord:
            fKey = PARSERTAG + '_inout_file_'
            IncoordDone=False
            if self.latestTrajFile['inrstFile'] is not None:
                incoordFile = self.latestTrajFile['inrstFile'].upper()
                if incoordFile in self.filesInOutputDir:
                    file_name = self.filesInOutputDir[incoordFile]
                    self.fileDict[fKey+'input_coord'].value = file_name.replace(working_dir_name+'/', '')
                    self.fileDict[fKey+'input_coord'].fileName = file_name
                    self.fileDict[fKey+'input_coord'].activeInfo = True
                    self.fileDict[fKey+'input_coord'].fileSupplied = True
                    atLeastOneFileExist = True
                    IncoordDone = True
            elif self.latestTrajFile['incoordFile'] is not None:
                incoordFile = self.latestTrajFile['incoordFile'].upper()
                if incoordFile in self.filesInOutputDir:
                    file_name = self.filesInOutputDir[incoordFile]
                    self.fileDict[fKey+'input_coord'].value = file_name.replace(working_dir_name+'/', '')
                    self.fileDict[fKey+'input_coord'].fileName = file_name
                    self.fileDict[fKey+'input_coord'].activeInfo = True
                    self.fileDict[fKey+'input_coord'].fileSupplied = True
                    atLeastOneFileExist = True
                    IncoordDone = True
            if self.latestTrajFile['incoordStr'] is not None:
                if self.fileDict[fKey+'in_coor_str'].strDict is None:
                    self.fileDict[fKey+'in_coor_str'].strDict = self.latestTrajFile['incoordStr']
                else:
                    self.fileDict[fKey+'in_coor_str'].strDict.update(self.latestTrajFile['incoordStr'])
                self.fileDict[fKey+'in_coor_str'].value = 'input coor card'
                self.fileDict[fKey+'in_coor_str'].fileName = None
                self.fileDict[fKey+'in_coor_str'].activeInfo = True
                self.fileDict[fKey+'in_coor_str'].fileSupplied = True
                atLeastOneFileExist = True
                IncoordDone = True

            # If we only have a new CRD file or COOR card and
            # have already a previous topology, we skip the new
            # coordinate file but if there is no topology
            # info and we have only coordinate stream/text-file, we
            # extract atom/residue types from this stream/text-file.
            #
            #
            # So we have a new topology and
            # topology streams and files can be set.
            # Move on to initilize them.

        if self.newTraj:
            fKey = PARSERTAG + '_inout_file_'
            trajDone=False
            if self.latestTrajFile['trajFile'] is not None:
                trajFile = self.latestTrajFile['trajFile'].upper()
                if trajFile in self.filesInOutputDir:
                    file_name = self.filesInOutputDir[trajFile]
                    self.fileDict[fKey+'trajectory'].value = file_name.replace(working_dir_name+'/', '')
                    self.fileDict[fKey+'trajectory'].fileName = file_name
                    self.fileDict[fKey+'trajectory'].activeInfo = True
                    self.fileDict[fKey+'trajectory'].fileSupplied = True
                    atLeastOneFileExist = True
                    trajDone = True
            elif self.latestTrajFile['outrstFile'] is not None:
                trajFile = self.latestTrajFile['outrstFile'].upper()
                if trajFile in self.filesInOutputDir:
                    file_name = self.filesInOutputDir[trajFile]
                    self.fileDict[fKey+'output_coord'].value = file_name.replace(working_dir_name+'/', '')
                    self.fileDict[fKey+'output_coord'].fileName = file_name
                    self.fileDict[fKey+'output_coord'].activeInfo = True
                    self.fileDict[fKey+'output_coord'].fileSupplied = True
                    atLeastOneFileExist = True
                    trajDone = True

        #if atLeastOneFileExist:
        #    updateDict = {
        #            'startSection'   : [[PARSERTAG+'_section_input_output_files']],
        #            'dictionary'     : self.fileDict
        #            }
        #    self.metaStorage.update(updateDict)
        #    self.metaStorage.updateBackend(backend.superBackend,
        #            startsection=[PARSERTAG+'_section_input_output_files'],
        #            autoopenclose=False)
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
                self.topology.n_atoms = self.numatoms
                self.topology._numAtoms = self.numatoms
                #self.MDData.initializeOutputCoordinateFileHandlers(self)
                #self.MDData.initializeFileHandlers(self)
                #if self.outputcoords:
                #    self.outputpositions = self.outputcoords.positions()

    def onOpen_x_charmm_section_control_parameters(self, backend, gIndex, section):
        # keep track of the latest section
        if self.inputControlIndex is None:
            self.inputControlIndex = gIndex

    def onClose_x_charmm_section_control_parameters(self, backend, gIndex, section):
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
        # CHARMM prints the initial and final energies to the log file.
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
        urstreadKey = None
        urstwriteKey = None
        ucrdwriteKey = None
        uvelwriteKey = None
        uxyzwriteKey = None
        urstread = -1
        urstwrite = -1
        ucrdwrite = -1
        uvelwrite = -1
        uxyzwrite = -1
        topoCmdNo = None
        # Check if the section is in input-output Cards info:
        #     self.inputOutputCards
        try:
            getattr(self, "latestTopoFile")
        except AttributeError:
            self.latestTopoFile = {}
            self.latestTopoFile.update({
                'topoPsfFile' : None,
                'topoStrDict' : None,
                'topoRtfFile' : None,
                'topoParFile' : None,
                'topoCorFile' : None,
                'topoPsfUnit' : -1,
                'topoRtfUnit' : -1,
                'topoParUnit' : -1,
                'topoCorUnit' : -1,
                'psfUnitCmdNo' : -1,
                'rtfUnitCmdNo' : -1,
                'parUnitCmdNo' : -1,
                'corUnitCmdNo' : -1,
                'rtfStrCmdNo' : -1,
                'parStrCmdNo' : -1,
                'corStrCmdNo' : -1,
                'corprintStrCmdNo' : -1,
                })
        if 'topoStrDict' in self.latestTopoFile:
            if self.latestTopoFile['topoStrDict'] is not None:
                topoStrDict=self.latestTopoFile['topoStrDict']
            else:
                topoStrDict={}
#        try:
#            getattr(self, "latestTrajFile")
#        except AttributeError:
        self.latestTrajFile = {}
        self.latestTrajFile.update({
            'trajFile' : None,
            'velFile' : None,
            'xyzFile' : None,
            'inrstFile' : None,
            'outrstFile' : None,
            'incoordFile' : None,
            'outcoordFile' : None,
            'incoordStr' : None,
            'outcoordStr' : None,
            })
        self.newTopo = False
        self.newTraj = False
        self.newIncoord = False
        if self.secRunGIndex in self.inputOutputCards:
            # check if section has a new topology
            if 'psf' in self.inputOutputCards[self.secRunGIndex]:
                if len(self.inputOutputCards[self.secRunGIndex]['psf'])>0:
                    latestpsf = self.inputOutputCards[self.secRunGIndex]['psf'][-1]
                    topoCmdNo = latestpsf[0]
                    psfunit = latestpsf[1]
                    if self.findTopoFileInIODict(parser, psfunit, topoCmdNo, 'psf'):
                        self.newTopo = True
            if 'psf_write' in self.inputOutputCards[self.secRunGIndex]:
                if len(self.inputOutputCards[self.secRunGIndex]['psf_write'])>0:
                    latestpsf = self.inputOutputCards[self.secRunGIndex]['psf_write'][-1]
                    topoCmdNo = latestpsf[0]
                    psfunit = latestpsf[1]
                    if self.findTopoFileInIODict(parser, psfunit, topoCmdNo, 'psf_write'):
                        self.newTopo = True
            if 'rtf' in self.inputOutputCards[self.secRunGIndex]:
                if len(self.inputOutputCards[self.secRunGIndex]['rtf'])>0:
                    latestrtf = self.inputOutputCards[self.secRunGIndex]['rtf'][-1]
                    topoCmdNo = latestrtf[0]
                    rtfunit = latestrtf[1]
                    if isinstance(rtfunit, list):
                        if int(topoCmdNo) > self.latestTopoFile['rtfStrCmdNo']:
                            topoStrDict.update({'rtf' : rtfunit})
                            self.latestTopoFile.update({
                                'topoStrDict' : topoStrDict,
                                'rtfStrCmdNo' : topoCmdNo,
                                })
                            self.newTopo = True
                    else:
                        if self.findTopoFileInIODict(parser, rtfunit, topoCmdNo, 'rtf'):
                            self.newTopo = True
            if 'par' in self.inputOutputCards[self.secRunGIndex]:
                if len(self.inputOutputCards[self.secRunGIndex]['par'])>0:
                    latestpar = self.inputOutputCards[self.secRunGIndex]['par'][-1]
                    topoCmdNo = latestpar[0]
                    parunit = latestpar[1]
                    if isinstance(parunit, list):
                        if int(topoCmdNo) > self.latestTopoFile['parStrCmdNo']:
                            topoStrDict.update({'par' : parunit})
                            self.latestTopoFile.update({
                                'topoStrDict' : topoStrDict,
                                'parStrCmdNo' : topoCmdNo,
                                })
                            self.newTopo = True
                    else:
                        if self.findTopoFileInIODict(parser, parunit, topoCmdNo, 'par'):
                            self.newTopo = True
            if 'cor' in self.inputOutputCards[self.secRunGIndex]:
                if len(self.inputOutputCards[self.secRunGIndex]['cor'])>0:
                    latestcor = self.inputOutputCards[self.secRunGIndex]['cor'][-1]
                    topoCmdNo = latestcor[0]
                    corunit = latestcor[1]
                    if isinstance(corunit, list):
                        if int(topoCmdNo) > self.latestTopoFile['corStrCmdNo']:
                            topoStrDict.update({'cor' : corunit})
                            self.latestTopoFile.update({
                                'topoStrDict' : topoStrDict,
                                'corStrCmdNo' : topoCmdNo,
                                })
                            #self.newIncoord = True
                    else:
                        if self.findTopoFileInIODict(parser, corunit, topoCmdNo, 'cor'):
                            pass
                            #self.newIncoord = True
            elif 'cor_print' in self.inputOutputCards[self.secRunGIndex]:
                if len(self.inputOutputCards[self.secRunGIndex]['cor_print'])>0:
                    latestcor = self.inputOutputCards[self.secRunGIndex]['cor_print'][-1]
                    topoCmdNo = latestcor[0]
                    corunit = latestcor[1]
                    if isinstance(corunit, list):
                        if int(topoCmdNo) > self.latestTopoFile['corStrCmdNo']:
                            topoStrDict.update({'cor' : corunit})
                            self.latestTopoFile.update({
                                'topoStrDict' : topoStrDict,
                                'corprintStrCmdNo' : topoCmdNo,
                                })
                            #self.newIncoord = True

        # Restart read unit
        urstreadKey = isMetaStrInDict("IUNREA",self.cntrlDict)
        # Restart write unit
        urstwriteKey = isMetaStrInDict("IUNWRI",self.cntrlDict)
        # Trajectory positions write unit
        ucrdwriteKey = isMetaStrInDict("IUNCRD",self.cntrlDict)
        # Trajectory velocities write unit
        uvelwriteKey = isMetaStrInDict("IUNVEL",self.cntrlDict)
        # Trajectory positions,velocities and forces write unit
        uxyzwriteKey = isMetaStrInDict("IUNXYZ",self.cntrlDict)
        if urstreadKey is not None:
            if self.cntrlDict[urstreadKey].activeInfo:
                urstread = conv_int(self.cntrlDict[urstreadKey].value, default=-1)
        if urstwriteKey is not None:
            if self.cntrlDict[urstwriteKey].activeInfo:
                urstwrite = conv_int(self.cntrlDict[urstwriteKey].value, default=-1)
        if ucrdwriteKey is not None:
            if self.cntrlDict[ucrdwriteKey].activeInfo:
                ucrdwrite = conv_int(self.cntrlDict[ucrdwriteKey].value, default=-1)
        if uvelwriteKey is not None:
            if self.cntrlDict[uvelwriteKey].activeInfo:
                uvelwrite = conv_int(self.cntrlDict[uvelwriteKey].value, default=-1)
        if uxyzwriteKey is not None:
            if self.cntrlDict[uxyzwriteKey].activeInfo:
                uxyzwrite = conv_int(self.cntrlDict[uxyzwriteKey].value, default=-1)

        if ucrdwrite>-1:
            newTrajCrd=False
            trajFile=None
            ucrdwriteList = self.findUnitFileInIODict(ucrdwrite)
            ucrdwriteList.sort(reverse=True, key=lambda tup: tup[0])
            for oact in ucrdwriteList:
                if 'w' in oact[1]:
                    if oact[0]>self.secRunGIndex:
                        break
                    else:
                        trajFile=oact[3]
                        newTrajCrd=True
                        break
            if newTrajCrd:
                self.newTraj=True
                self.latestTrajFile.update({'trajFile' : trajFile})

        if self.newIncoord is False:
            if urstread>-1:
                newRstRead=False
                trajFile=None
                urstreadList = self.findUnitFileInIODict(urstread)
                urstreadList.sort(reverse=True, key=lambda tup: tup[0])
                for oact in urstreadList:
                    if 'r' in oact[1]:
                        if oact[0]>self.secRunGIndex:
                            break
                        else:
                            trajFile=oact[3]
                            newRstRead=True
                            break
                if newRstRead:
                    self.newIncoord=True
                    self.latestTrajFile.update({'inrstFile' : trajFile})

        if self.newTraj is False:
            if urstwrite>-1:
                newRstWrite=False
                trajFile=None
                urstwriteList = self.findUnitFileInIODict(urstwrite)
                urstwriteList.sort(reverse=True, key=lambda tup: tup[0])
                for oact in urstwriteList:
                    if 'w' in oact[1]:
                        if oact[0]>self.secRunGIndex:
                            break
                        else:
                            trajFile=oact[3]
                            newRstWrite=True
                            break
                if newRstWrite:
                    self.newTraj=True
                    self.latestTrajFile.update({'outrstFile' : trajFile})

        self.charmm_input_output_files(backend, gIndex, section)

        nstructKey = isMetaStrInDict("STRUCTURE FILE",self.cntrlDict)
        #ninputKey = isMetaStrInDict("OPEN COOR",self.cntrlDict)
        noutputKey = isMetaStrInDict("WRITE COOR",self.cntrlDict)
        nstepKey = isMetaStrInDict("NSTEP", self.cntrlDict)
        nlogKey = isMetaStrInDict("NPRINT", self.cntrlDict)
        nxoutKey = isMetaStrInDict("NSAVC", self.cntrlDict)
        nvoutKey = isMetaStrInDict("NSAVV", self.cntrlDict)
        nfxyzoutKey = isMetaStrInDict("NSAVX", self.cntrlDict)
        if nstepKey is not None:
            if self.cntrlDict[nstepKey].activeInfo:
                nsteps = conv_int(self.cntrlDict[nstepKey].value, default=0)
            else:
                nsteps = conv_int(self.cntrlDict[nstepKey].defaultValue, default=0)
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
            if self.cntrlDict[nstructKey].activeInfo:
                nstructstep = 1
        #if ninputKey is not None:
        #    if self.cntrlDict[ninputKey].activeInfo:
        #        ninputstep = 1
        if noutputKey is not None:
            if self.cntrlDict[noutputKey].activeInfo:
                noutputstep = 1
        if nvoutKey is not None:
            if self.cntrlDict[nvoutKey].activeInfo:
                nvelsteps = conv_int(self.cntrlDict[nvoutKey].value, default=0)
        #if nfxyzoutKey is not None:
        #    if self.cntrlDict[nfxyzoutKey].activeInfo:
        #        nforcesteps = conv_int(self.cntrlDict[nfxyzoutKey].value, default=0)

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
                #updateDict = {
                #        'startSection'   : [[PARSERTAG+'_section_input_output_files']],
                #        'dictionary' : self.sectionInoutDict
                #        }
                #self.metaStorage.update(updateDict)
                #self.metaStorage.updateBackend(backend.superBackend,
                #        startsection=[PARSERTAG+'_section_input_output_files'],
                #        autoopenclose=False)

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

        # CHARMM default unit vectors. If all are zeros than the simulation cell is not periodic.
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
                    coordinates.unitcell_vectors, "Angstrom", self.unitDict))
                SloppyBackend.addArrayValues('simulation_cell', unit_cell)
                SloppyBackend.addArrayValues('lattice_vectors', unit_cell)
            if coordinates.unitcell_lengths is not None:
                SloppyBackend.addArrayValues(PARSERTAG + '_lattice_lengths', coordinates.unitcell_lengths)
            if coordinates.unitcell_angles is not None:
                SloppyBackend.addArrayValues(PARSERTAG + '_lattice_angles', coordinates.unitcell_angles)
            # CHARMM Guide says: (See http://www.ks.uiuc.edu/Research/charmm/2.12/ug/node11.html)
            # Positions in PDB/CHARMM binary/DCD files are stored in A.
            #pos_obj = getattr(self.trajectory, 'positions', None)
            #if callable(pos_obj):
            SloppyBackend.addArrayValues('atom_positions', np.transpose(np.asarray(
                self.metaStorage.convertUnits(positions, "Angstrom", self.unitDict))))
            if coordinates.velocities is not None:
                # Velocities in PDB files are stored in A/ps units.(PDB files are read for input
                #     coordinates, velocities, and forces)
                # Velocities in CHARMM binary/DCD files are stored in CHARMM internal units and must be multiplied
                #     by PDBVELFACTOR=20.45482706 to convert to A/ps. (These files are used for output trajectory)
                SloppyBackend.addArrayValues('atom_velocities', np.transpose(np.asarray(
                    self.metaStorage.convertUnits(
                        coordinates.velocities, "20.45482706*Angstrom/(pico-second)", self.unitDict))))
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
                    ['section_energy_van_der_waals']],
                #'muteSections' : [['section_sampling_method']],
                'dictionary' : section_singlevdw_Dict
                }
            self.secVDWGIndex = backend.superBackend.openSection("section_energy_van_der_waals")
            self.metaStorage.update(updateDictVDW)
            self.metaStorage.updateBackend(backend.superBackend,
                    startsection=['section_energy_van_der_waals'],
                    autoopenclose=False)
            backend.superBackend.closeSection("section_energy_van_der_waals", self.secVDWGIndex)
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
                # Forces in PDB/CHARMM binary/DCD files are stored in kcal/mol/A
                SloppyBackend.addArrayValues('atom_forces_xxx', np.transpose(np.asarray(
                    self.metaStorage.convertUnits(
                        self.atompositions.velocities, "kcal/(mol*Angstrom)", self.unitDict))))
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

    def fileReadWriteSave(self, fname, value):
        readin = isMetaStrInDict("READ",self.filecntrlDict)
        writein = isMetaStrInDict("WRITE",self.filecntrlDict)
        cardin = isMetaStrInDict("CARD",self.filecntrlDict)
        unitin = isMetaStrInDict("UNIT",self.filecntrlDict)
        readattr=None
        writeattr=None
        cardattr=None
        unitattr=None
        if readin is not None:
            if self.filecntrlDict[readin].value is not None:
                readattr = self.filecntrlDict[readin].value
                readattr = readattr.upper()
        if writein is not None:
            if self.filecntrlDict[writein].value is not None:
                writeattr = self.filecntrlDict[writein].value
                writeattr = writeattr.upper()
        cmdattr=None
        if readattr is not None:
            cmdattr=readattr
        if writeattr is not None:
            cmdattr=writeattr
        if cardin is not None:
            if self.filecntrlDict[cardin].value is not None:
                cardattr = self.filecntrlDict[cardin].value
                cardattr = cardattr.upper()
        if unitin is not None:
            if self.filecntrlDict[unitin].value is not None:
                unitattr = self.filecntrlDict[unitin].value
                unitattr = unitattr.upper()
        if unitattr is not None and self.fileUnitDict is not None:
            if unitattr in self.fileUnitDict:
                name=self.fileUnitDict[unitattr]['filename']
                fformat=self.fileUnitDict[unitattr]['fileformat']
                ftype=self.fileUnitDict[unitattr]['filetype']
                reason=self.fileUnitDict[unitattr]['reason']
                status=self.fileUnitDict[unitattr]['open']
                handle=self.fileUnitDict[unitattr]['handle']
                if cmdattr is not None:
                    if('RTF' in cmdattr or cmdattr.startswith('RTF')):
                        fformat = '.rtf'
                        ftype = 'charmmresidue'
                    if('PSF' in cmdattr or cmdattr.startswith('PSF')):
                        fformat = '.psf'
                        ftype = 'structure'
                    if('PARA' in cmdattr or cmdattr.startswith('PARA')):
                        fformat = '.par'
                        ftype = 'charmmforcefield'
                    if('COOR' in cmdattr or cmdattr.startswith('COOR')):
                        fformat = '.charmmcor'
                        if readattr is not None:
                            ftype = 'inputcoordinates'
                        if writeattr is not None:
                            ftype = 'outputcoordinates'
                    if(unitattr in self.fileUnitDict and
                       name not in self.fileUnitDict[unitattr]['filename']):
                        newunitattr = unitattr + '_' + str(int(unitattr)+1)
                        if newunitattr in self.fileUnitDict:
                            newunitattr = unitattr + '_' + str(int(
                                newunitattr.split('_')[1])+1)
                        self.fileUnitDict.update({
                            newunitattr : {
                                'filename'   : self.fileUnitDict[unitattr]['filename'],
                                'fileformat' : self.fileUnitDict[unitattr]['fileformat'],
                                'filetype'   : self.fileUnitDict[unitattr]['filetype'],
                                'reason'     : self.fileUnitDict[unitattr]['reason'],
                                'open'       : self.fileUnitDict[unitattr]['open'],
                                'handle'     : self.fileUnitDict[unitattr]['handle']
                                }
                            })
                    self.fileUnitDict.update({
                        unitattr : {
                            'filename'   : name,
                            'fileformat' : fformat,
                            'filetype'   : ftype,
                            'reason'     : reason,
                            'open'       : status,
                            'handle'     : handle
                            }
                        })
        return value

    def fileNameTrans(self, fname, value):
        openin = isMetaStrInDict("OPEN",self.filecntrlDict)
        unitin = isMetaStrInDict("UNIT",self.filecntrlDict)
        namein = isMetaStrInDict("NAME",self.filecntrlDict)
        pathin = isMetaStrInDict("Parameter:",self.filecntrlDict)
        openattr=None
        unitattr=None
        nameattr=None
        paraattr=None
        pathattr=None
        if openin is not None:
            if self.filecntrlDict[openin].value is not None:
                openattr = self.filecntrlDict[openin].value
                openattr = openattr.strip()
        if unitin is not None:
            if self.filecntrlDict[unitin].value is not None:
                unitattr = self.filecntrlDict[unitin].value
                unitattr = unitattr.strip()
        if namein is not None:
            if self.filecntrlDict[namein].value is not None:
                nameattr = self.filecntrlDict[namein].value
                nameattr = nameattr.strip()
        if pathin is not None:
            if self.filecntrlDict[pathin].value is not None:
                pathpara = self.filecntrlDict[pathin].value
                pathpara.replace('\n', '')
                paraattr = '@' + pathpara.split('->')[0]
                pathattr = pathpara.split('->')[1].replace('"','')
                paraattr = paraattr.strip()
                pathattr = pathattr.strip()
        if(openattr is not None and unitattr is not None and
           nameattr is not None and pathattr is not None):
            name=None
            try:
                name = nameattr.replace(str(paraattr),str(pathattr))
                if name:
                    name = self.working_dir_name + '/' + name
            except(TypeError,AttributeError):
                pass
            if name is not None:
                if(unitattr in self.fileUnitDict and
                   name not in self.fileUnitDict[unitattr]['filename']):
                    newunitattr = unitattr + '_' + str(int(unitattr)+1)
                    if newunitattr in self.fileUnitDict:
                        newunitattr = unitattr + '_' + str(int(
                            newunitattr.split('_')[1])+1)
                    self.fileUnitDict.update({
                        newunitattr : {
                            'filename'   : self.fileUnitDict[unitattr]['filename'],
                            'fileformat' : self.fileUnitDict[unitattr]['fileformat'],
                            'filetype'   : self.fileUnitDict[unitattr]['filetype'],
                            'reason'     : self.fileUnitDict[unitattr]['reason'],
                            'open'       : self.fileUnitDict[unitattr]['open'],
                            'handle'     : self.fileUnitDict[unitattr]['handle']
                            }
                        })
                self.fileUnitDict.update({
                        unitattr : {
                            'filename'   : name,
                            'fileformat' : None,
                            'filetype'   : None,
                            'reason'     : openattr.upper(),
                            'open'       : False,
                            'handle'     : None
                            }
                        })
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
                "CYCLE" : "MDcurrentstep",
                "EVAL" : "MDcurrentstep",
                "COORSTEP" : "MDcurrentstep",
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
        istimestep = isMetaStrInDict("TIME STEP",self.cntrlDict)
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

    def nextCommandInOutput(self, parser, startCmdNo, cmdLine,
            rec=False, recNumLines=None, recFirstLine=False):
        theLines=None
        thisLine=None
        thisNo=startCmdNo
        self.recordList.seek(0)
        printon=True
        recNext=False
        lcount=0
        for i,line in enumerate(self.recordList):
            if 'INPUT STREAM SWITCHING' in line:
                printon = False
            if 'RETURNING TO INPUT STREAM' in line:
                printon = True
            if printon:
                if 'CHARMM>' in line:
                    if recNext is True:
                        thisLine = line
                        thisNo = i
                        recNext = False
                        break
                    theCmd = ' '.join([
                        x for x in cmdLine.strip().split() if x])
                    theLine = ' '.join([
                        x for x in line.replace(
                            'CHARMM>', '').strip().split() if x])
                    if(theCmd.upper() == theLine.upper() and
                       i >= startCmdNo):
                        recNext = True
                        if rec is True:
                            theLines=[]
                            lcount=0
                if recNext is True:
                    thisLine = line
                    thisNo = i
                    if rec is True:
                        if recNumLines is None:
                            if recFirstLine is False:
                                if lcount > 0:
                                    theLines.append(line)
                            else:
                                theLines.append(line)
                        else:
                            if recFirstLine is False:
                                if lcount > 0 and lcount <= recNumLines:
                                    theLines.append(line)
                            else:
                                if lcount < recNumLines:
                                    theLines.append(line)
                        lcount += 1

        return thisNo, thisLine, theLines

    def guessInputCmdsFromOutput(self, parser):
        cmdlist=[]
        self.recordList.seek(0)
        printon=True
        for i,line in enumerate(self.recordList):
            if 'INPUT STREAM SWITCHING' in line:
                printon = False
            if 'RETURNING TO INPUT STREAM' in line:
                printon = True
            if printon:
                if 'CHARMM>' in line:
                    nline=line.replace('CHARMM>', '').strip()
                    uline=nline.upper()
                    if(uline.startswith('READ') or
                       uline.startswith('COOR') or
                       uline.startswith('WRIT') or
                       uline.startswith('OPEN') or
                       uline.startswith('MINI') or
                       uline.startswith('DYNA') or
                       uline.startswith('ENER') or
                       uline.startswith('GETE') or
                       uline.startswith('UPDA') or
                       uline.startswith('IC') or
                       uline.startswith('EDIT') or
                       uline.startswith('PRIN') or
                       uline.startswith('STOP') or
                       uline.startswith('END') or
                       uline.startswith('HBON') or
                       uline.startswith('GENE') or
                       uline.startswith('STRE')):
                        cmdlist.append(nline)
                        #sys.stdout.write("Line %d: %s\n" % (i, nline))
        return cmdlist

    def findUnitFileName(self, parser, oLine, lineNo):
        unitattr=None
        nameattr=None
        pathattr=None
        name=None
        oreadLine = ' '.join([
            x for x in oLine.strip().split() if x]).split()
        for orai, orarg in enumerate(oreadLine):
            if 'UNIT' in orarg.upper():
                unitattr = oreadLine[orai+1]
            if 'NAME' in orarg.upper():
                nameattr = oreadLine[orai+1]
        lineNo, theLine, recLines = self.nextCommandInOutput(
            parser,lineNo,oLine,rec=True)
        for lrec in recLines:
            lrecLine = ' '.join([
                x for x in lrec.strip().split() if x])
            if 'PARAMETER' in lrecLine.upper():
                pathpara = lrecLine.split()
                paraattr = '@' + pathpara[1]
                pathattr = pathpara[3].replace('"','')
                paraattr = paraattr.strip()
                pathattr = pathattr.strip()
        if(unitattr is not None and
           nameattr is not None and
           pathattr is not None):
           try:
               name = nameattr.replace(str(paraattr),str(pathattr))
               if name:
                   name = os.path.abspath(self.working_dir_name + '/' + name)
           except(TypeError,AttributeError):
               pass
        return lineNo, unitattr, name

    def findInputCmdFile(self, parser):
        findList=[]
        textFiles = self.textFileFoundInDir(parser)
        cmdList = self.guessInputCmdsFromOutput(parser)
        uniqCmdList = list(set(cmdList))
        acceptPerc = 0.80
        for tFile in textFiles:
            linecount=0
            linestore=[]
            if tFile == os.path.abspath(self.fName):
                break
            with open(tFile, 'r') as fin:
                for line in fin:
                    linestore.append(line)
                    linecount+=1
                    if linecount>50000:
                        break
                perc = 0.0
                if len(uniqCmdList)>0:
                    perc = [any(
                        cmd in tx for tx in linestore
                        ) for cmd in uniqCmdList
                        ].count(True)/len(uniqCmdList)
                if perc>=acceptPerc:
                    findList.append([tFile,perc])
        probInName=None
        if findList:
            probInText=findList[0]
            highPerc=probInText[1]
            probInName=probInText[0]
            for probInText in findList:
                if probInText[1]>highPerc:
                    highPerc=probInText[1]
                    probInName=probInText[0]

        # Remove dublicate lines for OPEN UNIT @X commands
        newCmdList = []
        storeCmd=None
        for cmd in cmdList:
            cmdLine = ' '.join([x for x in cmd.strip().split() if x])
            if storeCmd is not None:
                if storeCmd == cmdLine:
                    continue
            if('OPEN' in cmdLine.upper() and
               'UNIT' in cmdLine.upper()):
                cmdSeq = cmdLine.split()
                for sid, seq in enumerate(cmdSeq):
                    if 'UNIT' in seq.upper():
                        if '@' in cmdSeq[sid+1]:
                            storeCmd = cmdLine
            newCmdList.append(cmd)

        self.inputOutputCards={}
        secNo=0
        readMode=None
        readEnd=None
        secDict = {}
        secRTF = []
        secPAR = []
        secCOR = []
        secCOW = []
        secSEQ = []
        secPRT = []
        secPSF = []
        secPSW = []
        secOPR = []
        secOPW = []
        lineNo=0
        for lno, cmd in enumerate(newCmdList):
            cmdLine = ' '.join([x for x in cmd.strip().upper().split() if x])
            if lno == None:
            #if lno == readEnd:
                if readMode == 'rtf':
                    secRTF.append(cmd)
                    secDict.update({readMode : secRTF})
                if readMode == 'par':
                    secPAR.append(cmd)
                    secDict.update({readMode : secPAR})
                if readMode == 'cor':
                    secCOR.append(cmd)
                    secDict.update({readMode : secCOR})
                if readMode == 'seq':
                    secSEQ.append(cmd)
                    secDict.update({readMode : secSEQ})
                if readMode == 'psf':
                    secPSF.append(cmd)
                    secDict.update({readMode : secPSF})
                readMode=None
                readEnd=None
            if(cmdLine.startswith('READ') and
                'UNIT' not in cmdLine and
                not cmdLine.startswith('!')):
                cmdSeq = cmdLine.split()
                if cmdSeq[1].upper().startswith('RTF'):
                    readMode='rtf'
                    readEnd=lno+1
                    lineNo, theLine, recLines = self.nextCommandInOutput(parser,lineNo,cmd)
                    secRTF.append(theLine)
                    secDict.update({readMode : secRTF})
                if cmdSeq[1].upper().startswith('PARA'):
                    readMode='par'
                    readEnd=lno+1
                    lineNo, theLine, recLines = self.nextCommandInOutput(parser,lineNo,cmd)
                    secPAR.append(theLine)
                    secDict.update({readMode : secPAR})
                if cmdSeq[1].upper().startswith('COOR'):
                    readMode='cor'
                    readEnd=lno+1
                    lineNo, theLine, recLines = self.nextCommandInOutput(parser,lineNo,cmd)
                    secCOR.append(theLine)
                    secDict.update({readMode : secCOR})
                if cmdSeq[1].upper().startswith('SEQ'):
                    readMode='seq'
                    readEnd=lno+1
                    lineNo, theLine, recLines = self.nextCommandInOutput(parser,lineNo,cmd)
                    secSEQ.append(theLine)
                    secDict.update({readMode : secSEQ})
            elif(cmdLine.startswith('WRIT') and
                'UNIT' in cmdLine and
                not cmdLine.startswith('!')):
                cmdSeq = cmdLine.split()
                if cmdSeq[1].upper().startswith('COOR'):
                    readMode=None
                    readEnd=None
                    secCOW.append(cmd)
                    secDict.update({'cor_write' : secCOW})
                if cmdSeq[1].upper().startswith('PSF'):
                    readMode=None
                    readEnd=None
                    secPSW.append(cmd)
                    secDict.update({'psf_write' : secPSW})
            elif(cmdLine.startswith('READ') and
                'UNIT' in cmdLine and
                not cmdLine.startswith('!')):
                cmdSeq = cmdLine.split()
                if cmdSeq[1].upper().startswith('RTF'):
                    readMode=None
                    readEnd=None
                    secRTF.append(cmd)
                    secDict.update({'rtf' : secRTF})
                if cmdSeq[1].upper().startswith('PARA'):
                    readMode=None
                    readEnd=None
                    secPAR.append(cmd)
                    secDict.update({'par' : secPAR})
                if cmdSeq[1].upper().startswith('COOR'):
                    readMode=None
                    readEnd=None
                    secCOR.append(cmd)
                    secDict.update({'cor' : secCOR})
                if cmdSeq[1].upper().startswith('SEQ'):
                    readMode=None
                    readEnd=None
                    secSEQ.append(cmd)
                    secDict.update({'seq' : secSEQ})
                if cmdSeq[1].upper().startswith('PSF'):
                    readMode=None
                    readEnd=None
                    secPSF.append(cmd)
                    secDict.update({'psf' : secPSF})
            elif(cmdLine.startswith('PRIN') and
                'COOR' in cmdLine and
                'UNIT' not in cmdLine and
                not cmdLine.startswith('!')):
                cmdSeq = cmdLine.split()
                if cmdSeq[1].upper().startswith('COOR'):
                    readMode='cor_print'
                    readEnd=lno+1
                    #lineNo, theLine, recLines = self.nextCommandInOutput(parser,lineNo,cmd)
                    #secPRT.append(theLine)
                    secPRT.append(cmdLine)
                    secDict.update({readMode : secPRT})
            elif(cmdLine.startswith('OPEN') and
                'READ' in cmdLine and
                'UNIT' in cmdLine and
                not cmdLine.startswith('!')):
                unitno = None
                rtype = None
                rfile = None
                cmdOpen = ' '.join([x for x in cmd.strip().split() if x])
                cmdSeq = cmdOpen.split()
                for ti, tf in enumerate(cmdSeq):
                    if tf.upper().startswith('UNIT'):
                        if '@' in cmdSeq[ti+1]:
                            unitno = cmdSeq[ti+1]
                        else:
                            unitno = int(cmdSeq[ti+1])
                    if tf.upper().startswith('READ'):
                        rtype = cmdSeq[ti+1]
                    if tf.upper().startswith('NAME'):
                        rfile = cmdSeq[ti+1]
                if(unitno is not None and
                   rtype is not None and
                   rfile is not None):
                    readMode=None
                    readEnd=None
                    secOPR.append(cmd)
                    #secOPR.append([unitno, rtype, rfile])
                    secDict.update({'open_read' : secOPR})
            elif(cmdLine.startswith('OPEN') and
                'WRITE' in cmdLine and
                'UNIT' in cmdLine and
                not cmdLine.startswith('!')):
                unitno = None
                wtype = None
                wfile = None
                cmdOpen = ' '.join([x for x in cmd.strip().split() if x])
                cmdSeq = cmdOpen.split()
                for ti, tf in enumerate(cmdSeq):
                    if tf.upper().startswith('UNIT'):
                        if '@' in cmdSeq[ti+1]:
                            unitno = cmdSeq[ti+1]
                        else:
                            unitno = int(cmdSeq[ti+1])
                    if tf.upper().startswith('WRITE'):
                        wtype = cmdSeq[ti+1]
                    if tf.upper().startswith('NAME'):
                        wfile = cmdSeq[ti+1]
                if(unitno is not None and
                   wtype is not None and
                   wfile is not None):
                    readMode=None
                    readEnd=None
                    secOPW.append(cmd)
                    #secOPW.append([unitno, wtype, wfile])
                    secDict.update({'open_write' : secOPW})
            if lno == len(newCmdList)-1:
                self.inputOutputCards.update({
                    secNo : secDict
                    })
            if(cmdLine.startswith('MINI') or
               cmdLine.startswith('DYNA') or
               cmdLine.startswith('ENER') or
               cmdLine.startswith('GETE')):
                self.inputOutputCards.update({
                    secNo : secDict
                    })
                secNo += 1
                secDict = {}
                readMode=None
                readEnd=None
                secRTF = []
                secPAR = []
                secCOR = []
                secCOW = []
                secSEQ = []
                secPRT = []
                secPSF = []
                secPSW = []
                secOPR = []
                secOPW = []
        if probInName is not None:
            cmdLine=None
            cmdNo=0
            secNo=0
            readMode=None
            readEnd=None
            secDict = self.inputOutputCards[secNo]
            newSecDict = {}
            readRtfNo=-1
            readParNo=-1
            readCorNo=-1
            readCowNo=-1
            readSeqNo=-1
            readPrtNo=-1
            readPsfNo=-1
            readPswNo=-1
            readOprNo=-1
            readOpwNo=-1
            secRTF = []
            secPAR = []
            secCOR = []
            secCOW = []
            secSEQ = []
            secPRT = []
            secPSF = []
            secPSW = []
            secOPR = []
            secOPW = []
            if 'rtf' in secDict:
                for s in range(len(secDict['rtf'])):
                    secRTF.append([])
            if 'par' in secDict:
                for s in range(len(secDict['par'])):
                    secPAR.append([])
            if 'cor' in secDict:
                for s in range(len(secDict['cor'])):
                    secCOR.append([])
            if 'seq' in secDict:
                for s in range(len(secDict['seq'])):
                    secSEQ.append([])
            if 'psf' in secDict:
                for s in range(len(secDict['psf'])):
                    secPSF.append([])
            if 'cor_write' in secDict:
                for s in range(len(secDict['cor_write'])):
                    secCOW.append([])
            if 'psf_write' in secDict:
                for s in range(len(secDict['psf_write'])):
                    secPSW.append([])
            if 'cor_print' in secDict:
                for s in range(len(secDict['cor_print'])):
                    secPRT.append([])
            if 'open_read' in secDict:
                for s in range(len(secDict['open_read'])):
                    secOPR.append([])
            if 'open_write' in secDict:
                for s in range(len(secDict['open_write'])):
                    secOPW.append([])
            rtfEnd=False
            parEnd=False
            with open(probInName, 'r') as fin:
                for lno, cmd in enumerate(fin):
                    cmdLine = ' '.join([x for x in cmd.strip().split() if x]).upper()
                    if readEnd is not None:
                        theLine = ' '.join([x for x in readEnd.replace(
                            'CHARMM>', '').strip().split() if x]).upper()
                        if readMode == 'rtf' and 'END' in cmdLine:
                            rtfEnd = True
                        if readMode == 'par' and 'END' in cmdLine:
                            parEnd = True
                        if theLine == cmdLine:
                            if readMode == 'rtf' and rtfEnd is True:
                                readMode = None
                            if readMode == 'par' and parEnd is True:
                                readMode = None
                            if(readMode == 'cor' or
                               readMode == 'seq'):
                                readMode = None
                    if readMode == 'rtf':
                        secRTF[readRtfNo][1].append(cmd)
                        newSecDict.update({readMode : secRTF})
                    if readMode == 'par':
                        secPAR[readParNo][1].append(cmd)
                        newSecDict.update({readMode : secPAR})
                    if readMode == 'cor':
                        secCOR[readCorNo][1].append(cmd)
                        newSecDict.update({readMode : secCOR})
                    if readMode == 'seq':
                        secSEQ[readSeqNo][1].append(cmd)
                        newSecDict.update({readMode : secSEQ})
                    if(cmdLine.startswith('READ') and
                        'UNIT' not in cmdLine and
                        not cmdLine.startswith('!')):
                        cmdSeq = cmdLine.split()
                        if cmdSeq[1].upper().startswith('RTF'):
                            if 'rtf' in secDict:
                                cmdNo += 1
                                readRtfNo += 1
                                readMode='rtf'
                                rtfEnd=False
                                readEnd=secDict[readMode][readRtfNo]
                                #secRTF[readRtfNo].append([cmdNo, []])
                                secRTF[readRtfNo]=[cmdNo, []]
                        if cmdSeq[1].upper().startswith('PARA'):
                            if 'par' in secDict:
                                cmdNo += 1
                                readParNo += 1
                                readMode='par'
                                parEnd=False
                                readEnd=secDict[readMode][readParNo]
                                #secPAR[readParNo].append([cmdNo, []])
                                secPAR[readParNo]=[cmdNo, []]
                        if cmdSeq[1].upper().startswith('COOR'):
                            if 'cor' in secDict:
                                cmdNo += 1
                                readCorNo += 1
                                readMode='cor'
                                readEnd=secDict[readMode][readCorNo]
                                #secCOR[readCorNo].append([cmdNo, []])
                                secCOR[readCorNo]=[cmdNo, []]
                        if cmdSeq[1].upper().startswith('SEQ'):
                            if 'seq' in secDict:
                                cmdNo += 1
                                readSeqNo += 1
                                readMode='seq'
                                readEnd=secDict[readMode][readSeqNo]
                                #secSEQ[readSeqNo].append([cmdNo, [cmdLine]])
                                #secSEQ[readSeqNo]=[cmdNo, [cmdLine]]
                                if 'CARD' in cmdLine:
                                    secSEQ[readSeqNo]=[cmdNo, []]
                                else:
                                    secSEQ[readSeqNo]=[cmdNo, [cmdLine]]
                                newSecDict.update({readMode : secSEQ})
                    elif(cmdLine.startswith('WRIT') and
                        'UNIT' in cmdLine and
                        not cmdLine.startswith('!')):
                        cmdSeq = cmdLine.split()
                        for ti, tf in enumerate(cmdSeq):
                            if tf.upper().startswith('UNIT'):
                                unitno = int(cmdSeq[ti+1])
                                if cmdSeq[1].upper().startswith('COOR'):
                                    if 'cor_write' in secDict:
                                        cmdNo += 1
                                        readCowNo += 1
                                        readMode=None
                                        readEnd=None #secDict['cor'][readCorNo]
                                        #secCOW[readCowNo].append([cmdNo, unitno])
                                        secCOW[readCowNo]=[cmdNo, unitno]
                                        newSecDict.update({'cor_write' : secCOW})
                                if cmdSeq[1].upper().startswith('PSF'):
                                    if 'psf_write' in secDict:
                                        cmdNo += 1
                                        readPswNo += 1
                                        readMode=None
                                        readEnd=None #secDict['seq'][readSeqNo]
                                        #secPSW[readPswNo].append([cmdNo, unitno])
                                        secPSW[readPswNo]=[cmdNo, unitno]
                                        newSecDict.update({'psf_write' : secPSW})
                    elif(cmdLine.startswith('READ') and
                        'UNIT' in cmdLine and
                        not cmdLine.startswith('!')):
                        cmdSeq = cmdLine.split()
                        for ti, tf in enumerate(cmdSeq):
                            if tf.upper().startswith('UNIT'):
                                unitno = int(cmdSeq[ti+1])
                                if cmdSeq[1].upper().startswith('RTF'):
                                    if 'rtf' in secDict:
                                        cmdNo += 1
                                        readRtfNo += 1
                                        readMode=None
                                        readEnd=None #secDict['rtf'][readRtfNo]
                                        #secRTF[readRtfNo].append([cmdNo, unitno])
                                        secRTF[readRtfNo]=[cmdNo, unitno]
                                        newSecDict.update({'rtf' : secRTF})
                                if cmdSeq[1].upper().startswith('PARA'):
                                    if 'par' in secDict:
                                        cmdNo += 1
                                        readParNo += 1
                                        readMode=None
                                        readEnd=None #secDict['par'][readParNo]
                                        #secPAR[readParNo].append([cmdNo, unitno])
                                        secPAR[readParNo]=[cmdNo, unitno]
                                        newSecDict.update({'par' : secPAR})
                                if cmdSeq[1].upper().startswith('COOR'):
                                    if 'cor' in secDict:
                                        cmdNo += 1
                                        readCorNo += 1
                                        readMode=None
                                        readEnd=None #secDict['cor'][readCorNo]
                                        #secCOR[readCorNo].append([cmdNo, unitno])
                                        secCOR[readCorNo]=[cmdNo, unitno]
                                        newSecDict.update({'cor' : secCOR})
                                if cmdSeq[1].upper().startswith('SEQ'):
                                    if 'seq' in secDict:
                                        cmdNo += 1
                                        readSeqNo += 1
                                        readMode=None
                                        readEnd=None #secDict['seq'][readSeqNo]
                                        #secSEQ[readSeqNo].append([cmdNo, unitno])
                                        secSEQ[readSeqNo]=[cmdNo, unitno]
                                        newSecDict.update({'seq' : secSEQ})
                                if cmdSeq[1].upper().startswith('PSF'):
                                    if 'psf' in secDict:
                                        cmdNo += 1
                                        readPsfNo += 1
                                        readMode=None
                                        readEnd=None #secDict['seq'][readSeqNo]
                                        #secPSF[readPsfNo].append([cmdNo, unitno])
                                        secPSF[readPsfNo]=[cmdNo, unitno]
                                        newSecDict.update({'psf' : secPSF})
                    elif(cmdLine.startswith('PRIN') and
                        'COOR' in cmdLine and
                        'UNIT' not in cmdLine and
                        not cmdLine.startswith('!')):
                        cmdSeq = cmdLine.split()
                        if cmdSeq[1].upper().startswith('COOR'):
                            if 'cor_print' in secDict:
                                cmdNo += 1
                                readPrtNo += 1
                                readMode=None
                                readEnd=None #secDict[readMode][readCorNo]
                                #secPRT[readPrtNo].append([cmdNo, secDict['cor_print'][readPrtNo]])
                                secPRT[readPrtNo]=[cmdNo, secDict['cor_print'][readPrtNo]]
                                newSecDict.update({'cor_print' : secPRT})
                    elif(cmdLine.startswith('OPEN') and
                        'READ' in cmdLine and
                        'UNIT' in cmdLine and
                        not cmdLine.startswith('!')):
                        unitno = None
                        rtype = None
                        rfile = None
                        cmdOpen = ' '.join([x for x in cmd.strip().split() if x])
                        cmdSeq = cmdOpen.split()
                        for ti, tf in enumerate(cmdSeq):
                            if tf.upper().startswith('UNIT'):
                                if '@' in cmdSeq[ti+1]:
                                    unitno = cmdSeq[ti+1]
                                else:
                                    unitno = int(cmdSeq[ti+1])
                            if tf.upper().startswith('READ'):
                                rtype = cmdSeq[ti+1]
                            if tf.upper().startswith('NAME'):
                                rfile = cmdSeq[ti+1]
                        if(unitno is not None and
                            #rtype is not None and
                            rfile is not None):
                            cmdNo += 1
                            readOprNo += 1
                            readMode=None
                            readEnd=None
                            #secOPR[readOprNo].append([cmdNo, [unitno, rtype, rfile]])
                            #secOPR[readOprNo].append([cmdNo, secDict['open_read'][readOprNo]])
                            secOPR[readOprNo]=[cmdNo, secDict['open_read'][readOprNo]]
                            #secOPR[readOprNo]=[cmdNo, cmdOpen]
                            newSecDict.update({'open_read' : secOPR})
                    elif(cmdLine.startswith('OPEN') and
                        'WRITE' in cmdLine and
                        'UNIT' in cmdLine and
                        not cmdLine.startswith('!')):
                        unitno = None
                        wtype = None
                        wfile = None
                        cmdOpen = ' '.join([x for x in cmd.strip().split() if x])
                        cmdSeq = cmdOpen.split()
                        for ti, tf in enumerate(cmdSeq):
                            if tf.upper().startswith('UNIT'):
                                if '@' in cmdSeq[ti+1]:
                                    unitno = cmdSeq[ti+1]
                                else:
                                    unitno = int(cmdSeq[ti+1])
                            if tf.upper().startswith('WRIT'):
                                wtype = cmdSeq[ti+1]
                            if tf.upper().startswith('NAME'):
                                wfile = cmdSeq[ti+1]
                        if(unitno is not None and
                            wtype is not None and
                            wfile is not None):
                            cmdNo += 1
                            readOpwNo += 1
                            readMode=None
                            readEnd=None
                            #secOPW[readOpwNo].append([cmdNo, [unitno, wtype, wfile]])
                            #secOPW[readOpwNo].append([cmdNo, secDict['open_write'][readOpwNo]])
                            secOPW[readOpwNo]=[cmdNo, secDict['open_write'][readOpwNo]]
                            #secOPW[readOpwNo]=[cmdNo, cmdOpen]
                            newSecDict.update({'open_write' : secOPW})
                    if(cmdLine.startswith('MINI') or
                       cmdLine.startswith('DYNA') or
                       cmdLine.startswith('ENER') or
                       cmdLine.startswith('GETE')):
                        self.inputOutputCards.update({
                            secNo : newSecDict
                            })
                        secNo += 1
                        if secNo in self.inputOutputCards:
                            readMode=None
                            readEnd=None
                            readRtfNo=-1
                            readParNo=-1
                            readCorNo=-1
                            readCowNo=-1
                            readSeqNo=-1
                            readPrtNo=-1
                            readPsfNo=-1
                            readPswNo=-1
                            readOprNo=-1
                            readOpwNo=-1
                            secRTF = []
                            secPAR = []
                            secCOR = []
                            secCOW = []
                            secSEQ = []
                            secPRT = []
                            secPSF = []
                            secPSW = []
                            secOPR = []
                            secOPW = []
                            secDict = self.inputOutputCards[secNo]
                            newSecDict = {}
                            if 'rtf' in secDict:
                                for s in range(len(secDict['rtf'])):
                                    secRTF.append([])
                            if 'par' in secDict:
                                for s in range(len(secDict['par'])):
                                    secPAR.append([])
                            if 'cor' in secDict:
                                for s in range(len(secDict['cor'])):
                                    secCOR.append([])
                            if 'seq' in secDict:
                                for s in range(len(secDict['seq'])):
                                    secSEQ.append([])
                            if 'psf' in secDict:
                                for s in range(len(secDict['psf'])):
                                    secPSF.append([])
                            if 'cor_write' in secDict:
                                for s in range(len(secDict['cor_write'])):
                                    secCOW.append([])
                            if 'psf_write' in secDict:
                                for s in range(len(secDict['psf_write'])):
                                    secPSW.append([])
                            if 'cor_print' in secDict:
                                for s in range(len(secDict['cor_print'])):
                                    secPRT.append([])
                            if 'open_read' in secDict:
                                for s in range(len(secDict['open_read'])):
                                    secOPR.append([])
                            if 'open_write' in secDict:
                                for s in range(len(secDict['open_write'])):
                                    secOPW.append([])
                self.inputOutputCards.update({
                    secNo : newSecDict
                    })
        cmdNo=0
        lineNo=0
        for secNo, inOutCmd in self.inputOutputCards.items():
            if 'open_read' in inOutCmd:
                secOPR=[]
                for oread in inOutCmd['open_read']:
                    unitattr=None
                    nameattr=None
                    if probInName is not None:
                        cmdNo = oread[0]
                        orLine = oread[1]
                    else:
                        cmdNo = lineNo
                        orLine = oread
                    lineNo, unitattr, nameattr = self.findUnitFileName(parser, orLine, lineNo)
                    if probInName is None:
                        cmdNo = lineNo
                    if unitattr is not None and nameattr is not None:
                        secOPR.append([cmdNo, [unitattr, nameattr]])
                    else:
                        secOPR.append([cmdNo, orLine])
                self.inputOutputCards[secNo].update({'open_read' : secOPR})
        lineNo=0
        for secNo, inOutCmd in self.inputOutputCards.items():
            if 'open_write' in inOutCmd:
                secOPW=[]
                for oread in inOutCmd['open_write']:
                    unitattr=None
                    nameattr=None
                    if probInName is not None:
                        cmdNo = oread[0]
                        orLine = oread[1]
                    else:
                        cmdNo = lineNo
                        orLine = oread
                    lineNo, unitattr, nameattr = self.findUnitFileName(parser, orLine, lineNo)
                    if probInName is None:
                        cmdNo = lineNo
                    if unitattr is not None and nameattr is not None:
                        secOPW.append([cmdNo, [unitattr, nameattr]])
                    else:
                        secOPW.append([cmdNo, orLine])
                self.inputOutputCards[secNo].update({'open_write' : secOPW})
        lineNo=0
        for secNo, inOutCmd in self.inputOutputCards.items():
            if 'seq' in inOutCmd:
                secSEQ=[]
                for oread in inOutCmd['seq']:
                    if probInName is not None:
                        cmdNo = oread[0]
                        orLine = oread[1]
                    else:
                        cmdNo = lineNo
                        orLine = oread
                    seqLine = orLine[0]
                    seqCmd = ' '.join([x for x in orLine[0].strip().split() if x])
                    if 'READ' in seqCmd.upper() and 'SEQ' in seqCmd.upper():
                        lineNo, theLine, recLines = self.nextCommandInOutput(
                                parser,lineNo,seqLine,rec=True,recFirstLine=True)
                        if probInName is None:
                            cmdNo = lineNo
                        if recLines is not None:
                            newRecLines=[]
                            for rline in recLines:
                                if 'CHARMM>' in rline:
                                    rline = ' '.join([
                                        x for x in rline.replace(
                                            'CHARMM>', '').strip().split() if x
                                        ]).upper()
                                if rline.strip() == '':
                                    continue
                                newRecLines.append(rline)
                            secSEQ.append([cmdNo, newRecLines])
                        else:
                            secSEQ.append([cmdNo, orLine])
                    else:
                        secSEQ.append([cmdNo, orLine])
                self.inputOutputCards[secNo].update({'seq' : secSEQ})
        lineNo=0
        for secNo, inOutCmd in self.inputOutputCards.items():
            if 'cor_print' in inOutCmd:
                secPRT=[]
                for oread in inOutCmd['cor_print']:
                    if probInName is not None:
                        cmdNo = oread[0]
                        orLine = oread[1]
                    else:
                        cmdNo = lineNo
                        orLine = oread
                    lineNo, theLine, recLines = self.nextCommandInOutput(
                            parser,lineNo,orLine,rec=True)
                    if probInName is None:
                        cmdNo = lineNo
                    if recLines is not None:
                        newRecLines=[]
                        coorprintstart=False
                        for rline in recLines:
                            if 'CHARMM>' in rline:
                                rline = ' '.join([
                                    x for x in rline.replace(
                                        'CHARMM>', '').strip().split() if x
                                    ]).upper()
                            if('COORDINATE' in rline and
                               'FILE' in rline and
                               'MODULE' in rline):
                                coorprintstart=True
                                continue
                            if('TITLE' in rline or '*' in rline):
                                coorprintstart=True
                            if coorprintstart:
                                newRecLines.append(rline)
                        secPRT.append([cmdNo, newRecLines])
                    else:
                        secPRT.append([cmdNo, orLine])
                self.inputOutputCards[secNo].update({'cor_print' : secPRT})

        if probInName is not None:
            return probInName
        else:
            return None

    def build_subMatchers(self):
        """Builds the sub matchers to parse the main output file.
        """
        mddataNameList=getList_MetaStrInDict(self.mddataDict)

        self.miniInternHeaderDict={'MINI':0, 'INTERN:':1, 'BONDs':2, 'ANGLes':3, 'UREY-b':4, 'DIHEdrals':5, 'IMPRopers':6}
        self.miniExternHeaderDict={'MINI':0, 'EXTERN:':1, 'VDWaals':2, 'ELEC':3, 'HBONds':4, 'ASP':5, 'USER':6}
        self.dynaInternHeaderDict={'DYNA':0, 'INTERN:':1, 'BONDs':2, 'ANGLes':3, 'UREY-b':4, 'DIHEdrals':5, 'IMPRopers':6}
        self.dynaExternHeaderDict={'DYNA':0, 'EXTERN:':1, 'VDWaals':2, 'ELEC':3, 'HBONds':4, 'ASP':5, 'USER':6}

        cntrlNameList=getList_MetaStrInDict(self.metaDicts['cntrl'])
        filecntrlNameList=getList_MetaStrInDict(self.metaDicts['filecntrl'])
        extraNameList=getList_MetaStrInDict(self.metaDicts['extra'])

        self.enerOutputSubParsers = [
            # ENERGY/GETE parameters reader
            { "startReStr"        : "\s*CHARMM>\s*(?:GETE|ENERGY)\s*",
              "parser"            : "namelist_parser",
              "parsername"        : "energy_control_parser",
              "waitlist"          : None,
              "stopOnMatchStr"    : "\s*ENER\s+ENR:\s*Eval#\s*",
              "quitOnMatchStr"    : "\s*ENER\s+ENR:\s*Eval#\s*",
              "metaNameStart"     : PARSERTAG + "_inout_control",
              "matchNameList"     : cntrlNameList,
              "matchNameDict"     : "cntrlDict",
              "updateMatchDict"   : False,
              "onlyCaseSensitive" : True,
              "stopOnFirstLine"   : False,
              "parserOptions"     : { "lineFilter" : None }
              },
            # ENERGY EVAL header reader
            { "startReStr"        : r"\s*ENER\s+ENR:\s*Eval#\s*",
              "parser"            : "table_parser",
              "parsername"        : "ener_header_parser",
              "waitlist"          : None,
              "stopOnMatchStr"    : r"\s*(?:ENER|----------)\s+(?:>|INTERN|EXTERN|-----)\s*",
              "quitOnMatchStr"    : r"\s*CHARMM>\s*",
              "metaNameStart"     : PARSERTAG + "_mdout_",
              "matchNameList"     : mddataNameList,
              "matchNameDict"     : "mddataDict",
              "updateMatchDict"   : True,
              "onlyCaseSensitive" : True,
              "stopOnFirstLine"   : False,
              "parserOptions"     : {
                  "header"           : True,
                  "headersave"       : "enerEvalHeaderDict",
                  "wrap"             : False,
                  "tablelines"       : 0,
                  "tablestartsat"    : r"\s*ENER\s+ENR:\s*Eval#\s*",
                  "tableendsat"      : r"\s*(?:ENER|----------)\s+(?:>|INTERN|EXTERN|-----)\s*",
                  "lineFilter"       : {"ENER ENR:": "ENER-ENR:"},
                  "movetostopline"   : False,
                  "parsercntrlattr"  : "MDcurrentstep",
                  "parsercntrlin"    : "logsteps",
                  "lookupdict"       : "stepcontrolDict"
                  }
              },
            # ENER EXTERN energies header reader
            { "startReStr"        : r"\s*ENER\s+EXTERN:\s*",
              "parser"            : "table_parser",
              "parsername"        : "ener_extern_header_parser",
              "waitlist"          : None,
              "stopOnMatchStr"    : r"\s*(?:ENER|----------)\s+(?:>|INTERN|-----)\s*",
              "quitOnMatchStr"    : r"\s*CHARMM>\s*",
              "metaNameStart"     : PARSERTAG + "_mdout_",
              "matchNameList"     : mddataNameList,
              "matchNameDict"     : "mddataDict",
              "updateMatchDict"   : True,
              "onlyCaseSensitive" : True,
              "stopOnFirstLine"   : False,
              "parserOptions"     : {
                  "header"           : True,
                  "headersave"       : "enerExternHeaderDict",
                  "wrap"             : False,
                  "tablelines"       : 0,
                  "tablestartsat"    : r"\s*ENER\s+EXTERN:\s*",
                  "tableendsat"      : r"\s*(?:ENER|----------)\s+(?:>|INTERN|-----)\s*",
                  "lineFilter"       : None,
                  "movetostopline"   : False,
                  "parsercntrlattr"  : "MDcurrentstep",
                  "parsercntrlin"    : "logsteps",
                  "lookupdict"       : "stepcontrolDict"
                  }
              },
            # ENER INTERN energies header reader
            { "startReStr"        : r"\s*ENER\s+INTERN:\s*",
              "parser"            : "table_parser",
              "parsername"        : "ener_intern_header_parser",
              "waitlist"          : None,
              "stopOnMatchStr"    : r"\s*(?:ENER|----------)\s+(?:>|EXTERN|-----)\s*",
              "quitOnMatchStr"    : r"\s*CHARMM>\s*",
              "metaNameStart"     : PARSERTAG + "_mdout_",
              "matchNameList"     : mddataNameList,
              "matchNameDict"     : "mddataDict",
              "updateMatchDict"   : True,
              "onlyCaseSensitive" : True,
              "stopOnFirstLine"   : False,
              "parserOptions"     : {
                  "header"           : True,
                  "headersave"       : "enerInternHeaderDict",
                  "wrap"             : False,
                  "tablelines"       : 0,
                  "tablestartsat"    : r"\s*ENER\s+INTERN:\s*",
                  "tableendsat"      : r"\s*(?:ENER|----------)\s+(?:>|EXTERN|-----)\s*",
                  "lineFilter"       : None,
                  "movetostopline"   : False,
                  "parsercntrlattr"  : "MDcurrentstep",
                  "parsercntrlin"    : "logsteps",
                  "lookupdict"       : "stepcontrolDict"
                  }
              },
            # ENER evaluations reader
            { "startReStr"        : r"\s*ENER>\s*",
              "parser"            : "table_parser",
              "parsername"        : "ener_eval_parser",
              "waitlist"          : None,
              "stopOnMatchStr"    : r"\s*(?:ENER|----------)\s+(?:INTERN|EXTERN|-----)\s*",
              "quitOnMatchStr"    : r"\s*CHARMM>\s*",
              "metaNameStart"     : PARSERTAG + "_mdout_",
              "matchNameList"     : mddataNameList,
              "matchNameDict"     : "mddataDict",
              "updateMatchDict"   : True,
              "onlyCaseSensitive" : True,
              "stopOnFirstLine"   : False,
              "parserOptions"     : {
                  "header"           : False,
                  "headerList"       : "enerEvalHeaderDict",
                  "wrap"             : False,
                  "tablelines"       : 0,
                  "tablestartsat"    : r"\s*ENER>\s*",
                  "tableendsat"      : r"\s*(?:ENER|----------)\s+(?:INTERN|EXTERN|-----)\s*",
                  "lineFilter"       : None,
                  "movetostopline"   : False,
                  "parsercntrlattr"  : "MDcurrentstep",
                  "parsercntrlin"    : "logsteps",
                  "lookupdict"       : "stepcontrolDict"
                  }
              },
            # ENER INTERN output reader
            { "startReStr"        : r"\s*ENER\s+INTERN>\s*",
              "parser"            : "table_parser",
              "parsername"        : "ener_intern_parser",
              "waitlist"          : None,
              "stopOnMatchStr"    : r"\s*(?:ENER|----------)(?:>|\s+)(?:EXTERN|-----)\s*",
              "quitOnMatchStr"    : r"\s*CHARMM>\s*",
              "metaNameStart"     : PARSERTAG + "_mdout_",
              "matchNameList"     : mddataNameList,
              "matchNameDict"     : "mddataDict",
              "updateMatchDict"   : True,
              "onlyCaseSensitive" : True,
              "stopOnFirstLine"   : False,
              "parserOptions"     : {
                  "header"           : False,
                  "headerList"       : "enerInternHeaderDict",
                  "wrap"             : False,
                  "tablelines"       : 0,
                  "tablestartsat"    : r"\s*ENER\s+INTERN>\s*",
                  "tableendsat"      : r"\s*(?:ENER|----------)(?:>|\s+)(?:EXTERN|-----)\s*",
                  "lineFilter"       : None,
                  "movetostopline"   : False,
                  "parsercntrlattr"  : "MDcurrentstep",
                  "parsercntrlin"    : "logsteps",
                  "lookupdict"       : "stepcontrolDict"
                  }
              },
            # ENER EXTERN output reader
            { "startReStr"        : r"\s*ENER\s+EXTERN>\s*",
              "parser"            : "table_parser",
              "parsername"        : "ener_extern_parser",
              "waitlist"          : None,
              "stopOnMatchStr"    : r"\s*(?:ENER|----------)(?:>|\s+)(?:INTERN|-----)\s*",
              "quitOnMatchStr"    : r"\s*CHARMM>\s*",
              "metaNameStart"     : PARSERTAG + "_mdout_",
              "matchNameList"     : mddataNameList,
              "matchNameDict"     : "mddataDict",
              "updateMatchDict"   : True,
              "onlyCaseSensitive" : True,
              "stopOnFirstLine"   : False,
              "parserOptions"     : {
                  "header"           : False,
                  "headerList"       : "enerExternHeaderDict",
                  "wrap"             : False,
                  "tablelines"       : 0,
                  "tablestartsat"    : r"\s*ENER\s+EXTERN>\s*",
                  "tableendsat"      : r"\s*(?:ENER|----------)(?:>|\s+)(?:INTERN|-----)\s*",
                  "lineFilter"       : None,
                  "movetostopline"   : False,
                  "parsercntrlattr"  : "MDcurrentstep",
                  "parsercntrlin"    : "logsteps",
                  "lookupdict"       : "stepcontrolDict"
                  }
              },
            ]

        self.miniOutputSubParsers = [
            # MINI parameters reader
            { "startReStr"        : "\s*CHARMM>\s*MINI\s*",
              "parser"            : "namelist_parser",
              "parsername"        : "mini_control_parser",
              "waitlist"          : None,
              "stopOnMatchStr"    : "\s*MINI\s+MIN:\s+Cycle\s*",
              "quitOnMatchStr"    : "\s*MINI\s+MIN:\s+Cycle\s*",
              "metaNameStart"     : PARSERTAG + "_inout_control",
              "matchNameList"     : cntrlNameList,
              "matchNameDict"     : "cntrlDict",
              "updateMatchDict"   : False,
              "onlyCaseSensitive" : False,
              "stopOnFirstLine"   : False,
              "parserOptions"     : {
                  "controlsections"  : ["x_charmm_section_control_parameters"],
                  "controlsave"      : "sectioncontrol",
                  "controldict"      : "stepcontrolDict",
                  }
              },
            # Section Control Parser
            { "startReStr"        : "AlwaysRun",
              "parser"            : "section_control_parser",
              "parsername"        : "control_section_parser",
              "waitlist"          : [["mini_control_parser"]],
              "stopOnMatchStr"    : "AlwaysStop",
              "quitOnMatchStr"    : "AlwaysStop",
              "metaNameStart"     : None,
              "matchNameList"     : None,
              "matchNameDict"     : None,
              "updateMatchDict"   : False,
              "onlyCaseSensitive" : True,
              "stopOnFirstLine"   : False,
              "parserOptions"     : {
                  "sectionname"      : "x_charmm_section_control_parameters",
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
            # MINI cycle header reader
            { "startReStr"        : r"\s*MINI\s+MIN:\s+Cycle\s*",
              "parser"            : "table_parser",
              "parsername"        : "mini_header_parser",
              "waitlist"          : [["mini_control_parser"]],
              #"stopOnMatchStr"    : r"\s*(?:MINI|----------)\s+(?:>|INTERN|EXTERN|-----)\s*",
              "stopOnMatchStr"    : r"\s*(?:CONJUG|STEEPD|NRAPH|CHARMM)>\s*",
              "quitOnMatchStr"    : r"\s*(?:CONJUG|STEEPD|NRAPH|CHARMM)>\s*",
              "metaNameStart"     : PARSERTAG + "_mdout_",
              "matchNameList"     : mddataNameList,
              "matchNameDict"     : "mddataDict",
              "updateMatchDict"   : True,
              "onlyCaseSensitive" : False,
              "stopOnFirstLine"   : False,
              "parserOptions"     : {
                  "header"           : True,
                  "headersave"       : "miniCycleHeaderDict",
                  "wrap"             : False,
                  "tablelines"       : 0,
                  "tablestartsat"    : r"\s*MINI\s+MIN:\s+Cycle\s*",
                  "tableendsat"      : r"\s*(?:MINI|MINI>|----------)\s+(?:\s+|INTERN|EXTERN|-----)\s*",
                  "lineFilter"       : {"MINI MIN:": "MINI-MIN:"},
                  "movetostopline"   : True,
                  "parsercntrlattr"  : "MDcurrentstep",
                  "parsercntrlin"    : "logsteps",
                  "lookupdict"       : "stepcontrolDict"
                  }
              },
            # MINI EXTERN energies header reader
            { "startReStr"        : r"\s*MINI\s+EXTERN:\s*",
              "parser"            : "table_parser",
              "parsername"        : "mini_extern_header_parser",
              "waitlist"          : [["mini_control_parser"]],
              #"stopOnMatchStr"    : r"\s*(?:MINI|----------)\s+(?:>|INTERN|-----)\s*",
              "stopOnMatchStr"    : r"\s*(?:CONJUG|STEEPD|NRAPH|CHARMM)>\s*",
              "quitOnMatchStr"    : r"\s*(?:CONJUG|STEEPD|NRAPH|CHARMM)>\s*",
              "metaNameStart"     : PARSERTAG + "_mdout_",
              "matchNameList"     : mddataNameList,
              "matchNameDict"     : "mddataDict",
              "updateMatchDict"   : True,
              "onlyCaseSensitive" : False,
              "stopOnFirstLine"   : False,
              "parserOptions"     : {
                  "header"           : True,
                  "headersave"       : "miniExternHeaderDict",
                  "wrap"             : False,
                  "tablelines"       : 0,
                  "tablestartsat"    : r"\s*MINI\s+EXTERN:\s*",
                  "tableendsat"      : r"\s*(?:MINI|MINI>|----------)\s+(?:\s+|INTERN|-----)\s*",
                  "lineFilter"       : None,
                  "movetostopline"   : True,
                  "parsercntrlattr"  : "MDcurrentstep",
                  "parsercntrlin"    : "logsteps",
                  "lookupdict"       : "stepcontrolDict"
                  }
              },
            # MINI INTERN energies header reader
            { "startReStr"        : r"\s*MINI\s+INTERN:\s*",
              "parser"            : "table_parser",
              "parsername"        : "mini_intern_header_parser",
              "waitlist"          : [["mini_control_parser"]],
              #"stopOnMatchStr"    : r"\s*(?:MINI|----------)\s+(?:>|EXTERN|-----)\s*",
              "stopOnMatchStr"    : r"\s*(?:CONJUG|STEEPD|NRAPH|CHARMM)>\s*",
              "quitOnMatchStr"    : r"\s*(?:CONJUG|STEEPD|NRAPH|CHARMM)>\s*",
              "metaNameStart"     : PARSERTAG + "_mdout_",
              "matchNameList"     : mddataNameList,
              "matchNameDict"     : "mddataDict",
              "updateMatchDict"   : True,
              "onlyCaseSensitive" : False,
              "stopOnFirstLine"   : False,
              "parserOptions"     : {
                  "header"           : True,
                  "headersave"       : "miniInternHeaderDict",
                  "wrap"             : False,
                  "tablelines"       : 0,
                  "tablestartsat"    : r"\s*MINI\s+INTERN:\s*",
                  "tableendsat"      : r"\s*(?:MINI|MINI>|----------)\s+(?:\s+|EXTERN|-----)\s*",
                  "lineFilter"       : None,
                  "movetostopline"   : True,
                  "parsercntrlattr"  : "MDcurrentstep",
                  "parsercntrlin"    : "logsteps",
                  "lookupdict"       : "stepcontrolDict"
                  }
              },
            # MINI output cycles reader
            { "startReStr"        : r"\s*MINI>\s*",
              "parser"            : "table_parser",
              "parsername"        : "mini_cycle_parser",
              "waitlist"          : [["mini_control_parser"]],
              #"stopOnMatchStr"    : r"\s*(?:MINI|----------)\s+(?:INTERN|EXTERN|-----)\s*",
              "stopOnMatchStr"    : r"\s*(?:CONJUG|STEEPD|NRAPH|CHARMM)>\s*",
              "quitOnMatchStr"    : r"\s*(?:CONJUG|STEEPD|NRAPH|CHARMM)>\s*",
              "metaNameStart"     : PARSERTAG + "_mdout_",
              "matchNameList"     : mddataNameList,
              "matchNameDict"     : "mddataDict",
              "updateMatchDict"   : True,
              "onlyCaseSensitive" : False,
              "stopOnFirstLine"   : False,
              "parserOptions"     : {
                  "header"           : False,
                  "headerList"       : "miniCycleHeaderDict",
                  "wrap"             : False,
                  "tablelines"       : 0,
                  "tablestartsat"    : r"\s*MINI>\s*",
                  "tableendsat"      : r"\s*(?:MINI|----------)\s+(?:INTERN|EXTERN|-----)\s*",
                  "lineFilter"       : None,
                  "movetostopline"   : True,
                  "parsercntrlattr"  : "MDcurrentstep",
                  "parsercntrlin"    : "logsteps",
                  "lookupdict"       : "stepcontrolDict"
                  }
              },
            # MINI internal energies output reader
            { "startReStr"        : r"\s*MINI\s+INTERN>\s*",
              "parser"            : "table_parser",
              "parsername"        : "mini_intern_parser",
              "waitlist"          : [["mini_control_parser"]],
              #"stopOnMatchStr"    : r"\s*(?:MINI|----------)(?:>|\s+)(?:EXTERN|-----)\s*",
              "stopOnMatchStr"    : r"\s*(?:CONJUG|STEEPD|NRAPH|CHARMM)>\s*",
              "quitOnMatchStr"    : r"\s*(?:CONJUG|STEEPD|NRAPH|CHARMM)>\s*",
              "metaNameStart"     : PARSERTAG + "_mdout_",
              "matchNameList"     : mddataNameList,
              "matchNameDict"     : "mddataDict",
              "updateMatchDict"   : True,
              "onlyCaseSensitive" : False,
              "stopOnFirstLine"   : False,
              "parserOptions"     : {
                  "header"           : False,
                  "headerList"       : "miniInternHeaderDict",
                  "wrap"             : False,
                  "tablelines"       : 0,
                  "tablestartsat"    : r"\s*MINI\s+INTERN>\s*",
                  "tableendsat"      : r"\s*(?:MINI|MINI>|----------)\s+(?:\s+|EXTERN|-----)\s*",
                  "lineFilter"       : None,
                  "movetostopline"   : True,
                  "parsercntrlattr"  : "MDcurrentstep",
                  "parsercntrlin"    : "logsteps",
                  "lookupdict"       : "stepcontrolDict"
                  }
              },
            # MINI external energies output reader
            { "startReStr"        : r"\s*MINI\s+EXTERN>\s*",
              "parser"            : "table_parser",
              "parsername"        : "mini_extern_parser",
              "waitlist"          : [["mini_control_parser"]],
              #"stopOnMatchStr"    : r"\s*(?:MINI|----------)(?:>|\s+)(?:INTERN|-----)\s*",
              "stopOnMatchStr"    : r"\s*(?:CONJUG|STEEPD|NRAPH|CHARMM)>\s*",
              "quitOnMatchStr"    : r"\s*(?:CONJUG|STEEPD|NRAPH|CHARMM)>\s*",
              "metaNameStart"     : PARSERTAG + "_mdout_",
              "matchNameList"     : mddataNameList,
              "matchNameDict"     : "mddataDict",
              "updateMatchDict"   : True,
              "onlyCaseSensitive" : False,
              "stopOnFirstLine"   : False,
              "parserOptions"     : {
                  "header"           : False,
                  "headerList"       : "miniExternHeaderDict",
                  "wrap"             : False,
                  "tablelines"       : 0,
                  "tablestartsat"    : r"\s*MINI\s+EXTERN>\s*",
                  "tableendsat"      : r"\s*(?:MINI|MINI>|----------)\s+(?:\s+|INTERN|-----)\s*",
                  "lineFilter"       : None,
                  "movetostopline"   : True,
                  "parsercntrlattr"  : "MDcurrentstep",
                  "parsercntrlin"    : "logsteps",
                  "lookupdict"       : "stepcontrolDict"
                  }
              },
            # thermostat save Parser
            { "startReStr"        : "AlwaysRun",
              "parser"            : "dictionary_parser",
              "parsername"        : "mini_frameseq_step_parser",
              "waitlist"          : [["mini_control_parser", "mini_cycle_parser"]],
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
                  "keyMapper"        : {"CYCLE" : "MDcurrentstep"},
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
            # MINI exit reader
            { "startReStr"        : r">\s*Minimization\s*exiting\s*with\s*",
              "parser"            : "namelist_parser",
              "parsername"        : "mini_status_parser",
              "waitlist"          : None,
              #"stopOnMatchStr"    : r"\s*(?:CONJUG|STEEPD|NRAPH|CHARMM)>\s*",
              #"quitOnMatchStr"    : r"\s*(?:CONJUG|STEEPD|NRAPH|CHARMM)>\s*",
              "stopOnMatchStr"    : "\s*CHARMM>\s*((?!MINI|DYNA|ENER|GETE).)*$",
              "quitOnMatchStr"    : "\s*CHARMM>\s*((?!MINI|DYNA|ENER|GETE).)*$",
              "metaNameStart"     : PARSERTAG + "_inout_control",
              "matchNameList"     : cntrlNameList,
              "matchNameDict"     : "cntrlDict",
              "updateMatchDict"   : False,
              "onlyCaseSensitive" : False,
              "stopOnFirstLine"   : False,
              "parserOptions"     : { "lineFilter" : None }
              },
            # Section Control Parser
            { "startReStr"        : "AlwaysRun",
              "parser"            : "section_control_parser",
              "parsername"        : "mini_section_parser",
              "waitlist"          : [["mini_cycle_parser"]],
              "stopOnMatchStr"    : r"\s*MINI>\s*",
              "quitOnMatchStr"    : r"\s*MINI>\s*",
              "metaNameStart"     : None,
              "matchNameList"     : None,
              "matchNameDict"     : None,
              "updateMatchDict"   : False,
              "onlyCaseSensitive" : False,
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
              "stopOnMatchStr"    : "\s*CHARMM>\s*((?!MINI|DYNA|ENER|GETE).)*$",
              "quitOnMatchStr"    : "\s*CHARMM>\s*((?!MINI|DYNA|ENER|GETE).)*$",
              "metaNameStart"     : None,
              "matchNameList"     : None,
              "matchNameDict"     : None,
              "updateMatchDict"   : False,
              "onlyCaseSensitive" : True,
              "stopOnFirstLine"   : False,
              "parserOptions"     : {
                  "peeklineFirst"    : True,
                  "waitatlineStr"    : r"\s*MINI>\s*",
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

        self.dynaOutputSubParsers = [
            # DYNA parameters reader
            { "startReStr"        : r"\s*CHARMM>\s*DYNA\s*",
              "parser"            : "namelist_parser",
              "parsername"        : "dyna_control_parser",
              "waitlist"          : None,
              "stopOnMatchStr"    : r"\s*DYNA\s+DYN:\s+Step\s*",
              "quitOnMatchStr"    : r"\s*DYNA\s+DYN:\s+Step\s*",
              "metaNameStart"     : PARSERTAG + "_inout_control",
              "matchNameList"     : cntrlNameList,
              "matchNameDict"     : "cntrlDict",
              "updateMatchDict"   : False,
              "onlyCaseSensitive" : False,
              "stopOnFirstLine"   : False,
              "parserOptions"     : {
                  "controlsections"  : ["x_charmm_section_control_parameters"],
                  "controlsave"      : "sectioncontrol",
                  "controldict"      : "stepcontrolDict",
                  }
              },
            # Section Control Parser
            { "startReStr"        : "AlwaysRun",
              "parser"            : "section_control_parser",
              "parsername"        : "control_section_parser",
              "waitlist"          : [["dyna_control_parser"]],
              "stopOnMatchStr"    : "AlwaysStop",
              "quitOnMatchStr"    : "AlwaysStop",
              "metaNameStart"     : None,
              "matchNameList"     : None,
              "matchNameDict"     : None,
              "updateMatchDict"   : False,
              "onlyCaseSensitive" : True,
              "stopOnFirstLine"   : False,
              "parserOptions"     : {
                  "sectionname"      : "x_charmm_section_control_parameters",
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
            # DYNA step header reader
            { "startReStr"        : r"\s*DYNA\s+DYN:\s+Step\s*",
              "parser"            : "table_parser",
              "parsername"        : "dyna_header_parser",
              "waitlist"          : [["dyna_control_parser"]],
              "stopOnMatchStr"    : r"\s*(?:DYNA|----------)\s+(?:>|PROP:|EXTERN:|INTERN:|PRESS:|-----)\s*",
              "quitOnMatchStr"    : r"\s*CHARMM>\s*",
              "metaNameStart"     : PARSERTAG + "_mdout_",
              "matchNameList"     : mddataNameList,
              "matchNameDict"     : "mddataDict",
              "updateMatchDict"   : True,
              "onlyCaseSensitive" : False,
              "stopOnFirstLine"   : False,
              "parserOptions"     : {
                  "header"           : True,
                  "headersave"       : "dynaStepHeaderDict",
                  "wrap"             : False,
                  "tablelines"       : 0,
                  "tablestartsat"    : r"\s*DYNA\s+DYN:\s+Step\s*",
                  "tableendsat"      : r"\s*(?:DYNA|----------)\s+(?:>|PROP:|EXTERN:|INTERN:|PRESS:|-----)\s*",
                  "lineFilter"       : {"DYNA DYN": "DYNA-DYN"},
                  "movetostopline"   : False,
                  "parsercntrlattr"  : "MDcurrentstep",
                  "parsercntrlin"    : "logsteps",
                  "lookupdict"       : "stepcontrolDict"
                  }
              },
            # DYNA PROP energies header reader
            { "startReStr"        : r"\s*DYNA\s+PROP:\s*",
              "parser"            : "table_parser",
              "parsername"        : "dyna_prop_header_parser",
              "waitlist"          : [["dyna_control_parser"]],
              "stopOnMatchStr"    : r"\s*(?:DYNA|----------)\s+(?:>|EXTERN:|INTERN:|PRESS:|-----)\s*",
              "quitOnMatchStr"    : r"\s*CHARMM>\s*",
              "metaNameStart"     : PARSERTAG + "_mdout_",
              "matchNameList"     : mddataNameList,
              "matchNameDict"     : "mddataDict",
              "updateMatchDict"   : True,
              "onlyCaseSensitive" : False,
              "stopOnFirstLine"   : False,
              "parserOptions"     : {
                  "header"           : True,
                  "headersave"       : "dynaPropHeaderDict",
                  "wrap"             : False,
                  "tablelines"       : 0,
                  "tablestartsat"    : r"\s*DYNA\s+PROP:\s*",
                  "tableendsat"      : r"\s*(?:DYNA|----------)\s+(?:>|EXTERN:|INTERN:|PRESS:|-----)\s*",
                  "lineFilter"       : None,
                  "movetostopline"   : False,
                  "parsercntrlattr"  : "MDcurrentstep",
                  "parsercntrlin"    : "logsteps",
                  "lookupdict"       : "stepcontrolDict"
                  }
              },
            # DYNA EXTERN energies header reader
            { "startReStr"        : r"\s*DYNA\s+EXTERN:\s*",
              "parser"            : "table_parser",
              "parsername"        : "dyna_extern_header_parser",
              "waitlist"          : [["dyna_control_parser"]],
              "stopOnMatchStr"    : r"\s*(?:DYNA|----------)\s+(?:>|PROP:|INTERN:|PRESS:|-----)\s*",
              "quitOnMatchStr"    : r"\s*CHARMM>\s*",
              "metaNameStart"     : PARSERTAG + "_mdout_",
              "matchNameList"     : mddataNameList,
              "matchNameDict"     : "mddataDict",
              "updateMatchDict"   : True,
              "onlyCaseSensitive" : False,
              "stopOnFirstLine"   : False,
              "parserOptions"     : {
                  "header"           : True,
                  "headersave"       : "dynaExternHeaderDict",
                  "wrap"             : False,
                  "tablelines"       : 0,
                  "tablestartsat"    : r"\s*DYNA\s+EXTERN:\s*",
                  "tableendsat"      : r"\s*(?:DYNA|----------)\s+(?:>|PROP:|INTERN:|PRESS:|-----)\s*",
                  "lineFilter"       : None,
                  "movetostopline"   : False,
                  "parsercntrlattr"  : "MDcurrentstep",
                  "parsercntrlin"    : "logsteps",
                  "lookupdict"       : "stepcontrolDict"
                  }
              },
            # DYNA INTERN energies header reader
            { "startReStr"        : r"\s*DYNA\s+INTERN:\s*",
              "parser"            : "table_parser",
              "parsername"        : "dyna_intern_header_parser",
              "waitlist"          : [["dyna_control_parser"]],
              "stopOnMatchStr"    : r"\s*(?:DYNA|----------)\s+(?:>|PROP:|EXTERN:|PRESS:|-----)\s*",
              "quitOnMatchStr"    : r"\s*CHARMM>\s*",
              "metaNameStart"     : PARSERTAG + "_mdout_",
              "matchNameList"     : mddataNameList,
              "matchNameDict"     : "mddataDict",
              "updateMatchDict"   : True,
              "onlyCaseSensitive" : False,
              "stopOnFirstLine"   : False,
              "parserOptions"     : {
                  "header"           : True,
                  "headersave"       : "dynaInternHeaderDict",
                  "wrap"             : False,
                  "tablelines"       : 0,
                  "tablestartsat"    : r"\s*DYNA\s+INTERN:\s*",
                  "tableendsat"      : r"\s*(?:DYNA|----------)\s+(?:>|PROP:|EXTERN:|PRESS:|-----)\s*",
                  "lineFilter"       : None,
                  "movetostopline"   : False,
                  "parsercntrlattr"  : "MDcurrentstep",
                  "parsercntrlin"    : "logsteps",
                  "lookupdict"       : "stepcontrolDict"
                  }
              },
            # DYNA PRESS energies header reader
            { "startReStr"        : r"\s*DYNA\s+PRESS:\s*",
              "parser"            : "table_parser",
              "parsername"        : "dyna_press_header_parser",
              "waitlist"          : [["dyna_control_parser"]],
              "stopOnMatchStr"    : r"\s*(?:DYNA|----------)\s+(?:>|PROP:|EXTERN:|INTERN:|-----)\s*",
              "quitOnMatchStr"    : r"\s*CHARMM>\s*",
              "metaNameStart"     : PARSERTAG + "_mdout_",
              "matchNameList"     : mddataNameList,
              "matchNameDict"     : "mddataDict",
              "updateMatchDict"   : True,
              "onlyCaseSensitive" : False,
              "stopOnFirstLine"   : False,
              "parserOptions"     : {
                  "header"           : True,
                  "headersave"       : "dynaPressHeaderDict",
                  "wrap"             : False,
                  "tablelines"       : 0,
                  "tablestartsat"    : r"\s*DYNA\s+PRESS:\s*",
                  "tableendsat"      : r"\s*(?:DYNA|----------)\s+(?:>|PROP:|EXTERN:|INTERN:|-----)\s*",
                  "lineFilter"       : None,
                  "movetostopline"   : False,
                  "parsercntrlattr"  : "MDcurrentstep",
                  "parsercntrlin"    : "logsteps",
                  "lookupdict"       : "stepcontrolDict"
                  }
              },
            # DYNA output cycles reader
            { "startReStr"        : r"\s*DYNA>\s*",
              "parser"            : "table_parser",
              "parsername"        : "dyna_step_parser",
              "waitlist"          : [["dyna_control_parser"]],
              "stopOnMatchStr"    : r"\s*(?:DYNA|----------)\s+(?:PROP>|EXTERN>|INTERN>|PRESS>|-----)\s*",
              "quitOnMatchStr"    : r"\s*CHARMM>\s*",
              "metaNameStart"     : PARSERTAG + "_mdout_",
              "matchNameList"     : mddataNameList,
              "matchNameDict"     : "mddataDict",
              "updateMatchDict"   : True,
              "onlyCaseSensitive" : False,
              "stopOnFirstLine"   : False,
              "parserOptions"     : {
                  "header"           : False,
                  "headerList"       : "dynaStepHeaderDict",
                  "wrap"             : False,
                  "tablelines"       : 0,
                  "tablestartsat"    : r"\s*DYNA>\s*",
                  "tableendsat"      : r"\s*(?:DYNA|----------)\s+(?:PROP>|EXTERN>|INTERN>|PRESS>|-----)\s*",
                  "lineFilter"       : None,
                  "movetostopline"   : False,
                  "parsercntrlattr"  : "MDcurrentstep",
                  "parsercntrlin"    : "logsteps",
                  "lookupdict"       : "stepcontrolDict"
                  }
              },
            # DYNA PROP output reader
            { "startReStr"        : r"\s*DYNA\s+PROP>\s*",
              "parser"            : "table_parser",
              "parsername"        : "dyna_prop_parser",
              "waitlist"          : [["dyna_control_parser"]],
              "stopOnMatchStr"    : r"\s*(?:DYNA|----------)\s+(?:>|INTERN>|EXTERN>|PRESS>|-----)\s*",
              "quitOnMatchStr"    : r"\s*CHARMM>\s*",
              "metaNameStart"     : PARSERTAG + "_mdout_",
              "matchNameList"     : mddataNameList,
              "matchNameDict"     : "mddataDict",
              "updateMatchDict"   : True,
              "onlyCaseSensitive" : False,
              "stopOnFirstLine"   : False,
              "parserOptions"     : {
                  "header"           : False,
                  "headerList"       : "dynaPropHeaderDict",
                  "wrap"             : False,
                  "tablelines"       : 0,
                  "tablestartsat"    : r"\s*DYNA\s+PROP>\s*",
                  "tableendsat"      : r"\s*(?:DYNA|----------)\s+(?:>|INTERN>|EXTERN>|PRESS>|-----)\s*",
                  "lineFilter"       : None,
                  "movetostopline"   : False,
                  "parsercntrlattr"  : "MDcurrentstep",
                  "parsercntrlin"    : "logsteps",
                  "lookupdict"       : "stepcontrolDict"
                  }
              },
            # DYNA internal energies output reader
            { "startReStr"        : r"\s*DYNA\s+INTERN>\s*",
              "parser"            : "table_parser",
              "parsername"        : "dyna_intern_parser",
              "waitlist"          : [["dyna_control_parser"]],
              "stopOnMatchStr"    : r"\s*(?:DYNA|----------)\s+(?:>|PROP>|EXTERN>|PRESS>|-----)\s*",
              "quitOnMatchStr"    : r"\s*CHARMM>\s*",
              "metaNameStart"     : PARSERTAG + "_mdout_",
              "matchNameList"     : mddataNameList,
              "matchNameDict"     : "mddataDict",
              "updateMatchDict"   : True,
              "onlyCaseSensitive" : False,
              "stopOnFirstLine"   : False,
              "parserOptions"     : {
                  "header"           : False,
                  "headerList"       : "dynaInternHeaderDict",
                  "wrap"             : False,
                  "tablelines"       : 0,
                  "tablestartsat"    : r"\s*DYNA\s+INTERN>\s*",
                  "tableendsat"      : r"\s*(?:DYNA|----------)\s+(?:>|PROP>|EXTERN>|PRESS>|-----)\s*",
                  "lineFilter"       : None,
                  "movetostopline"   : False,
                  "parsercntrlattr"  : "MDcurrentstep",
                  "parsercntrlin"    : "logsteps",
                  "lookupdict"       : "stepcontrolDict"
                  }
              },
            # DYNA external energies output reader
            { "startReStr"        : r"\s*DYNA\s+EXTERN>\s*",
              "parser"            : "table_parser",
              "parsername"        : "dyna_extern_parser",
              "waitlist"          : [["dyna_control_parser"]],
              "stopOnMatchStr"    : r"\s*(?:DYNA|----------)\s+(?:>|PROP>|INTERN>|PRESS>|-----)\s*",
              "quitOnMatchStr"    : r"\s*CHARMM>\s*",
              "metaNameStart"     : PARSERTAG + "_mdout_",
              "matchNameList"     : mddataNameList,
              "matchNameDict"     : "mddataDict",
              "updateMatchDict"   : True,
              "onlyCaseSensitive" : False,
              "stopOnFirstLine"   : False,
              "parserOptions"     : {
                  "header"           : False,
                  "headerList"       : "dynaExternHeaderDict",
                  "wrap"             : False,
                  "tablelines"       : 0,
                  "tablestartsat"    : r"\s*DYNA\s+EXTERN>\s*",
                  "tableendsat"      : r"\s*(?:DYNA|----------)\s+(?:>|PROP>|INTERN>|PRESS>|-----)\s*",
                  "lineFilter"       : None,
                  "movetostopline"   : False,
                  "parsercntrlattr"  : "MDcurrentstep",
                  "parsercntrlin"    : "logsteps",
                  "lookupdict"       : "stepcontrolDict"
                  }
              },
            # DYNA PRESS output reader
            { "startReStr"        : r"\s*DYNA\s+PRESS>\s*",
              "parser"            : "table_parser",
              "parsername"        : "dyna_press_parser",
              "waitlist"          : [["dyna_control_parser"]],
              "stopOnMatchStr"    : r"\s*(?:DYNA|----------)\s+(?:>|PROP>|INTERN>|EXTERN>|-----)\s*",
              "quitOnMatchStr"    : r"\s*CHARMM>\s*",
              "metaNameStart"     : PARSERTAG + "_mdout_",
              "matchNameList"     : mddataNameList,
              "matchNameDict"     : "mddataDict",
              "updateMatchDict"   : True,
              "onlyCaseSensitive" : False,
              "stopOnFirstLine"   : False,
              "parserOptions"     : {
                  "header"           : False,
                  "headerList"       : "dynaPressHeaderDict",
                  "wrap"             : False,
                  "tablelines"       : 0,
                  "tablestartsat"    : r"\s*DYNA\s+PRESS>\s*",
                  "tableendsat"      : r"\s*(?:DYNA|----------)\s+(?:>|PROP>|INTERN>|EXTERN>|-----)\s*",
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
              "parsername"        : "dyna_frameseq_step_parser",
              "waitlist"          : [["dyna_control_parser", "dyna_step_parser"]],
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
              "waitlist"          : [["dyna_control_parser", "dyna_step_parser"]],
              "stopOnMatchStr"    : r"\s*DYNA>\s*",
              "quitOnMatchStr"    : r"\s*DYNA>\s*",
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
              "stopOnMatchStr"    : "\s*CHARMM>((?!MINI|DYNA|ENER|GETE).)*$",
              "quitOnMatchStr"    : "\s*CHARMM>((?!MINI|DYNA|ENER|GETE).)*$",
              "metaNameStart"     : None,
              "matchNameList"     : None,
              "matchNameDict"     : None,
              "updateMatchDict"   : False,
              "onlyCaseSensitive" : True,
              "stopOnFirstLine"   : False,
              "parserOptions"     : {
                  "peeklineFirst"    : True,
                  "waitatlineStr"    : r"\s*DYNA>\s*",
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

        self.crysOutputSubParsers = [
            # CRYSTAL parameters reader
            { "startReStr"        : r"\s*CHARMM>\s*(?:CRYS|crys)\s*",
              "parser"            : "namelist_parser",
              "parsername"        : "crystal_control_parser",
              "waitlist"          : None,
              "stopOnMatchStr"    : r"\s*CHARMM>\s*((?!CRYS|crys))*$",
              "quitOnMatchStr"    : r"\s*CHARMM>\s*((?!CRYS|crys))*$",
              "metaNameStart"     : PARSERTAG + "_inout_control",
              "matchNameList"     : cntrlNameList,
              "matchNameDict"     : "cntrlDict",
              "updateMatchDict"   : False,
              "onlyCaseSensitive" : False,
              "stopOnFirstLine"   : False,
              "parserOptions"     : {
                  "lineFilter"       : None,
                  "resetNameDict"    : True,
                  #"controlsections"  : ["x_charmm_section_control_parameters"],
                  #"controlsave"      : "sectioncontrol",
                  #"controldict"      : "stepcontrolDict",
                  }
              },
            ]

        self.fileWriteSubParsers = [
            # WRITE parameters reader
            { "startReStr"        : "\s*CHARMM>\s*(?:WRITE|write)\s*",
              "parser"            : "namelist_parser",
              "parsername"        : "write_control_parser",
              "waitlist"          : None,
              "stopOnMatchStr"    : "(?:^$|\s*VCLOSE|\s*MAINIO>|\s*PARMIO>|\s*TITLE>|\s*RDTITL>)",
              "quitOnMatchStr"    : "(?:^$|\s*VCLOSE|\s*MAINIO>|\s*PARMIO>|\s*TITLE>|\s*RDTITL>)",
              "metaNameStart"     : PARSERTAG + "_inout_control",
              "matchNameList"     : filecntrlNameList,
              "matchNameDict"     : "filecntrlDict",
              "updateMatchDict"   : False,
              "onlyCaseSensitive" : False,
              "stopOnFirstLine"   : False,
              "parserOptions"     : {
                  "lineFilter"       : None,
                  "resetNameDict"    : True,
                  #"controlsections"  : ["x_charmm_section_control_parameters"],
                  #"controlsave"      : "sectioncontrol",
                  #"controldict"      : "stepcontrolDict",
                  }
              },
            # file Parser
            { "startReStr"        : "AlwaysRun",
              "parser"            : "dictionary_parser",
              "parsername"        : "file_parser",
              "waitlist"          : [["write_control_parser"]],
              "stopOnMatchStr"    : "(?:^$|\s*VCLOSE|\s*MAINIO>|\s*PARMIO>|\s*TITLE>|\s*RDTITL>)",
              "quitOnMatchStr"    : "(?:^$|\s*VCLOSE|\s*MAINIO>|\s*PARMIO>|\s*TITLE>|\s*RDTITL>)",
              "metaNameStart"     : PARSERTAG + "_inout_file",
              "matchNameList"     : filecntrlNameList,
              "matchNameDict"     : "filecntrlDict",
              "updateMatchDict"   : True,
              "onlyCaseSensitive" : False,
              "stopOnFirstLine"   : True,
              "parserOptions"     : {
                  "readline"         : False,
                  "dictionary"       : "filecntrlDict",
                  "dicttype"         : "smartparser", # (standard or smartparser)
                  "readwritedict"    : "read",
                  "keyMapper"        : {
                      "structure"    : "STRUCTURE FILE",
                      "traj_coord"   : "COOR DCD FILE",
                      "traj_vel"     : "VEL DCD FILE",
                      "traj_force"   : "FORCE DCD FILE",
                      "input_coord"  : "INPUT COOR FILE",
                      "output_coord" : "OUTPUT COOR FILE",
                      "input_coord"  : "INPUT COOR CARD",
                      "output_coord" : "OUTPUT COOR CARD",
                      },
                  "preprocess"       : self.fileReadWriteSave
                  }
              },
            # Readline Control Parser
            { "startReStr"        : "AlwaysRun",
              "parser"            : "readline_control_parser",
              "parsername"        : "readline_parser",
              "waitlist"          : [["write_control_parser"],["file_parser"]],
              "stopOnMatchStr"    : "\s*CHARMM>\s*",
              "quitOnMatchStr"    : "\s*CHARMM>\s*",
              "metaNameStart"     : None,
              "matchNameList"     : None,
              "matchNameDict"     : None,
              "updateMatchDict"   : False,
              "onlyCaseSensitive" : False,
              "stopOnFirstLine"   : False,
              "parserOptions"     : {
                  "peeklineFirst"    : True,
                  "waitatlineStr"    : "\s*CHARMM>\s*",
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

        self.fileReadSubParsers = [
            # READ parameters reader
            { "startReStr"        : "\s*CHARMM>\s*(?:READ|read)\s*(?:RTF|rtf|PARA|para|COOR|coor)",
              "parser"            : "namelist_parser",
              "parsername"        : "read_control_parser",
              "waitlist"          : None,
              "stopOnMatchStr"    : "(?:^$|\s*MAINIO>|\s*PARMIO>|\s*TITLE>|"
                                    "\s*RDTITL>|SPATIAL\s*COORDINATES\s*BEING\s*READ)",
              "quitOnMatchStr"    : "(?:^$|\s*MAINIO>|\s*PARMIO>|\s*TITLE>|"
                                    "\s*RDTITL>|SPATIAL\s*COORDINATES\s*BEING\s*READ)",
              "metaNameStart"     : PARSERTAG + "_inout_control",
              "matchNameList"     : filecntrlNameList,
              "matchNameDict"     : "filecntrlDict",
              "updateMatchDict"   : False,
              "onlyCaseSensitive" : False,
              "stopOnFirstLine"   : False,
              "parserOptions"     : {
                  "lineFilter"       : None,
                  "resetNameDict"    : True,
                  #"controlsections"  : ["x_charmm_section_control_parameters"],
                  #"controlsave"      : "sectioncontrol",
                  #"controldict"      : "stepcontrolDict",
                  }
              },
            # file Parser
            { "startReStr"        : "AlwaysRun",
              "parser"            : "dictionary_parser",
              "parsername"        : "file_parser",
              "waitlist"          : [["read_control_parser"]],
              "stopOnMatchStr"    : "(?:^$|\s*MAINIO>|\s*PARMIO>|\s*TITLE>|"
                                    "\s*RDTITL>|SPATIAL\s*COORDINATES\s*BEING\s*READ)",
              "quitOnMatchStr"    : "(?:^$|\s*MAINIO>|\s*PARMIO>|\s*TITLE>|"
                                    "\s*RDTITL>|SPATIAL\s*COORDINATES\s*BEING\s*READ)",
              "metaNameStart"     : PARSERTAG + "_inout_file",
              "matchNameList"     : filecntrlNameList,
              "matchNameDict"     : "filecntrlDict",
              "updateMatchDict"   : True,
              "onlyCaseSensitive" : False,
              "stopOnFirstLine"   : True,
              "parserOptions"     : {
                  "readline"         : False,
                  "dictionary"       : "filecntrlDict",
                  "dicttype"         : "smartparser", # (standard or smartparser)
                  "readwritedict"    : "read",
                  "keyMapper"        : {
                      "structure"    : "STRUCTURE FILE",
                      "traj_coord"   : "COOR DCD FILE",
                      "traj_vel"     : "VEL DCD FILE",
                      "traj_force"   : "FORCE DCD FILE",
                      "input_coord"  : "INPUT COOR FILE",
                      "output_coord" : "OUTPUT COOR FILE",
                      "input_coord"  : "INPUT COOR CARD",
                      "output_coord" : "OUTPUT COOR CARD",
                      },
                  "preprocess"       : self.fileReadWriteSave
                  }
              },
            # Readline Control Parser
            { "startReStr"        : "AlwaysRun",
              "parser"            : "readline_control_parser",
              "parsername"        : "readline_parser",
              "waitlist"          : [["read_control_parser"],["file_parser"]],
              "stopOnMatchStr"    : "\s*CHARMM>\s*",
              "quitOnMatchStr"    : "\s*CHARMM>\s*",
              "metaNameStart"     : None,
              "matchNameList"     : None,
              "matchNameDict"     : None,
              "updateMatchDict"   : False,
              "onlyCaseSensitive" : False,
              "stopOnFirstLine"   : False,
              "parserOptions"     : {
                  "peeklineFirst"    : True,
                  "waitatlineStr"    : "\s*CHARMM>\s*",
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

        self.fileOpenSubParsers = [
            # OPEN parameters reader
            { "startReStr"        : "\s*CHARMM>\s*(?:OPEN|open)\s*",
              "parser"            : "namelist_parser",
              "parsername"        : "open_control_parser",
              "waitlist"          : None,
              "stopOnMatchStr"    : "(?:^$|\s*VOPEN>|\s*OPNLGU>)",
              "quitOnMatchStr"    : "(?:^$|\s*VOPEN>|\s*OPNLGU>)",
              "metaNameStart"     : PARSERTAG + "_inout_control",
              "matchNameList"     : filecntrlNameList,
              "matchNameDict"     : "filecntrlDict",
              "updateMatchDict"   : False,
              "onlyCaseSensitive" : False,
              "stopOnFirstLine"   : True,
              "parserOptions"     : {
                  "lineFilter"       : None,
                  "resetNameDict"    : True,
                  #"controlsections"  : ["x_charmm_section_control_parameters"],
                  #"controlsave"      : "sectioncontrol",
                  #"controldict"      : "stepcontrolDict",
                  }
              },
            # file Parser
            { "startReStr"        : "AlwaysRun",
              "parser"            : "dictionary_parser",
              "parsername"        : "file_parser",
              "waitlist"          : [["open_control_parser"]],
              "stopOnMatchStr"    : "(?:^$|\s*VOPEN>|\s*OPNLGU>)",
              "quitOnMatchStr"    : "(?:^$|\s*VOPEN>|\s*OPNLGU>)",
              "metaNameStart"     : PARSERTAG + "_inout_file",
              "matchNameList"     : filecntrlNameList,
              "matchNameDict"     : "filecntrlDict",
              "updateMatchDict"   : True,
              "onlyCaseSensitive" : False,
              "stopOnFirstLine"   : False,
              "parserOptions"     : {
                  "readline"         : False,
                  "dictionary"       : "filecntrlDict",
                  "dicttype"         : "smartparser", # (standard or smartparser)
                  "readwritedict"    : "read",
                  "keyMapper"        : {
                      "structure"    : "STRUCTURE FILE",
                      "traj_coord"   : "COOR DCD FILE",
                      "traj_vel"     : "VEL DCD FILE",
                      "traj_force"   : "FORCE DCD FILE",
                      "input_coord"  : "INPUT COOR FILE",
                      "output_coord" : "OUTPUT COOR FILE",
                      "input_coord"  : "INPUT COOR CARD",
                      "output_coord" : "OUTPUT COOR CARD",
                      },
                  "preprocess"       : self.fileNameTrans
                  }
              },
            # Readline Control Parser
            { "startReStr"        : "AlwaysRun",
              "parser"            : "readline_control_parser",
              "parsername"        : "readline_parser",
              "waitlist"          : [["open_control_parser"],["file_parser"]],
              "stopOnMatchStr"    : "\s*CHARMM>\s*",
              "quitOnMatchStr"    : "\s*CHARMM>\s*",
              "metaNameStart"     : None,
              "matchNameList"     : None,
              "matchNameDict"     : None,
              "updateMatchDict"   : False,
              "onlyCaseSensitive" : False,
              "stopOnFirstLine"   : False,
              "parserOptions"     : {
                  "peeklineFirst"    : True,
                  "waitatlineStr"    : "\s*CHARMM>\s*",
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

        outputSubParsers = [
            # Function Caller
            { "startReStr"        : r"\s*CHARMM>\s*(?:MINI|mini|DYNA|dyna|"
                                     "ENER|ener|GETE|gete|CRYS|crys|"
                                     "OPEN|open|READ|read|WRITE|write|"
                                     "PRINT|print)",
              "parser"            : "subparser_caller",
              "parsername"        : "command_subparser",
              "waitlist"          : None,
              "stopOnMatchStr"    : r"\s*CHARMM>\s*",
              "quitOnMatchStr"    : r"\s*CHARMM>\s*",
              "metaNameStart"     : None,
              "matchNameList"     : None,
              "matchNameDict"     : None,
              "updateMatchDict"   : False,
              "onlyCaseSensitive" : False,
              "stopOnFirstLine"   : False,
              "parserOptions"     : {
                  "matchFirstLetters" : 4,
                  "onStartRunFunction" : None,
                  "onQuitRunFunction" : None,
                  "onlySubParsersReadLine" : True,
                  "waitFirstCycle" : True,
                  "subparserMapper"  : {
                      #"OPEN"    : "fileOpenSubParsers",
                      #"READ"    : "fileReadSubParsers",
                      #"WRIT"    : "fileWriteSubParsers",
                      #"PRINT"   : "PrintOutputSubParsers",
                      "CRYS"    : "crysOutputSubParsers",
                      "MINI"    : "miniOutputSubParsers",
                      "DYNA"    : "dynaOutputSubParsers",
                      #"ENER"    : "enerOutputSubParsers",
                      #"GETE"    : "enerOutputSubParsers",
                      },
                  "subparserSection" : {
                      "MINI"    : ["section_run", "auto", "secRunOpen", "secRunGIndex"],
                      "DYNA"    : ["section_run", "auto", "secRunOpen", "secRunGIndex"],
                      "ENER"    : ["section_run", "auto", "secRunOpen", "secRunGIndex"],
                      "GETE"    : ["section_run", "auto", "secRunOpen", "secRunGIndex"],
                      },
                  }
              },
            # Readline Control Parser
            { "startReStr"        : "AlwaysRun",
              "parser"            : "readline_control_parser",
              "parsername"        : "readline_parser",
              "waitlist"          : None,
              "stopOnMatchStr"    : r"\s*(?:New\s*timer\s*profile"
                                     "|Average\s*profile)\s*",
              "quitOnMatchStr"    : r"\s*(?:New\s*timer\s*profile"
                                     "|Average\s*profile)\s*",
              "metaNameStart"     : None,
              "matchNameList"     : None,
              "matchNameDict"     : None,
              "updateMatchDict"   : False,
              "onlyCaseSensitive" : False,
              "stopOnFirstLine"   : False,
              "parserOptions"     : {
                  "peeklineFirst"    : True,
                  "waitatlineStr"    : "\s*CHARMM>\s*",
                  "controlwait"      : None,
                  "controlattr"      : "MDcurrentstep",
                  "controlskip"      : [-1],
                  "controlin"        : "opencntrlstep",
                  }
              },
            ]

        ########################################
        # return main Parser
        return [
            SM(name='MainRun',
                startReStr=r"\s*Chemistry\s*at\s*HARvard\s*Macromolecular\s*Mechanics\s*",
                endReStr=r"\s*CPU\s*TIME:\s*[0-9.]*\s*SECONDS\s*",
                repeats=True,
                required=True,
                #forwardMatch=True,
                sections=['section_run'],
                fixedStartValues={'program_name': PROGRAMNAME},
                subMatchers=[
                    SM(name='ProgramInfo',
                       startReStr=r"\s*\(CHARMM\)\s*-\s*"
                                   "(?P<"+PARSERTAG+"_mdin_finline>[a-zA-Z0-9:., ]+)\s*",
                       adHoc=lambda p: p.backend.addValue(
                           "program_version",
                           ' '.join(p.lastMatch[
                               PARSERTAG+"_mdin_finline"
                               ].replace('\n', ' ').strip().split()))),
                    SM(name='license',
                       startReStr=r"\s*Copyright\(c\)\s*",
                       coverageIgnore=True,
                       adHoc=lambda p:
                       self.adHoc_read_store_text_stop_parsing(p,
                           stopOnMatchStr=r"\s*(?:All\s*Rights|Current)\s*",
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
                       startReStr=r"\s*Current\s*operating\s*system:\s*"
                                   "(?P<"+PARSERTAG+"_mdin_finline>.*)\s*",
                       adHoc=lambda p: p.backend.addValue(
                           PARSERTAG+"_build_osarch",
                           ' '.join(p.lastMatch[
                               PARSERTAG+"_mdin_finline"
                               ].replace('\n', ' ').strip().split()))),
                    SM(name='logruninfo',
                       startReStr=r"\s*Created\s*on\s*"
                                   "(?P<"+PARSERTAG+"_mdin_finline>"
                                   "[at0-9/:. ]+)\s*by\s*user:\s*"
                                   "(?P<"+PARSERTAG+"_output_created_by_user>[a-zA-Z0-9.]+)\s*",
                       adHoc=lambda p: p.backend.addValue(
                           "time_run_date_start", datetime.datetime.strptime(
                               p.lastMatch[PARSERTAG+"_mdin_finline"].strip().replace(" at "," "),
                           '%x %H:%M:%S').timestamp())),
                    SM(name='newRun',
                       startReStr=r"\s*(?:RDTITL|CHARMM)>\s*",
                       endReStr=r"\s*(?:New\s*timer\s*profile"
                                 "|Average\s*profile|)",
                       forwardMatch=True,
                       adHoc=lambda p:
                       self.adHoc_takingover_parsing(p,
                           stopOnMatchStr=r"\s*(?:New\s*timer\s*profile"
                                           "|Average\s*profile)\s*",
                           quitOnMatchStr=r"\s*(?:New\s*timer\s*profile"
                                           "|Average\s*profile)\s*",
                           onStartRunFunction=self.textFileFoundInDir,
                           stopControl="stopControl", # if None or True, stop with quitMatch, else wait
                           record=True, # if False or None, no record, no replay
                           replay=1, # if 0 or None= no replay, if <0 infinite replay
                           onStartReplayRunFunction={1:"findInputCmdFile"},
                           parseOnlyRecorded=True, # if True, parsers only work on record
                           ordered=False,
                           onlySubParsersReadLine=True,
                           subParsers=outputSubParsers)),
                    SM(name='TimerHeaders',
                       startReStr=r"\s*\$\$\$\$\$\$\s*(?:New\s*timer\s*profile"
                                   "|Average\s*profile)\s*"),
                    SM(name='ComputationTimings',
                       startReStr=r"\s*Total\s*time\s*[0-9:.eEdD]+\s*Other:"),
                       # END Computation
                    SM(name='end_run',
                       startReStr=r"\s*NORMAL\s*TERMINATION\s*BY\s*"
                                   "(?:END\s*OF\s*FILE|"
                                   "NORMAL\s*STOP)\s*",
                       adHoc=lambda p: p.backend.addValue("run_clean_end",True)),
                    SM(name='WarningLevel',
                       startReStr=r"\s*MOST\s*SEVERE\s*WARNING\s*WAS\s*AT\s*LEVEL\s*"
                                   "(?P<"+PARSERTAG+"_most_severe_warning_level>[0-9]+)\s*"),
                    SM(r"\s*JOB\s*ACCOUNTING\s*INFORMATION\s*"),
                    SM(name='Walltime',
                       startReStr=r"\s*ELAPSED\s*TIME:\s*(?P<time_run_wall_end>[0-9:.eEdD]+)"),
                    SM(name='CPUtime',
                       startReStr=r"\s*CPU\s*TIME:\s*(?P<time_run_cpu1_end>[0-9:.eEdD]+)")
                    # END Timings
                ]) # END MainRun
            ]


class CharmmParserInterface():
   """ A proper class envolop for running this parser from within python. """
   def __init__(self, backend, **kwargs):
       self.backend_factory = backend

   def parse(self, mainfile):
        from unittest.mock import patch
        logging.info('charmm parser started')
        logging.getLogger('nomadcore').setLevel(logging.WARNING)
        backend = self.backend_factory("charmm.nomadmetainfo.json")
        parserInfo = {'name': 'charmm-parser', 'version': '1.0'}
        context = CHARMMParser()
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
    parser = CHARMMParser()
    parser.parse()
