import unittest

from textnode import TextNode, TextType, text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD_TYPE)
        node2 = TextNode("This is a text node", TextType.BOLD_TYPE)
        self.assertEqual(node, node2)

    def test_neq(self):
        node = TextNode("This is a text node and it's long", TextType.ITALIC_TYPE)
        node2 = TextNode("This is a text node", TextType.BOLD_TYPE)
        self.assertNotEqual(node, node2)
    
    def test_url(self):
        node = TextNode("This is a text node", TextType.BOLD_TYPE)
        node2 = TextNode("This is a text node", TextType.BOLD_TYPE, "http://www.boot.dev")
        self.assertNotEqual(node, node2) 

class TestTextNodeToHTMLNode(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.PLAIN_TYPE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
    
    def test_bold(self):
        node = TextNode("Bold text", TextType.BOLD_TYPE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "Bold text")
    
    def test_italic(self):
        node = TextNode("Italic text", TextType.ITALIC_TYPE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "Italic text")
    
    def test_code(self):
        node = TextNode("print('hello')", TextType.CODE_TYPE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "print('hello')")
    
    def test_link(self):
        node = TextNode("Click here", TextType.LINK_TYPE, "https://www.boot.dev")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "Click here")
        self.assertEqual(html_node.props, {"href": "https://www.boot.dev"})
    
    def test_image(self):
        node = TextNode("Alt text", TextType.IMAGE_TYPE, "https://example.com/image.png")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, None)
        self.assertEqual(html_node.props, {"src": "https://example.com/image.png", "alt": "Alt text"})


    def test_text(self):
        node = TextNode("This is a text node", TextType.PLAIN_TYPE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")


if __name__ == "__main__":
    unittest.main()