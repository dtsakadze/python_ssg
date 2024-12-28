import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
  def test_props_to_html(self):
    html_node = HTMLNode("a", "Hello, World!", props={"href": "https://boot.dev"})
    self.assertEqual(html_node.props_to_html(), ' href="https://boot.dev"')

    html_node2 = HTMLNode("a", "Hello, World!")
    self.assertEqual(html_node2.props_to_html(), "")

    html_node3 = HTMLNode("a", "Hello, World!", props={"href": "https://boot.dev", "target": "_blank"})
    self.assertEqual(html_node3.props_to_html(), ' href="https://boot.dev" target="_blank"')


if __name__ == "__main__":
  unittest.main()
