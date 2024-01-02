const MyChooseOne = (ruleTuple, factElValue) => {
  const res = [];
  for (const mainEl in ruleTuple) {
    const currentRow = {};
    for (const el in ruleTuple) {
      if (mainEl === el) {
        const currentEl = calculateEqual(ruleTuple[el], factElValue);
        currentRow[el] = currentEl;
      } else {
        const currentEl = calculateLess(ruleTuple[el], factElValue);
        currentRow[el] = currentEl;
      }
    }
    res.push(currentRow);
  }
  return res;
};

const calculateEqual = (left, right) => {
  if (left < right) {
    return null;
  } else if (left === right) {
    return [right, 1];
  } else {
    return [right, right];
  }
};

const calculateLess = (left, right) => {
  return left <= right ? [0, 1] : [0, right];
};

const ConvertToList = (dct) => {
  const result = [];
  for (const value of Object.values(dct)) {
    result.push(Object.values(value));
  }
  return result;
};

const Cycle = (results) => {
  while (results.length > 1) {
    const temp = intersectionLine(
      results[results.length - 2],
      results[results.length - 1],
    );
    if (temp !== null) {
      results[results.length - 2] = temp;
      results.pop();
    } else {
      return null;
    }
  }
  return results;
};

const intersectionLine = (line1, line2) => {
  const line = [];
  for (const cond1 of line1) {
    for (const cond2 of line2) {
      const newCond = intersectionCond(cond1, cond2);
      if (newCond) {
        line.push(newCond);
      }
    }
  }
  return line;
};

const intersectionCond = (cond1, cond2) => {
  if (Object.values(cond1).includes(null) || Object.values(cond2).includes(null)) {
    return [];
  } else {
    const cond2values = Object.values(cond2);
    const answ = Object.values(cond1).map((first, i) => {
        if (!cond2values[i]) {
            return "filter"
        }
        const v = intersection(first, cond2values[i])
        return v
    });
    if (!answ.includes("filter")) {
        console.log(answ)
        return answ.includes(null) ? [] : answ;
    } 
  }
};

const intersection = (interval1, interval2) => {
  if (!interval1 || !interval2) {
    return null;
  } else {
    const x1 = Math.max(interval1[0], interval2[0]);
    const x2 = Math.min(interval1[1], interval2[1]);
    return x1 <= x2 ? [x1, x2] : null;
  }
};

const returnUnique = (left, right) => {
  let leftUniqueCounter = 0;
  let leftRightCounter = 0;
  for (let i = 0; i < left.length; i++) {
    const leftEl = left[i];
    const rightEl = right[i];
    if (leftEl[0] >= rightEl[0] && leftEl[1] <= rightEl[1]) {
      leftRightCounter++;
    }
    if (leftEl[0] <= rightEl[0] && leftEl[1] >= rightEl[1]) {
      leftUniqueCounter++;
    }
  }
  if (leftUniqueCounter === left.length) {
    return left;
  }
  if (leftRightCounter === left.length) {
    return right;
  }
};

const DeleteUnimportant = (results) => {
  for (let i = 0; i < results.length; i++) {
    const elI = results[i];
    for (let j = 0; j < results.length; j++) {
      const elJ = results[j];
      if (elI && elJ && i !== j) {
        const rez = returnUnique(elI, elJ);
        if (rez === elI) {
          results[j] = null;
        }
        if (rez === elJ) {
          results[i] = null;
        }
      }
    }
  }
  return results.filter((a) => a);
};

module.exports = {
  MyChooseOne,
  ConvertToList,
  Cycle,
  DeleteUnimportant,
};
