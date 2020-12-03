import os

# A dict with keys being the old filenames and values being the new filenames
mapping = {}

# Read through the mapping file line-by-line and populate 'mapping'
with open('ant_man_card_name.txt') as mapping_file:
    for line in mapping_file:
        # Split the line along whitespace
        # Note: this fails if your filenames have whitespace
        old_name, new_name = line.split()
        # The names in the mapping file all have "04" as a prefix and then also leading 0s
        # whereas the actual image files do not have that
        # so this just gets rid of the unwanted prefixes to create a new mapping file that matches the existing image file names
        old_name = old_name.lstrip("0")
        old_name = old_name.lstrip("12")
        old_name = old_name.lstrip("0")
        mapping[old_name] = new_name
        
        
for filename in os.listdir('C:\Development\OCTGN-Marvel-Champions\images\Ant-Man'):
    root, extension = os.path.splitext(filename)
    stripped_root = root.replace("MC12en_","")
    if stripped_root in mapping:
        if stripped_root[-1] == 'b':
            os.rename(os.path.join('C:\Development\OCTGN-Marvel-Champions\images\Ant-Man',filename), os.path.join('C:\Development\OCTGN-Marvel-Champions\images\Ant-Man',''.join(mapping[stripped_root] + '.b' + extension)))
        elif stripped_root[-1] == 'c':
            os.rename(os.path.join('C:\Development\OCTGN-Marvel-Champions\images\Ant-Man',filename), os.path.join('C:\Development\OCTGN-Marvel-Champions\images\Ant-Man',''.join(mapping[stripped_root] + '.c' + extension)))
        else:
            os.rename(os.path.join('C:\Development\OCTGN-Marvel-Champions\images\Ant-Man',filename), os.path.join('C:\Development\OCTGN-Marvel-Champions\images\Ant-Man',''.join(mapping[stripped_root] + extension)))
