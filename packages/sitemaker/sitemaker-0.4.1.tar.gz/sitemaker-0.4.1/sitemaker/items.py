class item:

    def __init__(self,ctx=""):
        return self.init(ctx)

    def init(self,ctx=""):
        self.content=ctx
        
    def getItem(self):
        return self

        
    def build(self):
        return self.content

class attr:
    def __init__(self,name,value):
        self.name=name
        self.value=value

class line(item):

    def __init__(self,ctx=""):
        self.init(ctx+"<br>")
    def setText(self,ctx=""):
        self.content=ctx+"<br>"
    def getItem(self):
        return self
        
class script(item):

    def __init__(self,ctx=""):
        self.init("<script>\n"+ctx+"\n</script>\n")

    def setText(self,ctx=""):
        self.content="<script>\n"+ctx+"\n</script>\n"


class image(item):

    def __init__(self,src=None,cls=None):
        self.init()
        self.attrs=[]
        if src:
            self.addAttr("src",src)
        if cls:
            self.addAttr("class",cls)
        
    def addAttr(self,name,value):
        self.attrs.append(attr(name,value))
        
    def setImage(self,src):
        self.addAttr("src",src)
        
    def build(self):
        
        self.content="<img "
        for a in self.attrs:
                self.content+=str(a.name)+"=\""+str(a.value)+"\" "
        self.content+=">"
        return self.content

