from concurrent.futures import ProcessPoolExecutor
import subprocess as sp
import sys

rootdir = "fill_this_in"

def run_ale(path):
    
    try:
        observe = "ALEobserve " + path + " burnin=0"
        sp.call(observe, shell=True)
        #print(observe)
        move = "mv " + path + ".ale " + path.replace("gene_trees", "results") + ".ale"
        sp.call(move, shell=True)
        run = "ALEml_undated " + rootdir + "/protein/rp16/rp16_crossenv.cpronly.treefile " + \
            path.replace("gene_trees", "results") + ".ale separators=$ " + \
            "fraction_missing=" + rootdir + "ale/fraction_missing.txt"
        sp.call(run, shell=True)
        #print(run)
    
    except:
        print("Error with %s" %(path))
        
input_list = [item.strip() for item in open(sys.argv[1]).readlines()]

with ProcessPoolExecutor(48) as executor:
    executor.map(run_ale, input_list)
