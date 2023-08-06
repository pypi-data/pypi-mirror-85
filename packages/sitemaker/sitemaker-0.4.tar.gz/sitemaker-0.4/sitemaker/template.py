from sitemaker.items import item

class content:

    def __init__(self):
        self.items=[]
        
    def addItem(self,item):
        self.items.append(item)
        
    def addText(self,txt):
       self.items.append(item(txt))
        
    def build(self):
        content=""
        for item in self.items:
            content+="\n"+item.build()
        return content

      
        
class page:

    def __init__(self):
        self.init()
        
    def init(self):
        self.header=content()
        self.content=content()
        self.footer=content()
        self.title=None
        self.rels=[]
        
        self.ctx=""
        self.path="./index.html"

    
    def build(self):
        content="<html>\n"
        content+="<head>\n"
        if self.title != None:
            content+="<title>"+self.title+"</title>\n"
        for rel in self.rels:
            content+=rel.build()+"\n"
        content+="</head>\n"
        content+="<body>\n"
        content+="<div class=\"main\">\n"
        content+="<!--header begin-->"
        content+=self.header.build()+"\n"
        content+="<!--header end-->\n"
        content+="<!--content begin-->"
        content+=self.content.build()+"\n"
        content+="<!--content end-->\n"
        content+="<!--footer begin-->"
        content+=self.footer.build()+"\n"
        content+="<!--footer end-->\n"
        content+="</div>"
        content+="</body>\n"
        content+="</html>\n"
        ctx=content
        return content
    
    def save(self,path="./index.html"):
        with open(path,"w") as file:
            file.write(self.build())
            
    def addRel(self,href=None,rel="Stylesheet",typ=None,name="link"):
         ctx="<"+name+" "
         if rel:
             ctx+="rel=\""+str(rel)+"\" "
         if typ:
             ctx+="type=\""+str(typ)+"\" "
         if href:
             ctx+="href=\""+str(href)+"\" "
         ctx+="/>"
         self.rels.append(item(ctx))
        
class site:
    def __init__(self):
        self.pages=[]
        
    def addPage(self,page):
        self.pages.append(page)

    def save(self):
        for page in self.pages:
            page.save()
        
