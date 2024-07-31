import os
import re
import shutil

def copy_directory(src, dst):
    if os.path.exists(dst):
        shutil.rmtree(dst)
    os.mkdir(dst)

    for item in os.listdir(src):
        src_path = os.path.join(src, item)
        dst_path = os.path.join(dst, item)

        if os.path.isdir(src_path):
            copy_directory(src_path, dst_path)
        else:
            shutil.copy(src_path, dst_path)
            print(f"Copied file: {src_path}")

def extract_title(markdown):
    match  = re.search(r'^#\s+(.*)', markdown, re.MULTILINE)

    if match:
        return match.group(1).strip()
    else:
        raise Exception("No h1 header found")

def main():
    source_dir = 'static'
    public_dir = 'public'
    
    copy_directory(source_dir, public_dir)
    print("Directory copy completed.")
            
if __name__ == '__main__':
    main()