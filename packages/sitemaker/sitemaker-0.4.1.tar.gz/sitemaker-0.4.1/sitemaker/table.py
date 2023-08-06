from sitemaker.containers import container
from sitemaker.items import item
class table(container):
    def __init__(self,x=1,y=1):
        self.container_init()
        self.items=[]

        for i in range(0,x):
            row=[]
            for j in range(0,y):
                row.append(item())
            self.items.append(row)
                    
    def setItem(self,x=0,y=0,item=None):
        if item:
            self.items[x][y]=item
            
    def build(self):
        self.content="<table "
        for a in self.attrs:
                self.content+=" "+str(a.name)+"=\""+str(a.value)+"\" "
        self.content+=">\n"
        for i in self.items:
            self.content+="<tr>\n"
            for j in i:
                self.content+="<th>\n"
                self.content+=j.build()
                self.content+="</th>\n"
            self.content+="</tr>\n"
        self.content+="</table>\n"
        return self.content                
