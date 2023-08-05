import numpy as np

from nomad.metainfo import Package, Quantity, Section
from nomad.datamodel.metainfo import common_experimental


m_package = Package(name='mpes')


class Method(common_experimental.Method):

    m_def = Section(validate=False, extends_base_section=True)

    general_beamline = Quantity(
        type=str,
        description='''
        Name of the beamline the experiment took place.
        ''')

    general_source_pump = Quantity(
        type=str,
        description='''
        Name or model of the pump light source.
        ''')

    general_source_probe = Quantity(
        type=str,
        description='''
        Name or model of the probe light source.
        ''')

    number_of_axes = Quantity(
        type=int,
        description='''
        Number of axes in the measurement hardware.
        ''')

    general_measurement_axis = Quantity(
        type=str,
        shape=['number_of_axes'],
        description='''
        Names of the axes in the measurement hardware.
        ''')

    general_physical_axis = Quantity(
        type=str,
        shape=['number_of_axes'],
        description='''
        Names of the axes in physical terms.
        ''')

    source_pump_repetition_rate = Quantity(
        type=np.dtype(np.float64),
        unit='hertz',
        description='''
        Repetition rate of the pump source.
        ''')

    source_pump_pulse_duration = Quantity(
        type=np.dtype(np.float64),
        unit='femtosecond',
        description='''
        Pulse duration of the pump source.
        ''')

    source_pump_wavelength = Quantity(
        type=np.dtype(np.float64),
        unit='nanometer',
        description='''
        Center wavelength of the pump source.
        ''')

    source_pump_spectrum = Quantity(
        type=np.dtype(np.float64),
        shape=['length_of_spectrum'],
        description='''
        Spectrum of the pump source.
        ''')

    source_pump_photon_energy = Quantity(
        type=np.dtype(np.float64),
        unit='electron_volt',
        description='''
        Photon energy of the pump source.
        ''')

    source_pump_size = Quantity(
        type=np.dtype(np.float64),
        shape=['none_shape'],
        unit='millimeter ** 2',
        description='''
        Full-width at half-maximum (FWHM) of the pump source size at or closest to the
        sample position.
        ''')

    source_pump_fluence = Quantity(
        type=np.dtype(np.float64),
        shape=['none_shape'],
        unit='millijoule / millimeter ** 2',
        description='''
        Fluence of the pump source at or closest to the sample position.
        ''')

    source_pump_polarization = Quantity(
        type=str,
        description='''
        Polarization of the pump source.
        ''')

    source_pump_bunch = Quantity(
        type=np.dtype(np.int32),
        description='''
        Total bunch number of the pump source.
        ''')

    source_probe_repetition_rate = Quantity(
        type=np.dtype(np.float64),
        unit='hertz',
        description='''
        Repetition rate of the probe source.
        ''')

    source_probe_pulse_duration = Quantity(
        type=np.dtype(np.float64),
        unit='femtosecond',
        description='''
        Pulse duration of the probe source.
        ''')

    source_probe_wavelength = Quantity(
        type=np.dtype(np.float64),
        unit='nanometer',
        description='''
        Center wavelength of the probe source.
        ''')

    length_of_spectrum = Quantity(
        type=int,
        description='''
        Number of pixel elements in the spectrum.
        ''')

    source_probe_spectrum = Quantity(
        type=np.dtype(np.float64),
        shape=['length_of_spectrum'],
        description='''
        Spectrum of the probe source.
        ''')

    source_probe_photon_energy = Quantity(
        type=np.dtype(np.float64),
        unit='electron_volt',
        description='''
        Photon energy of the probe source.
        ''')

    source_probe_size = Quantity(
        type=np.dtype(np.float64),
        shape=['none_shape'],
        unit='millimeter ** 2',
        description='''
        Full-width at half-maximum (FWHM) of the probe source size at or closest to the
        sample position.
        ''')

    source_probe_fluence = Quantity(
        type=np.dtype(np.float64),
        shape=['none_shape'],
        unit='millijoule / millimeter ** 2',
        description='''
        Fluence of the probe source at or closest to the sample position.
        ''')

    source_probe_polarization = Quantity(
        type=str,
        description='''
        Polarization of the probe source.
        ''')

    source_probe_bunch = Quantity(
        type=np.dtype(np.int32),
        description='''
        Total bunch number of the probe source.
        ''')

    source_temporal_resolution = Quantity(
        type=np.dtype(np.float64),
        unit='femtosecond',
        description='''
        Full-width at half-maximum (FWHM) of the pump-probe cross-correlation function.
        ''')

    detector_extractor_voltage = Quantity(
        type=np.dtype(np.float64),
        unit='volt',
        description='''
        Voltage between the extractor and the sample.
        ''')

    detector_work_distance = Quantity(
        type=np.dtype(np.float64),
        unit='millimeter',
        description='''
        Distance between the sample and the detector entrance.
        ''')

    number_of_lenses = Quantity(
        type=int,
        description='''
        Number of electron lenses in the electron detector.
        ''')

    detector_lens_names = Quantity(
        type=str,
        shape=['number_of_lenses'],
        description='''
        Set of names for the electron-optic lenses.
        ''')

    detector_lens_voltages = Quantity(
        type=np.dtype(np.float64),
        shape=['number_of_lenses'],
        unit='volt',
        description='''
        Set of electron-optic lens voltages.
        ''')

    detector_tof_distance = Quantity(
        type=np.dtype(np.float64),
        unit='meter',
        description='''
        Drift distance of the time-of-flight tube.
        ''')

    number_of_tof_voltages = Quantity(
        type=int,
        description='''
        Number of time-of-flight (TOF) drift tube voltage values in the electron detector.
        ''')

    detector_tof_voltages = Quantity(
        type=np.dtype(np.float64),
        shape=['number_of_tof_voltages'],
        unit='volt',
        description='''
        Voltage applied to the time-of-flight tube.
        ''')

    detector_sample_bias = Quantity(
        type=np.dtype(np.float64),
        unit='volt',
        description='''
        Voltage bias applied to sample.
        ''')

    detector_magnification = Quantity(
        type=np.dtype(np.float64),
        description='''
        Detector magnification.
        ''')

    number_of_detector_voltages = Quantity(
        type=int,
        description='''
        Number of detector voltage settings in the electron detector.
        ''')

    detector_voltages = Quantity(
        type=np.dtype(np.float64),
        shape=['number_of_detector_voltages'],
        unit='volt',
        description='''
        Voltage applied to detector.
        ''')

    detector_type = Quantity(
        type=str,
        description='''
        Description of the detector type (e.g. ‘MCP’, ‘CCD’, ‘CMOS’, etc.).
        ''')

    number_of_sensor_sizes = Quantity(
        type=int,
        description='''
        Number of detector sensor size dimensions (depending on the number of sensors).
        ''')

    detector_sensor_size = Quantity(
        type=np.dtype(np.float64),
        shape=['number_of_sensor_sizes'],
        unit='millimeter',
        description='''
        Size of each of the imaging sensor chip on the detector.
        ''')

    detector_sensor_count = Quantity(
        type=np.dtype(np.int32),
        description='''
        Number of imaging sensor chips on the detector.
        ''')

    detector_sensor_pixel_size = Quantity(
        type=np.dtype(np.float64),
        shape=['none_shape'],
        unit='micrometer',
        description='''
        Pixel size of the imaging sensor chip on the detector.
        ''')

    number_of_momentum_calibration_coefficients = Quantity(
        type=int,
        description='''
        Number of the momentum calibration parameters for the detector.
        ''')

    detector_calibration_x_to_momentum = Quantity(
        type=np.dtype(np.float64),
        shape=['number_of_momentum_calibration_coefficients'],
        unit='1 / angstrom',
        description='''
        Pixel x axis to kx momentum calibration.
        ''')

    detector_calibration_y_to_momentum = Quantity(
        type=np.dtype(np.float64),
        shape=['number_of_momentum_calibration_coefficients'],
        unit='1 / angstrom',
        description='''
        Pixel y axis to ky momentum calibration.
        ''')

    number_of_energy_calibration_coefficients = Quantity(
        type=int,
        description='''
        Number of the energy calibration parameters for the detector.
        ''')

    detector_calibration_tof_to_energy = Quantity(
        type=np.dtype(np.float64),
        shape=['number_of_energy_calibration_coefficients'],
        unit='electron_volt',
        description='''
        Time-of-flight to energy calibration.
        ''')

    detector_calibration_stage_to_delay = Quantity(
        type=np.dtype(np.float64),
        shape=['number_of_delay_calibration_coefficients'],
        unit='femtosecond',
        description='''
        Translation stage position to pump-probe delay calibration.
        ''')

    number_of_other_calibration_coefficients = Quantity(
        type=int,
        description='''
        Number of the other calibration parameters for the detector.
        ''')

    detector_calibration_other_converts = Quantity(
        type=np.dtype(np.float64),
        shape=['number_of_other_calibration_coefficients'],
        description='''
        Conversion factor between other measured and physical axes.
        ''')

    detector_momentum_resolution = Quantity(
        type=np.dtype(np.float64),
        shape=['none_shape'],
        unit='1 / angstrom',
        description='''
        Momentum resolution of the detector.
        ''')

    detector_spatial_resolution = Quantity(
        type=np.dtype(np.float64),
        shape=['none_shape'],
        unit='micrometer',
        description='''
        Spatial resolution of the source.
        ''')

    detector_energy_resolution = Quantity(
        type=np.dtype(np.float64),
        shape=['none_shape'],
        unit='electron_volt',
        description='''
        Energy resolution of the detector.
        ''')


