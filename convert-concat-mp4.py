# concatenate all videos from the src dir
import os
import shutil

src_dir_name = "src"
tmp_dir_name = "tmp"
list_file_name = "list.txt"
output_file_name = "output.mp4"

# clear the file
list_file = open(list_file_name, "w")
list_file.close()

os.system("chcp 65001 > nul")

# Before concatenation we need to convert all videos to the same format
for (dir_path, dir_names, file_names) in os.walk(os.getcwd() + "\\" + src_dir_name):
    for file_name in file_names:
        source_file = dir_path + "\\" + file_name
        processed_file = tmp_dir_name + "\\" + file_name
        
        # The -y parameter replaces all existing files without any questions
        # Assumed that all files have the same width
        ffmpeg_command = 'ffmpeg -y -i "{}" -r 24 -vcodec h264 -acodec aac -strict experimental "{}"'.format(source_file, processed_file)
        
        if not os.path.exists(tmp_dir_name):
            os.makedirs(tmp_dir_name)
        os.system(ffmpeg_command)
        
        list_file = open(list_file_name, "a")
        list_file.write("file '{}'\n".format(processed_file))
        list_file.close()
os.system('ffmpeg -f concat -safe 0 -i "{}" -c copy "{}"'.format(list_file_name, output_file_name))

shutil.rmtree(tmp_dir_name)
os.remove(list_file_name)
