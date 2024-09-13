import os
from block_markdown import markdown_to_html_node

def extract_title(markdown):
    lines = markdown.split("\n")
    for line in lines:
        if line[:2] == "# ":
            return line.lstrip("#").strip()
    raise Exception("No h1 header found")

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    # Store from_path file to a variable
    with open(from_path) as content_file:
        contents_from = content_file.read()
    # Store template_path file to a variable
    with open(template_path) as template_file:
        contents_template = template_file.read()
    # Extract title from contents
    title = extract_title(contents_from)
    # Convert contents to html string
    html_string = markdown_to_html_node(contents_from).to_html()
    # Replace title and content placeholders in template with actual title and placeholders
    contents_template = contents_template.replace("{{ Title }}", title).replace("{{ Content }}", html_string)
    # Creates dest_path directory if it does not already exist
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    # Write template to a new file
    with open(dest_path,"w") as html_file:
        html_file.write(contents_template)

def generate_page_recursive(dir_path_content, template_path, dest_dir_path):
    print(f"Generating pages from {dir_path_content} to {dest_dir_path} using {template_path}")
    if not os.path.exists(dir_path_content): 
        raise FileNotFoundError(f"Error: Source directory '{dir_path_content}' does not exist")
    # Iterates over files in dir_path_content directory
    for file_path in os.listdir(dir_path_content):
            try:
                # Create source file path and destination file path
                src_file_path = os.path.join(dir_path_content, file_path)
                dst_file_path = os.path.join(dest_dir_path, file_path)
                # Checks if file path is a file that ends in .md (markdown file)
                if os.path.isfile(src_file_path) and src_file_path.endswith(".md"):
                    # Replaces .md extension with .html
                    dst_file_path = dst_file_path.replace(".md",".html")
                    # Generates html file
                    generate_page(src_file_path, template_path, dst_file_path)
                    print(f"Page from {src_file_path} generated to {dst_file_path}")
                # Checks if file path is a directory
                elif os.path.isdir(src_file_path):
                    # Creates directory in destination directory if it doesn't already exist
                    os.makedirs(dst_file_path, exist_ok=True)
                    # Recursive to crawl over files in directory and generate .html files for them
                    generate_page_recursive(src_file_path, template_path, dst_file_path)
                    print(f"Directory {src_file_path} generated to {dst_file_path}")
                # Deals with other file types
                else:
                    print(f"{file_path} is not a markdown file or directory")
                    continue

            except Exception as e:
                print(f"Error: {str(e)}")