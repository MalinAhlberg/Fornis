def pylist_to_conslist(in_list):
    out_list = ()

    for el in reversed(in_list):
        out_list = (el,out_list)

    return out_list


def suffix_conslist(in_list):
    
    while in_list:
        yield in_list
        in_list = in_list[1]



if __name__=='__main__':
    
    p = ['a','a','a','b','b','c']
    
    c = pylist_to_conslist(p)

    print p
    print c

    for s in suffix_conslist(c):
        print s
