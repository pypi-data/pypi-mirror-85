# -*- coding: utf-8 -*-
"""

Created on October 2020

@email: huangke@shangahitech.edu.cn

"""

import pandas as pd
import os
import re
import sys
#from multiprocessing import Pool
import threading
import numpy as np
import argparse
import queue


description= \
        "Description:\n\n " + \
        "Input file:           \
        1. VCF files directory  \
        2. RNA fastq files directory\n" + \
        "The function of this script is to call RNA reads of every heterozygosity SNVs\n" + \
        "The method of this script is that: \
        1. STAR mapping using WASP model \
        2. Remove WASP filed reads from bam  \
        3. Phaser caculate allelic reads from bam"




parser = argparse.ArgumentParser()
parser.add_argument('Calling',
        help='call ASE')

parser.add_argument('--sample',
        dest='sample',
        type=str,
        required=True,
        help='samples file that first column is DNAid and second column is RNAid')

parser.add_argument('--rnaseq',
        dest='rnaseq',
        type=str,
        required=True,
        help='RNA fastq seq directory')

parser.add_argument('--vcf',
        dest='vcf',
        type=str,
        required=True,
        help='VCF file directory')

parser.add_argument('--process',
        dest='process',
        type=int,
        required=True,
        help='Number of concurrent processes')

args = parser.parse_args()

## get phaser.py file path
def phaser_path():
    filepath=os.path.join(os.path.split(os.path.realpath(__file__))[0],'src/phaser.py')
    return filepath
def star_WASP_filter(sample_int):
    data=pd.read_table(args.sample)
    data.columns=['DNA_name','RNA_name']
    RNAseq_file_list=list()
    vcf_file_list=list()
    RNA_samplename=data['RNA_name'][sample_int]
    DNA_samplename=data['DNA_name'][sample_int]
    print(RNA_samplename)
    print(DNA_samplename)
    RNAseq_file=os.listdir(args.rnaseq)
    vcf_file=os.listdir(args.vcf)
    for filename in RNAseq_file:
        RNAseq_file_list.append(os.path.join(args.rnaseq,filename))
    for filename in vcf_file:
        if re.findall('tbi',filename):
            pass
        else:
            vcf_file_list.append(os.path.join(args.vcf,filename))
    RNA_matching = [RNA_filepath for RNA_filepath in RNAseq_file_list if RNA_samplename  in RNA_filepath]
    vcf_matching = [vcf_filepath for vcf_filepath in vcf_file_list if DNA_samplename  in vcf_filepath]


    if  re.findall('.gz',vcf_matching[0]):
        os.system('gunzip -d '+vcf_matching[0])
        vcf_matching[0]=vcf_matching[0][:-3]
    else:
        vcf_matching[0]=vcf_matching[0]
    print(RNA_matching)
    print(vcf_matching)
    os.system('mkdir -p ./ASE_calling_out/'+RNA_samplename)
    order1='STAR --runThreadN 4 --genomeDir /picb/humpopg-bigdata5/ningzhilin/RNA_genotype/WASP/hg19 \
		         --readFilesIn '+RNA_matching[0] +' '+RNA_matching[1] +'\
                         --twopassMode Basic  --readFilesCommand zcat  --waspOutputMode SAMtag --varVCFfile '+vcf_matching[0]+'  \
                          --outSAMtype BAM SortedByCoordinate  \
			--outFileNamePrefix ./ASE_calling_out/'+RNA_samplename+'/'+RNA_samplename

    order2='samtools view -h ./ASE_calling_out/'+'/'+RNA_samplename+'/'+RNA_samplename+'Aligned.sortedByCoord.out.bam | \
            grep -v "vW:i:[2-7]"  | samtools sort > ./ASE_calling_out/'+'/'+RNA_samplename+'/'+RNA_samplename+'Aligned.sortedByCoord.out.WASP.bam'
    order3='samtools index ./ASE_calling_out/'+RNA_samplename+'/'+RNA_samplename+'Aligned.sortedByCoord.out.WASP.bam'
    
    order4='bgzip '+vcf_matching[0]
    order5=' tabix -f '+vcf_matching[0]+'.gz'
    ##python2 /picb/humpopg-bigdata5/huangke/software/phaser/phaser/phaser.py
    order6=' python2 '+phaser_path() +'  \
            --vcf '+vcf_matching[0]+'.gz' +' \
            --bam ./ASE_calling_out/'+RNA_samplename+'/'+'/'+RNA_samplename+'Aligned.sortedByCoord.out.WASP.bam \
         --paired_end 1 --mapq 255 --baseq 10 --threads 4 --sample '+DNA_samplename +' --o ./ASE_calling_out/'+RNA_samplename+'/'+RNA_samplename
    os.system(order1)
    os.system(order2)
    os.system(order3)
    os.system(order4)
    os.system(order5)
    os.system(order6)

def main():
    import concurrent.futures
    data_sample=pd.read_table(args.sample)
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.process) as executor:
        executor.map(star_WASP_filter, range(len(data_sample)))
if __name__ == "__main__":
    main()
