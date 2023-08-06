# -*- coding: utf-8 -*-
"""

Created on October 2020

@email: huangke@shangahitech.edu.cn

"""

import argparse
import pandas as pd
import sys
import gzip as gz
import os
import scipy.stats as stats
import threading
import queue
import concurrent.futures
from multiprocessing import Pool
parser = argparse.ArgumentParser()

parser.add_argument('aseQTL',
                help='call aseQTL')

parser.add_argument("--ase",
        dest='ase',
        type=str,
        required=True,
        help='population level ASE reads file that suffix is reads.txt')
parser.add_argument("--vcf",
        dest='vcf',
        type=str,
        required=True,
        help='vcf filepath file splited by chromosome')

parser.add_argument('--process',
        type=int,
        required=False,
        default=6,
       help='multiprocessing according chromosome')

parser.add_argument("--out",
        type=str,
        required=False,
        default='./aseQTL.res.out',
        help="aseQTL result file output")
args = parser.parse_args()



def vcf_file():
    data=pd.read_table(args.vcf,sep='\s+',dtype=str)
    data.columns=['chr','filepath']
    if len(data['chr'][0])>1:
        data['chr']=data['chr'].str[3:]
    else:
        pass
    return data

def XJU_aseQTL_format(rank):
    ## input vcffilepath .txt file,count '#' line
    n=0
    vcf_filepath=vcf_file()
    geno_file=vcf_filepath['filepath'][rank]
    Chr=vcf_filepath['chr'][rank]
    print('ase filepath',args.ase)
    print('vcf filepath',geno_file)
    file_data=gz.open(geno_file,'r')
    i=0
    for line in file_data:
        line=line.decode()
        i=i+1
        if line[0:2]=='##':
            i=i+1
        else:
            break
    file_data.close()

    ## read ase file,remain at least 10 individuals heterozygous in ase loci
    data_ase=pd.read_table(args.ase,dtype=str)
    chr_list=list(data_ase['variantID'].str.split('_').str[0])
    pos_list=list(data_ase['variantID'].str.split('_').str[1])

    data_ase.insert(loc=1,column='Chr',value=chr_list)
    data_ase.insert(loc=2,column='POS',value=pos_list)
    
    data_ase=data_ase.loc[data_ase['Chr']==str(Chr)]
    data_ase['sum']=data_ase.iloc[:,3:].notnull().sum(axis=1)
    data_ase=data_ase.loc[data_ase['sum']>=10]
    data_ase=data_ase.drop(['sum'],axis=1)
    
    ## pandas read file, replace genotype by 0,1,2
    data_geno=pd.read_table(geno_file,dtype=str,skiprows=int((i-1)/2))
    if len(data_geno.iloc[0][10])==3:
        if data_geno.iloc[0][10][1]=='/':
            data_geno=data_geno.replace({'0/0':'0','0/1':'1','1/0':'1','1/1':'2'})
        else:
            data_geno=data_geno.replace({'0|0':'0','0|1':'1','1|0':'1','1|1':'2'})
    data_geno['POS']=data_geno['POS'].astype(int)
    
    os.system('mkdir -p '+os.path.join('./aseQTL.format.file/',str(Chr)))
    for i in range(len(data_ase)):
        n=n+1
        if n>100:
            break

        POS=int(data_ase['POS'].iloc[i])
        ## upstream and downstream 100kb
        ## output format:
        ## AI   SNP1    SNP2    SNP3
        data_ase_geno=data_geno.loc[(data_geno['POS']>=POS-100000)&(data_geno['POS']<=POS+100000)]
        data_ase_format=data_ase_geno.T.iloc[9:]
        data_ase_format.columns=list(data_ase_geno.T.iloc[1])
        data_ase_format.insert(loc=0,column='allele imblance',value=list(data_ase.iloc[i][3:]))
        data_ase_format=data_ase_format[data_ase_format['allele imblance'].notnull()]
        AI=(data_ase_format['allele imblance'].str.split('|').str[0].astype(int)/(data_ase_format['allele imblance'].str.split('|').str[1].astype(int)+data_ase_format['allele imblance'].str.split('|').str[0].astype(int))-0.5).abs()
        data_ase_format.insert(loc=1,column='AI_value',value=list(AI))
        Chr=str(Chr)
        data_ase_format.to_csv(os.path.join('./aseQTL.format.file/',Chr,Chr+'_'+str(POS)+'.format.txt'),index=None,sep='\t')



