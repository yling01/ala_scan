import os
import numpy as np
global min_residue
min_residue = 3
max_distance = 10
from os import path
import shutil 
import sys
def extract_files():
    start = "PyRosettaResults/"
    root = []
    for root_temp, dummy, dummy in os.walk(start):
        if root_temp != start:
            root.append(root_temp)
    return root

def extract_hotspots(result_file):
    hotspots = []
    result_file = result_file + "/ddG_out_total.txt"
    read = False
    with open(result_file) as fo:
        for line in fo:
            if read:
                hotspots.append(line.strip())
            elif line == "Likely Hotspot Residues\n":
                read = True
    return hotspots

def if_less_than_cutoff(resid_array):
    assert len(resid_array) >= min_residue
    if resid_array[-1] - resid_array[0] <= max_distance:
        return True
    for i in range(len(resid_array) - 2):
        if resid_array[i + 2] - resid_array[i] <= max_distance:
            return True
    return False 

def identify_hotloop(hotspots):
    if len(hotspots) < 3:
        return False
    chainA_count = 0
    chainB_count = 0
    resid_A = []
    resid_B = []
    for info in hotspots:
        chain = info.split()[0]
        resid = int(info.split()[1])
        if chain == "A":
            chainA_count += 1
            resid_A.append(resid)
        else:
            chainB_count += 1
            resid_B.append(resid)

    if chainA_count < min_residue and chainB_count < min_residue:
        return False 

    if chainA_count >= min_residue:
        if if_less_than_cutoff(resid_A):
            return True

    elif chainB_count >= min_residue:
        return if_less_than_cutoff(resid_B)

    return False

if __name__ == '__main__':
    
    if path.exists("results_filtered.txt"):
        os.remove("results_filtered.txt")
    hotloop_found = False
    for directory in extract_files():
        file_directory_head = "Results_Clean"
        hotspots = extract_hotspots(directory)
        if identify_hotloop(hotspots):
            pdb_filename = "../" + directory.split("/")[1][0:-4] + ".pdb"
            assert os.path.exists(pdb_filename)
            file_directory = "/".join((file_directory_head, directory.split("/")[1][0:-4]))
            if not os.path.exists(file_directory):
                os.makedirs(file_directory) 
            pdb_copy = "/".join((file_directory, pdb_filename.split("/")[1]))
            shutil.copyfile(pdb_filename, pdb_copy)
            file_name = file_directory + "/out_hotspots.txt"
            hotloop_found = True
            write = False
            result_file = directory + "/ddG_out_total.txt"
            with open(result_file, "r") as fi:
                lines = fi.readlines()
                with open("results_filtered.txt", "a") as fo:
                    with open(file_name, "w+") as fo_separate:
                        header = "=> " + result_file + " <=\n"
                        fo.write(header)
                        for line in lines:
                            fo.write(line)
                            if write:
                                fo_separate.write(line)
                            elif line == "Likely Hotspot Residues\n":
                                write = True
                        fo.write("\n\n")
    if not hotloop_found:
        print("No Potential Hotloop Found")


