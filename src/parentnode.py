from htmlnode import HTMLNode

class ParentNode(HTMLNode):
  def __init__(self, tag, children, props=None):
    super().__init__(tag, None, children, props)

  def to_html(self):
    if self.tag is None:
      raise ValueError("ParentNode must have a tag")
    
    if self.children is None or len(self.children) == 0:
      raise ValueError("ParentNode must have children")
    
    children_html = "".join(list(map(lambda child: child.to_html(), self.children)))

    return f"<{self.tag}>{children_html}</{self.tag}>"