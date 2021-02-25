from multiprocessing import Pool
from Bio import SeqIO
import os
import gzip
import pandas as pd
import sys
from datetime import date

def datestamp():
    return date.today().strftime("%Y-%m-%d")

rootdir = "fill_this_in"
reads = [line.strip() for line in open(rootdir + "/metadata/read_files.txt").readlines()]
print(reads)

#sys.exit()

# get per sample read counts in parallel
sample_read_counts = {}

def compute(readfile):
    
    count = 0
    
    try:
        
        with gzip.open(readfile, "rt") as handle:
            for record in SeqIO.FastaIO.SimpleFastaParser(handle):
                count+=1

        return (os.path.basename(readfile), count)
    
    except: return(os.path.basename(readfile), "None")

p = Pool(min(len(reads),48))
pools = p.map(compute, reads)

print("Done")

for item in pools:
    sample_read_counts[item[0]] = item[1]
    
sdf = pd.DataFrame.from_dict(sample_read_counts, orient="index").reset_index()
sdf.columns = ["sample", "read_count"]
sdf.to_csv(rootdir + "/metadata/read_counts_" + datestamp() + ".tsv", sep="\t", index=False)

sys.exit()
