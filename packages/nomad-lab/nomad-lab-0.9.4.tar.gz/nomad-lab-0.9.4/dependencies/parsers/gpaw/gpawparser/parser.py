# Copyright 2015-2018 Mikkel Strange, Fawzi Mohamed, Ankit Kariryaa, Ask Hjorth Larsen, Jens Jørgen Mortensen
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

from __future__ import division
import os
import logging
from contextlib import contextmanager
import numpy as np
from ase.data import chemical_symbols
# import setup_paths
from nomadcore.unit_conversion.unit_conversion import convert_unit as cu
from nomadcore.local_meta_info import loadJsonFile, InfoKindEl
from gpawparser.tar import Reader
from gpawparser.libxc_names import get_libxc_xc_names
from gpawparser.versions import get_prog_version

@contextmanager
def open_section(p, name):
    gid = p.openSection(name)
    yield gid
    p.closeSection(name, gid)


def c(value, unit=None):
    """ Dummy function for unit conversion"""
    return cu(value, unit)


parser_info = {"name": "parser_gpaw", "version": "1.0"}
path = '../../../../nomad-meta-info/meta_info/nomad_meta_info/' +\
        'gpaw.nomadmetainfo.json'

class GPAWParserWrapper():
    """ A proper class envolop for running this parser using Noamd-FAIRD infra. """
    def __init__(self, backend, **kwargs):
        self.backend_factory = backend

    def parse(self, mainfile):
        logging.info('GPAW parser started')
        logging.getLogger('nomadcore').setLevel(logging.WARNING)
        backend = self.backend_factory("gpaw.nomadmetainfo.json")
        backend = parse_without_class(mainfile, backend)
        return backend

