# Copyright 2016-2018 Ask Hjorth Larsen, Fawzi Mohamed
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# Main author and maintainer: Ask Hjorth Larsen <asklarsen@gmail.com>

from __future__ import print_function
import os
import sys
import re
import logging

import numpy as np
from ase import Atoms
from ase.spacegroup import crystal
#from ase.data import chemical_symbols

from nomadcore.simple_parser import mainFunction, SimpleMatcher as SM
from nomadcore.local_meta_info import loadJsonFile, InfoKindEl
from nomadcore.unit_conversion.unit_conversion \
    import register_userdefined_quantity, convert_unit

from .functionals import functionals


parser_info = {'name': 'molcas-parser', 'version': '1.0'}

# OK
#    "program_basis_set_type",
#    "program_name",
#    "program_version",
#    "configuration_periodic_dimensions"
#    "simulation_cell",  # molcas never has a cell



#    "atom_labels",
#    "atom_positions",
#    "energy_total",

#    'section_system',
#    'section_method',
#    'section_frame_sequence',
#    'section_sampling_method',
#    'single_configuration_to_calculation_method_ref',
#    'single_configuration_calculation_to_system_ref',
#    'atom_forces_raw',
#    'frame_sequence_local_frames_ref',
#    'frame_sequence_to_sampling_ref',

#    'XC_functional_name',
#    'smearing_kind',
#    'smearing_width'
#    'eigenvalues_kpoints',
#    'eigenvalues_values',
#    'eigenvalues_occupation',
#    'band_k_points',
#    'band_energies',
#    'band_segm_start_end',
#    'band_segm_labels',
#    'dos_energies',
#    'dos_values',
#    'section_XC_functionals',



