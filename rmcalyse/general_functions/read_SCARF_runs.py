import os
from supercell_class import SuperCell

head_path = '/Users/Anton/Documents/SCARF/STO_xNB_all/scarf_STO-00NB_10-10-10/'

rmc6f_file = '/SrTiO3_00Nb.rmc6f'

# def read_SCARF(filename, head_path)

run_files = os.listdir(head_path)

if '.DS_Store' in run_files:
    run_files.remove('.DS_Store')

else:
    pass

run_list = []

for run_dir in run_files:
    path = head_path + run_dir + rmc6f_file
    rmc_data = SuperCell(path)
    run_list.append(rmc_data)


run_list[0].get_data()
run_list[0].orthonormalise_cell()
print(run_list[0].orth_pos_lbl[:5])
