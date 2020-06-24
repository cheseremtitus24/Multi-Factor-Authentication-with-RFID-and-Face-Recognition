
def format_key():
    try:
        infile = open("cheserem.key", mode='r')
        # print(infile.read())
        tmp = infile.read()
        # print("Temp file " + tmp)
        tmp2 = tmp.split()
        # print(tmp2)
        holder = []
        holder.append(tmp2[2:])
        # print("holder contains ")
        # print(holder)
        combine_to_string = []
        for item in holder:
            combine_to_string += item
        # print(combine_to_string)
        holdings = ""
        for item in combine_to_string:
            holdings += item
        # print(holdings)
        almost_done = holdings.split("0x")
        holdings2 = ""
        for item in almost_done:
            holdings2 += item
        # print(holdings2.__len__())
        return holdings2
    except:
        print("REading failed")
    finally:
        infile.close()

# print(format_key())