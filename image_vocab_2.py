# !/usr/bin/env python3
# @AUTHOR : njmck

import image_vocab_functions as ivf
import argparse
import pandas as pd
import os
# from importlib import reload



def main():
	# Accept argument for vocab spreadsheet:
	parser = argparse.ArgumentParser(description='vocabulary spreadsheet file')
	parser.add_argument('spreadsheet', metavar='spreadsheet', type=str, help='enter your team')
	args = parser.parse_args()
	second_spreadsheet = args.spreadsheet

	# Use functions to process the spreadsheet data and export a second spreadsheet:
	query_dict = ivf.second_spreadsheet(second_spreadsheet)
	kanji_stories = ivf.kanji_stories(query_dict)
	query_dict["kanji story"] = kanji_stories
	fc_dict = ivf.second_scan(query_dict)
	flashcards_filename = second_spreadsheet[:-19] + "flashcards.xlsx"
	fc_df = pd.DataFrame(fc_dict)
	print("Exporting " + flashcards_filename + " ...")
	fc_df.to_excel(flashcards_filename, sheet_name='Sheet1', index=False)
	os.rename("img", flashcards_filename + " Media")
	os.mkdir("img")
	print(flashcards_filename + " successfully exported.")


if __name__ == '__main__':
	main()
