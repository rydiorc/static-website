from textnode import *
from htmlnode import *
from func import *
import os
import shutil
import re
import sys

def main():
    basepath = "/"
    if len(sys.argv) > 1:
        basepath = sys.argv[1]
    static = "static"
    public = "docs"
    content = "content"
    if os.path.exists(static):
        copy_dir(static, public, True)
    #generate_page(os.path.join("content", "index.md"), "template.html", os.path.join("docs", "index.html"))
    generate_pages_recursive(content, "template.html", public, basepath)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    if os.path.exists(dir_path_content):
        files = os.listdir(dir_path_content)
        for f in files:
            src = os.path.join(dir_path_content, f)
            dst = os.path.join(dest_dir_path, f)
            if os.path.isfile(src):
                if src.endswith(".md"):
                    dst = dst.replace(".md", ".html")
                    generate_page(src, template_path, dst, basepath)
            if os.path.isdir(src):
                generate_pages_recursive(src, template_path, dst, basepath)
    

def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    md = None
    template = None
    with open(from_path) as f:
        md = f.read()
    with open(template_path) as t:
        template = t.read()
    node = markdown_to_html_node(md)
    html = node.to_html()
    title = extract_title(md)
    #print(title)
    template = template.replace("{{ Title }}", title)
    final_html = template.replace("{{ Content }}", html)
    final_html = final_html.replace('href="/', f"href=\"{basepath}")
    final_html = final_html.replace('src="/', f"src=\"{basepath}")
    #print(final_html)
    # Get the directory portion of the path
    dest_dir = os.path.dirname(dest_path)
    # Create the directory if it doesn't exist
    if dest_dir:  # Check if there's a directory part (not just a filename)
        os.makedirs(dest_dir, exist_ok=True)
    with open(dest_path, "w") as file:
        #print("Final Opened")
        file.write(final_html)



def copy_dir(dir, destination, is_top_level=False):
    if is_top_level and os.path.exists(destination):
        print(f"removing {destination}")
        shutil.rmtree(destination)
        print(f"recreating {destination}")
        os.mkdir(destination)
    elif not os.path.exists(destination):
        print(f"creating {destination}")
        os.mkdir(destination)

    if os.path.exists(dir):
        files = os.listdir(dir)
        for f in files:
            src = os.path.join(dir, f)
            dst = os.path.join(destination, f)
            if os.path.isfile(src):
                # Copy file
                print(f"Copying {src} to {dst}")
                shutil.copy(src, dst)
            if os.path.isdir(src):
                copy_dir(src, dst)

main()
