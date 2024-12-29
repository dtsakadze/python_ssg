from textnode import TextType, TextNode
import re

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
