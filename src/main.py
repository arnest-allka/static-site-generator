from leafnode import LeafNode


def main():
    leaf_node = LeafNode(tag="span", value="Example text", props={"class": "example-class"})
    print(leaf_node)
    print(leaf_node.to_html())
    
main()