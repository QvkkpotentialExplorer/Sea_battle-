# Sea Battle README
## 1. Запуск проекта из репозитория
1) Для начала нужно [скачать](https://github.com/QvkkpotentialExplorer/Sea_battle-) репозиторий
2) Открыть редактор кода(Pycharm)
3) Открыть  файл app.py
4) Запустить данный файл
## 2. Структура данных
*Схема бд*
## 3. Функциональные блоки
|Модуль разграничения прав|
![demarcation system](images/Codeblocks/demarcation_module.jpg)
Пример
```
def user():
    user = db_sess.query(User).filter(User.login == current_user.login).first()
    prizes = [db_sess.query(PrizeData).filter(PrizeData.owner_id == current_user.id).all()]

    if current_user.is_admin:
        return render_template('admin.html')
    else:
        return render_template('user.html', user=user)
```
## 4. Скриншоты интерфейса
|Логин|
![Login interface](images/Screenshots/Login.png)
|Регистрация|
![Registration](images/Screenshots/Registration.png)
## 5. Ссылка на [видео](https://www.youtube.com/) с работой
