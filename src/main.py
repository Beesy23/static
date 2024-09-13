import os
import shutil
from block_markdown import *
from inline_markdown import *
from gencontent import *

def main():
    src_dir = "static"
    dst_dir = "public"
    try:
        # Copies everything in static directory to public directory
        copy_dir(src_dir, dst_dir)
        print("Static files copied sucessfully")
    except Exception as e:
        print(f"Error occurred copying static files: {str(e)}")

    try:
        # Generates .html files in public directory for all .md files in content directory 
        generate_page_recursive("content", "template.html", "public")
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
