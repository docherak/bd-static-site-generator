import re

from textnode import TextNode, TextType


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.NORMAL:
            new_nodes.append(old_node)
            continue
        parts = old_node.text.split(delimiter)
        if len(parts) % 2 == 0:
            raise ValueError("invalid markdown")
        for i in range(len(parts)):
            if parts[i] == "":
                continue
            if i % 2 == 0:
                new_nodes.append(TextNode(parts[i], TextType.NORMAL))
            else:
                new_nodes.append(TextNode(parts[i], text_type))
    return new_nodes


def extract_markdown_images(text):
    return re.findall(r"!\[(.*?)\]\((.*?)\)", text)


def extract_markdown_links(text):
    return re.findall(r"\[(.*?)\]\((.*?)\)", text)


def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.NORMAL:
            new_nodes.append(old_node)
            continue
        original_text = old_node.text
        images = extract_markdown_images(original_text)
        for alt, link in images:
            parts = original_text.split(f"![{alt}]({link})", 1)
            if len(parts) != 2:
                raise ValueError("invalid markdown")
            if parts[0] != "":
                new_nodes.append(TextNode(parts[0], TextType.NORMAL))
            new_nodes.append(TextNode(alt, TextType.IMAGE, link))
            original_text = parts[1]
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.NORMAL))
    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.NORMAL:
            new_nodes.append(old_node)
            continue
        original_text = old_node.text
        links = extract_markdown_links(original_text)
        for alt, link in links:
            parts = original_text.split(f"[{alt}]({link})", 1)
            if len(parts) != 2:
                raise ValueError("invalid markdown")
            if parts[0] != "":
                new_nodes.append(TextNode(parts[0], TextType.NORMAL))
            new_nodes.append(TextNode(alt, TextType.LINK, link))
            original_text = parts[1]
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.NORMAL))
    return new_nodes


def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.NORMAL)]
    for c in [("**", TextType.BOLD), ("*", TextType.ITALIC), ("`", TextType.CODE)]:
        nodes = split_nodes_delimiter(nodes, c[0], c[1])
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes
