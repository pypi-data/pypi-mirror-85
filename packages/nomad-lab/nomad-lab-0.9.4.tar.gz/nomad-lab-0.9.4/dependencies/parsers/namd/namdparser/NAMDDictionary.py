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

import numpy as np
from .NAMDCommon import PARSERNAME, PROGRAMNAME, PARSERTAG
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
        'activeSections'  : [PARSERTAG+'_section_input_output_files']
        }
    namelist = {
        'structure'     : FileInfoMap(startpage, fileFormat=['.psf'], activeInfo=True,
                                      infoPurpose=['topology', 'unitcell']),
        'traj_coord'    : FileInfoMap(startpage, fileFormat=['.dcd'], activeInfo=True,
                                      infoPurpose=['trajectory', 'unitcell']),
        'traj_vel'      : FileInfoMap(startpage, fileFormat=['.dcd'], activeInfo=True,
                                      infoPurpose=['velocities']),
        'traj_force'    : FileInfoMap(startpage, fileFormat=['.dcd'], activeInfo=True,
                                      infoPurpose=['forces']),
        'output_coord'  : FileInfoMap(startpage, fileFormat=['.namdbin'], activeInfo=False,
                                      infoPurpose=['outputcoordinates', 'unitcell']),
        'output_vel'    : FileInfoMap(startpage, fileFormat=['.namdbin'], activeInfo=False,
                                      infoPurpose=['outputvelocities']),
        'output_force'  : FileInfoMap(startpage, fileFormat=['.namdbin'], activeInfo=False,
                                      infoPurpose=['outputforces']),
        'input_coord'   : FileInfoMap(startpage, fileFormat=['.pdb'],
                                      infoPurpose=['inputcoordinates', 'inputunitcell']),
        'input_vel'     : FileInfoMap(startpage, fileFormat=['.pdb'],
                                      infoPurpose=['inputvelocities']),
        'restart_coord' : FileInfoMap(startpage, fileFormat=['.cpt'],
                                      infoPurpose=['inputcoordinates', 'inputunitcell']),
        'restart_vel'   : FileInfoMap(startpage, fileFormat=['.cpt'],
                                      infoPurpose=['inputvelocities']),
        'fftw_datafile' : FileInfoMap(startpage, fileFormat=['.txt'], infoPurpose=['fftwdata']),
        'mdlog'         : FileInfoMap(startpage),
        }
    return MapDictionary(namelist)

