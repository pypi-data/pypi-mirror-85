# Copyright 2016-2019 Markus Scheidgen, Markus Kühbach
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
import re
import numpy as np
from datetime import datetime

from nomad.parsing.parser import FairdiParser
from nomad.datamodel.metainfo.common_experimental import (
    Experiment, Data, Method, Sample, Location, Material)


class APTFIMParser(FairdiParser):
    def __init__(self):
        super().__init__(
            name='parsers/aptfim', code_name='mpes', code_homepage='https://github.com/mpes-kit/mpes',
            domain='ems', mainfile_mime_re=r'(application/json)|(text/.*)', mainfile_name_re=(r'.*.aptfim')
        )

    def parse(self, filepath, archive, logger=None):
        with open(filepath, 'rt') as f:
            data = json.load(f)

        experiment = archive.m_create(Experiment)
        experiment.raw_metadata = data

        # Read general tool environment details
        location = experiment.m_create(Location)
        location.address = data.get('experiment_location')
        location.facility = data.get('experiment_facility_institution')
        experiment.experiment_summary = '%s of %s.' % (
            data.get('experiment_method').capitalize(), data.get('specimen_description'))

        try:
            experiment.experiment_time = datetime.strptime(
                data.get('experiment_date_global_start'), '%d.%m.%Y %M:%H:%S')
        except ValueError:
            pass

        try:
            experiment.experiment_end_time = datetime.strptime(
                data.get('experiment_date_global_end'), '%d.%m.%Y %M:%H:%S')
        except ValueError:
            pass

        # Read data parameters
        section_data = experiment.m_create(Data)
        section_data.repository_name = data.get('data_repository_name')
        section_data.entry_repository_url = data.get('data_repository_url')
        section_data.repository_url = '/'.join(data.get('data_repository_url').split('/')[0:3])
        preview_url = data.get('data_preview_url')
        # TODO: This a little hack to correct the preview url and should be removed
        # after urls are corrected
        preview_url = '%s/files/%s' % tuple(preview_url.rsplit('/', 1))
        section_data.preview_url = preview_url

        # Read parameters related to method
        method = experiment.m_create(Method)
        method.data_type = 'image'
        method.method_name = data.get('experiment_method')
        method.method_abbreviation = 'APT/FIM'
        method.probing_method = 'electric pulsing'
        method.instrument_description = data.get('instrument_info')

        method.measured_number_ions_evaporated = data.get('measured_number_ions_evaporated')
        method.measured_detector_hit_pos = data.get('measured_detector_hit_pos') == 'yes'
        method.measured_detector_hit_mult = data.get('measured_detector_hit_mult') == 'yes'
        method.measured_detector_dead_pulses = data.get('measured_detector_dead_pulses') == 'yes'
        method.measured_time_of_flight = data.get('measured_time_of_flight') == 'yes'
        method.measured_standing_voltage = data.get('measured_standing_voltage') == 'yes'
        method.measured_pulse_voltage = data.get('measured_pulse_voltage') == 'yes'
        method.experiment_operation_method = data.get('experiment_operation_method') == 'yes'
        method.experiment_imaging_method = data.get('experiment_imaging_method') == 'yes'

        # Read parameters related to sample
        sample = experiment.m_create(Sample)
        sample.sample_description = data.get('specimen_description')
        sample.sample_microstructure = data.get('specimen_microstructure')
        sample.sample_constituents = data.get('specimen_constitution')

        material = sample.m_create(Material)
        atom_labels = data.get('specimen_chemistry')
        formula = ase.Atoms(atom_labels).get_chemical_formula()
        material.atom_labels = np.array(atom_labels)
        material.chemical_formula = formula
        material.chemical_name = formula
