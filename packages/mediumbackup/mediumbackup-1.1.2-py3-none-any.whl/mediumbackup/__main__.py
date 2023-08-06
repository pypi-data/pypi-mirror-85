import mediumbackup as mb
import argparse

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Backup your Medium stories.')

    parser.add_argument("username",
                        help="A Medium username",
                        )
                        
    parser.add_argument("--backup_dir", "-bd", 
                        default=mb.DEFAULT_BACKUP_DIR,
                        help="backup directory",
                        )
                        
    parser.add_argument("--format", "-f", 
                        default=mb.DEFAULT_FORMAT,
                        help="\"html\" or \"md\" for markdown",
                        )
                        
    parser.add_argument("--download_images", "-i", 
                        action="store_true", 
                        help="Download images locally",
                        )
    parser.set_defaults(download_images=False)
    
    parser.add_argument("--images_dir", "-id", 
                        default=None,
                        help="images directory (if not in backup directory)",
                        )
                        
    parser.add_argument("--jekyll_front_matter", "-jfm", 
                        action="store_true", 
                        help="Include jekyll front matter if markdown",
                        )
    parser.set_defaults(jekyll_front_matter=False)
    
    arguments = parser.parse_args()
    mb.backup_stories(
        arguments.username, backup_dir=arguments.backup_dir, 
        format=arguments.format, download_images=arguments.download_images,
        images_dir=arguments.images_dir,
        jekyll_front_matter=arguments.jekyll_front_matter,
        )
    
    