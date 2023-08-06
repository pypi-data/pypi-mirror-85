page_template = '''<!DOCTYPE html> 
 <html> 
  <head> 
   <meta charset="UTF-8"/> 
   <style>
     {css}
   </style>
   <title>{title}</title> 
  </head> 
  <body> 
    <div class="content">
      <div class="sidenav">
        <h3>Links</h3>
        {links}
      </div>
      <div class="article">
        <h1>{title}</h1>
        {content}
      </div>
    </div>
  </body> 
</html>
'''


def page_layout(title, content, css):
    return page_template.format(
        title=title,
        content=content.body,
        css=css,
        links=content.links)

