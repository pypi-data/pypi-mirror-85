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

functionals = {'LSDA': ['LDA_X', 'LDA_C_VWN_3'],
               'LDA': ['LDA_X', 'LDA_C_VWN_3'],
               'SVWN': ['LDA_X', 'LDA_C_VWN_3'],
               'LSDA5': ['LDA_X', 'LDA_C_VWN'],
               'LDA5': ['LDA_X', 'LDA_C_VWN'],
               'SVWN5': ['LDA_X', 'LDA_C_VWN'],
               'HFB': ['GGA_X_B88'], #['GGA_X_B88' + Becke's 1988 exchange functional which includes the Slater exchange along with corrections involving the gradient of the density],
               'HFS': ['LDA_X'],  # Original HK/KS articles?  No libxc name...
               'HFB86': ['GGA_X_B86'],
               'HFO': ['GGA_X_OPTX'],
               'BLYP': ['GGA_X_B88', 'GGA_C_LYP'],
               'BPBE': ['GGA_X_B88', 'GGA_C_PBE'],
               'B3LYP': ['HYB_GGA_XC_B3LYP'],
               'B3LYP5': ['HYB_GGA_XC_B3LYP5'],
               #'B2PLYP': {'LDA_X': 0.47,
               #           'HF_X': 1. - 0.47,
               #           'GGA_X_B88': 0.47,
               #           },  # No clue how to set this one
               'B86LYP': ['GGA_X_B86', 'GGA_C_LYP'],
               'BWIG': ['GGA_X_B88', 'LDA_C_WIGNER'],
               'GLYP': ['GGA_X_G96', 'GGA_C_LYP'],
               'OLYP': ['GGA_X_OPT', 'GGA_C_LYP'],
               'OPBE': ['GGA_X_OPT', 'GGA_C_PBE'],
               'O3LYP': ['HYB_GGA_XC_O3LYP'],  # Or hideous composite thingy?
               #'O3LYP': {'HF_X': 0.1161,
               #          'LDA_X': 0.9262,
               #          'GGA_X_OPT': 0.8133,
               #          'GGA_C_VWN': 0.19,
               #          'GGA_C_LYP': 0.81}, ?
               #'KT3': ['GGA_X_KT...3'], TODO add to nomad xc functionals
               'TLYP': ['HF_X', 'GGA_C_LYP'],
               'PBE': ['GGA_X_PBE', 'GGA_C_PBE'],
               'PBE0': None,  # wtf
               'PBESOL': ['GGA_X_PBE_SOL', 'GGA_C_PBE_SOL'],
               'RGE2': ['GGA_X_RGE2', 'GGA_C_PBE_SOL'],
               'PTCA': ['GGA_X_PBE', 'GGA_C_TCA'],
               'SSB': ['GGA_X_SSB', 'GGA_C_PBE'],
               'M06': ['HYB_MGGA_XC_M06'],
               'M06L': ['MGGA_C_M06_L', 'MGGA_X_M06_L'],
               'M06HF': ['HYB_MGGA_XC_M06_HF'],  # Is this good enough?
               'M062X': ['HYB_MGGA_XC_M06_2X']}
