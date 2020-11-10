a_table = [['ID', 'Name', 'Age'], ['1', 'John', '35'], ['2', 'Joseph', '40']]

print(a_table)


length_list = [len(element) for row in a_table for element in row]
#Find lengths of row elements


column_width = max(length_list)
#Longest element sets column_width

for row in a_table:
    row = "".join(element.ljust(column_width + 2) for element in row)
#Print elements with even spacing

    print(row)
