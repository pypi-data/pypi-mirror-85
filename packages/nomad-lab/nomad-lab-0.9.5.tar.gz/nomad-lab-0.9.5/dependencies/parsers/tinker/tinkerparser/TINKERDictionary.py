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
from .TINKERCommon import PARSERNAME, PROGRAMNAME, PARSERTAG
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
        'fileInterface'   : ["tinkerread", "parmed", "mdanalysis", "mdtraj", "pymolfile"]
        }
    namelist = {
        'structure'     : FileInfoMap(startpage, fileFormat=['.tinkerxyz', '.txyz'], activeInfo=False,
                                      infoPurpose=['topology', 'inputcoordinates']),
        'input_coord'   : FileInfoMap(startpage, fileFormat=['.tinkerxyz', '.txyz'], activeInfo=False,
                                      infoPurpose=['inputcoordinates', 'inputvelocities']),
        'output_coord'  : FileInfoMap(startpage, fileFormat=['.tinkerdyn', '.dyn'], activeInfo=False,
                                      infoPurpose=['outputcoordinates', 'outputvelocities']),
        'trajectory'    : FileInfoMap(startpage, fileFormat=['.txyz', '.arc'], activeInfo=False,
                                      infoPurpose=['trajectory']),
        'parameter'     : FileInfoMap(startpage, fileFormat=['.tinkerprm'], activeInfo=False,
                                      infoPurpose=['forcefield']),
        'output_log'    : FileInfoMap(startpage),
        'control_input' : FileInfoMap(startpage),
        }
    return MapDictionary(namelist)

