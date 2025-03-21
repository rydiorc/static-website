from textnode import *
from htmlnode import *
from func import *
import os
import shutil
import re

def main():
    static = "static"
    public = "public"
    if os.path.exists(static):
        copy_dir(static, public, True)
    generate_page(os.path.join("content", "index.md"), "template.html", os.path.join("public", "index.html"))

def generate_page(from_path, template_path, dest_path):
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
