import glob
import json

def modify_json(input_file_path, strings_to_check, output_file_path):
    """
    Reads a JSON file, removes `retrieved_context` entries if they match strings in `strings_to_check`,
    and writes the modified content to a new file.

    Parameters:
        input_file_path (str): Path to the input JSON file.
        strings_to_check (list[str]): List of strings to check against `retrieved_context`.
        output_file_path (str): Path to save the modified JSON file.
    
    Returns:
        list[int]: List of ids whose `retrieved_context` is modified.
    """
    
    with open(input_file_path, 'r') as fr:
        data = json.load(fr)
        fr.close()

    modified_query_ids_with_num = {}
    
    for i in range(0, 11):
        modified_query_ids_with_num[i] = []
    
    for id, item in enumerate(data):
        # Filter out retrieved_context elements that are in strings_to_check
        new_retrieved_context = []
        num = 0
        for context in item['retrieved_context']:
            if context not in strings_to_check:
                new_retrieved_context.append(context)
            else:
                num += 1
        if id not in modified_query_ids_with_num[num]:
            modified_query_ids_with_num[num].append(id)
        item['retrieved_context'] = new_retrieved_context

    with open(output_file_path, 'w') as fw:
        json.dump(data, fw, indent=4)
        fw.close()
    
    return modified_query_ids_with_num


strings_to_check = []

reference_dir = "reference_paper/"
file_names = glob.glob(reference_dir + "*.txt")
for file_name in file_names:
    with open(file_name, 'r', encoding='utf-8') as fr:
        content = fr.read()
        paragraphs = content.split("\n")

        for paragraph in paragraphs:
            if len(paragraph) > 0:
                strings_to_check.append(paragraph)

        fr.close()
'''
keyword_file = "keywords.txt"
with open(keyword_file, 'r') as fr:
    content = fr.read()
    paragraphs = content.split("\n")
    for paragraph in paragraphs:
        if len(paragraph) > 0:
            strings_to_check.append(paragraph)
'''
input_file = "input_dir/9907_RR100_nFT_Llama32_1000Q_k10.json"
output_file = "output_dir/9907_RR100_nFT_Llama32_1000Q_k10_noReference.json"


if __name__ == "__main__":
    modified_query_ids_with_num = modify_json(input_file, strings_to_check, output_file)
    print(modified_query_ids_with_num)
    for num in modified_query_ids_with_num:
        print(len(modified_query_ids_with_num[num]))
