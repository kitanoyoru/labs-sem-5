const operations = require("./src/operations");
const { loadFromFile } = require("./src/data_loader");

function main() {
  const { facts, functions } = loadFromFile("/tmp/data");

  const functionTables = {};
  const functionTablesTitles = [];

  for (const [functionHead, functionObj] of Object.entries(functions)) {
    functionTablesTitles.push(functionObj.head);

    const [firstSetName, secondSetName] = functionObj.tailWithoutVariables;
    const firstSet = facts[firstSetName];
    const secondSet = facts[secondSetName];

    functionTables[functionHead] = operations.matrixImpl(
      firstSet.tail,
      secondSet.tail
    );
  }


  const result = [];

  for (const functionTable of Object.values(functionTables)) {
    for (const fact of Object.values(facts)) {
      try {
        const tmp = operations.builtImplTable(fact.tail, functionTable);
        console.log(tmp)
        result.push(operations.compress(tmp));
      } catch (_) {
      }
    }
  }

  console.log("Result:", result);

  const resultStr = result.map((conclusionSet) =>
    Object.entries(conclusionSet)
      .map((pair) => `(${pair[0]}, ${pair[1]})`)
      .join(", ")
  );

  console.log("Ответ: {", resultStr.join("}, {"), "}.");
}

if (require.main === module) {
  main();
}
