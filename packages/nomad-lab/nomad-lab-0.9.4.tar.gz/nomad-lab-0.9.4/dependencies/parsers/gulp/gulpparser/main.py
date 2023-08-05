# Copyright 2016-2018 Ask Hjorth Larsen, Fawzi Mohamed
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

#
# Main author and maintainer: Ask Hjorth Larsen <asklarsen@gmail.com>

from __future__ import print_function
import os
import sys
import re

import numpy as np
import logging
from ase import Atoms
from ase.spacegroup import crystal
#from ase.data import chemical_symbols

from nomadcore.simple_parser import mainFunction, SimpleMatcher as SM
from nomadcore.local_meta_info import loadJsonFile, InfoKindEl
from nomadcore.unit_conversion.unit_conversion \
    import register_userdefined_quantity, convert_unit

# relative import
from gulpparser.spacegroups import get_spacegroup_number
#from util import floating, integer

# Generate list of all energy contributions:
# cat outputs/example*.got | grep "Components of energy" -A 20 | grep = |grep eV | cut -c 1-30 | sort|uniq|less
energy_contributions = """\
Attachment energy
Attachment energy/unit
Bond-order potentials
Brenner potentials
Bulk energy
Dispersion (real+recip)
Electric_field*distance
Energy shift
Four-body potentials
Improper torsions
Interatomic potentials
Many-body potentials
Monopole - monopole (real)
Monopole - monopole (recip)
Monopole - monopole (total)
Neutralising energy
  Non-primitive unit cell
Out of plane potentials
  Primitive unit cell
ReaxFF force field
Region 1-2 interaction
Region 2-2 interaction
Self energy (EEM/QEq/SM)
SM Coulomb correction
Solvation energy
Three-body potentials
Total lattice energy"""


def get_gulp_energy_patterns():
    for name in energy_contributions.splitlines():
        name = name.strip()
        basepattern = re.escape(name)
        name = name.lower()
        name = name.replace(' - ', '_')
        name = name.replace(' (', '_')
        name = name.replace(')', '')
        name = name.replace('field*distance', 'field_times_distance')
        name = re.sub(r'[-+/\s]', '_', name)

        metaname = 'x_gulp_energy_%s' % name
        pattern = r'\s*%s\s*=\s*(?P<%s__eV>\S+)\s*eV' % (basepattern,
                                                         metaname)
        yield name, metaname, pattern

energy_term_template = """{
    "description": "GULP energy term for %(name)s",
    "name": "%(metaname)s",
    "superNames": [ "section_single_configuration_calculation" ],
    "dtypeStr": "f",
    "shape": []
  }, """

def generate_energy_json():
    for name, metaname, pattern in get_gulp_energy_patterns():
        print(energy_term_template % dict(name=name,
                                          metaname=metaname), end='')
# generate_energy_json()  # Print JSON for energy terms to stdout

def get_gulp_energy_sm():
    sms = []
    for name, metaname, pattern in get_gulp_energy_patterns():
        #print(pattern)
        sms.append(SM(pattern, name=name))

    return SM(r'\s*Components of energy :',
              name='gulp-energy',
              subFlags=SM.SubFlags.Unordered,
              subMatchers=sms)

#TODO
#----

#OK    "program_name",
#OK    "atom_labels",
#OK    "atom_positions",
#OK    "program_version",
#OK    "energy_total",
#OK    "simulation_cell",
#OK    "configuration_periodic_dimensions"

#OK    'section_system',
#    'section_method',
#    'section_frame_sequence',
#    'section_sampling_method',
#OK    'single_configuration_to_calculation_method_ref',
#OK    'single_configuration_calculation_to_system_ref',
#    'atom_forces_raw',
#    'frame_sequence_local_frames_ref',
#    'frame_sequence_to_sampling_ref',

#DFT-only
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
#    'program_basis_set_type',