class Sample(common_experimental.Sample):

    sample_state_of_matter = Quantity(
        type=str,
        description='''
        Physical state of the sample.
        ''')

    sample_purity = Quantity(
        type=np.dtype(np.float64),
        description='''
        Chemical purity of the sample.
        ''')

    sample_surface_termination = Quantity(
        type=str,
        description='''
        Surface termination of the sample (if crystalline).
        ''')

    sample_layers = Quantity(
        type=str,
        description='''
        Sample layer or bulk structure.
        ''')

    sample_stacking_order = Quantity(
        type=str,
        description='''
        Stacking order of the solid surface (if crystalline).
        ''')

    sample_chemical_id_cas = Quantity(
        type=str,
        description='''
        CAS registry number of the sample’s chemical content.
        ''')

    sample_pressure = Quantity(
        type=np.dtype(np.float64),
        unit='pascal',
        description='''
        Pressure surrounding the sample at the time of measurement.
        ''')

    sample_growth_method = Quantity(
        type=str,
        description='''
        Sample growth method.
        ''')

    sample_preparation_method = Quantity(
        type=str,
        description='''
        Sample preparation method.
        ''')

    sample_vendor = Quantity(
        type=str,
        description='''
        Name of the sample vendor.
        ''')

    sample_substrate_material = Quantity(
        type=str,
        description='''
        Material of the substrate the sample has immediate contact with.
        ''')

    sample_substrate_state_of_matter = Quantity(
        type=str,
        description='''
        State of matter of the substrate material.
        ''')

    sample_substrate_vendor = Quantity(
        type=str,
        description='''
        Name of the substrate vendor.
        ''')


m_package.__init_metainfo__()
