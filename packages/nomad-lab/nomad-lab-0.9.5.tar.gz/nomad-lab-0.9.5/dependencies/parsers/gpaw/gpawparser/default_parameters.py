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

"""
used with parser2.py, the new file format (aff)
"""
import numpy as np

parameters = {
    'mode': 'fd',
    'xc': 'LDA',
    'occupations': None,
    'poissonsolver': None,
    'h': None,  # Angstrom
    'gpts': None,
    'kpts': [(0.0, 0.0, 0.0)],
    'nbands': None,
    'charge': 0,
    'setups': {},
    'basis': {},
    'spinpol': None,
    'fixdensity': False,
    'filter': None,
    'mixer': None,
    'eigensolver': None,
    'background_charge': None,
    'external': None,
    'random': False,
    'hund': False,
    'maxiter': 333,
    'idiotproof': True,
    'symmetry': {'point_group': True,
                 'time_reversal': True,
                 'symmorphic': True,
                 'tolerance': 1e-7},
    'convergence': {'energy': 0.0005,  # eV / electron
                    'density': 1.0e-4,
                    'eigenstates': 4.0e-8,  # eV^2
                    'bands': 'occupied',
                    'forces': np.inf},  # eV / Ang
    'dtype': None,  # Deprecated
    'width': None,  # Deprecated
    'verbose': 0}


