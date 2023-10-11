package internal

import "fmt"

func gedelImpl(v1, v2 float64) float64 {
	if v1 <= v2 {
		return 1
	}

	return v2
}

func matrixImpl(set1, set2 map[int]float64) map[int]map[int]float64 {
	result := make(map[int]map[int]float64)
	for i := range set1 {
		result[i] = make(map[int]float64)
		for j := range set2 {
			result[i][j] = gedelImpl(set1[i], set2[j])
		}
	}

	return result
}

func tNorm(v1, v2 float64) float64 {
	if v1 < v2 {
		return v1
	}

	return v2
}

func buildImplTable(set1, relation map[int]map[int]float64) map[int]map[int]float64 {
	for key := range set1 {
		if _, ok := relation[key]; !ok {
			panic(fmt.Sprintf("Key %d not found in relation", key))
		}
	}

	result := make(map[int]map[int]float64)
	for i := range relation {
		result[i] = make(map[int]float64)
		for j := range relation[i] {
			result[i][j] = tNorm(set1[i], relation[i][j])
		}
	}

	return result
}

func compress(implTable map[int]map[int]float64) map[int]float64 {
	rowKeys := make([]int, 0, len(implTable))
	for key := range implTable {
		rowKeys = append(rowKeys, key)
	}
	colKeys := make([]int, 0, len(implTable[rowKeys[0]]))
	for key := range implTable[rowKeys[0]] {
		colKeys = append(colKeys, key)
	}
	result := make(map[int]float64)
	for _, colKey := range colKeys {
		maxValue := float64(0)
		for _, rowKey := range rowKeys {
			if implTable[rowKey][colKey] > maxValue {
				maxValue = implTable[rowKey][colKey]
			}
		}
		result[colKey] = maxValue
	}
	return result
}

/*
def gedel_impl(v1, v2):
    return 1 if v1 <= v2 else v2


def matrix_impl(set1, set2):
    return {i: {j: gedel_impl(set1[i], set2[j]) for j in set2} for i in set1}


def t_norm(v1, v2):
    return min(v1, v2)


def built_impl_table(set1, relation):
    if set(set1.keys()) != set(relation.keys()):
        raise ValueError(f"{set(set1.keys())} != {set(relation.keys())}")
    return {i: {j: t_norm(set1[i], relation[i][j]) for j in relation[i]} for i in relation}


def compress(impl_table):
    row_keys = list(impl_table.keys())
    col_keys = list(impl_table[row_keys[0]].keys())
    return {col_key: max([impl_table[row_key][col_key] for row_key in row_keys]) for col_key in col_keys}
*/
