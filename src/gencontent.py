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
    with open(from_path) as content_file:
        contents_from = content_file.read()
    with open(template_path) as template_file:
        contents_template = template_file.read()
    title = extract_title(contents_from)
    html_string = markdown_to_html_node(contents_from).to_html()
    contents_template = contents_template.replace("{{ Title }}", title).replace("{{ Content }}", html_string)
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path,"w") as html_file:
        html_file.write(contents_template)

def generate_page_recursive(dir_path_content, template_path, dest_dir_path):
    print(f"Generating pages from {dir_path_content} to {dest_dir_path} using {template_path}")
    if not os.path.exists(dir_path_content): 
        raise FileNotFoundError(f"Error: Source directory '{dir_path_content}' does not exist")
    for file_path in os.listdir(dir_path_content):
            if file_path != "":
                try:
                    src_file_path = os.path.join(dir_path_content, file_path)
                    dst_file_path = os.path.join(dest_dir_path, file_path)
                    if os.path.isfile(src_file_path) and src_file_path.endswith(".md"):
                        dst_file_path = dst_file_path.replace(".md",".html")
                        generate_page(src_file_path, template_path, dst_file_path)
                        print(f"Page from {src_file_path} generated to {dst_file_path}")
                    elif os.path.isdir(src_file_path):
                        os.makedirs(dst_file_path, exist_ok=True)
                        generate_page_recursive(src_file_path, template_path, dst_file_path)
                        print(f"Directory {src_file_path} generated to {dst_file_path}")
                    else:
                        print(f"{file_path} is not a markdown file or directory")
                        continue

                except Exception as e:
                    print(f"Error: {str(e)}")