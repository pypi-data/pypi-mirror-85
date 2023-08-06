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

from builtins import range
from builtins import object
import numpy as np
import nomadcore.ActivateLogging
from nomadcore.caching_backend import CachingLevel
from nomadcore.simple_parser import mainFunction
from nomadcore.simple_parser import SimpleMatcher as SM
from nomadcore.local_meta_info import loadJsonFile, InfoKindEl
from .OnetepCommon import get_metaInfo
import logging, os, re, sys



############################################################
# This is the parser for the *.md file of Onetep.
############################################################

logger = logging.getLogger("nomad.OnetepTSParser")

class OnetepTSParserContext(object):
    """Context for parsing Onetep *.md file.


    The onClose_ functions allow processing and writing of cached values after a section is closed.
    They take the following arguments:
        backend: Class that takes care of wrting and caching of metadata.
        gIndex: Index of the section that is closed.
        section: The cached values and sections that were found in the section that is closed.
    """
    def __init__(self, writeMetaData = True):
        """Args:
            writeMetaData: Deteremines if metadata is written or stored in class attributes.
        """
        self.writeMetaData = writeMetaData

        self.total_energy = []
        self.total_energy_final = []
        self.total_energy_pro = []

        self.md_forces =[]
        self.md_veloc =[]
        self.frame_atom_label =[]

        self.total_forces =[]
        self.atom_label = []
        self.frame_stress_tensor =[]
        self.total_positions =[]
        self.frame_cell=[]
        self.frame_cell_final=[]
        self.vector_velocities=[]
        self.frame_time =[]
        self.path_ts = []
        self.path_final = []
        self.path_pro = []
        self.total_positions_final=[]
        self.total_positions_pro=[]
    def startedParsing(self, fInName, parser):
        """Function is called when the parsing starts and the compiled parser is obtained.

        Args:
            fInName: The file name on which the current parser is running.
            parser: The compiled parser. Is an object of the class SimpleParser in nomadcore.simple_parser.py.
        """
        self.parser = parser

    def onClose_x_onetep_section_ts_store(self, backend, gIndex, section):


        vet = section ['x_onetep_ts_cell_vectors_store']
        forces_ts = section ['x_onetep_ts_forces_store']

        position = section ['x_onetep_ts_positions_store']
        energy = section['x_onetep_ts_energy']
        # path_step = section ['x_Onetep_ts_path']

        # for i in range (len(path_step)):
        #     self.path_ts.append(path_step[i])
        bohr_to_m = float(5.29177211e-11)
        Hr_J_converter = float(4.35974e-18)
        HrK_to_K_coverter= float(3.1668114e-6)
        hrang_to_N = float(4.359745e-8)
        for i in energy:

            energy = [x * Hr_J_converter for x in energy]
            self.total_energy.extend(energy)


        if vet:
            self.cell =[]
            for i in range(len(vet)):
                vet[i] = vet[i].split()
                vet[i] = [float(j) for j in vet[i]]
                vet_list = vet[i]
                vet_list = [x * bohr_to_m for x in vet_list]
                self.cell.append(vet_list)
            self.frame_cell.append(self.cell)


        if position:
            self.at_nr = len(position)
            self.atom_position=[]
            for i in range(0, self.at_nr):
                position[i] = position[i].split()
                position[i] = [float(j) for j in position[i]]
                pos_list = position[i]
                pos_list = [x * bohr_to_m  for x in pos_list]
                self.atom_position.append(pos_list)
            self.total_positions.append(self.atom_position)

        if forces_ts is not None:

            self.ts_forces = []
            for f in forces_ts:
                f = f.split()
                f = [float(k) for k in f]
                f_st_intts = f
                f_st_intts = [x * hrang_to_N for x in f_st_intts]
                self.ts_forces.append(f_st_intts)
            self.total_forces.append(self.ts_forces)

    def onClose_x_onetep_section_ts_final_store(self, backend, gIndex, section):
        # path_final_ts = section ['x_Onetep_ts_path_ts_final']
        vet_final = section ['x_onetep_ts_cell_vectors_final_store']
        forces_final = section ['x_onetep_ts_forces_final_store']

        position_final = section ['x_onetep_ts_positions_final_store']
        energy_final = section['x_onetep_ts_energy_final_store']

        # for i in range (len(path_final_ts)):
        #     self.path_final = path_final_ts[i]
        bohr_to_m = float(5.29177211e-11)
        Hr_J_converter = float(4.35974e-18)
        HrK_to_K_coverter= float(3.1668114e-6)

        hrang_to_N = float(4.359745e-8)

        self.total_energy_final = Hr_J_converter * energy_final[0]
        # self.total_energy_final = energy_final


        if vet_final:
            self.cell_final =[]
            for i in range(len(vet_final)):
                vet_final[i] = vet_final[i].split()
                vet_final[i] = [float(j) for j in vet_final[i]]
                vetf_list = vet_final[i]
                vetf_list = [x * bohr_to_m for x in vetf_list]
                self.cell_final.append(vetf_list)
        # self.frame_cell_final.append(self.cell_final)


        if position_final:
            self.at_nr = len(position_final)
            self.atomf_position=[]
            for i in range(0, self.at_nr):
                position_final[i] = position_final[i].split()
                position_final[i] = [float(j) for j in position_final[i]]
                posf_list = position_final[i]
                posf_list = [x * bohr_to_m for x in posf_list]
                self.atomf_position.append(posf_list)
            # self.total_positions_final.append(self.atomf_position)

        if forces_final is not None:

            self.md_forces_final = []
            for f in forces_final:
                f = f.split()
                f = [float(k) for k in f]
                f_st_intf = f
                f_st_intf = [x * hrang_to_N for x in f_st_intf]
                self.md_forces_final.append(f_st_intf)

            # self.total_forces_final.append(self.md_forces_final)

    def onClose_x_onetep_section_ts_product_store(self, backend, gIndex, section):
         # path_product = section ['x_Onetep_ts_path_product']
        vet_pro = section ['x_onetep_ts_cell_vectors_pro_store']
        forces_pro = section ['x_onetep_ts_forces_pro_store']

        position_pro = section ['x_onetep_ts_positions_pro_store']
        energy_pro = section['x_onetep_ts_energy_product_store']

        bohr_to_m = float(5.29177211e-11)
        Hr_J_converter = float(4.35974e-18)
        HrK_to_K_coverter= float(3.1668114e-6)
        hrang_to_N = float(4.359745e-8)
        # for i in range (len(path_product)):
        #     self.path_pro = path_product[i]



        self.total_energy_pro = energy_pro[0] * Hr_J_converter


        if vet_pro:
            self.cell_pro =[]
            for i in range(len(vet_pro)):
                vet_pro[i] = vet_pro[i].split()
                vet_pro[i] = [float(j) for j in vet_pro[i]]
                vetp_list = vet_pro[i]
                vetp_list = [x * bohr_to_m for x in vetp_list]
                self.cell_pro.append(vetp_list)
        # self.frame_cell_final.append(self.cell_final)


        if position_pro:
            self.at_nr = len(position_pro)
            self.atomp_position=[]
            for i in range(0, self.at_nr):
                position_pro[i] = position_pro[i].split()
                position_pro[i] = [float(j) for j in position_pro[i]]
                posp_list = position_pro[i]
                posp_list = [x * bohr_to_m for x in posp_list]
                self.atomp_position.append(posp_list)
            # self.total_positions_final.append(self.atomf_position)

        if forces_pro is not None:

            self.md_forces_pro = []
            for f in forces_pro:
                f = f.split()
                f = [float(k) for k in f]
                f_st_intp = f
                f_st_intp = [x * hrang_to_N for x in f_st_intp]
                self.md_forces_pro.append(f_st_intp)

    def onClose_section_run(self, backend, gIndex, section):
        path_product = section ['x_onetep_ts_path_product']
        path_final_ts = section ['x_onetep_ts_path_ts_final']
        path_step = section ['x_onetep_ts_path']
        if path_step:
            for i in range (len(path_step)):
                self.path_ts.append(path_step[i])
        if path_product:
            for i in range (len(path_product)):
                self.path_pro = path_product[i]
        if path_final_ts:
            for i in range (len(path_final_ts)):
                self.path_final = path_final_ts[i]

