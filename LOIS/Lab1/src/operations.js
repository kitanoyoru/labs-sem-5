function gedelImplication(v1, v2) {
  return v1 <= v2 ? 1 : v2;
}

function matrixImplication(set1, set2) {
  return Object.fromEntries(
    Object.entries(set1).map(([i, v1]) => [
      i,
      Object.fromEntries(
        Object.entries(set2).map(([j, v2]) => [j, gedelImplication(v1, v2)]),
      ),
    ]),
  );
}

function triangularNorm(v1, v2) {
  return Math.min(v1, v2);
}

function buildImplicationTable(set1, relation) {
  const set1Keys = Object.keys(set1);
  const relationKeys = Object.keys(relation);

  if (!isEqualSets(set1Keys, relationKeys)) {
    throw new Error(
      `${JSON.stringify(set1Keys)} != ${JSON.stringify(relationKeys)}`,
    );
  }

  return Object.fromEntries(
    relationKeys.map((i) => [
      i,
      Object.fromEntries(
        Object.entries(relation[i]).map(([j, v]) => [
          j,
          triangularNorm(set1[i], v),
        ]),
      ),
    ]),
  );
}

function maxComposition(implTable) {
  const rowKeys = Object.keys(implTable);
  const colKeys = Object.keys(implTable[rowKeys[0]]);
  return Object.fromEntries(
    colKeys.map((colKey) => [
      colKey,
      Math.max(...rowKeys.map((rowKey) => implTable[rowKey][colKey])),
    ]),
  );
}

function isEqualSets(set1, set2) {
  return (
    set1.length === set2.length && set1.every((value) => set2.includes(value))
  );
}

module.exports = {
  gedelImplication,
  matrixImplication,
  triangularNorm,
  buildImplicationTable,
  isEqualSets,
  maxComposition,
};
