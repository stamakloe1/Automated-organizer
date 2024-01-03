import os
import time
import shutil
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from plyer import notification

#create a class 
class FileOrganizer:
    def __init_(self):
        self.user_profile = os.path.expanduser("~")
        self.system_directories = ['Desktop', 'Documents', 'Downloads', 'Music', 'Pictures', 'Videos']
        self.onedrive_directories = os.path.join(self.user_profile, 'OneDrive')

        #======================================================================================================================================
        #join profile and put it in a one-line linear loop
        self.source_directories = [os.path.join(self.user_profile, dir) for die in self.system_directories] + [self.onedrive_directories]

        #------------------------------------------------------------------------------------------------------------------------------------------
        #create a dictionary distnation directories and join the profile
        self.dest_direct = {
            'docs': os.path.join(self.user_profile, 'Documents'),
            'images': os.path.join(self.user_profile, 'Pictures'),
            'music': os.path.join(self.user_profile, 'Music'),
            'video': os.path.join(self.user_profile, 'Videos'),
            'myzp': os.path.join(self.user_profile, 'Downloads'),
            'executable': os.path.join(self.user_profile, 'Downloads', 'Executables'),
            'onedrive': os.path.join(self.user_profile, 'OneDrive', 'Organized_files') #adding one drive to the destination directories
        }

        #---------------------------------------------------------------------------------------------------------------------------------------------
        #create dictionary for subdirectories
        self.subdirs = {
                'docs': {'Word': ['docx', 'txt'], 'Pdf': ['pdf'], 'Excel': ['xlsx', 'csv'], 'Power Point': ['pptx']},
                'executable': {'Setup': ['dmg', 'exe', 'deb', 'pkg', 'msi', 'whl'], 'Iso': ['iso']},
                'myzp': {'Zip_Files': ["zip", "rar", "cpgz", "gz", "xz", "bz2"]},
                'images': {'Photo': ['jpg', 'jpeg', 'png', 'gif', 'bmp', 'tiff'], 'Photoshop': ['psd']},
                'video': {'Video': ['avi', 'flv', 'wmv', 'mov', 'mp4', 'mkv']},
                'audio': {'Musics': ["aac", "aa", "dvf", "m4a", "m4b", "mp3", ".msv", "ogg", "oga", ".raw", "vox", "wav", "wma"]}
            }
        
        #----------------------------------------------------------------------------------------------------------------------------------------------
        #function to check if the giving path is a user created diretory within a system directories
        def is_user_created_directory(self, path):
            return os.path.isdir(path) and os.path.basename(path) not in self.system_directories
        
        def Organized_files(self, path):
            for src_dir in self.source_directories:
                for root, dirs, files in os.walk(src_dir):
                    #ignore user created directories within system directories
                    dir[:] = [my_dir for my_dir in dirs if not self.is_user_created_directory(os.path.join (root, my_dir))]

                    for file in files:
                        file_extenion = file.split('.')[-1]
                        for file_type, extensions in self.subdirs.items():
                            for subdir, ext_list in extensions.items():
                                if file_extenion in ext_list:
                                    dest_dir = os.path.join(self.dest_directories[file_type], subdir)
                                    break
                            else:
                                continue
                            break
                        else:
                            continue

                        source_file_path = os.path.join(root, file)
                        dest_file_path = os.path.join(dest_dir, file)

                        os.makedirs(dest_dir, exist_ok=True)

                        # Retry mechanism to handle file in use
                        max_retries = 5
                        retry_count = 0
                        while retry_count < max_retries:
                            try:
                                shutil.move(source_file_path, dest_file_path)
                                self.notify(f"Moved {file} to {dest_dir}")
                                break  # Break out of the retry loop if successful
                            except (shutil.Error, FileNotFoundError, PermissionError) as e:
                                retry_count += 1
                                if retry_count < max_retries:
                                    time.sleep(1)  # Wait for 1 second before retrying
                                else:
                                    self.notify(f"Error moving {file}: {e}")

    #-----------------------------------------------------------------------------------------------------------------------------------------------------------------------
    #function for notifyer 
    def notify(self, message):
        notification.notify(
            title='File Organizer',
            message=message,
            app_name='File Organizer'
        )


class FileHandler(FileSystemEventHandler):
    def __init__(self, file_organizer):
        self.file_organizer = file_organizer

    def on_modified(self, event):
        if event.is_directory:
            return
        self.file_organizer.organize_files()


if __name__ == "__main__":
    file_organizer = FileOrganizer()

    # Initial organization
    file_organizer.organize_files()

    # Set up the observer
    observer = Observer()
    event_handler = FileHandler(file_organizer)
    for src_dir in file_organizer.source_directories:
        observer.schedule(event_handler, src_dir, recursive=True)

    # Start the observer
    observer.start()

    try:
        while True:
            pass
    except KeyboardInterrupt:
        observer.stop()

    observer.join()


    


