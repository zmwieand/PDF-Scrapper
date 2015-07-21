import os
import zipfile
from shutil import copyfile

def download_clicked(selected_list):
    # make a list of all file names to be downloaded
    cp_files(selected_list)
    zip_folder()
    # clean out Download/ directory
    rm_files()

def cp_files(selected_files):
    for a in selected_files:
        current = "samples/" + a
        destination = "Download/" + a
        copyfile(current, destination)

def rm_files():
    path = 'Download/'
    for a in os.listdir(path):
        os.remove(path + a)

def zip_folder():
    foo = zipfile.ZipFile('Resumes.zip', 'w')
    for root, dirs, files in os.walk('Download/'):
        for f in files:
            foo.write(os.path.join(root, f))
    foo.close()

my_list = ['ZachWieandResume.pdf']
download_clicked(my_list)