class MolcasContext(object):
    def __init__(self):
        self.data = {}
        self.last_line = None
        self.current_module_name = None
        self.section_refs = {}
        self.basis_info = []
        self.buffered_lines = {}

    def onOpen_section_method(self, backend, gindex, section):
        self.section_refs['method'] = gindex

    def onOpen_section_system(self, backend, gindex, section):
        self.section_refs['system'] = gindex

    def startedParsing(self, fname, parser):
        pass

    def adhoc_store_line(self, parser):
        self.last_line = parser.fIn.readline()

    def adhoc_pushback_last(self, parser):
        assert self.last_line is not None
        parser.fIn.pushbackLine(self.last_line)
        self.last_line = None

    def onClose_section_single_configuration_calculation(self, backend, gindex, section):
        backend.addValue('single_configuration_to_calculation_method_ref',
                         self.section_refs['method'])
        backend.addValue('single_configuration_calculation_to_system_ref',
                         self.section_refs['system'])

        #print(self.buffered_lines.keys())

        def lines2arrays(name):
            elines = self.buffered_lines.pop('energy_%s' % name)
            olines = self.buffered_lines.pop('occupations_%s' % name)
            energies = []
            occupations = []
            assert len(elines) == len(olines)
            for l1, l2 in zip(elines, olines):
                energies += l1.split()[1:]  # Energy <numbers>
                occupations += l2.split()[2:]  # Occ. No.  <numbers>
            assert len(energies) == len(occupations)
            energies = np.array(energies).astype(float)
            energies = convert_unit(energies, 'hartree')
            occupations = np.array(occupations).astype(float)

            # Sort by energy:
            args = np.argsort(energies)
            energies = energies[args]
            occupations = occupations[args]
            return energies.reshape(1, 1, -1), occupations.reshape(1, 1, -1)

        energies = None

        try:
            energies, occupations = lines2arrays('nospin')
            nspins = 1
            nstates = energies.shape[-1]
        except KeyError:
            pass

        try:
            ealpha, oalpha = lines2arrays('alpha')
            ebeta, obeta = lines2arrays('beta')
        except KeyError:
            pass
        else:
            # The spinup and spindown (alpha, beta)
            # arrays can have different lengths
            # so we must allocate arrays that are big enough
            # and fill out with zeros or something else
            assert energies is None
            nspins = 2
            nstates = max(ealpha.shape[-1], ebeta.shape[-1])
            energies = np.empty((nspins, 1, nstates))
            # We will only fill out the values that we have.
            # The rest will be nan:
            energies.fill(np.nan)
            occupations = np.zeros((nspins, 1, nstates))
            energies[0, :, :ealpha.shape[2]] = ealpha[0]
            occupations[0, :, :ealpha.shape[2]] = oalpha[0]
            energies[1, 0, :ebeta.shape[2]] = ebeta[0]
            occupations[1, 0, :ebeta.shape[2]] = obeta[0]

        if energies is not None:
            for arr in [energies, occupations]:
                assert arr.shape == (nspins, 1, nstates)
            g = backend.openSection('section_eigenvalues')
            backend.addArrayValues('eigenvalues_values', energies)
            backend.addArrayValues('eigenvalues_occupation', occupations)
            backend.closeSection('section_eigenvalues', g)


    def onClose_section_method(self, backend, gindex, section):

        for line in self.basis_info:
            m = re.match('\s*Basis set label:(.*?)\.(.*?)\s*$', line)
            atomlabel, name = m.group(1, 2)
            # The terrible syntax in molcas has a lot of dots everywhere.
            # Replace sequences of dots with single dots to make things
            # reasonable.
            name = re.sub(r'\.+', '.', name).strip('.')
            g = backend.openSection('x_molcas_section_basis')
            backend.addValue('x_molcas_basis_atom_label', atomlabel)
            backend.addValue('x_molcas_basis_name', name)
            backend.closeSection('x_molcas_section_basis', g)
        del self.basis_info[:]

        #print('SECTION', section)
        #methods = section['x_molcas_method']
        xc = []

        methods = section['x_molcas_method_name']
        assert len(methods) == 1, methods
        method = methods[0]

        uhf = method.startswith('UHF ')
        if uhf:
            method = method[4:].strip()
        backend.addValue('x_molcas_uhf', uhf)

        if method == 'SCF':
            # XXX distinguish somehow between these two?
            esm = 'DFT'
            xc = ['HF_X']
        elif method in ['RASSCF', 'RAS-CI', 'CASPT2', 'CCSDT']:
            esm = method
        elif method in ['CASVB', 'MRCI']:
            esm = 'MRCISD'
        elif method == 'MCPF':
            esm = method  ## Not defined by nomad
        elif method == 'MBPT2':
            esm = 'MP2'
        elif method in functionals:
            esm = 'DFT'
            xc = functionals[method]
            assert xc is not None, 'no xc: %s' % method
        else:
            raise ValueError('method: %s' % method)

        backend.addValue('electronic_structure_method', esm)
        for xcfunc in xc:
            g = backend.openSection('section_XC_functionals')
            backend.addValue('XC_functional_name', xcfunc)
            backend.closeSection('section_XC_functionals', g)


        if 0:
            if methods is not None:
                assert len(methods) == 1
                method = methods[0]
                scfnames = section['x_molcas_method_name']
                assert len(scfnames) == 1, scfnames
                scfname = scfnames[0]
                if scfname == 'SCF':
                    backend.addValue('electronic_structure_method', 'DFT')
                    g = backend.openSection('section_XC_functionals')
                    backend.addValue('XC_functional_name', 'HF_X')
                    backend.closeSection('section_XC_functionals', g)

        #print(self.current_module_name)
        #scftype = section['x_molcas_method_name']
        #if scftype is not None:
        #    print('SCF', scftype)

    def onClose_section_system(self, backend, gindex, section):
        matrix = self.data.pop('coordinates')
        assert matrix.shape[1] == 4
        atom_labels = matrix[:, 0]
        coords = matrix[:, 1:4].astype(float)
        assert coords.shape[1] == 3
        coords = convert_unit(coords, 'bohr')

        backend.addArrayValues('atom_labels', atom_labels)
        backend.addArrayValues('atom_positions', coords)
        backend.addArrayValues('configuration_periodic_dimensions', np.zeros(3, bool))

    def adhoc_add_basis_set(self, parser):
        line = parser.fIn.readline()
        self.basis_info.append(line)

    def adhoc_add_energies(self, parser):
        line = parser.fIn.readline()
        self.energies.append(line)

    def adhoc_add_occupations(self, parser):
        line = parser.fIn.readline()
        self.occupations.append(line)

    # multi_sm copied from Siesta/GULP
    def multi_sm(self, name, startpattern, linepattern, endmatcher=None,
                 conflict='fail',  # 'fail', 'keep', 'overwrite'
                 *args, **kwargs):

        pat = re.compile(linepattern)  # XXX how to get compiled pattern?
        ngroups = pat.groups

        allgroups = []
        def addline(parser):
            line = parser.fIn.readline()
            match = pat.match(line)
            assert match is not None
            thislinegroups = match.groups()
            assert len(thislinegroups) == ngroups
            allgroups.append(thislinegroups)

        def savearray(parser):
            arr = np.array(allgroups, dtype=object)
            del allgroups[:]
            if name in self.data:
                if conflict == 'fail':
                    raise ValueError('grrr %s %s' % (name, self.data[name]))
                elif conflict == 'keep':
                    return  # Do not save array
                elif conflict == 'overwrite':
                    pass
                else:
                    raise ValueError('Unknown keyword %s' % conflict)
            #if arr.size > 0:
            if arr.size == 0:
                arr.shape = (0, ngroups)
            self.data[name] = arr

        if endmatcher is None:
            endmatcher = r'.*'

        if hasattr(endmatcher, 'swapcase'):
            endmatcher = SM(endmatcher,
                            endReStr='',
                            forwardMatch=True,
                            name='%s-end' % name,
                            adHoc=savearray)

        sm = SM(startpattern,
                name=name,
                subMatchers=[
                    SM(linepattern,
                       name='%s-line' % name,
                       repeats=True,
                       forwardMatch=True,
                       required=True,
                       adHoc=addline),
                    endmatcher,
                ], **kwargs)
        return sm

