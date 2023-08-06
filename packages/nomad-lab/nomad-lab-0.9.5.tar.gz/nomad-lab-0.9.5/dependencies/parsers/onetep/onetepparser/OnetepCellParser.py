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
# This is the parser for the *.cell file of Onetep.
############################################################

logger = logging.getLogger("nomad.OnetepCellParser")

class OnetepCellParserContext(object):
    """Context for parsing Onetep *.cell file.


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
        self.cell_store = []
        self.at_nr = []
        self.onetep_atom_positions_store=[]
        self.atom_labels_store=[]

    def startedParsing(self, fInName, parser):
        """Function is called when the parsing starts and the compiled parser is obtained.

        Args:
            fInName: The file name on which the current parser is running.
            parser: The compiled parser. Is an object of the class SimpleParser in nomadcore.simple_parser.py.
        """
        self.parser = parser

        # get unit from metadata for band energies
        # allows to reset values if the same superContext is used to parse different files
        # self.band_energies = None
        # self.band_k_points = None
        # self.band_occupations = None

        # self.k_crd = []
        # self.k_sgt_start_end = []
    def onClose_x_onetep_section_cell(self, backend, gIndex, section):
        """trigger called when _onetep_section_cell is closed"""
        # get cached values for onetep_cell_vector
        units = section['x_onetep_units']
        vet = section['x_onetep_cell_vector']
        bohr_to_m = float(5.29177211e-11)
        ang_to_m = float(1e-10)
        if units:
            if units[0] == 'bohr':
                vet[0] = vet[0].split()
                vet[0] = [float(i) for i in vet[0]]
                vet[0]= [i * bohr_to_m for i in vet[0]]
                vet[1] = vet[1].split()
                vet[1] = [float(i) for i in vet[1]]
                vet[1]= [i * bohr_to_m for i in vet[1]]
                vet[2] = vet[2].split()
                vet[2] = [float(i) for i in vet[2]]
                vet[2]= [i * bohr_to_m for i in vet[2]]
                self.cell_store.append(vet[0])
                self.cell_store.append(vet[1])
                self.cell_store.append(vet[2]) # Reconstructing the unit cell vector by vector
            elif units[0] == 'ang':
                vet[0] = vet[0].split()
                vet[0] = [float(i) for i in vet[0]]
                vet[0]= [i * ang_to_m for i in vet[0]]
                vet[1] = vet[1].split()
                vet[1] = [float(i) for i in vet[1]]
                vet[1]= [i * ang_to_m for i in vet[1]]
                vet[2] = vet[2].split()
                vet[2] = [float(i) for i in vet[2]]
                vet[2]= [i * ang_to_m for i in vet[2]]
                self.cell_store.append(vet[0])
                self.cell_store.append(vet[1])
                self.cell_store.append(vet[2]) # Reconstructing t
        else:
            vet[0] = vet[0].split()
            vet[0] = [float(i) for i in vet[0]]
            vet[0]= [i * bohr_to_m for i in vet[0]]
            vet[1] = vet[1].split()
            vet[1] = [float(i) for i in vet[1]]
            vet[1]= [i * bohr_to_m for i in vet[1]]
            vet[2] = vet[2].split()
            vet[2] = [float(i) for i in vet[2]]
            vet[2]= [i * bohr_to_m for i in vet[2]]
            self.cell_store.append(vet[0])
            self.cell_store.append(vet[1])
            self.cell_store.append(vet[2]) # Reco

    def onClose_section_system(self, backend, gIndex, section):
        unitsap = section['x_onetep_units_atom_position']
        pos = section['x_onetep_store_atom_positions']

        bohr_to_m = float(5.29177211e-11)
        ang_to_m = float(1e-10)
        if unitsap is not None:
            if unitsap[0] == 'bohr':

                pos = section['x_onetep_store_atom_positions']

                if pos:
                    self.at_nr = len(pos)
                    for i in range(0, self.at_nr):
                        pos[i] = pos[i].split()
                        pos[i] = [float(j) for j in pos[i]]
                        pos[i]= [ii * bohr_to_m for ii in pos[i]]
                        self.onetep_atom_positions_store.append(pos[i])

            elif unitsap[0] == 'ang':
                pos = section['x_onetep_store_atom_positions']

                if pos:
                    self.at_nr = len(pos)
                    for i in range(0, self.at_nr):
                        pos[i] = pos[i].split()
                        pos[i] = [float(j) for j in pos[i]]
                        pos[i]= [ii * ang_to_m for ii in pos[i]]

                        self.onetep_atom_positions_store.append(pos[i])
            else:
                pass





        if pos:
            bohr_to_m = float(5.29177211e-11)
            self.at_nr = len(pos)
            for i in range(0, self.at_nr):
                pos[i] = pos[i].split()
                pos[i] = [float(j) for j in pos[i]]
                pos[i]= [ii * bohr_to_m for ii in pos[i]]
                self.onetep_atom_positions_store.append(pos[i])
        #get cached values of onetep_store_atom_labels

        lab = section['x_onetep_store_atom_labels']

        for i in range(0, len(lab)):
            lab[i] = re.sub('\s+', ' ', lab[i]).strip()
        self.atom_labels_store.extend(lab)



def build_OnetepCellFileSimpleMatcher():
    """Builds the SimpleMatcher to parse the *.cell file of Onetep.

    SimpleMatchers are called with 'SM (' as this string has length 4,
    which allows nice formating of nested SimpleMatchers in python.

    Returns:
       SimpleMatcher that parses *.cell file of Onetep.
    """

    return SM(name = "systemDescription",
                startReStr = "",
                forwardMatch = True,
                sections = ["section_system"],
                subMatchers = [

           # cell information
                    SM(name = 'cellInformation',
                        startReStr = r"\%block\slattice\_cart\s*",
                        # forwardMatch = True,
                        sections = ["x_onetep_section_cell"],
                            subMatchers = [
                                SM(r"(?P<x_onetep_units>[A-Za-z]+)"),
                                SM(r"\s*(?P<x_onetep_cell_vector>[-+0-9.eEdD]+\s+[-+0-9.eEdD]+\s+[-+0-9.eEd]+)",
                     #SM(r"\s*(?P<onetep_cell_vector>[\d\.]+\s+[\d\.]+\s+[\d\.]+) \s*[-+0-9.eEdD]*\s*[-+0-9.eEdD]*\s*[-+0-9.eEdD]*",
                        # endReStr = "\%endblock\s*lattice\_cart\s*",
                                repeats = True),

                            ]), # CLOSING onetep_section_cell
                    SM(name = 'cellInformation',
                        startReStr = r"\s*\%block\slattice\_cart\s*",
                        # forwardMatch = True,
                        sections = ["x_onetep_section_cell"],
                            subMatchers = [
                                SM(r"(?P<x_onetep_units>[A-Za-z]+)"),
                                SM(r"\s*(?P<x_onetep_cell_vector>[-+0-9.eEdD]+\s+[-+0-9.eEdD]+\s+[-+0-9.eEd]+)",
                     #SM(r"\s*(?P<onetep_cell_vector>[\d\.]+\s+[\d\.]+\s+[\d\.]+) \s*[-+0-9.eEdD]*\s*[-+0-9.eEdD]*\s*[-+0-9.eEdD]*",
                        # endReStr = "\%endblock\s*lattice\_cart\s*",
                                repeats = True),

                            ]), # CLOSING onetep_section_cell
                    SM(name = 'cellInformation',
                        startReStr = r"\%block\s*lattice\_cart\s*",
                        # forwardMatch = True,
                        sections = ["x_onetep_section_cell"],
                            subMatchers = [
                                SM(r"(?P<x_onetep_units>[A-Za-z]+)"),
                                SM(r"\s*(?P<x_onetep_cell_vector>[-+0-9.eEdD]+\s+[-+0-9.eEdD]+\s+[-+0-9.eEd]+)",
                     #SM(r"\s*(?P<onetep_cell_vector>[\d\.]+\s+[\d\.]+\s+[\d\.]+) \s*[-+0-9.eEdD]*\s*[-+0-9.eEdD]*\s*[-+0-9.eEdD]*",
                        # endReStr = "\%endblock\s*lattice\_cart\s*",
                                repeats = True),

                            ]), # CLOSING onet
                    SM(name = 'cellInformation',
                        startReStr = r"\s*\%block\s*lattice\_cart\s*",
                        # forwardMatch = True,
                        sections = ["x_onetep_section_cell"],
                            subMatchers = [
                                SM(r"(?P<x_onetep_units>[A-Za-z]+)"),
                                SM(r"\s*(?P<x_onetep_cell_vector>[-+0-9.eEdD]+\s+[-+0-9.eEdD]+\s+[-+0-9.eEd]+)",
                     #SM(r"\s*(?P<onetep_cell_vector>[\d\.]+\s+[\d\.]+\s+[\d\.]+) \s*[-+0-9.eEdD]*\s*[-+0-9.eEdD]*\s*[-+0-9.eEdD]*",
                        # endReStr = "\%endblock\s*lattice\_cart\s*",
                                repeats = True),

                            ]), # CLOSING onet

                    SM(name = 'cellInformation',
                        startReStr = r"\%BLOCK\sLATTICE\_CART\s*",
                        # forwardMatch = True,
                        sections = ["x_onetep_section_cell"],
                            subMatchers = [
                                SM(r"(?P<x_onetep_units>[A-Za-z]+)"),
                                SM(r"\s*(?P<x_onetep_cell_vector>[-+0-9.eEdD]+\s+[-+0-9.eEdD]+\s+[-+0-9.eEd]+)",
                     #SM(r"\s*(?P<onetep_cell_vector>[\d\.]+\s+[\d\.]+\s+[\d\.]+) \s*[-+0-9.eEdD]*\s*[-+0-9.eEdD]*\s*[-+0-9.eEdD]*",
                        # endReStr = "\%endblock\s*lattice\_cart\s*",
                                repeats = True),

                            ]), # CLOSING onetep_section_cell
                    SM(name = 'cellInformation',
                        startReStr = r"\s*\%BLOCK\sLATTICE\_CART\s*",
                        # forwardMatch = True,
                        sections = ["x_onetep_section_cell"],
                            subMatchers = [
                                SM(r"(?P<x_onetep_units>[A-Za-z]+)"),
                                SM(r"\s*(?P<x_onetep_cell_vector>[-+0-9.eEdD]+\s+[-+0-9.eEdD]+\s+[-+0-9.eEd]+)",
                     #SM(r"\s*(?P<onetep_cell_vector>[\d\.]+\s+[\d\.]+\s+[\d\.]+) \s*[-+0-9.eEdD]*\s*[-+0-9.eEdD]*\s*[-+0-9.eEdD]*",
                        # endReStr = "\%endblock\s*lattice\_cart\s*",
                                repeats = True),

                            ]), # CLOSING onetep_section_cell
                    SM(name = 'cellInformation',
                        startReStr = r"\%BLOCK\s*LATTICE\_CART\s*",
                        # forwardMatch = True,
                        sections = ["x_onetep_section_cell"],
                            subMatchers = [
                                SM(r"(?P<x_onetep_units>[A-Za-z]+)"),
                                SM(r"\s*(?P<x_onetep_cell_vector>[-+0-9.eEdD]+\s+[-+0-9.eEdD]+\s+[-+0-9.eEd]+)",
                     #SM(r"\s*(?P<onetep_cell_vector>[\d\.]+\s+[\d\.]+\s+[\d\.]+) \s*[-+0-9.eEdD]*\s*[-+0-9.eEdD]*\s*[-+0-9.eEdD]*",
                        # endReStr = "\%endblock\s*lattice\_cart\s*",
                                repeats = True),

                            ]), # CLOSING onet
                    SM(name = 'cellInformation',
                        startReStr = r"\s*\%BLOCK\s*LATTICE\_CART\s*",
                        # forwardMatch = True,
                        sections = ["x_onetep_section_cell"],
                            subMatchers = [
                                SM(r"(?P<x_onetep_units>[A-Za-z]+)"),
                                SM(r"\s*(?P<x_onetep_cell_vector>[-+0-9.eEdD]+\s+[-+0-9.eEdD]+\s+[-+0-9.eEd]+)",
                     #SM(r"\s*(?P<onetep_cell_vector>[\d\.]+\s+[\d\.]+\s+[\d\.]+) \s*[-+0-9.eEdD]*\s*[-+0-9.eEdD]*\s*[-+0-9.eEdD]*",
                        # endReStr = "\%endblock\s*lattice\_cart\s*",
                                repeats = True),

                            ]), # CLOSING onet

                    SM(startReStr = r"\%block\spositions\_abs\s*",
                        forwardMatch = True,
                        sections = ["x_onetep_section_atom_positions"],
                        endReStr = "\n",
                        subMatchers = [
                        SM(r"(?P<x_onetep_units_atom_position>[A-Za-z]+)"),

                        SM(r"(?P<x_onetep_store_atom_labels>[A-Za-z0-9]+)\s*(?P<x_onetep_store_atom_positions>[-\d\.]+\s+[-\d\.]+\s+[-\d\.]+)",
                            # endReStr = "\n",
                            repeats = True)

                                 ]), # CLOSING onet
                    SM(startReStr = r"\s*\%block\spositions\_abs\s*",
                        forwardMatch = True,
                        sections = ["x_onetep_section_atom_positions"],
                        endReStr = "\n",
                        subMatchers = [
                        SM(r"(?P<x_onetep_units_atom_position>[A-Za-z]+)"),
                        SM(r"\s*(?P<x_onetep_store_atom_labels>[A-Za-z0-9]+)\s*(?P<x_onetep_store_atom_positions>[-\d\.]+\s+[-\d\.]+\s+[-\d\.]+)",
                            # endReStr = "\n",
                            repeats = True)

                                 ]), # CLOS
                    SM(startReStr = r"\%block\s*positions\_abs\s*",
                        forwardMatch = True,
                        sections = ["x_onetep_section_atom_positions"],
                        endReStr = "\n",
                        subMatchers = [
                        SM(r"(?P<x_onetep_units_atom_position>[A-Za-z]+)"),
                        SM(r"(?P<x_onetep_store_atom_labels>[A-Za-z0-9]+)\s*(?P<x_onetep_store_atom_positions>[-\d\.]+\s+[-\d\.]+\s+[-\d\.]+)",
                            # endReStr = "\n",
                            repeats = True)

                                 ]), # CLOSING onetep_section_atom_position
                    SM(startReStr = r"\s*\%block\s*positions\_abs\s*",
                        forwardMatch = True,
                        sections = ["x_onetep_section_atom_positions"],
                        endReStr = "\n",
                        subMatchers = [
                        SM(r"(?P<x_onetep_units_atom_position>[A-Za-z]+)"),
                        SM(r"\s*(?P<x_onetep_store_atom_labels>[A-Za-z0-9]+)\s*(?P<x_onetep_store_atom_positions>[-\d\.]+\s+[-\d\.]+\s+[-\d\.]+)",
                            # endReStr = "\n",
                            repeats = True)

                                 ]), # CLOSI



                    SM(startReStr = r"\%BLOCK\sPOSITIONS\_ABS",
                        forwardMatch = True,
                        sections = ["x_onetep_section_atom_positions"],
                        endReStr = "\n",
                        subMatchers = [
                        SM(r"(?P<x_onetep_units_atom_position>[A-Za-z]+)"),
                        SM(r"(?P<x_onetep_store_atom_labels>[A-Za-z0-9]+)\s*(?P<x_onetep_store_atom_positions>[-\d\.]+\s+[-\d\.]+\s+[-\d\.]+)",
                            # endReStr = "\n",
                            repeats = True)

                                 ]), # CLOSING onet
                    SM(startReStr = r"\s*\%BLOCK\sPOSITIONS\_ABS",
                        forwardMatch = True,
                        sections = ["x_onetep_section_atom_positions"],
                        endReStr = "\n",
                        subMatchers = [
                        SM(r"(?P<x_onetep_units_atom_position>[A-Za-z]+)"),
                        SM(r"\s*(?P<x_onetep_store_atom_labels>[A-Za-z0-9]+)\s*(?P<x_onetep_store_atom_positions>[-\d\.]+\s+[-\d\.]+\s+[-\d\.]+)",
                            # endReStr = "\n",
                            repeats = True)

                                 ]), # CLOS
                    SM(startReStr = r"\%BLOCK\s*POSITIONS\_ABS",
                        forwardMatch = True,
                        sections = ["x_onetep_section_atom_positions"],
                        endReStr = "\n",
                        subMatchers = [
                        SM(r"(?P<x_onetep_units_atom_position>[A-Za-z]+)"),
                        SM(r"(?P<x_onetep_store_atom_labels>[A-Za-z0-9]+)\s*(?P<x_onetep_store_atom_positions>[-\d\.]+\s+[-\d\.]+\s+[-\d\.]+)",
                            # endReStr = "\n",
                            repeats = True)

                                 ]), # CLOSING onetep_section_atom_position
                    SM(startReStr = r"\s*\%BLOCK\s*POSITIONS\_ABS",
                        forwardMatch = True,
                        sections = ["x_onetep_section_atom_positions"],
                        endReStr = "\n",
                        subMatchers = [
                        SM(r"(?P<x_onetep_units_atom_position>[A-Za-z]+)"),
                        SM(r"\s*(?P<x_onetep_store_atom_labels>[A-Za-z0-9]+)\s*(?P<x_onetep_store_atom_positions>[-\d\.]+\s+[-\d\.]+\s+[-\d\.]+)",
                            # ,
                            repeats = True)

                                 ]), # CLOSI
                   ]) # CLOSING SM systemDescription





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
                               'section_system': CachingLvl,
                                # 'section_run': CachingLvl,
                                # 'section_single_configuration_calculation': CachingLvl,
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
    OnetepCellFileSimpleMatcher = build_OnetepCellFileSimpleMatcher()
    # loading metadata from nomad-meta-info/meta_info/nomad_meta_info/Onetep.nomadmetainfo.json
    metaInfoPath = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)),"../../../../nomad-meta-info/meta_info/nomad_meta_info/onetep.nomadmetainfo.json"))
    metaInfoEnv = get_metaInfo(metaInfoPath)
    # set parser info
    parserInfo = {'name':'Onetep-cell-parser', 'version': '1.0'}
    # get caching level for metadata
    cachingLevelForMetaName = get_cachingLevelForMetaName(metaInfoEnv, CachingLvl)
    # start parsing
    mainFunction(mainFileDescription = OnetepCellFileSimpleMatcher,
                 metaInfoEnv = metaInfoEnv,
                 parserInfo = parserInfo,
                 cachingLevelForMetaName = cachingLevelForMetaName,
                 superContext = OnetepCellParserContext())

if __name__ == "__main__":
    main(CachingLevel.Forward)







