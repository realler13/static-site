import unittest
from inline_markdown import (
    split_nodes_delimiter, 
    extract_markdown_links, 
    extract_markdown_images,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes,
    extract_title
)


from textnode import TextNode, TextType


class TestInlineMarkdown(unittest.TestCase):
    def test_delim_bold(self):
        node = TextNode("This is text with a **bolded** word", TextType.PLAIN_TYPE)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD_TYPE)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.PLAIN_TYPE),
                TextNode("bolded", TextType.BOLD_TYPE),
                TextNode(" word", TextType.PLAIN_TYPE),
            ],
            new_nodes,
        )

    def test_delim_bold_double(self):
        node = TextNode(
            "This is text with a **bolded** word and **another**", TextType.PLAIN_TYPE
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD_TYPE)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.PLAIN_TYPE),
                TextNode("bolded", TextType.BOLD_TYPE),
                TextNode(" word and ", TextType.PLAIN_TYPE),
                TextNode("another", TextType.BOLD_TYPE),
            ],
            new_nodes,
        )

    def test_delim_bold_multiword(self):
        node = TextNode(
            "This is text with a **bolded word** and **another**", TextType.PLAIN_TYPE
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD_TYPE)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.PLAIN_TYPE),
                TextNode("bolded word", TextType.BOLD_TYPE),
                TextNode(" and ", TextType.PLAIN_TYPE),
                TextNode("another", TextType.BOLD_TYPE),
            ],
            new_nodes,
        )

    def test_delim_italic(self):
        node = TextNode("This is text with an _italic_ word", TextType.PLAIN_TYPE)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC_TYPE)
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.PLAIN_TYPE),
                TextNode("italic", TextType.ITALIC_TYPE),
                TextNode(" word", TextType.PLAIN_TYPE),
            ],
            new_nodes,
        )

    def test_delim_bold_and_italic(self):
        node = TextNode("**bold** and _italic_", TextType.PLAIN_TYPE)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD_TYPE)
        new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC_TYPE)
        self.assertListEqual(
            [
                TextNode("bold", TextType.BOLD_TYPE),
                TextNode(" and ", TextType.PLAIN_TYPE),
                TextNode("italic", TextType.ITALIC_TYPE),
            ],
            new_nodes,
        )

    def test_delim_code(self):
        node = TextNode("This is text with a `code block` word", TextType.PLAIN_TYPE)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE_TYPE)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.PLAIN_TYPE),
                TextNode("code block", TextType.CODE_TYPE),
                TextNode(" word", TextType.PLAIN_TYPE),
            ],
            new_nodes,
        )
class TestMarkdownExtraction(unittest.TestCase):
    def test_extract_single_image(self):
        text = "This is text with an ![image](https://example.com/image.png)"
        result = extract_markdown_images(text)
        self.assertEqual(result, [("image", "https://example.com/image.png")])
    
    def test_extract_multiple_images(self):
        text = "![first](https://img1.com) and ![second](https://img2.com)"
        result = extract_markdown_images(text)
        self.assertEqual(result, [("first", "https://img1.com"), ("second", "https://img2.com")])
    
    def test_extract_no_images(self):
        text = "This is plain text with no images"
        result = extract_markdown_images(text)
        self.assertEqual(result, [])
    
    def test_extract_single_link(self):
        text = "This is text with a [link](https://www.boot.dev)"
        result = extract_markdown_links(text)
        self.assertEqual(result, [("link", "https://www.boot.dev")])
    
    def test_extract_multiple_links(self):
        text = "[first](https://link1.com) and [second](https://link2.com)"
        result = extract_markdown_links(text)
        self.assertEqual(result, [("first", "https://link1.com"), ("second", "https://link2.com")])
    
    def test_extract_no_links(self):
        text = "This is plain text with no links"
        result = extract_markdown_links(text)
        self.assertEqual(result, [])
    
    def test_links_dont_extract_images(self):
        text = "![image](https://img.com) and [link](https://link.com)"
        result = extract_markdown_links(text)
        self.assertEqual(result, [("link", "https://link.com")])
    
    def test_images_dont_extract_links(self):
        text = "![image](https://img.com) and [link](https://link.com)"
        result = extract_markdown_images(text)
        self.assertEqual(result, [("image", "https://img.com")])
    
    def test_extract_image_with_empty_alt(self):
        text = "![](https://example.com/image.png)"
        result = extract_markdown_images(text)
        self.assertEqual(result, [("", "https://example.com/image.png")])

    def test_split_image(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.PLAIN_TYPE,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.PLAIN_TYPE),
                TextNode("image", TextType.IMAGE_TYPE, "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes,
        )

    def test_split_image_single(self):
        node = TextNode(
            "![image](https://www.example.COM/IMAGE.PNG)",
            TextType.PLAIN_TYPE,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE_TYPE, "https://www.example.COM/IMAGE.PNG"),
            ],
            new_nodes,
        )

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.PLAIN_TYPE,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.PLAIN_TYPE),
                TextNode("image", TextType.IMAGE_TYPE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.PLAIN_TYPE),
                TextNode(
                    "second image", TextType.IMAGE_TYPE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with a [link](https://boot.dev) and [another link](https://blog.boot.dev) with text that follows",
            TextType.PLAIN_TYPE,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.PLAIN_TYPE),
                TextNode("link", TextType.LINK_TYPE, "https://boot.dev"),
                TextNode(" and ", TextType.PLAIN_TYPE),
                TextNode("another link", TextType.LINK_TYPE, "https://blog.boot.dev"),
                TextNode(" with text that follows", TextType.PLAIN_TYPE),
            ],
            new_nodes,
        )

