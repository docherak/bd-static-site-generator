from enum import Enum
import re
from htmlnode import ParentNode
from inline_md import text_to_textnodes
from textnode import text_node_to_html_node

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def markdown_to_blocks(markdown):
    blocks = markdown.strip().split("\n\n")
    
    cleaned_blocks = [
        "\n".join(line.strip() for line in block.split("\n")).strip()
        for block in blocks
        if block
    ]
    
    return cleaned_blocks


def block_to_block_type(markdown_block):
    lines = markdown_block.split("\n")
    if re.match(r"^#{1,6} ", markdown_block):
        return BlockType.HEADING
    if markdown_block.startswith("```") and len(lines) > 1 and lines[-1].startswith("```"):
        return BlockType.CODE
    if markdown_block.startswith(">"):
        for line in lines:
            if not line.startswith(">"):
                return BlockType.PARAGRAPH
        return BlockType.QUOTE
    for c in ["* ", "- "]:
        if markdown_block.startswith(c):
            for line in lines:
                if not line.startswith(c):
                    return BlockType.PARAGRAPH
            return BlockType.UNORDERED_LIST
    if markdown_block.startswith("1. "):
        i = 1
        for line in lines:
            if not line.startswith(f"{i}. "):
                return BlockType.PARAGRAPH
            i += 1
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = [block_to_html_node(block) for block in blocks]
    return ParentNode("div", children, None)


def block_to_html_node(block):
    block_type = block_to_block_type(block)
    match block_type:
        case BlockType.PARAGRAPH:
            return paragraph_to_html_node(block)
        case BlockType.HEADING:
            return heading_to_html_node(block)
        case BlockType.CODE:
            return code_to_html_node(block)
        case BlockType.QUOTE:
            return quote_to_html_node(block)
        case BlockType.UNORDERED_LIST:
            return u_list_to_html_node(block)
        case BlockType.ORDERED_LIST:
            return o_list_to_html_node(block)   
    raise ValueError("invalid block type")


def get_children(text):
    text_nodes = text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)
    return children


def paragraph_to_html_node(block):
    paragraph = " ".join(block.split("\n"))
    children = get_children(paragraph)
    return ParentNode("p", children)


def heading_to_html_node(block):
    level = 0
    for char in block:
        if char == "#":
            level += 1
        else:
            break
    if level + 1 >= len(block):
        raise ValueError(f"Invalid heading level: {level}")
    text = block[level + 1 :]
    children = get_children(text)
    return ParentNode(f"h{level}", children)


def code_to_html_node(block):
    if not block.startswith("```") or not block.endswith("```"):
        raise ValueError("Invalid code block")
    text = block[4:-3]
    children = get_children(text)
    code = ParentNode("code", children)
    return ParentNode("pre", [code])


def quote_to_html_node(block):
    lines = block.split("\n")
    new_lines = []
    for line in lines:
        if not line.startswith(">"):
            raise ValueError("Invalid quote block")
        new_lines.append(line.lstrip(">").strip())
    content = " ".join(new_lines)
    children = get_children(content)
    return ParentNode("blockquote", children)


def u_list_to_html_node(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[2:]
        children = get_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ul", html_items)


def o_list_to_html_node(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[3:]
        children = get_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ol", html_items)