context = MolcasContext()

#def get_inputfile_echo_sm():
#    m = SM(r'\+\+\s*----+\s*Input file\s*---+',
#           endReStr='--\s*-------+',
#           sections=['section_method'],
#           name='inputfile')
#    return m


def get_system_sm():
    m = SM(r'\s*Molecular structure info:',
           name='structure',
           sections=['section_system'],
           subMatchers=[
               SM(r'\s*--------+', name='bar'),
               SM(r'.*?Cartesian Coordinates / Bohr, Angstrom\s*\*+',
                  name='coords',
                  subMatchers=[
                      context.multi_sm('coordinates',
                                       r'\s*Center\s*Label\s*x\s*y\s*z\s*x\s*y\s*z',
                                       r'\s*\d+\s*(\S+)\s*(\S+)\s*(\S+)\s*(\S+)')
                  ])
           ])
    return m


def get_finalresults_sm():  # Other modes than SCF/KS-DFT?
    m = SM(r'\s*\*\s*SCF/KS-DFT Program, Final results',
           endReStr='\s*Molecular Properties',  # No clue when to really stop matching this
           sections=['section_single_configuration_calculation'],
           name='results',
           subMatchers=[
               SM(r'\s*Total SCF energy\s*(?P<energy_total__hartree>\S+)', name='etot')
           ])
    return m

def get_header_sm():
    m = SM(r'[\s^]*M O L C A S',
           endReStr=r'\s*For the author list and the recommended.*',
           name='header',
           subMatchers=[
               SM(r'[\s^]*version\s*(?P<program_version>.*?)\s*$',
                  name='version')
           ])
    return m

# Does not include 'auto'
molcas_modules = ('alaska|caspt2|casvb|ccsdt|cpf|expbas|ffpt|gateway|'
                  'genano|grid_it|guessorb|guga|last_energy|loprop|mbpt2|'
                  'mckinley|mclr|motra|mrci|numerical_gradient|rasscf|'
                  'rassi|scf|seward|slapaf|vibrot').split('|')

ignore_modules = {'alaska',  # OK
                  'numerical_gradient',  # OK
                  'rassi',  # OK
                  'motra',
                  'guga',
                  'ffpt',
                  'genano',
                  'grid_it',
                  'loprop',
                  'guessorb',
                  'expbas',
                  'vibrot',
                  'mckinley'
                  #'last_energy',
}

