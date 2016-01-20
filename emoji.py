from PIL import Image
import numpy as np
import sys

ICON_SIZE = 20

def crop_icon(img, row, col):
	return img.crop((
		col * ICON_SIZE,
		row * ICON_SIZE,
		(col + 1) * ICON_SIZE,
		(row + 1) * ICON_SIZE))

def img_hist(img):
	arr = np.array(img.getdata(), np.uint8)
	return np.histogramdd(arr[:,:-1], bins = 6, range = [[0, 256]] * 3, weights = arr[:,3])[0]

def hist_distance(hist1, hist2):
	return np.linalg.norm(hist1 - hist2)

icons_image = Image.open("emoji_sprite.png")
x_size, y_size = icons_image.size
x_icons = x_size / ICON_SIZE
y_icons = y_size / ICON_SIZE

icons = [
    crop_icon(icons_image, row, col)
    for col in range(x_icons) for row in range(y_icons)]
icon_hists = map(img_hist, icons)

img_filename = sys.argv[1]
img = Image.open(img_filename).convert('RGBA')
x_size, y_size = img.size
x_size -= (x_size % ICON_SIZE)
y_size -= (y_size % ICON_SIZE)

new_img = Image.new("RGB", (x_size, y_size), "white")
for row in range(y_size / ICON_SIZE):
	for col in range(x_size / ICON_SIZE):
		region_hist = img_hist(crop_icon(img, row, col))
		icon = min(
			enumerate(icons),
			key = lambda icon: hist_distance(icon_hists[icon[0]], region_hist))[1]
		new_img.paste(icon, (col * ICON_SIZE, row * ICON_SIZE),
			mask = icon.split()[3])

new_img.show()
new_img.save(img_filename + '.out.png')
