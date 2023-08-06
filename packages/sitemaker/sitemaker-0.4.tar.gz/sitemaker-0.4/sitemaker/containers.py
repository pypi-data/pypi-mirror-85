from sitemaker.items import item, attr

class container(item):

    def __init__(self,i=None,cls=None):
        self.container_init(i,cls)        
        if i:
            self.items.append(i)
        if cls:
            self.addAttr("class",cls)


    def addItem(self,item):
        self.items.append(item.getItem())

    def addText(self,ctx):
        self.items.append(item(ctx))

    def addLine(self,ctx):
        self.items.append(item(ctx+"<br>"))
        
    def addAttr(self,name,value):
        self.attrs.append(attr(name,value))


    def setClass(self,cls):
        self.attrs.append(attr("class",cls))
        
    def setId(self,id):
        self.attrs.append(attr("id",id))

    def container_init(self,i=None,cls=None):
        self.items=[]
        self.attrs=[]
        self.init()
        self.items=[]

        
class tagged(container):
    def __init__(self,tag="",i=None,cls=None):
        self.container_init(i,cls)
        self.tag=tag
        if i:
            self.items.append(i)
        if cls:
            self.addAttr("class",cls)

    
    def build(self):
        self.content+="<"+self.tag
        for a in self.attrs:
                self.content+=" "+str(a.name)+"=\""+str(a.value)+"\" "
        self.content+=">\n"
        for j in self.items:
            self.content+=j.build()
        self.content+="\n</"+self.tag+">\n"
        return self.content


class div(tagged):
     def __init__(self,i=None,cls=None):
        self.container_init(i,cls)
        self.tag="div"
        if i:
            self.items.append(i)
        if cls:
            self.addAttr("class",cls)


class center(tagged):
     def __init__(self,i=None,cls=None):
        self.container_init(i,cls)
        self.tag="center"
        if i:
            self.items.append(i)
        if cls:
            self.addAttr("class",cls)


class span(tagged):
    def __init__(self,i=None,cls=None):
        self.container_init(i,cls)
        self.tag="span"
        if i:
            self.items.append(i)
        if cls:
            self.addAttr("class",cls)


class link(tagged):
    def __init__(self,href="",content="",cls=None,i=None):
        self.container_init(i,cls)
        self.tag="a"
        self.addAttr("href",href)
        self.items.append(item(content))
        if cls:
            self.addAttr("class",cls)

