from PIL import Image
import os
import re
import glob



modify_dir = "modify_dir"
output_dir = modify_dir + "/output"

def dakuten_fix():
    '''
    Solves an issue where the dakuten '゙' or the handakuten '゚' separates from the kana.
    This bug occurs when I use a YouTube screenshot Chrome extension and the filename is given automatically.
    Modifies file names in place (no copies of files made).
    '''
    global modify_dir
    # Start reading image files:
    ext_list = ['jpg', 'jpeg', 'png', 'bmp', 'tif', 'gif']
    img_file_list = []
    for ext in ext_list:
        img_file_list += glob.glob(modify_dir + '/*.' + ext)
    img_file_list = sorted(img_file_list)
    dakuten_bug_dict = {"が": "が", "ぎ": "ぎ", "ぐ": "ぐ", "げ": "げ", "ご": "ご",
                       "ざ": "ざ", "じ": "じ", "ず": "ず", "ぜ": "ぜ", "ぞ": "ぞ",
                       "だ": "だ", "ぢ": "ぢ", "づ": "づ", "で": "で", "ど": "ど",
                       "ば": "ば", "び": "び", "ぶ": "ぶ", "べ": "べ", "ぼ": "ぼ",
                       "ゔ": "ゔ",
                       "ぱ": "ぱ", "ぴ": "ぴ", "ぷ": "ぷ", "ぺ": "ぺ", "ぽ": "ぽ",
                       "ガ": "ガ", "ギ": "ギ", "グ": "グ", "ゲ": "ゲ", "ゴ": "ゴ",
                       "ザ": "ザ", "ジ": "ジ", "ズ": "ズ", "ゼ": "ゼ", "ゾ": "ゾ",
                       "ダ": "ダ", "ヂ": "ヂ", "ヅ": "ヅ", "デ": "デ", "ド": "ド",
                       "バ": "バ", "ビ": "ビ", "ブ": "ブ", "ベ": "ベ", "ボ": "ボ",
                       "ヴ": "ヴ",
                       "パ": "パ", "ピ": "ピ", "プ": "プ", "ペ": "ペ", "ポ": "ポ"
                       }
    # For all files in the desired directory:
    for old_name in img_file_list:
        filename = str(old_name)
        for char in dakuten_bug_dict.keys():
            filename = re.sub(char, dakuten_bug_dict[char], filename)
        if filename != old_name:
            new_name = str(filename)
            # os.rename(old_name, new_name)
            print("\"" + old_name + "\"" + " renamed to " + "\"" + new_name + "\"")
        else:
            print("\"" + old_name + "\"" + " name change not necessary.")


def compress_img(quality):
    '''
    :param quality: Integer between 1 to 95 which determines quality of the compressed output image.
    '''
    global modify_dir, output_dir
    # Extract all of the images:
    files = os.listdir(modify_dir)
    print("Looking for image files in " + modify_dir + "...")
    image_list = [file for file in files if file.endswith(('jpg', 'png', 'jpeg', 'gif'))]

    # Loop over every image:
    if image_list == []:
        print("Error. No images found.")
    else:
        for image in image_list:
            # Open every image:
            img = Image.open(modify_dir + "/" + image)

            rgb_img = img.convert('RGB')
            filename = output_dir + "/" + image[:-4] + '.jpg'

            # Compress every image and save it with a new name:
            rgb_img.save(filename, optimize=True, quality=quality)
            print("Saving modified image as " + output_dir + "/" + image)


def rotate_images(angle):
    '''
    :param angle: Integer representing angle of rotation in anti-clockwise direction.
    '''
    global modify_dir, output_dir
    # Extract all of the images:
    files = os.listdir(modify_dir)
    print("Looking for image files in " + modify_dir + "...")
    image_list = [file for file in files if file.endswith(('jpg', 'png', 'jpeg', 'gif'))]
    # rotate image
    if image_list == []:
        print("Error. No images found.")
    else:
        for image in image_list:
            im = Image.open(modify_dir + "/" + image)
            out = im.rotate(angle, expand=True)
            filename = output_dir + "/" + image[:-4] + '.jpg'
            out.save(filename)
            print("Saving modified image as " + output_dir + "/" + image)
