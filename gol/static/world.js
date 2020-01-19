class World {
    constructor(width, height, rootId, rules) {
        this.pallet = {
            'r': '#f00f',
            'g': '#0f0f',
            'b': '#00ff',
            'k': '#555',
        };

        this.canvas = document.getElementById(rootId);
        this.canvas.height = this.canvas.width = 500;
        this.ctx = this.canvas.getContext('2d');

        this.init(width, height, rules);

        this.loopSet = false;

        this.canvas.addEventListener('click', this.canvasClick.bind(this), false);

        this.switchToPlane();
        this.selectColor('g');

        this.historyLength = 3;
    }

    init(width, height, rules){
        this.width = width;
        this.height = height;

        this.automata = new Automata(width, height, rules);
        this.automata.fill

        this.clear();
        this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
        this.drawTable();

        this.levelBackup = null;
        this.levelHistory = [];
    }
    
    // Time controlling methods ------------------------------------------------------
    nextTick(){
        this.stop();

        const table = this.automata.getCurrentTable();
        const level = Array(table.length);
        for (let x = 0; x < table.length; x++) {
            level[x] = Array(table[x].length);
            for (let y = 0; y < table[x].length; y++) {
                level[x][y] = table[x][y];
            }
        }
        this.levelHistory.push(level);
        if (this.levelHistory.length > this.historyLength) {
            this.levelHistory.shift()
        }

        this.automata.nextTick();
        this.drawTable();
    }

    prevTick(){
        this.stop();

        if (this.levelHistory.length == 0) return;
        const level = this.levelHistory.pop();
        this.automata.setTable(level);

        this.drawTable();
    }

    run() {
        if (this.loopSet) return;

        this.loop = setInterval(this.nextTick.bind(this), 200);
        this.loopSet = true;
    }

    stop() {
        if (!this.loopSet) return;

        clearInterval(this.loop);
        this.loopSet = false;
    }

    save() {
        const table = this.automata.getCurrentTable();
        this.levelBackup = Array(table.length);
        for (let x = 0; x < table.length; x++) {
            this.levelBackup[x] = Array(table[x].length);
            for (let y = 0; y < table[x].length; y++) {
                this.levelBackup[x][y] = table[x][y];
            }
        }
        document.getElementById('load-last').disabled = false;
    }

    load() {
        this.stop();

        if (this.levelBackup == null) return;
        this.automata.setTable(this.levelBackup);
        this.drawTable();
    }

    switchToPlane() {
        this.automata.isTorus = false;
        $('#torus-btn').removeClass('selected');
        $('#plane-btn').addClass('selected');
    }

    switchToTorus() {
        this.automata.isTorus = true;

        $('#plane-btn').removeClass('selected');
        $('#torus-btn').addClass('selected');
    }

    selectColor(c){
        this.pickedColor = c;
        $('.color-btn').removeAttr('style')
        $('.color-btn.'+c).css({
            'background-color' : this.pallet[c],
            'color' : c=='k' ? 'white' : 'black', 
        });
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
        this.stop();

        $('#console-info').text('Zpracovávám...');

        const src = editor.getValue();

        if (src.trim().length == 0)
        {
            $('#console-info').text('Prázdný vstup');
            $('#console-info').addClass('warning');
            return;
        }
        
        $.ajax({
            type: 'POST',
            url: '/rules/parse?colors=rgbk',
            data: src,
            dataType: 'text',
            headers: {
                "X-CSRFToken": CSRF_TOKEN,
            },
            success: ((data)=>{
                const rules = Rule.deserialize(JSON.parse(data));
                this.automata.setRules(rules);
                $('#console-info').text('OK');
                $('#console-info').removeClass('warning');
            }),
            error: ((xhr)=>{
                $('#console-info').text(xhr.responseText);
                $('#console-info').addClass('warning');
            })
        });

        const newWidth = Math.floor($('#width-input').val());
        const newHeight = Math.floor($('#height-input').val());

        if (newWidth != this.width || newHeight != this.height){
            this.init(newWidth, newHeight, this.automata.rules);
            this.drawTable();
        }
    }

    canvasClick(event){
        const x = Math.floor(event.offsetX * this.width / this.canvas.scrollWidth);
        const y = Math.floor(event.offsetY * this.height / this.canvas.scrollHeight);
        this.automata.setCell(this.pickedColor, x, y);
        this.drawTable();
    }

    clear() {
        this.stop();

        this.automata.fill('k');
        this.drawTable();
    }

    fill() {
        this.stop();

        this.automata.fill(this.pickedColor);
        this.drawTable();
    }

    onLoadFile(input_text, info_elem) {
        if (/*wrong input format*/ false) {
            info_elem.innerHTML = "<b>Chyba při načítání. (Špatný formát)</b><br><br>Pokud byste měli pocit, že váš soubor má správný formát, kontaktujte organizátory.";
        }

        this.stop();

        info_elem.innerHTML = "Loaded:<br>";
        info_elem.innerHTML += input_text;
    }
}