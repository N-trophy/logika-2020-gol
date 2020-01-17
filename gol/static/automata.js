class Automata {
    constructor(width, height, rules) {
        this.tables = [new Array(width), new Array(width)];
        this.tick = 0;

        this.width = width;
        this.height = height;
        
        this.rules = rules

        for (let i = 0; i < width; i++) {
            this.tables[0][i] = new Array(height);
            this.tables[1][i] = new Array(height);
        }

        this.fill(0);

        this.isTorus = true;
    }

    nextTick(){
        this.tick++;

        for (let x=0; x<this.width; x++){
            for (let y=0; y < this.height; y++){
                this.tables[this.tick % 2][x][y] = this.rules.eval(this.tables[(this.tick + 1) % 2], x, y, this.isTorus);
            }
        }
    }

    fill(char){
        for (let x = 0; x < this.width; x++) {
            for (let y = 0; y < this.height; y++) {
                this.tables[0][x][y] = this.tables[1][x][y] = char;
            }
        }
    }

    setCell(char, x, y) {
        this.tables[0][x][y] = this.tables[1][x][y] = char;
    }

    getCell(x, y) {
        return this.tables[this.tick % 2][x][y];
    }

    writeOut(){
        for (let y = 0; y < this.height; y++) {
            let line = "";
            for (let x = 0; x < this.width; x++) {
                line += this.tables[this.tick % 2][x][y];
            }
            console.log(line);
        }
    }

    getCurrentTable(){
        return this.tables[this.tick % 2];
    }

    setTable(table){
        for (let y = 0; y < this.height; y++) {
            for (let x = 0; x < this.width; x++) {
                this.tables[this.tick % 2][x][y] = table[x][y];
            }
        }
    }

    setRules(rules){
        this.rules = rules;
    }
}

// Selectors ------------------------------------------------------------------------------------------
class Selector {
    constructor(){
    }

    match_table(){
    }
}


class GridSelector extends Selector {
    constructor(cells) {
        super()
        this.cells = cells;
    }

    match_table(table, x, y, isTorus) {
        let s = 0;
        let p = 0;
        
        for (let j=-1; j<=1; j++) {
            for (let i=-1; i<=1; i++) {
                p++;

                if (isTorus) {
                    const w = table.length;
                    const h = table[0].length;

                    const px = (x+i+w) % w;
                    const py = (y+j+h) % h;

                    if (this.cells[p-1] == table[px][py]) s++;
                } else {
                    if (x+i < 0 || y+j < 0 || x+i >= table.length || y+j >= table[0].length) continue;
                    if (this.cells[p-1] == table[x+i][y+j]) s++;
                }
            } 
        }
        
        return s;
    }
}

class ConstantSelector extends Selector {
    constructor(value){
        super()
        this.value = value;
    }

    match_table(table, x, y, isTorus) {
        return this.value;
    }
}

class OperationSelector extends Selector {
    constructor(op, ...operands){
        super()
        this.op = this.getOperator(op);
        this.operands = operands;
    }

    match_table(table, x, y, isTorus) {
        let results = this.operands.map(o=>o.match_table(table, x, y, isTorus))
        let first = results.shift()
        return results.reduce(this.op, first)
    }

    getOperator(op){
        if (cmpName == '*') return (a,b)=>{a * b}
        if (cmpName == '/') return (a,b)=>{a / b}
        if (cmpName == '%') return (a,b)=>{a % b}
        if (cmpName == '+') return (a,b)=>{a + b}
        if (cmpName == '-') return (a,b)=>{a - b}
    }
}


// Logical expressions -----------------------------------------------------------------------------
class BoolExpr {
    eval(table, x, y, isTorus) {}
}

class Comparator extends BoolExpr {
    constructor(cmp, ...operands) {
        super()
        this.operands = operands;
        this.cmp = Comparator.getComparator(cmp);
    }

    eval(table, x, y, isTorus) {        
        let results = this.operands.map(o=>o.match_table(table, x, y, isTorus))
        let good = true;
        for (let i=0;i<results.length-1;i++){
            good &= this.cmp(results[i], results[i+1])
        }
        return good;
    }

    static getComparator(cmpName){
        if (cmpName == "<=") return ((x,y) => x <= y);
        if (cmpName == "<") return ((x,y) => x < y);
        if (cmpName == ">=") return ((x,y) => x >= y);
        if (cmpName == ">") return ((x,y) => x > y);
        if (cmpName == "==") return ((x,y) => x == y);
    }
}

class BoolOperator extends BoolExpr {
    constructor(op, ...operands) {
        super()
        this.op = BoolOperator.getOperator(op);
        this.operands = operands;
    }

    eval(table, x, y, isTorus) {
        let results = this.operands.map(o=>o.eval(table, x, y, isTorus))
        let first = results.shift()
        return results.reduce(this.op, first)
    }

    static getOperator(cmpName){
        if (cmpName == "and") return ((x,y) => x && y);
        if (cmpName == "or") return ((x,y) => x || y);
    }
}

// Rules ----------------------------------------------------------------------------------------------
class Rule {
    eval(table, x, y, isTorus){}

    static deserialize(object) {
        const className = object.className
        const klass = classMap[className]

        object.args = object.args.map((arg, i)=>{
            if ((i>=argsMap[className].length && argsMap[className][argsMap[className].length-1]) || argsMap[className][i]) {
                return Rule.deserialize(arg);
            } else {
                return arg;
            }
        })

        return new klass(...object.args);
    }
}

class ConstantRule extends Rule {
    constructor (value) {
        super();
        this.value = value;
    }

    eval(table, x, y, isTorus) {
        return this.value;
    }
}

class ConditionalRule extends Rule {
    constructor (ifBranch, elseBranch, condition) {
        super();
        this.ifBranch = ifBranch;
        this.elseBranch = elseBranch;
        this.condition = condition;
    }

    eval(table, x, y, isTorus) {
        if (this.condition.eval(table, x, y, isTorus)) {
            return this.ifBranch.eval(table, x, y, isTorus);
        } else {
            return this.elseBranch.eval(table, x, y, isTorus);
        }
    }
}

argsMap = {
    "GridSelector" : [false],
    "ConstantSelector" : [false],
    "OperationSelector" : [false, true],
    "Comparator" : [false, true],
    "BoolOperator" : [false, true],
    "ConstantRule" : [false],
    "ConditionalRule" : [true, true, true]
}

classMap = {
    "GridSelector" : GridSelector,
    "ConstantSelector" : ConstantSelector,
    "OperationSelector" : OperationSelector,
    "Comparator" : Comparator,
    "BoolOperator" : BoolOperator,
    "ConstantRule" : ConstantRule,
    "ConditionalRule" : ConditionalRule,
}
