import unittest

from textnode import TextNode, TextType
from htmlnode import HTMLNode


class TestTextNode(unittest.TestCase):
  def test_eq(self):
    node = TextNode("This is a text node", TextType.BOLD)
    node2 = TextNode("This is a text node", TextType.BOLD)
    self.assertEqual(node, node2)

    node3 = TextNode("This is a text node", TextType.TEXT, "https://boot.dev")
    self.assertNotEqual(node, node3)

    node4 = TextNode("This is a text node", TextType.CODE, "https://boot.dev")
    node5 = TextNode("This is a text node", TextType.CODE, "https://boot.dev")
    self.assertEqual(node4, node5)

  def test_repr(self):
    node = TextNode("This is a text node", TextType.BOLD)
    self.assertEqual(repr(node), "TextNode(This is a text node, bold, None)")

    node2 = TextNode("This is a text node", TextType.IMAGE, "https://boot.dev")
    self.assertEqual(repr(node2), "TextNode(This is a text node, image, https://boot.dev)")

  def test_text_node_to_html_node(self):
    with self.assertRaises(ValueError):
      TextNode("Hello", "other type")

    text_node = TextNode("Hello", TextType.TEXT)
    self.assertEqual(text_node.text_node_to_html_node().to_html(), "Hello")

    bold_node = TextNode("Hello", TextType.BOLD)
    self.assertEqual(bold_node.text_node_to_html_node().to_html(), "<b>Hello</b>")

    italic_node = TextNode("Hello", TextType.ITALIC)
    self.assertEqual(italic_node.text_node_to_html_node().to_html(), "<i>Hello</i>")

    code_node = TextNode("Hello", TextType.CODE)
    self.assertEqual(code_node.text_node_to_html_node().to_html(), "<code>Hello</code>")

    link_node = TextNode("Hello", TextType.LINK, "https://boot.dev")
    self.assertEqual(link_node.text_node_to_html_node().to_html(), '<a href="https://boot.dev">Hello</a>')

    image_node = TextNode("Hello", TextType.IMAGE, "https://boot.dev")
    self.assertEqual(image_node.text_node_to_html_node().to_html(), '<img src="https://boot.dev" alt="Hello"></img>')


if __name__ == "__main__":
  unittest.main()
