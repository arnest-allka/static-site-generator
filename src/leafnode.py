from htmlnode import HTMLNode

class LeafNode(HTMLNode):
    def __init__(self, tag: str = None, value: str = None, props: dict = None):
        if value is None or (tag!='img' and not value):
            raise ValueError("LeafNode must have a value")
        super().__init__(tag, value, None, props)
        
    def to_html(self):
        if self.value is None or (self.tag!='img' and not self.value):
            raise ValueError("All leaf nodes must have a value")
        elif not self.tag:
            return f"{self.value}"
        else:
            props = self.props_to_html().strip()
            if self.tag!='img':
                return f"<{self.tag}{' '+props if props else ''}>{self.value}</{self.tag}>"
            else:
                return f"<{self.tag}{' '+props if props else ''}>{self.value}"
            
    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"