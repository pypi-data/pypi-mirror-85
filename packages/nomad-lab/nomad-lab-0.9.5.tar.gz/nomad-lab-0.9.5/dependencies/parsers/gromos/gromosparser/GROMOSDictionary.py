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
from .GROMOSCommon import PARSERNAME, PROGRAMNAME, PARSERTAG
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
        'fileInterface'   : ["gromosread", "parmed", "mdtraj", "mdanalysis"]
        }
    namelist = {
        'structure'     : FileInfoMap(startpage, fileFormat=['.gromostop', '.top'], activeInfo=False,
                                      infoPurpose=['topology']),
        'input_coord'   : FileInfoMap(startpage, fileFormat=['.gromoscnf', '.cnf', '.g96'], activeInfo=False,
                                      infoPurpose=['topology', 'inputcoordinates', 'inputvelocities']),
        'output_coord'  : FileInfoMap(startpage, fileFormat=['.gromoscnf', '.cnf', '.g96'], activeInfo=False,
                                      infoPurpose=['outputcoordinates', 'outputvelocities']),
        'trajectory'    : FileInfoMap(startpage, fileFormat=['.gromostrc', '.trc'], activeInfo=False,
                                      infoPurpose=['trajectory', 'unitcell']),
        'traj_vel'      : FileInfoMap(startpage, fileFormat=['.gromostrv', '.trv'], activeInfo=False,
                                      infoPurpose=['velocities']),
        'traj_force'    : FileInfoMap(startpage, fileFormat=['.gromostrf', '.trf'], activeInfo=False,
                                      infoPurpose=['forces']),
        'output_log'    : FileInfoMap(startpage),
        'control_input' : FileInfoMap(startpage),
        }
    return MapDictionary(namelist)

