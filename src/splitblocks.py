import re

from textnode import BlockType, TextNode, TextType
from htmlnode import HTMLNode, LeafNode, ParentNode, text_node_to_html_node, text_to_children
from helper import choose_heading_level

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    filtered = []
    for block in blocks:
        block = block.strip()
        if block == "":
            continue
        filtered.append(block)
    return filtered

def block_to_blocktype(block):
    if len(re.findall(r"^#{1,6} .*", block)) > 0:
        return BlockType.HEADING
    if len(re.findall( r"^```[\s\S]*```$",block)) > 0:
        return BlockType.CODE
    if len(re.findall(r"^(>.+\n{0,1})+(>.+){0,1}",block)) > 0:
        return BlockType.QUOTE
    if len(re.findall(r"^(- .+\n{0,1})+(- .+){0,1}", block)) > 0:
        return BlockType.UNORDERED
    if block[0] == "1":
        islist = True
        lines = block.split("\n")
        for i in range(len(lines)):
            if lines[i][0] != str(i+1) or len(re.findall(r"^\d+\. .*", lines[i])) == 0:
                islist = False
                break
        if islist:
            return BlockType.ORDERED
    return BlockType.PARAGRAPH

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    all_nodes = []
    for block in blocks:
        blocktype = block_to_blocktype(block)
        match blocktype:
            case BlockType.PARAGRAPH:
                node = ParentNode("p", text_to_children(block))
            case BlockType.HEADING:
                node = LeafNode(choose_heading_level(block), block.split(" ", 1)[1])
            case BlockType.QUOTE:
                lines = block.split("\n")
                text = ""
                for line in lines:
                    text += line[1:]
                node = ParentNode("blockquote", text_to_children(text))
            case BlockType.CODE:
                node = ParentNode("pre", [text_node_to_html_node(TextNode(block[3:-3], TextType.CODE))])
            case BlockType.UNORDERED:
                children = []
                lines = block.split("\n")
                for line in lines:
                    text = line[2:]
                    children.append(ParentNode("li", text_to_children(text)))
                node = ParentNode("ul", children)
            case BlockType.ORDERED:
                children = []
                lines = block.split("\n")
                for line in lines:
                    text = line.split(". ", 1)
                    children.append(ParentNode("li", text_to_children(text[1])))
                node = ParentNode("ol", children)
        all_nodes.append(node)
    return ParentNode("div", all_nodes)
