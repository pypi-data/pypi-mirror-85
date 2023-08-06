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

import numpy as np
from .CHARMMCommon import PARSERNAME, PROGRAMNAME, PARSERTAG
from nomadcore.smart_parser.SmartParserDictionary import metaNameConverter, metaNameConverter_UnderscoreSpaceDash
from nomadcore.smart_parser.SmartParserDictionary import MetaInfoMap, FileInfoMap, MapDictionary
from nomadcore.smart_parser.SmartParserDictionary import getDict_MetaStrInDict, getList_MetaStrInDict, get_unitDict
import nomadcore.md_data_access.MDDataAccess as MDData

def get_fileListDict():
    """Loads dictionary for file namelists.

    Returns:
        the list of defaults file namelists
    """

    startpage = {
        'nameTranslate'   : metaNameConverter,
        'metaHeader'      : PARSERTAG,
        'metaNameTag'     : 'inout_file',
        'metaInfoType'    : 'C',
        'activeMetaNames' : [],
        'activeSections'  : [PARSERTAG+'_section_input_output_files'],
        'fileInterface'   : ["charmmcoor", "parmed", "mdtraj", "mdanalysis"]
        #'fileInterface'   : ["charmmcoor", "parmed", "mdtraj", "mdanalysis", "pymolfile"]
        #'fileInterface'   : ["charmmcoor", "parmed", "pymolfile", "mdanalysis", "mdtraj"]
        }
    namelist = {
        'structure'     : FileInfoMap(startpage, fileFormat=['.psf'], activeInfo=True,
                                      infoPurpose=['topology', 'unitcell']),
        'trajectory'    : FileInfoMap(startpage, fileFormat=['.dcd'], activeInfo=True,
                                      infoPurpose=['trajectory', 'unitcell']),
        'traj_vel'      : FileInfoMap(startpage, fileFormat=['.dcd'], activeInfo=True,
                                      infoPurpose=['velocities']),
        'traj_force'    : FileInfoMap(startpage, fileFormat=['.xyz'], activeInfo=True,
                                      infoPurpose=['forces']),
        'output_coord'  : FileInfoMap(startpage, fileFormat=['.charmmcor'], activeInfo=False,
                                      infoPurpose=['outputcoordinates']),
        'out_coor_str'  : FileInfoMap(startpage, fileFormat=['.charmmstream'], activeInfo=False,
                                      infoPurpose=['outputcoordinates'], strDict=None),
        'output_vel'    : FileInfoMap(startpage, fileFormat=['.charmmcor'], activeInfo=False,
                                      infoPurpose=['outputvelocities']),
        'output_force'  : FileInfoMap(startpage, fileFormat=['.charmmcor'], activeInfo=False,
                                      infoPurpose=['outputforces']),
        'input_coord'   : FileInfoMap(startpage, fileFormat=['.charmmcor'],
                                      infoPurpose=['inputcoordinates']),
        'in_coor_str'   : FileInfoMap(startpage, fileFormat=['.charmmstream'],
                                      infoPurpose=['inputcoordinates'], strDict=None),
        'input_vel'     : FileInfoMap(startpage, fileFormat=['.charmmcor'],
                                      infoPurpose=['inputvelocities']),
        'restart_coord' : FileInfoMap(startpage, fileFormat=['.charmmcor'],
                                      infoPurpose=['inputcoordinates', 'outputcoordinates', 'unitcell']),
        'restart_vel'   : FileInfoMap(startpage, fileFormat=['.charmmcor'],
                                      infoPurpose=['inputvelocities', 'outputvelocities']),
        'rtf_file'      : FileInfoMap(startpage, fileFormat=['.charmmtop'],
                                      infoPurpose=['topology']),
        'prm_file'      : FileInfoMap(startpage, fileFormat=['.charmmpar'],
                                      infoPurpose=['topology']),
        'cor_file'      : FileInfoMap(startpage, fileFormat=['.charmmcor'],
                                      infoPurpose=['topology', 'inputcoordinates']),
        'stream'        : FileInfoMap(startpage, fileFormat=['.charmmstream'],
                                      infoPurpose=['topology'], strDict=None),
        'str_rtf'       : FileInfoMap(startpage, fileFormat=['.charmmstrrtf'],
                                      infoPurpose=['topology'], strDict=None),
        'str_par'       : FileInfoMap(startpage, fileFormat=['.charmmstrpar'],
                                      infoPurpose=['topology'], strDict=None),
        'output_log'    : FileInfoMap(startpage),
        'control_input' : FileInfoMap(startpage),
        }
    return MapDictionary(namelist)

