def markup(s,m="",cls=None):
    ret="<"+m
    if cls:
        ret+=" class=\""+cls + "\""
    ret+=">"+s+"</"+m+">"
    return ret
    
def bold(s,cls=None):
    return markup(s,"b",cls)
    
def italic(s,cls=None):
    return markup(s,"i",cls)
    
def H(s,size=1,cls=None):
    return markup(s,("H"+str(size)),cls)
    
