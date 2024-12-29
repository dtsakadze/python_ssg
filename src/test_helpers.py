import unittest

from helpers import split_nodes_delimiter
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


if __name__ == "__main__":
  unittest.main()
