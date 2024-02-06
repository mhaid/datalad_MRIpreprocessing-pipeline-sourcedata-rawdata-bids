import os
import subprocess

# Execution has to be done in root folder of subdataset (not root folder of project)!
# In this example it has to be run from "data_bids" folder


def execute(cmd):
    popen = subprocess.Popen(cmd, stdout=subprocess.PIPE, universal_newlines=True)
    for line in popen.stdout: print(line, end='')
    popen.stdout.close()
    return_code = popen.wait()
    if return_code:
        raise subprocess.CalledProcessError(return_code, cmd)


ROOTPATH = os.path.join(os.getcwd(), "sourcedata/rawdata-dicom")
print("Root: " + ROOTPATH)

# Loop trough all elements in DICOM-dir
for dir in os.listdir( ROOTPATH ):
    
    # Decode byte-string to utf-8 string
    dirname = dir
    dirpath = os.path.join(ROOTPATH, dirname)

    # check if name belongs to a directory
    if os.path.isdir( dirpath ):

        # do for all folders, except they are "dot-hidden"
        # assumes there are only subject folders in dir "data-dicom"
        if not dirname.startswith('.'):
            print("Subject found: " + dirname)

            # Loop trough all elements in Subject dir
            for subdir in os.listdir( dirpath ):
                
                subdirname = subdir
                subdirpath = os.path.join(ROOTPATH, dirname, subdirname)
                
                # check if name belongs to a directory
                if os.path.isdir( subdirpath ):
            
                    # do for all folders, except they are "dot-hidden"
                    # assumes there are only session folders in subdir
                    if not subdirname.startswith('.'):
                        print("    Session found: " + subdirname)

                        script = 'datalad containers-run --container-name heudiconv -- -d /tmp/sourcedata/rawdata-dicom/{{subject}}/{{session}}/*/DICOM/*.dcm -s ' + dirname + ' --ses ' + subdirname + ' -f /tmp/code/converter.py -c dcm2niix -b -o /tmp/'

                        # run HeuDiConv command
                        print("    Running script: " + script)
                        execute(script.split())