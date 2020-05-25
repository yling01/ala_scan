import os
import ala_scan

def main():
	pdb_files = os.listdir()
	for pdb_filename in pdb_files:
		if pdb_filename == "test.pdb" or pdb_filename[-3:] != "pdb":
			continue
		partners = "A_B"
		mutant_aa = "A"
		neighbor_cutoff = 8.0
		interface_cutoff = 4.0
		repack_cutoff = 6.5
		trials = 20
		trial_output = "ddG_out"
		output = False

	    scanning(pdb_filename, partners, mutant_aa,
	        neighbor_cutoff, interface_cutoff, repack_cutoff,
	        trials, trial_output, output)

if __name__ == '__main__':
	main()