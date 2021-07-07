#!/opt/anaconda3/bin/python


#		What interpretor

'''
#-------------------------------------------------------------------------------
'''
       
print("                                                                   ")
print("-------------------------------------------------------------------")
print("                             Lets have a go                        ")
print("-------------------------------------------------------------------")
print("                                                                   ")
   
   
#		I love a good print statment

'''
#-------------------------------------------------------------------------------
'''


#rmc6f_input = open(raw_input("Specify a file: ") + ".rmc6f", "r")
rmc6f_input = open("1_Test.rmc6f", "r")


#		Load the file!

'''
#-------------------------------------------------------------------------------
'''                                                           


line_density = []
line_supercell = []
line_cell =[]
line_atom_list = []

for i in rmc6f_input:
	#	header
	if i.find("Number density") >= 0:
		line_density = i
	if i.find("Supercell") >= 0:
		line_supercell = i
	if i.find("Cell") >= 0:
		line_cell = i
	#	atom lines
	if i.find("[1]") >= 0:
		line_atom_list.append(i)		
rmc6f_input.close()

#		extract the useful header info and make a list of the atom lines

'''
#-------------------------------------------------------------------------------
''' 

import re
temp = re.findall('\d+\.\d+', line_density)
density = [float(i) for i in temp]
temp = re.findall('[-+]?\d*\.\d+|\d+', line_supercell)
supercell = [int(i) for i in temp]
temp = re.findall('[-+]?\d*\.\d+|\d+', line_cell)
cell = [float(i) for i in temp]


#print(line_density)
print(" Density:")
print(density)
print("\n Supercell:")
#print(line_supercell)
print(supercell)
print("\n Cell Parameters:")
#print(line_cell)
print(cell)


#		Deal with the header

'''
#-------------------------------------------------------------------------------
''' 

atom_list = []
for line in line_atom_list:
	temp = []
	temp_1 = re.findall(r'\b\d+\b', line)		#	ints
	temp_2 = re.findall('[a-zA-Z]+', line)		#	letters
	temp_3 = re.findall('\d+\.\d+', line)		#	floats
	temp.append(temp_2[0])
	temp.append(int(temp_1[0]))
	temp.append(float(temp_3[0]))
	temp.append(float(temp_3[1]))
	temp.append(float(temp_3[2]))
	atom_list.append(temp)


print("\n The Format of the List-of-Lists: ")
print(atom_list[0])
#print(line_atom_list[0])                              


#		sort the atom lines and create a list of lists where each list
#		is the element, atom number, and the xyx coordintates
                  
'''
#-------------------------------------------------------------------------------
'''                              

       
print("                                                                   ")
print("-------------------------------------------------------------------")
print("                             Well go on then                       ")
print("-------------------------------------------------------------------")
print("                                                                   ")
          
