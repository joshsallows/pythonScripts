import sys, os



def delete_line_by_condition(original_file, condition):
    """in a file, delete the lines at line number in given list"""

    dummy_file = original_file.split('.')[0]+'.bak'
    is_skipped = False

    with open(original_file, 'r') as read_obj, open(dummy_file, 'w') as write_obj:
        #line by line copy data from the original file to the dummy file
        for line in read_obj:
            #if the current line matches the given condition then skip that line
            if line.__contains__(condition) == True:
                write_obj.write(line)
            else:
                is_skipped = True

    # # if any line is skipped then rename the dummy file as original file:
    # if is_skipped:
    #     os.remove(original_file)
    #     os.rename(dummy_file, original_file)
    # else:
    #     os.remove(dummy_file)

def delete_line_with_word(filename):
    words = ["Baker", "baker", "BAKER"]
    for word in words:
        delete_line_by_condition(filename, word)
        
delete_line_with_word(sys.argv[1])