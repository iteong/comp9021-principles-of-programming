# Extracts titles from a front page of the Sydney Morning Herald.
#
# Written by Eric Martin for COMP9021

import re


def extract_text(line, pattern):
    extracted_text = pattern.search(line)
    if extracted_text:
        title = extracted_text.groups()[0]
        print(title.replace('&nbsp;', ''))

# We look for text of the form title=....>TITLE</a></h3>
full_title_pattern = re.compile('title=[^>]*>([^<]*)</a></h3>')
# In some cases, </a></3> is at the beginning of the next line
title_at_end_of_line_pattern = re.compile('[^>]*>([^<]*)\n$')
end_tags_at_start_of_next_line_pattern = re.compile('^</a></h3>')

file = open('SMH.txt', 'r')
line = file.readline()
for next_line in file:
    if end_tags_at_start_of_next_line_pattern.search(next_line):
        extract_text(line, title_at_end_of_line_pattern)
    else:
        extract_text(line, full_title_pattern)
    line = next_line
# Process last line in the unique possible way
extract_text(line, full_title_pattern)
file.close()
