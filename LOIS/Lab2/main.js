const { ParseDataFile } = require("./src/data_loader");
const { MyChooseOne, ConvertToList, Cycle, DeleteUnimportant } = require('./src/operations');
const { HeaderToStr, ResultToStr, AnswerToStr } = require('./src/stringify');


const main = () => {
  const { rules, facts } = ParseDataFile();
  for (const rule of rules) {
    for (const fact of facts) {
      const ruleName = Object.keys(rule)[0];
      const ruleValue = Object.values(rule)[0];

      const factName = Object.keys(fact)[0];
      const factValue = Object.values(fact)[0];

      console.log(HeaderToStr(ruleName, ruleValue, factName, factValue));

      const results = {};
      for (const [factElKey, factElValue] of Object.entries(factValue)) {
        results[factElKey] = MyChooseOne(ruleValue[factElKey], factElValue);
      }

      console.log(ResultToStr(results, factValue, ruleValue));

      let resultsList = ConvertToList(results);
      resultsList = Cycle(resultsList);

      const answer = DeleteUnimportant(...resultsList);
      console.log(AnswerToStr(answer), "\n\n\n");
    }
  }
};

if (require.main == module) {
  main();
}
