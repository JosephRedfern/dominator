import json
import cv2
import os.path
import numpy as np


def test_dominos(json_filename, test_function):
    """
    Function read in the JSON 'A.json', run the test function on 'A.jpg' and
    testing if the returned result matches up with the expected value.

    """
    base, ext = os.path.splitext(json_filename)

    jpg_filename = base+'.jpg'
    test_dict = {}

    result_dict = {}

    try:
        image = cv2.imread(jpg_filename)
        test_dict = test_function(image)

    except:
        # Just pass the error on for now, no meanigful action to be made here.
        raise

    with open(json_filename, 'r') as json_file:
        gt_dict = json.load(json_file)
        for key in test_dict:
            if type(gt_dict[key]) is list:
                ## Make all lists sets to make position irrelevant
                a = set(gt_dict[key])
                b = set(test_dict[key])

            elif type(gt_dict[key]) is str:
                ## if its a type string, check if its a file
                if os.path.exists(gt_dict[key]):
                    path, ext = os.path.splitext(gt_dict[key])
                    if ext == '.npy':
                        a = np.load(gt_dict[key])
                        b = np.load(test_dict[key])

            else:
                a = gt_dict[key]
                b = test_dict[key]

            ## See the result of the comparison
            comp = a == b
            result_dict[key] = comp

    return result_dict


def dummy_function(image):
    return { 'scores' : True, 'end_val': 16, 'end_values': [2, 3, 4]}


if __name__ == '__main__':
    r = test_dominos('/home/c1114016/Documents/dominos/dominator/data/IMG_4229.json' , dummy_function)
    print(r)
