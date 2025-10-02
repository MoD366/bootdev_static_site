from textnode import *
from splitblocks import markdown_to_html_node
from helper import extract_title
import os
import shutil
import sys

def main():
    if len(sys.argv) == 1:
        basepath = "/"
    else:
        basepath = sys.argv[1]
    copy_files("static", "docs")
    generate_page_recursive("content", "template.html", "docs", basepath)

def copy_files(source, target):
    #print(f"Reading from {source} to copy to {target}")
    if not os.path.exists(source):
        raise Exception("Source directory does not exist.")
    if os.path.exists(target):
        shutil.rmtree(target)
    os.mkdir(target)

    content = os.listdir(source)
    for entry in content:
        entry_source = os.path.join(source, entry)
        entry_target = os.path.join(target, entry)
        if os.path.isdir(entry_source):
            copy_files(entry_source,entry_target)
        elif os.path.isfile(entry_source):
            shutil.copy(entry_source, entry_target)

def generate_page(source, template, destination, basepath):
    print(f"Generating page from {source} to {destination} using {template}")

    mdfile = open(source)
    markdown = mdfile.read()
    mdfile.close()
    tfile = open(template)
    temp = tfile.read()
    tfile.close()
    html = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)
    temp = temp.replace("{{ Title }}", title).replace("{{ Content }}", html)
    temp = temp.replace('href="/', f'href="{basepath}').replace('src="/', f'src="{basepath}')
    htmlfile = open(destination, "w")
    htmlfile.write(temp)

def generate_page_recursive(source_path, template, destination_path, basepath):
    for entry in os.listdir(source_path):
        entry_source = os.path.join(source_path, entry)
        entry_dest = os.path.join(destination_path, entry)
        if os.path.isdir(entry_source):
            if not os.path.exists(entry_dest):
                os.mkdir(entry_dest)
            generate_page_recursive(entry_source, template, entry_dest, basepath)
        elif os.path.isfile(entry_source):
            generate_page(entry_source, template, entry_dest[:-3]+".html", basepath)

main()