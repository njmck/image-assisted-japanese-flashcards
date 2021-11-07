# !/usr/bin/env python3
# @AUTHOR : njmck

import json
import pandas as pd
import re
from PIL import Image
import time
import math



with open("JMdict_filtered.json", 'r') as jsonfile:
    jmdict = json.load(jsonfile)


def import_queries(spreadsheet_filename):
	'''
	:param query_spreadsheet: Filename string of the vocabulary spreadsheet.
	:return: Dictionary containing the contents of the vocabulary spreadsheet.
	'''
	query_df = pd.read_excel(spreadsheet_filename)
	query_dict = pd.DataFrame.to_dict(query_df, orient='list')
	query_dict.pop("count")
	# Strip whitespace from strings (which can happen often with human input):
	for key, value in query_dict.items():
		for enum, list_item in enumerate(value):
			if isinstance(list_item, str):
				value[enum] = (list_item.lstrip()).rstrip()
	# Replace floats with None:
	nan_rows = ["custom kana", "custom eng"]
	for colname in nan_rows:
		query_dict[colname] = [None for nan in query_dict[colname]]
	return query_dict


def match_jmdict_indices(query_dict):
	'''
	:param query_dict: Dictionary produced from "import_queries" function.
	:return: list containing indices of potential matches from jmdict.
	'''
	global jmdict
	potential_jmdict_indices = []
	for query_enum, query_jp in enumerate(query_dict["jp"]):
	    print('Searching ' + str(query_enum + 1) + ' of ' + str(len(query_dict["jp"])) + '...')
	    potential_child_list = []
	    # Search for the vocabulary within the wwwjdic database:
	    for jmdict_enum, jmdict_main in enumerate(jmdict["main_list"]):
	        for jmdict_single_vocab in jmdict_main:
	            if jmdict_single_vocab == query_jp:
	                potential_child_list.append(jmdict_enum)
	    potential_jmdict_indices.append(potential_child_list)
	return potential_jmdict_indices


def closest_match(query_dict, potential_jmdict_indices, spreadsheet_filename):
	'''
	:param query_dict: Dictionary produced from "import_queries" function.
	:param potential_jmdict_indices: List produced from "match_jmdict_indices" function.
	:param spreadsheet_filename: Filename string of the vocabulary spreadsheet.
	:return:
	'''
	# Test if there are multiple different meanings:
	global jmdict
	single_no_match = False
	search_dict = dict(query_dict)
	search_dict["jmdict index"] = []
	search_dict["query index"] = []
	for enum_pot, pot_single in enumerate(potential_jmdict_indices):
		if len(pot_single) == 1:
			search_dict["jmdict index"].append(pot_single[0])
			search_dict["query index"].append(0)
		elif len(pot_single) > 1:
			print("Multiple matches found. Which definition is most correct for:")
			im = Image.open("img/" + query_dict["image"][enum_pot])
			im.show()
			print(query_dict['jp'][enum_pot] + "?:")
			for pot_single_choices_enum, pot_single_choice in enumerate(pot_single):
				print('----------[' + str(pot_single_choices_enum + 1) + ']----------')
				print(' [' + ', '.join(jmdict["main_list"][pot_single_choice]) + ']')
				print_eng = re.sub('<b>', '', jmdict['en_list_neat'][pot_single_choice])
				print_eng = re.sub('</b>', '', print_eng)
				print_eng = re.sub('\|', '\n', print_eng)
				print(print_eng)
				print()
			user_choice = int(input()) - 1
			# If user choice index is out of range, don't continue:
			if user_choice >= len(pot_single) or not isinstance(user_choice, int):
				while user_choice >= len(pot_single):
					user_choice = int(input()) - 1
			# Append the user's choice:
			search_dict["jmdict index"].append(pot_single[user_choice])
			search_dict["query index"].append(user_choice)
		else:
			single_no_match = True
			search_dict["jmdict index"].append("")
			search_dict["query index"].append("")
	if single_no_match:
		for row_no, query in enumerate(search_dict["query index"]):
			if query == "":
				print("No match found for row " + str(row_no + 2) + " - " + query_dict['jp'][row_no])
		# Export the Excel file that is identical to the previous, only missing "count" and with no match data:
		export_df = pd.DataFrame(search_dict)
		try:
			export_df.to_excel(spreadsheet_filename[:-5] + "_jmdict_indices.xlsx", sheet_name='Sheet1', index=False)
			print(spreadsheet_filename[:-5] + "_jmdict_indices.xlsx exported successfully.")
		except BlockingIOError:
			print(spreadsheet_filename[:-5] + "_jmdict_indices.xlsx could NOT be exported. Ensure there is no file open of the same name in Excel.")
		print("Unmatched words found above. Add your own information to 'custom kana' and 'custom eng' before continuing.")
	else:
		print("Success! Matches found for all words. Move straight to next step.")
	return search_dict


