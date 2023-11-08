/*
Лабораторная работа №1
по дисциплине ЛОИС

Выполнена студентами группы 121703
Прокопович Иван Станиславович, Рутковский Алекасандр Mаксимович 

Вариант 21:
Реализовать прямой нечеткий логический вывод используя импликацию Геделя
*/

const readline = require("readline");

const operations = require("./src/operations");

const { loadFromFile, getFactsDict } = require("./src/data_loader");
const { Fact } = require("./src/data_validators");

function main() {
  let { facts, functions } = loadFromFile("/tmp/data");

  const functionTables = {};
  const functionTablesTitles = [];

  for (const [functionHead, functionObj] of Object.entries(functions)) {
    functionTablesTitles.push(functionObj.head);

    const [firstSetName, secondSetName] = functionObj.tailWithoutVariables;
    const firstSet = facts[firstSetName];
    const secondSet = facts[secondSetName];

    functionTables[functionHead] = operations.matrixImplication(
      firstSet.tail,
      secondSet.tail,
    );
  }

  console.log("Implication Function tables:", functionTables);

  const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout,
  });

  rl.input.on("keypress", (_, key) => {
    if (key.name === "return") {
      processLoop();
    }
  });

  function processLoop() {
    const result = [];

    for (const [functionHead, functionTable] of Object.entries(
      functionTables,
    )) {
      for (const fact of Object.values(facts)) {
        try {
          const tmp = operations.buildImplicationTable(
            fact.tail,
            functionTable,
          );
          console.log(
            "Triangular Norm",
            functionHead,
            "with",
            fact.head,
            ": ",
            tmp,
          );
          result.push(operations.maxComposition(tmp));
        } catch (_) {}
      }
    }

    const resultStr = result.map((conclusionSet) =>
      Object.entries(conclusionSet)
        .map((pair) => `(${pair[0]},${pair[1]})`)
        .join(","),
    );

    let newFacts = [];
    resultStr.forEach((val, i) => {
      newFacts.push(`${String.fromCharCode(97 + i)}(x)={${val}}`);
    });
    facts = getFactsDict(newFacts.map((fact) => new Fact(fact)));

    console.log("Result: {", resultStr.join("}, {"), "}.");
  }

  processLoop();
}

if (require.main === module) {
  main();
}
