from sitemaker.containers import container
from sitemaker.items import item, attr
HORIZORTAL=0
VERTICAL=1

class navbar(container):
    def __init__(self,typ=0,cls=None):
        self.type=typ
        self.container_init()
        if cls:
            self.addAttr("class",cls)
        
    def addItem(self,i):
        self.items.append(i)
        
    def build(self):
        self.content="<nav"
        for a in self.attrs:
                self.content+=" "+str(a.name)+"=\""+str(a.value)+"\" "
        self.content+=">\n"
        self.content+="<ul>\n"
        for i in self.items:
            self.content+="<li"
            if self.type == 0:
                self.content+=" style=\"display: block;\" "
            self.content+=">"
            self.content+=i.getItem().build()
            self.content+="</li>\n"
        self.content+="</ul>\n"
        self.content+="</nav>"
        return self.content
