from htmlnode import HTMLNode

class ParentNode(HTMLNode):  
    def __init__(self, tag, children, props=None):
        super().__init__(tag=tag, value=None, children=children, props=props)
        
    def to_html(self):
        if self.tag is None: 
            raise ValueError("parent missing tag")
        if self.children is None:
            raise ValueError("parent missing children")
        child_text = ""
        for nodes in self.children:
            child_text += nodes.to_html()
        return f"<{self.tag}{self.props_to_html()}>{child_text}</{self.tag}>"
