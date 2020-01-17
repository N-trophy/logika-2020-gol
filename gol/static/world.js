class World {
    constructor(width, height, rootId, rules, colors) {
        this.pallet = {
            'w': 'rgba(255, 255, 255, 0.5)',
            'b': 'rgba(255, 255, 255, 0.1)',
        };

        this.colors = colors;

        this.width = width;
        this.height = height;
        this.canvas = document.getElementById(rootId);
        this.canvas.height = this.canvas.width = 500;
        this.ctx = this.canvas.getContext('2d');

        this.automata = new Automata(25, 25, rules);
        this.automata.fill

        this.clear();
        this.drawTable();

        this.loopSet = false;

        this.canvas.addEventListener('click', this.canvasClick.bind(this), false);
    }    
    
    // Time controlling methods ------------------------------------------------------
    nextTick(){
        this.automata.nextTick();
        this.drawTable();
    }

    prevTick(){
        this.automata.nextTick();
        this.drawTable();
    }

    run() {
        if (this.loopSet) return;

        this.loop = setInterval(this.nextTick.bind(this), 200);
        this.loopSet = true;

        this.canvas.addClass('running')
    }

    stop() {
        if (!this.loopSet) return;

        clearInterval(this.loop);
        this.loopSet = false;

        this.root.removeClass('running')
    }


    // Drawing methods ----------------------------------------------------------------    
    drawSquare(x, y, color){
        const px = x * this.canvas.width / this.width;
        const py = y * this.canvas.height / this.height;
        const dx = this.canvas.width / this.width;
        const dy = this.canvas.height / this.height;
        this.ctx.fillStyle = color;
        this.ctx.clearRect(px, py, dx-3, dy-3);
        this.ctx.fillRect(px, py, dx-3, dy-3);
    }
    
    drawTable(){
        const table = this.automata.getCurrentTable()

        for (let x = 0; x<this.width; x++) {
            for (let y = 0; y<this.height; y++) {
                const val = table[x][y]
                this.drawSquare(x, y, this.pallet[val]);
            }
        }
    }

    loadSource(editor) {
        $('#console-info').text('Zpracovávám...');

        const src = editor.getValue()
        
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
                $('#console-info').text('OK');
                $('#console-info').removeClass('w3-red')
                $('#console-info').addClass('w3-green')
            }),
            error: ((xhr)=>{
                $('#console-info').text(xhr.responseText);
                $('#console-info').removeClass('w3-green')
                $('#console-info').addClass('w3-red')
            })
        });
    }

    canvasClick(event){
        const x = Math.floor(event.offsetX * this.width / this.canvas.scrollWidth);
        const y = Math.floor(event.offsetY * this.height / this.canvas.scrollHeight);
        this.toggle(x, y);
    }

    toggle(x, y) {
        const a = this.colors[0];
        const b = this.colors[1];
        this.automata.setCell(this.automata.getCell(x, y) == a ? b : a, x, y);
        this.drawTable();
    }

    clear() {
        this.automata.fill(this.colors[0]);
        this.drawTable();
    }

    fill() {
        this.automata.fill(this.colors[1]);
        this.drawTable();
    }
}