import os
import zipfile

def fix_xml(data):
    """Cleans up XML to prevent XML parsing errors"""

    #removes newline characters from reading file as one string with read()
    data = data.replace('\n', '')
    
    # sometimes console output is logged to remove everything before the first <rpc-reply> tag
    find_text = "<rpc-reply"
    k = data.rfind(find_text)
    data = data[k:]

    # removes everything after the last </rpc-reply>
    find_text = "</rpc-reply>"
    k = data.rfind(find_text)
    k += len(find_text)
    data = data[:k]

    return data


def parse_hostname_from_filename(file):
    """Parses hostname from filename"""

    # strip path
    hostname = file.split("/")[-1].split("\\")[-1]
    
    # strip extensions
    hostname = hostname.split(".")[0]

    return hostname

def process_zip(file, target_dir=None):
    """Unzips file to directory of same name and returns list of files"""

    # generate target_dir path if not already provided
    if not target_dir:
        target_dir = parse_hostname_from_filename(file)
        target_dir = os.path.join(os.getcwd(), target_dir)

    # create target_dir if it doesn't exist
    if os.path.exists(target_dir):
        raise Exception("'{0}' already exists".format(target_dir))
    else:
        os.mkdir(target_dir)

    with zipfile.ZipFile(file, 'r') as zip_ref:
        zip_ref.extractall(target_dir)

    files = [os.path.join(target_dir, f) for f in os.listdir(target_dir)]

    return files, target_dir
