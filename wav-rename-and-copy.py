import argparse
import os
import datetime
import shutil
from win32_setctime import setctime

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
wavFilePathList = [f for f in fileList if f.endswith(".wav")]
if len(wavFilePathList) == 0:
    print("Отсутствуют .wav файлы в исходном каталоге")
    exit(1)
if len(wavFilePathList) > 1:
    print(f"Найдено несколько .wav файлов в исходном каталоге: {wavFilePathList}. Для выполнения скрипта необходимо наличие только одного файла.")
    exit(1)
sourceFilePath = wavFilePathList[0]
print(f"Обработка файла {sourceFilePath}")

# rename and move the file
currentDate = datetime.datetime.now()
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
newSourceFilePath = f"{sourceDir}/{newFileName}"
print(f"Переименование исходного файла: {newSourceFilePath}")
os.rename(sourceFilePath, newSourceFilePath)

if sourceDir == destDir:
    # reset create/modify date
    print("Сброс даты создания и изменения файла.")
    timestamp = currentDate.timestamp()
    os.utime(newSourceFilePath, (timestamp, timestamp))
    setctime(newSourceFilePath, timestamp)
else:
    targetFilePath = f"{destDir}/{newFileName}"
    if os.path.isfile(targetFilePath):
        print(f"Файл {targetFilePath} уже существует. Копирование невозможно.")
        exit(1)
    print(f"Копирование в каталог {targetFilePath}. Пожалуйста, подождите...")
    shutil.copy(newSourceFilePath, targetFilePath)
    print("Копирование завершено")
    print("Удаление исходного файла. Пожалуйста, подождите...")
    os.remove(newSourceFilePath)

print("Обработка завершена")
