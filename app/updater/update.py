import board
import sys
import json
import shutil
import os
import hashlib
import psutil
import tarfile
import subprocess



BASE=os.path.expanduser('~')+"/projects/app/"

LATEST_VERSION="2.0.0"
APP_NAME="hello_log_app"
APP_PATH=os.path.join(BASE,"usr/bin")
UPDATE_NAME=APP_NAME+"-"+LATEST_VERSION
TAR_SRC=os.path.join(BASE,"updater/"+UPDATE_NAME+".tar")
TAR_DEST=BASE+"app_update/"+UPDATE_NAME+".tar"
TAR_MD5="c8d4f61a0e2b0c9ad3554986fcaea70f"
BACKUP_DIR=BASE+"backup"

BACKUP_DIR_LIST=[BASE+'config',BASE+'log'] #absolute path
BACKUP_FILE_LIST=[]


command = [sys.executable, APP_PATH+"/"+APP_NAME+".py"]



with open(BASE+'data/board_data.json', 'r') as file:
     board_data = json.load(file, object_hook=board.board_decoder)  
     

def isUpgradable():
        return board_data.version < LATEST_VERSION

def downloadUpdate():
    #check the any partial files if then remove
    if os.path.isfile(TAR_DEST):
        os.remove(TAR_DEST)
        print("Partial file found and deleted")

    #copy new tar into a /tmp
    print("Downloading file.....")
    shutil.copy(TAR_SRC,TAR_DEST)
    print("Download completed")


def chkFileIntegrity():
    print("Checking file integrity...")
    with open(TAR_DEST, 'rb') as file_obj:
        file_contents = file_obj.read()
        md5_hash = hashlib.md5(file_contents).hexdigest()

    print(md5_hash)

    return md5_hash==TAR_MD5


def kill_process_by_name(process_name):
    """Kill a process by its name or command line arguments."""
    for process in psutil.process_iter(['pid', 'name', 'cmdline']):
        # Check if the process name or command line matches the target process
        #print(process.info['cmdline'])
        if process.info['cmdline'] and len(process.info['cmdline'])>1 and process_name in process.info['cmdline'][1]:
            print(f"Killing process {process_name} with PID {process.info['pid']}")
            process.kill()
            return
    print("App is not running")
        


def backupDir():

    print("Start backup")
    for directory in BACKUP_DIR_LIST:
        if os.path.isdir(directory):
            dest_dir = os.path.join(BACKUP_DIR, os.path.basename(directory))
            try:
                shutil.copytree(directory, dest_dir, dirs_exist_ok=True)
                print(f"{directory} backup successfully.")
            except Exception as e:
                print(f"Failed to backup {directory}: {e}")
        else:
            try:
                shutil.copy2(directory, BACKUP_DIR)
                print(f"{directory} copied successfully.")
            except Exception as e:
                print(f"Failed to copy {directory}: {e}")

    print("Backup completed")



def restoreDir():

    print("Starting to restore the backups")

    try:
        shutil.copytree(BACKUP_DIR, BASE, dirs_exist_ok=True)
        print("Restoration completed")
        shutil.rmtree(BACKUP_DIR)
    except Exception as e:
        print("Restoration failed")
    

    

    
def unTarTheApp():
    with tarfile.open(TAR_DEST, 'r') as tar:
    # Extract all contents of the tar file to the specified directory
        tar.extractall(path=BASE)


def main():


   
   #Check the version and find is it need to upgraded
    if(isUpgradable()):
        print("Update available")
    else:
        print("Your version is already upto date")
        sys.exit(0)
   
    print("Start upgrading.....")

    #Download the update into a directory
    downloadUpdate()

    
    if(chkFileIntegrity()):
        print("Integrity check completed sucessfully")
    else:
        print("Integrity error")
    

    
    #kill the process    
    kill_process_by_name("hello_log_app.py")
   
    
    #backup the config and log

    backupDir()
   

    unTarTheApp() 
    #copy the new app into location
    
    sys.exit(1)

    restoreDir()   
    #restore the backuped files
    


    #run the app
    subprocess.Popen(["python", "program_2.py"])
    sys.exit(0)  








    






         
    

    



        
    






if __name__ == "__main__":
    main()

        