def get_anymodule_sms():
    sms = []
    for modulename in molcas_modules:
        adhoc = None
        if modulename not in ignore_modules:
            class AdHoc:
                def __init__(self, name):
                    self.name = name
                def __call__(self, parser):
                    raise ValueError('module: %s' % self.name)
            adhoc = AdHoc(modulename)
        sms.append(SM(r'--- Start Module:\s*%s' % modulename,
                      adHoc=adhoc,
                      name=modulename))
    return sms

#def module_sm(name, *args, **kwargs):
#    m = SM(r'--- Start Module:\s*(%s)' % name, *args, name=name, **kwargs)
#    return m

# mw = "module-wrapper" for SM
# The idea is to guarantee that matchers modules that do not always write a proper header (e.g. SLAPAF)
# are invoked when the module starts, but that the matcher's sections are only opened if recognizable
# output is written (sometimes they write nothing).
#
# Typically, pass a matcher which opens some sections but will only match actual output of the module
# This wrapper will call the wrapped matcher when the module is started, but the wrapped matcher
# will only match if the output is actually there, and also will only open its sections in that case.
def mw(modname, *args, **kwargs):
    m = SM(r'--- Start Module:\s*%s' % modname,
           name=modname,
           subMatchers=[
               SM(*args, **kwargs)
           ])
    return m

def mod_pattern(lower, upper=None):
    if upper is None:
        upper = lower.upper()
    return (r'---\s*Start Module:\s*{0}|'
            r'\s*MOLCAS executing module\s*{1}'.format(lower, upper))

# Define these separately or not?
def startmod_pattern(name):
    return r'---\s*Start Module:\s*{}'.format(name)
def execmod_pattern(name):
    return r'\s*MOLCAS executing module\s*{}'.format(name)

def gateway_seward():
    m = SM(mod_pattern(r'(:?gateway|seward)'),
           #weak=True,
           name='gate/seward',
           #r'\s*MOLCAS executing module (GATEWAY|SEWARD)', name='seward',
           subMatchers=[
               SM(r'\s*Basis set label:(.*?)\s*$',
                  forwardMatch=True,
                  repeats=True,
                  adHoc=context.adhoc_add_basis_set,
                  name='basis'),
               get_system_sm()
           ])
    return m

def eigenvalue_line_matcher(pattern, spinname):

    class AdHocLineAccumulator:
        def __init__(self, var):
            self.var = var

        def __call__(self, parser):
            line = parser.fIn.readline()
            context.buffered_lines.setdefault(self.var, []).append(line)
            #print(context.buffered_lines)
            #sdfkjsdfkj

    m = SM(pattern, name=spinname,
           subMatchers=[
               SM(r'\s*Orbital',
                  repeats=True,
                  subMatchers=[
                      SM(r'\s*Energy\s*(.*)', name='energies', adHoc=AdHocLineAccumulator('energy_%s' % spinname),
                         forwardMatch=True),
                      SM(r'\s*Occ\. No\.\s*(.*)', name='occ', adHoc=AdHocLineAccumulator('occupations_%s' % spinname),
                         forwardMatch=True)
                  ])
           ])
    return m

def scf_rasscf():
    m = SM(mod_pattern(r'(:?ras)?scf'),
           name='(ras)scf', #r'(?:ras)?scf', r'\s*MOLCAS executing module (?:SCF|RASSCF)', name='scf',
           #sections=['section_method', 'section_single_configuration_calculation'],
           subMatchers=[  # XXX opens method section even if there is no outpout
               SM(r'\s*(?P<x_molcas_method_name>.*?)\s*iterations: Energy and convergence statistics',
                  sections=['section_method'],
                  name='scfiter'),
               SM(r'\s*CI only, no orbital optimization',
                  sections=['section_method'],
                  fixedStartValues={'x_molcas_method_name': 'RAS-CI'}),
               SM(r'\s*\*\s*Final Results\s*\*',
                  name='finalresults',
                  sections=['section_single_configuration_calculation'],
                  subMatchers=[
                      SM(r'\s*Total \S+ energy\s*(?P<energy_total__hartree>\S+)', name='E-tot'),
                      SM(r'\s*RASSCF root number\s*\d+\s*Total energy\s*=\s*(?P<energy_total__hartree>\S+)', name='E-ras'),
                      SM(r'\s*Molecular orbitals:',
                         name='mol-orb',
                         endReStr=r'\s*Molecular Charges:',
                         subMatchers=[
                             eigenvalue_line_matcher(r'\s*Title:\s*.*?\s*orbitals\s*$', 'nospin'),
                             eigenvalue_line_matcher(r'\s*Title:\s*.*?\s*orbitals\s*\(alpha\)', 'alpha'),
                             eigenvalue_line_matcher(r'\s*Title:\s*.*?\s*orbitals\s*\(beta\)', 'beta')
                         ])
                  ])
           ])
    return m

