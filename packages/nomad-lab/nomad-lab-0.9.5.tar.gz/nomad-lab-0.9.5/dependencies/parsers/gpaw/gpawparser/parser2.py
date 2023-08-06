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
from contextlib import contextmanager
import numpy as np
import logging
from ase import units
from ase.data import chemical_symbols
from ase.io.ulm import ulmopen
from ase.utils import basestring
#from ase.io.trajectory import read_atoms
from ase.data import atomic_masses
from ase.units import Rydberg
from nomadcore.unit_conversion.unit_conversion import convert_unit as cu
from nomadcore.local_meta_info import loadJsonFile, InfoKindEl
from gpawparser.libxc_names import get_libxc_name
from gpawparser.default_parameters import parameters as parms


@contextmanager
def open_section(p, name):
    gid = p.openSection(name)
    yield gid
    p.closeSection(name, gid)


def c(value, unit=None):
    """ Dummy function for unit conversion"""
    return cu(value, unit)


parser_info = {"name": "parser2_gpaw", "version": "1.0"}
path = '../../../../nomad-meta-info/meta_info/nomad_meta_info/' +\
        'gpaw.nomadmetainfo.json'

class GPAWParser2Wrapper():
    """ A proper class envolop for running this parser using Noamd-FAIRD infra. """
    def __init__(self, backend, **kwargs):
        self.backend_factory = backend

    def parse(self, mainfile):
        logging.info('GPAW parser 2 (note the 2) started')
        logging.getLogger('nomadcore').setLevel(logging.WARNING)
        backend = self.backend_factory("gpaw.nomadmetainfo.json")
        backend = parse_without_class(mainfile, backend)
        return backend


