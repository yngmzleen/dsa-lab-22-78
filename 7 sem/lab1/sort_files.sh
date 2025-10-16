#!/bin/bash

directory="/Users/egorivanov/Documents/7 семестр/РПП/dsa-lab-22-78/7 sem"

if [ ! -d "$directory" ]; then
    echo "Ошибка: Директория '$directory' не существует"
    exit 1
fi

echo "Список файлов в директории '$directory', отсортированных по дате модификации:"

ls -lt "$directory" | grep "^-" | head -20