def caspt2():
    m = SM(mod_pattern(r'caspt2'),
           #caspt2', r'\s*MOLCAS executing module CASPT2',
           name='caspt2',  # XXX opens section even if there is no output
           sections=['section_method', 'section_single_configuration_calculation'],
           fixedStartValues={'x_molcas_method_name': 'CASPT2'},
           subMatchers=[
               SM(r'\s*Total energy:\s*(?P<energy_total__hartree>\S+)', name='E-caspt2')
           ])
    return m

def molcas_main_loop_sm():
    m = SM(r'--- Start Module:\s*(?:%s)' % '|'.join(molcas_modules),
           endReStr='--- Stop Module:',
           repeats=True,
           forwardMatch=True,
           name='module',
           subMatchers=[
               gateway_seward(),
               scf_rasscf(),
               caspt2(),
               SM(r'%s|%s' % (mod_pattern(r'slapaf'),
                              # Sometimes the damn thing starts without a proper header!!  ARGH!
                              r's*Specification of the internal coordinates according to the user-defined'),
                  name='slapaf',
                  # The slapaf module writes forces, but only for a symmetry-reduced set of atoms.
                  # Therefore they are not useful to parse.  We could parse the set of symmetries probably
                  # and somehow make it possible to get the full set of Cartesian forces,
                  # but the operation would be very complicated.
                  #
                  # Let us consider parsing the reduced forces and
                  # symmetries the day that someone wants to implement
                  # this symmetry-unreduction (this will not happen).
                  subMatchers=[
                      SM(r'\*\s*Energy Statistics for Geometry Optimization',
                         name='opt-loop',
                         endReStr=r'\s*$',
                         sections=['section_single_configuration_calculation'],
                         subMatchers=[
                             SM(r'\s*\d+\s*\S+\s*', name='opt-iter', repeats=True, forwardMatch=True, adHoc=context.adhoc_store_line),
                             SM(r'\s*$', forwardMatch=True, adHoc=context.adhoc_pushback_last, name='pushback'),
                             # Molcas is supposed to have spaces between the numbers, but with grdNorm/Max,
                             # it sometimes writes 0.051834-0.037589 in one.  Thus we use -?[^\s-]+ to match such a number.
                             SM(r'\s*\d+\s*(?P<energy_total__hartree>\S+)\s*'
                                r'\S+\s*(?P<x_molcas_slapaf_grad_norm>-?[^\s-]+)\s*'
                                r'(?P<x_molcas_slapaf_grad_max>\S+)',
                                name='opt-iter', repeats=True),
                         ]),
                      SM(r'\s*\*\s*Nuclear coordinates for the next iteration / Bohr',
                         endReStr=r'\s*$',
                         name='newcoords',
                         sections=['section_system'],
                         subMatchers=[
                             context.multi_sm('coordinates',
                                              r'\s*ATOM\s*X\s*Y\s*Z',
                                              r'\s*(\S+)\s*(\S+)\s*(\S+)\s*(\S+)')
                             ])
                  ]),
               # last_energy just means it calls some other modules with annoyingly irregular output format
               SM(mod_pattern(r'last_energy'),
                  name='last',
                  subMatchers=[
                      gateway_seward(),
                      scf_rasscf(),
                      caspt2(),
                  ]),
               SM(mod_pattern('casvb'),
                  name='casvb',
                  sections=['section_method'],
                  fixedStartValues={'x_molcas_method_name': 'CASVB'},
                  subMatchers=[
                      SM('\s*CASSCF energy\s*:\s*(?P<energy_total__hartree>\S+)',
                         sections=['section_single_configuration_calculation'],
                         name='e-tot')
                  ]),
               SM(mod_pattern('mrci'),
                  name='mrci',
                  sections=['section_method'],
                  fixedStartValues={'x_molcas_method_name': 'MRCI'},
                  subMatchers=[
                      SM(r'\s*CI ENERGY:\s*(?P<energy_total__hartree>\S+)',
                         sections=['section_single_configuration_calculation'])
                  ]),
               SM(mod_pattern('cpf', 'CPFMCPF'),
                  name='cpf',
                  sections=['section_method'],
                  fixedStartValues={'x_molcas_method_name': 'MCPF'},
                  subMatchers=[
                      SM(r'\s*FINAL MCPF ENERGY\s*(?P<energy_total__hartree>\S+)',
                         sections=['section_single_configuration_calculation'])
                  ]),
               SM(mod_pattern('ccsdt', r'CCSD\(T\)'),
                  name='ccsdt',
                  sections=['section_method'],
                  fixedStartValues={'x_molcas_method_name': 'CCSDT'},
                  subMatchers=[
                      SM(r'\s*Total energy \(diff\)\s*:\s*(?P<energy_total__hartree>\S+)',
                         sections=['section_single_configuration_calculation'])
                  ]),
               SM(mod_pattern('mbpt2'),
                  name='mbpt2',
                  fixedStartValues={'x_molcas_method_name': 'MBPT2'},
                  sections=['section_method', 'section_single_configuration_calculation'],
                  subMatchers=[
                      SM(r'\s*Total energy\s*=\s*(?P<energy_total__hartree>\S+)\s*a\.u\.')
                  ]),
               SM(mod_pattern('mclr'),
                  name='mclr',
                  subMatchers=[
                      SM(r'\s*\*\s*Harmonic frequencies in cm-1\s*\*',
                         endReStr=r'\s*\*\s*THERMOCHEMISTRY',
                         sections=['section_single_configuration_calculation'],
                         subMatchers=[
                             SM(r'\s*Symmetry\s*(?P<x_molcas_frequency_symmetry>\S+)',
                                name='symm',
                                repeats=True,
                                sections=['x_molcas_section_frequency'],
                                subMatchers=[
                                    SM(r'\s*Freq\.\s*i(?P<x_molcas_imaginary_frequency_value__cm_1>\S+)', name='ifreq'),
                                    SM(r'\s*Freq\.\s*(?P<x_molcas_frequency_value>\S+)', name='freq'),
                                    SM(r'\s*Intensity:\s*(?P<x_molcas_frequency_intensity__km_mol_1>\S+)', name='intensity')
                                ])
                         ]),
                  ]),
           ] + get_anymodule_sms())
    return m

def main_file_description():
    return SM(
        name='root',
        weak=True,
        startReStr='',
        fixedStartValues={'program_name': 'MOLCAS',
                        'program_basis_set_type': 'gaussians'},
        sections=['section_run'],
        subMatchers=[
            get_header_sm(),
            #get_inputfile_echo_sm(),
            molcas_main_loop_sm(),
            SM(r'x^',  # force parser to parse the whole file
            name='impossible')
        ])


class MolcasParser():
    """ A proper class envolop for running this parser from within python. """
    def __init__(self, backend, **kwargs):
        self.backend_factory = backend

    def parse(self, mainfile):
        global context
        context = MolcasContext()

        from unittest.mock import patch
        logging.debug('molcas parser started')
        logging.getLogger('nomadcore').setLevel(logging.WARNING)
        backend = self.backend_factory("molcas.nomadmetainfo.json")
        with patch.object(sys, 'argv', ['<exe>', '--uri', 'nmd://uri', mainfile]):
            mainFunction(
                mainFileDescription=main_file_description(),
                metaInfoEnv=None,
                parserInfo=parser_info,
                cachingLevelForMetaName={},
                superContext=context,
                superBackend=backend)

        return backend