def parse_without_class(filename, backend):
    p = backend
    o = open_section
    r = Reader(filename)
    p.startedParsingSession(filename, parser_info)

    with o(p, 'section_run'):
        p.addValue('program_name', 'GPAW')
        p.addValue('program_version', get_prog_version(r.version))
        if r.Mode == 'pw':
            p.addValue('program_basis_set_type', 'plane waves')
            with o(p, 'section_basis_set_cell_dependent'):
                p.addValue('basis_set_cell_dependent_name',
                           'PW_%.1f_Ry' % (r.PlaneWaveCutoff * 2.0))  # in Ry
                p.addRealValue('basis_set_planewave_cutoff',
                               c(r.PlaneWaveCutoff, 'hartree'))
        elif r.Mode == 'fd':
            with o(p, 'section_basis_set_cell_dependent'):
                h1 = np.linalg.norm(r.UnitCell[0]) / r.dims['ngptsx']
                h2 = np.linalg.norm(r.UnitCell[1]) / r.dims['ngptsy']
                h3 = np.linalg.norm(r.UnitCell[2]) / r.dims['ngptsz']
                h = (h1 + h2 + h3) / 3.0
                p.addValue('basis_set_cell_dependent_name',
                           'GR_%.1f' % (c(h, 'bohr') * 1.0E15))  # in fm
        elif r.Mode == 'lcao':
            p.addValue('program_basis_set_type', 'numeric AOs')
            with o(p, 'section_basis_set_atom_centered'):
                p.addValue('basis_set_atom_centered_short_name', r.BasisSet)
        with o(p, 'section_system') as system_gid:
            p.addArrayValues('simulation_cell', c(r.UnitCell, 'bohr'))
            symbols = np.array([chemical_symbols[z] for z in r.AtomicNumbers])
            p.addArrayValues('atom_labels', symbols)
            p.addArrayValues('atom_positions', c(r.CartesianPositions, 'bohr'))
            if r.Mode == 'pw':
                pbc = np.array((1, 1, 1), bool)
            else:
                pbc = np.array(r.BoundaryConditions, bool)
            p.addArrayValues('configuration_periodic_dimensions', pbc)
        with o(p, 'section_sampling_method'):
            p.addValue('ensemble_type', 'NVE')
        with o(p, 'section_frame_sequence'):
            pass
        with o(p, 'section_method') as method_gid:
            p.addValue('relativity_method', 'pseudo_scalar_relativistic')
            p.addValue('electronic_structure_method', 'DFT')
            p.addValue('scf_threshold_energy_change', c(r.EnergyError,
                                                        'hartree'))
            if 'FixMagneticMoment' in r:
                p.addValue('x_gpaw_fix_magnetic_moment',
                           r.FixMagneticMoment)
                if r.FixMagneticMoment:
                    p.addValue('x_gpaw_fixed_spin_Sz',
                               r.MagneticMoments.sum() / 2.)
            if 'FermiWidth' in r:
                p.addValue('smearing_kind', 'fermi')
                p.addRealValue('smearing_width',
                               c(r.FermiWidth, 'hartree'))
            if 'FixDensity' in r:
                p.addValue('x_gpaw_fix_density', r.FixDensity)
            if 'DensityConvergenceCriterion' in r:
                p.addRealValue('x_gpaw_density_convergence_criterion',
                               r.DensityConvergenceCriterion)
            if 'MixClass' in r:
                p.addValue('x_gpaw_mix_class', r.MixClass)
            if 'MixBeta' in r:
                p.addValue('x_gpaw_mix_beta', r.MixBeta)
            if 'MixWeight' in r:
                p.addValue('x_gpaw_mix_weight', r.MixWeight)
            if 'MixOld' in r:
                p.addValue('x_gpaw_mix_old', r.MixOld)
            if 'MaximumAngularMomentum' in r:
                p.addValue('x_gpaw_maximum_angular_momentum',
                           r.MaximumAngularMomentum)
            if 'SymmetryTimeReversalSwitch' in r:
                p.addValue('x_gpaw_symmetry_time_reversal_switch',
                           r.SymmetryTimeReversalSwitch)
            p.addValue('x_gpaw_xc_functional', r.XCFunctional)
            xc_names = get_libxc_xc_names(r.XCFunctional)
            for name in xc_names.values():
                if name is not None:
                    with o(p, 'section_XC_functionals'):
                        p.addValue('XC_functional_name', name)
        with o(p, 'section_single_configuration_calculation'):
            p.addValue('single_configuration_calculation_to_system_ref',
                       system_gid)
            p.addValue('single_configuration_to_calculation_method_ref',
                       method_gid)
            p.addRealValue('energy_total', c(r.Epot, 'hartree'))
            p.addRealValue('energy_XC', c(r.Exc, 'hartree'))
            p.addRealValue('electronic_kinetic_energy', c(r.Ekin, 'hartree'))
            p.addRealValue('energy_correction_entropy', c(r.S, 'hartree'))
            if 'CartesianForces' in r:
                p.addArrayValues('atom_forces_free',
                                 c(r.CartesianForces, 'bohr/hartree'))
            p.addArrayValues('x_gpaw_magnetic_moments', r.MagneticMoments)
            p.addRealValue('x_gpaw_spin_Sz', r.MagneticMoments.sum() / 2.0)
            #p.addArrayValues('x_gpaw_atomic_density_matrices',
            #                 r.AtomicDensityMatrices)
            #p.addArrayValues('x_gpaw_projections_real', r.Projections.real)
            #p.addArrayValues('x_gpaw_projections_imag', r.Projections.imag)
            with o(p, 'section_eigenvalues'):
                p.addValue('eigenvalues_kind', 'normal')
                p.addArrayValues('eigenvalues_values',
                                 c(r.Eigenvalues, 'hartree'))
                p.addArrayValues('eigenvalues_occupation', r.OccupationNumbers)
                p.addArrayValues('eigenvalues_kpoints', r.IBZKPoints)
    p.finishedParsingSession("ParseSuccess", None)
    return p  # Return the backend

if __name__ == '__main__':
    import sys
    filename = sys.argv[1]
    parse(filename)
