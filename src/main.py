import os
import sys
from textnode import TextNode, TextType, text_node_to_html_node
from static_to_public import static_to_public
from generate_page import generate_pages_recursive

def main():
    
    basepath = sys.argv[1] if len(sys.argv) > 1 else "/"
    
    print(TextNode("Some text", TextType.LINK, "https://www.boots.dev"))
    
    static_to_public("static", "docs")
    generate_pages_recursive("content", "template.html", "docs", basepath)

if __name__ == "__main__":
    main()