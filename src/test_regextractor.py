import unittest

from regextractor import extract_markdown_images, extract_markdown_links

class RegexExtraction(unittest.TestCase):
    def test_single_image(self):
        tomatch = extract_markdown_images("This text includes a very nice picture of me ![Picture of the Mona Lisa](https://i.otto.de/i/otto/60745673-49b6-56f6-b657-87fe0e302f45?w=750&h=1000). Isn't it beautiful?")
        self.assertListEqual([("Picture of the Mona Lisa", "https://i.otto.de/i/otto/60745673-49b6-56f6-b657-87fe0e302f45?w=750&h=1000")], tomatch)

    def test_two_images(self):
        tomatch = extract_markdown_images("This text includes a very nice picture of me ![Picture of the Mona Lisa](https://i.otto.de/i/otto/60745673-49b6-56f6-b657-87fe0e302f45?w=750&h=1000). Isn't it beautiful? And here's my boyfriend ![Brad Pitt](https://upload.wikimedia.org/wikipedia/commons/thumb/9/90/Brad_Pitt-69858.jpg/800px-Brad_Pitt-69858.jpg)")
        self.assertListEqual([("Picture of the Mona Lisa", "https://i.otto.de/i/otto/60745673-49b6-56f6-b657-87fe0e302f45?w=750&h=1000"),("Brad Pitt", "https://upload.wikimedia.org/wikipedia/commons/thumb/9/90/Brad_Pitt-69858.jpg/800px-Brad_Pitt-69858.jpg")], tomatch)


    def test_single_link(self):
        tomatch = extract_markdown_links("This text includes a link to [my website](https://mod366.de). Isn't it beautiful?")
        self.assertListEqual([("my website", "https://mod366.de")], tomatch)

    def test_two_links(self):
        tomatch = extract_markdown_links("This text includes a link to [my website](https://mod366.de) and my [Twitch channel](https://twitch.tv/MoD366)")
        self.assertListEqual([("my website", "https://mod366.de"),("Twitch channel", "https://twitch.tv/MoD366")], tomatch)

    def test_single_link_but_image(self):
        tomatch = extract_markdown_links("This text includes a link to [my website](https://mod366.de). Isn't it beautiful? There's also a picture of me: picture of me ![Picture of the Mona Lisa](https://i.otto.de/i/otto/60745673-49b6-56f6-b657-87fe0e302f45?w=750&h=1000).")
        self.assertListEqual([("my website", "https://mod366.de")], tomatch)