# Copyright 2016-2018 Fawzi Mohamed, Adriel Domínguez
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

from builtins import object
from nomadcore.simple_parser import SimpleMatcher as SM, mainFunction
from nomadcore.local_meta_info import loadJsonFile, InfoKindEl
from nomadcore.unit_conversion import unit_conversion
import os, sys, json
import numpy as np
import logging

class dftb_plusContext(object):
    """ context for dftb_plus parser """

    def __init__(self):
        self.parser = None

    def initialize_values(self):
        """allows to reset values if the same superContext is used to parse different files"""
        pass

    def startedParsing(self, path, parser):
        """called when parsing starts"""
        self.parser = parser
        # allows to reset values if the same superContext is used to parse different files
        self.initialize_values()

    def onClose_section_molecule_type(self, backend, gIndex, section):

        atom_charge = section['x_dftbp_charge']
        if atom_charge is not None:
           backend.addArrayValues('atom_in_molecule_charge', np.asarray(atom_charge))

    def onClose_section_eigenvalues(self, backend, gIndex, section):

        eigenvalues = section['x_dftbp_eigenvalues_values']
        occ = section['x_dftbp_eigenvalues_occupation']
        # DISABLED
        # WRONG dimensions, (flat), should be [number_of_spin_channels,number_of_eigenvalues_kpoints,number_of_eigenvalues]

        #if eigenvalues is not None:
        #    backend.addArrayValues('eigenvalues_values', np.asarray(eigenvalues))
        #if occ is not None:
        #    backend.addArrayValues('eigenvalues_occupation', np.asarray(occ))

    def onClose_section_single_configuration_calculation(self, backend, gIndex, section):

        atom_force = []
        for i in ['X', 'Y', 'Z']:
           forces = section['x_dftbp_atom_forces_' + i]
           if forces is not None:
              atom_force.append(forces)
        if atom_force:
           backend.addArrayValues('atom_forces', np.transpose(np.asarray(atom_force)))

    def onClose_section_system(self, backend, gIndex, section):

        atom_coord = []
        for i in ['X', 'Y', 'Z']:
           coord = section['x_dftbp_atom_positions_' + i]
           if coord is not None:
              atom_coord.append(coord)
        if atom_coord:
           backend.addArrayValues('atom_positions', np.transpose(np.asarray(atom_coord)))