def get_nameListDict(deflist):
    """Loads control in data of CHARMM.

    Args:
        deflist: name list definition (cntrl/parm).

    matchWith parameters:
        EOL = End of line
        PL  = Match with previous line
        PW  = Previous word
        NW  = Next word (until space, comma) (DEFAULT)
        UD  = until delimeter (can be any string/character)

        The text matched inside apostrophe or qoutation is extracted

    Returns:
        the list of namelists
    """
    startpage = {
        'nameTranslate'   : metaNameConverter_UnderscoreSpaceDash,
        'metaHeader'      : PARSERTAG,
        'metaNameTag'     : 'inout_control',
        'metaInfoType'    : 'C',
        'activeMetaNames' : [],
        'activeSections'  : [PARSERTAG+'_section_control_parameters'],
        }

    cntrllist = {
        'CRYSTAL' : MetaInfoMap(startpage, defaultValue=None),
        'Crystal Type =' : MetaInfoMap(startpage, defaultValue=None, replaceTag='Crystal Type'),
        'A     =' : MetaInfoMap(startpage, defaultValue=None, replaceTag='a length'),
        'B     =' : MetaInfoMap(startpage, defaultValue=None, replaceTag='b length'),
        'C     =' : MetaInfoMap(startpage, defaultValue=None, replaceTag='c length'),
        'Alpha =' : MetaInfoMap(startpage, defaultValue=None, replaceTag='Alpha'),
        'Beta ='  : MetaInfoMap(startpage, defaultValue=None, replaceTag='Beta'),
        'Gamma =' : MetaInfoMap(startpage, defaultValue=None, replaceTag='Gamma'),
        'MINI'    : MetaInfoMap(startpage, defaultValue=None),
        'NSTEP'   : MetaInfoMap(startpage, defaultValue=None),
        'INBFRQ'  : MetaInfoMap(startpage, defaultValue=None),
        ' STEP '  : MetaInfoMap(startpage, defaultValue=None, replaceTag='STEP'),
        'PRTMIN'  : MetaInfoMap(startpage, defaultValue=None),
        'TOLFUN'  : MetaInfoMap(startpage, defaultValue=None),
        'TOLGRD'  : MetaInfoMap(startpage, defaultValue=None),
        'TOLITR'  : MetaInfoMap(startpage, defaultValue=None),
        'TOLSTP'  : MetaInfoMap(startpage, defaultValue=None),
        'TFREQ'   : MetaInfoMap(startpage, defaultValue=None),
        ' PCUT '  : MetaInfoMap(startpage, defaultValue=None, replaceTag='PCUT'),
        'IHBFRQ'  : MetaInfoMap(startpage, defaultValue=None),
        'NCGCYC'  : MetaInfoMap(startpage, defaultValue=None, matchFirst=4),
        'NPRINT'  : MetaInfoMap(startpage, defaultValue=None, matchFirst=4),
        'NONBOND OPTION FLAGS:'    : MetaInfoMap(startpage, defaultValue=None,
            appendMatchesList=[('ELEC', 'MW'), ('VDW', 'MW'), ('ATOM', 'MW'),
                               ('RDIE', 'MW'), ('SWIT', 'MW'), ('VATO', 'MW'),
                               ('VSWI', 'MW'), ('BYGR', 'MW'), ('NOEX', 'MW'),
                               ('NOEW', 'MW')],
            appendMatchesUntil='CUTNB  =', appendMaxLines=2, addAsList=True),
        'CUTNB'   : MetaInfoMap(startpage, defaultValue=None),
        'CTEXNB'  : MetaInfoMap(startpage, defaultValue=None),
        'CTONNB'  : MetaInfoMap(startpage, defaultValue=None),
        'CTOFNB'  : MetaInfoMap(startpage, defaultValue=None),
        'CGONNB'  : MetaInfoMap(startpage, defaultValue=None),
        'CGOFNB'  : MetaInfoMap(startpage, defaultValue=None),
        'WMIN'    : MetaInfoMap(startpage, defaultValue=None),
        'CDIE'    : MetaInfoMap(startpage, defaultValue=None),
        'SWITCH'  : MetaInfoMap(startpage, defaultValue=None, matchFirst=4),
        'VSWITCH' : MetaInfoMap(startpage, defaultValue=None, matchFirst=4),
        'ATOMS'   : MetaInfoMap(startpage, defaultValue=None, matchFirst=4, matchAlso='CHARMM>'),
        'WRNMXD'  : MetaInfoMap(startpage, defaultValue=None),
        'E14FAC'  : MetaInfoMap(startpage, defaultValue=None),
        ' EPS '   : MetaInfoMap(startpage, defaultValue=None, replaceTag='EPS'),
        'NBXMOD'  : MetaInfoMap(startpage, defaultValue=None),
        'CUToff Hydrogen Bond  distance' : MetaInfoMap(startpage, defaultValue=None,
                                                       replaceTag='hydrogen bond cutoff distance'),
        '   Angle =' : MetaInfoMap(startpage, defaultValue=None,
                                   replaceTag='hydrogen bond cutoff angle'),
        'CuT switching ON HB dist.' : MetaInfoMap(startpage, defaultValue=None,
                                                  replaceTag='hydrogen bond switching on distance'),
        'OFf HB dist.' : MetaInfoMap(startpage, defaultValue=None,
                                     replaceTag='hydrogen bond switching off distance'),
        'CuT switching ON Hb Angle' : MetaInfoMap(startpage, defaultValue=None,
                                                  replaceTag='hydrogen bond switching on angle'),
        'OFf Hb Angle' : MetaInfoMap(startpage, defaultValue=None,
                                     replaceTag='hydrogen bond switching off angle'),
        'ACCEptor antecedents' : MetaInfoMap(startpage, defaultValue=None),
        'HBFIND-exclusions' : MetaInfoMap(startpage, defaultValue=None,
                                          replaceTag='hbond exclusions due to distance cutoff'),
        'due to distance cutoff,' : MetaInfoMap(startpage, defaultValue=None,
                                                replaceTag='hbond exclusions due to angle cutoff'),
        'HBEDIT-deletions' : MetaInfoMap(startpage, defaultValue=None,
                                         replaceTag='hbond deletions due to duplications'),
        'due to duplications,' : MetaInfoMap(startpage, defaultValue=None,
                                             replaceTag='hbond deletions due to best option'),
        'due to fixed atoms' : MetaInfoMap(startpage, defaultValue=None, matchWith='PW',
                                           replaceTag='hbond deletions due to fixed atoms'),
        'due to exclusions' : MetaInfoMap(startpage, defaultValue=None, matchWith='PW',
                                          replaceTag='hbond deletions due to exclusion'),
        'HBEDIT: currently' : MetaInfoMap(startpage, defaultValue=None,
                                          replaceTag='hydrogen bonds present'),
        'NCGCYC'  : MetaInfoMap(startpage, defaultValue=None),
        'Minimization exiting with' : MetaInfoMap(startpage, defaultValue=None,
                matchWith='EOL', replaceTag='minimization exit status'),
        'DYNA'    : MetaInfoMap(startpage, defaultValue=None),
        'AKMASTP' : MetaInfoMap(startpage, defaultValue=None),
        'FIRSTT'  : MetaInfoMap(startpage, defaultValue=None),
        'ISEED'   : MetaInfoMap(startpage, defaultValue=None),
        'IPRFRQ'  : MetaInfoMap(startpage, defaultValue=None),
        'IHTFRQ'  : MetaInfoMap(startpage, defaultValue=None),
        'IEQFRQ'  : MetaInfoMap(startpage, defaultValue=None),
        'IUNREA'  : MetaInfoMap(startpage, defaultValue=None),
        'IUNWRI'  : MetaInfoMap(startpage, defaultValue=None),
        'IUNOS'   : MetaInfoMap(startpage, defaultValue=None),
        'IUNCRD'  : MetaInfoMap(startpage, defaultValue=None),
        'IUNVEL'  : MetaInfoMap(startpage, defaultValue=None),
        'IUNXYZ'  : MetaInfoMap(startpage, defaultValue=None),
        'KUNIT'   : MetaInfoMap(startpage, defaultValue=None),
        'NSAVC'   : MetaInfoMap(startpage, defaultValue=None),
        'NSAVV'   : MetaInfoMap(startpage, defaultValue=None),
        'NSAVX'   : MetaInfoMap(startpage, defaultValue=None),
        'ISCALE'  : MetaInfoMap(startpage, defaultValue=None),
        'ISCVEL'  : MetaInfoMap(startpage, defaultValue=None),
        'IASORS'  : MetaInfoMap(startpage, defaultValue=None),
        'IASVEL'  : MetaInfoMap(startpage, defaultValue=None),
        'ICHECW'  : MetaInfoMap(startpage, defaultValue=None),
        'NTRFRQ'  : MetaInfoMap(startpage, defaultValue=None),
        'ILBFRQ'  : MetaInfoMap(startpage, defaultValue=None),
        'IMGFRQ'  : MetaInfoMap(startpage, defaultValue=None),
        'ISVFRQ'  : MetaInfoMap(startpage, defaultValue=None),
        'NCYCLE'  : MetaInfoMap(startpage, defaultValue=None, matchFirst=4),
        'NSNOS'   : MetaInfoMap(startpage, defaultValue=None),
        'TEMINC'  : MetaInfoMap(startpage, defaultValue=None),
        'TSTRUC'  : MetaInfoMap(startpage, defaultValue=None),
        'FINALT'  : MetaInfoMap(startpage, defaultValue=None),
        'TWINDH'  : MetaInfoMap(startpage, defaultValue=None),
        'TWINDL'  : MetaInfoMap(startpage, defaultValue=None),
        'TIME STEP' : MetaInfoMap(startpage, defaultValue=None),
        'RANDOM NUM. GEN. SEED\(S\)' : MetaInfoMap(startpage, defaultValue=None, matchWith='EOL'),
        'NUMBER OF DEGREES OF FREEDOM' : MetaInfoMap(startpage, defaultValue=None),
        'GAUSSIAN OPTION                  IS' : MetaInfoMap(startpage, defaultValue=None),
        'VELOCITIES ASSIGNED AT TEMPERATURE' : MetaInfoMap(startpage, defaultValue=None),
        'SEEDS>'  : MetaInfoMap(startpage, defaultValue=None, matchWith='EOL'),
        'SHAKE TOLERANCE' : MetaInfoMap(startpage, defaultValue=None),
        'DYNA'    : MetaInfoMap(startpage, defaultValue=None),
        'STRT'    : MetaInfoMap(startpage, defaultValue=None),
        'REST'    : MetaInfoMap(startpage, defaultValue=None),
        'QREF'    : MetaInfoMap(startpage, defaultValue=None),
        'TREF'    : MetaInfoMap(startpage, defaultValue=None),
        'HOOVER'  : MetaInfoMap(startpage, defaultValue=None, matchFirst=4),
        'REFT'    : MetaInfoMap(startpage, defaultValue=None, matchFirst=4),
        'TMASS'   : MetaInfoMap(startpage, defaultValue=None),
        'PCONS'   : MetaInfoMap(startpage, defaultValue=None),
        'PMASS'   : MetaInfoMap(startpage, defaultValue=None),
        }

    filecntrllist = {
        'OPEN'  : MetaInfoMap(startpage, defaultValue=None),
        'READ'  : MetaInfoMap(startpage, defaultValue=None),
        'WRITE' : MetaInfoMap(startpage, defaultValue=None),
        'CARD'  : MetaInfoMap(startpage, defaultValue=None),
        'COOR'  : MetaInfoMap(startpage, defaultValue=None),
        'FILE'  : MetaInfoMap(startpage, defaultValue=None),
        'UNIT'  : MetaInfoMap(startpage, defaultValue=None),
        'NAME'  : MetaInfoMap(startpage, defaultValue=None),
        'Parameter:' : MetaInfoMap(startpage, defaultValue=None, matchWith='EOL'),
        }

    readcntrllist = {
        'READ'  : MetaInfoMap(startpage, defaultValue=None),
        'WRITE' : MetaInfoMap(startpage, defaultValue=None),
        'CARD'  : MetaInfoMap(startpage, defaultValue=None),
        'COOR'  : MetaInfoMap(startpage, defaultValue=None),
        'FILE'  : MetaInfoMap(startpage, defaultValue=None),
        'UNIT'  : MetaInfoMap(startpage, defaultValue=None),
        }

    startpage.update({
        'metaNameTag'     : 'mdout',
        'activeSections'  : ['section_single_configuration_calculation']
        })
    mddatalist = {
        'CYCLE'     : MetaInfoMap(startpage, matchFirst=4),
        'EVAL'      : MetaInfoMap(startpage, matchLast=4),
        'STEP'      : MetaInfoMap(startpage, matchFirst=4),
        'ENERGY'    : MetaInfoMap(startpage, matchFirst=4),
        'TOTENER'   : MetaInfoMap(startpage, matchFirst=4),
        'TOTKE'     : MetaInfoMap(startpage, matchFirst=4),
        'TEMPERATURE' : MetaInfoMap(startpage, matchFirst=4),
        'DELTA-E'   : MetaInfoMap(startpage, matchFirst=4),
        'GRMS'      : MetaInfoMap(startpage, matchFirst=4),
        'HFCTOTE'   : MetaInfoMap(startpage, matchFirst=4),
        'HFCKE'     : MetaInfoMap(startpage, matchFirst=4),
        'EHFCOR'    : MetaInfoMap(startpage, matchFirst=4),
        'VIRKE'     : MetaInfoMap(startpage, matchFirst=4),
        'STEP-SIZE' : MetaInfoMap(startpage),
        'BONDS'     : MetaInfoMap(startpage, matchFirst=4),
        'ANGLES'    : MetaInfoMap(startpage, matchFirst=4),
        'UREY-B'    : MetaInfoMap(startpage, matchFirst=4),
        'DIHEDRALS' : MetaInfoMap(startpage, matchFirst=4),
        'IMPROPERS' : MetaInfoMap(startpage, matchFirst=4),
        'VDWAALS'   : MetaInfoMap(startpage, matchFirst=3),
        'ELEC'      : MetaInfoMap(startpage, matchFirst=4),
        'HBONDS'    : MetaInfoMap(startpage, matchFirst=4),
        'ASP'       : MetaInfoMap(startpage),
        'USER'      : MetaInfoMap(startpage),
        'Virial-Tensor' : MetaInfoMap(startpage),
        'Pressure-Tensor' : MetaInfoMap(startpage),
        'TIME'      : MetaInfoMap(startpage, matchFirst=4),
        'VIRI'      : MetaInfoMap(startpage, matchFirst=4),
        'VIRE'      : MetaInfoMap(startpage, matchFirst=4),
        'PRESSE'    : MetaInfoMap(startpage, matchFirst=4),
        'PRESSI'    : MetaInfoMap(startpage, matchFirst=4),
        'VOLUME'    : MetaInfoMap(startpage, matchFirst=4),
        'BPRE'      : MetaInfoMap(startpage, matchFirst=4),
        'VTOT'      : MetaInfoMap(startpage, matchFirst=4),
        'VKIN'      : MetaInfoMap(startpage, matchFirst=4),
        'EHYS'      : MetaInfoMap(startpage, matchFirst=4),
        'PRSE'      : MetaInfoMap(startpage, matchFirst=4),
        'PRSI'      : MetaInfoMap(startpage, matchFirst=4),
        'CMAP'      : MetaInfoMap(startpage, matchFirst=4),
        'STRB'      : MetaInfoMap(startpage, matchFirst=4),
        'OOPL'      : MetaInfoMap(startpage, matchFirst=4),
        'HARM'      : MetaInfoMap(startpage, matchFirst=4),
        'CDIH'      : MetaInfoMap(startpage, matchFirst=4),
        'CPUC'      : MetaInfoMap(startpage, matchFirst=4),
        'CIC'       : MetaInfoMap(startpage, matchFirst=4),
        'CDRO'      : MetaInfoMap(startpage, matchFirst=4),
        'NOE'       : MetaInfoMap(startpage, matchFirst=4),
        'SBOU'      : MetaInfoMap(startpage, matchFirst=4),
        'IMNB'      : MetaInfoMap(startpage, matchFirst=4),
        'EXTE'      : MetaInfoMap(startpage, matchFirst=4),
        'EWKS'      : MetaInfoMap(startpage, matchFirst=4),
        'EWSE'      : MetaInfoMap(startpage, matchFirst=4),
        'RXNF'      : MetaInfoMap(startpage, matchFirst=4),
        'ST2'       : MetaInfoMap(startpage, matchFirst=4),
        'IMST'      : MetaInfoMap(startpage, matchFirst=4),
        'TSM'       : MetaInfoMap(startpage, matchFirst=4),
        'QMEL'      : MetaInfoMap(startpage, matchFirst=4),
        'QMVD'      : MetaInfoMap(startpage, matchFirst=4),
        'EHAR'      : MetaInfoMap(startpage, matchFirst=4),
        'GEO'       : MetaInfoMap(startpage, matchFirst=4),
        'MDIP'      : MetaInfoMap(startpage, matchFirst=4),
        'PRMS'      : MetaInfoMap(startpage, matchFirst=4),
        'PANG'      : MetaInfoMap(startpage, matchFirst=4),
        'SSBP'      : MetaInfoMap(startpage, matchFirst=4),
        'BK4D'      : MetaInfoMap(startpage, matchFirst=4),
        'SHEL'      : MetaInfoMap(startpage, matchFirst=4),
        'RESD'      : MetaInfoMap(startpage, matchFirst=4),
        'SHAP'      : MetaInfoMap(startpage, matchFirst=4),
        'PULL'      : MetaInfoMap(startpage, matchFirst=4),
        'POLA'      : MetaInfoMap(startpage, matchFirst=4),
        'DMC'       : MetaInfoMap(startpage, matchFirst=4),
        'RGY'       : MetaInfoMap(startpage, matchFirst=4),
        'EWEX'      : MetaInfoMap(startpage, matchFirst=4),
        'EWQC'      : MetaInfoMap(startpage, matchFirst=4),
        'EWUT'      : MetaInfoMap(startpage, matchFirst=4),
        'VEXX'      : MetaInfoMap(startpage, matchFirst=4),
        'VEXY'      : MetaInfoMap(startpage, matchFirst=4),
        'VEXZ'      : MetaInfoMap(startpage, matchFirst=4),
        'VEYX'      : MetaInfoMap(startpage, matchFirst=4),
        'VEYY'      : MetaInfoMap(startpage, matchFirst=4),
        'VEYZ'      : MetaInfoMap(startpage, matchFirst=4),
        'VEZX'      : MetaInfoMap(startpage, matchFirst=4),
        'VEZY'      : MetaInfoMap(startpage, matchFirst=4),
        'VEZZ'      : MetaInfoMap(startpage, matchFirst=4),
        'VIXX'      : MetaInfoMap(startpage, matchFirst=4),
        'VIXY'      : MetaInfoMap(startpage, matchFirst=4),
        'VIXZ'      : MetaInfoMap(startpage, matchFirst=4),
        'VIYX'      : MetaInfoMap(startpage, matchFirst=4),
        'VIYY'      : MetaInfoMap(startpage, matchFirst=4),
        'VIYZ'      : MetaInfoMap(startpage, matchFirst=4),
        'VIZX'      : MetaInfoMap(startpage, matchFirst=4),
        'VIZY'      : MetaInfoMap(startpage, matchFirst=4),
        'VIZZ'      : MetaInfoMap(startpage, matchFirst=4),
        'PEXX'      : MetaInfoMap(startpage, matchFirst=4),
        'PEXY'      : MetaInfoMap(startpage, matchFirst=4),
        'PEXZ'      : MetaInfoMap(startpage, matchFirst=4),
        'PEYX'      : MetaInfoMap(startpage, matchFirst=4),
        'PEYY'      : MetaInfoMap(startpage, matchFirst=4),
        'PEYZ'      : MetaInfoMap(startpage, matchFirst=4),
        'PEZX'      : MetaInfoMap(startpage, matchFirst=4),
        'PEZY'      : MetaInfoMap(startpage, matchFirst=4),
        'PEZZ'      : MetaInfoMap(startpage, matchFirst=4),
        'PIXX'      : MetaInfoMap(startpage, matchFirst=4),
        'PIXY'      : MetaInfoMap(startpage, matchFirst=4),
        'PIXZ'      : MetaInfoMap(startpage, matchFirst=4),
        'PIYX'      : MetaInfoMap(startpage, matchFirst=4),
        'PIYY'      : MetaInfoMap(startpage, matchFirst=4),
        'PIYZ'      : MetaInfoMap(startpage, matchFirst=4),
        'PIZX'      : MetaInfoMap(startpage, matchFirst=4),
        'PIZY'      : MetaInfoMap(startpage, matchFirst=4),
        'PIZZ'      : MetaInfoMap(startpage, matchFirst=4),
        }

    startpage.update({
        'metaNameTag'     : 'parm',
        'activeSections'  : [PARSERTAG+'_mdin_method']
        })
    extralist = {
        'flags' : MetaInfoMap(startpage),
        'number_of_atoms' : MetaInfoMap(startpage),
        'minimization' : MetaInfoMap(startpage, activeInfo=True),
        'integrator' : MetaInfoMap(startpage, activeInfo=True),
        'thermostat' : MetaInfoMap(startpage, activeInfo=True),
        'barostat' : MetaInfoMap(startpage, activeInfo=True),
        'box_info' : MetaInfoMap(startpage),
        'unitcell_radius' : MetaInfoMap(startpage),
        'total_memory' : MetaInfoMap(startpage),
        'file_format' : MetaInfoMap(startpage),
        'file_version' : MetaInfoMap(startpage),
        'file_date' : MetaInfoMap(startpage),
        'file_time' : MetaInfoMap(startpage)
        }

    if deflist == 'mddata':
        namelist = mddatalist
