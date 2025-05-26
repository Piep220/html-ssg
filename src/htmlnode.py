class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("to_html method not implemented")
    
    def props_to_html(self):
        if self.props is None:
            return ""
        return_string = ""
        for key, value in self.props.items():
            return_string = return_string + f" {key}=\"{value}\""
        return return_string
    
    def __eq__(self, other):
        if not isinstance(other, HTMLNode):
            return False
        return (
            self.tag == other.tag and
            self.value == other.value and
            self.children == other.children and
            self.props == other.props
        )

    def __repr__(self):
        #return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"
        return f"HTMLNode({self.tag}, {self.value}, children: {self.children}, {self.props})"
    
class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag=tag, value=value, children=[], props=props)
        
    def to_html(self):
        if self.value is None: 
            raise ValueError("leaf missing tag")
        if self.tag is None:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
    
    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"



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
