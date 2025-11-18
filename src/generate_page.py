import os
import logging
from pathlib import Path


from block_markdown import markdown_to_html_node

logging.basicConfig(
    level=logging.INFO, 
    format='%(levelname)s: %(message)s'
)

def generate_page(from_path, template_path, dest_path, basepath="/"):
    logging.info(f"Generating page from {from_path} to {dest_path} using {template_path}")
    
    # Read the markdown file
    with open(from_path, 'r') as source:
        content = source.read()
    
    # Read the template
    with open(template_path, 'r') as template_file:
        template = template_file.read()
    
    # Convert markdown to HTML
    htmlstring = markdown_to_html_node(content).to_html()
    title = extract_title(content)
    
    # Replace placeholders in template
    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", htmlstring)
    
    # Replace paths with basepath
    template = template.replace('href="/', f'href="{basepath}')
    template = template.replace('src="/', f'src="{basepath}')
    
    # Create destination directory and write file
    dest_dir = os.path.dirname(dest_path)
    if dest_dir:
        os.makedirs(dest_dir, exist_ok=True)
    
    with open(dest_path, "w") as file:
        file.write(template)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath="/"):
    for filename in os.listdir(dir_path_content):
        from_path = os.path.join(dir_path_content, filename)
        dest_path = os.path.join(dest_dir_path, filename)
        
        if os.path.isfile(from_path):
            # Only process .md files
            if not from_path.endswith('.md'):
                logging.info(f"Skipping non-markdown file: {from_path}")
                continue
            
            # Change .md extension to .html
            dest_path = Path(dest_path).with_suffix(".html")
            generate_page(from_path, template_path, dest_path, basepath)
        else:
            # Recursively process subdirectories
            generate_pages_recursive(from_path, template_path, dest_path, basepath)



def extract_title(md):
    lines = md.split("\n")
    for line in lines:
        if line.startswith("# "):
            return line[2:]
    raise ValueError("no title found")