def build_OnetepTSFileSimpleMatcher():
    """Builds the SimpleMatcher to parse the *.md file of Onetep.

    SimpleMatchers are called with 'SM (' as this string has length 4,
    which allows nice formating of nested SimpleMatchers in python.

    Returns:
       SimpleMatcher that parses *.md file of Onetep.
    """
    return SM (name = 'Root1',
        startReStr = "",
        sections = ['section_run'],
        forwardMatch = True,
        weak = True,
        subMatchers = [
            SM (name = 'Root2',
            startReStr =r"\sLST\s*[0-9.]\s*(?P<x_onetep_ts_path>[-+0-9.eEdD]+)\s*",
            endReStr ="/n",
            sections = ['x_onetep_section_ts_store'],
            repeats = True,
            subMatchers = [
                SM (r"\s*(?P<x_onetep_ts_energy>[-+0-9.eEdD]+)\s*[-+0-9.eEdD]+\s*\<\-\-\sE\s*"),
                SM (r"\s*(?P<x_onetep_ts_cell_vectors_store>[-+0-9.eEdD]+\s*[-+0-9.eEdD]+\s*[-+0-9.eEdD]+)\s*\<\-\-\sh\s",repeats = True),
                SM(r"\s*[A-Za-z]+\s*[0-9.]+\s*(?P<x_onetep_ts_positions_store>[-+0-9.eEdD]+\s*[-+0-9.eEdD]+\s*[-+0-9.eEdD]+)\s*\<\-\-\sR\s*",repeats = True),
                SM(r"\s*[A-Za-z]+\s*[0-9.]+\s*(?P<x_onetep_ts_forces_store>[-+0-9.eEdD]+\s*[-+0-9.eEdD]+\s*[-+0-9.eEdD]+)\s*\<\-\-\sF\s*",repeats = True,endReStr ="/n"),

                   ]),
            SM (name = 'Root3',
            startReStr =r"\sQST\s*[0-9.]\s*(?P<x_onetep_ts_path>[-+0-9.eEdD]+)\s*",
            endReStr ="/n",
            sections = ['x_onetep_section_ts_store'],
            repeats = True,
            subMatchers = [
                SM (r"\s*(?P<x_onetep_ts_energy>[-+0-9.eEdD]+)\s*[-+0-9.eEdD]+\s*\<\-\-\sE\s*"),
                SM (r"\s*(?P<x_onetep_ts_cell_vectors_store>[-+0-9.eEdD]+\s*[-+0-9.eEdD]+\s*[-+0-9.eEdD]+)\s*\<\-\-\sh\s",repeats = True),
                SM(r"\s*[A-Za-z]+\s*[0-9.]+\s*(?P<x_onetep_ts_positions_store>[-+0-9.eEdD]+\s*[-+0-9.eEdD]+\s*[-+0-9.eEdD]+)\s*\<\-\-\sR\s*",repeats = True),
                SM(r"\s*[A-Za-z]+\s*[0-9.]+\s*(?P<x_onetep_ts_forces_store>[-+0-9.eEdD]+\s*[-+0-9.eEdD]+\s*[-+0-9.eEdD]+)\s*\<\-\-\sF\s*",repeats = True,endReStr ="/n"),

                   ]),
            SM (name = 'Root4',
                startReStr =r"\sTS\s*0\s*(?P<x_onetep_ts_path_ts_final>[-+0-9.eEdD]+)\s*",
                endReStr ="/n",
                sections = ['x_onetep_section_ts_final_store'],
                repeats = True,
                subMatchers = [
                            SM (r"\s*(?P<x_onetep_ts_energy_final_store>[-+0-9.eEdD]+)\s*[-+0-9.eEdD]+\s*\<\-\-\sE\s*"),
                            SM (r"\s*(?P<x_onetep_ts_cell_vectors_final_store>[-+0-9.eEdD]+\s*[-+0-9.eEdD]+\s*[-+0-9.eEdD]+)\s*\<\-\-\sh\s",repeats = True),
                            SM(r"\s*[A-Za-z]+\s*[0-9.]+\s*(?P<x_onetep_ts_positions_final_store>[-+0-9.eEdD]+\s*[-+0-9.eEdD]+\s*[-+0-9.eEdD]+)\s*\<\-\-\sR\s*",repeats = True),
                            SM(r"\s*[A-Za-z]+\s*[0-9.]+\s*(?P<x_onetep_ts_forces_final_store>[-+0-9.eEdD]+\s*[-+0-9.eEdD]+\s*[-+0-9.eEdD]+)\s*\<\-\-\sF\s*",repeats = True,endReStr ="/n"),
                    ]),
            SM (name = 'Root5',
                startReStr =r"\sPRO\s*0\s*(?P<x_onetep_ts_path_product>[-+0-9.eEdD]+)\s*",
                endReStr ="/n",
                sections = ['x_onetep_section_ts_product_store'],
                repeats = True,
                subMatchers = [
                            SM (r"\s*(?P<x_onetep_ts_energy_product_store>[-+0-9.eEdD]+)\s*[-+0-9.eEdD]+\s*\<\-\-\sE\s*"),
                            SM (r"\s*(?P<x_onetep_ts_cell_vectors_pro_store>[-+0-9.eEdD]+\s*[-+0-9.eEdD]+\s*[-+0-9.eEdD]+)\s*\<\-\-\sh\s",repeats = True),
                            SM(r"\s*[A-Za-z]+\s*[0-9.]+\s*(?P<x_onetep_ts_positions_pro_store>[-+0-9.eEdD]+\s*[-+0-9.eEdD]+\s*[-+0-9.eEdD]+)\s*\<\-\-\sR\s*",repeats = True),
                            SM(r"\s*[A-Za-z]+\s*[0-9.]+\s*(?P<x_onetep_ts_forces_pro_store>[-+0-9.eEdD]+\s*[-+0-9.eEdD]+\s*[-+0-9.eEdD]+)\s*\<\-\-\sF\s*",repeats = True,endReStr ="/n"),
                    ]),

            ])





