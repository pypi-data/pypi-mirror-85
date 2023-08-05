import os
import logging

import medium
from markdownify import markdownify as md
from bs4 import BeautifulSoup as bs
import requests

MAX_FILENAME_LENGTH = 30 # Ignores date and extension, e.g. 2020-10-31<-- 30 characthers -->.md
FORBIDDEN_FILENAME_CHARS = "*?"

DEFAULT_BACKUP_DIR = "backup"
DEFAULT_FORMAT = "html"

class MediumStory():
    
    def __init__(self, raw):
        self.raw = raw
        self.pub_date = raw["pubDate"][:len("yyyy-mm-dd")]
        self.title = raw["title"]
        self.link = raw["link"].split("?")[0]
        self.content = raw["content"]
        self._html = None
        self._markdown = None
    
    def html(self):
        
        if self._html is not None:
            return self._html
        
        # Add story title to the content
        html = "<h3>{}</h3>{}".format(self.title, self.content)
        
        # Remove placeholder images for stats
        # They are used to count views from e.g. rss feeds
        soup = bs(html, "html.parser")
        for img in soup.find_all("img"):
            if img["src"].startswith("https://medium.com/_/stat"):
                img.decompose()
        html = str(soup)  
        
        # Embrace loose links in a figure, otherwise embedded content
        # stays on the same line as the next paragraph and looks weird
        # especially when converted to markdown. E.g.:
        # <a href="https://medium.com/media/abcdef123456/href">
        #    https://medium.com/media/abcdef123456/href
        # </a><p>Lorem Ipsum [...] dolor sit amet.</p>
        soup = bs(html, "html.parser")
        links_to_replace = []
        for a in soup.find_all("a"):
            if a.parent.name == "[document]":
                links_to_replace.append(str(a))
        html = str(soup)    
        for link in links_to_replace:
            html = html.replace(link, "<figure>{}</figure>".format(link))
        
        # Check links starting with https://medium.com/media/, which are 
        # probably embedded content and redirect to other websites. 
        # If so, replace the url with the final one
        links_redirects = []
        soup = bs(html, "html.parser")
        for a in soup.find_all("a"):
            a_href = a["href"]
            if a_href.startswith("https://medium.com/media/"):
                r = requests.get(a_href, allow_redirects=True)
                if not r.ok:
                    logging.warning("Could not resolve \"{}\", maybe the link is broken.".format(a_href))
                if a_href != r.url:
                    links_redirects.append((a_href, r.url))
        for medium_link, redirect_link in links_redirects:
            html = html.replace(medium_link, redirect_link)
        
        
        # Replace gist links with embedding script
        soup = bs(html, "html.parser")
        for a in soup.find_all("a"):
            a_href = a["href"]
            if a_href == a.string and a_href.startswith("https://gist.github.com/"):
                embedding_tag = soup.new_tag("script", src=a_href + ".js")
                a.replace_with(embedding_tag)
        html = str(soup)
        
        
        self._html = html
        return self._html
    
    def download_images(self, images_dir, images_src=None):
        """ Download images and update the html to use the local images as source.
        
        Keyword arguments:
        images_dir    -- the directory where the images should be saved
                         e.g. /backup/images or /assets/images
        images_src    -- the source parameter to be entered in html 
                         e.g. /images
        """
        
        # If images_src is missing, assume the directory
        # Replace "\" with "/" for Windows
        if images_src is None:
            images_src = images_dir.replace("\\", "/")
        
        # If the folder doesn't exist yet, create it
        os.makedirs(images_dir, exist_ok=True)
            
        # Parse the html source for all images
        html = self.html()
        soup = bs(html, "html.parser")
        img_sources = [img["src"] for img in soup.find_all("img")]
        
        # For each image, download it and update the html source
        for img_src in img_sources:
            
            # Build the filename of the image
            filename = img_src.split("/")[-1]
            for char in FORBIDDEN_FILENAME_CHARS:
                filename = filename.replace(char, "")
            
            # Download the image
            r = requests.get(img_src)
                    
            # Save the image
            file_path = os.path.join(images_dir, filename)
            with open(file_path, "wb") as f:
                f.write(r.content)
                logging.info("Downloaded \"{}\" to \"{}\".".format(img_src, file_path))
                
            #Replace src attributes to point to the downloaded image
            new_src = "/".join((images_src, filename))
            html = html.replace("src=\"" + img_src  + "\"",
            "src=\"" + new_src + "\"")        
        
        # Update html paramter with local sources paths
        self._html = html
        return
        
    def markdown(self, jekyll_front_matter=False):
        """ Return the content of the story in markdown.
        
        Keyword arguments:
        jekyll_front_matter    -- include a front matter to use with jekyll 
        """
        
        if self._markdown is not None:
            return self._markdown
        
        html = self.html()
        
        # Add two new lines after figures and blockquotes 
        # to prevent formatting errors with markdown
        # https://github.com/matthewwithanm/python-markdownify/pull/25
        for closing_tag in ["</figure>", "</blockquote>"]:
            html = html.replace(closing_tag, closing_tag + "<br><br>")
        
        # Workaround for ordered lists in markdownify
        # https://github.com/matthewwithanm/python-markdownify/issues/8
        # https://github.com/matthewwithanm/python-markdownify/pull/23
        html = html.replace("\n<li>", "<li>")
        
        # Escape sequence for grave accent
        html = html.replace("`", "\\`")
        
        # Workaround for <pre> tags not being converted
        html = html.replace("<pre>", "<pre>```").replace("</pre>", "```</pre>")
        
        # Convert to markdown
        md_story = md(html, heading_style="ATX")
        
        # Ensure that "```" stays on its own line
        md_story = md_story.replace("```", "\n```\n")
        
        # Remove leading whitspaces
        # https://github.com/matthewwithanm/python-markdownify/issues/17
        md_story = "\n".join([line.strip() for line in md_story.split("\n")])
        
        # Add jekyll front matter
        if jekyll_front_matter:
            front_matter = "---\ntitle: {}\ncanonicalurl: {}\n---\n\n".format(
                self.title, self.link
            )
            md_story = front_matter + md_story
            
        self._markdown = md_story
        return self._markdown
        
    def backup(self, backup_dir, format, download_images=False, images_dir=None, jekyll_front_matter=False):
        """ Download the story locally.
        
        Keyword arguments:
        backup_dir          -- destination directory name, default "backup"
        format              -- "html" or "md" for markdown, default "html"
        download_images     -- True to download images and adjust the source, default False
        images_dir          -- directory to save the images, if different from backup_dir/images 
        jekyll_front_matter -- Include jekyll front matter, only valid with markdown
        """
        
        logging.info("Downloading story \"{}\" published on \"{}\".".format(self.title, self.pub_date))
        
        # Check user input
        if format not in ["html", "md"]:
            logging.warning("Format {} not recognized, html will be used instead.".format(format))
        
        if format != "md" and jekyll_front_matter:
            logging.warning("Format {} cannot include a jekyll front matter. For that use markdown (\"md\") instead.".format(format))
        
        # Create backup directory if not existent
        if not os.path.exists(backup_dir):
            os.mkdir(backup_dir)
        
        # Download images if necessary
        if download_images:
            if images_dir is None:
                images_dir = "/".join((backup_dir, "images"))
                images_src = "images"
            else:
                images_src = None
            self.download_images(images_dir=images_dir, images_src=images_src)
        
        # Get the content formatted correctly
        if format == "md":
            content = self.markdown(jekyll_front_matter=jekyll_front_matter)
        else:
            # html is the default option
            content = self.html()
        
        # Find the url path portion of the story url 
        # (i.e. whatever comes after the last /)
        # and remove invalid filename characthers
        url_path = self.link.split("/")[-1]
        for char in FORBIDDEN_FILENAME_CHARS:
            url_path = url_path.replace(char, "")
            
        # Build the filename and save the file
        filename = "".join([self.pub_date, "-", url_path[:MAX_FILENAME_LENGTH], ".", format])
        with open(os.path.join(backup_dir, filename), "wt", encoding="utf8") as f:
            f.write(content)
        logging.info("Story \"{}\" downloaded to \"{}\".".format(self.title, filename))
        
        return
        
def backup_stories(username, backup_dir=DEFAULT_BACKUP_DIR, 
                   format=DEFAULT_FORMAT, 
                   download_images=False,
                   images_dir=None,
                   jekyll_front_matter=False,
                   ):
    """ Download all public stories by username. """
    
    # Get the stories list through a medium client, 
    # authentication is not required in this case 
    mclient = medium.Client()
    list_stories = mclient.list_articles(username=username)
    
    # For each story, crate a backup file
    for story_raw in list_stories:
        story = MediumStory(story_raw)
        story.backup(backup_dir, format=format, 
                     download_images=download_images,
                     images_dir=images_dir,
                     jekyll_front_matter=jekyll_front_matter,
                     )
        print("Downloaded Medium story: \"{}\"".format(story.title))
    
    return
    
    