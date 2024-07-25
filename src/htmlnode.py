class HTMLNode:
    def __init__(self, tag: str = None, value: str = None, children: list = None, props: dict = None):
        self.tag = tag
        self.value = value 
        self.children = children if children is not None else []
        self.props = props if props is not None else {}
        
    def to_html(self):
        raise NotImplementedError()
    
    def props_to_html(self):
        props_str = ""
        if self.props:
            for key, value in self.props.items():
                props_str += f'{key}="{value}" '
        return props_str
    
    def __repr__(self):
        result = "HTMLNode:\n"
        if self.tag:
            result += f"tag: {self.tag}\n"
        if self.value:
            result += f"value: {self.value}\n"
        if self.children:
            result += f"children: {self.children}\n"
        if self.props:
            result += f"props: {self.props}\n"
        return result