def chr_number():
    j=0
    for dir_number in os.walk('./aseQTL.format.file/'):
        j=j+1
        if j==1:
            return dir_number[1]
        else:
            break


def XJU_aseQTL_statis(Chr):
    Chr=str(Chr)
    df_list=list()
    i=0
    print('run aseQTL Chr'+Chr)
    if  os.path.exists(args.out)==False:
        try:
            os.system('mkdir '+args.out)
        except:
            pass
    for filename in os.listdir(os.path.join('./aseQTL.format.file/',Chr)):
        filepath=os.path.join('./aseQTL.format.file/',Chr,filename)
        ASE_pos=filepath.split('/')[-1].split('.')[0]
        SNP_list=list()
        ASE_site_list=list()
        pvalue_list=list()
        data=pd.read_table(filepath)

        ## all AI value is 0.5
        if len(data.drop_duplicates(['AI_value']))==1:
            continue
        ## if no SNP located in up and down 100kb 
        if len(data.columns)==2:
            continue
        
        ## mannwhiteyu test in every hete SNP
        ## split SNP into two groups: 'hete homo'
        for SNP in list(data.columns[2:]):
            corr_data=data[['AI_value',SNP]]
            het_corr_data=corr_data.loc[corr_data[SNP]==1]    
            ## drop homo SNP
            if len(het_corr_data)==0:
                continue
            homo_corr_data=corr_data.loc[corr_data[SNP]!=1]
            if len(homo_corr_data)==0:
                continue

            ## statistic test
            pvalue=stats.mannwhitneyu(het_corr_data['AI_value'],homo_corr_data['AI_value'],alternative='greater')[1]
            SNP_list.append(Chr+':'+SNP)
            ASE_site_list.append(ASE_pos)
            pvalue_list.append(pvalue)
        df=pd.DataFrame({'ASE_site':ASE_site_list,'SNP':SNP_list,'pvalue':pvalue_list})
        df_list.append(df)
    df_total=pd.concat(df_list)
    df_total['Chr']=Chr
    col=['ASE_site','Chr','SNP','pvalue']
    df_total.to_csv(os.path.join(args.out,'ASEqtl.Chr'+Chr+'.res.txt'),index=None,sep='\t',columns=col)

def multi_aseQTL_format():
    vcf_filepath=pd.read_table(args.vcf,sep='\s+')
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.process) as executor:
         executor.map(XJU_aseQTL_format, range(len(vcf_filepath)))

def multi_aseQTL_statis():
    vcf_filepath=pd.read_table(args.vcf,sep='\s+')
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.process) as executor:
        executor.map(XJU_aseQTL_statis, chr_number())
def pool_aseQTL_fromat():
    vcf_filepath=pd.read_table(args.vcf,sep='\s+')
    p=Pool(args.process)
    for rank in range(len(vcf_filepath)):
        p.apply_async(XJU_aseQTL_format,(rank,))
    p.close()
    p.join()
def pool_aseQTL():
    p=Pool(args.process)
    chr_list=chr_number()
    for Chr in chr_list:
        p.apply_async(XJU_aseQTL_statis,(Chr,))
    p.close()
    p.join()

def main():
    pool_aseQTL_fromat()
    pool_aseQTL()

    #multi_aseQTL_format()
    #multi_aseQTL_statis()
if __name__ == "__main__":
    main()

