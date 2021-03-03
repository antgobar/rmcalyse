# ------------------------------------------------------------------------
###
# Program/module to read *.rmc6f file and get data
# e.g. cell dimension and atomic positions
###
# Example of how to call this module:
###
### import read_rmc6f as rr
###
### cell = rr.read_in('SrTiO3_00Nb_222.rmc6f')[0]
### atom_list = read_in('SrTiO3_00Nb_222.rmc6f')[1]
###
# ------------------------------------------------------------------------
import numpy as np
import re           # regular expressions
from dataclasses import dataclass

@dataclass
class MetaData:
    a: float
    b: float
    c: float
    al_deg: float
    be_deg: float
    ga_deg: float
    atoms: list

    def __post_init__(self):
        self.al, self.be, self.ga = np.deg2rad([self.al_deg, self.be_deg, self.ga_deg])
        self.V = self.a*self.b*self.c * (1 - np.cos(self.al)**2 - np.cos(self.be)**2 -np.cos(self.ga)**2 + 2*np.cos(self.al)*np.cos(self.be)*np.cos(self.ga))**0.5
        a1 = self.a
        a2 = 0
        a3 = 0
        b1 = self.b * np.cos(self.ga)
        b2 = self.b * np.sin(self.ga)
        b3 = 0
        c1 = self.c * np.cos(self.be)
        c2 = self.c * (np.cos(self.al) - (np.cos(self.be) * np.cos(self.ga))) / np.sin(self.ga)
        c3 = self.V / (self.a * self.b * np.sin(self.ga))
        self.M = np.array([[a1, b1, c1], [a2, b2, c2], [a3, b3, c3]])

def convert_meta_list_to_meta_object(rmc6f_input):
    line_elements = []
    line_density = []
    line_supercell = []
    line_cell = []
    line_atom_list = []

    # Extract and save variables
    for line in rmc6f_input:
        #   header
        if line.find('Atom types present:') >= 0:
            line_elements = line
        if line.find('Number density') >= 0:
            line_density = line
        if line.find('Supercell') >= 0:
            line_supercell = line
        if line.find('Cell') >= 0:
            line_cell = line
        #   atom lines
        if line.find('[1]') >= 0:
            line_atom_list.append(line)

    # Put element, atom no. and atomic positions into lists

    # elements
    keyword = 'Atom types present:'
    leading_string, keyword, elements_string = line_elements.partition(keyword)
    elements_string = elements_string.strip()
    elements = re.sub("[^\w]", " ",  elements_string).split()

    # density
    temp = re.findall('\d+\.\d+', line_density)
    density = [float(i) for i in temp]

    # supercell dimensions e.g. 4 4 4
    temp = re.findall('[-+]?\d*\.\d+|\d+', line_supercell)
    supercell = [int(i) for i in temp]

    # supercell parameters: a, b, c, alpha, beta, gamma
    temp = re.findall('[-+]?\d*\.\d+|\d+', line_cell)
    cell = [float(i) for i in temp]  # Needed for interatomic distances

    meta = MetaData(*cell, elements)

    return meta
