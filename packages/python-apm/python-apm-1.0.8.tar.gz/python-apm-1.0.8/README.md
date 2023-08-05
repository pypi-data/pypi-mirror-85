# APM - Ansible package manager

### Allows you to set dependencies from a file meta/main.yml

![alt text](https://github.com/WeslyG/apm/blob/master/etc/screen.png?raw=true)


### TODO:

Надо конфигурацию написать, пока все захардкожено
Работает с
- dependencies
- optional_dependencies

И с файлом /meta/requirements.yml ansible 2.10
Важно, содержимое requirements.yml должно являться словарем (list) иначе ничего работать не будет

### Why?

Ansible-galaxy предлагает использовать meta/main.yml для описания зависимостей, однако не позволяет
установить их из этого файла. Вместо этого нам предлагают использовать `requirements.yml` с другим форматом (collections/roles)
И устанавливать через него с помощью `ansible-galaxy install -r requirements.yml`
И при установке роли, если в ней есть зависимость в meta/main то она будет установленна. Выходит
что `meta/main` подходит только для установки транзитивных зависимостей, что мне не нравится.
Я считаю не верным иметь 2 разных метода установки зависимостей! (а ведь некоторые используют еще и GILT)

Чтобы избежать путаницы, и сложности, я написал обертку -  пакет APM (Ansible Package Manager)
Который фокусируется на файле meta/main.yml как едином файле зависимостей.
Пакетный менеджер может установить ваши зависимости из этого файла (под капотом, он конвертирует формат `meta/main` в `requirements.yml` и отправляет
их в ansible-galaxy) что исключает лишнюю логику, и не дает ничему сломаться. Также по умолчанию APM использует
локальную папку с ролями, а не устанавливает их в глобальную область видимости.

В будущем управлять поведением APM можно с помощью файла конфигурации `.apmrc` в папке пользователя глобально, или в папке проекта локально.
Также через ENV (для удобства работы CI систем).

### Функционал

Сегодня функционал apm ограничен, он умеет лишь устанавливать зависимости из файла meta/main.yml + meta/requirements.yml
Проверять их наличие, и обрабатывать ошибки.

```
apm install
```

### Config

temp_dir = /tmp

ROLES_FOLDER = env
roles_folder = ./remote_roles

### galaxy params
force = True
ignore_errors = False
