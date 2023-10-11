package load

import (
	"os"
	"strings"
)

func LoadFromFile(path string) (map[string]*Fact, map[string]*Function, error) {
	fileData, err := os.ReadFile(path)
	if err != nil {
		return nil, nil, err
	}

	fileContent := string(fileData)

	fileSections := strings.Split(fileContent, "\n\n")
	factsSection := strings.TrimSpace(fileSections[0])
	functionsSection := strings.TrimSpace(fileSections[1])

	factStrings := strings.Split(factsSection, "\n")
	facts := make([]*Fact, len(factStrings))
	for i, factStr := range factStrings {
		fact, err := NewFact(strings.Join(strings.Split(factStr, " "), ""))
		if err != nil {
			return nil, nil, err
		}
		facts[i] = fact
	}

	functionStrings := strings.Split(functionsSection, "\n")
	functions := make([]*Function, len(functionStrings))
	for i, funcStr := range functionStrings {
		function, err := NewFunction(strings.Join(strings.Split(funcStr, " "), ""))
		if err != nil {
			return nil, nil, err
		}
		functions[i] = function
	}

	factsDict := getFactsDict(facts)
	functionsDict := getFunctionsDict(functions)

	return factsDict, functionsDict, nil
}

func getFactsDict(facts []*Fact) map[string]*Fact {
	factsDict := make(map[string]*Fact)
	for _, fact := range facts {
		factsDict[fact.headWithoutVars] = fact
	}
	return factsDict
}

func getFunctionsDict(functions []*Function) map[string]*Function {
	functionsDict := make(map[string]*Function)
	for _, function := range functions {
		functionsDict[function.headWithoutVars] = function
	}
	return functionsDict
}
