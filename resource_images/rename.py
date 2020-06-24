import os

path = "../images/kioko/"
print(path)
list_ = os.listdir(path)
print(list_)
#saves all files in a list
sequence = 0
for item in list_:
    name,extension = os.path.splitext(item)
    print(name)
    incriment = sequence
    new_name: str = f"{incriment}"
    sequence = sequence + 1


    # os.renames(name + extension, new_name+ extension)
    os.rename(path+name+extension,path+new_name+extension)