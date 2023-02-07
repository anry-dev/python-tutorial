Обеспечение работы нового сайта
================================
## Необходимые пакеты:
* nginx
* Python 3.9
* virtualenv + pip
* Git
например, в Debian
	apt-get install nginx

## Конфигурация виртуального узла Nginx
* см. nginx.template.conf
* заменить SITENAME, например, на staging.my-domain.com
* заменить ROOT на папку, где лежат сайты

## Служба Systemd
* см. gunicorn-systemd.template.service
* заменить SITENAME, например, на staging.my-domain.com
* заменить ROOT на папку, где лежат сайты
* заменить USER на пользователя, под которым все работает
* вручную создать файл .emailpass , куда поместить пароль для отправки почты
  пока только для фиксированного пользователя

## Структура папок:
Если допустить, что есть учетная запись пользователя в /home/username
/home/username
└── sites
    └── SITENAME
        ├── database
        ├── source
        ├── static
        └── virtualenv
