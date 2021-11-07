# !/usr/bin/env python3
# @AUTHOR : njmck

import image_vocab_functions as ivf
import argparse
# from importlib import reload



def main():
	# Spreadsheet must have following columns:
	# image - image file name including file extension
	# jp - the Japanese vocabulary
	# count - =COUNTIF($B$2:$B$9771,BX). Human-readable column to prevent doubles
	# custom kana - enter custom kana if necessary
	# custom eng - enter custom English vocab if necessary

	# Accept argument for vocab spreadsheet in the command line:
	parser = argparse.ArgumentParser(description='vocabulary spreadsheet file')
	parser.add_argument('spreadsheet', metavar='spreadsheet', type=str, help='enter vocab spreadsheet filename')
	args = parser.parse_args()
	spreadsheet_filename = args.spreadsheet

	# Use functions to process the spreadsheet data and export a second spreadsheet:
	query_dict = ivf.import_queries(spreadsheet_filename)
	potential_jmdict_indices = ivf.match_jmdict_indices(query_dict)
	search_dict = ivf.closest_match(query_dict, potential_jmdict_indices, spreadsheet_filename)
	ivf.show_no_match_images(search_dict)


if __name__ == '__main__':
	main()
