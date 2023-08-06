# mediumbackup - A Backup Utility for Medium

Saves all your Medium stories locally as html or markdown files. 

## Installation
```
pip install mediumbackup
```

## Usage
### As a script from the command line
```
python -m mediumbackup "<your username>"
```
### As a module
```
import mediumbackup as mb

username = "<your username>"
mb.backup_stories(username)
```

## Options
Specify a folder.
``` 
python -m mediumbackup "<username>" --backup_dir "backup 2020-11-01"
```
Save as markdown.
``` 
python -m mediumbackup "<username>" --format "md"
```
Download images.
``` 
python -m mediumbackup "<username>" --format -i
```
Download images to a different folder than the stories.
``` 
python -m mediumbackup "<username>" --backup_dir "posts" --download_images --images_dir "assets/images" 
```
Include a front matter for jekyll.
``` 
python -m mediumbackup "<username>" --format "md" --jekyll_front_matter
```


## Tests
To run the tests, execute:
```
python -m tests
```
