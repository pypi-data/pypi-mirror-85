from sitemaker import *
class theme_css:

    def __init__(self):
        self.css=None
        self.navbar_background="black"
        self.navbar_color="white"
        self.header_background="black"
        self.footer_background="black"
        self.body_color="black"
        self.text_color="white"
        self.main_background="black"
        self.accent="blue"

    def build(self):
        if not self.css:
            self.css=cssfile()
            c_main=css("main")
            c_main.add("max-width","1000px")
            c_main.add("margin","auto")

            c_main.add("text-align","center")
            c_main.add("align-items","center")
            c_main.add("background",self.main_background)
            c_main.add("height","auto")
        
            c_body=css("body",2)
            c_body.add("background",self.body_color)
            c_body.add("color",self.text_color)

            
            c_header=css("header")
            c_header.add("text-align","center")
            c_header.add("background",self.header_background)
            c_header.add("min-height","100px")
            
            c_navbar=css("navbar")
            c_navbar.add("background",self.navbar_background)
            c_navbar.add("clear","both")
            c_navbar.add("text-align","center")
            c_navbar.add("min-height","30px")
            c_navbar.add("color",self.navbar_color)
            
            c_footer=css("footer",2)
            c_footer.add("min-height","100px")
            c_footer.add("padding","20px")
            c_footer.add("color","black")
            c_footer.add("background",self.footer_background)
            c_footer.add("text-align","center")
            
            
            c_link=css("a",2)
            c_link.add("color",self.accent)
            c_link.add("text-decoration","none")

            c_h3=css("h3",2)
            c_h3.add("margin","0px 0px 10px 0px")
            c_h3.add("color",self.accent)
            
            c_ctx=css("content")
            c_ctx.add("min-height","350px")
            c_ctx.add("margin","3%")
            c_ctx.add("text-align","left")
            c_ctx.add("align-items","left")
            c_ctx.add("background",self.main_background)
        
            self.css.addCss(c_main)
            self.css.addCss(c_header)
            self.css.addCss(c_body)
            self.css.addCss(c_footer)
            self.css.addCss(c_navbar)
            self.css.addCss(c_link)
            self.css.addCss(c_h3)
            self.css.addCss(c_ctx)
            return self.css.build()
            
    def save(self,path):
          with open(path,"w") as file:
            file.write(self.build())

class theme_page:

    def __init__(self):
        self.p=page()
        self.logo=image()
        self.menu=[]
        self.sections=[]
        self.title=""
        self.footers=[]
        
    def build(self):
        c=content()
        nav=navbar("h",cls="navbar")
        t=table(1,2)
        t.setItem(0,0,self.logo)
        t.setItem(0,1,item(H(self.title,2)))
        c.addItem(t)
        for n in self.menu:
            nav.addItem(n)
        c.addItem(nav)
        c.addItem(item("<hr>"))
        self.p.header=center(c)
        ctx=div(cls="content")
        for sec in self.sections:
            ctx.addItem(div(sec,cls="section"))
        self.p.content=ctx
        footer=tagged("footer")
        footer.addItem(item("<hr>"))
        for f in self.footers:
            footer.addItem(f)
        self.p.footer=footer
        return self.p.build()

    def add(self,item):
        self.sections.append(item)
        
    def addFooter(self,item):
        self.footers.append(item)

    def addCss(self,name):
        self.p.addRel(name)
        
    def save(self,path="index.html"):
        with open(path,"w") as file:
            file.write(self.build())
