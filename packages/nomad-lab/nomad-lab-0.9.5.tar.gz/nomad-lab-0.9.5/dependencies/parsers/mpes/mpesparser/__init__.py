# Copyright 2016-2020 R. Patrick Xian, Markus Scheidgen
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
    Experiment, Data, Method, Sample, Material, Location)


class MPESParser(FairdiParser):
    def __init__(self):
        super().__init__(
            name='parsers/mpes', code_name='mpes', code_homepage='https://github.com/mpes-kit/mpes',
            domain='ems', mainfile_mime_re=r'(application/json)|(text/.*)', mainfile_name_re=(r'.*.meta'),
            mainfile_contents_re=(r'"data_repository_name": "zenodo.org"')
        )

    def parse(self, filepath, archive, logger=None):
        with open(filepath, 'rt') as f:
            data = json.load(f)

        experiment = archive.m_create(Experiment)
        experiment.raw_metadata = data

        # Read general experimental parameters
        # experiment.experiment_location = ', '.join(reversed(re.findall(r"[\w']+", data.get('experiment_location'))))
        location = experiment.m_create(Location)
        location.address = data.get('experiment_location')
        location.institution = data.get('facility_institution')
        location.facility = data.get('facility')

        dates = data.get('experiment_date')
        if dates:
            start, end = dates.split(' ')
            try:
                experiment.experiment_time = datetime.strptime(start, '%m.%Y')
            except ValueError:
                pass
            try:
                experiment.experiment_end_time = datetime.strptime(end, '%m.%Y')
            except ValueError:
                pass
        experiment.experiment_summary = data.get('experiment_summary')

        # Read data parameters
        section_data = experiment.m_create(Data)
        section_data.repository_name = data.get('data_repository_name')
        section_data.entry_repository_url = data.get('data_repository_url')
        section_data.repository_url = '/'.join(data.get('data_repository_url').split('/')[0:3])
        section_data.preview_url = 'preview.png'

        # Read method parameters
        method = experiment.m_create(Method)
        method.data_type = 'multidimensional spectrum'
        method.method_name = data.get('experiment_method')
        method.method_abbreviation = data.get('experiment_method_abbrv')
        method.instrument_description = data.get('equipment_description')
        method.probing_method = 'laser pulses'
        method.general_beamline = data.get('beamline')
        method.general_source_pump = data.get('source_pump')
        method.general_source_probe = data.get('source_probe')
        method.general_measurement_axis = np.array(re.findall(r"[\w']+", data.get('measurement_axis')))
        method.general_physical_axis = np.array(re.findall(r"[\w']+", data.get('physical_axis')))

        # Read parameters related to experimental source
        # source_gid = backend.openSection('experiment_source_parameters')
        method.source_pump_repetition_rate = data.get('pump_rep_rate')
        method.source_pump_pulse_duration = data.get('pump_pulse_duration')
        method.source_pump_wavelength = data.get('pump_wavelength')
        method.source_pump_spectrum = np.array(data.get('pump_spectrum'))
        method.source_pump_photon_energy = data.get('pump_photon_energy')
        method.source_pump_size = np.array(data.get('pump_size'))
        method.source_pump_fluence = np.array(data.get('pump_fluence'))
        method.source_pump_polarization = data.get('pump_polarization')
        method.source_pump_bunch = data.get('pump_bunch')
        method.source_probe_repetition_rate = data.get('probe_rep_rate')
        method.source_probe_pulse_duration = data.get('probe_pulse_duration')
        method.source_probe_wavelength = data.get('probe_wavelength')
        method.source_probe_spectrum = np.array(data.get('probe_spectrum'))
        method.source_probe_photon_energy = data.get('probe_photon_energy')
        method.source_probe_size = np.array(data.get('probe_size'))
        method.source_probe_fluence = np.array(data.get('probe_fluence'))
        method.source_probe_polarization = data.get('probe_polarization')
        method.source_probe_bunch = data.get('probe_bunch')
        method.source_temporal_resolution = data.get('temporal_resolution')

        # Read parameters related to detector
        # detector_gid = backend.openSection('experiment_detector_parameters')
        method.detector_extractor_voltage = data.get('extractor_voltage')
        method.detector_work_distance = data.get('work_distance')
        method.detector_lens_names = np.array(re.findall(r"[\w']+", data.get('lens_names')))
        method.detector_lens_voltages = np.array(data.get('lens_voltages'))
        method.detector_tof_distance = data.get('tof_distance')
        method.detector_tof_voltages = np.array(data.get('tof_voltages'))
        method.detector_sample_bias = data.get('sample_bias')
        method.detector_magnification = data.get('magnification')
        method.detector_voltages = np.array(data.get('detector_voltages'))
        method.detector_type = data.get('detector_type')
        method.detector_sensor_size = np.array(data.get('sensor_size'))
        method.detector_sensor_count = data.get('sensor_count')
        method.detector_sensor_pixel_size = np.array(data.get('sensor_pixel_size'))
        method.detector_calibration_x_to_momentum = np.array(data.get('calibration_x_to_momentum'))
        method.detector_calibration_y_to_momentum = np.array(data.get('calibration_y_to_momentum'))
        method.detector_calibration_tof_to_energy = np.array(data.get('calibration_tof_to_energy'))
        method.detector_calibration_stage_to_delay = np.array(data.get('calibration_stage_to_delay'))
        method.detector_calibration_other_converts = np.array(data.get('calibration_other_converts'))
        method.detector_momentum_resolution = np.array(data.get('momentum_resolution'))
        method.detector_spatial_resolution = np.array(data.get('spatial_resolution'))
        method.detector_energy_resolution = np.array(data.get('energy_resolution'))

        # Read parameters related to sample
        sample = experiment.m_create(Sample)
        sample.sample_description = data.get('sample_description')
        sample.sample_id = data.get('sample_id')
        sample.sample_state_of_matter = data.get('sample_state')
        sample.sample_purity = data.get('sample_purity')
        sample.sample_surface_termination = data.get('sample_surface_termination')
        sample.sample_layers = data.get('sample_layers')
        sample.sample_stacking_order = data.get('sample_stacking_order')
        sample.sample_chemical_id_cas = data.get('chemical_id_cas')
        sample.sample_temperature = data.get('sample_temperature')
        sample.sample_pressure = data.get('sample_pressure')
        sample.sample_growth_method = data.get('growth_method')
        sample.sample_preparation_method = data.get('preparation_method')
        sample.sample_vendor = data.get('sample_vendor')
        sample.sample_substrate_material = data.get('substrate_material')
        sample.sample_substrate_state_of_matter = data.get('substrate_state')
        sample.sample_substrate_vendor = data.get('substrate_vendor')

        material = sample.m_create(Material)
        material.space_group = data.get('sample_space_group')
        material.chemical_name = data.get('chemical_name')
        material.chemical_formula = data.get('chemical_formula')
        atoms = set(ase.Atoms(data.get('chemical_formula')).get_chemical_symbols())
        material.atom_labels = np.array(list(atoms))

        # TODO sample classification
        sample.sample_microstructure = 'bulk sample, polycrystalline'
        sample.sample_constituents = 'multi phase'
