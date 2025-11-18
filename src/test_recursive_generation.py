import unittest
import os
import shutil
from generate_page import generate_pages_recursive  # Replace 'your_module' with your actual module name


class TestGeneratePagesRecursive(unittest.TestCase):
    
    def setUp(self):
        """
        Create temporary directories and files before each test.
        This runs automatically before each test method.
        """
        # Define paths for test directories and template
        self.test_content_dir = "test_content"
        self.test_dest_dir = "test_dest"
        self.template_path = "test_template.html"
        
        # Create the content and destination directories
        os.makedirs(self.test_content_dir, exist_ok=True)
        os.makedirs(self.test_dest_dir, exist_ok=True)
        
        # Create a simple HTML template with placeholders
        template_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{{ Title }}</title>
</head>
<body>
    {{ Content }}
</body>
</html>"""
        
        with open(self.template_path, 'w') as f:
            f.write(template_content)
    
    def tearDown(self):
        """
        Clean up temporary directories and files after each test.
        This runs automatically after each test method.
        """
        # Remove test directories if they exist
        if os.path.exists(self.test_content_dir):
            shutil.rmtree(self.test_content_dir)
        if os.path.exists(self.test_dest_dir):
            shutil.rmtree(self.test_dest_dir)
        
        # Remove template file if it exists
        if os.path.exists(self.template_path):
            os.remove(self.template_path)
    
    def test_single_markdown_file(self):
        """
        Test that a single markdown file is converted correctly.
        Should create an index.html with the title and content.
        """
        # Create a test markdown file
        md_file_path = os.path.join(self.test_content_dir, "test.md")
        md_content = "# Hello World\n\nThis is a test paragraph."
        
        with open(md_file_path, 'w') as f:
            f.write(md_content)
        
        # Run the function on the single file
        # When processing a single file directly, it goes to dest_dir_path/index.html
        generate_pages_recursive(md_file_path, self.template_path, self.test_dest_dir)
        
        # Check that the output file was created
        output_file = os.path.join(self.test_dest_dir, "index.html")
        self.assertTrue(os.path.exists(output_file), "Output index.html should exist")
        
        # Read the output file and verify its content
        with open(output_file, 'r') as f:
            html_output = f.read()
        
        # Verify the title was inserted
        self.assertIn("<title>Hello World</title>", html_output, "Title should be in the HTML")
        
        # Verify the content was converted and inserted
        self.assertIn("This is a test paragraph.", html_output, "Paragraph content should be in the HTML")
        self.assertIn("<h1>", html_output, "H1 tag should be present for the title")
    
    def test_directory_with_multiple_files(self):
        """
        Test that a directory with multiple markdown files creates
        separate subdirectories for each file (without .md extension).
        """
        # Create multiple markdown files
        files_data = {
            "page1.md": "# Page One\n\nThis is the first page.",
            "page2.md": "# Page Two\n\nThis is the second page.",
            "page3.md": "# Page Three\n\nThis is the third page."
        }
        
        for filename, content in files_data.items():
            filepath = os.path.join(self.test_content_dir, filename)
            with open(filepath, 'w') as f:
                f.write(content)
        
        # Run the function on the directory
        generate_pages_recursive(self.test_content_dir, self.template_path, self.test_dest_dir)
        
        # Verify each file created its own subdirectory with index.html
        # The .md extension should be stripped from the directory name
        expected_outputs = {
            "page1": ("Page One", "This is the first page."),
            "page2": ("Page Two", "This is the second page."),
            "page3": ("Page Three", "This is the third page.")
        }
        
        for subdir_name, (expected_title, expected_content) in expected_outputs.items():
            # The subdirectory should be named without .md extension
            output_file = os.path.join(self.test_dest_dir, subdir_name, "index.html")
            
            # Check that the file exists
            self.assertTrue(os.path.exists(output_file), 
                          f"Output file should exist at {output_file}")
            
            # Verify the content
            with open(output_file, 'r') as f:
                html_output = f.read()
            
            self.assertIn(expected_title, html_output, 
                         f"Title '{expected_title}' should be in {output_file}")
            self.assertIn(expected_content, html_output, 
                         f"Content '{expected_content}' should be in {output_file}")
    
    def test_nested_directories(self):
        """
        Test that nested directory structures are preserved
        when generating pages recursively.
        """
        # Create a nested directory structure
        # test_content/
        #   └── subdir/
        #       └── nested.md
        subdir_path = os.path.join(self.test_content_dir, "subdir")
        os.makedirs(subdir_path, exist_ok=True)
        
        # Create a markdown file in the subdirectory
        nested_md_path = os.path.join(subdir_path, "nested.md")
        nested_content = "# Nested Page\n\nThis is nested content."
        
        with open(nested_md_path, 'w') as f:
            f.write(nested_content)
        
        # Run the function on the parent directory
        generate_pages_recursive(self.test_content_dir, self.template_path, self.test_dest_dir)
        
        # Verify the nested structure was created
        # Should create: test_dest/subdir/nested/index.html (without .md extension)
        expected_output = os.path.join(self.test_dest_dir, "subdir", "nested", "index.html")
        
        self.assertTrue(os.path.exists(expected_output), 
                       f"Nested output should exist at {expected_output}")
        
        # Verify the content
        with open(expected_output, 'r') as f:
            html_output = f.read()
        
        self.assertIn("Nested Page", html_output, "Title should be in nested HTML")
        self.assertIn("This is nested content.", html_output, "Content should be in nested HTML")
    
    def test_deeply_nested_directories(self):
        """
        Test that deeply nested directory structures work correctly.
        """
        # Create a deeper nested structure
        # test_content/
        #   └── level1/
        #       └── level2/
        #           └── deep.md
        deep_dir = os.path.join(self.test_content_dir, "level1", "level2")
        os.makedirs(deep_dir, exist_ok=True)
        
        deep_md_path = os.path.join(deep_dir, "deep.md")
        deep_content = "# Deep Page\n\nThis is deeply nested."
        
        with open(deep_md_path, 'w') as f:
            f.write(deep_content)
        
        # Run the function
        generate_pages_recursive(self.test_content_dir, self.template_path, self.test_dest_dir)
        
        # Verify the deep structure (without .md extension)
        expected_output = os.path.join(self.test_dest_dir, "level1", "level2", "deep", "index.html")
        
        self.assertTrue(os.path.exists(expected_output), 
                       "Deeply nested output should exist")
        
        with open(expected_output, 'r') as f:
            html_output = f.read()
        
        self.assertIn("Deep Page", html_output)
        self.assertIn("This is deeply nested.", html_output)
    
    def test_mixed_files_and_directories(self):
        """
        Test processing a directory that contains both files and subdirectories.
        """
        # Create a file in the root
        root_md = os.path.join(self.test_content_dir, "root.md")
        with open(root_md, 'w') as f:
            f.write("# Root Page\n\nRoot content.")
        
        # Create a subdirectory with a file
        subdir = os.path.join(self.test_content_dir, "articles")
        os.makedirs(subdir, exist_ok=True)
        
        article_md = os.path.join(subdir, "article.md")
        with open(article_md, 'w') as f:
            f.write("# Article Page\n\nArticle content.")
        
        # Run the function
        generate_pages_recursive(self.test_content_dir, self.template_path, self.test_dest_dir)
        
        # Verify both outputs exist (without .md extension)
        root_output = os.path.join(self.test_dest_dir, "root", "index.html")
        article_output = os.path.join(self.test_dest_dir, "articles", "article", "index.html")
        
        self.assertTrue(os.path.exists(root_output), "Root file output should exist")
        self.assertTrue(os.path.exists(article_output), "Article output should exist")
        
        # Verify content
        with open(root_output, 'r') as f:
            self.assertIn("Root Page", f.read())
        
        with open(article_output, 'r') as f:
            self.assertIn("Article Page", f.read())
    
    def test_empty_directory(self):
        """
        Test that an empty directory doesn't cause errors.
        """
        # The directory is already created in setUp and is empty
        # This should run without errors
        generate_pages_recursive(self.test_content_dir, self.template_path, self.test_dest_dir)
        
        # The destination directory should exist but be empty
        self.assertTrue(os.path.exists(self.test_dest_dir))
        # Check that dest_dir is empty
        dest_contents = os.listdir(self.test_dest_dir)
        # Should be empty since no markdown files were processed
        self.assertEqual(len(dest_contents), 0, "Destination should be empty for empty source")
    
    def test_multiple_files_in_nested_structure(self):
        """
        Test a more complex directory structure with multiple files at various levels.
        """
        # Create structure:
        # test_content/
        #   ├── index.md
        #   ├── about.md
        #   └── blog/
        #       ├── post1.md
        #       └── post2.md
        
        # Root level files
        with open(os.path.join(self.test_content_dir, "index.md"), 'w') as f:
            f.write("# Home\n\nWelcome home.")
        
        with open(os.path.join(self.test_content_dir, "about.md"), 'w') as f:
            f.write("# About\n\nAbout us.")
        
        # Blog directory with posts
        blog_dir = os.path.join(self.test_content_dir, "blog")
        os.makedirs(blog_dir, exist_ok=True)
        
        with open(os.path.join(blog_dir, "post1.md"), 'w') as f:
            f.write("# First Post\n\nFirst post content.")
        
        with open(os.path.join(blog_dir, "post2.md"), 'w') as f:
            f.write("# Second Post\n\nSecond post content.")
        
        # Run the function
        generate_pages_recursive(self.test_content_dir, self.template_path, self.test_dest_dir)
        
        # Verify all outputs exist
        expected_files = [
            ("index", "index.html", "Home", "Welcome home."),
            ("about", "index.html", "About", "About us."),
            (os.path.join("blog", "post1"), "index.html", "First Post", "First post content."),
            (os.path.join("blog", "post2"), "index.html", "Second Post", "Second post content."),
        ]
        
        for subdir, filename, title, content in expected_files:
            output_path = os.path.join(self.test_dest_dir, subdir, filename)
            self.assertTrue(os.path.exists(output_path), 
                          f"Output should exist at {output_path}")
            
            with open(output_path, 'r') as f:
                html = f.read()
                self.assertIn(title, html, f"Title should be in {output_path}")
                self.assertIn(content, html, f"Content should be in {output_path}")
    
    def test_md_extension_stripping(self):
        """
        Specifically test that .md extension is stripped from directory names.
        """
        # Create a file with .md extension
        md_file = os.path.join(self.test_content_dir, "my-page.md")
        with open(md_file, 'w') as f:
            f.write("# My Page\n\nContent here.")
        
        # Run the function on the directory
        generate_pages_recursive(self.test_content_dir, self.template_path, self.test_dest_dir)
        
        # Should create test_dest/my-page/index.html (NOT test_dest/my-page.md/index.html)
        correct_output = os.path.join(self.test_dest_dir, "my-page", "index.html")
        wrong_output = os.path.join(self.test_dest_dir, "my-page.md", "index.html")
        
        self.assertTrue(os.path.exists(correct_output), 
                       "Output should exist without .md in directory name")
        self.assertFalse(os.path.exists(wrong_output), 
                        "Output should NOT exist with .md in directory name")
    
    def test_non_markdown_files_ignored(self):
        """
        Test that non-.md files are handled appropriately (if at all).
        """
        # Create a markdown file and a non-markdown file
        with open(os.path.join(self.test_content_dir, "page.md"), 'w') as f:
            f.write("# Page\n\nContent.")
        
        with open(os.path.join(self.test_content_dir, "readme.txt"), 'w') as f:
            f.write("This is a readme.")
        
        # Run the function
        generate_pages_recursive(self.test_content_dir, self.template_path, self.test_dest_dir)
        
        # The markdown file should be processed
        md_output = os.path.join(self.test_dest_dir, "page", "index.html")
        self.assertTrue(os.path.exists(md_output), "Markdown file should be processed")
        
        # The .txt file behavior depends on your implementation
        # It might create an empty directory or skip it entirely
        # Adjust this assertion based on your desired behavior
    
    def test_directory_with_index_file(self):
        """
        Test a common web pattern: a directory with an index.md file.
        """
        # Create test_content/about/index.md
        about_dir = os.path.join(self.test_content_dir, "about")
        os.makedirs(about_dir, exist_ok=True)
        
        index_md = os.path.join(about_dir, "index.md")
        with open(index_md, 'w') as f:
            f.write("# About Us\n\nLearn about our team.")
        
        # Run the function
        generate_pages_recursive(self.test_content_dir, self.template_path, self.test_dest_dir)
        
        # Should create test_dest/about/index/index.html
        output = os.path.join(self.test_dest_dir, "about", "index", "index.html")
        self.assertTrue(os.path.exists(output), "Index file should be processed")
        
        with open(output, 'r') as f:
            html = f.read()
            self.assertIn("About Us", html)
            self.assertIn("Learn about our team.", html)


if __name__ == "__main__":
    unittest.main()