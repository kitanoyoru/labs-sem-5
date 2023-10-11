function gedelImpl(v1, v2) {
  return v1 <= v2 ? 1 : v2;
}

function matrixImpl(set1, set2) {
  return Object.fromEntries(
    Object.entries(set1).map(([i, v1]) => [
      i,
      Object.fromEntries(
        Object.entries(set2).map(([j, v2]) => [j, gedelImpl(v1, v2)])
      ),
    ])
  );
}

function tNorm(v1, v2) {
  return Math.min(v1, v2);
}

function builtImplTable(set1, relation) {
  const set1Keys = Object.keys(set1);
  const relationKeys = Object.keys(relation);

  if (!isEqualSets(set1Keys, relationKeys)) {
    throw new Error(
      `${JSON.stringify(set1Keys)} != ${JSON.stringify(relationKeys)}`
    );
  }

  return Object.fromEntries(
    relationKeys.map((i) => [
      i,
      Object.fromEntries(
        Object.entries(relation[i]).map(([j, v]) => [j, tNorm(set1[i], v)])
      ),
    ])
  );
}

function compress(implTable) {
  const rowKeys = Object.keys(implTable);
  const colKeys = Object.keys(implTable[rowKeys[0]]);
  return Object.fromEntries(
    colKeys.map((colKey) => [
      colKey,
      Math.max(...rowKeys.map((rowKey) => implTable[rowKey][colKey])),
    ])
  );
}

function isEqualSets(set1, set2) {
  return (
    set1.length === set2.length && set1.every((value) => set2.includes(value))
  );
}

module.exports = {
  gedelImpl,
  matrixImpl,
  tNorm,
  builtImplTable,
  isEqualSets,
  compress,
};
