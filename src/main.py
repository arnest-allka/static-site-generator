import os
import re
import shutil

from block_markdown import markdown_to_html_node

def copy_directory(src, dst):
    if os.path.exists(dst):
        shutil.rmtree(dst)
    os.mkdir(dst)

    for item in os.listdir(src):
        src_path = os.path.join(src, item)
        dst_path = os.path.join(dst, item)

        if os.path.isdir(src_path):
            copy_directory(src_path, dst_path)
        else:
            shutil.copy(src_path, dst_path)
            print(f"Copied file: {src_path}")

def extract_title(markdown):
    match  = re.search(r'^#\s+(.*)', markdown, re.MULTILINE)

    if match:
        return match.group(1).strip()
    else:
        raise Exception("No h1 header found")

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    
    with open(from_path, 'r') as file:
        markdown_content = file.read()

    with open(template_path, 'r') as file:
        template_content = file.read()

    html_node = markdown_to_html_node(markdown_content)
    html_content = html_node.to_html()

    title = extract_title(markdown_content)

    full_html = template_content.replace("{{ Title }}", title).replace("{{ Content }}", html_content)

    os.makedirs(os.path.dirname(dest_path), exist_ok=True)

    with open(dest_path, 'w') as file:
        file.write(full_html)
    
    print(f"Page generated: {dest_path}")

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    if not os.path.exists(dest_dir_path):
        os.makedirs(dest_dir_path)
    
    for item in os.listdir(dir_path_content):
        src_path = os.path.join(dir_path_content, item)
        dst_path = os.path.join(dest_dir_path, item)

        if os.path.isdir(src_path):
            generate_pages_recursive(src_path, template_path, dst_path)
        elif src_path.endswith(".md"):
            dst_path = dst_path.replace(".md", ".html")
            generate_page(src_path, template_path, dst_path)


def main():
    source_dir = 'static'
    public_dir = 'public'
    
    copy_directory(source_dir, public_dir)
    print("Directory copy completed.")
    
    markdown_path = 'content'
    template_path = 'template.html'
    dest_path = 'public'

    generate_pages_recursive(markdown_path, template_path, dest_path)
  
if __name__ == '__main__':
    main()