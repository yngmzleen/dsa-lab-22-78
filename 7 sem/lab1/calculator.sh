#!/bin/bash

echo "Calculator"

num1=75
num2=0

sum=$((num1 + num2))
echo "Sum: $sum"

sub=$((num1 - num2))
echo "Sub: $sub"

mul=$((num1 * num2))
echo "Mul: $mul"

if [ $num2 -ne 0 ]; then
    div=$((num1 / num2))
    echo "Div: $div"
else
    echo "Div: Ошибка - деление на ноль!"
fi

