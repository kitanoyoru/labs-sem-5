const HeaderToStr = (ruleName, ruleValue, factName, factValue) => {
  return `\x1b[92mStep:\n\t Rule:\t ${ruleToStr(
    ruleName,
    ruleValue,
  )}\n\t Fact:\t ${factToStr(factName, factValue)}\n\x1b[00m`;
};

const ruleToStr = (ruleName, ruleValue) => {
  const pairs = [];
  for (const y in ruleValue) {
    for (const x in ruleValue[y]) {
      pairs.push(`(${x}, ${y}), ${ruleValue[y][x]})`);
    }
  }
  return `${ruleName} = {${pairs.join(", ")}}`;
};

const factToStr = (factName, factValue) => {
  const pairs = [];
  for (const key in factValue) {
    pairs.push(`(${key}, ${factValue[key]})`);
  }
  return `${factName} = {${pairs.join(", ")}}`;
};

const ResultToStr = (result, facts, rules) => {
  const resultStrList = [];
  for (const key in result) {
    const pairs = [];
    for (const x in rules[key]) {
      pairs.push(`(${x}, ${key}), ${rules[key][x]})`);
    }
    resultStrList.push(
      `from (${key}, ${facts[key]}) and {${pairs.join(", ")}}:`,
    );
    for (const line of result[key]) {
      const lineStr = Object.entries(line)
        .map(([key, value]) => `${key} ∈ ${value || "∅"}`)
        .join(" and ");
      resultStrList.push(`\t${lineStr}`);
    }
    resultStrList.push("");
  }
  return resultStrList.join("\n");
};

const AnswerToStr = (answer) => {
  const answerStr = answer.map((part) => part.join(" x ")).join(") U (");
  return `\x1b[91mAnswer: (${answerStr})\x1b[00m`;
};

module.exports = {
  HeaderToStr,
  ResultToStr,
  AnswerToStr,
};
