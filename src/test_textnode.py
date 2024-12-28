import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
  def test_eq(self):
    node = TextNode("This is a text node", TextType.BOLD)
    node2 = TextNode("This is a text node", TextType.BOLD)
    self.assertEqual(node, node2)

    node3 = TextNode("This is a text node", TextType.NORMAL, "https://boot.dev")
    self.assertNotEqual(node, node3)

    node4 = TextNode("This is a text node", TextType.CODE, "https://boot.dev")
    node5 = TextNode("This is a text node", TextType.CODE, "https://boot.dev")
    self.assertEqual(node4, node5)

  def test_repr(self):
    node = TextNode("This is a text node", TextType.BOLD)
    self.assertEqual(repr(node), "TextNode(This is a text node, bold, None)")

    node2 = TextNode("This is a text node", TextType.IMAGE, "https://boot.dev")
    self.assertEqual(repr(node2), "TextNode(This is a text node, image, https://boot.dev)")


if __name__ == "__main__":
  unittest.main()
