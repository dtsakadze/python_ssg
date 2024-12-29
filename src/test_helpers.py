import unittest

from helpers import split_nodes_delimiter, extract_markdown_images, extract_markdown_links
from textnode import TextType, TextNode


class TestHelpers(unittest.TestCase):
  def test_split_nodes_delimiter(self):
    new_nodes = split_nodes_delimiter(
      [
        TextNode("Hello", TextType.TEXT),
        TextNode("Goodbye **world**", TextType.TEXT)
      ],
      "**",
      TextType.BOLD
    )
    self.assertEqual(new_nodes, [TextNode("Hello", TextType.TEXT), TextNode("Goodbye ", TextType.TEXT), TextNode("world", TextType.BOLD)])

    node = TextNode("This is text with a `code block` word", TextType.TEXT)
    new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
    self.assertEqual(new_nodes, [TextNode("This is text with a ", TextType.TEXT), TextNode("code block", TextType.CODE), TextNode(" word", TextType.TEXT)])

  def test_extract_markdown_images(self):
    text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
    images = extract_markdown_images(text)
    self.assertEqual(images, [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")])

  def test_extract_markdown_links(self):
    text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
    links = extract_markdown_links(text)
    self.assertEqual(links, [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")])


if __name__ == "__main__":
  unittest.main()
