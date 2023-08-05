import unittest
import filecmp
import os
import shutil

import mediumbackup as mb


def dummy_medium_story():
    dummy_raw = {
        "title": "Lorem Ipsum Dolor sit Amet",
        "pubDate": "2020-11-07 11:12:13",
        "link": "https://medium.com/@johndoe/some-title-and-random-charachters-abcdef123456",
        "guid": "https://medium.com/p/abcdef123456",
        "author": "Jon Doe",
        "thumbnail": "https://cdn-images-1.medium.com/max/1024/abcdef123456.png",
        "description": "",
        "content": "",
        "enclosure": "",
        "categories": ["tagA", "tagB", "tagC"],
    }
    return mb.MediumStory(dummy_raw)

class MediumStoriesTest(unittest.TestCase):
    
    def test_stripped_link(self):
        links = [
            "https://medium.com/@johndoe/some-title-abc123",
            "https://medium.com/@johndoe/some-title-abc123?source=rss-abc123",
        ]
        for link in links:
            story = dummy_medium_story()
            story.raw["link"] = link
            story = mb.MediumStory(story.raw)
            self.assertEqual(links[0], story.link)
            
    
    def test_backup_stories_wo_images(self):
        test_backup_dir = os.path.join("tests","backup")
        for format in ("html", "md"):
            mb.backup_stories(username="lucafrance", backup_dir=test_backup_dir, format=format)
            file_extension = "." + format
            reference_story_name = "2020-10-05-come-aggiungere-i-caratteri-ma"
            test_file = os.path.join(test_backup_dir, reference_story_name) + file_extension
            reference_file = os.path.join("tests", reference_story_name) + file_extension
            self.assertTrue(os.path.exists(test_file))
        shutil.rmtree(test_backup_dir)
    
    
    def test_title(self):
        story = dummy_medium_story()
        story.title = "Lorem Ipsum"
        story.content = "<p>Dolor sit amet</p>"
        self.assertEqual(story.html(), "<h3>Lorem Ipsum</h3><p>Dolor sit amet</p>")
    
    
    def test_download_images(self):
        story = dummy_medium_story()
        images_dir = os.path.join("tests", "images")
        img_url = "http://www.python.org/static/community_logos/python-logo-master-v3-TM.png"
        story.content = "<img src=\"{}\"></img>".format(img_url)
        story.download_images(images_dir=images_dir)
        img_path = os.path.join(images_dir, "python-logo-master-v3-TM.png")
        self.assertTrue(os.path.exists(img_path))
        shutil.rmtree(images_dir)
    
    
    def test_stat_image_removal(self):
        story = dummy_medium_story()
        story.content = "<img alt=\"\" height=\"1\" src=\"https://medium.com/_/stat?event=post.clientViewed&amp;referrerSource=full_rss&amp;postId=abcdef123456\" width=\"1\"/>"
        self.assertFalse("https://medium.com/_" in story.html())
    
    
    def test_gist_embedding(self):
        story = dummy_medium_story()
        story.content = "<a href=\"https://medium.com/media/b32cf10831e25c6c315a79bfee55dc8e/href\">https://medium.com/media/b32cf10831e25c6c315a79bfee55dc8e/href</a>" 
        self.assertTrue("<script src=\"https://gist.github.com/lucafrance/2a88f1e7a261292a8be63f8974ef1ca6.js\"></script>" in story.html())
    
    
    def test_jekyll_front_matter(self):
        story = dummy_medium_story()
        story.title = "Lorem Ipsum"
        story.link = "www.example.com"
        self.assertTrue(story.markdown(jekyll_front_matter=True).startswith("---\ntitle: Lorem Ipsum\ncanonicalurl: www.example.com\n---\n\n"))
    
    
if __name__ == "__main__":
    unittest.main()
