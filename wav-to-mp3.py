import argparse
import os

argParser = argparse.ArgumentParser(
    description='Process .wav files from the current directory and convert them to .mp3. '
                'The processing includes audio normalizing and removing of pauses.'
)
argParser.add_argument(
    '-r', '--reverse',
    help='Defines, if the alphabetical sorting order should be reversed. False by default.',
    action=argparse.BooleanOptionalAction,
    default=False,
)
argParser.add_argument(
    '-s', '--start',
    help='The first file for processing (inclusively) according to the sorting order. '
         'By default, the first file in the directory.'
)
argParser.add_argument(
    '-e', '--end',
    help='The last file for processing exclusively. '
         'If not specified, process all files in the directory from the --start.'
)
args = argParser.parse_args()

# To support cyrillic on Windows
# os.system("chcp 65001 > nul")

if not os.path.exists("converted"):
    os.makedirs("converted")

file_names = os.listdir(os.getcwd())
file_names = filter(lambda file_name: file_name.endswith('.wav'), file_names)
file_names = sorted(file_names, reverse=args.reverse)

start_index = 0
if args.start is not None:
    try:
        start_index = file_names.index(args.start)
    except ValueError:
        print('The file "{}" is not found or not a .wav'.format(args.start))

end_index = len(file_names)
if args.end is not None:
    try:
        end_index = file_names.index(args.end)
    except ValueError:
        print('The file "{}" is not found or not a .wav'.format(args.end))

file_names = file_names[start_index:end_index]
print('Start script: {} files'.format(len(file_names)))
for idx, src_file in enumerate(file_names):
    print('-------------------------------------------------------------------------------')
    print('{} ({}/{})'.format(src_file, idx + 1, len(file_names)))
    dest_file = "converted/" + src_file.replace("wav", "mp3")
    convert_command = 'ffmpeg -y -i "{}" -b:a 128k -af silenceremove=stop_periods=-1:' \
                      'stop_duration=5:stop_threshold=-50dB,dynaudnorm "{}"'\
        .format(src_file, dest_file)
    os.system(convert_command)
 