def parse_without_class(filename, backend):
    p = backend
    o = open_section
    r = ulmopen(filename) #  Reader(filename)
    p.startedParsingSession(filename, parser_info)
    parms.update(r.parameters.asdict())
    with o(p, 'section_run'):
        p.addValue('program_name', 'GPAW')
        p.addValue('program_version', r.gpaw_version)
        mode = parms['mode']
        if isinstance(mode, basestring):
            mode = {'name': mode}
        if mode['name'] == 'pw':
            p.addValue('program_basis_set_type', 'plane waves')
            with o(p, 'section_basis_set_cell_dependent'):
                p.addValue('basis_set_cell_dependent_name',
                           'PW_%.1f_Ry' % (mode['ecut'] / r.ha * 2))  # in Ry
                p.addRealValue('basis_set_planewave_cutoff',
                               c(mode['ecut'], 'eV'))
        elif mode['name'] == 'fd':
            p.addValue('program_basis_set_type', 'real space grid')
            with o(p, 'section_basis_set_cell_dependent'):
                cell = r.atoms.cell
                ngpts = r.density.density.shape
                h1 = np.linalg.norm(cell[0]) / ngpts[0]
                h2 = np.linalg.norm(cell[1]) / ngpts[1]
                h3 = np.linalg.norm(cell[2]) / ngpts[2]
                h = (h1 + h2 + h3) / 3.0
                p.addValue('basis_set_cell_dependent_name',
                           'GR_%.1f' % (c(h, 'angstrom') * 1.0E15))  # in fm
        elif mode['name'] == 'lcao':
            p.addValue('program_basis_set_type', 'numeric AOs')
            with o(p, 'section_basis_set_atom_centered'):
                p.addValue('basis_set_atom_centered_short_name',
                          parms['basis'])
        with o(p, 'section_system') as system_gid:
            p.addArrayValues('simulation_cell',
                             c(r.atoms.cell, 'angstrom'))
            symbols = np.array([chemical_symbols[z] for z in r.atoms.numbers])
            p.addArrayValues('atom_labels', symbols)
            p.addArrayValues('atom_positions', c(r.atoms.positions, 'angstrom'))
            p.addArrayValues('configuration_periodic_dimensions',
                             np.array(r.atoms.pbc, bool))
            if 'momenta' in r.atoms:
                masses = atomic_masses[r.atoms.numbers]
                velocities = r.atoms.momenta / masses.reshape(-1, 1)
                p.addArrayValues('atom_velocities',
                                c(velocities * units.fs / units.Angstrom,
                                  'angstrom/femtosecond'))
        with o(p, 'section_sampling_method'):
            p.addValue('ensemble_type', 'NVE')
        with o(p, 'section_frame_sequence'):
            pass
        with o(p, 'section_method') as method_gid:
            p.addValue('relativity_method', 'pseudo_scalar_relativistic')
            p.addValue('electronic_structure_method', 'DFT')
            p.addValue('scf_threshold_energy_change',
                       c(parms['convergence']['energy'], 'eV')) # eV / electron
            #if r.FixMagneticMoment:
            #    p.addValue('x_gpaw_fixed_spin_Sz',
            #               r.MagneticMoments.sum() / 2.)
            if parms['occupations'] is None:  # use default values
                if tuple(parms['kpts']) == (1, 1, 1):
                    width = 0.0
                else:
                    width = 0.1
                parms['occupations'] = {'width': width, 'name': 'fermi-dirac'}

            p.addValue('smearing_kind', parms['occupations']['name'])
            p.addRealValue('smearing_width',
                               c(parms['occupations']['width'], 'eV'))
            p.addRealValue('total_charge', parms['charge'])
            with o(p, 'section_XC_functionals'):
                p.addValue('XC_functional_name',
                           get_libxc_name(parms['xc']))
        with o(p, 'section_single_configuration_calculation'):
            p.addValue('single_configuration_calculation_to_system_ref',
                       system_gid)
            p.addValue('single_configuration_to_calculation_method_ref',
                       method_gid)
            p.addValue('single_configuration_calculation_converged',
                      r.scf.converged)
            p.addRealValue('energy_total',
                           c(r.hamiltonian.e_total_extrapolated, 'eV'))
            p.addRealValue('energy_free',
                           c(r.hamiltonian.e_total_free, 'eV'))
            p.addRealValue('energy_XC', c(r.hamiltonian.e_xc, 'eV'))
            p.addRealValue('electronic_kinetic_energy',
                           c(r.hamiltonian.e_kinetic, 'eV'))
            p.addRealValue('energy_correction_entropy',
                           c(r.hamiltonian.e_entropy, 'eV'))
            nspin = r.density.density.shape[0]
            ef = r.occupations.fermilevel
            fermilevels = np.zeros(nspin)
            if nspin == 1:
                fermilevels[:] = ef
            elif nspin == 2:
                split = r.occupations.split
                fermilevels[0] = ef + 0.5 * split
                fermilevels[1] = ef - 0.5 * split
            p.addArrayValues('energy_reference_fermi',
                             c(fermilevels, 'eV'))

            # Load 3D arrays ("volumetric data")
            origin = -0.5 * r.atoms.cell.sum(axis=0)
            npoints = np.array(r.density.density.shape[1:])
            npoints[~r.atoms.pbc] += 1
            displacements = r.atoms.cell / npoints

            def add_3d_array(values, kind, unit):
                with o(p, 'section_volumetric_data'):
                    p.addArrayValues('volumetric_data_origin',
                                     c(origin, 'angstrom'))
                    p.addArrayValues('volumetric_data_displacements',
                                     c(displacements, 'angstrom'))
                    p.addArrayValues('volumetric_data_values',
                                     c(values, unit))
                    p.addValue('volumetric_data_kind', kind)

            # H.atom.ulm.gpw test can be used to verify that pseudodensity
            # integrates to 0.98, corresponding closely to the norm of the
            # H 1s pseudowavefunction (see output of "gpaw-setup H").
            # It has mixed BCs so this should show that npoints is taken
            # care of correctly, hopefully.
            add_3d_array(r.density.density, kind='density',
                         unit='angstrom**(-3)')
            add_3d_array(r.hamiltonian.potential, kind='potential_effective',
                         unit='eV*angstrom**(-3)')

            if 'forces' in r.results:
                p.addArrayValues('atom_forces_free_raw',
                                 c(r.results.forces, 'eV/angstrom'))
            if 'magmons' in r.results:
                p.addArrayValues('x_gpaw_magnetic_moments',
                                 r.results.magmoms)
                p.addRealValue('x_gpaw_spin_Sz', r.results.magmoms.sum() / 2.0)
            #p.addArrayValues('x_gpaw_atomic_density_matrices',
            #                 r.AtomicDensityMatrices)
            #p.addArrayValues('x_gpaw_projections_real', r.Projections.real)
            #p.addArrayValues('x_gpaw_projections_imag', r.Projections.imag)
            with o(p, 'section_eigenvalues'):
                p.addValue('eigenvalues_kind', 'normal')
                p.addArrayValues('eigenvalues_values',
                                 c(r.wave_functions.eigenvalues, 'eV'))
                p.addArrayValues('eigenvalues_occupation',
                                 r.wave_functions.occupations)
                #p.addArrayValues('eigenvalues_kpoints', r.IBZKPoints)
            if 'band_paths' in r.wave_functions: # could change
                with o(p, 'section_k_band'):
                    for band_path in r.wave_functions.band_paths:
                        with o(p, 'section_k_band_segment'):
                            p.addArrayValues('band_energies',
                                            c(band_path.eigenvalues, 'eV'))
                            p.addArrayValues('band_k_points', 'eV',
                                             band_path.kpoints)
                            p.addArrayValues('band_segm_labels',
                                            band_path.labels)
                            p.addArrayValues('band_segm_start_end',
                                             np.asarray(
                                                 [band_path.kpoints[0],
                                                  band_path.kpoints[-1]]))


    p.finishedParsingSession("ParseSuccess", None)
    return p

if __name__ == '__main__':
    import sys
    filename = sys.argv[1]
    parse(filename)
