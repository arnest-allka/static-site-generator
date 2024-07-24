class TextNode():
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url
        
    def __eq__(self, other):
        if self.text == other.text and self.text_type == other.text_type:
            if self.url and other.url:
                if self.url == other.url:
                    return True
                else:
                    return False
            else:
                return True
        else:
            return False
        
        
    def __repr__(self):
        if self.url:
            return f"TextNode({self.text}, {self.text_type}, {self.url})"
        else:
            return f"TextNode({self.text}, {self.text_type})"

