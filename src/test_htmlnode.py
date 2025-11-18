import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_repr(self):
        node = HTMLNode("p", "This is a paragraph")
        self.assertEqual(repr(node), "HTMLNode(p, This is a paragraph, None, None)")
    
    def test_repr_with_props(self):
        node = HTMLNode("a", "Click me", None, {"href": "https://www.boot.dev"})
        self.assertEqual(
            repr(node), 
            "HTMLNode(a, Click me, None, {'href': 'https://www.boot.dev'})"
        )
    
    def test_props_to_html(self):
        node = HTMLNode("a", "Link", None, {"href": "https://www.boot.dev", "target": "_blank"})
        props_html = node.props_to_html()
        # This test will help you discover the bug in your props_to_html method!
        self.assertIn("href=", props_html)
        self.assertIn("target=", props_html)
    
    def test_to_html_raises_error(self):
        node = HTMLNode("p", "test")
        with self.assertRaises(NotImplementedError):
            node.to_html()
    
    def test_init_defaults(self):
        node = HTMLNode()
        self.assertIsNone(node.tag)
        self.assertIsNone(node.value)
        self.assertIsNone(node.children)
        self.assertIsNone(node.props)

class TestLeafNode(unittest.TestCase):
    def test_to_html_no_tag(self):
        node = LeafNode(None, "Just plain text")
        self.assertEqual(node.to_html(), "Just plain text")
    
    def test_to_html_with_tag(self):
        node = LeafNode("p", "This is a paragraph")
        self.assertEqual(node.to_html(), "<p>This is a paragraph</p>")
    
    def test_to_html_with_props(self):
        node = LeafNode("a", "Click me", {"href": "https://www.boot.dev"})
        self.assertEqual(node.to_html(), '<a href="https://www.boot.dev">Click me</a>')
    
    def test_no_value_raises_error(self):
        node = LeafNode("p", None)
        with self.assertRaises(ValueError):
            node.to_html()
    
    def test_to_html_bold(self):
        node = LeafNode("b", "Bold text")
        self.assertEqual(node.to_html(), "<b>Bold text</b>")


class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )
    def test_to_html_with_one_child(self):
        node = ParentNode(
            "p",
            [LeafNode(None, "Hello world")]
        )
        self.assertEqual(node.to_html(), "<p>Hello world</p>")
    
    def test_to_html_with_multiple_children(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, " and "),
                LeafNode("i", "italic text")
            ]
        )
        self.assertEqual(node.to_html(), "<p><b>Bold text</b> and <i>italic text</i></p>")
    
    def test_to_html_with_nested_parents(self):
        node = ParentNode(
            "div",
            [
                ParentNode("p", [LeafNode(None, "First paragraph")]),
                ParentNode("p", [LeafNode(None, "Second paragraph")])
            ]
        )
        self.assertEqual(node.to_html(), "<div><p>First paragraph</p><p>Second paragraph</p></div>")
    
    def test_no_tag_raises_error(self):
        node = ParentNode(None, [LeafNode(None, "text")])
        with self.assertRaises(ValueError):
            node.to_html()
    
    def test_no_children_raises_error(self):
        node = ParentNode("div", None)
        with self.assertRaises(ValueError):
            node.to_html()
    
    def test_deeply_nested(self):
        node = ParentNode(
            "div",
            [
                ParentNode(
                    "ul",
                    [
                        ParentNode("li", [LeafNode("b", "Item 1")]),
                        ParentNode("li", [LeafNode("b", "Item 2")])
                    ]
                )
            ]
        )
        expected = "<div><ul><li><b>Item 1</b></li><li><b>Item 2</b></li></ul></div>"
        self.assertEqual(node.to_html(), expected)


if __name__ == "__main__":
    unittest.main()