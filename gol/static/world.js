class World {
    constructor(width, height, rootId, rules) {
        this.width = width;
        this.height = height;
        this.root = $("#" + rootId);

        this.automata = new Automata(25, 25, rules);
        
        this.initTableImage();

        this.loopSet = false;
    }    
    
    tick(){
        this.automata.nextTick();
        this.drawTable();
    }

    run() {
        if (this.loopSet) return;

        this.loop = setInterval(this.tick.bind(this), 200);
        this.loopSet = true;
    }

    stop() {
        if (!this.loopSet) return;

        clearInterval(this.loop);
        this.loopSet = false;
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

    loadSource(srcId) {
        document.getElementById('parse-info').innerHTML = 'Zpracovávám...';
        const src = $('#' + srcId).val();
        $.ajax({
            type: 'POST',
            url: '/rules/parse',
            data: src,
            dataType: 'text',
            headers: {
                "X-CSRFToken": CSRF_TOKEN,
            },
            success: ((data)=>{
                const rules = Rule.deserialize(JSON.parse(data));
                this.automata.setRules(rules);
                document.getElementById('parse-info').innerHTML = 'OK';
            }),
            error: ((xhr)=>{
                document.getElementById('parse-info').innerHTML = xhr.responseText;
            }).bind(this)
        });
    }
}

class BWWorld extends World {
    constructor(width, height, rootId, ruleSet) {
        super(width, height, rootId, ruleSet);

        this.automata.fill('w');

        this.pallet = {
            'w': 'rgba(255, 255, 255, 0.5)',
            'b': 'rgba(255, 255, 255, 0.1)',
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

    clear() {
        this.automata.fill('w');
        this.drawTable();
    }

    fill() {
        this.automata.fill('b');
        this.drawTable();
    }
}
