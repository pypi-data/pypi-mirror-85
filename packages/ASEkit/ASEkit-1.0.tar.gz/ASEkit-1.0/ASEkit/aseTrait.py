import os
import argparse
import pandas as pd
description= \
        "Description:\n\n " + \
        "Input file:           \
        1. refCount file  \
        2.altCount file \
        3. pehnotype file\n" + \
        "The function of this script is to run a binomial Generalized Linear Mixed Model by eagle\n"


parser = argparse.ArgumentParser()
parser.add_argument('aseTrait',
                help='ASE assocaite with trait')

parser.add_argument('--ase',
    dest='ase',
    type=str,
    required=True,
    help='population ASE file')
parser.add_argument('--pheno',
        dest='pheno',
        type=str,
        required=True,
        help='pehnotype file')

parser.add_argument('--out',
        dest='out',
        type=str,
        required=True,
        help='output directory')
args = parser.parse_args()


def r_code_filepath():
    filepath=os.path.join(os.path.split(os.path.realpath(__file__))[0],'aseTrait/ASEassociateTrait.r')
    return filepath

def main():
    if os.path.exists(args.out)==False:
        os.system('mkdir '+args.out)
    r_script=r_code_filepath()
    order='Rscript '+r_script +' -a '+args.ase +' -p '+args.pheno +' -o '+args.out
    print(order)
    os.system(order)

if __name__ == "__main__":
    main()
