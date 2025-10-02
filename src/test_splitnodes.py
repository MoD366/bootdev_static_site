import unittest

from textnode import TextNode, TextType
from splitnodes import split_nodes_delimiter, split_nodes_image, split_nodes_link, text_to_textnode

class TestNodeSplitting(unittest.TestCase):
    def test_bold(self):
        node = TextNode("This text has **bold words** contained within.", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node],"**",TextType.BOLD)
        self.assertEqual(new_nodes[0], TextNode("This text has ", TextType.TEXT))
        self.assertEqual(new_nodes[1], TextNode("bold words", TextType.BOLD))
        self.assertEqual(new_nodes[2], TextNode(" contained within.", TextType.TEXT))

    def test_double_bold(self):
        node = TextNode("This **text** has **bold words** contained within.", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node],"**",TextType.BOLD)
        self.assertEqual(new_nodes[0], TextNode("This ", TextType.TEXT))
        self.assertEqual(new_nodes[1], TextNode("text", TextType.BOLD))
        self.assertEqual(new_nodes[2], TextNode(" has ", TextType.TEXT))
        self.assertEqual(new_nodes[3], TextNode("bold words", TextType.BOLD))
        self.assertEqual(new_nodes[4], TextNode(" contained within.", TextType.TEXT))

    def test_italics(self):
        node = TextNode("This text has _italicized words_ contained within.", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node],"_",TextType.ITALICS)
        self.assertEqual(new_nodes[0], TextNode("This text has ", TextType.TEXT))
        self.assertEqual(new_nodes[1], TextNode("italicized words", TextType.ITALICS))
        self.assertEqual(new_nodes[2], TextNode(" contained within.", TextType.TEXT))

    def test_bold_italics(self):
        node = TextNode("This text has **bold** and _italicized_ words contained within.", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node],"**",TextType.BOLD)
        newer_nodes = split_nodes_delimiter(new_nodes,"_",TextType.ITALICS)
        self.assertEqual(newer_nodes[0], TextNode("This text has ", TextType.TEXT))
        self.assertEqual(newer_nodes[1], TextNode("bold", TextType.BOLD))
        self.assertEqual(newer_nodes[2], TextNode(" and ", TextType.TEXT))
        self.assertEqual(newer_nodes[3], TextNode("italicized", TextType.ITALICS))
        self.assertEqual(newer_nodes[4], TextNode(" words contained within.", TextType.TEXT))

    def test_code(self):
        node = TextNode("This text has `code` contained within.", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node],"`",TextType.CODE)
        self.assertEqual(new_nodes[0], TextNode("This text has ", TextType.TEXT))
        self.assertEqual(new_nodes[1], TextNode("code", TextType.CODE))
        self.assertEqual(new_nodes[2], TextNode(" contained within.", TextType.TEXT))

    def test_image(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        )

    def test_link(self):
        node = TextNode(
            "This is text with a [link](https://mod366.de) and another [second link](https://twitch.tv/MoD366)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://mod366.de"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second link", TextType.LINK, "https://twitch.tv/MoD366"),
            ],
            new_nodes,
        )

    def test_text_to_textnode1(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        tomatch = text_to_textnode(text)
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALICS),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            tomatch
        )