from textnode import TextType, TextNode
import re
from parentnode import ParentNode
from textnode import text_node_to_html_node

block_type_paragraph = "paragraph"
block_type_heading = "heading"
block_type_code = "code"
block_type_quote = "quote"
block_type_olist = "ordered_list"
block_type_ulist = "unordered_list"

def split_nodes_delimiter(old_nodes, delimiter, text_type):
  new_nodes = []
  for node in old_nodes:
    if node.text_type != TextType.TEXT:
      new_nodes.append(node)
      continue
    
    delimeters_count = node.text.count(delimiter)
    if delimeters_count > 0 and delimeters_count != 2:
      raise Exception("Closing delimiter not found")
    
    split_text_list = node.text.split(delimiter)
    split_text_list = list(filter(lambda item: item != "", split_text_list))

    for i, text in enumerate(split_text_list):
      if i == 1:
        new_nodes.append(TextNode(text, text_type))
      else:
        new_nodes.append(TextNode(text, TextType.TEXT))

  return new_nodes

def extract_markdown_images(text):
  return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text):
  return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def split_nodes_image(old_nodes):
  new_nodes = []
  for old_node in old_nodes:
    if old_node.text_type != TextType.TEXT:
      new_nodes.append(old_node)
      continue

    original_text = old_node.text
    images = extract_markdown_images(original_text)

    if len(images) == 0:
      new_nodes.append(old_node)
      continue

    for image in images:
      sections = original_text.split(f"![{image[0]}]({image[1]})", 1)

      if len(sections) != 2:
        raise ValueError("Invalid markdown, image section not closed")

      if sections[0] != "":
        new_nodes.append(TextNode(sections[0], TextType.TEXT))

      new_nodes.append(
        TextNode(
          image[0],
          TextType.IMAGE,
          image[1],
        )
      )
      original_text = sections[1]

    if original_text != "":
      new_nodes.append(TextNode(original_text, TextType.TEXT))

  return new_nodes

def split_nodes_link(old_nodes):
  new_nodes = []
  for old_node in old_nodes:
    if old_node.text_type != TextType.TEXT:
      new_nodes.append(old_node)
      continue

    original_text = old_node.text
    links = extract_markdown_links(original_text)

    if len(links) == 0:
      new_nodes.append(old_node)
      continue

    for link in links:
      sections = original_text.split(f"[{link[0]}]({link[1]})", 1)

      if len(sections) != 2:
        raise ValueError("Invalid markdown, link section not closed")

      if sections[0] != "":
        new_nodes.append(TextNode(sections[0], TextType.TEXT))

      new_nodes.append(TextNode(link[0], TextType.LINK, link[1]))
      original_text = sections[1]

    if original_text != "":
      new_nodes.append(TextNode(original_text, TextType.TEXT))

  return new_nodes

def text_to_textnodes(text):
  nodes = [TextNode(text, TextType.TEXT)]
  nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
  nodes = split_nodes_delimiter(nodes, "*", TextType.ITALIC)
  nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
  nodes = split_nodes_image(nodes)
  nodes = split_nodes_link(nodes)
  return nodes

def markdown_to_blocks(markdown):
  blocks = markdown.split("\n\n")
  filtered_blocks = []
  for block in blocks:
    if block == "":
      continue

    filtered_blocks.append(block.strip())

  return filtered_blocks

def block_to_block_type(block):
  lines = block.split("\n")

  if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
    return block_type_heading

  if len(lines) > 1 and lines[0].startswith("```") and lines[-1].startswith("```"):
    return block_type_code

  if block.startswith(">"):
    for line in lines:
      if not line.startswith(">"):
        return block_type_paragraph
    return block_type_quote

  if block.startswith("* "):
    for line in lines:
      if not line.startswith("* "):
        return block_type_paragraph
    return block_type_ulist

  if block.startswith("- "):
    for line in lines:
      if not line.startswith("- "):
        return block_type_paragraph
    return block_type_ulist

  if block.startswith("1. "):
    i = 1
    for line in lines:
      if not line.startswith(f"{i}. "):
        return block_type_paragraph
      i += 1
    return block_type_olist

  return block_type_paragraph

def markdown_to_html_node(markdown):
  blocks = markdown_to_blocks(markdown)
  children = []
  for block in blocks:
    html_node = block_to_html_node(block)
    children.append(html_node)
  return ParentNode("div", children, None)


def block_to_html_node(block):
  block_type = block_to_block_type(block)
  if block_type == block_type_paragraph:
    return paragraph_to_html_node(block)
  if block_type == block_type_heading:
    return heading_to_html_node(block)
  if block_type == block_type_code:
    return code_to_html_node(block)
  if block_type == block_type_olist:
    return olist_to_html_node(block)
  if block_type == block_type_ulist:
    return ulist_to_html_node(block)
  if block_type == block_type_quote:
    return quote_to_html_node(block)
  raise ValueError("Invalid block type")


def text_to_children(text):
  text_nodes = text_to_textnodes(text)
  children = []
  for text_node in text_nodes:
    html_node = text_node_to_html_node(text_node)
    children.append(html_node)
  return children


def paragraph_to_html_node(block):
  lines = block.split("\n")
  paragraph = " ".join(lines)
  children = text_to_children(paragraph)
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
  children = text_to_children(text)
  return ParentNode(f"h{level}", children)


def code_to_html_node(block):
  if not block.startswith("```") or not block.endswith("```"):
    raise ValueError("Invalid code block")
  text = block[4:-3]
  children = text_to_children(text)
  code = ParentNode("code", children)
  return ParentNode("pre", [code])


def olist_to_html_node(block):
  items = block.split("\n")
  html_items = []
  for item in items:
    text = item[3:]
    children = text_to_children(text)
    html_items.append(ParentNode("li", children))
  return ParentNode("ol", html_items)


def ulist_to_html_node(block):
  items = block.split("\n")
  html_items = []
  for item in items:
    text = item[2:]
    children = text_to_children(text)
    html_items.append(ParentNode("li", children))
  return ParentNode("ul", html_items)


def quote_to_html_node(block):
  lines = block.split("\n")
  new_lines = []
  for line in lines:
    if not line.startswith(">"):
      raise ValueError("Invalid quote block")
    new_lines.append(line.lstrip(">").strip())
  content = " ".join(new_lines)
  children = text_to_children(content)
  return ParentNode("blockquote", children)
