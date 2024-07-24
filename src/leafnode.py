from htmlnode import HTMLNode

class LeafNode(HTMLNode):
    def __init__(self, tag=None, value=None, props=None):
        if not value:
            raise ValueError("All leaf nodes must have a value")
        super().__init__(tag, value, None, props)
        
    def to_html(self):
        if not self.value:
            raise ValueError("All leaf nodes must have a value")
        elif not self.tag:
            return f"{self.value}"
        else:
            props = self.props_to_html().strip()
            return f"<{self.tag}{' '+props if props else ''}>{self.value}</{self.tag}>"
        