#    elif deflist == 'parm':
#        namelist = parmlist
    elif deflist == 'extra':
        namelist = extralist
    elif deflist == 'filecntrl':
        namelist = filecntrllist
    elif deflist == 'stepcontrol':
        namelist = stepcontrol
    else:
        namelist = cntrllist
    return MapDictionary(namelist)

def set_Dictionaries(self):
        self.unitDict = get_unitDict('si')
        self.akmaDict = get_unitDict('akma')
        self.fileDict = get_fileListDict()
        self.cntrlDict = get_nameListDict('cntrl')
        self.filecntrlDict = get_nameListDict('filecntrl')
        #self.parmDict = get_nameListDict('parm')
        self.mddataDict = get_nameListDict('mddata')
        self.extraDict = get_nameListDict('extra')
        self.mdoutHeaderDict = {}
        #self.fileUnitDict = {}
        self.stepcontrolDict = {
            'logsteps'       : None,
            'nextlogsteps'   : None,
            'trajsteps'      : None,
            'velsteps'       : None,
            'forcesteps'     : None,
            'steps'          : None,
            'follow'         : None,
            'sectioncontrol' : None,
            'cntrlparmstep'  : [-1],
        }
        self.metaDicts = {
            'file'   : self.fileDict,
            'cntrl'  : self.cntrlDict,
            'filecntrl'  : self.filecntrlDict,
#            'parm'   : self.parmDict,
            'mddata' : self.mddataDict,
            'extra'  : self.extraDict,
            }
        self.sectionDict = {
                'section' : {
                    "metaNameTag"      : ['input_output_files',
                                          'control_parameters'],
                    "listTypStr"       : 'type_section',
                    "repeatingSection" : False,
                    "supraNames"       : ["section_run"]
                    }
                }

