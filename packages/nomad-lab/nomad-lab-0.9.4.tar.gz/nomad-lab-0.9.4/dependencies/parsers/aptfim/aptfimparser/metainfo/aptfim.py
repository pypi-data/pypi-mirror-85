from nomad.metainfo import Package, Quantity, Section
from nomad.datamodel.metainfo import common_experimental

m_package = Package(name='aptfim')


class Method(common_experimental.Method):

    m_def = Section(validate=False, extends_base_section=True)

    experiment_operation_method = Quantity(
        type=str,
        description='Operation mode of the instrument (APT, FIM or combination)')

    experiment_imaging_method = Quantity(
        type=str,
        description='Pulsing method to enforce a controlled ion evaporation sequence')

    number_ions_evaporated = Quantity(
        type=int,
        description='Number of ions successfully evaporated')

    measured_detector_hit_pos = Quantity(
        type=bool,
        description='Detector hit positions x and y was measured')

    measured_detector_hit_mult = Quantity(
        type=bool,
        description='Detector hit multiplicity was measured')

    measured_detector_dead_pulses = Quantity(
        type=bool,
        description='Detector number of dead pulses was measured')

    measured_time_of_flight = Quantity(
        type=bool,
        description='Raw ion time of flight was measured')

    measured_standing_voltage = Quantity(
        type=bool,
        description='Standing voltage was measured')

    measured_pulse_voltage = Quantity(
        type=bool,
        description='Pulse voltage was measured')


m_package.__init_metainfo__()