def get_nameListDict(deflist):
    """Loads control in data of GROMOS.

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

    topocntrllist = {
        'MAKE_TOP' : MetaInfoMap(startpage, defaultValue=None, matchWith='EOL',
            replaceTag='topology_parameter_files', subFunc=lambda x:
            ', '.join(' '.join(x.strip().split()).replace(
                'topology,', '').replace(
                    'using:', '').replace('Force-field code:', ''
                        ).strip().split()[:-1]) if x is not None else None),
        'Force-field code' : MetaInfoMap(startpage, defaultValue=None,
                            subFunc=lambda x: 'Gromos-'+x if x is not None else None),
        'topology type' : MetaInfoMap(startpage, defaultValue=None,
                                      activeInfo=False, matchWith='PW'),
        'using atomistic' : MetaInfoMap(startpage, defaultValue=None,
                            replaceTag='topology_parameters', subFunc=lambda x:
                            'Atomistic' if x is not None else None),
        'using coarse-grained' : MetaInfoMap(startpage, defaultValue=None,
                                 replaceTag='topology_parameters', subFunc=lambda x:
                                 'Coarse-Grained' if x is not None else None),
        'RESNAME' : MetaInfoMap(startpage, defaultValue=None, matchWith='EOL',
            subFunc=lambda x: ', '.join(' '.join(x.strip().split()
                ).replace('END', '').replace(
                    'RESNAME', '').strip().split()
                ) if x is not None else None),
        'atom types' : MetaInfoMap(startpage, defaultValue=None, matchWith='PW',
            replaceTag='number_of_atom_types', matchAlso="ATOMTYPENAME",
            subFunc=lambda x: ' '.join(x.strip().split()
                ).replace('END', '').replace('ATOMTYPENAME', ''
                    ) if x is not None else None),
        'number of atoms' : MetaInfoMap(startpage, defaultValue=None, replaceTag='number of atoms solute',
            matchAlso="SOLUTEATOM", subFunc=lambda x: ' '.join(x.strip().split()
                ).replace('END', '').replace('SOLUTEATOM', ''
                    ) if x is not None else None),
        'Lennard-Jones exceptions' : MetaInfoMap(startpage, defaultValue=None, matchWith='PW',
            matchAlso="LJEXCEPTIONS", subFunc=lambda x: ' '.join(x.strip().split()
                ).replace('END', '').replace('LJEXCEPTIONS', ''
                    ) if x is not None else None),
        'bonds from BONDH block added to CONSTRAINT' : MetaInfoMap(startpage,
            defaultValue=None, matchWith='PW', replaceTag='number of H bonds at CONSTRAINT',
            matchAlso="END", subFunc=lambda x: ' '.join(x.strip().split()
                ).replace('END', '') if x is not None else None),
        'bonds from BOND block added to CONSTRAINT' : MetaInfoMap(startpage,
            defaultValue=None, matchWith='PW',
            replaceTag='number of bonds at CONSTRAINT', matchAlso="END"),
        'bondangles containing hydrogens' : MetaInfoMap(startpage,
            defaultValue=None, matchAlso="BONDANGLE"),
        'bondangles not containing hydrogens' : MetaInfoMap(startpage,
            defaultValue=None, matchAlso="BONDANGLE"),
        'improper dihedrals not containing hydrogens' : MetaInfoMap(startpage,
            defaultValue=None, matchAlso="IMPDIHEDRAL"),
        'improper dihedrals containing hydrogens' : MetaInfoMap(startpage,
            defaultValue=None, matchAlso="IMPDIHEDRAL"),
        'propdihedrals not containing hydrogens' : MetaInfoMap(startpage,
            defaultValue=None, matchAlso="DIHEDRAL",
            replaceTag='dihedrals not containing hydrogens'),
        'propdihedrals containing hydrogens' : MetaInfoMap(startpage,
            defaultValue=None, matchAlso="DIHEDRAL",
            replaceTag='dihedrals containing hydrogens'),
        'crossdihedrals not containing hydrogens' : MetaInfoMap(startpage,
            defaultValue=None, matchAlso="CROSSDIHEDRAL"),
        'crossdihedrals containing hydrogens' : MetaInfoMap(startpage,
            defaultValue=None, matchAlso="CROSSDIHEDRAL"),
        'atoms' : MetaInfoMap(startpage, defaultValue=None, matchAlso="SOLVENT",
                replaceTag='number of solvent atoms'),
        'constraints' : MetaInfoMap(startpage, defaultValue=None, matchAlso="SOLVENT",
                replaceTag='number of solvent constraints'),
        'adding' : MetaInfoMap(startpage, defaultValue=None, matchAlso="SOLVENT",
                replaceTag='number of solvents added'),
        'molecules' : MetaInfoMap(startpage, defaultValue=None, matchAlso="SOLUTE",
                replaceTag='number of molecules in solute'),
        'temperature groups' : MetaInfoMap(startpage, defaultValue=None, matchAlso="SOLUTE",
                replaceTag='number of temperature groups for solute'),
        'pressure groups' : MetaInfoMap(startpage, defaultValue=None, matchAlso="SOLUTE",
                replaceTag='number of pressure groups for solute'),
        #''           : MetaInfoMap(startpage, defaultValue=None),
        }

    ffcntrllist = {
        'bond angle \(cosine\) interaction' : MetaInfoMap(startpage, defaultValue=None,
            matchAlso="FORCEFIELD", replaceTag='bond angle interaction in force field',
            subFunc=lambda x: 'Yes' if x is not None else None),
        'improper-dihedral-interaction' : MetaInfoMap(startpage, defaultValue=None,
            matchAlso="FORCEFIELD", replaceTag='improper dihedral interaction in force field',
            subFunc=lambda x: 'Yes' if x is not None else None),
        'propdihedral_interaction' : MetaInfoMap(startpage, defaultValue=None,
            matchAlso="FORCEFIELD", replaceTag='dihedral interaction in force field',
            subFunc=lambda x: 'Yes' if x is not None else None),
        'crossdihedral interaction' : MetaInfoMap(startpage, defaultValue=None,
            matchAlso="FORCEFIELD", replaceTag='cross dihedral interaction in force field',
            subFunc=lambda x: 'Yes' if x is not None else None),
        'nonbonded force' : MetaInfoMap(startpage, defaultValue=None, matchWith='EOL',
            matchAlso="FORCEFIELD", replaceTag='nonbonded definitions in force field',
            subFunc=lambda x: ', '.join(x.strip().split()) if x is not None else None),
        'Pairlist Algorithm'  : MetaInfoMap(startpage, defaultValue=None, matchWith='EOL',
            subFunc=lambda x: ' '.join(x.strip().split()) if x is not None else None),
        'boundary'  : MetaInfoMap(startpage, defaultValue=None, matchWith='EOL',
            replaceTag='periodic boundary conditions',
            subFunc=lambda x: ' '.join(x.strip().split()) if x is not None else None),
        'virial'  : MetaInfoMap(startpage, defaultValue=None, matchWith='EOL',
            subFunc=lambda x: ' '.join(x.strip().split()) if x is not None else None),
        'cutoff '  : MetaInfoMap(startpage, defaultValue=None, matchAlso='pairlist creation',
                                  replaceTag='cutoff type'),
        'shortrange-cutoff-'  : MetaInfoMap(startpage, defaultValue=None,
                                      replaceTag='shortrange cutoff'),
        'longrange-cutoff-'  : MetaInfoMap(startpage, defaultValue=None,
                                      replaceTag='longrange cutoff'),
        'pairlist creation every'  : MetaInfoMap(startpage, defaultValue=None,
                                      replaceTag='pairlist update step frequency'),
        'reactionfield cutoff '  : MetaInfoMap(startpage, defaultValue=None,
            replaceTag='reactionfield cutoff'),
        'epsilon '  : MetaInfoMap(startpage, defaultValue=None,
            replaceTag='force field epsilon'),
        'reactionfield-epsilon-'  : MetaInfoMap(startpage, defaultValue=None,
            replaceTag='reactionfield epsilon'),
        'kappa'  : MetaInfoMap(startpage, defaultValue=None,
            replaceTag='force field kappa'),
        'perturbation'  : MetaInfoMap(startpage, defaultValue=None,
            replaceTag='force field perturbation'),
        }

    filecntrllist = {
        'parameter read from'  : MetaInfoMap(startpage, defaultValue=None,
                                             replaceTag='input file'),
        'topology read from'  : MetaInfoMap(startpage, defaultValue=None,
                                             replaceTag='topology file'),
        'configuration read from'  : MetaInfoMap(startpage, defaultValue=None,
                                             replaceTag='configuration file'),
        }

    cntrllist = {
        'TITLE'  : MetaInfoMap(startpage, defaultValue=None),
        'EMIN-NTEM'  : MetaInfoMap(startpage, defaultValue=None),
        'EMIN-NCYC'  : MetaInfoMap(startpage, defaultValue=None),
        'EMIN-DELE'  : MetaInfoMap(startpage, defaultValue=None),
        'EMIN-DX0'  : MetaInfoMap(startpage, defaultValue=None),
        'EMIN-DXM'  : MetaInfoMap(startpage, defaultValue=None),
        'EMIN-NMIN'  : MetaInfoMap(startpage, defaultValue=None),
        'EMIN-FLIM'  : MetaInfoMap(startpage, defaultValue=None),
        'SYS-NPM'  : MetaInfoMap(startpage, defaultValue=None),
        'SYS-NSM'  : MetaInfoMap(startpage, defaultValue=None),
        'INIT-NTIVEL'  : MetaInfoMap(startpage, defaultValue=None),
        'INIT-NTISHK'  : MetaInfoMap(startpage, defaultValue=None),
        'INIT-NTINHT'  : MetaInfoMap(startpage, defaultValue=None),
        'INIT-NTINHB'  : MetaInfoMap(startpage, defaultValue=None),
        'INIT-NTISHI'  : MetaInfoMap(startpage, defaultValue=None),
        'INIT-NTIRTC'  : MetaInfoMap(startpage, defaultValue=None),
        'INIT-NTICOM'  : MetaInfoMap(startpage, defaultValue=None),
        'INIT-NTISTI'  : MetaInfoMap(startpage, defaultValue=None),
        'INIT-IG'  : MetaInfoMap(startpage, defaultValue=None),
        'INIT-TEMPI'  : MetaInfoMap(startpage, defaultValue=None),
        'STEP-NSTLIM'  : MetaInfoMap(startpage, defaultValue=None),
        'STEP-T'  : MetaInfoMap(startpage, defaultValue=None),
        'STEP-DT'  : MetaInfoMap(startpage, defaultValue=None),
        'BCND-NTB'  : MetaInfoMap(startpage, defaultValue=None),
        'BCND-NDFMIN'  : MetaInfoMap(startpage, defaultValue=None),
        'BATH-ALG'  : MetaInfoMap(startpage, defaultValue=None),
        'BATH-NUM'  : MetaInfoMap(startpage, defaultValue=None),
        'BATH-NBATHS'  : MetaInfoMap(startpage, defaultValue=None),
        'BATH-TEMP'  : MetaInfoMap(startpage, defaultValue=None),
        'BATH-TAU'  : MetaInfoMap(startpage, defaultValue=None),
        'BATH-DOFSET'  : MetaInfoMap(startpage, defaultValue=None),
        'BATH-LAST'  : MetaInfoMap(startpage, defaultValue=None),
        'BATH-COMBATH'  : MetaInfoMap(startpage, defaultValue=None),
        'BATH-IRBATH'  : MetaInfoMap(startpage, defaultValue=None),
        'PRES-COUPLE'  : MetaInfoMap(startpage, defaultValue=None),
        'PRES-SCALE'  : MetaInfoMap(startpage, defaultValue=None),
        'PRES-COMP'  : MetaInfoMap(startpage, defaultValue=None),
        'PRES-TAUP'  : MetaInfoMap(startpage, defaultValue=None),
        'PRES-VIRIAL'  : MetaInfoMap(startpage, defaultValue=None),
        'PRES-ANISO'  : MetaInfoMap(startpage, defaultValue=None),
        'PRES-INIT0'  : MetaInfoMap(startpage, defaultValue=None),
        'COVF-NTBBH'  : MetaInfoMap(startpage, defaultValue=None),
        'COVF-NTBAH'  : MetaInfoMap(startpage, defaultValue=None),
        'COVF-NTBDN'  : MetaInfoMap(startpage, defaultValue=None),
        'SOLM-NSPM'  : MetaInfoMap(startpage, defaultValue=None),
        'SOLM-NSP'  : MetaInfoMap(startpage, defaultValue=None),
        'COMT-NSCM'  : MetaInfoMap(startpage, defaultValue=None),
        'PRNT-NTPR'  : MetaInfoMap(startpage, defaultValue=None),
        'PRNT-NTPP'  : MetaInfoMap(startpage, defaultValue=None),
        'WRIT-NTWX'  : MetaInfoMap(startpage, defaultValue=None),
        'WRIT-NTWSE'  : MetaInfoMap(startpage, defaultValue=None),
        'WRIT-NTWV'  : MetaInfoMap(startpage, defaultValue=None),
        'WRIT-NTWF'  : MetaInfoMap(startpage, defaultValue=None),
        'WRIT-NTWE'  : MetaInfoMap(startpage, defaultValue=None),
        'WRIT-NTWG'  : MetaInfoMap(startpage, defaultValue=None),
        'WRIT-NTWB'  : MetaInfoMap(startpage, defaultValue=None),
        'CNST-NTC'  : MetaInfoMap(startpage, defaultValue=None),
        'CNST-NTCP'  : MetaInfoMap(startpage, defaultValue=None),
        'CNST-NTCP0'  : MetaInfoMap(startpage, defaultValue=None),
        'CNST-NTCS'  : MetaInfoMap(startpage, defaultValue=None),
        'CNST-NTCS0'  : MetaInfoMap(startpage, defaultValue=None),
        'FORC-BONDS'  : MetaInfoMap(startpage, defaultValue=None),
        'FORC-ANGS'  : MetaInfoMap(startpage, defaultValue=None),
        'FORC-IMPS'  : MetaInfoMap(startpage, defaultValue=None),
        'FORC-DIHS'  : MetaInfoMap(startpage, defaultValue=None),
        'FORC-ELEC'  : MetaInfoMap(startpage, defaultValue=None),
        'FORC-VDW'  : MetaInfoMap(startpage, defaultValue=None),
        'FORC-NEGR'  : MetaInfoMap(startpage, defaultValue=None),
        'FORC-NRE'  : MetaInfoMap(startpage, defaultValue=None),
        'PAIR-ALG'  : MetaInfoMap(startpage, defaultValue=None),
        'PAIR-NSNB'  : MetaInfoMap(startpage, defaultValue=None),
        'PAIR-RCUTP'  : MetaInfoMap(startpage, defaultValue=None),
        'PAIR-RCUTL'  : MetaInfoMap(startpage, defaultValue=None),
        'PAIR-SIZE'  : MetaInfoMap(startpage, defaultValue=None),
        'PAIR-TYPE'  : MetaInfoMap(startpage, defaultValue=None),
        'NONB-NLRELE'  : MetaInfoMap(startpage, defaultValue=None),
        'NONB-APPAK'  : MetaInfoMap(startpage, defaultValue=None),
        'NONB-RCRF'  : MetaInfoMap(startpage, defaultValue=None),
        'NONB-EPSRF'  : MetaInfoMap(startpage, defaultValue=None),
        'NONB-NSLFEXCL'  : MetaInfoMap(startpage, defaultValue=None),
        'NONB-NSHAPE'  : MetaInfoMap(startpage, defaultValue=None),
        'NONB-ASHAPE'  : MetaInfoMap(startpage, defaultValue=None),
        'NONB-NA2CLC'  : MetaInfoMap(startpage, defaultValue=None),
        'NONB-TOLA2'  : MetaInfoMap(startpage, defaultValue=None),
        'NONB-EPSLS'  : MetaInfoMap(startpage, defaultValue=None),
        'NONB-NKX'  : MetaInfoMap(startpage, defaultValue=None),
        'NONB-NKY'  : MetaInfoMap(startpage, defaultValue=None),
        'NONB-NKZ'  : MetaInfoMap(startpage, defaultValue=None),
        'NONB-KCUT'  : MetaInfoMap(startpage, defaultValue=None),
        'NONB-NGX'  : MetaInfoMap(startpage, defaultValue=None),
        'NONB-NGY'  : MetaInfoMap(startpage, defaultValue=None),
        'NONB-NGZ'  : MetaInfoMap(startpage, defaultValue=None),
        'NONB-NASORD'  : MetaInfoMap(startpage, defaultValue=None),
        'NONB-NFDORD'  : MetaInfoMap(startpage, defaultValue=None),
        'NONB-NALIAS'  : MetaInfoMap(startpage, defaultValue=None),
        'NONB-NSPORD'  : MetaInfoMap(startpage, defaultValue=None),
        'NONB-NQEVAL'  : MetaInfoMap(startpage, defaultValue=None),
        'NONB-FACCUR'  : MetaInfoMap(startpage, defaultValue=None),
        'NONB-NRDGRD'  : MetaInfoMap(startpage, defaultValue=None),
        'NONB-NWRGRD'  : MetaInfoMap(startpage, defaultValue=None),
        'NONB-NLRLJ'  : MetaInfoMap(startpage, defaultValue=None),
        'NONB-SLVDNS'  : MetaInfoMap(startpage, defaultValue=None),
        'Parameter' : MetaInfoMap(startpage, defaultValue=None, matchWith='EOL'),
        }

    startpage.update({
        'metaNameTag'     : 'mdout',
        'activeSections'  : ['section_single_configuration_calculation']
        })
    mddatalist = {
        'STEP'      : MetaInfoMap(startpage, matchWith='EOL',
            subFunc=lambda x: x.strip().split()[1] if len(x.strip().split())>1 is not None else None),
        'TIME'      : MetaInfoMap(startpage, matchWith='EOL',
            subFunc=lambda x: x.strip().split()[1] if len(x.strip().split())>1 is not None else None),
        'T_avg'   : MetaInfoMap(startpage, matchWith='EOL',
            subFunc=lambda x: x.strip().split()[4] if len(x.strip().split())>1 is not None else None),
        'E_Total'   : MetaInfoMap(startpage, matchAlso=":"),
        'E_Kinetic' : MetaInfoMap(startpage, matchAlso=":"),
        'E_Potential\+Special' : MetaInfoMap(startpage, matchAlso=":",
            replaceTag='E_Potential_Special'),
        'E_Potential' : MetaInfoMap(startpage, matchAlso=":"),
        'E_Covalent' : MetaInfoMap(startpage, matchAlso=":"),
        'E_Bonds'   : MetaInfoMap(startpage, matchAlso=":"),
        'E_Angles'  : MetaInfoMap(startpage, matchAlso=":"),
        'E_Improper' : MetaInfoMap(startpage, matchAlso=":"),
        'E_Dihedral' : MetaInfoMap(startpage, matchAlso=":"),
        'E_Crossdihedral' : MetaInfoMap(startpage, matchAlso=":"),
        'E_Non-bonded' : MetaInfoMap(startpage, matchAlso=":"),
        'E_Vdw'     : MetaInfoMap(startpage, matchAlso=":"),
        'E_El \(RF\)' : MetaInfoMap(startpage, matchAlso=":",
            replaceTag='E_El_RF'),
        'E_El \(LF\)' : MetaInfoMap(startpage, matchAlso=":",
            replaceTag='E_El_LF'),
        'E_El \(pair\)' : MetaInfoMap(startpage, matchAlso=":",
            replaceTag='E_El_pair'),
        'E_El \(real-space\)' : MetaInfoMap(startpage, matchAlso=":",
            replaceTag='E_El_real-space'),
        'E_El \(k-space\)' : MetaInfoMap(startpage, matchAlso=":",
            replaceTag='E_El_k-space'),
        'E_El \(A term\)' : MetaInfoMap(startpage, matchAlso=":",
            replaceTag='E_El_A term'),
        'E_El \(lattice sum self\)' : MetaInfoMap(startpage, matchAlso=":",
            replaceTag='E_El_lattice sum self'),
        'E_El \(surface term\)' : MetaInfoMap(startpage, matchAlso=":",
            replaceTag='E_El_surface term'),
        'E_Polarisation self' : MetaInfoMap(startpage, matchAlso=":"),
        'E_Special' : MetaInfoMap(startpage, matchAlso=":"),
        'E_SASA                 :' : MetaInfoMap(startpage,
            replaceTag='E_SASA'),
        'E_SASA Volume' : MetaInfoMap(startpage, matchAlso=":"),
        'E_Constraints' : MetaInfoMap(startpage, matchAlso=":"),
        'E_Distanceres' : MetaInfoMap(startpage, matchAlso=":"),
        'E_Disfieldres' : MetaInfoMap(startpage, matchAlso=":"),
        'E_Dihrest' : MetaInfoMap(startpage, matchAlso=":"),
        'E_Posrest' : MetaInfoMap(startpage, matchAlso=":"),
        'E_Jrest'   : MetaInfoMap(startpage, matchAlso=":"),
        'E_X-ray restraints' : MetaInfoMap(startpage, matchAlso=":"),
        'E_Local elevation' : MetaInfoMap(startpage, matchAlso=":"),
        'E_Order-parameter rest.' : MetaInfoMap(startpage, matchAlso=":",
            replaceTag='E_Order-parameter-rest'),
        'E_RDCrest' : MetaInfoMap(startpage, matchAlso=":"),
        'E_Symmetry restraints' : MetaInfoMap(startpage, matchAlso=":"),
        'E_EDS reference' : MetaInfoMap(startpage, matchAlso=":"),
        'E_Entropy' : MetaInfoMap(startpage, matchAlso=":"),
        'E_QM'      : MetaInfoMap(startpage, matchAlso=":"),
        'pressure'  : MetaInfoMap(startpage, matchAlso=":"),
        'volume'    : MetaInfoMap(startpage, matchAlso=":"),
        'virial'    : MetaInfoMap(startpage),
        #'molecular kinetic energy'    : MetaInfoMap(startpage),
        'pressure tensor'    : MetaInfoMap(startpage),
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
    elif deflist == 'topocntrl':
        namelist = topocntrllist
    elif deflist == 'ffcntrl':
        namelist = ffcntrllist
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
    self.fileDict = get_fileListDict()
    self.cntrlDict = get_nameListDict('cntrl')
    self.topocntrlDict = get_nameListDict('topocntrl')
    self.ffcntrlDict = get_nameListDict('ffcntrl')
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
            'topocntrl'  : self.topocntrlDict,
            'ffcntrl'  : self.ffcntrlDict,
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
#            'settings_Monte_Carlo' : MetaInfoMap(startpage),
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
        #'x_gromos_barostat_type' : MetaInfoMap(startpage,
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
        #'x_gromos_barostat_target_pressure' : MetaInfoMap(startpage,
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
        #'x_gromos_barostat_tau' : MetaInfoMap(startpage,
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
        #'x_gromos_integrator_type' : MetaInfoMap(startpage,
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
        'x_gromos_integrator_dt' : MetaInfoMap(startpage,
            depends=[
                {'test' : [['DYNA', ' is not None'],
                           ['TIME STEP', ' is not None']],
                 'value' : 'TIME STEP'},
                ],
            lookupdict=self.cntrlDict,
            valtype='float',
            unitdict=self.unitDict,
            unit='nano-seconds',
            #autoSections=True,
            activeInfo=True,
            activeSections=['settings_integrator']
            ),
        'x_gromos_number_of_steps_requested' : MetaInfoMap(startpage,
            depends=[{'value' : 'NSTEP'}],
            lookupdict=self.cntrlDict,
            valtype='int',
            #autoSections=True,
            activeInfo=True,
            activeSections=['settings_integrator']
            ),
        #'x_gromos_thermostat_type' : MetaInfoMap(startpage,
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
        'x_gromos_thermostat_target_temperature' : MetaInfoMap(startpage,
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
        #'x_gromos_thermostat_tau' : MetaInfoMap(startpage,
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
        'x_gromos_periodicity_type' : MetaInfoMap(startpage,
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
            depends=[{'value' : 'E_Non-bonded'}],
            valtype='float',
            unitdict=self.unitDict,
            unit='kilo-joule/mol',
            activeInfo=True,
            lookupdict=self.mddataDict
            ),
        'energy_free_per_atom' : MetaInfoMap(startpage),
        'energy_free' : MetaInfoMap(startpage),
        #'energy_method_current' : MetaInfoMap(startpage,
        #    depends=[{'assign' : 'Force Field'}],
        #    lookupdict=self.mddataDict
        #    ),
        'energy_T0_per_atom' : MetaInfoMap(startpage),
        'energy_total_T0_per_atom' : MetaInfoMap(startpage),
        'energy_total_T0' : MetaInfoMap(startpage,
            depends=[{'value' : 'E_Potential'}],
            valtype='float',
            unitdict=self.unitDict,
            unit='kilo-joule/mol',
            activeInfo=True,
            lookupdict=self.mddataDict
            ),
        'energy_total' : MetaInfoMap(startpage,
            depends=[{'value' : 'E_Total'}],
            valtype='float',
            unitdict=self.unitDict,
            unit='kilo-joule/mol',
            activeInfo=True,
            lookupdict=self.mddataDict
            ),
        'hessian_matrix' : MetaInfoMap(startpage),
        'single_configuration_calculation_converged' : MetaInfoMap(startpage),
        'single_configuration_calculation_to_system_ref' : MetaInfoMap(startpage),
        'single_configuration_to_calculation_method_ref' : MetaInfoMap(startpage),
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
        'energy_van_der_Waals_value' : MetaInfoMap(startpage,
            depends=[{'value' : 'E_Vdw'}],
            lookupdict=self.mddataDict,
            valtype='float',
            unitdict=self.unitDict,
            unit='kilo-joule/mol',
            #autoSections=True,
            activeSections=['section_energy_van_der_Waals']
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
            value='GROMOS License',
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
            value='GROMOS',
            #autoSections=True,
            activeInfo=True,
            activeSections=['section_restricted_uri']
            ),
        }

    # ------------------------------------------
    #   Definitions for section_frame_sequence
    # ------------------------------------------
    frameseq = {
        #'frame_sequence_conserved_quantity_frames' : MetaInfoMap(startpage,
        #    depends=[{'store' : 'TS'}],
        #    valtype='int',
        #    lookupdict=self.mddataDict
        #    ),
        #'frame_sequence_conserved_quantity_stats' : MetaInfoMap(startpage),
        #'frame_sequence_conserved_quantity' : MetaInfoMap(startpage,
        #    depends=[{'store' : ''}],
        #    valtype='float',
        #    unitdict=self.unitDict,
        #    unit='kilo-joule/mol',
        #    lookupdict=self.mddataDict
        #    ),
        'frame_sequence_continuation_kind' : MetaInfoMap(startpage),
        'frame_sequence_external_url' : MetaInfoMap(startpage),
        'frame_sequence_kinetic_energy_frames' : MetaInfoMap(startpage,
            depends=[{'store' : 'STEP'}],
            valtype='int',
            lookupdict=self.mddataDict
            ),
        'frame_sequence_kinetic_energy_stats' : MetaInfoMap(startpage),
        'frame_sequence_kinetic_energy' : MetaInfoMap(startpage,
            depends=[{'store' : 'E_Kinetic'}],
            valtype='float',
            unitdict=self.unitDict,
            unit='kilo-joule/mol',
            lookupdict=self.mddataDict
            ),
        'frame_sequence_local_frames_ref' : MetaInfoMap(startpage),
        'frame_sequence_potential_energy_frames' : MetaInfoMap(startpage,
            depends=[{'store' : 'STEP'}],
            valtype='int',
            lookupdict=self.mddataDict
            ),
        'frame_sequence_potential_energy_stats' : MetaInfoMap(startpage),
        'frame_sequence_potential_energy' : MetaInfoMap(startpage,
            depends=[{'store' : 'E_Potential'}],
            valtype='float',
            unitdict=self.unitDict,
            unit='kilo-joule/mol',
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
        'frame_sequence_pressure_frames' : MetaInfoMap(startpage,
            depends=[{'store' : 'STEP'}],
            valtype='int',
            lookupdict=self.mddataDict
            ),
        'frame_sequence_pressure_stats' : MetaInfoMap(startpage),
        'frame_sequence_pressure' : MetaInfoMap(startpage,
            depends=[{'store' : 'Pressure'}],
            valtype='float',
            unitdict=self.unitDict,
            unit='kilo-joule/(mol-(nano-meter)**3)',
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
        'frame_sequence_temperature_frames' : MetaInfoMap(startpage,
            depends=[{'store' : 'STEP'}],
            valtype='int',
            lookupdict=self.mddataDict
            ),
        'frame_sequence_temperature_stats' : MetaInfoMap(startpage),
        'frame_sequence_temperature' : MetaInfoMap(startpage,
            depends=[{'store' : 'T_avg'}],
            valtype='float',
            unitdict=self.unitDict,
            unit='Kelvin',
            lookupdict=self.mddataDict
            ),
        'frame_sequence_time' : MetaInfoMap(startpage,
            depends=[{'store' : 'TIME'}],
            valtype='float',
            unitdict=self.unitDict,
            unit='nano-second',
            # Calculates in AKMA units including inputs but prints in picoseconds.
            lookupdict=self.mddataDict
            ),
        'x_gromos_frame_sequence_volume_frames' : MetaInfoMap(startpage,
            activeSections=['section_frame_sequence'],
            depends=[{'store' : 'STEP'}],
            valtype='int',
            lookupdict=self.mddataDict
            ),
        'x_gromos_frame_sequence_volume' : MetaInfoMap(startpage,
            activeSections=['section_frame_sequence'],
            depends=[{'store' : 'volume'}],
            valtype='float',
            unitdict=self.unitDict,
            unit='(nano-meter)**3',
            lookupdict=self.mddataDict
            ),
        'x_gromos_frame_sequence_total_energy_frames' : MetaInfoMap(startpage,
            activeSections=['section_frame_sequence'],
            depends=[{'store' : 'STEP'}],
            valtype='int',
            lookupdict=self.mddataDict
            ),
        'x_gromos_frame_sequence_total_energy' : MetaInfoMap(startpage,
            activeSections=['section_frame_sequence'],
            depends=[{'store' : 'E_Total'}],
            valtype='float',
            unitdict=self.unitDict,
            unit='kilo-joule/mol',
            lookupdict=self.mddataDict
            ),
        'x_gromos_frame_sequence_total_kinetic_energy_frames' : MetaInfoMap(startpage,
            activeSections=['section_frame_sequence'],
            depends=[{'store' : 'STEP'}],
            valtype='int',
            lookupdict=self.mddataDict
            ),
        'x_gromos_frame_sequence_total_kinetic_energy' : MetaInfoMap(startpage,
            activeSections=['section_frame_sequence'],
            depends=[{'store' : 'E_Kinetic'}],
            valtype='float',
            unitdict=self.unitDict,
            unit='kilo-joule/mol',
            lookupdict=self.mddataDict
            ),
        #'x_gromos_frame_sequence_virial_kinetic_energy_frames' : MetaInfoMap(startpage,
        #    activeSections=['section_frame_sequence'],
        #    depends=[{'store' : 'STEP'}],
        #    valtype='int',
        #    lookupdict=self.mddataDict
        #    ),
        #'x_gromos_frame_sequence_virial_kinetic_energy_energy' : MetaInfoMap(startpage,
        #    activeSections=['section_frame_sequence'],
        #    depends=[{'store' : 'VIRKE'}],
        #    valtype='float',
        #    unitdict=self.unitDict,
        #    unit=self.unitDict['kilo-joule/mol'],
        #    lookupdict=self.mddataDict
        #    ),
        #'x_gromos_frame_sequence_boundary_frames' : MetaInfoMap(startpage,
        #    activeSections=['section_frame_sequence'],
        #    depends=[{'store' : 'STEP'}],
        #    valtype='int',
        #    lookupdict=self.mddataDict
        #    ),
        #'x_gromos_frame_sequence_boundary' : MetaInfoMap(startpage,
        #    activeSections=['section_frame_sequence'],
        #    depends=[{'store' : 'BOUNDARY'}],
        #    valtype='float',
        #    unitdict=self.unitDict,
        #    unit='kilo-joule/mol',
        #    lookupdict=self.mddataDict
        #    ),
        'x_gromos_frame_sequence_bond_energy_frames' : MetaInfoMap(startpage,
            activeSections=['section_frame_sequence'],
            depends=[{'store' : 'STEP'}],
            valtype='int',
            lookupdict=self.mddataDict
            ),
        'x_gromos_frame_sequence_bond_energy' : MetaInfoMap(startpage,
            activeSections=['section_frame_sequence'],
            depends=[{'store' : 'E_Bonds'}],
            valtype='float',
            unitdict=self.unitDict,
            unit='kilo-joule/mol',
            lookupdict=self.mddataDict
            ),
        'x_gromos_frame_sequence_angle_energy_frames' : MetaInfoMap(startpage,
            activeSections=['section_frame_sequence'],
            depends=[{'store' : 'STEP'}],
            valtype='int',
            lookupdict=self.mddataDict
            ),
        'x_gromos_frame_sequence_angle_energy' : MetaInfoMap(startpage,
            activeSections=['section_frame_sequence'],
            depends=[{'store' : 'E_Angles'}],
            valtype='float',
            unitdict=self.unitDict,
            unit='kilo-joule/mol',
            lookupdict=self.mddataDict
            ),
        'x_gromos_frame_sequence_proper_dihedral_energy_frames' : MetaInfoMap(startpage,
            activeSections=['section_frame_sequence'],
            depends=[{'store' : 'STEP'}],
            valtype='int',
            lookupdict=self.mddataDict
            ),
        'x_gromos_frame_sequence_proper_dihedral_energy' : MetaInfoMap(startpage,
            activeSections=['section_frame_sequence'],
            depends=[{'store' : 'E_Dihedral'}],
            valtype='float',
            unitdict=self.unitDict,
            unit='kilo-joule/mol',
            lookupdict=self.mddataDict
            ),
        'x_gromos_frame_sequence_improper_dihedral_energy_frames' : MetaInfoMap(startpage,
            activeSections=['section_frame_sequence'],
            depends=[{'store' : 'STEP'}],
            valtype='int',
            lookupdict=self.mddataDict
            ),
        'x_gromos_frame_sequence_improper_dihedral_energy' : MetaInfoMap(startpage,
            activeSections=['section_frame_sequence'],
            depends=[{'store' : 'E_Improper'}],
            valtype='float',
            unitdict=self.unitDict,
            unit='kilo-joule/mol',
            lookupdict=self.mddataDict
            ),
        'x_gromos_frame_sequence_cross_dihedral_energy_frames' : MetaInfoMap(startpage,
            activeSections=['section_frame_sequence'],
            depends=[{'store' : 'STEP'}],
            valtype='int',
            lookupdict=self.mddataDict
            ),
        'x_gromos_frame_sequence_cross_dihedral_energy' : MetaInfoMap(startpage,
            activeSections=['section_frame_sequence'],
            depends=[{'store' : 'E_Crossdihedral'}],
            valtype='float',
            unitdict=self.unitDict,
            unit='kilo-joule/mol',
            lookupdict=self.mddataDict
            ),
        'x_gromos_frame_sequence_vdw_energy_frames' : MetaInfoMap(startpage,
            activeSections=['section_frame_sequence'],
            depends=[{'store' : 'STEP'}],
            valtype='int',
            lookupdict=self.mddataDict
            ),
        'x_gromos_frame_sequence_vdw_energy' : MetaInfoMap(startpage,
            activeSections=['section_frame_sequence'],
            depends=[{'store' : 'E_Vdw'}],
            valtype='float',
            unitdict=self.unitDict,
            unit='kilo-joule/mol',
            lookupdict=self.mddataDict
            ),
        'x_gromos_frame_sequence_electrostatic_energy_frames' : MetaInfoMap(startpage,
            activeSections=['section_frame_sequence'],
            depends=[{'store' : 'STEP'}],
            valtype='int',
            lookupdict=self.mddataDict
            ),
        'x_gromos_frame_sequence_electrostatic_energy' : MetaInfoMap(startpage,
            activeSections=['section_frame_sequence'],
            depends=[{'store' : 'E_Non-bonded'}],
            valtype='float',
            unitdict=self.unitDict,
            unit='kilo-joule/mol',
            lookupdict=self.mddataDict
            ),
        'x_gromos_frame_sequence_covalent_energy_frames' : MetaInfoMap(startpage,
            activeSections=['section_frame_sequence'],
            depends=[{'store' : 'STEP'}],
            valtype='int',
            lookupdict=self.mddataDict
            ),
        'x_gromos_frame_sequence_covalent_energy' : MetaInfoMap(startpage,
            activeSections=['section_frame_sequence'],
            depends=[{'store' : 'E_Covalent'}],
            valtype='float',
            unitdict=self.unitDict,
            unit='kilo-joule/mol',
            lookupdict=self.mddataDict
            ),
        #'frame_sequence_to_sampling_ref' : MetaInfoMap(startpage),
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
        #            'frame_sequence_conserved_quantity_frames'
        #            )
        #        )
        #    ),
        'number_of_frames_in_sequence' : MetaInfoMap(startpage, activeInfo=True,
            value=(lambda x: np.array(x['val']).flatten().shape[0] if(
                x is not None and x['val'] is not None) else None)(
                self.metaStorage.fetchAttrValue(
                    'frame_sequence_potential_energy_frames'
                    )
                )
            ),
        'number_of_kinetic_energies_in_sequence' : MetaInfoMap(startpage, activeInfo=True,
            value=(lambda x: np.array(x['val']).flatten().shape[0] if(
                x is not None and x['val'] is not None) else None)(
                self.metaStorage.fetchAttrValue(
                    'frame_sequence_kinetic_energy_frames'
                    )
                )
            ),
        'number_of_potential_energies_in_sequence' : MetaInfoMap(startpage,
            activeInfo=True,
            value=(lambda x: np.array(x['val']).flatten().shape[0] if(
                x is not None and x['val'] is not None) else None)(
                self.metaStorage.fetchAttrValue(
                    'frame_sequence_potential_energy_frames'
                    )
                )
            ),
        'number_of_pressure_evaluations_in_sequence' : MetaInfoMap(startpage,
            activeInfo=True,
            value=(lambda x: np.array(x['val']).flatten().shape[0] if(
                x is not None and x['val'] is not None) else None)(
                self.metaStorage.fetchAttrValue(
                    'frame_sequence_pressure_frames'
                    )
                )
            ),
        'number_of_temperatures_in_sequence' : MetaInfoMap(startpage,
            activeInfo=True,
            value=(lambda x: np.array(x['val']).flatten().shape[0] if(
                x is not None and x['val'] is not None) else None)(
                self.metaStorage.fetchAttrValue(
                    'frame_sequence_temperature_frames'
                    )
                )
            ),
        'x_gromos_number_of_volumes_in_sequence' : MetaInfoMap(startpage,
            activeInfo=True,
            activeSections=['section_frame_sequence'],
            value=(lambda x: np.array(x['val']).flatten().shape[0] if(
                x is not None and x['val'] is not None) else None)(
                self.metaStorage.fetchAttrValue(
                    'x_gromos_frame_sequence_volume_frames'
                    )
                )
            ),
        #'x_gromos_number_of_boundary_energies_in_sequence' : MetaInfoMap(startpage,
        #    activeInfo=True,
        #    activeSections=['section_frame_sequence'],
        #    value=(lambda x: np.array(x['val']).flatten().shape[0] if(
        #        x is not None and x['val'] is not None) else None)(
        #        self.metaStorage.fetchAttrValue(
        #            'x_gromos_frame_sequence_boundary_frames'
        #            )
        #        )
        #    ),
        'x_gromos_number_of_bond_energies_in_sequence' : MetaInfoMap(startpage,
            activeInfo=True,
            activeSections=['section_frame_sequence'],
            value=(lambda x: np.array(x['val']).flatten().shape[0] if(
                x is not None and x['val'] is not None) else None)(
                self.metaStorage.fetchAttrValue(
                    'x_gromos_frame_sequence_bond_energy_frames'
                    )
                )
            ),
        'x_gromos_number_of_angle_energies_in_sequence' : MetaInfoMap(startpage,
            activeInfo=True,
            activeSections=['section_frame_sequence'],
            value=(lambda x: np.array(x['val']).flatten().shape[0] if(
                x is not None and x['val'] is not None) else None)(
                self.metaStorage.fetchAttrValue(
                    'x_gromos_frame_sequence_angle_energy_frames'
                    )
                )
            ),
        'x_gromos_number_of_electrostatic_energies_in_sequence' : MetaInfoMap(startpage,
            activeInfo=True,
            activeSections=['section_frame_sequence'],
            value=(lambda x: np.array(x['val']).flatten().shape[0] if(
                x is not None and x['val'] is not None) else None)(
                self.metaStorage.fetchAttrValue(
                    'x_gromos_frame_sequence_electrostatic_energy_frames'
                    )
                )
            ),
        'x_gromos_number_of_vdw_energies_in_sequence' : MetaInfoMap(startpage,
            activeInfo=True,
            activeSections=['section_frame_sequence'],
            value=(lambda x: np.array(x['val']).flatten().shape[0] if(
                x is not None and x['val'] is not None) else None)(
                self.metaStorage.fetchAttrValue(
                    'x_gromos_frame_sequence_vdw_energy_frames'
                    )
                )
            ),
        'x_gromos_number_of_proper_dihedral_energies_in_sequence' : MetaInfoMap(startpage,
            activeInfo=True,
            activeSections=['section_frame_sequence'],
            value=(lambda x: np.array(x['val']).flatten().shape[0] if(
                x is not None and x['val'] is not None) else None)(
                self.metaStorage.fetchAttrValue(
                    'x_gromos_frame_sequence_proper_dihedral_energy_frames'
                    )
                )
            ),
        'x_gromos_number_of_improper_dihedral_energies_in_sequence' : MetaInfoMap(startpage,
            activeInfo=True,
            activeSections=['section_frame_sequence'],
            value=(lambda x: np.array(x['val']).flatten().shape[0] if(
                x is not None and x['val'] is not None) else None)(
                self.metaStorage.fetchAttrValue(
                    'x_gromos_frame_sequence_improper_dihedral_energy_frames'
                    )
                )
            ),
        'x_gromos_number_of_cross_dihedral_energies_in_sequence' : MetaInfoMap(startpage,
            activeInfo=True,
            activeSections=['section_frame_sequence'],
            value=(lambda x: np.array(x['val']).flatten().shape[0] if(
                x is not None and x['val'] is not None) else None)(
                self.metaStorage.fetchAttrValue(
                    'x_gromos_frame_sequence_cross_dihedral_energy_frames'
                    )
                )
            ),
        'x_gromos_number_of_covalent_energies_in_sequence' : MetaInfoMap(startpage,
            activeInfo=True,
            activeSections=['section_frame_sequence'],
            value=(lambda x: np.array(x['val']).flatten().shape[0] if(
                x is not None and x['val'] is not None) else None)(
                self.metaStorage.fetchAttrValue(
                    'x_gromos_frame_sequence_covalent_energy_frames'
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
        'SC_matrix' : MetaInfoMap(startpage),
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


