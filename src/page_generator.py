from block_md import markdown_to_html_node
import os


def extract_markdown_title(markdown):
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("# "):
            return line[2:]
    raise ValueError("h1 header not found")


def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path, "r") as markdown_file:
        markdown_content = markdown_file.read()
        markdown_title = extract_markdown_title(markdown_content)
        html_content = markdown_to_html_node(markdown_content).to_html()

    with open(template_path, "r") as template_file:
        template_content = template_file.read()

    page_content = template_content.replace("{{ Title }}", markdown_title).replace(
        "{{ Content }}", html_content
    )

    dest_dir_path = os.path.dirname(dest_path)
    if dest_dir_path != "":
        os.makedirs(os.path.dirname(dest_path), exist_ok=True)

    with open(dest_path, "w") as html_file:
        html_file.write(page_content)


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    for filename in os.listdir(dir_path_content):
        content_path = os.path.join(dir_path_content, filename)
        dest_path = os.path.join(dest_dir_path, filename)
        if os.path.isfile(content_path) and os.path.splitext(content_path)[-1] == ".md":
            generate_page(
                content_path, template_path, dest_path.replace(".md", ".html")
            )
        else:
            generate_pages_recursive(content_path, template_path, dest_path)
