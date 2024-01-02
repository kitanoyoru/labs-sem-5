const { readFileSync } = require("fs");

const DataFile = { name: "/tmp/data", encoding: "utf8" };

const RegExpRulePattern =
  /^[A-Z]=\{(\(\([a-x\d]+\,[a-z\d]+\)\,\d\.\d\)\,?)*\}$/;
const RegExpFactPattern = /^[A-Z]=\{(\([a-z\d]+\,\d\.\d\),?)*\}$/;

const ParseDataFile = () => {
  const facts = [];
  const rules = [];
  const usedNames = [];

  const data = readFileSync(...Object.values(DataFile));
  const lines = data.split("\n");

  for (const line of lines) {
    const processedLine = line
      .trim()
      .replace(/\s/g, "")
      .replace(/,0\)/g, ",0.0)")
      .replace(/,1\)/g, ",1.0)");

    if (!processedLine) {
      continue;
    }

    const ruleMatch = processedLine.match(RegExpRulePattern);
    const factMatch = processedLine.match(RegExpFactPattern);

    if (ruleMatch) {
      try {
        const rule = parseRule(ruleMatch, usedNames);
        rules.push(rule);
        usedNames.push(Object.keys(rule)[0]);
      } catch (e) {
        console.log(e);
        continue;
      }
    } else if (factMatch) {
      try {
        const fact = parseFact(factMatch, usedNames);
        facts.push(fact);
        usedNames.push(Object.keys(fact)[0]);
      } catch (e) {
        console.log(e);
        continue;
      }
    } else {
      console.log(`Line '${line}' is NOT in the correct format.`);
    }
  }

  return { rules, facts };
};

const parseRule = (match, usedNames) => {
  const name = match[0].split("=")[0].trim();

  if (usedNames.includes(name)) {
    throw new Error(`Rule name '${name}' is already used. Skipping...`);
  }

  const values = match[0].matchAll(/\(\(([a-x\d]+)\,([a-z\d]+)\)\,(\d\.\d)\)/g);
  const valuesArr = Array.from(values).map((value) => [
    value[1],
    value[2],
    parseFloat(value[3]),
  ]);

  const valuesDict = {};
  for (const value of valuesArr) {
    if (!valuesDict[value[1]]) {
      valuesDict[value[1]] = {};
    }
    valuesDict[value[1]][value[0]] = value[2];
  }

  const result = {};
  result[name] = valuesDict;

  return result;
};

const parseFact = (match, usedNames) => {
  const name = match[0].split("=")[0].trim();

  if (usedNames.includes(name)) {
    throw new Error(`Fact name '${name}' is already used. Skipping...`);
  }

  const values = match[0].matchAll(/\(([a-z\d]+)\,(\d\.\d)\)/g);
  const valuesDict = {};

  for (const value of values) {
    valuesDict[value[1]] = parseFloat(value[2]);
  }

  const result = {};
  result[name] = valuesDict;

  return result;
};

module.exports = {
  ParseDataFile,
};
