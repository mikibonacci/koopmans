"""Module containing functions relating to pseudopotentials."""

import re
from itertools import chain
from pathlib import Path
from typing import Dict, List, OrderedDict

from ase_koopmans import Atoms
from upf_tools import UPFDict

local_base_directory = (Path(__file__).parent / 'pseudopotentials').resolve()
local_libraries = set([str(f.parent.relative_to(local_base_directory))
                       for f in chain(local_base_directory.rglob('*.upf'),
                                      local_base_directory.rglob('*.UPF'))])


def pseudopotential_library_citations(library: str) -> List[str]:
    """Determine the appropriate citations for a pseudopotential library."""
    citations = []
    if library.startswith('SG15'):
        citations.append('Hamann2013')
        citations.append('Schlipf2015')
        if 'FR' in library:
            citations.append('Scherpelz2016')
    elif library.startswith('PseudoDojo'):
        citations.append('Hamann2013')
        citations.append('vanSetten2018')
    return citations


def element_from_pseudo_filename(filename: str) -> str:
    """Extract the element name from a pseudopotential filename."""
    splitname = re.split(r'\.|_|-', filename)[0]
    element = splitname[0].upper() + splitname[1:].lower()
    return element


def read_pseudo_file(filename: Path) -> UPFDict:
    """Read in settings from a .upf file."""
    if not filename.exists():
        raise FileNotFoundError(f'Could not find the pseudopotential file `{filename}`')

    upf = UPFDict.from_upf(filename)

    return upf


def nelec_from_pseudos(atoms: Atoms, pseudopotentials: OrderedDict[str, UPFDict]) -> int:
    """Determine the number of electrons in the system using information from pseudopotential files."""
    valences_dct = {key: int(value['header']['z_valence']) for key, value in pseudopotentials.items()}

    if len(set(atoms.get_tags())) > 1:
        labels = [s + str(t) if t > 0 else s for s, t in zip(atoms.symbols, atoms.get_tags())]
    else:
        labels = atoms.symbols

    valences = [valences_dct[label] for label in labels]
    return sum(valences)


def expected_subshells(atoms: Atoms, pseudopotentials: OrderedDict[str, UPFDict]) -> Dict[str, List[str]]:
    """Determine which subshells will make up the valences of a set of pseudopotentials.

    Returns
    -------
    OrderedDict[str, List[str]]
        a dict mapping element names to a corresponding list of suborbitals that *might* be in the pseudopotential
        valence (depending on how many bands are included)
    """
    z_core_to_first_orbital = {0: '1s', 2: '2s', 4: '2p', 10: '3s', 12: '3p', 18: '3d', 28: '4s', 30: '4p',
                               36: '4d', 46: '4f', 60: '5s', 62: '5p', 68: '6s'}

    expected_orbitals = {}
    for atom in atoms:
        label = atom.symbol + str(atom.tag) if atom.tag > 0 else atom.symbol
        if label in expected_orbitals:
            continue
        z_core = atom.number - int(pseudopotentials[label]['header']['z_valence'])
        if z_core in z_core_to_first_orbital:
            first_orbital = z_core_to_first_orbital[z_core]
        else:
            raise ValueError(f'Failed to identify the subshells of the valence of `{pseudopotentials[label].filename}`')
        all_orbitals = list(z_core_to_first_orbital.values()) + ['5d', '6p', '6d']
        expected_orbitals[label] = sorted(all_orbitals[all_orbitals.index(first_orbital):])
    return expected_orbitals
