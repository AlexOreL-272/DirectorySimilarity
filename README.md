# Author: Шевчук Александр Андреевич

## Task №4 DirectorySimilarity
## Установка и запуск проекта через консоль
1. Установите Python одной из последних версий.
2. Склонируйте репозиторий в удобную Вам директорию.
3. С помощью поиска или сочетанием клавиш `Win + R` откройте cmd.
4. В открывшейся консоли введите `cd "path to repo directory"`, заменив `"path to repo directory"` на путь к склонированному проекту.
5. Введите `main.py`.

## Установка и запуск проекта в IDE на примере PyCharm
1. Установите Python одной из последних версий.
2. Создайте пустой проект (**File -> New Project**).
3. Введите имя проекта и в поле `Base interpreter` выберите интерпретатор соответствующей версии.
4. Нажмите кнопку `Create`.
5. Откройте консоль
    * С помощью поиска или сочетанием клавиш Win + R откройте cmd.
    * В __PyCharm__ перейдите на вкладку `Terminal` в самом низу окна.
6. В открывшейся консоли склонируйте репозиторий в папку с __PyCharm__ проектом.
7. Запустите проект, нажав на зелёную кнопку в виде треугольника в верхнем правом углу.

## Как работать с программой
После запуска программы Вам будет предложено ввести названия первой и второй директории, а также минимальный процент совпадения, 
при котором файлы считаются схожими. После ввода данных программа выведет полностью совпадающие файлы, затем схожие файлы с указание 
процента схожести, и в конце уникальные файлы.

## Описание работы программы
В файле `directory_check` находится класс, производящий вышеупомянутые действия. 
Метод `check_dirs` сравнивает каждый файл первой директории с каждым файлом из второй директории и делает соответствующие выводы.
Определение процента схожести файлов производится путем вычисления расстояния Левенштейна между содержимым файлов.

## Добавленные оптимизации к работе программы
1. Если отношение минимального размера файла к максимальному меньше, чем заданный минимальный процент схожести, то такие файлы не могут быть
схожими, а тем более идентичными.
2. Использование "транзитивности": если `file_1` идентичен `file_2`, а `file_2` идентичен `file_3`, то, очевидно, `file_1` идентичен `file_3`.
3. Если `file_1` и `file_2` есть `hardlink` на некоторый файл или `file_1` -- `hardlink` на `file_2` (справедливо и обратное),
то их содержимое совпадает, а значит, `file_1` идентичен `file_2`.

## Принятые решения
1. Будем считать `file-symlink` и файл, на который он ссылается, различными, если их содержимое не совпадает, так как в `symlink`-файле хранится
путь к файлу, на который он ссылается, а не содержимое ссылаемого файла.

## Замечание
Работа программы тестировалась на ОС `Windows`.
