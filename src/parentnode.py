from htmlnode import HTMLNode

class ParentNode(HTMLNode):
    def __init__(self, tag: str = None, children: list = None, props: dict = None):
        if not children:
            raise ValueError("ParentNode must have children")
        if not tag:
            raise ValueError("ParentNode must have a tag")
        super().__init__(tag, None, children, props)
        
    def to_html(self):
        if not self.tag:
            raise ValueError("All parent nodes must have a tag")
        elif not self.children:
            raise ValueError("All parent nodes must have children")
        else:
            props = self.props_to_html().strip()
            front_tag =  f"<{self.tag}{' '+props if props else ''}>"
            for child in self.children:
                front_tag += child.to_html()
            return front_tag + f"</{self.tag}>"
        
    def __repr__(self):
        return f"ParentNode({self.tag}, children: {self.children}, {self.props})"