/*
Лабораторная работа №1 по дисциплине ЛОИС

Выполнена студентами группы 121703
Прокопович Иван Сттаниславович, Рутковский Александр Максимович

Вариант 21:
Реализовать прямой нечеткий логический вывод используя импликацию Геделя
*/

package main

import (
	"fmt"

	"github.com/kitanoyoru/labs-sem-5/LOIS/Lab1/internal/load"
)

const DataPath = "/tmp/data"

func main() {
	facts, functions, err := load.LoadFromFile(DataPath)
	if err != nil {
		panic(err)
	}

	fmt.Println(facts)
	fmt.Println(functions)
}
