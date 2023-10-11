package main

import (
	"fmt"
	"reflect"
	"testing"

	"github.com/kitanoyoru/labs-sem-5/LOIS/Lab1/internal/load"
)

func TestNewFact_ValidFact(t *testing.T) {
	factStr := "a(x)={(b,1.5),(c,2.0)}"
	expectedFact := &load.Fact{
		Fact:            "a(x)={(b,1.5),(c,2.0)}",
		Head:            "a(x)",
		HeadWithoutVars: "a",
		Tail: map[string]float64{
			"b": 1.5,
			"c": 2.0,
		},
	}

	fact, err := load.NewFact(factStr)

	if err != nil {
		t.Errorf("Unexpected error: %v", err)
	}

	if !reflect.DeepEqual(fact, expectedFact) {
		t.Errorf("Expected fact: %v, got: %v", expectedFact, fact)
	}
}

func TestNewFact_InvalidFact(t *testing.T) {
	factStr := "invalid_fact"
	expectedErr := &load.InvalidFactException{Fact: factStr}

	fact, err := load.NewFact(factStr)

	if fact != nil {
		t.Errorf("Expected fact to be nil, got: %v", fact)
	}

	if !reflect.DeepEqual(err, expectedErr) {
		t.Errorf("Expected error: %v, got: %v", expectedErr, err)
	}
}

func TestNewFunction_ValidFunction(t *testing.T) {
	functionStr := "f(x,y)=(p(x)~>v(y))"
	expectedFunction := &load.Function{
		Function:        "f(x,y)=(p(x)~>v(y))",
		Head:            "f(x,y)",
		HeadWithoutVars: "f,", // FIX
		Tail:            []string{"p(x)", "v(y)"},
		TailWithoutVars: []string{"p", "v"},
	}

	function, err := load.NewFunction(functionStr)

	if err != nil {
		t.Errorf("Unexpected error: %v", err)
	}

	if !reflect.DeepEqual(function, expectedFunction) {
		t.Errorf("Expected function: %v, got: %v", expectedFunction, function)
	}
}

func TestNewFunction_InvalidFunction(t *testing.T) {
	functionStr := "invalid_function"
	expectedErr := &load.InvalidFunctionException{Function: functionStr}

	function, err := load.NewFunction(functionStr)

	if function != nil {
		t.Errorf("Expected function to be nil, got: %v", function)
	}

	if !reflect.DeepEqual(err, expectedErr) {
		t.Errorf("Expected error: %v, got: %v", expectedErr, err)
	}
}

func TestRemoveVariables(t *testing.T) {
	head := "a(x,y,z)"
	expectedResult := "a,,"
	result := load.RemoveVariables(head)

	if result != expectedResult {
		t.Errorf("Expected result: %s, got: %s", expectedResult, result)
	}
}

func TestGetHead(t *testing.T) {
	fact := &load.Fact{
		Fact: "a(x)={(b,1.5),(c,2.0)}",
	}

	expectedHead := "a(x)"
	result := fact.GetHead()

	if result != expectedHead {
		t.Errorf("Expected head: %s, got: %s", expectedHead, result)
	}
}

func TestGetTail(t *testing.T) {
	function := &load.Function{
		Function: "f(x,y)=(g(x),h(y))",
	}

	expectedTail := []string{"g(x)", "h(y)"}
	result := function.GetTail()

	if !reflect.DeepEqual(result, expectedTail) {
		t.Errorf("Expected tail: %v, got: %v", expectedTail, result)
	}
}

func TestGetTailWithoutVariables(t *testing.T) {
	function := &load.Function{
		Tail: []string{"g(x)", "h(y)"},
	}

	expectedTailWithoutVars := []string{"g", "h"}
	result := function.GetTailWithoutVariables()

	if !reflect.DeepEqual(result, expectedTailWithoutVars) {
		t.Errorf("Expected tailWithoutVars: %v, got: %v", expectedTailWithoutVars, result)
	}
}

func TestFloatParse(t *testing.T) {
	valueStr := "3.14"
	expectedValue := 3.14

	result := load.ParseFloat(valueStr)

	if result != expectedValue {
		t.Errorf("Expected value: %f, got: %f", expectedValue, result)
	}
}

func TestFactIsValid_ValidFact(t *testing.T) {
	fact := &load.Fact{
		Fact: "a(x)={(b,1.5),(c,2.0)}",
	}

	result := fact.IsValid()

	if !result {
		t.Errorf("Expected isValid to be true, got false")
	}
}

func TestFactIsValid_InvalidFact(t *testing.T) {
	fact := &load.Fact{
		Fact: "invalid_fact",
	}

	result := fact.IsValid()

	if result {
		t.Errorf("Expected isValid to be false, got true")
	}
}

func TestFunctionIsValid_ValidFunction(t *testing.T) {
	function := &load.Function{
		Function: "f(x,y)=(g(x)~>h(y))",
	}

	result := function.IsValid()

	if !result {
		t.Errorf("Expected isValid to be true, got false")
	}
}

func TestFunctionIsValid_InvalidFunction(t *testing.T) {
	function := &load.Function{
		Function: "invalid_function",
	}

	result := function.IsValid()

	if result {
		t.Errorf("Expected isValid to be false, got true")
	}
}

func TestInvalidFactException_Error(t *testing.T) {
	fact := "invalid_fact"
	expectedError := fmt.Sprintf("Invalid format of fact: %s", fact)
	exception := &load.InvalidFactException{
		Fact: fact,
	}

	result := exception.Error()

	if result != expectedError {
		t.Errorf("Expected error: %s, got: %s", expectedError, result)
	}
}

func TestInvalidFunctionException_Error(t *testing.T) {
	function := "invalid_function"
	expectedError := fmt.Sprintf("Invalid format of function: %s", function)
	exception := &load.InvalidFunctionException{
		Function: function,
	}

	result := exception.Error()

	if result != expectedError {
		t.Errorf("Expected error: %s, got: %s", expectedError, result)
	}
}
