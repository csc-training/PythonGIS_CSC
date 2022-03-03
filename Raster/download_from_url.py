import os
import urllib

def get_filename(url):
    """
    Parses filename from given url
    """
    if url.find('/'):
        return url.rsplit('/', 1)[1]

def download_data(url_list):
    # Filepaths
    outdir = r"data"



    # Create folder if it does not exist
    if not os.path.exists(outdir):
        os.makedirs(outdir)

    # Download files
    for url in url_list:
        # Parse filename
        fname = get_filename(url)
        outfp = os.path.join(outdir, fname)
        # Download the file if it does not exist already
        if not os.path.exists(outfp):
            print("Downloading", fname)
            r = urllib.request.urlretrieve(url, outfp)

