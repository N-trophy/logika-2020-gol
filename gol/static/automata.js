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
    }

    nextTick(){
        this.tick++;

        for (let x=0; x<this.width; x++){
            for (let y=0; y < this.height; y++){
                this.tables[this.tick % 2][x][y] = this.rules.eval(this.tables[(this.tick + 1) % 2], x, y);
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

    match_table(table, x, y) {
        let s = 0;
        let p = 0;
        
        for (let j=-1; j<=1; j++) {
            for (let i=-1; i<=1; i++) {
                p++;
                if (x+i < 0 || y+j < 0 || x+i >= table.length || y+j >= table[0].length) continue;
                if (this.cells[p-1] == table[x+i][y+j]) s++;
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

    match_table(table, x, y) {
        return this.value;
    }
}


// Logical expressions -----------------------------------------------------------------------------
class BoolExpr {
    eval(table, x, y) {}
}

class Comparator extends BoolExpr {
    constructor(left, right, cmp) {
        super()
        this.left = left;
        this.right = right;
        this.cmp = Comparator.getComparator(cmp);
    }

    eval(table, x, y) {
        return this.cmp(this.left.match_table(table, x, y), this.right.match_table(table, x, y));
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
    constructor(left, right, op) {
        super()
        this.left = left;
        this.right = right;
        this.op = BoolOperator.getOperator(op);
    }

    eval(table, x, y) {
        return this.op(this.left.eval(table, x, y), this.right.eval(table, x, y));
    }

    static getOperator(cmpName){
        if (cmpName == "and") return ((x,y) => x && y);
        if (cmpName == "or") return ((x,y) => x || y);
    }
}

// Rules ----------------------------------------------------------------------------------------------
class Rule {
    eval(table, x, y){}

    static deserialize(object) {
        const klass = classMap[object.className]

        for (let i=0; i < argsMap[object.className].length; i++) {
            if (argsMap[object.className][i]) {
                object.args[i] = Rule.deserialize(object.args[i]);
            }
        }

        return new klass(...object.args);
    }
}

class ConstantRule extends Rule {
    constructor (value) {
        super();
        this.value = value;
    }

    eval(table, x, y) {
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

    eval(table, x, y) {
        if (this.condition.eval(table, x, y)) {
            return this.ifBranch.eval(table, x, y);
        } else {
            return this.elseBranch.eval(table, x, y);
        }
    }
}

argsMap = {
    "GridSelector" : [false],
    "ConstantSelector" : [false],
    "Comparator" : [true, true, false],
    "BoolOperator" : [true, true, false],
    "ConstantRule" : [false],
    "ConditionalRule" : [true, true, true]
}

classMap = {
    "GridSelector" : GridSelector,
    "ConstantSelector" : ConstantSelector,
    "Comparator" : Comparator,
    "BoolOperator" : BoolOperator,
    "ConstantRule" : ConstantRule,
    "ConditionalRule" : ConditionalRule,
}
