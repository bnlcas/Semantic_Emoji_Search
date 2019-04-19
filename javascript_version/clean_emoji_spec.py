# Edit Emoji Text
root_directory = '/Users/benlucas/Documents/Semantic_Emoji_Search/'
emoji_data_file = root_directory + 'emoji-test.txt'
emoji_data_cleaned_file = root_directory + 'emoji_text_cleaned.txt'

with open(emoji_data_file, 'r') as f:
    raw_txt_data = f.readlines()

raw_emoji_data = [x for x in raw_txt_data if(x[0] != '\n' and x[0] != '#')]
unicode_rep = []
hexidecimal_rep = []
description = []

cleaned_emoji_data = []
for row in raw_emoji_data:
    sections = row.split(';')
    if(len(sections) > 1):
        description_sections = sections[1].split('#')
        if(len(description_sections) > 1):
            if('non-fully-qualified' not in description_sections[0] and ':' not in description_sections[1]):
                cleaned_emoji_data.append(row)


with open(emoji_data_cleaned_file, 'w') as f:
    for row in cleaned_emoji_data:
        f.write(row)
