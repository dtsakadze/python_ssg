import unittest

from helpers import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link
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

  def test_split_nodes_image(self):
    node = TextNode(
      "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)",
      TextType.TEXT,
    )
    new_nodes = split_nodes_image([node])
    self.assertEqual(
      new_nodes,
      [
        TextNode("This is text with a ", TextType.TEXT),
        TextNode("rick roll", TextType.IMAGE, "https://i.imgur.com/aKaOqIh.gif"),
        TextNode(" and ", TextType.TEXT),
        TextNode("obi wan", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
      ],
    )

  def test_split_nodes_link(self):
    node = TextNode(
      "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
      TextType.TEXT,
    )
    new_nodes = split_nodes_link([node])
    self.assertEqual(
      new_nodes,
      [
        TextNode("This is text with a link ", TextType.TEXT),
        TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
        TextNode(" and ", TextType.TEXT),
        TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"),
      ],
    )


if __name__ == "__main__":
  unittest.main()
