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

from __future__ import print_function
from builtins import str
from builtins import object
import tarfile
import xml.etree.ElementTree as ElementTree

import numpy as np


class Reader(object):
    def __init__(self, name):
        self.dims = {}
        self.shapes = {}
        self.dtypes = {}
        self.parameters = {}
        self.tar = tarfile.open(name, 'r')
        f = self.tar.extractfile('info.xml').read()
        root = ElementTree.fromstring(f)
        self.byteswap = ((root.attrib['endianness'] == 'little') !=
                         np.little_endian)
        for child in root:
            a = child.attrib
            if child.tag == 'parameter':
                try:
                    value = eval(a['value'], {})
                except (SyntaxError, NameError):
                    value = str(a['value'])
                self.parameters[a['name']] = value
            elif child.tag == 'array':
                name = a['name']
                self.dtypes[name] = a['type']
                self.shapes[name] = []
                for dim in child:
                    n = int(dim.attrib['length'])
                    self.shapes[name].append(n)
                    self.dims[dim.attrib['name']] = n

    def __contains__(self, name):
        return name in self.parameters or name in self.shapes

    def __getattr__(self, name):
        if name in self.parameters:
            return self.parameters[name]
        else:
            return self.get_array(name)

    def get_array(self, name):
        fileobj = self.tar.extractfile(name)
        shape = self.shapes[name]
        dtype = self.dtypes[name]
        dtype = np.dtype({'int': 'int32'}.get(dtype, dtype))
        size = np.prod(shape) * dtype.itemsize
        array = np.fromstring(fileobj.read(size), dtype)
        if self.byteswap:
            array = array.byteswap()
        if dtype == np.int32:
            array = np.asarray(array, int)
        array.shape = shape
        return array

    def close(self):
        self.tar.close()


if __name__ == '__main__':
    r = Reader('H2.gpw')
    print(r.Eigenvalues, r.FermiLevel, r.UnitCell)
    print('UnitCell' in r, 'sdgsdgsdfg' in r)
