const {
  gedelImpl,
  matrixImplication,
  tNorm,
  buildImplicationTable,
  compress,
  isEqualSets,
} = require('../src/operations.js');

describe('gedelImpl', () => {
  test('should return the minimum value when v1 <= v2', () => {
    const v1 = 2;
    const v2 = 3;
    const expectedResult = 1;

    const result = gedelImpl(v1, v2);

    expect(result).toBe(expectedResult);
  });

  test('should return v2 when v1 > v2', () => {
    const v1 = 5;
    const v2 = 4;
    const expectedResult = 4;

    const result = gedelImpl(v1, v2);

    expect(result).toBe(expectedResult);
  });
});

describe('matrixImpl', () => {
  test('should compute the matrix implementation', () => {
    const set1 = { a: 2, b: 3 };
    const set2 = { x: 1, y: 4 };
    const expectedResult = {
      a: { x: 1, y: 1 },
      b: { x: 1, y: 1 },
    };

    const result = matrixImplication(set1, set2);

    expect(result).toEqual(expectedResult);
  });
});

describe('tNorm', () => {
  test('should return the minimum value between v1 and v2', () => {
    const v1 = 2;
    const v2 = 3;
    const expectedResult = 2;

    const result = tNorm(v1, v2);

    expect(result).toBe(expectedResult);
  });
});

describe('builtImplTable', () => {
  test('should build the implementation table', () => {
    const set1 = { a: 2, b: 3 };
    const relation = {
      a: { x: 1, y: 4 },
      b: { x: 3, y: 2 },
    };
    const expectedResult = {
      a: { x: 1, y: 2 },
      b: { x: 3, y: 2 },
    };

    const result = buildImplicationTable(set1, relation);

    expect(result).toEqual(expectedResult);
  });

  test('should throw an error for different sets', () => {
    const set1 = { a: 2, b: 3 };
    const relation = {
      a: { x: 1, y: 4 },
      c: { x: 3, y: 2 },
    };

    expect(() => {
      builtImplTable(set1, relation);
    }).toThrow(Error);
  });
});

describe('compress', () => {
  test('should compress the implementation table', () => {
    const implTable = {
      a: { x: 1, y: 2 },
      b: { x: 2, y: 3 },
    };
    const expectedResult = {
      x: 2,
      y: 3,
    };

    const result = compress(implTable);

    expect(result).toEqual(expectedResult);
  });
});

describe('isEqualSets', () => {
  test('should return true for equal sets', () => {
    const set1 = ['a', 'b', 'c'];
    const set2 = ['a', 'b', 'c'];

    const result = isEqualSets(set1, set2);

    expect(result).toBe(true);
  });

  test('should return false for different sets', () => {
    const set1 = ['a', 'b', 'c'];
    const set2 = ['a', 'b'];

    const result = isEqualSets(set1, set2);

    expect(result).toBe(false);
  });
});
