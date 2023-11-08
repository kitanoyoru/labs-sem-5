function removeVariables(head) {
  const name = head.split("(")[0];
  return name;
  const numOfComma = (head.match(/,/g) || []).length;
  return `${name}(${",".repeat(numOfComma)})`;
}

class Fact {
  constructor(fact) {
    this.fact = fact;
    if (!this.isValid()) {
      throw new Fact.InvalidFactException(fact);
    }
    this.head = this.getHead();
    this.headWithoutVariables = removeVariables(this.head);
    this.tail = this.getTail();
    if (!this.isTailValid()) {
      throw new Fact.InvalidFactException(fact);
    }
    this.tail = Object.fromEntries(this.tail);
  }

  isValid() {
    // p(x)={(a,0),(b,0.3),(c,1)}
    const pattern =
      /^[a-z]\([a-z]\)={(\([a-z],\d(\.\d)?\),)*(\([a-z],\d(\.\d)?\))?}$/;
    return pattern.test(this.fact);
  }

  getHead() {
    const headTailPattern = /^(.+)={(.*)}$/;
    return this.fact.match(headTailPattern)[1];
  }

  getTail() {
    const headTailPattern = /^(.+)={(.*)}$/;
    const pairsStr = this.fact.match(headTailPattern)[2];
    const pairs = pairsStr
      .slice(1, -1)
      .split("),(")
      .map((pair) => pair.split(","));
    return pairs[0].length === 1
      ? []
      : pairs.map(([key, value]) => [key, parseFloat(value)]);
  }

  isTailValid() {
    return (
      new Set(Object.keys(this.tail)).size === Object.keys(this.tail).length
    );
  }
}

Fact.InvalidFactException = class InvalidFactException extends Error {
  constructor(fact) {
    super(`Invalid format of fact: ${fact}`);
  }
};

class Function {
  constructor(func) {
    this.func = func;
    if (!this.isValid()) {
      throw new Function.InvalidFunctionException(func);
    }
    this.head = this.getHead();
    this.headWithoutVariables = removeVariables(this.head);
    this.tail = this.getTail();
    this.tailWithoutVariables = this.tail.map(removeVariables);
  }

  isValid() {
    const pattern =
      /^[a-z]\(([a-z],)*[a-z]\)=\([a-z]\([a-z]\)~>[a-z]\([a-z]\)\)$/;
    return pattern.test(this.func);
  }

  getHead() {
    const headTailPattern = /^(.+)=(.*)$/;
    return this.func.match(headTailPattern)[1];
  }

  getTail() {
    const headTailPattern = /^(.+)=(.*)$/;
    const pairsStr = this.func.match(headTailPattern)[2];
    return pairsStr.slice(1, -1).split("~>");
  }
}

Function.InvalidFunctionException = class InvalidFunctionException extends (
  Error
) {
  constructor(func) {
    super(`Invalid format of function: ${func}`);
  }
};

module.exports = {
  removeVariables,
  Fact,
  Function,
};
