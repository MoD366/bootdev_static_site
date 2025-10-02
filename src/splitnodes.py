from textnode import TextType, TextNode
from regextractor import extract_markdown_images, extract_markdown_links

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if delimiter not in node.text:
            new_nodes.append(node)
            continue
        parts = node.text.split(delimiter, maxsplit=2)
        new_nodes.append(TextNode(parts[0], TextType.TEXT))
        new_nodes.append(TextNode(parts[1], text_type))
        new_nodes += split_nodes_delimiter([TextNode(parts[2], TextType.TEXT)], delimiter, text_type)
    return new_nodes
    
def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        images = extract_markdown_images(node.text)
        if len(images) == 0:
            new_nodes.append(node)
            continue
        image_pos_end = -1
        for image in images:
            image_pos_start = image_pos_end + 1 + node.text[image_pos_end+1:].find("!["+image[0])
            if image_pos_start > 0:
                new_nodes.append(TextNode(node.text[image_pos_end+1:image_pos_start], TextType.TEXT))
            new_nodes.append(TextNode(image[0], TextType.IMAGE, image[1]))
            image_pos_end = image_pos_start+len(image[0])+4 + node.text[image_pos_start+len(image[0])+4:].find(")")
        if image_pos_end+1 != len(node.text):
            new_nodes.append(TextNode(node.text[image_pos_end+1:], TextType.TEXT))
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        links = extract_markdown_links(node.text)
        if len(links) == 0:
            new_nodes.append(node)
            continue
        link_pos_end = -1
        for link in links:
            link_pos_start = link_pos_end + 1 + node.text[link_pos_end+1:].find("["+link[0])
            if link_pos_start > 0:
                new_nodes.append(TextNode(node.text[link_pos_end+1:link_pos_start], TextType.TEXT))
            new_nodes.append(TextNode(link[0], TextType.LINK, link[1]))
            link_pos_end = link_pos_start+len(link[0])+3 + node.text[link_pos_start+len(link[0])+3:].find(")")
        if link_pos_end+1 != len(node.text):
            new_nodes.append(TextNode(node.text[link_pos_end+1:], TextType.TEXT))
    return new_nodes

def text_to_textnode(text):
    stripped_text = " ".join(text.split("\n"))
    new_nodes = split_nodes_delimiter([TextNode(stripped_text.strip(), TextType.TEXT)], "**", TextType.BOLD)
    new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALICS)
    new_nodes = split_nodes_delimiter(new_nodes, "`", TextType.CODE)
    new_nodes = split_nodes_image(new_nodes)
    new_nodes = split_nodes_link(new_nodes)
    return new_nodes