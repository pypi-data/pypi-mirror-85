# Copyright 2016-2018 Lauri Himanen, Fawzi Mohamed
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

import logging
import numpy as np
from yaml import Loader, YAMLError
from yaml import ScalarNode, SequenceNode, MappingNode, MappingEndEvent
from nomadcore.baseclasses import AbstractBaseParser
from bigdftparser.generic.libxc_codes import LIB_XC_MAPPING
import ase.data
LOGGER = logging.getLogger("nomad")


class BigDFTMainParser(AbstractBaseParser):
    """The main parser class that is called for all run types. Parses the NWChem
    output file.
    """
    def __init__(self, parser_context):
        """
        """
        super(BigDFTMainParser, self).__init__(parser_context)

        # Map keys in the output to funtions that handle the values
        self.key_to_funct_map = {
            "Version Number": lambda x: self.backend.addValue("program_version", x),
            "Atomic structure": self.atomic_structure,
            "Sizes of the simulation domain": self.simulation_domain,
            "Atomic System Properties": self.atomic_system_properties,
            "dft": self.dft,
            "DFT parameters": self.dft_parameters,
            "Ground State Optimization": self.ground_state_optimization,
            "Atomic Forces (Ha/Bohr)": self.atomic_forces,
            "Energy (Hartree)": lambda x: self.backend.addRealValue("energy_total", float(x), unit="hartree"),
        }

    def parse(self, filepath):
        """The output file of a BigDFT run is a YAML document. Here we directly
        parse this document with an existing YAML library, and push its
        contents into the backend. This function will read the document in
        smaller pieces, thus preventing the parser from opening too large files
        directly into memory.
        """
        self.prepare()
        self.print_json_header()
        with open(filepath, "r") as fin:
            try:
                # Open default sections and output default information
                section_run_id = self.backend.openSection("section_run")
                section_system_id = self.backend.openSection("section_system")
                section_method_id = self.backend.openSection("section_method")
                section_scc_id = self.backend.openSection("section_single_configuration_calculation")
                self.backend.addValue("program_name", "BigDFT")
                self.backend.addValue("electronic_structure_method", "DFT")
                self.backend.addValue("program_basis_set_type", "real-space grid")
                self.backend.addValue("single_configuration_calculation_to_system_ref", section_system_id)
                self.backend.addValue("single_configuration_to_calculation_method_ref", section_method_id)

                loader = Loader(fin)
                generator = self.generate_root_nodes(loader)

                # Go through all the keys in the mapping, and call an appropriate
                # function on the value.
                for key, value in generator:

                    function = self.key_to_funct_map.get(key)
                    if function is not None:
                        function(value)

                # Close default sections
                self.backend.closeSection("section_single_configuration_calculation", section_scc_id)
                self.backend.closeSection("section_method", section_method_id)
                self.backend.closeSection("section_system", section_system_id)
                self.backend.closeSection("section_run", section_run_id)
            except YAMLError:
                raise Exception("There was a syntax error in the BigDFT YAML output file.")

        self.print_json_footer()

    def generate_root_nodes(self, loader):
        # Ignore the first two events
        loader.get_event()  # StreamStarEvetn
        loader.get_event()  # DocumentStartEvent
        start_event = loader.get_event()  # MappingStartEvent
        tag = start_event.tag

        # This is the root mapping that contains everything
        node = MappingNode(tag, [],
                start_event.start_mark, None,
                flow_style=start_event.flow_style)

        while not loader.check_event(MappingEndEvent):
            key = loader.construct_scalar(loader.compose_node(node, None))
            value = loader.compose_node(node, key)
            if isinstance(value, MappingNode):
                value = loader.construct_mapping(value, deep=True)
            elif isinstance(value, SequenceNode):
                value = loader.construct_sequence(value, deep=True)
            elif isinstance(value, ScalarNode):
                value = loader.construct_scalar(value)
            yield (key, value)

    #===========================================================================
    # The following functions handle the different sections in the output
    def ground_state_optimization(self, value):
        subspace_optimization = value[0]["Hamiltonian Optimization"]
        subspace_optimization = subspace_optimization[0]["Subspace Optimization"]
        wavefunction_iterations = subspace_optimization["Wavefunctions Iterations"]
        n_iterations = len(wavefunction_iterations)
        self.backend.addValue("number_of_scf_iterations", n_iterations)
        for iteration in wavefunction_iterations:

            scf_id = self.backend.openSection("section_scf_iteration")
            energies = iteration["Energies"]
            # ekin = energies["Ekin"]
            # epot = energies["Epot"]
            # enl = energies["Enl"]
            # eh = energies["EH"]
            # gradient = iteration["gnrm"]
            exc = energies.get("EXC")  # Use get instead, because this value is not always present
            evxc = energies.get("EvXC")  # Use get instead, because this value is not always present
            etotal = iteration["EKS"]
            energy_change = iteration["D"]
            self.backend.addRealValue("energy_total_scf_iteration", etotal, unit="hartree")
            if exc is not None:
                self.backend.addRealValue("energy_XC_scf_iteration", exc, unit="hartree")
            if evxc is not None:
                self.backend.addRealValue("energy_XC_potential_scf_iteration", evxc, unit="hartree")
            self.backend.addRealValue("energy_change_scf_iteration", energy_change, unit="hartree")
            self.backend.closeSection("section_scf_iteration", scf_id)

    def atomic_structure(self, value):
        np_positions = []
        np_labels = []
        positions = value["Positions"]
        for position in positions:
            for key, value in position.items():
                # Not all keys are chemical symbols, e.g. spin, etc.
                if key in ase.data.chemical_symbols:
                    np_positions.append(value)
                    np_labels.append(key)
        np_positions = np.array(np_positions)
        np_labels = np.array(np_labels)
        self.backend.addArrayValues("atom_positions", np_positions, unit="angstrom")
        self.backend.addArrayValues("atom_labels", np_labels)

    def simulation_domain(self, value):
        simulation_cell = np.diag(value["Angstroem"])
        self.backend.addArrayValues("simulation_cell", simulation_cell, unit="angstrom")

    def atomic_system_properties(self, value):
        # Number of atoms
        n_atoms = value["Number of atoms"]
        self.backend.addValue("number_of_atoms", n_atoms)

        # Periodicity
        boundary = value["Boundary Conditions"]
        if boundary == "Free":
            periodic_dimensions = np.array([False, False, False])
        elif boundary == "Periodic":
            periodic_dimensions = np.array([True, True, True])
        elif boundary == "Surface":
            periodic_dimensions = np.array([True, False, True])
        else:
            raise Exception("Unknown boundary condtions.")
        self.backend.addArrayValues("configuration_periodic_dimensions", periodic_dimensions)

    def dft(self, value):
        # Total_charge
        charge = value["qcharge"]
        self.backend.addValue("total_charge", charge)

        # SCF options
        max_iter = value["itermax"]
        self.backend.addValue("scf_max_iteration", max_iter)

        # Spin channels
        n_spin = value["nspin"]
        self.backend.addValue("number_of_spin_channels", n_spin)

    def atomic_forces(self, value):
        forces = []
        for force in value:
            forces.append(*force.values())
        forces = np.array(forces)
        self.backend.addArrayValues("atom_forces", forces, unit="hartree/bohr")

    def dft_parameters(self, value):
        # XC functional
        exchange_settings = value["eXchange Correlation"]
        xc_id = exchange_settings["XC ID"]

        # LibXC codes, see http://bigdft.org/Wiki/index.php?title=XC_codes
        if xc_id < 0:
            xc_parts = []
            xc_id_str = str(xc_id)[1:]
            xc_id_str_len = len(xc_id_str)
            if xc_id_str_len <= 3:
                xc_id_str = "0"*(3-xc_id_str_len)+xc_id_str
                xc_parts.append(xc_id_str)
            elif xc_id_str_len == 6:
                xc_parts.append(xc_id_str[:3])
                xc_parts.append(xc_id_str[3:])

            xc = []
            for part in xc_parts:
                xc1 = LIB_XC_MAPPING.get(part)
                if xc1 is not None:
                    xc.append(xc1)
                else:
                    raise Exception("Unknown LibXC functional number: '{}'".format(part))
        # ABINIT codes, see
        # http://www.tddft.org/programs/octopus/wiki/index.php/Developers_Manual:ABINIT
        # and
        # http://bigdft.org/Wiki/index.php?title=XC_codes
        else:
            mapping = {
                1: ["LDA_XC_TETER93"],
                # 2: ["LDA_C_PZ"],  # Not really sure...
                # 3: Unknown
                # 4: ["LDA_C_WIGNER"],  # Not really sure...
                # 5: ["LDA_C_HL"],  # Not really sure...
                # 6: ["LDA_C_XALPHA"],  # Not really sure...
                # 7: ["LDA_XC_PW"],  # Not really sure...
                # 8: ["LDA_X_PW"],  # Not really sure...
                # 9: ["LDA_X_PW", "LDA_C_RPA"],  # Not really sure...
                # 10: Internal
                11: ["GGA_C_PBE", "GGA_X_PBE"],
                12: ["GGA_X_PBE"],
                # 13: ["GGA_C_PBE","GGA_X_LB"],  # Not really sure...
                # 14: ["GGA_C_PBE","GGA_X_PBE_R"],  # Not really sure...
                15: ["GGA_C_PBE", "GGA_X_RPBE"],
                16: ["GGA_XC_HCTH_93"],
                17: ["GGA_XC_HCTH_120"],
                # 20: Unknown
                # 21: Unknown
                # 22: Unknown
                # 23: ["GGA_X_WC"],  # Not really sure...
                # 24: ["GGA_X_C09X"],  # Not really sure...
                # 25: Internal
                26: ["GGA_XC_HCTH_147"],
                27: ["GGA_XC_HCTH_407"],
                # 28: Internal
                100: ["HF_X"],
            }
            xc = mapping.get(xc_id)

        # Create the XC sections and a summary
        if xc is None:
            raise Exception("Unknown functional number: '{}'".format(xc_id))
        sorted_xc = sorted(xc)
        summary = ""
        n_names = len(sorted_xc)
        for i_name, name in enumerate(sorted_xc):
            weight = 1.0
            xc_id = self.backend.openSection("section_XC_functionals")
            self.backend.addValue("XC_functional_name", name)
            self.backend.addValue("XC_functional_weight", weight)
            self.backend.closeSection("section_XC_functionals", xc_id)
            summary += "{}*{}".format(weight, name)
            if i_name+1 != n_names:
                summary += "_"
        self.backend.addValue("XC_functional", summary)
