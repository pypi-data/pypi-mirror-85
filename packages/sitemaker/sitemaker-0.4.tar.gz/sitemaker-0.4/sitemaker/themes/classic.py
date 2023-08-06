from sitemaker import *
class theme_css:

    def __init__(self):
        self.css=None
        self.navbar_background="#aeaca8"
        self.navbar_color="black"
        self.header_background="#eeeeee"
        self.footer_background="#aeaca8"
        self.body_color="#f9f8f6;"
        self.main_background="white"
        self.accent="#de6581"

    def build(self):
        if not self.css:
            self.css=cssfile()
            c_main=css("main")
            c_main.add("max-width","1000px")
            c_main.add("margin","0px auto 0px auto")
            c_main.add("background",self.main_background)
            c_main.add("height","auto")
            c_main.add("border"," 2px solid black")
        
            c_body=css("body",2)
            c_body.add("background",self.body_color)
            
            c_header=css("header")
            c_header.add("background",self.header_background)
            c_header.add("min-height","100px")
            
            c_navbar=css("navbar")
            c_navbar.add("background",self.navbar_background)
            c_navbar.add("clear","both")
            c_navbar.add("border-top"," 1px solid black")
            c_navbar.add("border-bottom"," 1px solid black")
            c_navbar.add("min-height","30px")
            c_navbar.add("color",self.navbar_color)
            c_navbar.add("vertical-align","middle")
            
            c_footer=css("footer",2)
            c_footer.add("font-size","80%")
            c_footer.add("min-height","100px")
            c_footer.add("padding","20px")
            c_footer.add("color","black")
            c_footer.add("background",self.footer_background)
            c_footer.add("text-align","center")
            c_footer.add("border-top","1px solid black")
            
            
            c_link=css("a",2)
            c_link.add("color",self.accent)
            c_link.add("text-decoration","none")

            c_h=css("h1, h2, h3 h2",2)
            c_h.add("font-weight"," normal")
            
            c_h2=css("h2",2)
            c_h2.add("margin","10px 0px 5px 0px")
            c_h2.add("padding"," 0px")

            c_h3=css("h3",2)
            c_h3.add("margin","0px 0px 10px 0px")
            c_h3.add("color",self.accent)

            c_nav_ul=css("nav ul",2)
            c_nav_ul.add("margin","0px")
            c_nav_ul.add("padding","5px 0px 5px 30px")

            c_nav_li=css("nav li",2)
            c_nav_li.add("display","inline")
            c_nav_li.add("margin-right","40px")

            c_nav_a=css("nav li a",2)
            c_nav_a.add("color","#ffffff")

            c_nav_aa=css("nav li a:hover, nav li a.current",2)
            c_nav_aa.add("color","#000000")
            
            c_menu=css("menu")
            c_menu.add("background","red")
            c_menu.add("text-align","center")
            
            c_article=css("article",2)
            c_article.add("clear","both")
            c_article.add("overflow","auto")
            c_article.add("max-width","100%")

            c_figure=css("figure",2)
            c_figure.add("float","left")
            c_figure.add("max-width","290px")
            c_figure.add("height","220px")
            c_figure.add("padding","5px")
            c_figure.add("margin","20px")
            c_figure.add("border"," 1px solid #eeeeee")
            
            c_img_medium=css("img.medium",2)
            c_img_medium.add("height","250px")
            
            c_img_large=css("img.large",2)
            c_img_large.add("height","500px")
            
            c_img_small=css("img.small",2)
            c_img_small.add("height","125px")
            
            c_ctx=css("content")
            c_ctx.add("min-height","350px")
            c_ctx.add("margin","3%")
            c_ctx.add("background",self.main_background)
        
            self.css.addCss(c_main)
            self.css.addCss(c_header)
            self.css.addCss(c_menu)
            self.css.addCss(c_body)
            self.css.addCss(c_footer)
            self.css.addCss(c_navbar)
            self.css.addCss(c_link)
            self.css.addCss(c_h)
            self.css.addCss(c_h2)
            self.css.addCss(c_h3)
            self.css.addCss(c_nav_ul)
            self.css.addCss(c_nav_li)
            self.css.addCss(c_nav_a)
            self.css.addCss(c_nav_aa)
            self.css.addCss(c_article)
            self.css.addCss(c_figure)
            self.css.addCss(c_img_medium)
            self.css.addCss(c_img_small)
            self.css.addCss(c_img_large)
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
        t.setClass("header")
        t.setItem(0,0,self.logo)
        t.setItem(0,1,item(H(self.title,2)))
        c.addItem(t)
        for n in self.menu:
            nav.addItem(n)
        c.addItem(nav)
        self.p.header=div(c,"header")
        ctx=div(cls="content")
        for sec in self.sections:
            ctx.addItem(div(sec,cls="section"))
        self.p.content=ctx
        footer=tagged("footer")
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
