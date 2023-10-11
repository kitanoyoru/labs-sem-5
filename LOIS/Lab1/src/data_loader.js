const { readFileSync } = require("fs");

const { Fact } = require('./data_validators');
const { Function } = require('./data_validators');

function loadFromFile(path) {
    let facts, functions;
    const fileContent = readFileSync(path, 'utf8');
    [facts, functions] = fileContent.split('\n\n').map(line => line.split('\n').map(x => x.replace(/\s/g, '')));
    
    facts = facts.map(fact => new Fact(fact));
    functions = functions.map(func => new Function(func));
    return {
        facts: getFactsDict(facts),
        functions: getFunctionsDict(functions)
    };
}

function getFactsDict(facts) {
    const factsDict = {};
    for (const fact of facts) {
        factsDict[fact.headWithoutVariables] = fact;
    }
    return factsDict;
}

function getFunctionsDict(functions) {
    const functionsDict = {};
    for (const func of functions) {
        functionsDict[func.headWithoutVariables] = func;
    }
    return functionsDict;
}

module.exports = {
    loadFromFile
};