# description of the input
def build_root_parser(*args, **kwargs):
    return SM(
        name = 'root',
        weak = True,
        forwardMatch = True,
        startReStr = "",
        subMatchers = [
            SM(name = 'newRun',
            startReStr = r"\s*Fermi distribution function",
            #repeats = True,
            required = True,
            forwardMatch = True,
            sections   = ['section_run'],
            fixedStartValues={'program_name': 'DFTB+', 'program_basis_set_type': 'LCAO'},
            subMatchers = [
                SM(name = 'header',
                    startReStr = r"\s*Fermi distribution function",
                    #forwardMatch = True,
                    #subMatchers=[ ]
                ),
                SM(name = 'coordinates',
                    startReStr = r"\s*Coordinates of moved atoms\s*\(?(au)?\)?:",
                    #forwardMatch = True,
                    sections   = ['section_system','section_topology','section_molecule_type'],
                    subMatchers = [
                        SM(r"\s*Coordinates of moved atoms\s*\(?(au)?\)?:"),
                        SM(r"\s*(?P<atom>\d+)\s*(?P<x_dftbp_atom_positions_X__bohr>[+-]?\d+\.\d+)\s*(?P<x_dftbp_atom_positions_Y__bohr>[+-]?\d+\.\d+)\s*(?P<x_dftbp_atom_positions_Z__bohr>[+-]?\d+\.\d+)\s*", repeats = True),
                    ],
                ),
                SM(name = 'charges',
                    startReStr = r"\s*Net atomic charges .e.",
                    #endReStr = r"\s*",
                    #forwardMatch = True,
                    sections   = ['section_molecule_type'],
                    subMatchers = [
                        SM(r"\s*Atom\s*Net charge"),
                        SM(r"\s*(?P<atom>\d+)\s*(?P<x_dftbp_charge__e>[+-]?\d+\.\d+)\s*", repeats = True),
                                    #SM(r"\s*")
                    ],
                ),
                SM(name = 'eigenvalues_H',
                    startReStr = r"\s*Eigenvalues /H",
                    #forwardMatch = True,
                    sections   = ['section_eigenvalues'],
                    subMatchers = [
                        SM(r"\s*Eigenvalues /H"),
                        SM(r"\s*(?P<x_dftbp_eigenvalues_values__hartree>[+-]?\d+\.\d+)\s*", repeats = True),
                    ],
                ),
                    SM(name = 'eigenvalues_eV',
                        startReStr = r"\s*Eigenvalues /eV",
                        #forwardMatch = True,
                        sections   = ['section_eigenvalues'],
                        subMatchers = [
                            SM(r"\s*Eigenvalues /eV"),
                            SM(r"\s*(?P<x_dftbp_eigenvalues_values__eV>[+-]?\d+\.\d+)\s*", repeats = True),
                    ],
                ),
                    SM(name = 'Occupations',
                        startReStr = r"\s*Fillings",
                        #forwardMatch = True,
                        sections   = ['section_eigenvalues'],
                        subMatchers = [
                            SM(r"\s*Fillings"),
                            SM(r"\s*(?P<x_dftbp_eigenvalues_occupation>\d+\.\d+)\s*", repeats = True),
                    ],
                ),
                SM(name = 'energies',
                    startReStr = r"\s*Fermi energy:.*",
                    sections   = ['section_single_configuration_calculation'],
                    subMatchers = [
                        SM(r"\s*Fermi energy:.*"),
                        #SM(r"\s*Band energy:.*"),
                        SM(r"\s*Total energy:\s*(?P<energy_total__hartree>[+-]?\d+\.\d+)\s*H.*"),
                        SM(r"\s*Total Mermin free energy:\s*(?P<energy_free__hartree>[+-]?\d+\.\d+)\s*H.*"),
                    ],
                    #forwardMatch = True,
                    #required = True,
                ),
                SM(name = 'forces',
                    startReStr = r"\s*Total Forces",
                    sections   = ['section_single_configuration_calculation'],
                    subMatchers = [
                        SM(r"\s*Total Forces*"),
                        SM(r"\s*(?P<x_dftbp_atom_forces_X__forceAu>[+-]?\d+\.\d+E?[+-]?\d+)\s*(?P<x_dftbp_atom_forces_Y__forceAu>[+-]?\d+\.\d+E?[+-]?\d+)\s*(?P<x_dftbp_atom_forces_Z__forceAu>[+-]?\d+\.\d+E?[+-]?\d+)\s*", repeats = True),
                        SM(r"\s*Maximal derivative component:\s*(?P<x_dftbp_force_max__forceAu>[+-]?\d+\.\d+E?[+-]?\d+)\s*(au)?"),
                        SM(r"\s*Max force for moved atoms::\s*(?P<x_dftbp_force_max_mov__forceAu>[+-]?\d+\.\d+E?[+-]?\d+)\s*(au)?"),
                    ],

                ),
            ])
            ])

# loading metadata from nomad-meta-info/meta_info/nomad_meta_info/dftb_plus.nomadmetainfo.json

parserInfo = {
  "name": "parser_dftb+",
  "version": "1.0"
}

# metaInfoPath = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)),"../../../../nomad-meta-info/meta_info/nomad_meta_info/dftb_plus.nomadmetainfo.json"))
# metaInfoEnv, warnings = loadJsonFile(filePath = metaInfoPath, dependencyLoader = None, extraArgsHandling = InfoKindEl.ADD_EXTRA_ARGS, uri = None)

# if __name__ == "__main__":
#     superContext = dftb_plusContext()
#     mainFunction(mainFileDescription, metaInfoEnv, parserInfo, superContext = superContext)

class DFTBPlusParser():
   """ A proper class envolop for running this parser from within python. """
   def __init__(self, backend, **kwargs):
       self.backend_factory = backend

   def parse(self, mainfile):
       from unittest.mock import patch
       logging.info('dftbplus parser started')
       logging.getLogger('nomadcore').setLevel(logging.WARNING)
       backend = self.backend_factory("dftbplus.nomadmetainfo.json")
       context = dftb_plusContext()
       with patch.object(sys, 'argv', ['<exe>', '--uri', 'nmd://uri', mainfile]):
           mainFunction(
               build_root_parser(context),
               None,
               parserInfo,
               cachingLevelForMetaName=dict(),
               superContext=context,
               superBackend=backend)

       return backend