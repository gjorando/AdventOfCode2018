#!/usr/bin/env python3

with open("input") as input_file:
    input_list = input_file.readline().replace("\n", "").split(" ")
    input_list = [int(elem) for elem in input_list]

def new_node():
    return {"children": [], "metadata": []}

def process_children(input_list, output_tree):
    """
        Computes the children of the node output_tree, using the remaining input_list, and returns the number of elements processed in the list.
    """
    
    children_count = input_list[0]
    metadata_count = input_list[1]
    
    skipped_elements = 0

    for i in range(children_count):
        curr_child = new_node()
        skipped_elements+= process_children(input_list[2+skipped_elements:], curr_child)
        output_tree["children"].append(curr_child)

    for i in range(metadata_count):
        output_tree["metadata"].append(input_list[2+skipped_elements+i])

    skipped_elements+= metadata_count+2

    return skipped_elements

def calculate_value(tree):
    """
        Calculates the value of a tree.
    """
    total = 0

    if len(tree["children"]) == 0:
        total = sum(tree["metadata"])
    else:
        for metadata in tree["metadata"]:
            index = metadata-1
            if (index >= 0) and (index < len(tree["children"])):
                total+= calculate_value(tree["children"][index])


    return total

root = new_node()

process_children(input_list, root)

result = calculate_value(root)

print("Answer for puzzle #16: {}".format(result))
