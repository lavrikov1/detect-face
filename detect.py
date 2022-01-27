import os
import re
import sys
import numpy
import sqlite3
import face_recognition

red = "\033[1;31m"
gr = "\033[1;32m"
cy = "\033[1;36m"
ff = "\033[0;35m"

def check_new_model():
    checking = str(input("Обновить базу? (1-Да / 2-Нет): "))
    if checking == 1:
        print("Поиск новых моделей в каталоге! ...")

        directory = 'img'
        files = os.listdir(directory)

        # Проверка наличия в каталоге новых лиц
        # если найденно новое лицо - помещаем его в базу (для быстрого поиска в будущем)
        for row in files:
            if re.search(".jpg", row) or re.search(".jpeg", row):
                # /--=-- DataBase SQLite3 --=--\
                connect = sqlite3.connect("box.db")
                cursor = connect.cursor()

                link_name = cursor.execute(f"SELECT namefile FROM link WHERE namefile='{row}'").fetchone()
                if link_name == None:  # Если нового лица нет в базе
                    img2 = face_recognition.load_image_file(f"{directory}/{row}")  # Берём фотографию
                    img2_encodings = face_recognition.face_encodings(img2)[0]  # Извлечение параметров лица
                    fatures_face = numpy.ndarray.dumps(img2_encodings)  # Маринуем параметры лица в строку

                    # /--=--=-- Добавляем лицо в базу --=--=--\
                    sq_insert_query = """INSERT INTO link (np, namefile) VALUES (?, ?);"""
                    data_tuple = (fatures_face, row)  # Масив + имя фотографии
                    cursor.execute(sq_insert_query, data_tuple)
                    print(f"[+] новая актриса: {row}")

                    """
                    cursor.execute(f"SELECT np FROM link")
                    data = cursor.fetchone()[0]
                    data1 = numpy.loads(data)   # Восстанавливаем параметры лица
                    """

                    connect.commit()
                    cursor.close()
        print("Готово!\nПриступаю к поиску ...")
    elif checking == 2:
        pass



def face_rec():
    face_img = face_recognition.load_image_file('img/anjelina.jpeg')
    face_location = face_recognition.face_locations(face_img)

def compare_faces(img1_path, img2_path, woman):
    # /--=-- DataBase SQLite3 --=--\
    connect = sqlite3.connect("box.db")
    cursor = connect.cursor()

    result = face_recognition.compare_faces([img1_path], img2_path)

    global numx
    numx += 1
    if result[0] == False:
        # print(f"{cy}[{numx} - {numall}]  {red}{result} - {img2_path}{ff}")
        pass
    if result[0]:
        # print(f"{cy}[{numx} - {numall}]  {gr}{result} - {img2_path}{ff}")
        #x = cursor.execute(f"SELECT namefile FROM link WHERE np={model}").fetchone()
        os.system(f'open img/{woman}')


def main():
    # /--=-- DataBase SQLite3 --=--\
    connect = sqlite3.connect("box.db")
    cursor = connect.cursor()

    img1 = face_recognition.load_image_file(sys.argv[1])
    goal = face_recognition.face_encodings(img1)[0]


    directory = 'img'
    files = os.listdir(directory)

    global numx
    numx = 0
    global numall
    numall = len(files)


    all_model = cursor.execute("SELECT * FROM link").fetchall()
    for model in all_model:
        woman_name = model[1]
        model_clear = numpy.loads(model[0])
        compare_faces(goal, model_clear, woman_name)

if __name__ == '__main__':
    check_new_model()
    main()