def show_no_match_images(search_dict):
	print("Showing images for which no match was found in the dictionary. Please wait...")
	for enum, image_filename in enumerate(search_dict['image']):
		if search_dict['jmdict index'][enum] == "":
			im = Image.open("img/" + image_filename)
			im.show()
			time.sleep(2) # Allow for loading of images gradually.


def second_spreadsheet(second_spreadsheet):
	query_df = pd.read_excel(second_spreadsheet)
	query_dict = pd.DataFrame.to_dict(query_df, orient='list')
	# Strip whitespace from strings (which can happen often with human input):
	for key, value in query_dict.items():
		for enum, list_item in enumerate(value):
			if isinstance(list_item, str):
				value[enum] = (list_item.lstrip()).rstrip()
			# Change floats to ints to be used as indices.
			elif isinstance(list_item, float):
				if math.isnan(list_item):
					value[enum] = ""
				else:
					value[enum] = int(list_item)
	return query_dict


def kanji_stories(query_dict):
	'''
    input_dir = vocab file where the first column must contain the kanji-containing Japanese vocab.
    stories_filename = filename of our 3-column kanji stories file.
    stories_colname = column name for the additional column in which stories will be added.
    '''
	stories_df = pd.read_excel("2021.02.18_all_kodansha_kanji_course.xlsx", header=None)
	stories_df.columns = ["kanji", "meaning", "story"]
	stories_file_dict = pd.DataFrame.to_dict(stories_df, orient='list')
	# Scan each word in the vocab dataframe 'kanji' column for kanji that appear in the stories file:
	parent_kanji_list = []
	for word in query_dict['jp']:
		child_kanji_list = []
		for moji in word:
			for kanji in stories_file_dict['kanji']:
				if moji == kanji:
					if kanji not in child_kanji_list:
						child_kanji_list.append(kanji)
		parent_kanji_list.append(child_kanji_list)
	# Create structured nested lists containing relevant kanji information and colour formatting:
	parent_story_list = []
	for child_kanji_list in parent_kanji_list:
		child_story_list = []
		for single_kanji in child_kanji_list:
			for enum, story_file_kanji in enumerate(stories_file_dict["kanji"]):
				gc_list = []
				if single_kanji == story_file_kanji:
					# Add a yellow colour tag to make the kanji more readable:
					gc_list.append("<color yellow>" + stories_file_dict["kanji"][enum] + "</color>")
					gc_list.append("<color yellow>" + stories_file_dict["meaning"][enum] + "</color>")
					gc_list.append(stories_file_dict["story"][enum])
					child_story_list.append(gc_list)
		parent_story_list.append(child_story_list)
	# Create a single list of strings with Flashcards Deluxe formatting for each vocab:
	story_string_list = []
	for child_story_list in parent_story_list:
		if child_story_list == []:
			story_string = ""
		else:
			string_prep_list = []
			for story in child_story_list:
				joined = ("|").join(story)
				string_prep_list.append(joined)
			story_string = ("||").join(string_prep_list)
		story_string_list.append(story_string)
	return story_string_list


def second_scan(query_dict):
	global jmdict
	# Initialise
	fc_dict = {"Text 1": [], # kanji
			   "Text 2": [], # kana
			   "Text 3": [], # eng definition
			   "Picture 1": [], # image containing word
			   "Text 4": []} # kanji stories
	# Text 1 - Kanji
	fc_dict["Text 1"] = query_dict['jp']
	# Picture 1 - Image containing word
	fc_dict["Picture 1"] = query_dict['image']
	# Text 4 - Kanji stories
	fc_dict["Text 4"] = query_dict["kanji story"]
	# Handle depending on whether custom kana and English definition had to be added:
	for row_no, jmdict_index in enumerate(query_dict['jmdict index']):
		# If there is no custom meaning added:
		if query_dict['custom kana'][row_no] == '' and query_dict['custom eng'][row_no] == '':
			# Text 2 - Kana
			fc_dict["Text 2"].append(jmdict['kana_list'][query_dict['jmdict index'][row_no]][0])
			# Text 3 - English meaning
			fc_dict["Text 3"].append(jmdict['en_list_neat'][query_dict['jmdict index'][row_no]])
		elif query_dict['custom kana'][row_no] != '' and query_dict['custom eng'][row_no] != '':
			# Text 2 - Kana
			fc_dict["Text 2"].append(query_dict['custom kana'][row_no])
			# Text 3 - English meaning
			fc_dict["Text 3"].append(query_dict['custom eng'][row_no])
		elif query_dict['custom kana'][row_no] == '' and query_dict['custom eng'][row_no] != '':
			# Text 2 - Kana
			fc_dict["Text 2"].append("")
			# Text 3 - English meaning
			fc_dict["Text 3"].append(query_dict['custom eng'][row_no])
		else:
			# Text 2 - Kana
			fc_dict["Text 2"].append(query_dict['custom kana'][row_no])
			# Text 3 - English meaning
			fc_dict["Text 3"].append("")
	return fc_dict
