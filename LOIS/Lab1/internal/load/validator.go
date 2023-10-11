package load

import (
	"fmt"
	"regexp"
	"strconv"
	"strings"
)

func removeVariables(head string) string {
	name := strings.Split(head, "(")[0]
	numOfComma := strings.Count(head, ",")
	return fmt.Sprintf("%s%s", name, strings.Repeat(",", numOfComma))
}

func parseFloat(s string) float64 {
	value, _ := strconv.ParseFloat(s, 64)
	return value
}

type Fact struct {
	fact            string
	head            string
	headWithoutVars string
	tail            map[string]float64
}

type InvalidFactException struct {
	fact string
}

func (e *InvalidFactException) Error() string {
	return fmt.Sprintf("Invalid format of fact: %s", e.fact)
}

func NewFact(fact string) (*Fact, error) {
	f := &Fact{
		fact: fact,
	}

	if !f.isValid() {
		return nil, &InvalidFactException{fact: fact}
	}

	f.head = f.getHead()
	f.headWithoutVars = removeVariables(f.head)
	f.tail = f.getTail()

	return f, nil
}

func (f *Fact) isValid() bool {
	pattern := regexp.MustCompile(`^[a-z]\([a-z]\)={(\([a-z],\d(\.\d)?\),)*(\([a-z],\d(\.\d)?\))?}$`)
	return pattern.MatchString(f.fact)
}

func (f *Fact) getHead() string {
	headTailPattern := regexp.MustCompile(`^(.+)={(.*)}$`)
	matches := headTailPattern.FindStringSubmatch(f.fact)
	return matches[1]
}

func (f *Fact) getTail() map[string]float64 {
	headTailPattern := regexp.MustCompile(`^(.+)={(.*)}$`)
	matches := headTailPattern.FindStringSubmatch(f.fact)
	pairsStr := matches[2]
	pairs := strings.Split(pairsStr[1:len(pairsStr)-1], "),(")
	tail := make(map[string]float64)

	if len(pairs) == 1 && pairs[0] == "" {
		return tail
	}

	for _, pair := range pairs {
		pairParts := strings.Split(pair, ",")
		key := strings.Trim(pairParts[0], "()")
		value := pairParts[1]
		tail[key] = parseFloat(value)
	}

	return tail
}

type Function struct {
	function        string
	head            string
	headWithoutVars string
	tail            []string
	tailWithoutVars []string
}

type InvalidFunctionException struct {
	function string
}

func (e *InvalidFunctionException) Error() string {
	return fmt.Sprintf("Invalid format of function: %s", e.function)
}

func NewFunction(function string) (*Function, error) {
	f := &Function{
		function: function,
	}

	if !f.isValid() {
		return nil, &InvalidFunctionException{function: function}
	}

	f.head = f.getHead()
	f.headWithoutVars = removeVariables(f.head)
	f.tail = f.getTail()
	f.tailWithoutVars = f.getTailWithoutVariables()

	return f, nil
}

func (f *Function) isValid() bool {
	pattern := regexp.MustCompile(`^[a-z]\(([a-z],)*[a-z]\)=\([a-z]\([a-z]\)~>[a-z]\([a-z]\)\)$`)
	return pattern.MatchString(f.function)
}

func (f *Function) getHead() string {
	headTailPattern := regexp.MustCompile(`^(.+)=(.*)$`)
	matches := headTailPattern.FindStringSubmatch(f.function)
	return matches[1]
}

func (f *Function) getTail() []string {
	headTailPattern := regexp.MustCompile(`^(.+)=(.*)$`)
	matches := headTailPattern.FindStringSubmatch(f.function)
	tailStr := matches[2]
	return strings.Split(tailStr[1:len(tailStr)-1], "~>")
}

func (f *Function) getTailWithoutVariables() []string {
	tailWithoutVars := make([]string, len(f.tail))
	for i, t := range f.tail {
		tailWithoutVars[i] = removeVariables(t)
	}
	return tailWithoutVars
}
