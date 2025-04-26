import os
import shutil
import sys
from block_markdown import *
from inline_markdown import *
from gencontent import *

script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)

static_path = os.path.join(project_root, "static")
doc_path = os.path.join(project_root, "docs")
content_path = os.path.join(project_root, "content")
template_path = os.path.join(project_root, "template.html")

def main():

    base_path = "/"
    if len(sys.argv) > 1:
        base_path = str(sys.argv[1])

    try:
        # Copies everything in static directory to public directory
        copy_dir(static_path, doc_path)
        print("Static files copied sucessfully")
    except Exception as e:
        print(f"Error occurred copying static files: {str(e)}")
    
    #generate_page(os.path.join(content_path, "index.md"), template_path, os.path.join(public_path,"index.html"))

    try:
        # Generates .html files in public directory for all .md files in content directory 
        generate_page_recursive(content_path, template_path, doc_path, base_path)
        print("Function: generate_page_recursive executed")
    except Exception as e:
        print(f"Error occured generating pages: {str(e)}")

def copy_dir(src, dst):
    try:
        # Checks is destination directory already exists
        if os.path.exists(dst):
            # Deletes destination directory for clean copy
            shutil.rmtree(dst)
        # Creates new destination directory
        os.mkdir(dst)  
        # Checks if source directory exists and raise an error if not
        if not os.path.exists(src): 
            raise FileNotFoundError(f"Error: Source directory '{src}' does not exist")
        # Iterates over file in source directory
        for item in os.listdir(src):
            # Assigns file paths for files in source directory and destination directory
            s = os.path.join(src, item)
            d = os.path.join(dst, item)
            try:
                # Checks if source directory file path is a file
                if os.path.isfile(s):
                    # Copies file in source directory to destination directory
                    shutil.copy(s, d)
                    print(f"Copied file {s} to {d}")
                else:
                    # Creates source directory in destination directory
                    print(f"Creating directory {d}")
                    copy_dir(s,d)
            except Exception as e:
                print(f"Error processing {s}: {str(e)}")
    except Exception as e:
        print(f"Error: {str(e)}")


main()
