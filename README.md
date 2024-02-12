# Sea Battle README
## 1. Запуск проекта из репозитория
1) Скачать репозиторий - ```git clone https://github.com/QvkkpotentialExplorer/Sea_battle-.git```
2) Перейти в папку Sea_battle- - ```cd Sea_battle-```
3) Скачать все требования - ```pip install -r requirements.txt```
4) Запустить файл app.py - ```python app.py```
## 2. Структура данных
### Схема бд
![db](images/Codeblocks/dbsystem.jpg)
## 3. Функциональные блоки
### Модуль разграничения прав
![demarcation system](images/Codeblocks/demarcation_module.jpg)
https://github.com/QvkkpotentialExplorer/Sea_battle-/blob/614fe94604ccdea180005c22a9133def1fa2c69c/blueprints/profiles/profile.py#L19-L26

### Модуль пользователя

![user module](images/Codeblocks/user_interface.jpg)
https://github.com/QvkkpotentialExplorer/Sea_battle-/blob/614fe94604ccdea180005c22a9133def1fa2c69c/blueprints/profiles/profile.py#L31-L49
https://github.com/QvkkpotentialExplorer/Sea_battle-/blob/b43dae419dbf5f0b1f3001887428663fbe8422a1/blueprints/boards/board.py#L20-L30

### Модуль игрового поля
![playfield module](images/Codeblocks/playfield_module.jpg)
https://github.com/QvkkpotentialExplorer/Sea_battle-/blob/59f155b856ed63c6a5572dada64f37a7d32ef30a/blueprints/boards/board.py#L35-L49

### Модуль выстрелов
![shoot module](images/Codeblocks/shot_module.jpg)
https://github.com/QvkkpotentialExplorer/Sea_battle-/blob/ba2bb57e30f45c35a83698779b47baa561b15d65/blueprints/api/api.py#L34-L73

### Регистрация пользователя
![user_registration_module](images/Codeblocks/user_registration.jpg)
https://github.com/QvkkpotentialExplorer/Sea_battle-/blob/c39fe7d6b9abe1ee357317054c44726cbb10a093/blueprints/auth/auth_app.py#L16-L24
https://github.com/QvkkpotentialExplorer/Sea_battle-/blob/c39fe7d6b9abe1ee357317054c44726cbb10a093/blueprints/auth/auth_app.py#L27-L37
https://github.com/QvkkpotentialExplorer/Sea_battle-/blob/c39fe7d6b9abe1ee357317054c44726cbb10a093/blueprints/auth/auth_app.py#L40-L57

### Регистрация админа
![admin_registration_module]()
https://github.com/QvkkpotentialExplorer/Sea_battle-/blob/c39fe7d6b9abe1ee357317054c44726cbb10a093/blueprints/admin/admin.py#L16-L30

## 4. Скриншоты интерфейса
### Логин
![Login interface](images/Screenshots/Login.png)
### Регистрация
![Registration](images/Screenshots/Registration.png)
### Добавление поля
![Addboard](images/6_1-usercase/2.addfield.PNG)
### Выбор поля для игры
![board_list](images/6_2-usercase/fields.PNG)
### Игровое поле
![game_room](images/6_2-usercase/field.PNG)
### Добваление приза
![add_prize](images/Screenshots/add_prize.png)
### Список призов
![prize_list](images/Screenshots/prize_list.png)
## 5. [Видео](https://www.youtube.com/) с работой
