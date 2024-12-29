import unittest

from leafnode import LeafNode


class TestLeafNode(unittest.TestCase):
  def test_to_html(self):
    leaf_node = LeafNode("a", "Hello, World!", {"href": "https://boot.dev"})
    self.assertEqual(leaf_node.to_html(), '<a href="https://boot.dev">Hello, World!</a>')

    leaf_node = LeafNode(None, "Hello, World!", None)
    self.assertEqual(leaf_node.to_html(), "Hello, World!")

    leaf_node = LeafNode("a", None, None)
    with self.assertRaises(ValueError):
      leaf_node.to_html()


if __name__ == "__main__":
  unittest.main()
