import unittest
import os
import shutil
from static_to_public import static_to_public

class TestStaticToPublic(unittest.TestCase):
    
    def setUp(self):
        """Create test directories before each test"""
        self.test_dir = "test_temp"
        self.static_path = os.path.join(self.test_dir, "static")
        self.public_path = os.path.join(self.test_dir, "public")
        
        # Clean up any existing test directory
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
        
        # Create fresh test directories
        os.makedirs(self.test_dir)
    
    def tearDown(self):
        """Clean up test directories after each test"""
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
    
    def _create_test_file(self, path, content="test content"):
        """Helper method to create a test file with content"""
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w') as f:
            f.write(content)
    
    def test_copy_simple_files(self):
        """Test copying files without subdirectories"""
        # Create static directory with files
        os.makedirs(self.static_path)
        self._create_test_file(os.path.join(self.static_path, "file1.txt"), "content1")
        self._create_test_file(os.path.join(self.static_path, "file2.txt"), "content2")
        
        # Run the function
        static_to_public(self.static_path, self.public_path)
        
        # Verify files were copied
        self.assertTrue(os.path.exists(os.path.join(self.public_path, "file1.txt")))
        self.assertTrue(os.path.exists(os.path.join(self.public_path, "file2.txt")))
        
        # Verify content is correct
        with open(os.path.join(self.public_path, "file1.txt"), 'r') as f:
            self.assertEqual(f.read(), "content1")
    
    def test_copy_nested_directories(self):
        """Test copying nested directory structures"""
        # Create nested structure
        os.makedirs(self.static_path)
        self._create_test_file(os.path.join(self.static_path, "root.txt"), "root")
        self._create_test_file(os.path.join(self.static_path, "images", "pic1.jpg"), "image1")
        self._create_test_file(os.path.join(self.static_path, "images", "pic2.jpg"), "image2")
        self._create_test_file(os.path.join(self.static_path, "docs", "nested", "deep.txt"), "deep")
        
        # Run the function
        static_to_public(self.static_path, self.public_path)
        
        # Verify structure was copied
        self.assertTrue(os.path.exists(os.path.join(self.public_path, "root.txt")))
        self.assertTrue(os.path.exists(os.path.join(self.public_path, "images", "pic1.jpg")))
        self.assertTrue(os.path.exists(os.path.join(self.public_path, "images", "pic2.jpg")))
        self.assertTrue(os.path.exists(os.path.join(self.public_path, "docs", "nested", "deep.txt")))
        
        # Verify content in nested file
        with open(os.path.join(self.public_path, "docs", "nested", "deep.txt"), 'r') as f:
            self.assertEqual(f.read(), "deep")
    
    def test_clears_existing_content(self):
        """Test that existing content in public_path is deleted"""
        # Create static directory
        os.makedirs(self.static_path)
        self._create_test_file(os.path.join(self.static_path, "new_file.txt"), "new")
        
        # Create public directory with existing content
        os.makedirs(self.public_path)
        self._create_test_file(os.path.join(self.public_path, "old_file.txt"), "old")
        os.makedirs(os.path.join(self.public_path, "old_dir"))
        self._create_test_file(os.path.join(self.public_path, "old_dir", "old.txt"), "old")
        
        # Run the function
        static_to_public(self.static_path, self.public_path)
        
        # Verify old content is gone
        self.assertFalse(os.path.exists(os.path.join(self.public_path, "old_file.txt")))
        self.assertFalse(os.path.exists(os.path.join(self.public_path, "old_dir")))
        
        # Verify new content exists
        self.assertTrue(os.path.exists(os.path.join(self.public_path, "new_file.txt")))
    
    def test_creates_public_path_if_not_exists(self):
        """Test that public_path is created if it doesn't exist"""
        # Create static directory
        os.makedirs(self.static_path)
        self._create_test_file(os.path.join(self.static_path, "file.txt"), "content")
        
        # Don't create public_path - let the function do it
        
        # Run the function
        static_to_public(self.static_path, self.public_path)
        
        # Verify public_path was created and file was copied
        self.assertTrue(os.path.exists(self.public_path))
        self.assertTrue(os.path.exists(os.path.join(self.public_path, "file.txt")))
    
    def test_raises_error_when_static_path_not_exists(self):
        """Test that FileNotFoundError is raised when static_path doesn't exist"""
        # Don't create static_path
        os.makedirs(self.public_path)
        
        # Verify error is raised
        with self.assertRaises(FileNotFoundError):
            static_to_public(self.static_path, self.public_path)
    
    def test_empty_static_directory(self):
        """Test copying from an empty static directory"""
        # Create empty static directory
        os.makedirs(self.static_path)
        
        # Run the function
        static_to_public(self.static_path, self.public_path)
        
        # Verify public_path exists but is empty
        self.assertTrue(os.path.exists(self.public_path))
        self.assertEqual(len(os.listdir(self.public_path)), 0)
    
    def test_mixed_content(self):
        """Test copying mix of files and directories at same level"""
        # Create mixed content
        os.makedirs(self.static_path)
        self._create_test_file(os.path.join(self.static_path, "file1.txt"), "file1")
        os.makedirs(os.path.join(self.static_path, "folder1"))
        self._create_test_file(os.path.join(self.static_path, "folder1", "nested.txt"), "nested")
        self._create_test_file(os.path.join(self.static_path, "file2.txt"), "file2")
        os.makedirs(os.path.join(self.static_path, "folder2"))
        
        # Run the function
        static_to_public(self.static_path, self.public_path)
        
        # Verify everything was copied
        self.assertTrue(os.path.exists(os.path.join(self.public_path, "file1.txt")))
        self.assertTrue(os.path.exists(os.path.join(self.public_path, "file2.txt")))
        self.assertTrue(os.path.exists(os.path.join(self.public_path, "folder1")))
        self.assertTrue(os.path.exists(os.path.join(self.public_path, "folder2")))
        self.assertTrue(os.path.exists(os.path.join(self.public_path, "folder1", "nested.txt")))

if __name__ == '__main__':
    unittest.main()