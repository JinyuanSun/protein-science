# Sebastian Raschka 2014
# Script that splits a multi-mol2 file into individual mol2 files.

import sys
import os


def split_multimol2(multimol2, generator=False):
    """
    Splits a multi-mol2 file (a mol2 file consisting of multiple mol2 entries)
        into individual mol2-file contents.

    Keyword arguments:
        multimol2 (string): path to the multi-mol2 file
        generator (bool): If True, returns a generator instead of a list.

    Returns:
        A generator object for lists for every extracted mol2-file. Lists contain
        the molecule ID and the mol2 file contents.
        e.g., ['ID1234', '@<TRIPOS>MOLECULE...']

    """
    with open(multimol2, 'r') as mol2file:
        line = ""
        mol2cont = ""
        single_mol2s = []
        line = mol2file.readline()

        while not mol2file.tell() == os.fstat(mol2file.fileno()).st_size:
            if line.startswith("@<TRIPOS>MOLECULE"):
                mol2cont = ""
                mol2cont += line
                line = mol2file.readline()
                molecule_id = line.strip()

                while not line.startswith("@<TRIPOS>MOLECULE"):
                    mol2cont += line
                    line = mol2file.readline()
                    if mol2file.tell() == os.fstat(mol2file.fileno()).st_size:
                        mol2cont += line
                        break

                yield [molecule_id, mol2cont]


if __name__ == '__main__':

    import argparse

    parser = argparse.ArgumentParser(
        description='Splits a multi-mol2 file into individual mol2 files',
        formatter_class=argparse.RawTextHelpFormatter
        )

    parser.add_argument('MOL2_FILE')
    parser.add_argument('OUT_DIR')
    parser.add_argument('-v', '--version', action='version', version='split_multimol2 v. 1.0')

    args = parser.parse_args()

    if not os.path.exists(args.OUT_DIR):
        os.mkdir(args.OUT_DIR)

    assert len(sys.argv) == 3
    multimol2 = sys.argv[1]
    out_dir = sys.argv[2]

    single_mol2s = split_multimol2(args.MOL2_FILE)
    for mol2 in single_mol2s:
        out_mol2 = os.path.join(out_dir, mol2[0]) + '.mol2'
        with open(out_mol2, 'w') as out_file:
            for line in mol2[1]:
                out_file.write(line)



