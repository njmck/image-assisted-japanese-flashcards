# Image-assisted Vocab Flashcard Automation
___
## Description

A series of functions and scripts written in Python which can be used for creating Japanese-English
flashcards for rote memorisation of Japanese vocabulary using the [Flashcards Deluxe](https://orangeorapple.com/Flashcards/) app, with the added benefit of
adding an image file to help make the words less abstract through visual context. The
script also makes use of my [kanji-story-flashcards](https://github.com/njmck/kanji-story-flashcards)
functions to better understand the kanji too.

### Workflow

1. Create an Excel spreadsheet with the column headers below. Use "template_1.xlsx" included in
this repository as a template:
* 'image' - The filename of the image containing the word of interest. Images need to
be stored in the 'img' directory.
* 'jp' - The Japanese vocabulary of interest in its original form.
* 'count' - Not used in the script itself, but rather serves to detect replicates
of particular words that appear in the 'jp' column using the Excel "=COUNTIF()" formula.
* 'custom kana' - (Optional) Enter a custom kana pronunciation if one exists. Otherwise,
leave blank.
* 'custom eng' - (Optional) Enter a custom English definition if one exists. Otherwise,
leave blank.

2. Copy all of your image files listed within the 'image' column of your "template_1.xlsx" spreadsheet
into the "img" directory.


3. Use the command line to run the 'image_vocab_1.py' and use the "template.xlsx" or
your own spreadsheet as an argument. The script may then prompt you for an integer input
if it finds more than one match for a particular word. The image will also be opened in 
your default image viewer to assist with finding the closest English definition. Once all words have been processed, the
script will output another Excel
file called 'template_jmdict_indices.xlsx'. This file is a modified version of the original
Excel file, but has an additional column indicating the relevant matching index found within the JMdict EDICT dictionary.

```
## ---- UNIX TERMINAL ---- ##
python3 image_vocab_1.py template.xlsx
```

4. Open the 'template_jmdict_indices.xlsx' Excel spreadsheet and enter a custom kana and
custom English definition for rows in which the JMdict index was not found. Make sure to
save the file once changes have been made and close it.


5. Use the command line to run the 'image_vocab_2.py' script and use the edited
'template_jmdict_indices.xlsx' spreadsheet as an argument. This will output a file called
'templates_flashcards.xlsx'.

```
## ---- UNIX TERMINAL ---- ##
python3 image_vocab_2.py template_jmdict_indices.xlsx
```

6. Copy the 'templates_flashcards.xlsx' spreadsheet and 'templates_flashcards.xlsx Media' folder
into whatever directory you use to import data into [Flashcards Deluxe](https://orangeorapple.com/Flashcards/).

### data_prep.py
Script used for converting much of the data from the
[WWWJDIC online Japanese dictionary](http://www.edrdg.org/wiki/index.php/JMdict-EDICT_Dictionary_Project)
into Python dictionaries. This script also exports a json file called 'JMdict_filtered.json'
which is imported in the main functions file 'image_vocab_functions.py'.

### compress_images.py
Compresses image files in "modify_dir" and outputs compressed image files to
"modify_dir/output". You can specify a 'quality level' integer from most compressed (1)
to least compressed (95). Naturally, more compresses images take up less storage.

Example:
```
## ---- UNIX TERMINAL ---- ##
python3 compress_images.py 75
```

### rotate_images.py
Rotate images in "modify_dir" and outputs then to "modify_dir/output". Run the
script from the command line with an integer argument to specify the angle of
rotation in a counter-clockwise direction.

Example:
```
## ---- UNIX TERMINAL ---- ##
python3 rotate_images.py 90
```

### dakuten_fix.py
I've encountered bugs in Japanese text in file names where the dakuten can separate
from the character in the kana. For example, "が" instead of "が". This script
renames the files in place to join the dakuten character to its relative kana.
