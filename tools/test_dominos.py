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
    result_dict = { 'test_commit ' : 1 , 'function_name' : test_function.__qualname__}
    result_sub_dict = {}

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
            result_sub_dict[key] = comp

    result_dict['test_results'] = result_sub_dict

    return result_dict


def dummy_function(image):
    return { 'scores_bool' : True, 'end_val_num': 16, 'end_values_set': [2, 3, 4]}


def test_pretty_print(results_dict):
    """

    Pretty printing for the results of the dictionary, addig in types for the various
    results types, made useful to store this as part of the dictionary keys, to help
    reduce the number of special cases.

    """
    #Print pre able
    intro_str = "Results of test function '" +  results_dict["function_name"] + "'\n"
    result_str =  ""

    test_results = results_dict["test_results"]
    for key in test_results:
        #Append formated results string depending on the different attributes of the keys
        result_str += "Results of '" + key + "' : "
        if key.endswith("_bool"):
            if test_results[key]:
                result_str +=  "PASS\n"
            else:
                result_str += "FAIL\n"

        elif key.endswith("_num"):
            if test_results[key]:
                result_str += "PASS\n"
            else:
                result_str += "FAIL\n"

        elif key.endswith("_set"):
            if test_results[key]:
                result_str += "PASS\n"
            else:
                result_str += "FAIL\n"

        elif key.endswith("_nparray"):
            #Sum the over the true false array to get a percentage the correct
            count = 0
            r_array = test_results[key]
            for el in r_array:
                if el:
                    count += 0

            percentage  = count / len(r_array)
            result_str += str(precentage) + "%\n"

        else:
            result_str += "\n"
            pass

    print(intro_str)
    print(result_str)

if __name__ == '__main__':
    r = test_dominos('../data/IMG_4229.json' , dummy_function)
    test_pretty_print(r)