class TestTextToTextNodes(unittest.TestCase):
    def test_plain_text(self):
        text = "This is plain text"
        result = text_to_textnodes(text)
        expected = [TextNode("This is plain text", TextType.PLAIN_TYPE)]
        self.assertEqual(result, expected)
    
    def test_bold_text(self):
        text = "This is **bold** text"
        result = text_to_textnodes(text)
        expected = [
            TextNode("This is ", TextType.PLAIN_TYPE),
            TextNode("bold", TextType.BOLD_TYPE),
            TextNode(" text", TextType.PLAIN_TYPE)
        ]
        self.assertEqual(result, expected)
    
    def test_italic_text(self):
        text = "This is _italic_ text"
        result = text_to_textnodes(text)
        expected = [
            TextNode("This is ", TextType.PLAIN_TYPE),
            TextNode("italic", TextType.ITALIC_TYPE),
            TextNode(" text", TextType.PLAIN_TYPE)
        ]
        self.assertEqual(result, expected)
    
    def test_code_text(self):
        text = "This is `code` text"
        result = text_to_textnodes(text)
        expected = [
            TextNode("This is ", TextType.PLAIN_TYPE),
            TextNode("code", TextType.CODE_TYPE),
            TextNode(" text", TextType.PLAIN_TYPE)
        ]
        self.assertEqual(result, expected)
    
    def test_all_formats(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        result = text_to_textnodes(text)
        expected = [
            TextNode("This is ", TextType.PLAIN_TYPE),
            TextNode("text", TextType.BOLD_TYPE),
            TextNode(" with an ", TextType.PLAIN_TYPE),
            TextNode("italic", TextType.ITALIC_TYPE),
            TextNode(" word and a ", TextType.PLAIN_TYPE),
            TextNode("code block", TextType.CODE_TYPE),
            TextNode(" and an ", TextType.PLAIN_TYPE),
            TextNode("obi wan image", TextType.IMAGE_TYPE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.PLAIN_TYPE),
            TextNode("link", TextType.LINK_TYPE, "https://boot.dev"),
        ]
        self.assertEqual(result, expected)
    
    def test_multiple_bold(self):
        text = "**First** and **second** bold"
        result = text_to_textnodes(text)
        expected = [
            TextNode("First", TextType.BOLD_TYPE),
            TextNode(" and ", TextType.PLAIN_TYPE),
            TextNode("second", TextType.BOLD_TYPE),
            TextNode(" bold", TextType.PLAIN_TYPE)
        ]
        self.assertEqual(result, expected)
    
    def test_image_and_link(self):
        text = "![image](https://img.com) [link](https://link.com)"
        result = text_to_textnodes(text)
        expected = [
            TextNode("image", TextType.IMAGE_TYPE, "https://img.com"),
            TextNode(" ", TextType.PLAIN_TYPE),
            TextNode("link", TextType.LINK_TYPE, "https://link.com")
        ]
        self.assertEqual(result, expected)

class TestExtractTitle(unittest.TestCase):
    
    def test_title_at_beginning(self):
        """Test that a title at the start of the markdown is extracted correctly"""
        markdown = "# Hello World\n\nThis is some content."
        result = extract_title(markdown)
        self.assertEqual(result, "Hello World")
    
    def test_title_after_content(self):
        """Test that the first h1 title is found even if there's content before it"""
        markdown = "Some intro text\n\n# My Title\n\nMore content here."
        result = extract_title(markdown)
        self.assertEqual(result, "My Title")
    
    def test_multiple_titles_returns_first(self):
        """Test that when multiple h1 headers exist, only the first is returned"""
        markdown = "# First Title\n\nSome content\n\n# Second Title"
        result = extract_title(markdown)
        self.assertEqual(result, "First Title")
    
    def test_no_title_returns_none(self):
        """Test that None is returned when no h1 header exists"""
        markdown = "Just some regular text\n\nWith multiple paragraphs"
        result = extract_title(markdown)
        self.assertIsNone(result)
    
    def test_title_with_extra_spaces(self):
        """Test that extra spaces after the # are stripped correctly"""
        markdown = "#    Title With Spaces   \n\nContent here."
        result = extract_title(markdown)
        self.assertEqual(result, "Title With Spaces")
    
    def test_empty_markdown(self):
        """Test that empty markdown returns None"""
        markdown = ""
        result = extract_title(markdown)
        self.assertIsNone(result)
    
    def test_h2_not_matched(self):
        """Test that h2 headers (##) are not matched as titles"""
        markdown = "## This is h2\n\n# This is h1"
        result = extract_title(markdown)
        self.assertEqual(result, "This is h1")
    
    def test_title_only(self):
        """Test markdown that contains only a title"""
        markdown = "# Just A Title"
        result = extract_title(markdown)
        self.assertEqual(result, "Just A Title")
    
    def test_title_with_special_characters(self):
        """Test that titles with special characters are preserved"""
        markdown = "# Title with $pecial Ch@racters!\n\nContent"
        result = extract_title(markdown)
        self.assertEqual(result, "Title with $pecial Ch@racters!")


if __name__ == "__main__":
    unittest.main()
