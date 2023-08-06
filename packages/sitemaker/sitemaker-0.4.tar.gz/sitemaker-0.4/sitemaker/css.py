CSS_CLASS=0
CSS_ID=1
CSS_TAG=2


class css_attr:
    def __init__(self,name,value):
        self.name=name
        self.value=value
        

class cssfile:
    def __init__(self):
         self.csss=[]
         self.path=""

    def addCss(self,item):
        self.csss.append(item)
        
    def build(self):
        ctx=""
        for c in self.csss:
            ctx+=c.build()
        return ctx

    def save(self,path="index.css"):
        with open(path,"w") as file:
            file.write(self.build()+"\n")

class rawcss:

    def __init__(self,ctx):
        self.content=ctx
    
    def build(self):
        ret=""
        for line in self.content.split("\n"):
            ret+=line.strip()+"\n"
        return ret


class css(cssfile):
    def __init__(self,name,typ=0):
        # type 0 = .name   { == class
        # type 1 = #name { == id
        # type 2 = name    { == tag
        self.name=name
        self.attrs=[]
        self.csss=[]
        self.type=typ
            
    def add(self,name,value):
       self.attrs.append(css_attr(name,value))

    def build(self):
        if self.type == 0:
            ctx="."
        elif self.type == 1:
            ctx="#"
        elif self.type == 2:
            ctx=""
        ctx+=self.name+" {\n"
        for a in self.attrs:
            ctx+=str(a.name)+": "+str(a.value)+";\n"
        for c in self.csss:
            ctx+=c.build()
        ctx+="}\n"
        return ctx
        
