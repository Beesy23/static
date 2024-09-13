import os
import shutil
from block_markdown import *
from inline_markdown import *
from gencontent import *

def main():
    src_dir = "static"
    dst_dir = "public"
    try:
        copy_static(src_dir, dst_dir)
        print("Static files copied sucessfully")
    except Exception as e:
        print(f"Error occurred copying static files: {str(e)}")

    try:
        generate_page_recursive("content", "template.html", "public")
        print("Function: generate_page_recursive completed")
    except Exception as e:
        print(f"Error occured generating pages: {str(e)}")

def copy_static(src, dst):
    try:
        if os.path.exists(dst):
            shutil.rmtree(dst)
        os.mkdir(dst)  
        if not os.path.exists(src): 
            raise FileNotFoundError(f"Error: Source directory '{src}' does not exist")
        
        for item in os.listdir(src):
            s = os.path.join(src, item)
            d = os.path.join(dst, item)
            try:
                if os.path.isfile(s):
                    shutil.copy(s, d)
                    print(f"Copied file {s} to {d}")
                else:
                    print(f"Creating diectory {d}")
                    copy_static(s,d)
            except Exception as e:
                print(f"Error processing {s}: {str(e)}")
    except Exception as e:
        print(f"Error: {str(e)}")


main()
