import requests


def download_file(url, local_filename):
    """
    Taken from here
    NOTE the stream=True parameter
    https://stackoverflow.com/questions/16694907/how-to-download-large-file-in-python-with-requests-py/16696317#16696317
    :param url:
    :param local_filename:
    :return:
    """
    r = requests.get(url, stream=True)
    if r.ok:
        with open(local_filename, "wb") as f:
            for chunk in r.iter_content(chunk_size=1024):
                if chunk:  # filter out keep-alive new chunks
                    f.write(chunk)
                    #  f.flush() commented by recommendation from J.F.Sebastian
        return local_filename
    else:
        return None
