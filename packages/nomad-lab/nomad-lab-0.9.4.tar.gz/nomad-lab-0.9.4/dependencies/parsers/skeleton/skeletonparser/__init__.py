# Copyright 2016-2018 Markus Scheidgen
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

import sys
import os.path
import json
import ase
import numpy as np
from datetime import datetime

from nomadcore.simple_parser import SimpleMatcher
from nomadcore.baseclasses import ParserInterface, AbstractBaseParser

from nomad.parsing import Backend


class SkeletonParserInterface(ParserInterface):

    def get_metainfo_filename(self):
        """
        The parser specific metainfo. To include other metadata definitions, use
        the 'dependencies' key to refer to other local nomadmetainfo.json files or
        to nomadmetainfo.json files that are part of the general nomad-meta-info
        submodule (i.e. ``dependencies/nomad-meta-info``).
         """
        return os.path.join(os.path.dirname(__file__), 'skeleton.nomadmetainfo.json')

    def get_parser_info(self):
        """ Basic info about parser used in archive data and logs. """
        return {
            'name': 'you parser name',
            'version': '1.0.0'
        }

    def setup_version(self):
        """ Can be used to call :func:`setup_main_parser` differently for different code versions. """
        self.setup_main_parser(None)

    def setup_main_parser(self, _):
        """ Setup the actual parser (behind this interface) """
        self.main_parser = SkeletonParser(self.parser_context)


class SkeletonParser(AbstractBaseParser):
    def parse(self, filepath):
        backend = self.parser_context.super_backend

        with open(filepath, 'rt') as f:
            data = json.load(f)

        # You need to open sections before you can add values or sub sections to it.
        # The returned 'gid' can be used to reference a specific section if multiple
        # sections of the same type are opened.
        root_gid = backend.openSection('section_experiment')
        # Values are added to the open section of the given metadata definitions. In
        # the following case 'experiment_location' is a quantity of 'section_experiment'.
        # When multiple sections of the same type (e.g. 'section_experiment') are open,
        # you can use the 'gid' as an additional argument.
        backend.addValue('experiment_location', data.get('location'))
        # The backend will check the type of the given value agains the metadata definition.
        backend.addValue('experiment_time', int(datetime.strptime(data.get('date'), '%d.%M.%Y').timestamp()))

        # Subsections work like before. The parent section must still be open.
        method_gid = backend.openSection('section_method')
        backend.addValue('experiment_method_name', data.get('method', 'Bare eyes'))
        # Values do not necessarely have to be read from the parsed file.
        backend.addValue('probing_method', 'laser pulsing')
        backend.closeSection('section_method', method_gid)

        data_gid = backend.openSection('section_data')
        backend.addValue('data_repository_name', 'zenodo.org')
        backend.addValue('data_repository_url', 'https://zenodo.org/path/to/mydata')
        backend.addValue('data_preview_url', 'https://www.physicsforums.com/insights/wp-content/uploads/2015/09/fem.jpg')
        backend.closeSection('section_data', data_gid)

        # Subsections work like before. The parent section must still be open.
        sample_gid = backend.openSection('section_sample')
        backend.addValue('sample_chemical_name', data.get('sample_chemical'))
        backend.addValue('sample_chemical_formula', data.get('sample_formula'))
        backend.addValue('sample_temperature', data.get('sample_temp'))
        backend.addValue('sample_microstructure', 'thin films')
        backend.addValue('sample_constituents', 'multi phase')

        atoms = set(ase.Atoms(data.get('sample_formula')).get_chemical_symbols())
        # To add arrays (vectors, matrices, etc.) use addArrayValues and provide a
        # numpy array. The shape of the numpy array must match the shape defined in
        # the respective metadata definition.
        backend.addArrayValues('sample_atom_labels', np.array(list(atoms)))

        # Close sections in the reverse order.
        backend.closeSection('section_sample', sample_gid)
        backend.closeSection('section_experiment', root_gid)