def get_cachingLevelForMetaName(metaInfoEnv, CachingLvl):
    """Sets the caching level for the metadata.

    Args:
        metaInfoEnv: metadata which is an object of the class InfoKindEnv in nomadcore.local_meta_info.py.
        CachingLvl: Sets the CachingLevel for the sections k_band, run, and single_configuration_calculation.
            This allows to run the parser without opening new sections.

    Returns:
        Dictionary with metaname as key and caching level as value.
    """
    # manually adjust caching of metadata
    cachingLevelForMetaName = {
                                 'section_run': CachingLvl,
                                 # 'x_onetep_section_ts_store': CachingLvl,
                                 # 'x_onetep_section_ts_final_store': CachingLvl,
                                 # 'x_onetep_section_ts_product_store': CachingLvl,
                              }
    # Set all band metadata to Cache as they need post-processsing.
    for name in metaInfoEnv.infoKinds:
        if name.startswith('x_onetep_'):
            cachingLevelForMetaName[name] = CachingLevel.Cache
    return cachingLevelForMetaName


def main(CachingLvl):
    """Main function.

    Set up everything for the parsing of the Onetep *.cell file and run the parsing.

    Args:
        CachingLvl: Sets the CachingLevel for the sections k_band, run, and single_configuration_calculation.
            This allows to run the parser without opening new sections.
    """
    # get band.out file description
    OnetepTSFileSimpleMatcher = build_OnetepTSFileSimpleMatcher()
    # loading metadata from nomad-meta-info/meta_info/nomad_meta_info/Onetep.nomadmetainfo.json
    metaInfoPath = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)),"../../../../nomad-meta-info/meta_info/nomad_meta_info/onetep.nomadmetainfo.json"))
    metaInfoEnv = get_metaInfo(metaInfoPath)
    # set parser info
    parserInfo = {'name':'Onetep-ts-parser', 'version': '1.0'}
    # get caching level for metadata
    cachingLevelForMetaName = get_cachingLevelForMetaName(metaInfoEnv, CachingLvl)
    # start parsing
    mainFunction(mainFileDescription = OnetepTSFileSimpleMatcher,
                 metaInfoEnv = metaInfoEnv,
                 parserInfo = parserInfo,
                 cachingLevelForMetaName = cachingLevelForMetaName,
                 superContext = OnetepTSParserContext())

if __name__ == "__main__":
    main(CachingLevel.Forward)
