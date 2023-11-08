const {
  removeVariables,
  Fact,
  Function,
} = require("../src/data_validators.js");

describe("removeVariables", () => {
  test("should remove variables from the head", () => {
    const head = "a(x,y,z)";
    const expectedResult = "a(,,)";

    const result = removeVariables(head);

    expect(result).toBe(expectedResult);
  });
});

describe("Fact", () => {
  describe("constructor", () => {
    test("should create a valid Fact instance", () => {
      const factStr = "p(x)={(a,0),(b,0.3),(c,1)}";

      const fact = new Fact(factStr);

      expect(fact.fact).toBe(factStr);
      expect(fact.head).toBe("p(x)");
      expect(fact.headWithoutVariables).toBe("p()");
      expect(fact.tail).toEqual({
        a: 0,
        b: 0.3,
        c: 1,
      });
    });

    test("should throw an error for an invalid fact", () => {
      const factStr = "invalid_fact";

      expect(() => {
        new Fact(factStr);
      }).toThrow(Fact.InvalidFactException);
    });
  });

  describe("isValid", () => {
    test("should return true for a valid fact", () => {
      const factStr = "p(x)={(a,0),(b,0.3),(c,1)}";

      const result = new Fact(factStr).isValid();

      expect(result).toBe(true);
    });
  });

  describe("isTailValid", () => {
    test("should return true if the tail is valid", () => {
      const factStr = "p(x)={(a,0),(b,0.3),(c,1)}";

      const result = new Fact(factStr).isTailValid();

      expect(result).toBe(true);
    });
  });
});

describe("Function", () => {
  describe("constructor", () => {
    test("should create a valid Function instance", () => {
      const functionStr = "f(x,y)=(g(x)~>h(y))";

      const func = new Function(functionStr);

      expect(func.func).toBe(functionStr);
      expect(func.head).toBe("f(x,y)");
      expect(func.headWithoutVariables).toBe("f(,)");
      expect(func.tail).toEqual(["g(x)", "h(y)"]);
      expect(func.tailWithoutVariables).toEqual(["g()", "h()"]);
    });

    test("should throw an error for an invalid function", () => {
      const functionStr = "invalid_function";

      expect(() => {
        new Function(functionStr);
      }).toThrow(Function.InvalidFunctionException);
    });
  });

  describe("isValid", () => {
    test("should return true for a valid function", () => {
      const functionStr = "f(x,y)=(g(x)~>h(y))";

      const result = new Function(functionStr).isValid();

      expect(result).toBe(true);
    });
  });
});
