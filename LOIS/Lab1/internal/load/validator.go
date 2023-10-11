package load

import (
	"fmt"
	"regexp"
	"strconv"
	"strings"
)

func RemoveVariables(head string) string {
	name := strings.Split(head, "(")[0]
	numOfComma := strings.Count(head, ",")
	return fmt.Sprintf("%s%s", name, strings.Repeat(",", numOfComma))
}

func ParseFloat(s string) float64 {
	value, _ := strconv.ParseFloat(s, 64)
	return value
}

type Fact struct {
	Fact            string
	Head            string
	HeadWithoutVars string
	Tail            map[string]float64
}

type InvalidFactException struct {
	Fact string
}

func (e *InvalidFactException) Error() string {
	return fmt.Sprintf("Invalid format of fact: %s", e.Fact)
}

func NewFact(fact string) (*Fact, error) {
	f := &Fact{
		Fact: fact,
	}

	if !f.IsValid() {
		return nil, &InvalidFactException{Fact: fact}
	}

	f.Head = f.GetHead()
	f.HeadWithoutVars = RemoveVariables(f.Head)
	f.Tail = f.GetTail()

	return f, nil
}

func (f *Fact) IsValid() bool {
	pattern := regexp.MustCompile(`^[a-z]\([a-z]\)={(\([a-z],\d(\.\d)?\),)*(\([a-z],\d(\.\d)?\))?}$`)
	return pattern.MatchString(f.Fact)
}

func (f *Fact) GetHead() string {
	headTailPattern := regexp.MustCompile(`^(.+)={(.*)}$`)
	matches := headTailPattern.FindStringSubmatch(f.Fact)
	return matches[1]
}

func (f *Fact) GetTail() map[string]float64 {
	headTailPattern := regexp.MustCompile(`^(.+)={(.*)}$`)
	matches := headTailPattern.FindStringSubmatch(f.Fact)
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
		tail[key] = ParseFloat(value)
	}

	return tail
}

type Function struct {
	Function        string
	Head            string
	HeadWithoutVars string
	Tail            []string
	TailWithoutVars []string
}

type InvalidFunctionException struct {
	Function string
}

func (e *InvalidFunctionException) Error() string {
	return fmt.Sprintf("Invalid format of function: %s", e.Function)
}

func NewFunction(function string) (*Function, error) {
	f := &Function{
		Function: function,
	}

	if !f.IsValid() {
		return nil, &InvalidFunctionException{Function: function}
	}

	f.Head = f.GetHead()
	f.HeadWithoutVars = RemoveVariables(f.Head)
	f.Tail = f.GetTail()
	f.TailWithoutVars = f.GetTailWithoutVariables()

	return f, nil
}

func (f *Function) IsValid() bool {
	pattern := regexp.MustCompile(`^[a-z]\(([a-z],)*[a-z]\)=\([a-z]\([a-z]\)~>[a-z]\([a-z]\)\)$`)
	return pattern.MatchString(f.Function)
}

func (f *Function) GetHead() string {
	headTailPattern := regexp.MustCompile(`^(.+)=(.*)$`)
	matches := headTailPattern.FindStringSubmatch(f.Function)
	return matches[1]
}

func (f *Function) GetTail() []string {
	headTailPattern := regexp.MustCompile(`^(.+)=(.*)$`)
	matches := headTailPattern.FindStringSubmatch(f.Function)
	tailStr := matches[2]
	return strings.Split(tailStr[1:len(tailStr)-1], "~>")
}

func (f *Function) GetTailWithoutVariables() []string {
	tailWithoutVars := make([]string, len(f.Tail))
	for i, t := range f.Tail {
		tailWithoutVars[i] = RemoveVariables(t)
	}
	return tailWithoutVars
}
