from textnode import TextType, TextNode
import re

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
