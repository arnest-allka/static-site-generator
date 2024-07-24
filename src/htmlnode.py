class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value 
        self.children = children
        self.props = props
        
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