def get_nameListDict(deflist):
    """Loads control in data of NAMD.

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
        'Info: TIMESTEP'          : MetaInfoMap(startpage, defaultValue=1,
                                                replaceTag='TIMESTEP'),
        'NUMBER OF STEPS'         : MetaInfoMap(startpage, defaultValue=0),
        'STEPS PER CYCLE'         : MetaInfoMap(startpage, defaultValue=1),
        'PERIODIC CELL BASIS 1'   : MetaInfoMap(startpage, defaultValue=None, matchWith='EOL'),
        'PERIODIC CELL BASIS 2'   : MetaInfoMap(startpage, defaultValue=None, matchWith='EOL'),
        'PERIODIC CELL BASIS 3'   : MetaInfoMap(startpage, defaultValue=None, matchWith='EOL'),
        'PERIODIC CELL CENTER'    : MetaInfoMap(startpage, defaultValue=None, matchWith='EOL'),
        'LOAD BALANCER'           : MetaInfoMap(startpage, defaultValue=None, matchWith='EOL'),
        'LOAD BALANCING STRATEGY' : MetaInfoMap(startpage, defaultValue="New Load Balancers", matchWith='EOL'),
        'LDB PERIOD'              : MetaInfoMap(startpage, defaultValue=None),
        'FIRST LDB TIMESTEP'      : MetaInfoMap(startpage, defaultValue=None),
        'LAST LDB TIMESTEP'       : MetaInfoMap(startpage, defaultValue=None),
        'LDB BACKGROUND SCALING'  : MetaInfoMap(startpage, defaultValue=None),
        'HOM BACKGROUND SCALING'  : MetaInfoMap(startpage, defaultValue=None),
        'PME BACKGROUND SCALING'  : MetaInfoMap(startpage, defaultValue=None),
        'MIN ATOMS PER PATCH'     : MetaInfoMap(startpage, defaultValue=None),
        'INITIAL TEMPERATURE'     : MetaInfoMap(startpage, defaultValue=None),
        'CENTER OF MASS MOVING INITIALLY?' : MetaInfoMap(startpage, defaultValue=None,
                                                         replaceTag='CENTER OF MASS MOVING INITIALLY'),
        'DIELECTRIC'              : MetaInfoMap(startpage, defaultValue=None),
        'EXCLUDE'                 : MetaInfoMap(startpage, defaultValue=None, matchWith='EOL',
                                                         replaceTag='EXCLUDED SPECIES OR GROUPS'),
        '1-4 ELECTROSTATICS SCALED BY' : MetaInfoMap(startpage, defaultValue=None,
                                                     replaceTag='1-4 ELECTROSTATICS SCALE'),
        'Info: DCD FILENAME'      : MetaInfoMap(startpage, defaultValue=None,
                                                replaceTag='TRAJ DCD FILENAME'),
        'Info: DCD FREQUENCY'     : MetaInfoMap(startpage, defaultValue=None,
                                                replaceTag='TRAJ DCD FREQUENCY'),
        'Info: DCD FIRST STEP'    : MetaInfoMap(startpage, defaultValue=None,
                                                replaceTag='TRAJ DCD FIRST STEP'),
        'VELOCITY DCD FILENAME'   : MetaInfoMap(startpage, defaultValue=None),
        'VELOCITY DCD FREQUENCY'  : MetaInfoMap(startpage, defaultValue=None),
        'VELOCITY DCD FIRST STEP' : MetaInfoMap(startpage, defaultValue=None),
        'FORCE DCD FILENAME'      : MetaInfoMap(startpage, defaultValue=None),
        'FORCE DCD FREQUENCY'     : MetaInfoMap(startpage, defaultValue=None),
        'FORCE DCD FIRST STEP'    : MetaInfoMap(startpage, defaultValue=None),
        'OUTPUT FILENAME'         : MetaInfoMap(startpage, defaultValue=None),
        'BINARY OUTPUT'           : MetaInfoMap(startpage, defaultValue=None, matchWith='EOL'),
        'RESTART FILENAME'        : MetaInfoMap(startpage, defaultValue=None),
        'RESTART FREQUENCY'       : MetaInfoMap(startpage, defaultValue=None),
        'BINARY RESTART'          : MetaInfoMap(startpage, defaultValue=None),
        'SWITCHING ACT'           : MetaInfoMap(startpage, defaultValue='Active',
                                                replaceTag='SWITCHING'),
        'SWITCHING ON'            : MetaInfoMap(startpage, defaultValue=None),
        'SWITCHING OFF'           : MetaInfoMap(startpage, defaultValue=None),
        'PAIRLIST DISTANCE'       : MetaInfoMap(startpage, defaultValue=None),
        'PAIRLIST SHRINK RATE'    : MetaInfoMap(startpage, defaultValue=None),
        'PAIRLIST GROW RATE'      : MetaInfoMap(startpage, defaultValue=None),
        'PAIRLIST TRIGGER'        : MetaInfoMap(startpage, defaultValue=None),
        'PAIRLISTS PER CYCLE'     : MetaInfoMap(startpage, defaultValue=None),
        'PAIRLISTS EN'            : MetaInfoMap(startpage, defaultValue='ENABLED',
                                                replaceTag='PAIRLISTS'),
        'MARGIN'                  : MetaInfoMap(startpage, defaultValue=None),
        'HYDROGEN GROUP CUTOFF'   : MetaInfoMap(startpage, defaultValue=None),
        'PATCH DIMENSION'         : MetaInfoMap(startpage, defaultValue=None),
        'ENERGY OUTPUT STEPS'     : MetaInfoMap(startpage, defaultValue=None),
        'CROSSTERM ENERGY'        : MetaInfoMap(startpage, defaultValue=None, matchWith='EOL'),
        'TIMING OUTPUT STEPS'     : MetaInfoMap(startpage, defaultValue=None),
        'VELOCITY RESCALE FREQ'   : MetaInfoMap(startpage, defaultValue=None),
        'VELOCITY RESCALE TEMP'   : MetaInfoMap(startpage, defaultValue=None),
        'VELOCITY REASSIGNMENT FREQ' : MetaInfoMap(startpage, defaultValue=None),
        'VELOCITY REASSIGNMENT TEMP' : MetaInfoMap(startpage, defaultValue=None),
        'VELOCITY REASSIGNMENT INCR' : MetaInfoMap(startpage, defaultValue=None),
        'VELOCITY REASSIGNMENT HOLD' : MetaInfoMap(startpage, defaultValue=None),
        'LOWE-ANDERSEN DYNAMICS'  : MetaInfoMap(startpage, defaultValue=None),
        'LOWE-ANDERSEN TEMPERATURE' : MetaInfoMap(startpage, defaultValue=None),
        'LOWE-ANDERSEN RATE'      : MetaInfoMap(startpage, defaultValue=None),
        'LOWE-ANDERSEN CUTOFF'    : MetaInfoMap(startpage, defaultValue=None),
        'LANGEVIN DYNAMICS'       : MetaInfoMap(startpage, defaultValue=None),
        'LANGEVIN TEMPERATURE'    : MetaInfoMap(startpage, defaultValue=None),
        'LANGEVIN USING'          : MetaInfoMap(startpage, defaultValue=None,
                                                 replaceTag='LANGEVIN INTEGRATOR'),
        'LANGEVIN DAMPING FILE IS' : MetaInfoMap(startpage, defaultValue=None,
                                                 replaceTag='LANGEVIN DAMPING FILE'),
        'LANGEVIN DAMPING COLUMN:' : MetaInfoMap(startpage, defaultValue=None,
                                                 replaceTag='LANGEVIN DAMPING COLUMN'),
        'LANGEVIN DAMPING COEFFICIENT IS' : MetaInfoMap(startpage, defaultValue=None,
                                                 replaceTag='LANGEVIN DAMPING COEFFICIENT UNIT'),
        'LANGEVIN DYNAMICS NOT APPLIED TO' : MetaInfoMap(startpage, defaultValue=None),
        'TEMPERATURE COUPLING'    : MetaInfoMap(startpage, defaultValue=None),
        'COUPLING TEMPERATURE'    : MetaInfoMap(startpage, defaultValue=None),
        'BERENDSEN PRESSURE COUPLING' : MetaInfoMap(startpage, defaultValue=None),
        'COMPRESSIBILITY ESTIMATE IS' : MetaInfoMap(startpage, defaultValue=None,
                                                    replaceTag='BERENDSEN COMPRESSIBILITY ESTIMATE'),
        'RELAXATION TIME IS' : MetaInfoMap(startpage, defaultValue=None,
                                                    replaceTag='BERENDSEN RELAXATION TIME'),
        'APPLIED EVERY'           : MetaInfoMap(startpage, defaultValue=None,
                                                replaceTag='BERENDSEN COUPLING FREQUENCY'),
        'LANGEVIN PISTON PRESSURE CONTROL' : MetaInfoMap(startpage, defaultValue=None),
        'TARGET PRESSURE IS'      : MetaInfoMap(startpage, defaultValue=None,
                                                replaceTag='TARGET PRESSURE'),
        'OSCILLATION PERIOD IS'   : MetaInfoMap(startpage, defaultValue=None,
                                                replaceTag='LANGEVIN OSCILLATION PERIOD'),
        'DECAY TIME IS'           : MetaInfoMap(startpage, defaultValue=None,
                                                replaceTag='LANGEVIN DECAY TIME'),
        'PISTON TEMPERATURE IS'   : MetaInfoMap(startpage, defaultValue=None,
                                                replaceTag='LANGEVIN PISTON TEMPERATURE'),
        'PRESSURE CONTROL IS'     : MetaInfoMap(startpage, defaultValue=None,
                                                replaceTag='PRESSURE CONTROL'),
        'INITIAL STRAIN RATE IS'  : MetaInfoMap(startpage, defaultValue=None, matchWith='EOL',
                                                replaceTag='INITIAL STRAIN RATE'),
        'CELL FLUCTUATION IS'     : MetaInfoMap(startpage, defaultValue=None,
                                                replaceTag='CELL FLUCTUATION'),
        'PARTICLE MESH EWALD \(PME\)' : MetaInfoMap(startpage, defaultValue=None,
                                                    replaceTag='PARTICLE MESH EWALD'),
        'PME TOLERANCE'           : MetaInfoMap(startpage, defaultValue=None),
        'PME EWALD COEFFICIENT'   : MetaInfoMap(startpage, defaultValue=None),
        'PME INTERPOLATION ORDER' : MetaInfoMap(startpage, defaultValue=None),
        'PME GRID DIMENSIONS'     : MetaInfoMap(startpage, defaultValue=None, matchWith='EOL'),
        'PME MAXIMUM GRID SPACING' : MetaInfoMap(startpage, defaultValue=None),
        'Writing FFTW data to'    : MetaInfoMap(startpage, defaultValue=None,
                                                    replaceTag='FFTW data file'),
        'FULL ELECTROSTATIC EVALUATION FREQUENCY' : MetaInfoMap(startpage, defaultValue=None),
        'MINIMIZATION'            : MetaInfoMap(startpage, defaultValue=None),
        'VELOCITY QUENCHING'      : MetaInfoMap(startpage, defaultValue=None),
        'USING VERLET I \(r-RESPA\)' : MetaInfoMap(startpage, defaultValue='r-RESPA',
                replaceTag='VERLET INTEGRATOR', subFunc=lambda x: 'r-RESPA' if x is not None else None),
        'RANDOM NUMBER SEED'      : MetaInfoMap(startpage, defaultValue=None),
        'USE HYDROGEN BONDS?'     : MetaInfoMap(startpage, defaultValue=None,
                                                replaceTag='USE HYDROGEN BONDS'),
        'COORDINATE PDB'          : MetaInfoMap(startpage, defaultValue=None),
        'STRUCTURE FILE'          : MetaInfoMap(startpage, defaultValue=None),
        'PARAMETER file'          : MetaInfoMap(startpage, defaultValue=None, matchWith='EOL'),
        'Info: PARAMETERS'        : MetaInfoMap(startpage, defaultValue=None, addAsList=True,
                                                replaceTag='PARAMETERS'),
        }

    startpage.update({
        'metaNameTag'     : 'mdout',
        'activeSections'  : ['section_single_configuration_calculation']
        })
    mddatalist = {
        'WRITING COORDINATES TO DCD FILE' : MetaInfoMap(startpage,
            replaceTag='DCDSTEP', subFunc=lambda x: x.split()[-1].replace('\n','').strip()),
        'WRITING VELOCITIES TO DCD FILE AT STEP' : MetaInfoMap(startpage,
            replaceTag='VELSTEP', subFunc=lambda x: x.replace('\n','').strip()),
        'WRITING FORCES TO DCD FILE AT STEP' : MetaInfoMap(startpage,
            replaceTag='FORCESTEP', subFunc=lambda x: x.replace('\n','').strip()),
        'TS' : MetaInfoMap(startpage),
        'BOND' : MetaInfoMap(startpage),
        'ANGLE' : MetaInfoMap(startpage),
        'DIHED' : MetaInfoMap(startpage),
        'IMPRP' : MetaInfoMap(startpage),
        'ELECT' : MetaInfoMap(startpage),
        'VDW' : MetaInfoMap(startpage),
        'BOUNDARY' : MetaInfoMap(startpage),
        'MISC' : MetaInfoMap(startpage),
        'KINETIC' : MetaInfoMap(startpage),
        'TOTAL' : MetaInfoMap(startpage),
        'TEMP' : MetaInfoMap(startpage),
        'POTENTIAL' : MetaInfoMap(startpage),
        'TOTAL2' : MetaInfoMap(startpage),
        'TOTAL3' : MetaInfoMap(startpage),
        'TEMPAVG' : MetaInfoMap(startpage),
        'PRESSURE' : MetaInfoMap(startpage),
        'GPRESSURE' : MetaInfoMap(startpage),
        'VOLUME' : MetaInfoMap(startpage),
        'PRESSAVG' : MetaInfoMap(startpage),
        'GPRESSAVG' : MetaInfoMap(startpage),
        'Virial-Tensor' : MetaInfoMap(startpage),
        'Pressure-Tensor' : MetaInfoMap(startpage),
        'TIME' : MetaInfoMap(startpage),
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
    elif deflist == 'stepcontrol':
        namelist = stepcontrol
    else:
        namelist = cntrllist
    return MapDictionary(namelist)

def set_Dictionaries(self):
        self.unitDict = get_unitDict('si')
        self.fileDict = get_fileListDict()
        self.cntrlDict = get_nameListDict('cntrl')
        #self.parmDict = get_nameListDict('parm')
        self.mddataDict = get_nameListDict('mddata')
        self.extraDict = get_nameListDict('extra')
        self.mdoutHeaderDict = {}
        self.stepcontrolDict = {
            'logsteps'       : None,
            'nextlogsteps'   : None,
            'trajsteps'      : None,
            'velsteps'       : None,
            'forcesteps'     : None,
            'steps'          : None,
            'follow'         : None,
            'sectioncontrol' : None,
        }
        self.metaDicts = {
            'file'   : self.fileDict,
            'cntrl'  : self.cntrlDict,
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
        'ensemble_type' : MetaInfoMap(startpage, activeInfo=True,
            depends=[
                {'test' : [['minimization', ' is None'],
                           ['thermostat', ' in [\"tcouple\",'
                                          '\"rescale\",'
                                          '\"reassign\",'
                                          '\"andersen\",'
                                          '\"langevin\"]'],
                           ['barostat', ' in [\"berendsen\",'
                                         '\"langevin\"]']],
                 'assign' : 'NPT'},
                {'test' : [['minimization', ' is None'],
                           ['thermostat', ' in [\"langevin\"]'],
                           ['thermostat', ' not in [\"tcouple\",'
                                          '\"rescale\",'
                                          '\"reassign\",'
                                          '\"andersen\"]'],
                           ['barostat', ' is None']],
                 'assign' : 'Langevin'},
                {'test' : [['minimization', ' is None'],
                           ['thermostat', ' in [\"tcouple\",'
                                          '\"rescale\",'
                                          '\"reassign\",'
                                          '\"andersen\"]'],
                           ['barostat', ' is None']],
                 'assign' : 'NVT'},
                {'test' : [['minimization', ' is None'],
                           ['thermostat', ' is None'],
                           ['barostat', ' is None']],
                 'assign' : 'NVE'},
                {'test' : [['minimization', ' is not None']],
                 'assign' : 'minimization'},
                ],
            lookupdict=self.extraDict
            ),
        'sampling_method' : MetaInfoMap(startpage, activeInfo=True,
            depends=[
                {'test' : [['minimization', ' is not None']],
                 'assign' : 'geometry_optimization'},
                {'test' : [['minimization', ' is None']],
                 'assign' : 'molecular_dynamics'}
                ],
            lookupdict=self.extraDict
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
                {'test' : [['minimization', ' == \"cg\"']],
                 'assign' : 'CG'},
                {'test' : [['minimization', ' == \"quench\"']],
                 'assign' : 'Velocity Quenching'},
                ],
            lookupdict=self.extraDict,
            activeInfo=True,
            ),
#       'geometry_optimization_threshold_force' : MetaInfoMap(startpage),
        'x_namd_barostat_type' : MetaInfoMap(startpage,
            depends=[
                {'test' : [['minimization', ' is None'],
                           ['barostat', '== \"berendsen\"']],
                 'assign' : 'Berendsen'},
                {'test' : [['minimization', ' is None'],
                           ['barostat', '== \"langevin\"']],
                 'assign' : 'Nose-Hoover Langevin'}
                ],
            lookupdict=self.extraDict,
            #autoSections=True,
            activeInfo=True,
            activeSections=['settings_barostat']
            ),
        'x_namd_barostat_target_pressure' : MetaInfoMap(startpage,
            depends=[
                {'test' : [['TARGET PRESSURE', ' is not None']],
                 'value' : 'TARGET PRESSURE'}
                ],
            lookupdict=self.cntrlDict,
            valtype='float',
            unitdict=self.unitDict,
            unit='bar',
            #autoSections=True,
            activeInfo=True,
            activeSections=['settings_barostat']
            ),
        'x_namd_barostat_tau' : MetaInfoMap(startpage,
            depends=[
                {'test' : [['LANGEVIN OSCILLATION PERIOD', ' is not None']],
                 'value' : 'LANGEVIN OSCILLATION PERIOD'},
                {'test' : [['BERENDSEN RELAXATION TIME', ' is not None']],
                 'value' : 'BERENDSEN RELAXATION TIME'}
                ],
            lookupdict=self.cntrlDict,
            valtype='float',
            unitdict=self.unitDict,
            unit='femto-second',
            #autoSections=True,
            activeInfo=True,
            activeSections=['settings_barostat']
            ),
        'x_namd_integrator_type' : MetaInfoMap(startpage,
            depends=[
                {'test' : [['integrator', ' is not None']],
                 'value' : 'integrator'},
                {'test' : [['thermostat', ' == \"langevin\"']],
                 'assign' : 'Langevin'}
                ],
            lookupdict=self.extraDict,
            #autoSections=True,
            activeInfo=True,
            activeSections=['settings_integrator']
            ),
        'x_namd_integrator_dt' : MetaInfoMap(startpage,
            depends=[
                {'test' : [['MINIMIZATION', ' is None'],
                           ['VELOCITY QUENCHING', ' is None']],
                 'value' : 'TIMESTEP'},
                ],
            lookupdict=self.cntrlDict,
            valtype='float',
            unitdict=self.unitDict,
            unit='femto-second',
            #autoSections=True,
            activeInfo=True,
            activeSections=['settings_integrator']
            ),
        'x_namd_number_of_steps_requested' : MetaInfoMap(startpage,
            depends=[{'value' : 'NUMBER OF STEPS'}],
            lookupdict=self.cntrlDict,
            valtype='int',
            #autoSections=True,
            activeInfo=True,
            activeSections=['settings_integrator']
            ),
        'x_namd_thermostat_type' : MetaInfoMap(startpage,
            depends=[
                {'test' : [['minimization', ' is None'],
                           ['thermostat', ' == \"tcouple\"']],
                 'assign' : 'Berendsen'},
                {'test' : [['minimization', ' is None'],
                           ['thermostat', ' == \"rescale\"']],
                 'assign' : 'Velocity Rescaling'},
                {'test' : [['minimization', ' is None'],
                           ['thermostat', ' == \"reassign\"']],
                 'assign' : 'Velocity Reassigning'},
                {'test' : [['minimization', ' is None'],
                           ['thermostat', ' == \"andersen\"']],
                 'assign' : 'Andersen'},
                {'test' : [['minimization', ' is None'],
                           ['thermostat', ' == \"langevin\"']],
                 'assign' : 'Nose-Hoover Langevin'},
                ],
            lookupdict=self.extraDict,
            #autoSections=True,
            activeInfo=True,
            activeSections=['settings_thermostat']
            ),
        'x_namd_thermostat_target_temperature' : MetaInfoMap(startpage,
            depends=[
                {'test' : [['MINIMIZATION', ' is None'],
                           ['VELOCITY QUENCHING', ' is None'],
                           ['VELOCITY RESCALE TEMP', ' is not None']],
                 'value' : 'VELOCITY RESCALE TEMP'},
                {'test' : [['MINIMIZATION', ' is None'],
                           ['VELOCITY QUENCHING', ' is None'],
                           ['VELOCITY REASSIGNMENT TEMP', ' is not None']],
                 'value' : 'VELOCITY REASSIGNMENT TEMP'},
                {'test' : [['MINIMIZATION', ' is None'],
                           ['VELOCITY QUENCHING', ' is None'],
                           ['LOWE-ANDERSEN TEMPERATURE', ' is not None']],
                 'value' : 'LOWE-ANDERSEN TEMPERATURE'},
                {'test' : [['MINIMIZATION', ' is None'],
                           ['VELOCITY QUENCHING', ' is None'],
                           ['LANGEVIN TEMPERATURE', ' is not None']],
                 'value' : 'LANGEVIN TEMPERATURE'},
                {'test' : [['MINIMIZATION', ' is None'],
                           ['VELOCITY QUENCHING', ' is None'],
                           ['COUPLING TEMPERATURE', ' is not None']],
                 'value' : 'COUPLING TEMPERATURE'},
                ],
            lookupdict=self.cntrlDict,
            valtype='float',
            unitdict=self.unitDict,
            unit='kelvin',
            #autoSections=True,
            activeInfo=True,
            activeSections=['settings_thermostat']
            ),
        'x_namd_thermostat_tau' : MetaInfoMap(startpage,
            depends=[
                {'test' : [['MINIMIZATION', ' is None'],
                           ['VELOCITY QUENCHING', ' is None'],
                           ['VELOCITY RESCALE FREQ', ' is not None']],
                 'value' : 'VELOCITY RESCALE FREQ'},
                {'test' : [['MINIMIZATION', ' is None'],
                           ['VELOCITY QUENCHING', ' is None'],
                           ['VELOCITY REASSIGNMENT FREQ', ' is not None']],
                 'value' : 'VELOCITY REASSIGNMENT FREQ'},
                {'test' : [['MINIMIZATION', ' is None'],
                           ['VELOCITY QUENCHING', ' is None'],
                           ['LOWE-ANDERSEN RATE', ' is not None']],
                 'value' : 'LOWE-ANDERSEN RATE'},
                ],
            lookupdict=self.cntrlDict,
            valtype='float',
            unitdict=self.unitDict,
            unit='pico-second',
            #autoSections=True,
            activeInfo=True,
            activeSections=['settings_thermostat']
            ),
        'x_namd_periodicity_type' : MetaInfoMap(startpage,
            depends=[
                {'test' : [['PERIODIC CELL BASIS', ' is None']],
                 'assign' : 'no periodic boundaries'},
                {'test' : [['PERIODIC CELL BASIS', ' is not None']],
                 'assign' : 'periodic boundaries'}
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
        #'energy_current' : MetaInfoMap(startpage,
        #    depends=[{'value' : 'EPtot'}],
        #    lookupdict=self.mddataDict
        #    ),
        'energy_current' : MetaInfoMap(startpage),
        'energy_electrostatic' : MetaInfoMap(startpage,
            depends=[{'value' : 'ELECT'}],
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
            depends=[{'value' : 'POTENTIAL'}],
            valtype='float',
            unitdict=self.unitDict,
            unit='kilo-joule/mol',
            activeInfo=True,
            lookupdict=self.mddataDict
            ),
        'energy_total' : MetaInfoMap(startpage,
            depends=[{'value' : 'TOTAL'}],
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
        #'stress_tensor_kind' : MetaInfoMap(startpage,
        #    depends=[
        #        {'test' : [['minimization', ' is not None']],
        #         'assign' : 'geometry_optimization'},
        #        {'test' : [['minimization', ' is None']],
        #         'assign' : 'molecular_dynamics'}
        #        ],
        #    activeInfo=True,
        #    lookupdict=self.extraDict
        #    ),
        'stress_tensor_value' : MetaInfoMap(startpage)
        }

    # section_single_energy_van_der_Waals of section_single_configuration_calculation
    singlevdw = {
        'energy_van_der_Waals_value' : MetaInfoMap(startpage,
            depends=[{'value' : 'VDW'}],
            lookupdict=self.mddataDict,
            valtype='float',
            unitdict=self.unitDict,
            unit='kilo-joule/mol',
            #autoSections=True,
            activeSections=['section_energy_van_der_Waals']
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
            depends=[{'store' : 'TS'}],
            valtype='int',
            lookupdict=self.mddataDict
            ),
        'frame_sequence_kinetic_energy_stats' : MetaInfoMap(startpage),
        'frame_sequence_kinetic_energy' : MetaInfoMap(startpage,
            depends=[{'store' : 'KINETIC'}],
            valtype='float',
            unitdict=self.unitDict,
            unit='kilo-joule/mol',
            lookupdict=self.mddataDict
            ),
        'frame_sequence_local_frames_ref' : MetaInfoMap(startpage),
        'frame_sequence_potential_energy_frames' : MetaInfoMap(startpage,
            depends=[{'store' : 'TS'}],
            valtype='int',
            lookupdict=self.mddataDict
            ),
        'frame_sequence_potential_energy_stats' : MetaInfoMap(startpage),
        'frame_sequence_potential_energy' : MetaInfoMap(startpage,
            depends=[{'store' : 'POTENTIAL'}],
            valtype='float',
            unitdict=self.unitDict,
            unit='kilo-joule/mol',
            lookupdict=self.mddataDict
            ),
        'frame_sequence_pressure_average_frames' : MetaInfoMap(startpage,
            depends=[{'store' : 'TS'}],
            valtype='int',
            lookupdict=self.mddataDict
            ),
        'frame_sequence_pressure_average' : MetaInfoMap(startpage,
            depends=[{'store' : 'PRESSAVG'}],
            valtype='float',
            unitdict=self.unitDict,
            unit='bar',
            lookupdict=self.mddataDict
            ),
        'frame_sequence_pressure_frames' : MetaInfoMap(startpage,
            depends=[{'store' : 'TS'}],
            valtype='int',
            lookupdict=self.mddataDict
            ),
        'frame_sequence_pressure_stats' : MetaInfoMap(startpage),
        'frame_sequence_pressure' : MetaInfoMap(startpage,
            depends=[{'store' : 'PRESSURE'}],
            valtype='float',
            unitdict=self.unitDict,
            unit='bar',
            lookupdict=self.mddataDict
            ),
        'frame_sequence_temperature_average_frames' : MetaInfoMap(startpage,
            depends=[{'store' : 'TS'}],
            valtype='int',
            lookupdict=self.mddataDict
            ),
        'frame_sequence_temperature_average' : MetaInfoMap(startpage,
            depends=[{'store' : 'TEMPAVG'}],
            valtype='float',
            unitdict=self.unitDict,
            unit='Kelvin',
            lookupdict=self.mddataDict
            ),
        'frame_sequence_temperature_frames' : MetaInfoMap(startpage,
            depends=[{'store' : 'TS'}],
            valtype='int',
            lookupdict=self.mddataDict
            ),
        'frame_sequence_temperature_stats' : MetaInfoMap(startpage),
        'frame_sequence_temperature' : MetaInfoMap(startpage,
            depends=[{'store' : 'TEMP'}],
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
            lookupdict=self.mddataDict
            ),
        'x_namd_frame_sequence_volume_frames' : MetaInfoMap(startpage,
            activeSections=['section_frame_sequence'],
            depends=[{'store' : 'TS'}],
            valtype='int',
            lookupdict=self.mddataDict
            ),
        'x_namd_frame_sequence_volume' : MetaInfoMap(startpage,
            activeSections=['section_frame_sequence'],
            depends=[{'store' : 'VOLUME'}],
            valtype='float',
            unitdict=self.unitDict,
            unit='Angstrom**3',
            lookupdict=self.mddataDict
            ),
        'x_namd_frame_sequence_boundary_frames' : MetaInfoMap(startpage,
            activeSections=['section_frame_sequence'],
            depends=[{'store' : 'TS'}],
            valtype='int',
            lookupdict=self.mddataDict
            ),
        'x_namd_frame_sequence_boundary' : MetaInfoMap(startpage,
            activeSections=['section_frame_sequence'],
            depends=[{'store' : 'BOUNDARY'}],
            valtype='float',
            unitdict=self.unitDict,
            unit='kilo-joule/mol',
            lookupdict=self.mddataDict
            ),
        'x_namd_frame_sequence_bond_energy_frames' : MetaInfoMap(startpage,
            activeSections=['section_frame_sequence'],
            depends=[{'store' : 'TS'}],
            valtype='int',
            lookupdict=self.mddataDict
            ),
        'x_namd_frame_sequence_bond_energy' : MetaInfoMap(startpage,
            activeSections=['section_frame_sequence'],
            depends=[{'store' : 'BOND'}],
            valtype='float',
            unitdict=self.unitDict,
            unit='kilo-joule/mol',
            lookupdict=self.mddataDict
            ),
        'x_namd_frame_sequence_angle_energy_frames' : MetaInfoMap(startpage,
            activeSections=['section_frame_sequence'],
            depends=[{'store' : 'TS'}],
            valtype='int',
            lookupdict=self.mddataDict
            ),
        'x_namd_frame_sequence_angle_energy' : MetaInfoMap(startpage,
            activeSections=['section_frame_sequence'],
            depends=[{'store' : 'ANGLE'}],
            valtype='float',
            unitdict=self.unitDict,
            unit='kilo-joule/mol',
            lookupdict=self.mddataDict
            ),
        'x_namd_frame_sequence_proper_dihedral_energy_frames' : MetaInfoMap(startpage,
            activeSections=['section_frame_sequence'],
            depends=[{'store' : 'TS'}],
            valtype='int',
            lookupdict=self.mddataDict
            ),
        'x_namd_frame_sequence_proper_dihedral_energy' : MetaInfoMap(startpage,
            activeSections=['section_frame_sequence'],
            depends=[{'store' : 'DIHED'}],
            valtype='float',
            unitdict=self.unitDict,
            unit='kilo-joule/mol',
            lookupdict=self.mddataDict
            ),
        'x_namd_frame_sequence_improper_dihedral_energy_frames' : MetaInfoMap(startpage,
            activeSections=['section_frame_sequence'],
            depends=[{'store' : 'TS'}],
            valtype='int',
            lookupdict=self.mddataDict
            ),
        'x_namd_frame_sequence_improper_dihedral_energy' : MetaInfoMap(startpage,
            activeSections=['section_frame_sequence'],
            depends=[{'store' : 'IMPRP'}],
            valtype='float',
            unitdict=self.unitDict,
            unit='kilo-joule/mol',
            lookupdict=self.mddataDict
            ),
        'x_namd_frame_sequence_cmap_dihedral_energy_frames' : MetaInfoMap(startpage,
            activeSections=['section_frame_sequence'],
            depends=[{'store' : 'TS'}],
            valtype='int',
            lookupdict=self.mddataDict
            ),
        'x_namd_frame_sequence_cmap_dihedral_energy' : MetaInfoMap(startpage,
            activeSections=['section_frame_sequence'],
            depends=[{'store' : 'CMAP'}],
            valtype='float',
            unitdict=self.unitDict,
            unit='kilo-joule/mol',
            lookupdict=self.mddataDict
            ),
        'x_namd_frame_sequence_vdw_energy_frames' : MetaInfoMap(startpage,
            activeSections=['section_frame_sequence'],
            depends=[{'store' : 'TS'}],
            valtype='int',
            lookupdict=self.mddataDict
            ),
        'x_namd_frame_sequence_vdw_energy' : MetaInfoMap(startpage,
            activeSections=['section_frame_sequence'],
            depends=[{'store' : 'VDW'}],
            valtype='float',
            unitdict=self.unitDict,
            unit='kilo-joule/mol',
            lookupdict=self.mddataDict
            ),
        'x_namd_frame_sequence_electrostatic_energy_frames' : MetaInfoMap(startpage,
            activeSections=['section_frame_sequence'],
            depends=[{'store' : 'TS'}],
            valtype='int',
            lookupdict=self.mddataDict
            ),
        'x_namd_frame_sequence_electrostatic_energy' : MetaInfoMap(startpage,
            activeSections=['section_frame_sequence'],
            depends=[{'store' : 'ELECT'}],
            valtype='float',
            unitdict=self.unitDict,
            unit='kilo-joule/mol',
            lookupdict=self.mddataDict
            ),
        'x_namd_frame_sequence_total2_energy_frames' : MetaInfoMap(startpage,
            activeSections=['section_frame_sequence'],
            depends=[{'store' : 'TS'}],
            valtype='int',
            lookupdict=self.mddataDict
            ),
        'x_namd_frame_sequence_total2_energy' : MetaInfoMap(startpage,
            activeSections=['section_frame_sequence'],
            depends=[{'store' : 'TOTAL2'}],
            valtype='float',
            unitdict=self.unitDict,
            unit='kilo-joule/mol',
            lookupdict=self.mddataDict
            ),
        'x_namd_frame_sequence_total3_energy_frames' : MetaInfoMap(startpage,
            activeSections=['section_frame_sequence'],
            depends=[{'store' : 'TS'}],
            valtype='int',
            lookupdict=self.mddataDict
            ),
        'x_namd_frame_sequence_total3_energy' : MetaInfoMap(startpage,
            activeSections=['section_frame_sequence'],
            depends=[{'store' : 'TOTAL3'}],
            valtype='float',
            unitdict=self.unitDict,
            unit='kilo-joule/mol',
            lookupdict=self.mddataDict
            ),
        'x_namd_frame_sequence_misc_energy_frames' : MetaInfoMap(startpage,
            activeSections=['section_frame_sequence'],
            depends=[{'store' : 'TS'}],
            valtype='int',
            lookupdict=self.mddataDict
            ),
        'x_namd_frame_sequence_misc_energy' : MetaInfoMap(startpage,
            activeSections=['section_frame_sequence'],
            depends=[{'store' : 'MISC'}],
            valtype='float',
            unitdict=self.unitDict,
            unit='kilo-joule/mol',
            lookupdict=self.mddataDict
            ),
        #'frame_sequence_to_sampling_ref' : MetaInfoMap(startpage),
        'geometry_optimization_converged' : MetaInfoMap(startpage,
            value=self.minConverged
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
        'x_namd_number_of_volumes_in_sequence' : MetaInfoMap(startpage,
            activeInfo=True,
            activeSections=['section_frame_sequence'],
            value=(lambda x: np.array(x['val']).flatten().shape[0] if(
                x is not None and x['val'] is not None) else None)(
                self.metaStorage.fetchAttrValue(
                    'x_namd_frame_sequence_volume_frames'
                    )
                )
            ),
        'x_namd_number_of_boundary_energies_in_sequence' : MetaInfoMap(startpage,
            activeInfo=True,
            activeSections=['section_frame_sequence'],
            value=(lambda x: np.array(x['val']).flatten().shape[0] if(
                x is not None and x['val'] is not None) else None)(
                self.metaStorage.fetchAttrValue(
                    'x_namd_frame_sequence_boundary_frames'
                    )
                )
            ),
        'x_namd_number_of_bond_energies_in_sequence' : MetaInfoMap(startpage,
            activeInfo=True,
            activeSections=['section_frame_sequence'],
            value=(lambda x: np.array(x['val']).flatten().shape[0] if(
                x is not None and x['val'] is not None) else None)(
                self.metaStorage.fetchAttrValue(
                    'x_namd_frame_sequence_bond_energy_frames'
                    )
                )
            ),
        'x_namd_number_of_angle_energies_in_sequence' : MetaInfoMap(startpage,
            activeInfo=True,
            activeSections=['section_frame_sequence'],
            value=(lambda x: np.array(x['val']).flatten().shape[0] if(
                x is not None and x['val'] is not None) else None)(
                self.metaStorage.fetchAttrValue(
                    'x_namd_frame_sequence_angle_energy_frames'
                    )
                )
            ),
        'x_namd_number_of_electrostatic_energies_in_sequence' : MetaInfoMap(startpage,
            activeInfo=True,
            activeSections=['section_frame_sequence'],
            value=(lambda x: np.array(x['val']).flatten().shape[0] if(
                x is not None and x['val'] is not None) else None)(
                self.metaStorage.fetchAttrValue(
                    'x_namd_frame_sequence_electrostatic_energy_frames'
                    )
                )
            ),
        'x_namd_number_of_vdw_energies_in_sequence' : MetaInfoMap(startpage,
            activeInfo=True,
            activeSections=['section_frame_sequence'],
            value=(lambda x: np.array(x['val']).flatten().shape[0] if(
                x is not None and x['val'] is not None) else None)(
                self.metaStorage.fetchAttrValue(
                    'x_namd_frame_sequence_vdw_energy_frames'
                    )
                )
            ),
        'x_namd_number_of_total2_energies_in_sequence' : MetaInfoMap(startpage,
            activeInfo=True,
            activeSections=['section_frame_sequence'],
            value=(lambda x: np.array(x['val']).flatten().shape[0] if(
                x is not None and x['val'] is not None) else None)(
                self.metaStorage.fetchAttrValue(
                    'x_namd_frame_sequence_total2_energy_frames'
                    )
                )
            ),
        'x_namd_number_of_total3_energies_in_sequence' : MetaInfoMap(startpage,
            activeInfo=True,
            activeSections=['section_frame_sequence'],
            value=(lambda x: np.array(x['val']).flatten().shape[0] if(
                x is not None and x['val'] is not None) else None)(
                self.metaStorage.fetchAttrValue(
                    'x_namd_frame_sequence_total3_energy_frames'
                    )
                )
            ),
        'x_namd_number_of_proper_dihedral_energies_in_sequence' : MetaInfoMap(startpage,
            activeInfo=True,
            activeSections=['section_frame_sequence'],
            value=(lambda x: np.array(x['val']).flatten().shape[0] if(
                x is not None and x['val'] is not None) else None)(
                self.metaStorage.fetchAttrValue(
                    'x_namd_frame_sequence_proper_dihedral_energy_frames'
                    )
                )
            ),
        'x_namd_number_of_improper_dihedral_energies_in_sequence' : MetaInfoMap(startpage,
            activeInfo=True,
            activeSections=['section_frame_sequence'],
            value=(lambda x: np.array(x['val']).flatten().shape[0] if(
                x is not None and x['val'] is not None) else None)(
                self.metaStorage.fetchAttrValue(
                    'x_namd_frame_sequence_improper_dihedral_energy_frames'
                    )
                )
            ),
        'x_namd_number_of_cmap_dihedral_energies_in_sequence' : MetaInfoMap(startpage,
            activeInfo=True,
            activeSections=['section_frame_sequence'],
            value=(lambda x: np.array(x['val']).flatten().shape[0] if(
                x is not None and x['val'] is not None) else None)(
                self.metaStorage.fetchAttrValue(
                    'x_namd_frame_sequence_cmap_dihedral_energy_frames'
                    )
                )
            ),
        'x_namd_number_of_misc_energies_in_sequence' : MetaInfoMap(startpage,
            activeInfo=True,
            activeSections=['section_frame_sequence'],
            value=(lambda x: np.array(x['val']).flatten().shape[0] if(
                x is not None and x['val'] is not None) else None)(
                self.metaStorage.fetchAttrValue(
                    'x_namd_frame_sequence_misc_energy_frames'
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


