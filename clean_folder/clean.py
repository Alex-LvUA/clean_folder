import sys
import shutil
import os
"""
програма запускається з командної строки  
>python sort.py "E:/proba/"(Шлях до папки, яку треба відсортувати) 
--a ="шлях до теки з якою працюємо"

"""


LIST_TEK=("archives", "video", "audio", "documents", "images")
LIST_TYPE={"archives":('ZIP', 'GZ', 'TAR'),
           "video":('AVI', 'MP4', 'MOV', 'MKV'),
           "audio":('MP3', 'OGG', 'WAV', 'AMR'),
           "images":('JPEG', 'PNG', 'JPG', 'SVG'),
           "documents":('DOC', 'DOCX', 'TXT', 'PDF', '.LSX', 'PPTX')
           }
CYRILLIC_SYMBOLS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ"

TRANSLATION = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
               "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "ya", "je", "i", "ji", "g")

TRANS = {}
for s in CYRILLIC_SYMBOLS:
       TRANS[ord(s.upper())]=TRANSLATION[CYRILLIC_SYMBOLS.index(s)].upper()
       TRANS[ord(s)] = TRANSLATION[CYRILLIC_SYMBOLS.index(s)]

#teka="E:/proba/"

other_files=[]
archives_files=[]
video_files=[]
audio_files=[]
documents_files=[]
images_files=[]
exist_extension= set()
new_extension= set()
list_del=[]

def normalize(str):
    return str.translate(TRANS)

def list_dir(path):
   dir = os.listdir(path)
   for el_dir in dir:
        if os.path.isfile(path+el_dir):
            if el_dir.find(".")<0:  #  файл без розширення
                extension=None
                el_norm = normalize(el_dir)
                os.rename(path + el_dir, path + el_norm)
                other_files.append([path, el_norm])
                new_extension.add(extension)
                continue
            else:
                extension=el_dir.split('.')[-1]
                el_norm = normalize(el_dir[:-len(extension)])+extension
                os.rename(path + el_dir, path + el_norm)
            try :
                if extension.upper() in LIST_TYPE["images"]:
                    images_files.append([path,el_norm])
                    exist_extension.add(extension)
                elif extension.upper()in LIST_TYPE["documents"]:
                    documents_files.append([path,el_norm])
                    exist_extension.add(extension)
                elif extension.upper() in LIST_TYPE["video"]:
                    video_files.append([path,el_norm])
                    exist_extension.add(extension)
                elif extension.upper() in LIST_TYPE["audio"]:
                    audio_files.append([path,el_norm])
                    exist_extension.add(extension)
                elif extension.upper() in LIST_TYPE["archives"]:
                    archives_files.append([path,el_norm,'.'+extension])
                    exist_extension.add(extension)
                else:
                    other_files.append([path,el_norm])
                    new_extension.add(extension)
            except Exception:                               # Якщо розширення не латиниця
                other_files.append([path, el_norm])
                new_extension.add(extension)
        elif os.path.isdir(path+el_dir):
            el_norm = normalize(el_dir)
            os.rename(path + el_dir, path + el_norm)
            print(f'{el_dir}   {el_norm}')
            if el_norm not in LIST_TEK and len(os.listdir(path+el_norm+'/'))>0: # перевіряєм чи папка зарезервована і чи не пуста
                print(path+el_norm+'/')
                list_dir(path+el_norm+'/')
def move_files(teka,files):
     for file in files:
         if not os.path.isfile(teka+'/'+file[1]):
             shutil.move(file[0]+file[1],teka)
         else:
             answ=input(f"Файл {file[1]}  вже існує в папці {teka} замінити? Y/N :")
             if answ=="Y" or answ=="y":
                 os.remove(teka+'/'+file[1])
                 shutil.move(file[0] + file[1], teka)


def extract_files(teka,files):
    for file in files:
         new_folder = file[1][:-len(file[2])]
         try:
             os.mkdir(teka + new_folder)
             shutil.unpack_archive(file[0] + file[1], teka + new_folder)
             os.remove(file[0] + file[1])
         except FileExistsError:
             None
         dir = os.listdir(teka + new_folder)
         for el_dir in dir:
             el_norm = normalize(el_dir)
             os.rename(teka + new_folder+'/'+ el_dir, teka + new_folder+'/'+ el_norm)

def read_me(teka,text='-'):
    file_read_me_name=teka+"read_me.txt"
    with open(file_read_me_name,'w') as frm:
        frm.write(text)
def list_files(listf):
    result=''
    for l in listf:
        result+=l[0]+l[1]+',\n'
    result=result[:-2]
    result += '.\n'
    return result

def delete_empty_dir(path):
    dir = os.listdir(path)
    for el_dir in dir:
        if os.path.isfile(path + el_dir):
            None
        else:
            if os.path.isdir(path + el_dir):
                if len(os.listdir(path + el_dir)) == 0:
                    print("**********" + str(el_dir))
                    try:
                        os.rmdir(path + el_dir)
                        list_del.append([path, el_dir])
                    except PermissionError:
                        print(f'Неможливо видалити папку {path + el_dir}')
                else:
                    delete_empty_dir(path + el_dir +'/')

    return list_del

def main(teka):
    if os.path.isdir(teka):
        list_dir(teka) # шукає всі файли в папці і підпапках, сортує їх по типу
        move_files(str(teka)+"images",images_files)
        move_files(str(teka)+"documents", documents_files)
        move_files(str(teka)+"audio", audio_files)
        move_files(str(teka) +"video", video_files)
        extract_files(str(teka) + "archives"+'/', archives_files)

    print(f"знайдені розширення: {exist_extension} \nнові розирення: {new_extension}")
    print(other_files)
    print(images_files)
    print(documents_files)
    print(video_files)
    print(audio_files)
    print(archives_files)

    text=f"знайдені розширення: {exist_extension} \n\nнові розширення: {new_extension}\n\n"
    text+=(f'перенесено в папку "images":\n{list_files(images_files)}\n')
    text+=(f'перенесено в папку "video":\n{list_files(video_files)}\n')
    text+=(f'перенесено в папку "documents":\n{list_files(documents_files)}\n')
    text+=(f'перенесено в папку "audio":\n{list_files(audio_files)}\n')
    text+=(f"об'єкти, залишені в поточній папці:\n{list_files(other_files)}\n")
    text+=(f'розархівовані в папку "archives":\n{list_files(archives_files)}\n')
    text+=(f'були видалені пусті папки:\n{list_files(delete_empty_dir(teka))}\n')
    read_me(teka, text)

def start():
    try:
        print("+++++++++=+++" + sys.argv[1])
        main(sys.argv[1])  #
    except IndexError:
        print(" Не вказано шлях до папки")

if __name__ == "__main__":
    #args = createParser().parse_args()python sort.py
    try:
        main(sys.argv[1]) #

    except IndexError:
        print(" Не вказано шлях до папки")
