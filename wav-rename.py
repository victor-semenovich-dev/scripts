import argparse
import os
import codecs

argParser = argparse.ArgumentParser(
    description='Переименовать аудиозаписи служений. Сбросить дату создания и изменения файлов.'
)
argParser.add_argument(
    '-s', '--source',
    help='Исходный каталог',
    default='.',
)

args = argParser.parse_args()
sourceDir = args.source
mappingFileName = 'mapping.txt'

def process(sourceFile, mappingFile):
    mappingFile.write(f"{sourceFile} -> skip\n")
    return False

# validate arguments
if not os.path.isdir(sourceDir):
    print(f"Исходный каталог '{sourceDir}' не существует")
    exit(1)

fileList = [f for f in os.listdir(sourceDir) if os.path.isfile(f"{sourceDir}/{f}")]
with codecs.open(f"{sourceDir}/{mappingFileName}", "w", "utf-8") as mappingFile:
    for file in fileList:
        result = process(file, mappingFile)
        print(f"process '{file}': {result}")