"""File structure.  Example 4

Input for configuration = 1
  formula
  irreducible atoms/shells
  total atoms/shells
  dimensionalitycat
  symmetry
    space group
    cart lat vec
    cell param
    frac coord of asymm unit
  constraints

General input information
  species, type, atomic number, mass, charge, ... (table)
  general interatomic potentials (table)

"Start of fitting :"
  cycles... iterations
  fit completed successfuly
  final sum of squares
  final values of parameters (table)
  etc
  general interatomic potentials (table)
  total time to end of fitting

output for configuration 1
  components of energy :
    <components including total lattice energy>

"Start of bulk optimization"
  <iterations>
  Optimization achieved
  Final energy
  Components of energies <numbers>
  final asymmetric unit coords (table)
  final cartecian lattice vectors (ang) (table)
  final cell parameters and derivatives

comparison of initial and final structures: .....
time to end of optimisation
"job finished at ..."

"""


class GulpContext(object):
    def __init__(self):
        self.data = {}
        self.spacegroup = None
        self.current_raw_cell = None
        self.npbc = None
        self.use_spacegroup = None

        self.section_refs = {}

    def startedParsing(self, fname, parser):
        pass

    # Standard onOpen definitions from Siesta parser
    def onOpen_section_sampling_method(self, backend, gindex, section):
        self.section_refs['sampling_method'] = gindex

    def onOpen_section_frame_sequence(self, backend, gindex, section):
        self.section_refs['frame_sequence'] = gindex

    def onOpen_section_method(self, backend, gindex, section):
        self.section_refs['method'] = gindex

    def onOpen_section_system(self, backend, gindex, section):
        self.section_refs['system'] = gindex

    def adhoc_whether_using_spacegroup(self, parser):
        line = parser.fIn.readline()

        if 'Final coordinates of region' in line:
            self.use_spacegroup = False

    def onClose_section_method(self, backend, gindex, section):
        # species = self.data['species']
        # sym, types, charges = species.T
        # charges = convert_unit(charges.astype(float), 'e')
        # backend.addArrayValues('x_gulp_species_charge', charges)
        pass

    def onClose_section_system(self, backend, gindex, section):
        data = self.data

        ctable = data.pop('gulp_coordinate_table', None)
        if ctable is None:
            return  # This is probably an MD simulation or something.
            # I am sure we will get to suffer because of this relatively arbitrary
            # return, but what can you do

        symbols = ctable[:, 0]
        gulp_labels = ctable[:, 1]
        positions = ctable[:, 2:5].astype(float)

        chemical_symbols = []
        gulp_numeric_tags = []
        for sym in symbols:
            m = re.match(r'([A-Z][a-z]?)(\d*)', sym)
            chemical_symbols.append(m.group(1))
            gulp_numeric_tags.append(m.group(2))

        # Construct a mapping which combines gulp numeric tags and core/shell
        # etc. specification into a single numeric tag so ASE spacegroup
        # module can distinguish the atoms when constructing the full system
        types = {}
        tags = []

        ase_symbols = []
        for sym, label in zip(symbols, gulp_labels):
            full_label = '%s_%s' % (sym, label)
            tag = types.setdefault(full_label, len(types))
            tags.append(tag)
            ase_symbols.append(re.match(r'[A-Z][a-z]?', sym).group())

        # Really we want the opposite mapping
        tag2type = dict((v, k) for k, v in types.items())

        if self.npbc is None:
            self.npbc = section['x_gulp_pbc'][0]
        assert self.npbc in range(4)

        pbc = np.zeros(3, bool)
        pbc[:self.npbc] = True
        assert sum(pbc) == self.npbc

        # charge, occupancy?

        if self.spacegroup is None:
            spacegroup = section['x_gulp_space_group']
            if spacegroup is not None:
                spacegroup = spacegroup[0]
            self.spacegroup = spacegroup

        self.current_raw_cell = data.pop('cell', self.current_raw_cell)
        if self.npbc > 0:
            assert self.current_raw_cell is not None

        if self.use_spacegroup is None:
            self.use_spacegroup = (self.spacegroup is not None)

        if self.use_spacegroup:
            # group may be none ---- no spacegroup

            cellparnames = ['a', 'b', 'c', 'alpha', 'beta', 'gamma']

            #try:#if 'x_gulp_cell_a' in section:
            val = [section['x_gulp_cell_%s' % name] for name in cellparnames]
            if val[0] is None:
                # if we have the prim cell and not the full cell, it's because they
                # are identical (as far as I can tell).
                val = [section['x_gulp_prim_cell_%s' % name] for name in cellparnames]

            cellpar = []
            for v in val:
                assert len(v) == 1
                cellpar.append(v[0])
            assert len(cellpar) == 6

            num = get_spacegroup_number(self.spacegroup)

            basis_atoms = Atoms(ase_symbols, tags=tags,
                                cell=np.eye(3),
                                scaled_positions=positions)

            unique_labels = set(gulp_labels)
            thelabels = np.array(gulp_labels)

            constituents = []
            def build_atoms(label):
                b = basis_atoms[thelabels == label]
                atoms = crystal(b,
                                basis=b,
                                spacegroup=num,
                                cellpar=cellpar,
                                onduplicates='error')
                constituents.append(atoms)

            # Avoid duplicates when constructing space group atoms *grumble*
            # We want core and shell first
            for sym in 'cs':
                if sym in unique_labels:
                    unique_labels.remove(sym)
                    build_atoms(sym)
            for sym in sorted(unique_labels):
                build_atoms(sym)

            atoms = constituents[0]
            for other in constituents[1:]:
                atoms += other
        else:
            cell3d = np.identity(3)
            if self.npbc > 0:
                cell = self.current_raw_cell
                assert cell.shape == (self.npbc, 3), cell.shape
                cell3d[:self.npbc, :] = cell

            # use Atoms to get scaled positions/cell right:
            atoms = Atoms([0] * len(positions), cell=cell3d,
                          scaled_positions=positions, pbc=pbc,
                          tags=tags)

        atom_labels = [tag2type[tag] for tag in atoms.get_tags()]

        backend.addArrayValues('atom_labels', np.asarray(atom_labels))
        backend.addArrayValues('configuration_periodic_dimensions', pbc)
        backend.addValue('number_of_atoms', len(atom_labels))
        # The cell can be infinite in some directions.
        # In that case the cell value will just be one (it has to have some value!!)
        # but there will not be periodic boundary conditions in that direction.
        # We will have to live with this except if simulation_cell permits something
        # more general.
        backend.addArrayValues('simulation_cell',
                               convert_unit(atoms.cell, 'angstrom'))
        backend.addArrayValues('atom_positions',
                               convert_unit(atoms.positions, 'angstrom'))

    def onClose_section_single_configuration_calculation(self, backend,
                                                         gindex, section):
        backend.addValue('single_configuration_to_calculation_method_ref',
                         self.section_refs['method'])
        backend.addValue('single_configuration_calculation_to_system_ref',
                         self.section_refs['system'])

    # multi_sm is a copy from Siesta
    def multi_sm(self, name, startpattern, linepattern, endmatcher=None,
                 conflict='overwrite',  # 'fail', 'keep', 'overwrite'
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


context = GulpContext()

def get_input_system_sm():
    m = SM(r'\*\s*Input for Configuration',
           name='input-conf',
           sections=['section_system'],
           subMatchers=[
               SM(r'\s*Formula\s*=\s*(?P<x_gulp_formula>\S+)',
                  name='formula'),
               SM(r'\s*Dimensionality\s*=\s*(?P<x_gulp_pbc>\d+)',
                  name='pbc'),
               SM(r'\s*Symmetry\s*:',
                  name='symm-header',
                  subMatchers=[
                      SM(r'\s*Space group \S+\s+:\s*(?P<x_gulp_space_group>.+?)\s*$',
                         name='spacegroup'),
                      SM(r'\s*Patterson group\s*:\s*(?P<x_gulp_patterson_group>.+?)\s*$',
                         name='patterson'),
                  ]),
               SM(r'\s*([Cc]artesian lattice|Surface [Cc]artesian|Polymer [Cc]artesian) vectors? \(Angstroms\) :',
                  name='lattice-header',
                  subMatchers=[
                      context.multi_sm('cell',
                                       r'',
                                       r'\s*(\S+)\s*(\S+)\s*(\S+)')
                  ]),
               SM(r'\s*Primitive cell parameters\s*:\s*Full cell parameters\s*:',
                  name='cellpar1',
                  subMatchers=[
                      SM(r'\s*a\s*=\s*\S+\s*alpha\s*=\s*\S+\s*a\s*=\s*(?P<x_gulp_cell_a>\S+)\s+alpha\s*=\s*(?P<x_gulp_cell_alpha>\S+)'),
                      SM(r'\s*b\s*=\s*\S+\s*beta\s*=\s*\S+\s*b =\s*(?P<x_gulp_cell_b>\S+)\s+beta\s*=\s*(?P<x_gulp_cell_beta>\S+)'),
                      SM(r'\s*c\s*=\s*\S+\s*gamma\s*=\s*\S+\s*c =\s*(?P<x_gulp_cell_c>\S+)\s+gamma\s*=\s*(?P<x_gulp_cell_gamma>\S+)'),
                  ]),
               SM(r'\s*Cell parameters\s*\(Angstroms/Degrees\):',
                  name='cellpar2',
                  subMatchers=[
                      SM(r'\s*a =\s*(?P<x_gulp_cell_a>\S+)\s*alpha\s*=\s*(?P<x_gulp_cell_alpha>\S+)'),
                      SM(r'\s*b =\s*(?P<x_gulp_cell_b>\S+)\s*beta\s*=\s*(?P<x_gulp_cell_beta>\S+)'),
                      SM(r'\s*c =\s*(?P<x_gulp_cell_c>\S+)\s*gamma\s*=\s*(?P<x_gulp_cell_gamma>\S+)'),
                  ]),
               SM(r'\s*(Fractional|[Cc]artesian|Mixed fractional/[Cc]artesian) coordinates of (asymmetric unit|surface|polymer|cluster|)\s*:',
                  #r'\s*(Fractional coordinates of asymmetric unit'
                  #r'|Mixed fractional/Cartesian coordinates of (surface|polymer)'
                  #r'|Cartesian coordinates of cluster)\s*:',
                  subFlags=SM.SubFlags.Sequenced,
                  name='frac-coords',
                  subMatchers=[
                      SM(r'--------+', name='bar'),
                      # We need to skip the 'Region 1' headers, so stop criterion is the empty line!
                      context.multi_sm('gulp_coordinate_table',
                                       r'-----+',
                                       #No.  Atomic       x           y          z         Charge      Occupancy
                                       #     Label      (Frac)      (Frac)     (Frac)        (e)         (Frac)
                                       #
                                       #     1      La      c       0.333333   0.666667   0.245000    *  9.00000    1.000000
                                       r'\s*\d+\s+(\S+)\s+(\S+)[\s\*]+(\S+)[\s\*]+(\S+)[\s\*]+(\S+)[\s\*]+(\S+)[\s\*]+(\S+)',
                                       r'------------+')
                  ]),
               #SM(r'General interatomic potentials',
               #),
            ])
    return m


def get_output_config_sm():
    m = SM(r'\*\s*Output for configuration',
           name='output-conf',
           endReStr='\s*Total lattice energy.*?kJ',
           sections=['section_single_configuration_calculation'],
           subMatchers=[
               get_gulp_energy_sm()
           ])
    return m

def get_optimise_sm():
    m = SM(r'\s*\*+\s*Optimisation achieved\s*\**',
        #r'\s*Start of \S+ optimisation :', #r'\*\s*Output for configuration',
           name='opt-start',
           repeats=True,
           sections=['section_system',
                     'section_single_configuration_calculation'],
           subMatchers=[
               get_gulp_energy_sm(),
               #SM(r'\s*Components of energy :',
               #   name='e-components',
               #   subMatchers=[
               #       get_gulp_energy_sm()
                      #SM(r'\s*Interatomic potentials\s*=\s*(?P<x_gulp_energy_interatomic_potentials__eV>\S+)\s*eV'),
                      #SM(r'\s*Monopole - monopole \(real\)\s*=\s*(?P<x_gulp_energy_monopole_monopole_real>\S+)\s*eV'),
                      #SM(r'\s*Monopole - monopole \(recip\)\s*=\s*(?P<x_gulp_energy_monopole_monopole_recip>\S+)\s*eV'),
                      #SM(r'\s*Monopole - monopole \(total\)\s*=\s*(?P<x_gulp_energy_monopole_monopole_total>\S+)\s*eV'),
                      #SM(r'\s*Electric_field\*distance\s*=\s*(?P<x_gulp_energy_electric_field>\S+)\s*eV'),
                      #SM(r'\s*Total lattice energy\s*=\s*(?P<energy_total__eV>\S+)\s*eV',
                      #   name='etotal')
               #   ]),
               SM(r'\s*Final (asymmetric unit|fractional|fractional/[Cc]artesian|[Cc]artesian)?\s*coordinates\s*(of atoms|of region \d+)?\s*:',
                  forwardMatch=True,
                  adHoc=context.adhoc_whether_using_spacegroup,
                  subMatchers=[
                      context.multi_sm('gulp_coordinate_table',
                                       r'-------------+',
                                       # This table is slightly differently formatted than the one from the input
                                       #--------------------------------------------------------------------------------
                                       #   No.  Atomic        x           y           z         Radius
                                       #        Label       (Frac)      (Frac)      (Frac)       (Angs)
                                       #--------------------------------------------------------------------------------
                                       #     1      La      c     0.333   0.666   0.248   0.000
                                       #     2      O       c     0.000   0.000   0.000   0.000
                                       r'\s*\d+\s*(\S+)\s*(\S+)\s*(\S+)\s*(\S+)\s*(\S+)\s*(\S+)',
                                       r'^$')
                  ]),
               SM(r'\s*Final [Cc]artesian lattice vectors \(Angstroms\) :',
                  subMatchers=[
                      context.multi_sm(r'cell',
                                       r'',
                                       r'\s*(\S+)\s*(\S+)\s*(\S+)')
                  ]),
               SM(r'\s*Final cell parameters and derivatives :',
                  name='finalcell',
                  subMatchers=[
                      SM(r'\s*a\s*(?P<x_gulp_prim_cell_a>\S+)\s+Angstrom', name='a'),
                      SM(r'\s*b\s*(?P<x_gulp_prim_cell_b>\S+)\s+Angstrom', name='b'),
                      SM(r'\s*c\s*(?P<x_gulp_prim_cell_c>\S+)\s+Angstrom', name='c'),
                      SM(r'\s*alpha\s*(?P<x_gulp_prim_cell_alpha>\S+)\s+Degrees', name='alpha'),
                      SM(r'\s*beta\s*(?P<x_gulp_prim_cell_beta>\S+)\s+Degrees', name='beta'),
                      SM(r'\s*gamma\s*(?P<x_gulp_prim_cell_gamma>\S+)\s+Degrees', name='gamma'),
                  ]),
               SM(r'\s*Non-primitive lattice parameters :',
                  name='nonprim',
                  subMatchers=[
                      SM(r'\s*a\s*=\s*(?P<x_gulp_cell_a>\S+)\s*b\s*=\s*(?P<x_gulp_cell_b>\S+)\s*c\s*=\s*(?P<x_gulp_cell_c>\S+)'),
                      SM(r'\s*alpha\s*=\s*(?P<x_gulp_cell_alpha>\S+)\s*beta\s*=\s*(?P<x_gulp_cell_beta>\S+)\s*gamma\s*=\s*(?P<x_gulp_cell_gamma>\S+)'),
                  ]),
           ])
    return m

def get_header_sm():
    m = SM(r'\*\s*GENERAL UTILITY LATTICE PROGRAM\s*\*',
           name='header',
           endReStr=r'\s*Job Started',
           subMatchers=[
               SM(r'\*\s+.*?\s*\*$',
                  name='Julian and friends',
                  repeats=True),
               SM(r'\*\*+'),
               SM(r'\*\s*Version\s*=\s*(?P<program_version>\S+)',
                  name='version'),
               SM(r'\*\*\*\*+',
                  endReStr=r'\*\*\*\*+',
                  name='bar',
                  subMatchers=[
                      SM(r'\*\s*(?P<x_gulp_main_keyword>\S+)\s*-',
                         repeats=True,
                         sections=['x_gulp_section_main_keyword'],
                         name='mainkw')
                  ]),
               SM(r'\*\s*(?P<x_gulp_title>.*?)\s*\*$',
                  name='title')
           ])
    return m

def get_gulp_potential_species_pattern(nspecies):
    tokens = []
    for i in range(1, nspecies + 1):
        tokens.append(r'(?P<x_gulp_forcefield_species_%d>\w+)\s*' % i)
        tokens.append(r'(?P<x_gulp_forcefield_speciestype_%d>\S+)\s*' % i)
    return ''.join(tokens)


def get_forcefield_table_sm(header, columnheaderpattern, tablepattern, name):
    m = SM(header,#r'\s*(General interatomic|Intramolecular|Intermolecular) potentials :',
           name=name,
           subMatchers=[
               SM(columnheaderpattern,#r'\s*Atom\s*Types\s*Potential\s*A*\s*B\s*C\s*D',
                  #Atom  Types   Potential         A         B         C         D     Cutoffs(Ang)
                  #  1     2                                                            Min    Max
                  # -------------------------------------------------------------------------------
                  #O    s La   s Buckingham    0.570E+04 0.299      38.9      0.00     0.000 24.000
                  subMatchers=[
                      SM(r'----------+', name='potentials',
                         endReStr=r'----------+',
                         subMatchers=[
                             SM(tablepattern,#''.join(tokens),
                                #get_gulp_potential_species_pattern(2) +
                                #r'(?P<x_gulp_forcefield_species_1>\w+)\s*'
                                #r'(?P<x_gulp_forcefield_speciestype_1>\S+)\s*'
                                #r'(?P<x_gulp_forcefield_species_2>\S+)\s*'
                                #r'(?P<x_gulp_forcefield_speciestype_2>\S+)\s*'
                                # The SRGlue potential is badly written in the table and unparseable.
                                # Probably a bug.  So just ignore it.
                                #r'(SRGlue|(?P<x_gulp_forcefield_potential_name>\b.{1,14}?)\s*'
                                #r'(?P<x_gulp_forcefield_parameter_a>\S+)\s*'
                                #r'(?P<x_gulp_forcefield_parameter_b>\S+)\s*'
                                #r'(?P<x_gulp_forcefield_parameter_c>\S+)\s*'
                               # r'(?P<x_gulp_forcefield_parameter_d>\S+)\s*'
                               # r'(?P<x_gulp_forcefield_cutoff_min>\S+\s*)'
                               # r'(?P<x_gulp_forcefield_cutoff_max>\S+))$',
                                name='table',
                                sections=['x_gulp_section_forcefield'],
                                repeats=True
                            ),
                         ]),
                  ]),
           ])
    return m


def get_general_input_sm():
    m = SM(r'\*\s*General input information',
           name='general-input',
           sections=['section_method'],
           subMatchers=[
               SM(r'\s*Species output for all configurations :'),
               SM(r'\s*Species\s*Type\s*Atomic',
                  subMatchers=[
                      context.multi_sm('species',
                                       r'-------+',
                                       #    species   type             charge
                                       r'\s*(\S+)\s*(\S+)\s*\d+\s*\S+\s*(\S+)',
                                       r'-------+')
                  ]),
               get_forcefield_table_sm(r'\s*(General interatomic|Intramolecular) potentials :',
                                       r'\s*Atom\s*Types\s*Potential\s*A*\s*B\s*C\s*D',
                                       get_gulp_potential_species_pattern(2) +
                                       r'(SRGlue|'
                                       r'(?P<x_gulp_forcefield_potential_name>\b.{1,14}?)\s*'
                                       r'(?P<x_gulp_forcefield_parameter_a>\S+)\s*'
                                       r'(?P<x_gulp_forcefield_parameter_b>\S+)\s*'
                                       r'(?P<x_gulp_forcefield_parameter_c>\S+)\s*'
                                       r'(?P<x_gulp_forcefield_parameter_d>\S+)\s*'
                                       r'(?P<x_gulp_forcefield_cutoff_min>\S+\s*)'
                                       r'(?P<x_gulp_forcefield_cutoff_max>\S+)$)',
                                       name='interatomic'),
               get_forcefield_table_sm(r'\s*(Intermolecular) potentials :',  # Basically a copy of the one just above
                                       r'\s*Atom\s*Types\s*Potential\s*A*\s*B\s*C\s*D',
                                       get_gulp_potential_species_pattern(2) +
                                       r'(SRGlue|(?P<x_gulp_forcefield_potential_name>\b.{1,14}?)\s*'
                                       r'(?P<x_gulp_forcefield_parameter_a>\S+)\s*'
                                       r'(?P<x_gulp_forcefield_parameter_b>\S+)\s*'
                                       r'(?P<x_gulp_forcefield_parameter_c>\S+)\s*'
                                       r'(?P<x_gulp_forcefield_parameter_d>\S+)\s*'
                                       r'(?P<x_gulp_forcefield_cutoff_min>\S+\s*)'
                                       r'(?P<x_gulp_forcefield_cutoff_max>\S+))$',
                                       name='intermolecular'),
               get_forcefield_table_sm(r'\s*General Three-body potentials :',
                                       r'\s*Atom\s*Atom\s*Atom\s*Force Constants\s*Theta',
                                       get_gulp_potential_species_pattern(3) +
                                       r'(?P<x_gulp_forcefield_threebody_1>\S+)\s*'
                                       r'(?P<x_gulp_forcefield_threebody_2>\S+)\s*'
                                       r'(?P<x_gulp_forcefield_threebody_3>\S+)\s*'
                                       r'(?P<x_gulp_forcefield_threebody_theta>\S+)\s*',
                                       name='3-body'),
               get_forcefield_table_sm(r'\s*General Four-body potentials :',
                                       r'\s*Atom Types\s*Force cst\s*Sign\s*Phase\s*Phi0',
                                       get_gulp_potential_species_pattern(4) +
                                       r'(?P<x_gulp_forcefield_fourbody_force_constant>\S+)\s*'
                                       r'(?P<x_gulp_forcefield_fourbody_sign>\S+)\s*'
                                       r'(?P<x_gulp_forcefield_fourbody_phase>\S+)\s*'
                                       r'(?P<x_gulp_forcefield_fourbody_phi0>\S+)\s*',
                                       name='3-body'),
           ])
    return m

def get_md_sm():
    m = SM(r'\*\s*Molecular Dynamics',
           name='md',
           subMatchers=[
               SM(r'\s*Molecular dynamics production :',
                  name='mdstep',
                  subMatchers=[
                      SM(r'\s*\*\*\s*Time :\s*(?P<x_gulp_md_time__ps>\S+)\s*ps :',
                         sections=['section_system', 'section_single_configuration_calculation'],
                         repeats=True,
                         subMatchers=[
                             SM(r'\s*Kinetic energy\s*\(eV\)\s*=\s*(?P<x_gulp_md_kinetic_energy__eV>\S+)'),
                             SM(r'\s*Potential energy\s*\(eV\)\s*=\s*(?P<x_gulp_md_potential_energy__eV>\S+)'),
                             SM(r'\s*Total energy\s*\(eV\)\s*=\s*(?P<x_gulp_md_total_energy__eV>\S+)'),
                             SM(r'\s*Temperature\s*\(K\)\s*=\s*(?P<x_gulp_md_temperature__K>\S+)'),
                             SM(r'\s*Pressure\s*\(GPa\)\s*=\s*(?P<x_gulp_md_pressure__GPa>\S+)'),
                         ])
                  ])
           ])
    return m

infoFileDescription = SM(
    name='root',
    weak=True,
    startReStr='',
    fixedStartValues={'program_name': 'gulp',
                      'program_basis_set_type': 'unavailable'},
    sections=['section_run'],
    subMatchers=[
        get_header_sm(),
        get_input_system_sm(),
        get_general_input_sm(),
        get_output_config_sm(),
        get_optimise_sm(),  # note British spelling
        get_md_sm(),
        SM(r'x^',
           name='impossible')  # 'Parse' the whole file
    ])


class GULPParser():
    """ A proper class envolop for running this parser from within python. """
    def __init__(self, backend, **kwargs):
        self.backend_factory = backend

    def parse(self, mainfile):
        from unittest.mock import patch
        logging.info('GULP parser started')
        logging.getLogger('nomadcore').setLevel(logging.WARNING)
        backend = self.backend_factory("gulp.nomadmetainfo.json")
        with patch.object(sys, 'argv', ['<exe>', '--uri', 'nmd://uri', mainfile]):
            mainFunction(
                infoFileDescription,
                None,
                {'name': 'gulp-parser', 'version': '1.0'},
                cachingLevelForMetaName={},
                superContext=GulpContext(),
                superBackend=backend)

        return backend
