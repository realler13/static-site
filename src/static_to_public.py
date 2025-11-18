import os
import shutil
import logging

logging.basicConfig(
    level=logging.INFO, 
    format='%(levelname)s: %(message)s'
)

def static_to_public(static_path, public_path):
    
    if os.path.exists(public_path):
        contents = os.listdir(public_path)
        if len(contents) != 0:
            for item in contents:
                item_path = os.path.join(public_path, item)
                if os.path.isfile(item_path):
                    try:
                        os.remove(item_path)
                        logging.info(f"Deleted file: {item_path}")
                    except PermissionError as e:
                        logging.error(f"Permission denied: {e}")
                elif os.path.isdir(item_path):
                    try:
                        shutil.rmtree(item_path)
                        logging.info(f"Deleted directory: {item_path}")
                    except PermissionError as e:
                        logging.error(f"Permission denied: {e}")
    else:
        os.makedirs(public_path, exist_ok=True)
    
    if not os.path.exists(static_path):
        raise FileNotFoundError(f"Source directory not found: {static_path}")

    static_content = os.listdir(static_path)
    for item in static_content:
        item_path = os.path.join(static_path, item)
        if os.path.isfile(item_path):
            shutil.copy(item_path, public_path)
            logging.info(f"Copied file: {item_path} to {public_path}")
        elif os.path.isdir(item_path):
            destination_dir = os.path.join(public_path, item)
            os.makedirs(destination_dir)
            logging.info(f"Created directory: {destination_dir}")
            static_to_public(item_path, destination_dir)



def extract_title(md):
    lines = md.split("\n")
    for line in lines:
        if line.startswith("# "):
            return line[2:]
    raise ValueError("no title found")


