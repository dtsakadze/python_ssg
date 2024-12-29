from textnode import TextType, TextNode

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
