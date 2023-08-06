import os
from typing import Text
from uuid import UUID


def getOrElse(default, value):
    if value:
        return value
    else:
        return default


black = "black"
blue = "blue"
closed = "closed"
create = "create"
deleted = "deleted"
doing = "doing"
execution="execution"
formirovanie="formirovanie"
gray = "#808080"
green = "green"
handmade = "handmade"
in_production="in_production"
launched = "launched"
light_green = "#99CC00"
made = "made"
new = "new"
new_man = "new_man"
not_relevant = "not_relevant"
orange = "orange"
otkryt = "otkryt"
otmenen = "otmenen"
red = "red"
restarted = "restarted"
route_made="route_made"
sht = "шт"
started = "started"
started_another = "started_another"
stoped = "stoped"
transferred = "transferred"
unknown = "unknown"
update = "update"
value_odd = "value_odd"
zakryt = "zakryt"

name_closed="Закрыт"
name_doing="Выполнен"
name_formirovanie="Формирование"
name_handmade="Системный (ручное формирование)"
name_new="Новый"
name_new_h="Новый (р)"
name_new_s="Новый (с)"
name_restarted="Запущен (повторно)"
name_started="Запущен"
name_started_another="Запущен (раннее)"
name_stoped="Остановлен"
name_transferred="Назначенный"
name_unknown="Неопределеный"


def blinkString(text, blink=True, color="black", bold=False) -> Text:
    if blink:
        res = f'<div class="blink"><strong><font color="{color}"</font>{text}</strong></div>'
    else:
        res = f'<div><strong><font color="{color}"</font>{text}</strong></div>'

    if bold == True:
        return f'<b>{res}</b>'
    else:
        return res


def uuid5():
    return UUID(bytes=os.urandom(16), version=4)

def uuid4():
    return str(UUID(bytes=os.urandom(16), version=4)).upper().replace('-', '_')
