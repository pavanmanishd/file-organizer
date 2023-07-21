from os import scandir,rename,mkdir
from shutil import move
from os.path import splitext,exists,join
import json

# read the directories.json file
with open("directories.json","r") as file:
    data = file.read()
    data = json.loads(data)
    watch_dir = data["watch_dir"]
    dest_dir_video = data["dest_dir_video"]
    dest_dir_image = data["dest_dir_image"]
    dest_dir_documents = data["dest_dir_documents"]
    dest_dir_audio = data["dest_dir_audio"]
    dest_dir_others = data["dest_dir_others"]

# check if directories exists
if not exists(dest_dir_video):
    mkdir(dest_dir_video)
if not exists(dest_dir_image):
    mkdir(dest_dir_image)
if not exists(dest_dir_documents):
    mkdir(dest_dir_documents)
if not exists(dest_dir_audio):
    mkdir(dest_dir_audio)
if not exists(dest_dir_others):
    mkdir(dest_dir_others)

image_extensions = [".jpg", ".jpeg", ".jpe", ".jif", ".jfif", ".jfi", ".png", ".gif", ".webp", ".tiff", ".tif", ".psd", ".raw", ".arw", ".cr2", ".nrw", ".k25", ".bmp", ".dib", ".heif", ".heic", ".ind", ".indd", ".indt", ".jp2", ".j2k", ".jpf", ".jpf", ".jpx", ".jpm", ".mj2", ".svg", ".svgz", ".ai", ".eps", ".ico"]
video_extensions = [".mkv", ".webm", ".mpg", ".mp2", ".mpeg", ".mpe", ".mpv", ".ogg", ".mp4", ".mp4v", ".m4v", ".avi", ".wmv", ".mov", ".qt", ".flv", ".swf", ".avchd"]
audio_extensions = [".m4a", ".flac", "mp3", ".wav", ".wma", ".aac"]
document_extensions = [".doc", ".docx", ".odt", ".pdf", ".xls", ".xlsx", ".ppt", ".pptx", ".odp"]

def make_unique(dest,name):
    filename, extension = splitext(name)
    count = 1
    while exists(f"{dest}/{name}"):
        name = f"{filename}({str(count)}){extension}"
        count += 1
    return name


def move_file(dest,entry,name):
    if exists(f"{dest}/{name}"):
        unique_name = make_unique(dest,name)
        oldname = join(dest,name)
        newname = join(dest,unique_name)
        rename(oldname,newname)
    move(entry,dest)

class Handler():
    def on_modified(self):
        with scandir(watch_dir) as entries:
            for entry in entries:
                name = entry.name
                checked_doc = self.check_documents(entry,name)
                checked_img = self.check_images(entry,name)
                checked_aud = self.check_audio(entry,name)
                checked_vid = self.check_videos(entry,name)
                if checked_doc == False and checked_aud == False and checked_img == False and checked_vid == False :
                    self.check_others(entry,name)

    def check_videos(self,entry,name):
        for video_extension in video_extensions:
            if name.endswith(video_extension) or name.endswith(video_extension.upper()):
                move_file(dest_dir_video,entry,name)
                return True
        return False
    def check_documents(self,entry,name):
        for document_extension in document_extensions:
            if name.endswith(document_extension) or name.endswith(document_extension.upper()):
                move_file(dest_dir_documents,entry,name)
                return True
        return False
    def check_images(self,entry,name):
        for image_extension in image_extensions:
            if name.endswith(image_extension) or name.endswith(image_extension.upper()):
                move_file(dest_dir_image,entry,name)
                return True
        return False
    def check_audio(self,entry,name):
        for audio_extension in audio_extensions:
            if name.endswith(audio_extension) or name.endswith(audio_extension.upper()):
                move_file(dest_dir_audio,entry,name)
                return True
        return False
    def check_others(self,entry,name):
        if entry.is_file():
            move_file(dest_dir_others,entry,name)



if __name__ == "__main__":
    handler = Handler()
    handler.on_modified()