def get_updateDictionary(self, defname):

    def value_convert_array(itemdict):
        val = itemdict["value"]
        if(val is not None and isinstance(val, str)):
            if("[" in val or "(" in val):
                return False, np.asarray(val), itemdict
        return False, val, itemdict

    def value_convert_array_norm(itemdict):
        val = []
        depdict = itemdict["depends"]
        for item in depdict["value"]:
            st=self.metaStorage.fetchAttrValue(item)
            if(st is not None and isinstance(st, str)):
                if("[" in st or "(" in st):
                    val.append(list(storedtext))
        if val:
            return False, np.linalg.norm(np.asarray(val)), itemdict
        else:
            return False, itemdict["value"], itemdict

    startpage = {
        'metaHeader'      : '',
        'metaNameTag'     : '',
        'activeMetaNames' : [],
        'activeSections'  : ['section_sampling_method','section_single_configuration_calculation',PARSERTAG+'_mdout']
        }

    # ---------------------------------------------------------------
    #   Definitions of meta data values for section_sampling_method
    # ---------------------------------------------------------------
    sampling = {
        #'ensemble_type' : MetaInfoMap(startpage, activeInfo=True,
        #    depends=[
        #        {'test' : [['DYNA', ' is not None'],
        #                   ['FIRSTT', ' in [\"tcouple\",'
        #                                  '\"rescale\",'
        #                                  '\"reassign\",'
        #                                  '\"andersen\",'
        #                                  '\"langevin\"]'],
        #                   ['barostat', ' in [\"berendsen\",'
        #                                 '\"langevin\"]']],
        #         'assign' : 'NPT'},
        #        {'test' : [['minimization', ' is None'],
        #                   ['thermostat', ' in [\"langevin\"]'],
        #                   ['thermostat', ' not in [\"tcouple\",'
        #                                  '\"rescale\",'
        #                                  '\"reassign\",'
        #                                  '\"andersen\"]'],
        #                   ['barostat', ' is None']],
        #         'assign' : 'Langevin'},
        #        {'test' : [['minimization', ' is None'],
        #                   ['thermostat', ' in [\"tcouple\",'
        #                                  '\"rescale\",'
        #                                  '\"reassign\",'
        #                                  '\"andersen\"]'],
        #                   ['barostat', ' is None']],
        #         'assign' : 'NVT'},
        #        {'test' : [['minimization', ' is None'],
        #                   ['thermostat', ' is None'],
        #                   ['barostat', ' is None']],
        #         'assign' : 'NVE'},
        #        {'test' : [['minimization', ' is not None']],
        #         'assign' : 'minimization'},
        #        ],
        #    lookupdict=self.extraDict
        #    ),
        'sampling_method' : MetaInfoMap(startpage, activeInfo=True,
            depends=[
                {'test' : [['MINI', ' is not None']],
                 'assign' : 'geometry_optimization'},
                {'test' : [['DYNA', ' is not None']],
                 'assign' : 'molecular_dynamics'}
                ],
            lookupdict=self.cntrlDict
            ),
#            'settings_geometry_optimization' : MetaInfoMap(startpage),
#            'settings_metadynamics' : MetaInfoMap(startpage),
#            'settings_molecular_dynamics' : MetaInfoMap(startpage),
#            'settings_monte_carlo' : MetaInfoMap(startpage),
#        'geometry_optimization_energy_change' : MetaInfoMap(startpage,
#            depends={
#                '' : {'imin' : '1'},
#                },
#            lookupdict=self.cntrlDict
#            ),
#       'geometry_optimization_geometry_change' : MetaInfoMap(startpage),
        'geometry_optimization_method' : MetaInfoMap(startpage,
            depends=[
                {'test' : [['MINI',' is not None'],
                           ['MINI', ' in [\"SD\",\"sd\"]']],
                 'assign' : 'SD'},
                {'test' : [['MINI',' is not None'],
                           ['MINI', ' in [\"ABNR\",\"abnr\"]']],
                 'assign' : 'Adopted Basis Newton-Raphson'},
                {'test' : [['MINI',' is not None'],
                           ['MINI', ' in [\"NRAP\",\"nrap\"]']],
                 'assign' : 'Newton-Raphson'},
                {'test' : [['MINI',' is not None'],
                           ['MINI', ' in [\"POWELL\",\"powell\"]']],
                 'assign' : 'Powell'},
                {'test' : [['MINI',' is not None'],
                           ['MINI', ' in [\"POWE\",\"powe\"]']],
                 'assign' : 'Powell'},
                {'test' : [['MINI',' is not None'],
                           ['MINI', ' in [\"TNPACK\",\"tnpack\"]']],
                 'assign' : 'Truncated Newton Method'},
                {'test' : [['MINI',' is not None'],
                           ['MINI', ' not in [\"SD\",\"sd\",'
                                             '\"ABNR\",\"abnr\",'
                                             '\"NRAP\",\"nrap\",'
                                             '\"POWE\",\"powe\",'
                                             '\"POWELL\",\"powell\",'
                                             '\"TNPACK\",\"tnpack\"]']],
                 'assign' : 'CG'},
                ],
            lookupdict=self.cntrlDict,
            activeInfo=True,
            ),
#       'geometry_optimization_threshold_force' : MetaInfoMap(startpage),
        #'x_charmm_barostat_type' : MetaInfoMap(startpage,
        #    depends=[
        #        {'test' : [['minimization', ' is None'],
        #                   ['barostat', '== \"berendsen\"']],
        #         'assign' : 'Berendsen'},
        #        {'test' : [['minimization', ' is None'],
        #                   ['barostat', '== \"langevin\"']],
        #         'assign' : 'Nose-Hoover Langevin'}
        #        ],
        #    lookupdict=self.extraDict,
        #    #autoSections=True,
        #    activeInfo=True,
        #    activeSections=['settings_barostat']
        #    ),
        #'x_charmm_barostat_target_pressure' : MetaInfoMap(startpage,
        #    depends=[
        #        {'test' : [['TARGET PRESSURE', ' is not None']],
        #         'value' : 'TARGET PRESSURE'}
        #        ],
        #    lookupdict=self.cntrlDict,
        #    valtype='float',
        #    unitdict=self.unitDict,
        #    unit='atmosphere',
        #    #autoSections=True,
        #    activeInfo=True,
        #    activeSections=['settings_barostat']
        #    ),
        #'x_charmm_barostat_tau' : MetaInfoMap(startpage,
        #    depends=[
        #        {'test' : [['LANGEVIN OSCILLATION PERIOD', ' is not None']],
        #         'value' : 'LANGEVIN OSCILLATION PERIOD'},
        #        {'test' : [['BERENDSEN RELAXATION TIME', ' is not None']],
        #         'value' : 'BERENDSEN RELAXATION TIME'}
        #        ],
        #    lookupdict=self.cntrlDict,
        #    valtype='float',
        #    unitdict=self.unitDict,
        #    unit='akmatime',
        #    #autoSections=True,
        #    activeInfo=True,
        #    activeSections=['settings_barostat']
        #    ),
        #'x_charmm_integrator_type' : MetaInfoMap(startpage,
        #    depends=[
        #        {'test' : [['integrator', ' is not None']],
        #         'value' : 'integrator'},
        #        {'test' : [['thermostat', ' == \"langevin\"']],
        #         'assign' : 'Langevin'}
        #        ],
        #    lookupdict=self.extraDict,
        #    #autoSections=True,
        #    activeInfo=True,
        #    activeSections=['settings_integrator']
        #    ),
        'x_charmm_integrator_dt' : MetaInfoMap(startpage,
            depends=[
                {'test' : [['DYNA', ' is not None'],
                           ['TIME STEP', ' is not None']],
                 'value' : 'TIME STEP'},
                ],
            lookupdict=self.cntrlDict,
            valtype='float',
            unitdict=self.unitDict,
            unit='akmatime',
            #autoSections=True,
            activeInfo=True,
            activeSections=['settings_integrator']
            ),
        'x_charmm_number_of_steps_requested' : MetaInfoMap(startpage,
            depends=[{'value' : 'NSTEP'}],
            lookupdict=self.cntrlDict,
            valtype='int',
            #autoSections=True,
            activeInfo=True,
            activeSections=['settings_integrator']
            ),
        #'x_charmm_thermostat_type' : MetaInfoMap(startpage,
        #    depends=[
        #        {'test' : [['minimization', ' is None'],
        #                   ['thermostat', ' == \"tcouple\"']],
        #         'assign' : 'Berendsen'},
        #        {'test' : [['minimization', ' is None'],
        #                   ['thermostat', ' == \"rescale\"']],
        #         'assign' : 'Velocity Rescaling'},
        #        {'test' : [['minimization', ' is None'],
        #                   ['thermostat', ' == \"reassign\"']],
        #         'assign' : 'Velocity Reassigning'},
        #        {'test' : [['minimization', ' is None'],
        #                   ['thermostat', ' == \"andersen\"']],
        #         'assign' : 'Andersen'},
        #        {'test' : [['minimization', ' is None'],
        #                   ['thermostat', ' == \"langevin\"']],
        #         'assign' : 'Nose-Hoover Langevin'},
        #        ],
        #    lookupdict=self.extraDict,
        #    #autoSections=True,
        #    activeInfo=True,
        #    activeSections=['settings_thermostat']
        #    ),
        'x_charmm_thermostat_target_temperature' : MetaInfoMap(startpage,
            depends=[
                {'test' : [['DYNA', ' is not None'],
                           ['FINALT', ' is not None']],
                 'value' : 'FINALT'},
                ],
            lookupdict=self.cntrlDict,
            valtype='float',
            unitdict=self.unitDict,
            unit='Kelvin',
            #autoSections=True,
            activeInfo=True,
            activeSections=['settings_thermostat']
            ),
        #'x_charmm_thermostat_tau' : MetaInfoMap(startpage,
        #    depends=[
        #        {'test' : [['MINIMIZATION', ' is None'],
        #                   ['VELOCITY QUENCHING', ' is None'],
        #                   ['VELOCITY RESCALE FREQ', ' is not None']],
        #         'value' : 'VELOCITY RESCALE FREQ'},
        #        {'test' : [['MINIMIZATION', ' is None'],
        #                   ['VELOCITY QUENCHING', ' is None'],
        #                   ['VELOCITY REASSIGNMENT FREQ', ' is not None']],
        #         'value' : 'VELOCITY REASSIGNMENT FREQ'},
        #        {'test' : [['MINIMIZATION', ' is None'],
        #                   ['VELOCITY QUENCHING', ' is None'],
        #                   ['LOWE-ANDERSEN RATE', ' is not None']],
        #         'value' : 'LOWE-ANDERSEN RATE'},
        #        ],
        #    lookupdict=self.cntrlDict,
        #    valtype='float',
        #    unitdict=self.unitDict,
        #    unit='pico-second',
        #    #autoSections=True,
        #    activeInfo=True,
        #    activeSections=['settings_thermostat']
        #    ),
        'x_charmm_periodicity_type' : MetaInfoMap(startpage,
            depends=[
                {'test' : [['CRYSTAL', ' is not None']],
                 'assign' : 'periodic boundaries'},
                {'test' : [['CRYSTAL',' is None']],
                 'assign' : 'no periodic boundaries'},
                ],
            lookupdict=self.cntrlDict,
            #autoSections=True,
            activeInfo=True,
            activeSections=['settings_thermostat']
            )
        }

    # ------------------------------------------------------------
    #   Definitions for section_single_configuration_calculation
    # ------------------------------------------------------------
    singleconfcalc = {
        #'atom_forces_type' : MetaInfoMap(startpage,
        #    depends=[{'assign' : 'Force Field'}],
        #    lookupdict=self.mddataDict
        #    ),
        'energy_correction_entropy' : MetaInfoMap(startpage),
        'energy_current' : MetaInfoMap(startpage),
        'energy_electrostatic' : MetaInfoMap(startpage,
            depends=[{'value' : 'ELEC'}],
            valtype='float',
            unitdict=self.unitDict,
            unit=self.akmaDict['energy'],
            activeInfo=True,
            lookupdict=self.mddataDict
            ),
        'energy_free_per_atom' : MetaInfoMap(startpage),
        'energy_free' : MetaInfoMap(startpage),
        #'energy_method_current' : MetaInfoMap(startpage,
        #    depends=[{'assign' : 'Force Field'}],
        #    lookupdict=self.mddataDict
        #    ),
        'energy_t0_per_atom' : MetaInfoMap(startpage),
        'energy_total_t0_per_atom' : MetaInfoMap(startpage),
        'energy_total_t0' : MetaInfoMap(startpage,
            depends=[{'value' : 'ENERGY'}],
            valtype='float',
            unitdict=self.unitDict,
            unit=self.akmaDict['energy'],
            activeInfo=True,
            lookupdict=self.mddataDict
            ),
        'energy_total' : MetaInfoMap(startpage,
            depends=[{'value' : 'TOTENER'}],
            valtype='float',
            unitdict=self.unitDict,
            unit=self.akmaDict['energy'],
            activeInfo=True,
            lookupdict=self.mddataDict
            ),
        'hessian_matrix' : MetaInfoMap(startpage),
        'single_configuration_calculation_converged' : MetaInfoMap(startpage),
        'single_configuration_calculation_to_system_ref' : MetaInfoMap(startpage),
        'single_configuration_calculation_to_method_ref' : MetaInfoMap(startpage),
        'time_calculation' : MetaInfoMap(startpage),
        'time_single_configuration_calculation_cpu1_end' : MetaInfoMap(startpage),
        'time_single_configuration_calculation_cpu1_start' : MetaInfoMap(startpage),
        'time_single_configuration_calculation_date_end' : MetaInfoMap(startpage),
        'time_single_configuration_calculation_date_start' : MetaInfoMap(startpage),
        'time_single_configuration_calculation_wall_end' : MetaInfoMap(startpage),
        'time_single_configuration_calculation_wall_start' : MetaInfoMap(startpage),
        'stress_tensor_kind' : MetaInfoMap(startpage,
            depends=[
                {'test' : [['MINI', ' is not None']],
                 'assign' : 'geometry_optimization'},
                {'test' : [['DYNA', ' is not None']],
                 'assign' : 'molecular_dynamics'}
                ],
            activeInfo=True,
            lookupdict=self.extraDict
            ),
        'stress_tensor_value' : MetaInfoMap(startpage)
        }

    # section_single_energy_van_der_Waals of section_single_configuration_calculation
    singlevdw = {
        'energy_van_der_waals_value' : MetaInfoMap(startpage,
            depends=[{'value' : 'VDWAALS'}],
            lookupdict=self.mddataDict,
            valtype='float',
            unitdict=self.unitDict,
            unit=self.akmaDict['energy'],
            #autoSections=True,
            activeSections=['section_energy_van_der_waals']
            ),
        }

    # Info for section_restricted_uri
    restrictions = {
        'number_of_restricted_uri_files' : MetaInfoMap(startpage,
            value=int(1),
            #autoSections=True,
            activeInfo=True,
            activeSections=['section_restricted_uri']
            ),
        'restricted_uri_files' : MetaInfoMap(startpage,
            #autoSections=True,
            activeInfo=True,
            activeSections=['section_restricted_uri'],
            subfunction={
                'function' : self.parameter_file_name,
                'supportDict' : self.fileDict,
                },
            ),
        'restricted_uri_license' : MetaInfoMap(startpage,
            value='CHARMM License',
            #autoSections=True,
            activeInfo=True,
            activeSections=['section_restricted_uri']
            ),
        'restricted_uri_restriction' : MetaInfoMap(startpage,
            value='any access',
            #autoSections=True,
            activeInfo=True,
            activeSections=['section_restricted_uri']
            ),
        'restricted_uri_reason' : MetaInfoMap(startpage,
            value='propriety license',
            #autoSections=True,
            activeInfo=True,
            activeSections=['section_restricted_uri']
            ),
        'restricted_uri_issue_authority' : MetaInfoMap(startpage,
            value='CHARMM',
            #autoSections=True,
            activeInfo=True,
            activeSections=['section_restricted_uri']
            ),
        }

    # ------------------------------------------
    #   Definitions for section_frame_sequence
    # ------------------------------------------
    frameseq = {
        #'xxx_to_rm_frame_sequence_conserved_quantity_frames' : MetaInfoMap(startpage,
        #    depends=[{'store' : 'TS'}],
        #    valtype='int',
        #    lookupdict=self.mddataDict
        #    ),
        #'frame_sequence_conserved_quantity_stats' : MetaInfoMap(startpage),
        #'xxx_conserved_quantity' : MetaInfoMap(startpage,
        #    depends=[{'store' : ''}],
        #    valtype='float',
        #    unitdict=self.unitDict,
        #    unit='kilo-joule/mol',
        #    lookupdict=self.mddataDict
        #    ),
        'frame_sequence_continuation_kind' : MetaInfoMap(startpage),
        'frame_sequence_external_url' : MetaInfoMap(startpage),
        'xxx_to_rm_frame_sequence_kinetic_energy_frames' : MetaInfoMap(startpage,
            depends=[{'store' : 'STEP'}],
            valtype='int',
            lookupdict=self.mddataDict
            ),
        'frame_sequence_kinetic_energy_stats' : MetaInfoMap(startpage),
        'xxx_kinetic_energy' : MetaInfoMap(startpage,
            depends=[{'store' : 'TOTKE'}],
            valtype='float',
            unitdict=self.unitDict,
            unit=self.akmaDict['energy'],
            lookupdict=self.mddataDict
            ),
        'frame_sequence_to_frames_ref' : MetaInfoMap(startpage),
        'xxx_to_rm_frame_sequence_potential_energy_frames' : MetaInfoMap(startpage,
            depends=[{'store' : 'STEP'}],
            valtype='int',
            lookupdict=self.mddataDict
            ),
        'frame_sequence_potential_energy_stats' : MetaInfoMap(startpage),
        'xxx_potential_energy' : MetaInfoMap(startpage,
            depends=[{'store' : 'ENERGY'}],
            valtype='float',
            unitdict=self.unitDict,
            unit=self.akmaDict['energy'],
            lookupdict=self.mddataDict
            ),
        #'frame_sequence_pressure_average_frames' : MetaInfoMap(startpage,
        #    depends=[{'store' : 'STEP'}],
        #    valtype='int',
        #    lookupdict=self.mddataDict
        #    ),
        #'frame_sequence_pressure_average' : MetaInfoMap(startpage,
        #    depends=[{'store' : 'PRSI'}],
        #    valtype='float',
        #    unitdict=self.unitDict,
        #    unit='atmosphere',
        #    lookupdict=self.mddataDict
        #    ),
        'xxx_to_rm_frame_sequence_pressure_frames' : MetaInfoMap(startpage,
            depends=[{'store' : 'STEP'}],
            valtype='int',
            lookupdict=self.mddataDict
            ),
        'frame_sequence_pressure_stats' : MetaInfoMap(startpage),
        'xxx_instant_pressure' : MetaInfoMap(startpage,
            depends=[{'store' : 'PRESSI'}],
            valtype='float',
            unitdict=self.unitDict,
            unit='atmosphere',
            lookupdict=self.mddataDict
            ),
        'x_charmm_frame_sequence_external_pressure_frames' : MetaInfoMap(startpage,
            depends=[{'store' : 'STEP'}],
            valtype='int',
            lookupdict=self.mddataDict
            ),
        'x_charmm_frame_sequence_external_pressure_stats' : MetaInfoMap(startpage),
        'x_charmm_frame_sequence_external_pressure' : MetaInfoMap(startpage,
            depends=[{'store' : 'PRESSE'}],
            valtype='float',
            unitdict=self.unitDict,
            unit='atmosphere',
            lookupdict=self.mddataDict
            ),
        'x_charmm_frame_sequence_internal_pressure_frames' : MetaInfoMap(startpage,
            depends=[{'store' : 'STEP'}],
            valtype='int',
            lookupdict=self.mddataDict
            ),
        'x_charmm_frame_sequence_internal_pressure_stats' : MetaInfoMap(startpage),
        'x_charmm_frame_sequence_internal_pressure' : MetaInfoMap(startpage,
            depends=[{'store' : 'PRESSI'}],
            valtype='float',
            unitdict=self.unitDict,
            unit='atmosphere',
            lookupdict=self.mddataDict
            ),
        #'frame_sequence_temperature_average_frames' : MetaInfoMap(startpage,
        #    depends=[{'store' : 'TS'}],
        #    valtype='int',
        #    lookupdict=self.mddataDict
        #    ),
        #'frame_sequence_temperature_average' : MetaInfoMap(startpage,
        #    depends=[{'store' : 'TEMPAVG'}],
        #    valtype='float',
        #    unitdict=self.unitDict,
        #    unit='Kelvin',
        #    lookupdict=self.mddataDict
        #    ),
        'xxx_to_rm_frame_sequence_temperature_frames' : MetaInfoMap(startpage,
            depends=[{'store' : 'STEP'}],
            valtype='int',
            lookupdict=self.mddataDict
            ),
        'frame_sequence_temperature_stats' : MetaInfoMap(startpage),
        'xxx_instant_temperature' : MetaInfoMap(startpage,
            depends=[{'store' : 'TEMPERATURE'}],
            valtype='float',
            unitdict=self.unitDict,
            unit='Kelvin',
            lookupdict=self.mddataDict
            ),
        'frame_sequence_time' : MetaInfoMap(startpage,
            depends=[{'store' : 'TIME'}],
            valtype='float',
            unitdict=self.unitDict,
            unit='pico-second',
            # Calculates in AKMA units including inputs but prints in picoseconds.
            lookupdict=self.mddataDict
            ),
        'x_charmm_frame_sequence_volume_frames' : MetaInfoMap(startpage,
            activeSections=['section_frame_sequence'],
            depends=[{'store' : 'STEP'}],
            valtype='int',
            lookupdict=self.mddataDict
            ),
        'x_charmm_frame_sequence_volume' : MetaInfoMap(startpage,
            activeSections=['section_frame_sequence'],
            depends=[{'store' : 'VOLUME'}],
            valtype='float',
            unitdict=self.unitDict,
            unit='Angstrom**3',
            lookupdict=self.mddataDict
            ),
        'x_charmm_frame_sequence_total_energy_frames' : MetaInfoMap(startpage,
            activeSections=['section_frame_sequence'],
            depends=[{'store' : 'STEP'}],
            valtype='int',
            lookupdict=self.mddataDict
            ),
        'x_charmm_frame_sequence_total_energy' : MetaInfoMap(startpage,
            activeSections=['section_frame_sequence'],
            depends=[{'store' : 'TOTENER'}],
            valtype='float',
            unitdict=self.unitDict,
            unit=self.akmaDict['energy'],
            lookupdict=self.mddataDict
            ),
        'x_charmm_frame_sequence_total_kinetic_energy_frames' : MetaInfoMap(startpage,
            activeSections=['section_frame_sequence'],
            depends=[{'store' : 'STEP'}],
            valtype='int',
            lookupdict=self.mddataDict
            ),
        'x_charmm_frame_sequence_total_kinetic_energy' : MetaInfoMap(startpage,
            activeSections=['section_frame_sequence'],
            depends=[{'store' : 'TOTKE'}],
            valtype='float',
            unitdict=self.unitDict,
            unit=self.akmaDict['energy'],
            lookupdict=self.mddataDict
            ),
        'x_charmm_frame_sequence_high_frequency_correction_total_energy_frames' : MetaInfoMap(startpage,
            activeSections=['section_frame_sequence'],
            depends=[{'store' : 'STEP'}],
            valtype='int',
            lookupdict=self.mddataDict
            ),
        'x_charmm_frame_sequence_high_frequency_correction_total_energy' : MetaInfoMap(startpage,
            activeSections=['section_frame_sequence'],
            depends=[{'store' : 'HFCTOTE'}],
            valtype='float',
            unitdict=self.unitDict,
            unit=self.akmaDict['energy'],
            lookupdict=self.mddataDict
            ),
        'x_charmm_frame_sequence_high_frequency_correction_kinetic_energy_frames' : MetaInfoMap(startpage,
            activeSections=['section_frame_sequence'],
            depends=[{'store' : 'STEP'}],
            valtype='int',
            lookupdict=self.mddataDict
            ),
        'x_charmm_frame_sequence_high_frequency_correction_kinetic_energy' : MetaInfoMap(startpage,
            activeSections=['section_frame_sequence'],
            depends=[{'store' : 'HFCKE'}],
            valtype='float',
            unitdict=self.unitDict,
            unit=self.akmaDict['energy'],
            lookupdict=self.mddataDict
            ),
        'x_charmm_frame_sequence_high_frequency_correction_energy_frames' : MetaInfoMap(startpage,
            activeSections=['section_frame_sequence'],
            depends=[{'store' : 'STEP'}],
            valtype='int',
            lookupdict=self.mddataDict
            ),
        'x_charmm_frame_sequence_high_frequency_correction_energy' : MetaInfoMap(startpage,
            activeSections=['section_frame_sequence'],
            depends=[{'store' : 'EHFCOR'}],
            valtype='float',
            unitdict=self.unitDict,
            unit=self.akmaDict['energy'],
            lookupdict=self.mddataDict
            ),
        'x_charmm_frame_sequence_virial_kinetic_energy_frames' : MetaInfoMap(startpage,
            activeSections=['section_frame_sequence'],
            depends=[{'store' : 'STEP'}],
            valtype='int',
            lookupdict=self.mddataDict
            ),
        'x_charmm_frame_sequence_virial_kinetic_energy' : MetaInfoMap(startpage,
            activeSections=['section_frame_sequence'],
            depends=[{'store' : 'VIRKE'}],
            valtype='float',
            unitdict=self.unitDict,
            unit=self.akmaDict['energy'],
            lookupdict=self.mddataDict
            ),
        #'x_charmm_frame_sequence_boundary_frames' : MetaInfoMap(startpage,
        #    activeSections=['section_frame_sequence'],
        #    depends=[{'store' : 'STEP'}],
        #    valtype='int',
        #    lookupdict=self.mddataDict
        #    ),
        #'x_charmm_frame_sequence_boundary' : MetaInfoMap(startpage,
        #    activeSections=['section_frame_sequence'],
        #    depends=[{'store' : 'BOUNDARY'}],
        #    valtype='float',
        #    unitdict=self.unitDict,
        #    unit='kilo-joule/mol',
        #    lookupdict=self.mddataDict
        #    ),
        'x_charmm_frame_sequence_bond_energy_frames' : MetaInfoMap(startpage,
            activeSections=['section_frame_sequence'],
            depends=[{'store' : 'STEP'}],
            valtype='int',
            lookupdict=self.mddataDict
            ),
        'x_charmm_frame_sequence_bond_energy' : MetaInfoMap(startpage,
            activeSections=['section_frame_sequence'],
            depends=[{'store' : 'BONDS'}],
            valtype='float',
            unitdict=self.unitDict,
            unit=self.akmaDict['energy'],
            lookupdict=self.mddataDict
            ),
        'x_charmm_frame_sequence_angle_energy_frames' : MetaInfoMap(startpage,
            activeSections=['section_frame_sequence'],
            depends=[{'store' : 'STEP'}],
            valtype='int',
            lookupdict=self.mddataDict
            ),
        'x_charmm_frame_sequence_angle_energy' : MetaInfoMap(startpage,
            activeSections=['section_frame_sequence'],
            depends=[{'store' : 'ANGLES'}],
            valtype='float',
            unitdict=self.unitDict,
            unit=self.akmaDict['energy'],
            lookupdict=self.mddataDict
            ),
        'x_charmm_frame_sequence_proper_dihedral_energy_frames' : MetaInfoMap(startpage,
            activeSections=['section_frame_sequence'],
            depends=[{'store' : 'STEP'}],
            valtype='int',
            lookupdict=self.mddataDict
            ),
        'x_charmm_frame_sequence_proper_dihedral_energy' : MetaInfoMap(startpage,
            activeSections=['section_frame_sequence'],
            depends=[{'store' : 'DIHEDRALS'}],
            valtype='float',
            unitdict=self.unitDict,
            unit=self.akmaDict['energy'],
            lookupdict=self.mddataDict
            ),
        'x_charmm_frame_sequence_improper_dihedral_energy_frames' : MetaInfoMap(startpage,
            activeSections=['section_frame_sequence'],
            depends=[{'store' : 'STEP'}],
            valtype='int',
            lookupdict=self.mddataDict
            ),
        'x_charmm_frame_sequence_improper_dihedral_energy' : MetaInfoMap(startpage,
            activeSections=['section_frame_sequence'],
            depends=[{'store' : 'IMPROPERS'}],
            valtype='float',
            unitdict=self.unitDict,
            unit=self.akmaDict['energy'],
            lookupdict=self.mddataDict
            ),
        'x_charmm_frame_sequence_cmap_dihedral_energy_frames' : MetaInfoMap(startpage,
            activeSections=['section_frame_sequence'],
            depends=[{'store' : 'STEP'}],
            valtype='int',
            lookupdict=self.mddataDict
            ),
        'x_charmm_frame_sequence_cmap_dihedral_energy' : MetaInfoMap(startpage,
            activeSections=['section_frame_sequence'],
            depends=[{'store' : 'CMAP'}],
            valtype='float',
            unitdict=self.unitDict,
            unit=self.akmaDict['energy'],
            lookupdict=self.mddataDict
            ),
        'x_charmm_frame_sequence_vdw_energy_frames' : MetaInfoMap(startpage,
            activeSections=['section_frame_sequence'],
            depends=[{'store' : 'STEP'}],
            valtype='int',
            lookupdict=self.mddataDict
            ),
        'x_charmm_frame_sequence_vdw_energy' : MetaInfoMap(startpage,
            activeSections=['section_frame_sequence'],
            depends=[{'store' : 'VDWAALS'}],
            valtype='float',
            unitdict=self.unitDict,
            unit=self.akmaDict['energy'],
            lookupdict=self.mddataDict
            ),
        'x_charmm_frame_sequence_electrostatic_energy_frames' : MetaInfoMap(startpage,
            activeSections=['section_frame_sequence'],
            depends=[{'store' : 'STEP'}],
            valtype='int',
            lookupdict=self.mddataDict
            ),
        'x_charmm_frame_sequence_electrostatic_energy' : MetaInfoMap(startpage,
            activeSections=['section_frame_sequence'],
            depends=[{'store' : 'ELEC'}],
            valtype='float',
            unitdict=self.unitDict,
            unit=self.akmaDict['energy'],
            lookupdict=self.mddataDict
            ),
        'x_charmm_frame_sequence_urey_energy_frames' : MetaInfoMap(startpage,
            activeSections=['section_frame_sequence'],
            depends=[{'store' : 'STEP'}],
            valtype='int',
            lookupdict=self.mddataDict
            ),
        'x_charmm_frame_sequence_urey_energy' : MetaInfoMap(startpage,
            activeSections=['section_frame_sequence'],
            depends=[{'store' : 'UREY-B'}],
            valtype='float',
            unitdict=self.unitDict,
            unit=self.akmaDict['energy'],
            lookupdict=self.mddataDict
            ),
        #'frame_sequence_to_sampling_method_ref' : MetaInfoMap(startpage),
        'geometry_optimization_converged' : MetaInfoMap(startpage,
            depends=[
                {'test' : [["MINI", " is not None"],
                           ['Minimization exiting with', ' is not None']],
                 'assign' : True},
                ],
            activeInfo=True,
            lookupdict=self.cntrlDict
            ),
        #'previous_sequence_ref' : MetaInfoMap(startpage)
        }

    frameseqend = {
        #'number_of_conserved_quantity_evaluations_in_sequence' : MetaInfoMap(startpage,
        #    activeInfo=True,
        #    value=(lambda x: np.array(x['val']).flatten().shape[0] if(
        #        x is not None and x['val'] is not None) else None)(
        #        self.metaStorage.fetchAttrValue(
        #            'xxx_to_rm_frame_sequence_conserved_quantity_frames'
        #            )
        #        )
        #    ),
        'number_of_frames_in_sequence' : MetaInfoMap(startpage, activeInfo=True,
            value=(lambda x: np.array(x['val']).flatten().shape[0] if(
                x is not None and x['val'] is not None) else None)(
                self.metaStorage.fetchAttrValue(
                    'xxx_to_rm_frame_sequence_potential_energy_frames'
                    )
                )
            ),
        'number_of_kinetic_energies_in_sequence' : MetaInfoMap(startpage, activeInfo=True,
            value=(lambda x: np.array(x['val']).flatten().shape[0] if(
                x is not None and x['val'] is not None) else None)(
                self.metaStorage.fetchAttrValue(
                    'xxx_to_rm_frame_sequence_kinetic_energy_frames'
                    )
                )
            ),
        'number_of_potential_energies_in_sequence' : MetaInfoMap(startpage,
            activeInfo=True,
            value=(lambda x: np.array(x['val']).flatten().shape[0] if(
                x is not None and x['val'] is not None) else None)(
                self.metaStorage.fetchAttrValue(
                    'xxx_to_rm_frame_sequence_potential_energy_frames'
                    )
                )
            ),
        'number_of_pressure_evaluations_in_sequence' : MetaInfoMap(startpage,
            activeInfo=True,
            value=(lambda x: np.array(x['val']).flatten().shape[0] if(
                x is not None and x['val'] is not None) else None)(
                self.metaStorage.fetchAttrValue(
                    'xxx_to_rm_frame_sequence_pressure_frames'
                    )
                )
            ),
        'number_of_temperatures_in_sequence' : MetaInfoMap(startpage,
            activeInfo=True,
            value=(lambda x: np.array(x['val']).flatten().shape[0] if(
                x is not None and x['val'] is not None) else None)(
                self.metaStorage.fetchAttrValue(
                    'xxx_to_rm_frame_sequence_temperature_frames'
                    )
                )
            ),
        'x_charmm_number_of_volumes_in_sequence' : MetaInfoMap(startpage,
            activeInfo=True,
            activeSections=['section_frame_sequence'],
            value=(lambda x: np.array(x['val']).flatten().shape[0] if(
                x is not None and x['val'] is not None) else None)(
                self.metaStorage.fetchAttrValue(
                    'x_charmm_frame_sequence_volume_frames'
                    )
                )
            ),
        'x_charmm_number_of_boundary_energies_in_sequence' : MetaInfoMap(startpage,
            activeInfo=True,
            activeSections=['section_frame_sequence'],
            value=(lambda x: np.array(x['val']).flatten().shape[0] if(
                x is not None and x['val'] is not None) else None)(
                self.metaStorage.fetchAttrValue(
                    'x_charmm_frame_sequence_boundary_frames'
                    )
                )
            ),
        'x_charmm_number_of_bond_energies_in_sequence' : MetaInfoMap(startpage,
            activeInfo=True,
            activeSections=['section_frame_sequence'],
            value=(lambda x: np.array(x['val']).flatten().shape[0] if(
                x is not None and x['val'] is not None) else None)(
                self.metaStorage.fetchAttrValue(
                    'x_charmm_frame_sequence_bond_energy_frames'
                    )
                )
            ),
        'x_charmm_number_of_angle_energies_in_sequence' : MetaInfoMap(startpage,
            activeInfo=True,
            activeSections=['section_frame_sequence'],
            value=(lambda x: np.array(x['val']).flatten().shape[0] if(
                x is not None and x['val'] is not None) else None)(
                self.metaStorage.fetchAttrValue(
                    'x_charmm_frame_sequence_angle_energy_frames'
                    )
                )
            ),
        'x_charmm_number_of_electrostatic_energies_in_sequence' : MetaInfoMap(startpage,
            activeInfo=True,
            activeSections=['section_frame_sequence'],
            value=(lambda x: np.array(x['val']).flatten().shape[0] if(
                x is not None and x['val'] is not None) else None)(
                self.metaStorage.fetchAttrValue(
                    'x_charmm_frame_sequence_electrostatic_energy_frames'
                    )
                )
            ),
        'x_charmm_number_of_vdw_energies_in_sequence' : MetaInfoMap(startpage,
            activeInfo=True,
            activeSections=['section_frame_sequence'],
            value=(lambda x: np.array(x['val']).flatten().shape[0] if(
                x is not None and x['val'] is not None) else None)(
                self.metaStorage.fetchAttrValue(
                    'x_charmm_frame_sequence_vdw_energy_frames'
                    )
                )
            ),
        'x_charmm_number_of_total2_energies_in_sequence' : MetaInfoMap(startpage,
            activeInfo=True,
            activeSections=['section_frame_sequence'],
            value=(lambda x: np.array(x['val']).flatten().shape[0] if(
                x is not None and x['val'] is not None) else None)(
                self.metaStorage.fetchAttrValue(
                    'x_charmm_frame_sequence_total2_energy_frames'
                    )
                )
            ),
        'x_charmm_number_of_total3_energies_in_sequence' : MetaInfoMap(startpage,
            activeInfo=True,
            activeSections=['section_frame_sequence'],
            value=(lambda x: np.array(x['val']).flatten().shape[0] if(
                x is not None and x['val'] is not None) else None)(
                self.metaStorage.fetchAttrValue(
                    'x_charmm_frame_sequence_total3_energy_frames'
                    )
                )
            ),
        'x_charmm_number_of_proper_dihedral_energies_in_sequence' : MetaInfoMap(startpage,
            activeInfo=True,
            activeSections=['section_frame_sequence'],
            value=(lambda x: np.array(x['val']).flatten().shape[0] if(
                x is not None and x['val'] is not None) else None)(
                self.metaStorage.fetchAttrValue(
                    'x_charmm_frame_sequence_proper_dihedral_energy_frames'
                    )
                )
            ),
        'x_charmm_number_of_improper_dihedral_energies_in_sequence' : MetaInfoMap(startpage,
            activeInfo=True,
            activeSections=['section_frame_sequence'],
            value=(lambda x: np.array(x['val']).flatten().shape[0] if(
                x is not None and x['val'] is not None) else None)(
                self.metaStorage.fetchAttrValue(
                    'x_charmm_frame_sequence_improper_dihedral_energy_frames'
                    )
                )
            ),
        'x_charmm_number_of_cmap_dihedral_energies_in_sequence' : MetaInfoMap(startpage,
            activeInfo=True,
            activeSections=['section_frame_sequence'],
            value=(lambda x: np.array(x['val']).flatten().shape[0] if(
                x is not None and x['val'] is not None) else None)(
                self.metaStorage.fetchAttrValue(
                    'x_charmm_frame_sequence_cmap_dihedral_energy_frames'
                    )
                )
            ),
        'x_charmm_number_of_misc_energies_in_sequence' : MetaInfoMap(startpage,
            activeInfo=True,
            activeSections=['section_frame_sequence'],
            value=(lambda x: np.array(x['val']).flatten().shape[0] if(
                x is not None and x['val'] is not None) else None)(
                self.metaStorage.fetchAttrValue(
                    'x_charmm_frame_sequence_misc_energy_frames'
                    )
                )
            ),
        #'previous_sequence_ref' : MetaInfoMap(startpage)
        }

    # ----------------------------------
    #   Definitions for section_system
    # ----------------------------------
    # section_system
    sec_system = {
        #'topology_ref' : MetaInfoMap(startpage),
        'atom_velocities' : MetaInfoMap(startpage),
        'configuration_raw_gid' : MetaInfoMap(startpage),
        'local_rotations' : MetaInfoMap(startpage),
        'number_of_atoms' : MetaInfoMap(startpage,
            depends=[{'value' : 'number_of_atoms'}],
            valtype='int',
            lookupdict=self.extraDict
            ),
        'number_of_sites' : MetaInfoMap(startpage),
        'number_of_symmetry_operations' : MetaInfoMap(startpage),
        'reduced_symmetry_matrices' : MetaInfoMap(startpage),
        'reduced_symmetry_translations' : MetaInfoMap(startpage),
        'sc_matrix' : MetaInfoMap(startpage),
        'spacegroup_3D_choice' : MetaInfoMap(startpage),
        'spacegroup_3D_hall' : MetaInfoMap(startpage),
        'spacegroup_3D_international' : MetaInfoMap(startpage),
        'spacegroup_3D_number' : MetaInfoMap(startpage),
        'spacegroup_3D_origin_shift' : MetaInfoMap(startpage),
        'spacegroup_3D_pointgroup' : MetaInfoMap(startpage),
        'spacegroup_3D_std_lattice' : MetaInfoMap(startpage),
        'spacegroup_3D_std_positions' : MetaInfoMap(startpage),
        'spacegroup_3D_std_types' : MetaInfoMap(startpage),
        'spacegroup_3D_trasformation_matrix' : MetaInfoMap(startpage),
        'spacegroup_3D_wyckoff' : MetaInfoMap(startpage),
        'symmorphic' : MetaInfoMap(startpage),
        'system_name' : MetaInfoMap(startpage,
            activeInfo=True,
            activeSections=['section_system'],
            subfunction={
                'function' : MDData.MDDataConverter.topology_system_name,
                'supportDict' : self.topoDict,
                },
            #functionbase=self
            ),
        'time_reversal_symmetry' : MetaInfoMap(startpage)
        }

    # section_configuration_core of section_system
    configuration_core = {
        'number_of_electrons' : MetaInfoMap(startpage,
            #value=0,
            #valtype='float',
            ),
        'atom_labels' : MetaInfoMap(startpage,
            #subfunction=self.system_atom_labels()
            ),
        'atom_positions' : MetaInfoMap(startpage,
            #subfunction=self.system_atom_positions()
            ),
        'configuration_periodic_dimensions' : MetaInfoMap(startpage,
            ),
        'embedded_system' : MetaInfoMap(startpage),
        'lattice_vectors' : MetaInfoMap(startpage,
            #subfunction=self.system_lattice_vectors()
            ),
        'simulation_cell' : MetaInfoMap(startpage,
            #subfunction=self.system_simulation_cell()
            )
        }

    # section_spacegroup_3D_operation of section_system
    spacegroup_op = {
            'spacegroup_3D_rotation' : MetaInfoMap(startpage),
            'spacegroup_3D_translation' : MetaInfoMap(startpage)
        }

    # section_system_to_system_refs of section_system
    sys_to_sys = {
            'system_to_system_kind' : MetaInfoMap(startpage),
            'system_to_system_ref' : MetaInfoMap(startpage)
        }

    # --------------------------------------------------------
    #   Definitions of meta data values for section_topology
    # --------------------------------------------------------
    # section_topology of section_run
    topology = {
        'atom_to_molecule' : MetaInfoMap(startpage,
            subfunction={
                'function' : MDData.MDDataConverter.topology_atom_to_mol,
                'supportDict' : self.topoDict,
                },
            #functionbase=self
            ),
        'molecule_to_molecule_type_map' : MetaInfoMap(startpage),
        'number_of_topology_atoms' : MetaInfoMap(startpage,
            depends=[{'value' : 'number_of_atoms'}],
            valtype='int',
            lookupdict=self.extraDict
            ),
        'number_of_topology_molecules' : MetaInfoMap(startpage,
            subfunction={
                'function' : MDData.MDDataConverter.topology_num_topo_mol,
                'supportDict' : self.topoDict,
                },
            valtype='int',
            ),
        'topology_force_field_name' : MetaInfoMap(startpage,
            depends=[{'value' : 'PARAMETER file'}],
            lookupdict=self.cntrlDict
            )
        }

    # section_atom_type of section_topology
    atom_type = {
        'atom_type_charge' : MetaInfoMap(startpage),
        'atom_type_mass' : MetaInfoMap(startpage),
        'atom_type_name' : MetaInfoMap(startpage)
        }

    # section_constraint of section_topology
    constraint = {
        'constraint_atoms' : MetaInfoMap(startpage),
        'constraint_kind' : MetaInfoMap(startpage),
        'constraint_parameters' : MetaInfoMap(startpage),
        'number_of_atoms_per_constraint' : MetaInfoMap(startpage),
        'number_of_constraints' : MetaInfoMap(startpage)
        }

    # section_interaction of section_topology
    interaction = {
        'interaction_atoms' : MetaInfoMap(startpage),
        'interaction_kind' : MetaInfoMap(startpage),
        'interaction_parameters' : MetaInfoMap(startpage),
        'number_of_atoms_per_interaction' : MetaInfoMap(startpage),
        'number_of_interactions' : MetaInfoMap(startpage)
        }

    # -------------------------------------------------------------
    #   Definitions of meta data values for section_molecule_type
    # -------------------------------------------------------------
    # section_molecule_type of section_topology
    mol_type = {
        'molecule_type_name' : MetaInfoMap(startpage),
        'number_of_atoms_in_molecule' : MetaInfoMap(startpage),
        'settings_atom_in_molecule' : MetaInfoMap(startpage)
        }

    # section_molecule_constraint of section_molecule_type
    mol_constraint = {
        'molecule_constraint_atoms' : MetaInfoMap(startpage),
        'molecule_constraint_kind' : MetaInfoMap(startpage),
        'molecule_constraint_parameters' : MetaInfoMap(startpage),
        'number_of_atoms_per_molecule_constraint' : MetaInfoMap(startpage),
        'number_of_molecule_constraints' : MetaInfoMap(startpage)
        }

    # section_molecule_interaction of section_molecule_type
    mol_interaction = {
        'molecule_interaction_atoms' : MetaInfoMap(startpage),
        'molecule_interaction_kind' : MetaInfoMap(startpage),
        'molecule_interaction_parameters' : MetaInfoMap(startpage),
        'number_of_atoms_per_molecule_interaction' : MetaInfoMap(startpage),
        'number_of_molecule_interactions' : MetaInfoMap(startpage)
        }

    # section_atom_in_molecule of section_molecule_type
    atom_in_mol = {
        'atom_in_molecule_charge' : MetaInfoMap(startpage),
        'atom_in_molecule_name' : MetaInfoMap(startpage),
        'atom_in_molecule_to_atom_type_ref' : MetaInfoMap(startpage)
        }


    if defname == 'system':
        dictionary = systemDict
    elif defname == 'topology':
        dictionary = topology
    elif defname == 'singleconfcalc':
        dictionary = singleconfcalc
    elif defname == 'restrictions':
        dictionary = restrictions
    elif defname == 'frameseq':
        dictionary = frameseq
    elif defname == 'frameseqend':
        dictionary = frameseqend
    elif defname == 'atom_type':
        dictionary = atom_type
    elif defname == 'molecule_type':
        dictionary = moltypeDict
    elif defname == 'interaction':
        dictionary = interaction
    elif defname == 'sampling':
        dictionary = sampling
    elif defname == 'singlevdw':
        dictionary = singlevdw
    elif defname == 'confcore':
        dictionary = configuration_core
    else:
        dictionary = singleconfcalclist
    return MapDictionary(dictionary)


