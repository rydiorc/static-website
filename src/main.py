from textnode import *
from htmlnode import *
from func import *
import os
import shutil

def main():
    static = "static"
    public = "public"    
    if os.path.exists(static):
        copy_dir(static, public, True)
        
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
