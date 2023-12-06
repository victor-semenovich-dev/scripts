import os

os.system("chcp 65001 > nul")

if not os.path.exists("converted"):
    os.makedirs("converted")

file_names = sorted(os.listdir(os.getcwd()), reverse=True)
for src_file in file_names:
    if src_file.endswith(".wav"):
        print(src_file)
        dest_file = "converted/" + src_file.replace("wav", "mp3")
        convert_command = 'ffmpeg -y -i "{}" -b:a 128k -af silenceremove=stop_periods=-1:stop_duration=5:stop_threshold=-50dB,dynaudnorm "{}"'.format(src_file, dest_file)
        os.system(convert_command)
 