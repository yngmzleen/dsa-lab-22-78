#!/bin/bash

filename="/Users/egorivanov/Documents/7 семестр/РПП/dsa-lab-22-78/7 sem/calculator.sh"

if [ ! -f "$filename" ]; then
    echo "Ошибка: Файл '$filename' не существует"
    exit 1
fi

echo "Статистика для файла '$filename':"

lines=$(wc -l < "$filename")
echo "Количество строк: $lines"

words=$(wc -w < "$filename")
echo "Количество слов: $words"

chars=$(wc -c < "$filename")
echo "Количество символов: $chars"
