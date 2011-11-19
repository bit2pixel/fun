#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Author: Renan Cakirerk <public [at] cakirerk.org>
Usage: ./unshredder.py img.png
"""

from PIL import Image, ImageFilter
import math
import sys

image = Image.open(sys.argv[1])
data = image.getdata()

img_width, img_height = image.size

def get_pixel_value(slice_data, slice_width, x, y):
    # Get RGB values of the pixel
    pixel = slice_data[y * slice_width + x]
    return pixel

def get_slice_col(img_slice, column):
    # Get column of a slice
    col = []
    slice_w, slice_h = img_slice.size
    slice_data = img_slice.getdata()

    for y in range(slice_h):
        col.append(list(get_pixel_value(slice_data, slice_w, column, y)))

    return col

def slice_image(slice_width):
    # Slice an image with the given width
    no_of_slices = img_width / slice_width
    img_slice = []

    for x in range(no_of_slices):
        img = image.crop((x * slice_width, 0, x * slice_width + slice_width, img_height))
        img_slice.append(img)

    return img_slice

def get_col_diff(col1, col2):
    # Get differences of two columns
    pixel_diff_sum = 0

    for pix in range(len(col1)):
        p1 = col1[pix]
        p2 = col2[pix]

        distance = math.sqrt( pow(p1[0] - p2[0], 2) + pow(p1[1] - p2[1], 2) + pow(p1[2] - p2[2], 2) )
        pixel_diff_sum += distance

    return pixel_diff_sum

""" AUTOFIND SLICE WIDTH ATTEMPT """
def factors(img_width):
    # Find how many different ways an image can be sliced uniformly
    factors = []
    for i in range(1, img_width):
        if img_width % i == 0:
            factors.append(i)
    return factors

# Get diffs of all factors of the width
slice_by_factor_diffs = []
for f in factors(img_width):
    if f != 1:
        slice_diffs = []
        s_width = img_width / f
        slice_by_factor = slice_image(s_width)

        for s in slice_by_factor:
            if s == slice_by_factor[0]:
                s_pre_last_col = get_slice_col(s, s_width - 1)
                continue

            s_cur_first_col = get_slice_col(s, 0)
            slice_diffs.append(get_col_diff(s_pre_last_col, s_cur_first_col))
            s_pre_last_col = get_slice_col(s, s_width - 1)

        avg = sum(slice_diffs) / len(slice_diffs)
        slice_by_factor_diffs.append(int(avg))

# Get the largest 3 diff
largest_diffs = []
sorted_slice_by_factor_diffs = sorted(slice_by_factor_diffs)

if len(sorted_slice_by_factor_diffs) >= 3:
    largest_diffs = [sorted_slice_by_factor_diffs[-1],
                     sorted_slice_by_factor_diffs[-2],
                     sorted_slice_by_factor_diffs[-3]]

    largest_diffs_indexes = [slice_by_factor_diffs.index(largest_diffs[0]),
                             slice_by_factor_diffs.index(largest_diffs[1]),
                             slice_by_factor_diffs.index(largest_diffs[2])]
else:
    largest_diffs = [sorted_slice_by_factor_diffs[-1],
                     sorted_slice_by_factor_diffs[-2]]

    largest_diffs_indexes = [slice_by_factor_diffs.index(largest_diffs[0]),
                             slice_by_factor_diffs.index(largest_diffs[1])]
""" END OF AUTOFIND """

""" TRY THE LARGEST 3 DIFFS """
for d in largest_diffs_indexes:
    try:
        factor = factors(img_width)[d+1]
        slice_width = img_width / factor
        slices = slice_image(slice_width)

        # Get all first and last columns of the slices
        slice_first_cols = []
        slice_last_cols = []

        for s in range(len(slices)):
            slice_first_cols.append(get_slice_col(slices[s], 0))
            slice_last_cols.append(get_slice_col(slices[s], slice_width - 1))

        def find_next(relations, key):
            for i in range(len(slices)):
                if not relations[i].keys() == relations[i].values():
                    if relations[i].keys().__contains__(key):
                        return relations[i].values()[0]

        relations = []

        # Compare slices
        for i in range(len(slices)):
            z = []
            for j in range(len(slices)):
                diff = get_col_diff(slice_first_cols[i], slice_last_cols[j])
                z.append(diff)

            relations.append({z.index(min(z)): i})

        first_img = None

        # Get first
        for i in range(len(slices)):
            if relations[i].keys() == relations[i].values():
                first_img = relations[i].keys()[0]

        order = []
        next_img = first_img
        for i in range(len(slices)):
            order.append(next_img)
            next_img = find_next(relations, next_img)

        ordered_image = Image.new('RGBA', image.size)
        j = 0
        for i in order:
            ordered_image.paste(slices[i], (slice_width * j, 0))
            j+=1

        ordered_image.save('ordered-%s' % sys.argv[1])
        print "Saved file as 'ordered-%s'" % sys.argv[1]
        sys.exit(0)

    except Exception, e:
        pass

print "Failed to autodetect the slice size"