def get_nameListDict(deflist):
    """Loads control in data of TINKER.

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

    mdcntrllist = {
        'RMS Grad'      : MetaInfoMap(startpage),
        'Molecular Dynamics Trajectory via'  : MetaInfoMap(startpage, matchWith='EOL',
            replaceTag='integrator',
            subFunc=lambda x: ' '.join(x.strip().split()) if x is not None else None),
        'Optimization'  : MetaInfoMap(startpage, matchWith='BOL',
            replaceTag='optimization algorithm',
            subFunc=lambda x: ' '.join(x.strip().split()) if x is not None else None),
        'Algorithm'     : MetaInfoMap(startpage),
        'Random Number Generator Initialized with SEED' : MetaInfoMap(startpage,
            replaceTag='Random Number Generator seed'),
        'Preconditioning' : MetaInfoMap(startpage),
        'Termin'      : MetaInfoMap(startpage, matchWith='PW', matchAlso='--',
            replaceTag='termination status'),
        'nation'     : MetaInfoMap(startpage, matchAlso='--', matchWith='EOL',
            replaceTag='termination reason',
            subFunc=lambda x: ' '.join(x.strip().replace(
                'due to', '').replace('at', '').split()) if x is not None else None),
        'Function Value' : MetaInfoMap(startpage),
        'RMS Gradient' : MetaInfoMap(startpage),
        'RMS Coordinate Gradient' : MetaInfoMap(startpage),
        'RMS Lattice Gradient' : MetaInfoMap(startpage),
        'Final Gradient Norm' : MetaInfoMap(startpage),
        'Coordinate Gradient Norm' : MetaInfoMap(startpage),
        'Lattice Gradient Norm' : MetaInfoMap(startpage),
        #''           : MetaInfoMap(startpage, defaultValue=None),
        }

    filecntrllist = {
        'key file'  : MetaInfoMap(startpage, defaultValue=None),
        'coordinate file list'  : MetaInfoMap(startpage, defaultValue=None),
        'topology file'  : MetaInfoMap(startpage, defaultValue=None),
        'force field file'  : MetaInfoMap(startpage, defaultValue=None),
        'initial configuration file'  : MetaInfoMap(startpage, defaultValue=None),
        'final configuration file'  : MetaInfoMap(startpage, defaultValue=None),
        'initial trajectory file'  : MetaInfoMap(startpage, defaultValue=None),
        'restart file'  : MetaInfoMap(startpage, defaultValue=None),
        'archive file'  : MetaInfoMap(startpage, defaultValue=None),
        }

    topocntrllist = {
        'atom'  : MetaInfoMap(startpage, defaultValue=None),
        'vdw'  : MetaInfoMap(startpage, defaultValue=None),
        'bond'  : MetaInfoMap(startpage, defaultValue=None),
        'angle'  : MetaInfoMap(startpage, defaultValue=None),
        'ureybond'  : MetaInfoMap(startpage, defaultValue=None),
        'charge'  : MetaInfoMap(startpage, defaultValue=None),
        }

    cntrllist = {
        'NSTEP'  : MetaInfoMap(startpage, defaultValue=None),
        'parameters'  : MetaInfoMap(startpage, defaultValue=None),
        'verbose'  : MetaInfoMap(startpage, defaultValue=None),
        'lights'  : MetaInfoMap(startpage, defaultValue=None),
        'randomseed'  : MetaInfoMap(startpage, defaultValue=None),
        'a-axis'  : MetaInfoMap(startpage, defaultValue=None),
        'b-axis'  : MetaInfoMap(startpage, defaultValue=None),
        'c-axis'  : MetaInfoMap(startpage, defaultValue=None),
        'alpha'  : MetaInfoMap(startpage, defaultValue=None),
        'beta'  : MetaInfoMap(startpage, defaultValue=None),
        'gamma'  : MetaInfoMap(startpage, defaultValue=None),
        'vdwtype'  : MetaInfoMap(startpage, defaultValue=None),
        'radiusrule'  : MetaInfoMap(startpage, defaultValue=None),
        'radiustype'  : MetaInfoMap(startpage, defaultValue=None),
        'radiussize'  : MetaInfoMap(startpage, defaultValue=None),
        'epsilonrule'  : MetaInfoMap(startpage, defaultValue=None),
        'dielectric'  : MetaInfoMap(startpage, defaultValue=None),
        'integrator'  : MetaInfoMap(startpage, defaultValue=None),
        'rattle'  : MetaInfoMap(startpage, defaultValue=None),
        'lambda'  : MetaInfoMap(startpage, defaultValue=None),
        'mutate'  : MetaInfoMap(startpage, defaultValue=None),
        'basin'  : MetaInfoMap(startpage, defaultValue=None),
        'saddlepoint'  : MetaInfoMap(startpage, defaultValue=None),
        'neighbor-list'  : MetaInfoMap(startpage, defaultValue=None),
        'vdw-cutoff'  : MetaInfoMap(startpage, defaultValue=None),
        'vdw-correction'  : MetaInfoMap(startpage, defaultValue=None),
        'ewald'  : MetaInfoMap(startpage, defaultValue=None),
        'ewald-cutoff'  : MetaInfoMap(startpage, defaultValue=None),
        'pme-grid'  : MetaInfoMap(startpage, defaultValue=None),
        'pme-order'  : MetaInfoMap(startpage, defaultValue=None),
        'polar-eps'  : MetaInfoMap(startpage, defaultValue=None),
        'enforce-chirality'  : MetaInfoMap(startpage, defaultValue=None),
        'printout'  : MetaInfoMap(startpage, defaultValue=None),
        'digits'  : MetaInfoMap(startpage, defaultValue=None),
        'spacegroup'  : MetaInfoMap(startpage, defaultValue=None),
        'vib-roots'  : MetaInfoMap(startpage, defaultValue=None),
        'group-inter'  : MetaInfoMap(startpage, defaultValue=None),
        'group'  : MetaInfoMap(startpage, defaultValue=None),
        'debug'  : MetaInfoMap(startpage, defaultValue=None),
        'chargeterm'  : MetaInfoMap(startpage, defaultValue=None),
        'archive'  : MetaInfoMap(startpage, defaultValue=None),
        'barostat'  : MetaInfoMap(startpage, defaultValue=None),
        'aniso-pressure'  : MetaInfoMap(startpage, defaultValue=None),
        'trial-distance'  : MetaInfoMap(startpage, defaultValue=None),
        'trial-distribution'  : MetaInfoMap(startpage, defaultValue=None),
        #'restrain-torsion'  : MetaInfoMap(startpage, defaultValue=None, activeInfo=False),
        #'restrain-distance'  : MetaInfoMap(startpage, defaultValue=None, activeInfo=False),
        'group-molecule'  : MetaInfoMap(startpage, defaultValue=None),
        'mpole-list'  : MetaInfoMap(startpage, defaultValue=None),
        'tau-temperature'  : MetaInfoMap(startpage, defaultValue=None),
        'tau-pressure'  : MetaInfoMap(startpage, defaultValue=None),
        }

    startpage.update({
        'metaNameTag'     : 'mdout',
        'activeSections'  : ['section_single_configuration_calculation']
        })
    mddatalist = {
        'MD Step'     : MetaInfoMap(startpage),
        'InputCoordStep'  : MetaInfoMap(startpage),
        'OutputCoordStep' : MetaInfoMap(startpage),
        'E Total'     : MetaInfoMap(startpage),
        'E Potential' : MetaInfoMap(startpage),
        'E Kinetic'   : MetaInfoMap(startpage),
        'Temp'        : MetaInfoMap(startpage),
        'Pres'        : MetaInfoMap(startpage),
        'STEP'        : MetaInfoMap(startpage),
        'TIME'        : MetaInfoMap(startpage),
        'VOLUME'      : MetaInfoMap(startpage),
        'VIRIAL'      : MetaInfoMap(startpage),
        'Dynamics Steps'    : MetaInfoMap(startpage, defaultValue=None, matchWith='PW'),
        'Simulation Time'   : MetaInfoMap(startpage, defaultValue=None),
        'Total Energy'      : MetaInfoMap(startpage, defaultValue=None),
        'Potential Energy'  : MetaInfoMap(startpage, defaultValue=None),
        'Kinetic Energy'    : MetaInfoMap(startpage, defaultValue=None),
        'Temperature'       : MetaInfoMap(startpage, defaultValue=None),
        'Pressure'          : MetaInfoMap(startpage, defaultValue=None),
        'Density'           : MetaInfoMap(startpage, defaultValue=None),
        'Current Time'      : MetaInfoMap(startpage, defaultValue=None),
        'Current Potential' : MetaInfoMap(startpage, defaultValue=None),
        'Current Kinetic'   : MetaInfoMap(startpage, defaultValue=None),
        'Lattice Lengths'   : MetaInfoMap(startpage, defaultValue=None, matchWith='EOL',
            subFunc=lambda x: ','.join(x.strip().split()) if x is not None else None),
        'Lattice Angles'    : MetaInfoMap(startpage, defaultValue=None, matchWith='EOL',
            subFunc=lambda x: ','.join(x.strip().split()) if x is not None else None),
        'Frame Number'      : MetaInfoMap(startpage, defaultValue=None),
        'Coordinate File'   : MetaInfoMap(startpage, defaultValue=None),
        'VM Iter'     : MetaInfoMap(startpage),
        'TN Iter'     : MetaInfoMap(startpage),
        'QN Iter'     : MetaInfoMap(startpage),
        'CG Iter'     : MetaInfoMap(startpage),
        'F Value'     : MetaInfoMap(startpage),
        'G RMS'       : MetaInfoMap(startpage),
        'RMS G'       : MetaInfoMap(startpage),
        'F Move'      : MetaInfoMap(startpage),
        'X Move'      : MetaInfoMap(startpage),
        'Angle'       : MetaInfoMap(startpage),
        'FG Call'     : MetaInfoMap(startpage),
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
    elif deflist == 'mdcntrl':
        namelist = mdcntrllist
    elif deflist == 'topocntrl':
        namelist = topocntrllist
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
    self.mdcntrlDict = get_nameListDict('mdcntrl')
    self.topocntrlDict = get_nameListDict('topocntrl')
    self.mdoutDict = get_nameListDict('mdout')
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
            'file'      : self.fileDict,
            'cntrl'     : self.cntrlDict,
            'mdcntrl'   : self.mdcntrlDict,
            'topocntrl'   : self.topocntrlDict,
            'filecntrl' : self.filecntrlDict,
            'mddata'    : self.mddataDict,
            'extra'     : self.extraDict,
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
        #'x_tinker_barostat_type' : MetaInfoMap(startpage,
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
        #'x_tinker_barostat_target_pressure' : MetaInfoMap(startpage,
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
        #'x_tinker_barostat_tau' : MetaInfoMap(startpage,
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
        #'x_tinker_integrator_type' : MetaInfoMap(startpage,
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
        'x_tinker_integrator_dt' : MetaInfoMap(startpage,
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
        'x_tinker_number_of_steps_requested' : MetaInfoMap(startpage,
            depends=[{'value' : 'NSTEP'}],
            lookupdict=self.cntrlDict,
            valtype='int',
            #autoSections=True,
            activeInfo=True,
            activeSections=['settings_integrator']
            ),
        #'x_tinker_thermostat_type' : MetaInfoMap(startpage,
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
        'x_tinker_thermostat_target_temperature' : MetaInfoMap(startpage,
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
        #'x_tinker_thermostat_tau' : MetaInfoMap(startpage,
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
        'x_tinker_periodicity_type' : MetaInfoMap(startpage,
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
        #'energy_electrostatic' : MetaInfoMap(startpage,
        #    depends=[{'value' : 'E '}],
        #    valtype='float',
        #    unitdict=self.unitDict,
        #    unit='kilo-joule/mol',
        #    activeInfo=True,
        #    lookupdict=self.mddataDict
        #    ),
        'energy_free_per_atom' : MetaInfoMap(startpage),
        'energy_free' : MetaInfoMap(startpage),
        #'energy_method_current' : MetaInfoMap(startpage,
        #    depends=[{'assign' : 'Force Field'}],
        #    lookupdict=self.mddataDict
        #    ),
        'energy_T0_per_atom' : MetaInfoMap(startpage),
        'energy_total_T0_per_atom' : MetaInfoMap(startpage),
        'energy_total_T0' : MetaInfoMap(startpage,
            depends=[{'value' : 'E Potential'}],
            valtype='float',
            unitdict=self.unitDict,
            unit='kcal/mol',
            activeInfo=True,
            lookupdict=self.mddataDict
            ),
        'energy_total' : MetaInfoMap(startpage,
            depends=[{'value' : 'E Total'}],
            valtype='float',
            unitdict=self.unitDict,
            unit='kcal/mol',
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
            depends=[{'value' : 'E Vdw'}],
            lookupdict=self.mddataDict,
            valtype='float',
            unitdict=self.unitDict,
            unit='kcal/mol',
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
                'supportDict' : self.cntrlDict,
                },
            ),
        'restricted_uri_license' : MetaInfoMap(startpage,
            value='TINKER License',
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
            value='TINKER',
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
        #    unit='kcal/mol',
        #    lookupdict=self.mddataDict
        #    ),
        'frame_sequence_continuation_kind' : MetaInfoMap(startpage),
        'frame_sequence_external_url' : MetaInfoMap(startpage),
        'frame_sequence_kinetic_energy_frames' : MetaInfoMap(startpage,
            depends=[{'store' : 'MD Step'}],
            valtype='int',
            lookupdict=self.mddataDict
            ),
        'frame_sequence_kinetic_energy_stats' : MetaInfoMap(startpage),
        'frame_sequence_kinetic_energy' : MetaInfoMap(startpage,
            depends=[{'store' : 'E Kinetic'}],
            valtype='float',
            unitdict=self.unitDict,
            unit='kcal/mol',
            lookupdict=self.mddataDict
            ),
        'frame_sequence_local_frames_ref' : MetaInfoMap(startpage),
        'frame_sequence_potential_energy_frames' : MetaInfoMap(startpage,
            depends=[{'store' : 'MD Step'}],
            valtype='int',
            lookupdict=self.mddataDict
            ),
        'frame_sequence_potential_energy_stats' : MetaInfoMap(startpage),
        'frame_sequence_potential_energy' : MetaInfoMap(startpage,
            depends=[{'store' : 'E Potential'}],
            valtype='float',
            unitdict=self.unitDict,
            unit='kcal/mol',
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
            depends=[{'store' : 'MD Step'}],
            valtype='int',
            lookupdict=self.mddataDict
            ),
        'frame_sequence_pressure_stats' : MetaInfoMap(startpage),
        'frame_sequence_pressure' : MetaInfoMap(startpage,
            depends=[{'store' : 'Pres'}],
            valtype='float',
            unitdict=self.unitDict,
            unit='bar',
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
            depends=[{'store' : 'MD Step'}],
            valtype='int',
            lookupdict=self.mddataDict
            ),
        'frame_sequence_temperature_stats' : MetaInfoMap(startpage),
        'frame_sequence_temperature' : MetaInfoMap(startpage,
            depends=[{'store' : 'Temp'}],
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
        'x_tinker_frame_sequence_density_frames' : MetaInfoMap(startpage,
            activeSections=['section_frame_sequence'],
            depends=[{'store' : 'Dynamics Steps'}],
            valtype='int',
            lookupdict=self.mddataDict
            ),
        'x_tinker_frame_sequence_density' : MetaInfoMap(startpage,
            activeSections=['section_frame_sequence'],
            depends=[{'store' : 'Density'}],
            valtype='float',
            unitdict=self.unitDict,
            unit='1.0/Angstrom**3',
            lookupdict=self.mddataDict
            ),
        'x_tinker_frame_sequence_volume_frames' : MetaInfoMap(startpage,
            activeSections=['section_frame_sequence'],
            depends=[{'store' : 'MD Step'}],
            valtype='int',
            lookupdict=self.mddataDict
            ),
        'x_tinker_frame_sequence_volume' : MetaInfoMap(startpage,
            activeSections=['section_frame_sequence'],
            depends=[{'store' : 'volume'}],
            valtype='float',
            unitdict=self.unitDict,
            unit='Angstrom**3',
            lookupdict=self.mddataDict
            ),
        'x_tinker_frame_sequence_total_energy_frames' : MetaInfoMap(startpage,
            activeSections=['section_frame_sequence'],
            depends=[{'store' : 'MD Step'}],
            valtype='int',
            lookupdict=self.mddataDict
            ),
        'x_tinker_frame_sequence_total_energy' : MetaInfoMap(startpage,
            activeSections=['section_frame_sequence'],
            depends=[{'store' : 'E Total'}],
            valtype='float',
            unitdict=self.unitDict,
            unit='kcal/mol',
            lookupdict=self.mddataDict
            ),
        'x_tinker_frame_sequence_total_kinetic_energy_frames' : MetaInfoMap(startpage,
            activeSections=['section_frame_sequence'],
            depends=[{'store' : 'STEP'}],
            valtype='int',
            lookupdict=self.mddataDict
            ),
        'x_tinker_frame_sequence_total_kinetic_energy' : MetaInfoMap(startpage,
            activeSections=['section_frame_sequence'],
            depends=[{'store' : 'E Kinetic'}],
            valtype='float',
            unitdict=self.unitDict,
            unit='kcal/mol',
            lookupdict=self.mddataDict
            ),
        #'x_tinker_frame_sequence_virial_kinetic_energy_frames' : MetaInfoMap(startpage,
        #    activeSections=['section_frame_sequence'],
        #    depends=[{'store' : 'STEP'}],
        #    valtype='int',
        #    lookupdict=self.mddataDict
        #    ),
        #'x_tinker_frame_sequence_virial_kinetic_energy_energy' : MetaInfoMap(startpage,
        #    activeSections=['section_frame_sequence'],
        #    depends=[{'store' : 'VIRKE'}],
        #    valtype='float',
        #    unitdict=self.unitDict,
        #    unit=self.unitDict['kcal/mol'],
        #    lookupdict=self.mddataDict
        #    ),
        #'x_tinker_frame_sequence_boundary_frames' : MetaInfoMap(startpage,
        #    activeSections=['section_frame_sequence'],
        #    depends=[{'store' : 'STEP'}],
        #    valtype='int',
        #    lookupdict=self.mddataDict
        #    ),
        #'x_tinker_frame_sequence_boundary' : MetaInfoMap(startpage,
        #    activeSections=['section_frame_sequence'],
        #    depends=[{'store' : 'BOUNDARY'}],
        #    valtype='float',
        #    unitdict=self.unitDict,
        #    unit='kcal/mol',
        #    lookupdict=self.mddataDict
        #    ),
        #'x_tinker_frame_sequence_bond_energy_frames' : MetaInfoMap(startpage,
        #    activeSections=['section_frame_sequence'],
        #    depends=[{'store' : 'STEP'}],
        #    valtype='int',
        #    lookupdict=self.mddataDict
        #    ),
        #'x_tinker_frame_sequence_bond_energy' : MetaInfoMap(startpage,
        #    activeSections=['section_frame_sequence'],
        #    depends=[{'store' : 'E_Bonds'}],
        #    valtype='float',
        #    unitdict=self.unitDict,
        #    unit='kilo-joule/mol',
        #    lookupdict=self.mddataDict
        #    ),
        #'x_tinker_frame_sequence_angle_energy_frames' : MetaInfoMap(startpage,
        #    activeSections=['section_frame_sequence'],
        #    depends=[{'store' : 'STEP'}],
        #    valtype='int',
        #    lookupdict=self.mddataDict
        #    ),
        #'x_tinker_frame_sequence_angle_energy' : MetaInfoMap(startpage,
        #    activeSections=['section_frame_sequence'],
        #    depends=[{'store' : 'E_Angles'}],
        #    valtype='float',
        #    unitdict=self.unitDict,
        #    unit='kilo-joule/mol',
        #    lookupdict=self.mddataDict
        #    ),
        #'x_tinker_frame_sequence_proper_dihedral_energy_frames' : MetaInfoMap(startpage,
        #    activeSections=['section_frame_sequence'],
        #    depends=[{'store' : 'STEP'}],
        #    valtype='int',
        #    lookupdict=self.mddataDict
        #    ),
        #'x_tinker_frame_sequence_proper_dihedral_energy' : MetaInfoMap(startpage,
        #    activeSections=['section_frame_sequence'],
        #    depends=[{'store' : 'E_Dihedral'}],
        #    valtype='float',
        #    unitdict=self.unitDict,
        #    unit='kilo-joule/mol',
        #    lookupdict=self.mddataDict
        #    ),
        #'x_tinker_frame_sequence_improper_dihedral_energy_frames' : MetaInfoMap(startpage,
        #    activeSections=['section_frame_sequence'],
        #    depends=[{'store' : 'STEP'}],
        #    valtype='int',
        #    lookupdict=self.mddataDict
        #    ),
        #'x_tinker_frame_sequence_improper_dihedral_energy' : MetaInfoMap(startpage,
        #    activeSections=['section_frame_sequence'],
        #    depends=[{'store' : 'E_Improper'}],
        #    valtype='float',
        #    unitdict=self.unitDict,
        #    unit='kilo-joule/mol',
        #    lookupdict=self.mddataDict
        #    ),
        #'x_tinker_frame_sequence_cross_dihedral_energy_frames' : MetaInfoMap(startpage,
        #    activeSections=['section_frame_sequence'],
        #    depends=[{'store' : 'STEP'}],
        #    valtype='int',
        #    lookupdict=self.mddataDict
        #    ),
        #'x_tinker_frame_sequence_cross_dihedral_energy' : MetaInfoMap(startpage,
        #    activeSections=['section_frame_sequence'],
        #    depends=[{'store' : 'E_Crossdihedral'}],
        #    valtype='float',
        #    unitdict=self.unitDict,
        #    unit='kilo-joule/mol',
        #    lookupdict=self.mddataDict
        #    ),
        #'x_tinker_frame_sequence_vdw_energy_frames' : MetaInfoMap(startpage,
        #    activeSections=['section_frame_sequence'],
        #    depends=[{'store' : 'STEP'}],
        #    valtype='int',
        #    lookupdict=self.mddataDict
        #    ),
        #'x_tinker_frame_sequence_vdw_energy' : MetaInfoMap(startpage,
        #    activeSections=['section_frame_sequence'],
        #    depends=[{'store' : 'E_Vdw'}],
        #    valtype='float',
        #    unitdict=self.unitDict,
        #    unit='kilo-joule/mol',
        #    lookupdict=self.mddataDict
        #    ),
        #'x_tinker_frame_sequence_electrostatic_energy_frames' : MetaInfoMap(startpage,
        #    activeSections=['section_frame_sequence'],
        #    depends=[{'store' : 'STEP'}],
        #    valtype='int',
        #    lookupdict=self.mddataDict
        #    ),
        #'x_tinker_frame_sequence_electrostatic_energy' : MetaInfoMap(startpage,
        #    activeSections=['section_frame_sequence'],
        #    depends=[{'store' : 'E_Non-bonded'}],
        #    valtype='float',
        #    unitdict=self.unitDict,
        #    unit='kilo-joule/mol',
        #    lookupdict=self.mddataDict
        #    ),
        #'x_tinker_frame_sequence_covalent_energy_frames' : MetaInfoMap(startpage,
        #    activeSections=['section_frame_sequence'],
        #    depends=[{'store' : 'STEP'}],
        #    valtype='int',
        #    lookupdict=self.mddataDict
        #    ),
        #'x_tinker_frame_sequence_covalent_energy' : MetaInfoMap(startpage,
        #    activeSections=['section_frame_sequence'],
        #    depends=[{'store' : 'E_Covalent'}],
        #    valtype='float',
        #    unitdict=self.unitDict,
        #    unit='kilo-joule/mol',
        #    lookupdict=self.mddataDict
        #    ),
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
        'x_tinker_number_of_density_in_sequence' : MetaInfoMap(startpage,
            activeInfo=True,
            activeSections=['section_frame_sequence'],
            value=(lambda x: np.array(x['val']).flatten().shape[0] if(
                x is not None and x['val'] is not None) else None)(
                self.metaStorage.fetchAttrValue(
                    'x_tinker_frame_sequence_density_frames'
                    )
                )
            ),
        #'x_tinker_number_of_boundary_energies_in_sequence' : MetaInfoMap(startpage,
        #    activeInfo=True,
        #    activeSections=['section_frame_sequence'],
        #    value=(lambda x: np.array(x['val']).flatten().shape[0] if(
        #        x is not None and x['val'] is not None) else None)(
        #        self.metaStorage.fetchAttrValue(
        #            'x_tinker_frame_sequence_boundary_frames'
        #            )
        #        )
        #    ),
        #'x_tinker_number_of_bond_energies_in_sequence' : MetaInfoMap(startpage,
        #    activeInfo=True,
        #    activeSections=['section_frame_sequence'],
        #    value=(lambda x: np.array(x['val']).flatten().shape[0] if(
        #        x is not None and x['val'] is not None) else None)(
        #        self.metaStorage.fetchAttrValue(
        #            'x_tinker_frame_sequence_bond_energy_frames'
        #            )
        #        )
        #    ),
        #'x_tinker_number_of_angle_energies_in_sequence' : MetaInfoMap(startpage,
        #    activeInfo=True,
        #    activeSections=['section_frame_sequence'],
        #    value=(lambda x: np.array(x['val']).flatten().shape[0] if(
        #        x is not None and x['val'] is not None) else None)(
        #        self.metaStorage.fetchAttrValue(
        #            'x_tinker_frame_sequence_angle_energy_frames'
        #            )
        #        )
        #    ),
        #'x_tinker_number_of_electrostatic_energies_in_sequence' : MetaInfoMap(startpage,
        #    activeInfo=True,
        #    activeSections=['section_frame_sequence'],
        #    value=(lambda x: np.array(x['val']).flatten().shape[0] if(
        #        x is not None and x['val'] is not None) else None)(
        #        self.metaStorage.fetchAttrValue(
        #            'x_tinker_frame_sequence_electrostatic_energy_frames'
        #            )
        #        )
        #    ),
        #'x_tinker_number_of_vdw_energies_in_sequence' : MetaInfoMap(startpage,
        #    activeInfo=True,
        #    activeSections=['section_frame_sequence'],
        #    value=(lambda x: np.array(x['val']).flatten().shape[0] if(
        #        x is not None and x['val'] is not None) else None)(
        #        self.metaStorage.fetchAttrValue(
        #            'x_tinker_frame_sequence_vdw_energy_frames'
        #            )
        #        )
        #    ),
        #'x_tinker_number_of_proper_dihedral_energies_in_sequence' : MetaInfoMap(startpage,
        #    activeInfo=True,
        #    activeSections=['section_frame_sequence'],
        #    value=(lambda x: np.array(x['val']).flatten().shape[0] if(
        #        x is not None and x['val'] is not None) else None)(
        #        self.metaStorage.fetchAttrValue(
        #            'x_tinker_frame_sequence_proper_dihedral_energy_frames'
        #            )
        #        )
        #    ),
        #'x_tinker_number_of_improper_dihedral_energies_in_sequence' : MetaInfoMap(startpage,
        #    activeInfo=True,
        #    activeSections=['section_frame_sequence'],
        #    value=(lambda x: np.array(x['val']).flatten().shape[0] if(
        #        x is not None and x['val'] is not None) else None)(
        #        self.metaStorage.fetchAttrValue(
        #            'x_tinker_frame_sequence_improper_dihedral_energy_frames'
        #            )
        #        )
        #    ),
        #'x_tinker_number_of_cross_dihedral_energies_in_sequence' : MetaInfoMap(startpage,
        #    activeInfo=True,
        #    activeSections=['section_frame_sequence'],
        #    value=(lambda x: np.array(x['val']).flatten().shape[0] if(
        #        x is not None and x['val'] is not None) else None)(
        #        self.metaStorage.fetchAttrValue(
        #            'x_tinker_frame_sequence_cross_dihedral_energy_frames'
        #            )
        #        )
        #    ),
        #'x_tinker_number_of_covalent_energies_in_sequence' : MetaInfoMap(startpage,
        #    activeInfo=True,
        #    activeSections=['section_frame_sequence'],
        #    value=(lambda x: np.array(x['val']).flatten().shape[0] if(
        #        x is not None and x['val'] is not None) else None)(
        #        self.metaStorage.fetchAttrValue(
        #            'x_tinker_frame_sequence_covalent_energy_frames'
        #            )
        #        )
        #    ),
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


