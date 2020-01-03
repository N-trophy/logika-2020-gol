class World {
    constructor(width, height, rootId, ruleSet) {
        this.width = width;
        this.height = height;
        this.root = $("#" + rootId);
        this.ruleSet = ruleSet;

        this.automata = new Automata(25, 25, r);

        this.initTableImage();
    }    
    
    tick(){
        this.automata.nextTick();
        this.drawTable();
    }

    run() {
        this.loop = setInterval(this.tick.bind(this), 200);
    }

    stop() {
        clearInterval(this.loop);
    }

    initTableImage(){
        const rows = [];
        const table = this.automata.getCurrentTable();

        table[0].forEach(()=>{
            rows.push($("<tr></tr>"));
        });

        for (let x = 0; x<this.width; x++) {
            for (let y = 0; y<this.height; y++) {
                const cell = $('<td></td>', {
                    id: this.root.attr('id') + '_cell',
                    class: "cell c"+x + " r" + y,
                });

                rows[y].append(cell);
            }
        }

        this.root.append(rows);
    }
    
    
    drawTable(){
        const table = this.automata.getCurrentTable()
        for (let x = 0; x<this.width; x++) {
            for (let y = 0; y<this.height; y++) {
                const id = '#' + this.root.attr('id') + '_cell';
                const val = table[x][y];
                $(id + '.c' + x + '.r' + y).css('background-color', this.pallet[val]);
            }
        }
    }
}

class BWWorld extends World {
    constructor(width, height, rootId, ruleSet) {
        super(width, height, rootId, ruleSet);

        this.automata.fill('w');

        this.pallet = {
            'w': '#eeeeee',
            'b': '#000000',
        };

        for (let x = 0; x<this.width; x++) {
            for (let y = 0; y<this.height; y++) {
                const id = '#' + this.root.attr('id') + '_cell';
                $(id + '.c' + x + '.r' + y).click(()=>this.toggle(x, y));
            }
        }

        this.drawTable();
    }

    toggle(x, y) {
        this.automata.setCell(this.automata.getCell(x, y) == 'w' ? 'b' : 'w', x, y);
        this.drawTable();
    }
}