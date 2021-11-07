# !/usr/bin/env python3
# @AUTHOR : njmck

import misc_functions as mf
import argparse
# from importlib import reload



def main():
	# Accept argument for vocab spreadsheet in the command line:
	parser = argparse.ArgumentParser(description='image rotation by specifying angle')
	parser.add_argument('angle', metavar='angle of rotation', type=int, help='Enter integer representing angle of rotation in anti-clockwise direction.')
	args = parser.parse_args()
	rotation_angle = args.angle

	mf.rotate_images(rotation_angle)


if __name__ == '__main__':
	main()
