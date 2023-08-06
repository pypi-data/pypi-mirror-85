def get_tag(tag="body",s=""):
    i=False
    ret=""
    for line in s.split("\n"):
        for word in line.split(" "):
            if "</"+tag in word:
                i=False
            if i:
                ret+=word+" "
            if "<"+tag in word:
                i=True
        if i:
            ret+="\n"
    return ret
