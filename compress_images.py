# !/usr/bin/env python3
# @AUTHOR : njmck

import misc_functions as mf
import argparse
# from importlib import reload



def main():
	# Accept argument for vocab spreadsheet in the command line:
	parser = argparse.ArgumentParser(description='image compression level (1 = MIN, 95 = MAX)')
	parser.add_argument('quality', metavar='quality level', type=int, help='enter an integer representing the level of compression from 1-95')
	args = parser.parse_args()
	image_comp_lvl = args.quality

	mf.compress_img(image_comp_lvl)


if __name__ == '__main__':
	main()
