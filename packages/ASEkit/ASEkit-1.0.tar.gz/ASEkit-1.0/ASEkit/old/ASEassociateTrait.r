# _*_ coding: utf-8 _*_

#Created on October 2020
#@email: tanxinjiang2019@sibs.ac.cn 


########## PACKAGES ##########
library('getopt')
library('eagle')
library('data.table')
library('ggplot2')
library('parallel')
########## INPUT ##########
command=matrix(c( 
    'help', 'h', 0,'loical', '显示此帮助信息',
    'alt_counts_file', 'a', 1,'character', 'alt counts',
    'ref_counts_file', 'r', 1,'character', 'ref counts',
    'genotype_file', 'g', 1, 'character', '基因型',
    'phenotype_file', 'p', 1, 'character', '表型',
    'output_prefix', 'o', 1, 'character', '输出文件路径'),
    byrow=T, ncol=5
)
args=getopt(command)

if (!is.null(args$help) || is.null(args$alt_counts_file) || is.null(args$ref_counts_file) || is.null(args$genotype_file) || is.null(args$phenotype_file) || is.null(args$output_prefix)) {
  cat(paste(getopt(command, usage = T), "\n"))
  q(status=1)
}


########## DATA READ IN ##########
## genotype
genotype <- read.table(args$genotype_file,header=T,row.names=1,stringsAsFactors=F)
heterozygosity <- t(apply(genotype,1,function(x)ifelse(x==1,TRUE, FALSE)))
## phenotype
phenotype <- read.table(args$phenotype_file,header=T,row.names=1,stringsAsFactors=F)
## count 
ref_count <- read.table(args$ref_counts_file,header=T,row.names=1,stringsAsFactors=F)
alt_count <- read.table(args$alt_counts_file,header=T,row.names=1,stringsAsFactors=F)
total_count <- ref_count+alt_count

########## MAIN FUNCTION ##########
phenotype_cal <- function(line){
    pheno_now <- line
    pos.del= which(pheno_now > (mean(pheno_now)+3*sd(pheno_now)) | pheno_now < (mean(pheno_now)-3*sd(pheno_now))) ## 离群点
    if(length(pos.del)>0){ 
        environmentVar <- pheno_now[-pos.del]
        alt <- t(alt_count[,-pos.del])
        ref <- t(ref_count[,-pos.del])
        het <- t(heterozygosity[,-pos.del])
        eqtlGenotypes <- t(genotype[,-pos.del])
        totalreads <- t(total_count[,-pos.del])
    }else{
        environmentVar= pheno_now 
        alt <- t(alt_count)
        ref <- t(ref_count)
        het <- t(heterozygosity)
        eqtlGenotypes <- t(genotype)
        totalreads <- t(total_count)
    }
    ########## Default parameters ##########

    count.cutoff=5 # monoallelic if fewer reads than this...
    prop.cutoff=0.01 # ...or lower proportion than this mapping to one allele
    prop.mono.cutoff=0.5 # maximum proportion of hets who are allowed to how monoallelic expression
    minSampleSize=20
    minGroupSize=10 # minimum testable individuals in an environmental group (e.g. smokers)
    minModel=T     
    alt.list <- list()
    n.list <- list()
    x.null <- list()
    x.full <- list()
    original.index <- list()
    # iterate over exonic SNPs
    non.problematic.counter=1
    for (snp.index in 1:dim(eqtlGenotypes)[2]) {
        if (snp.index %% 1000 == 0){
              print(snp.index)}
        valid=het[,snp.index] & totalreads[,snp.index]>5 ## 对每个样本的布尔值 杂合&total reads > 5 
        valid[which(is.na(valid))]=FALSE ## NA设为False
        # check we have at least 20 valid samples 若该位点符合条件的个体数量小于minSampleSize(20)，舍去，进入下一个点
        if (sum(na.omit(valid))<minSampleSize)
            next
        ## 只保留符合条件的个体
        a=alt[valid,snp.index]
        r=ref[valid,snp.index]
        heteq=eqtlGenotypes[valid,snp.index]==1  
        x=environmentVar[valid]
        # check not too many are in one group (e.g. female, non-smokers)
        if ((length(x)-max(table(x)))<minGroupSize) 
            next
        n=a+r
        # check there isn't too much mono-allelic expression 是否太偏向一个allel
        min.a.r=apply(cbind(a,r),1,min)
        is.mono=(min.a.r<count.cutoff)|((as.double(min.a.r)/n)<prop.cutoff)  
        if (mean(is.mono)>prop.mono.cutoff)
            next
        ## 将较少的allel设为alt
        alt.list[[non.problematic.counter]]=if (minModel) pmin(a,r) else a
        n.list[[non.problematic.counter]]=n
        original.index[[non.problematic.counter]]=snp.index
        num.samples=length(x)
        #print(num.samples)  
        x.full[[non.problematic.counter]]=cbind(env=x,intercept=numeric(num.samples)+1.0)
        x.null[[non.problematic.counter]]=cbind(intercept=numeric(num.samples)+1.0)
        # add eQTL heterozygosity
        if (!any(is.na(heteq))) if ((sd(heteq)>0) & (min(table(heteq))>5)){ 
            x.full[[non.problematic.counter]]=cbind(x.full[[non.problematic.counter]],eqtl=heteq)
            x.null[[non.problematic.counter]]=cbind(x.null[[non.problematic.counter]],eqtl=heteq)
            # lots of conditions to decide whether to add an interaction terms
            if (min(table(heteq))>=10) { # only if at least 10 hets and 10 non-hets
                e1=x[heteq==1.0]
                e0=x[heteq==0.0]    
                if ((length(e1)-max(table(e1)))>=10 & (length(e0)-max(table(e0)))>=10){ 
                    if (length(unique(x))>2 | min(table(x,heteq))>=5){ 
                        temp=cbind(x.full[[non.problematic.counter]],interaction=x*heteq)
                        if (det(t(temp) %*% temp) > 1e-8){
                            x.full[[non.problematic.counter]]=temp
                        }
                    }
                }
            }
        }
    non.problematic.counter=non.problematic.counter+1
    }
    original.index=unlist(original.index)
    #---------------- run the model --------------------------
    library('eagle')
    s=eagle.settings()
    s$debug=F
    s$rev.model=2 # local regression
    s$normalised.depth=scale(log10(unlist(lapply(n,mean)))) # only required for rev.model=3
    s$max.iterations=10000
    s$convergence.tolerance=.001
    s$coeff.regulariser=0.1
    s$learn.rev=T
    # learnt parameters from the DGN dataset
    s$rep.global.shape=1.0
    s$rep.global.rate=0.0033
    s$traceEvery=1
    system.time( res <- eagle.helper(alt.list,n.list,x.full,x.null,s) ) 

    res <- t(rbind(colnames(eqtlGenotypes)[original.index],res$p.values))
    return(res)
}

cl <- makeCluster(getOption("cl.cores", length(rownames(phenotype))))
clusterExport(cl,varlist=c('genotype','heterozygosity','ref_count','alt_count','total_count'),envir = environment())
result <- parApply(cl, phenotype, 1, phenotype_cal)

for(i in 1:length(rownames(phenotype))){
    res <- data.frame(result[[i]])
    colnames(res) <- c('SNP','p_value')
    res$p_value <- as.numeric(as.character(res$p_value))
    res$FDR <-p.adjust(res$p_value,method = 'BH')
    res <- res[order(res$FDR),]
    output <- paste(args$output_prefix,rownames(phenotype)[i],'.ASE.association.txt',sep='')
    write.table(res,output,quote=F,sep='\t',row.names=F,col.names=T)
}





