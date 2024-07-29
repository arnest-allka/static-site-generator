def markdown_to_blocks(markdown):
    new_blocks = markdown.split("\n\n")
    new_blocks = [block.strip() for block in new_blocks]
    new_blocks = [block for block in new_blocks if block]
    return new_blocks