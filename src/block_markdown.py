import re


def markdown_to_blocks(markdown):
    new_blocks = markdown.split("\n\n")
    new_blocks = [block.strip() for block in new_blocks]
    new_blocks = [block for block in new_blocks if block]
    return new_blocks

def block_to_block_type(block):
    heading = re.findall(r'^(#{1,6})\s+(.*)', block)
    
    if heading:
        return 'heading'
    elif block[:3] == '```' and block[len(block)-3:] == '```': 
        return 'code'
    else:
        count = 0
        block_type = ''
        lines = block.split('\n')
        for i, line in enumerate(lines):
            if line[0] == '>':
                block_type = 'quote'
                count += 1
            elif line[:2] == '* ' or line[:2] == '- ':
                block_type = 'unordered_list'
                count += 1
            elif line[:3] == f"{i+1}. ":
                block_type = 'ordered_list'
                count += 1
        if count == len(lines):
            return block_type
        else:
            return 'paragraph'

markdown_string = """
###### This is a heading
## This is a heading

```
this is code
```

> this is a quote
> this is a quote
> this is a quote
> this is a quote

This is a paragraph of text. It has some **bold** and *italic* words inside of it.

* This is the first list item in a list block
* This is a list item
* This is another list item

1. one
2. two
3. three
"""
blocks = markdown_to_blocks(markdown_string)

for block in blocks:
    print(block_to_block_type(block))