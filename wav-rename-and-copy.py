import argparse
import os
import datetime

argParser = argparse.ArgumentParser(
    description='Переименовать и скопировать аудиозапись служения на сервер'
)

argParser.add_argument(
    '-s', '--source',
    help='Исходный каталог',
    default='.',
)
argParser.add_argument(
    '-d', '--dest',
    help='Целевой каталог',
    default='.',
)

args = argParser.parse_args()
sourceDir = args.source
destDir = args.dest

# validate arguments
if not os.path.isdir(sourceDir):
    print(f"Исходный каталог '{sourceDir}' не существует")
    exit(1)
if not os.path.isdir(destDir):
    print(f"Целевой каталог '{destDir}' не существует")
    exit(1)

# find a wav file
childrenList = os.listdir(sourceDir)
fileList = [f"{sourceDir}/{f}" for f in childrenList if os.path.isfile(f"{sourceDir}/{f}")]
wavFileList = [f for f in fileList if f.endswith(".wav")]
if len(wavFileList) == 0:
    print("Отсутствуют .wav файлы в исходном каталоге")
    exit(1)
if len(wavFileList) > 1:
    print(f"Найдено несколько .wav файлов в исходном каталоге: {wavFileList}. Для выполнения скрипта необходимо наличие только одного файла.")
    exit(1)
wavFile = wavFileList[0]
print(f"Обработка файла {wavFile}")

# reset create/modify date
currentDate = datetime.datetime.now()
# TODO currently works only for update time (not for create time)
print("Сброс даты создания и изменения файла")
timestamp = currentDate.timestamp()
os.utime(wavFile, (timestamp, timestamp))

# rename and move the file
year = currentDate.year
month = currentDate.month
day = currentDate.day
weekday = currentDate.weekday()
hour = currentDate.hour
weekdayNames = ["ПН", "ВТ", "СР", "ЧТ", "ПТ", "СБ", "ВС"]
formattedWeekday = weekdayNames[weekday]
dayPart = ""
if weekday == 6: # sunday
    if hour < 18:
        dayPart = " утро"
    else:
        dayPart = " вечер"
formattedDate = f"{year}{month:02d}{day:02d} {formattedWeekday}{dayPart}"
newFileName = f"{formattedDate}.wav"
print(f"Новое название файла: {newFileName}")
newFilePath = f"{destDir}/{newFileName}"
print(f"Переименование и перемещение в каталог {newFilePath}")
os.rename(wavFile, newFilePath)
print("Перемещение завершено")
