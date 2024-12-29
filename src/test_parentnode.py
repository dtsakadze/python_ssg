import unittest

from parentnode import ParentNode
from leafnode import LeafNode


class TestParentNode(unittest.TestCase):
  def test_to_html(self):
    parent_node = ParentNode(None, "Hello, World!")
    with self.assertRaises(ValueError):
      parent_node.to_html()

    parent_node = ParentNode("a", None)
    with self.assertRaises(ValueError):
      parent_node.to_html()

    parent_node = ParentNode(
      "p",
      [
        LeafNode("b", "Bold text"),
        LeafNode(None, "Normal text"),
        LeafNode("i", "italic text"),
        LeafNode(None, "Normal text"),
      ]
    )
    self.assertEqual(parent_node.to_html(), "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>")

    parent_node = ParentNode(
      "div",
      [
        LeafNode("p", "Bold text", { "class": "text-center" }),
        ParentNode(
          "div",
          [
            LeafNode("p", "Helloooo", { "class": "flex" }),
            LeafNode("span", "Bye!")
          ]
        )
      ]
    )
    self.assertEqual(parent_node.to_html(), "<div><p class=\"text-center\">Bold text</p><div><p class=\"flex\">Helloooo</p><span>Bye!</span></div></div>")


if __name__ == "__main__":
  unittest.main()
