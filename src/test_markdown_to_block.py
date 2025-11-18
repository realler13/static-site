import unittest

from block_markdown import (
    markdown_to_html_node,
    block_to_html_node,
    text_to_children,
    paragraph_to_html_node,
    heading_to_html_node,
    code_to_html_node,
    olist_to_html_node,
    ulist_to_html_node,
    quote_to_html_node,
    BlockType
)


class TestTextToChildren(unittest.TestCase):
    def test_text_to_children_plain(self):
        text = "Just plain text"
        children = text_to_children(text)
        self.assertEqual(len(children), 1)
        self.assertEqual(children[0].value, "Just plain text")
    
    def test_text_to_children_with_formatting(self):
        text = "Text with **bold** and _italic_"
        children = text_to_children(text)
        self.assertEqual(len(children), 4)  # Fixed: 4 children, not 5
        self.assertEqual(children[0].value, "Text with ")
        self.assertEqual(children[1].tag, "b")
        self.assertEqual(children[1].value, "bold")


class TestParagraphToHTMLNode(unittest.TestCase):
    def test_simple_paragraph(self):
        block = "This is a simple paragraph."
        node = paragraph_to_html_node(block)
        self.assertEqual(node.tag, "p")
        self.assertEqual(len(node.children), 1)
    
    def test_paragraph_with_formatting(self):
        block = "This has **bold** text"
        node = paragraph_to_html_node(block)
        self.assertEqual(node.tag, "p")
        self.assertTrue(len(node.children) > 1)
    
    def test_paragraph_multiline(self):
        block = "Line one\nLine two\nLine three"
        node = paragraph_to_html_node(block)
        html = node.to_html()
        self.assertIn("Line one Line two Line three", html)


class TestHeadingToHTMLNode(unittest.TestCase):
    def test_heading_h1(self):
        block = "# Heading 1"
        node = heading_to_html_node(block)
        self.assertEqual(node.tag, "h1")
        self.assertEqual(node.children[0].value, "Heading 1")
    
    def test_heading_h2(self):
        block = "## Heading 2"
        node = heading_to_html_node(block)
        self.assertEqual(node.tag, "h2")
    
    def test_heading_h6(self):
        block = "###### Heading 6"
        node = heading_to_html_node(block)
        self.assertEqual(node.tag, "h6")
    
    def test_heading_with_formatting(self):
        block = "# Heading with **bold**"
        node = heading_to_html_node(block)
        self.assertEqual(node.tag, "h1")
        self.assertTrue(len(node.children) > 1)


class TestCodeToHTMLNode(unittest.TestCase):
    def test_code_block(self):
        block = "```\ncode here\n```"
        node = code_to_html_node(block)
        self.assertEqual(node.tag, "pre")
        self.assertEqual(node.children[0].tag, "code")
    
    def test_code_block_multiline(self):
        block = "```\ndef hello():\n    print('world')\n```"
        node = code_to_html_node(block)
        html = node.to_html()
        self.assertIn("def hello():", html)
    
    def test_invalid_code_block(self):
        block = "```code without closing"
        with self.assertRaises(ValueError):
            code_to_html_node(block)


class TestOListToHTMLNode(unittest.TestCase):
    def test_ordered_list(self):
        block = "1. First\n2. Second\n3. Third"
        node = olist_to_html_node(block)
        self.assertEqual(node.tag, "ol")
        self.assertEqual(len(node.children), 3)
        self.assertEqual(node.children[0].tag, "li")
    
    def test_ordered_list_with_formatting(self):
        block = "1. **Bold** item\n2. _Italic_ item"
        node = olist_to_html_node(block)
        self.assertEqual(len(node.children), 2)


class TestUListToHTMLNode(unittest.TestCase):
    def test_unordered_list(self):
        block = "- First\n- Second\n- Third"
        node = ulist_to_html_node(block)
        self.assertEqual(node.tag, "ul")
        self.assertEqual(len(node.children), 3)
        self.assertEqual(node.children[0].tag, "li")
    
    def test_unordered_list_with_formatting(self):
        block = "- **Bold** item\n- `code` item"
        node = ulist_to_html_node(block)
        self.assertEqual(len(node.children), 2)


class TestQuoteToHTMLNode(unittest.TestCase):
    def test_simple_quote(self):
        block = ">This is a quote"
        node = quote_to_html_node(block)
        self.assertEqual(node.tag, "blockquote")
    
    def test_multiline_quote(self):
        block = ">Line one\n>Line two\n>Line three"
        node = quote_to_html_node(block)
        html = node.to_html()
        self.assertIn("Line one Line two Line three", html)
    
    def test_invalid_quote(self):
        block = ">Valid line\nInvalid line"
        with self.assertRaises(ValueError):
            quote_to_html_node(block)


class TestMarkdownToHTMLNode(unittest.TestCase):
    def test_simple_markdown(self):
        markdown = "# Heading\n\nThis is a paragraph."
        node = markdown_to_html_node(markdown)
        self.assertEqual(node.tag, "div")
        self.assertEqual(len(node.children), 2)
    
    def test_complex_markdown(self):
        markdown = """# Title

This is a paragraph with **bold** text.

## Subtitle

- Item 1
- Item 2

>A quote here"""
        node = markdown_to_html_node(markdown)
        self.assertEqual(node.tag, "div")
        self.assertEqual(len(node.children), 5)
    
    def test_markdown_with_code(self):
        markdown = "# Code Example\n\n```\ndef hello():\n    print(\"world\")\n```\n\nThat's the code."
        node = markdown_to_html_node(markdown)
        html = node.to_html()
        self.assertIn("<pre>", html)
        self.assertIn("<code>", html)
    
    def test_full_document(self):
        markdown = """# My Document

This is a paragraph.

## Section 1

Here's a list:

1. First item
2. Second item
3. Third item

## Section 2

>This is a quote
>with multiple lines

And a final paragraph."""
        node = markdown_to_html_node(markdown)
        html = node.to_html()
        self.assertIn("<h1>", html)
        self.assertIn("<h2>", html)
        self.assertIn("<ol>", html)
        self.assertIn("<blockquote>", html)


if __name__ == "__main__":
    unittest.main()