class World {
    constructor(rootId, width=25, height=25, rules='k', type='PLANE', colors='rgbk', mapConfig=undefined, taskId=undefined, isStepper=false) {
        this.pallet = {
            'r': '#f00f',
            'g': '#0f0f',
            'b': '#00ff',
            'k': '#555',
        };
        this.colors = colors;

        this.taskId = taskId;

        this.isStepper = isStepper;

        this.canvas = document.getElementById(rootId);
        this.canvas.height = this.canvas.width = 500;
        this.ctx = this.canvas.getContext('2d');

        this.init(width, height, new ConstantRule('k'));

        this.loopSet = false;

        this.canvas.addEventListener('click', this.canvasClick.bind(this));
        this.canvas.addEventListener('contextmenu', this.canvasRightClick.bind(this));

        if (type=='TORUS') this.switchToTorus();
        else this.switchToPlane();
        this.selectColor('g');

        this.historyLength = 3;

        if (mapConfig) this.onLoadFile(mapConfig, false);

        this.loaded = false;

        this.loadSource(editor, false);
    }

    init(width, height, rules){
        this.width = width;
        this.height = height;

        this.automata = new Automata(width, height, rules);
        this.automata.fill;

        this.clear();
        this.drawTable();

        this.levelBackup = null;
        this.levelHistory = [];
    }

    // Time controlling methods ------------------------------------------------------
    tableToString(){
        const table = this.automata.getCurrentTable();
        let data = ""
        for (let j=0; j<this.height; j++){
            for (let i=0; i<this.width; i++){
                data += table[i][j]
            }
            data += '\n'
        }
        return data;
    }

    nextTick(){
        if (this.isStepper) {
            $('#console-info').text('Počítám další krok...');
            $('#console-info').removeClass('warning');
            $.ajax({
                type: 'POST',
                url: '/task/' + this.taskId + '/step',
                data: JSON.stringify({
                    grid: this.tableToString(),
                }),
                contentType: "application/json",
                dataType: "json",
                headers: {
                    "X-CSRFToken": CSRF_TOKEN,
                },
                success: ((response)=>{
                    let grid_pure_text = response.grid;

                    for (let j=0; j<this.height; j++){
                        for (let i=0; i<this.width; i++){
                            this.automata.setCell(grid_pure_text[i + (this.width+1) * j], i, j);
                        }
                    }
                    $('#console-info').text('Krok proveden.');
                    $('#console-info').removeClass('warning');
                    this.drawTable();
                }),
                error: ((xhr)=>{
                    $('#console-info').text(xhr.responseText);
                    $('#console-info').addClass('warning');
                })
            });
        } else {
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
    }

    oneTick(){
        this.stop();
        this.nextTick();
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

        this.loop = setInterval(this.nextTick.bind(this), 100);
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
        this.stop();
        this.automata.isTorus = false;

        $('#torus-btn').removeClass('selected');
        $('#plane-btn').addClass('selected');
    }

    switchToTorus() {
        this.stop();
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
        this.ctx.clearRect(px, py, 0.9*dx, 0.9*dy);
        this.ctx.fillRect(px, py, 0.9*dx, 0.9*dy);
    }

    drawTable(){
        this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
        const table = this.automata.getCurrentTable()

        for (let x = 0; x<this.width; x++) {
            for (let y = 0; y<this.height; y++) {
                const val = table[x][y]
                this.drawSquare(x, y, this.pallet[val]);
            }
        }
    }

    loadSource(editor, submit_info_elem, resize=true) {
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
            url: '/rules/parse',
            data: JSON.stringify({
                expr: src,
                color: this.colors,
                task: this.taskId,
            }),
            contentType: "application/json",
            dataType: "json",
            headers: {
                "X-CSRFToken": CSRF_TOKEN,
            },
            success: ((data)=>{
                const rules = Rule.deserialize(data);
                this.automata.setRules(rules);
                
                $('#'+submit_info_elem).text = "Kód v textovém editoru se neshoduje s načteným kódem v simulaci. Bude odeslán kód z textového editoru.";
                $('#'+submit_info_elem).addClass("warning");

                $('#console-info').text('Kód načten.');
                $('#console-info').removeClass('warning');
            }),
            error: ((xhr)=>{
                $('#console-info').text(xhr.responseText);
                $('#console-info').addClass('warning');
            })
        });

        const newWidth = Math.floor($('#width-input').val());
        const newHeight = Math.floor($('#height-input').val());

        if (resize && (newWidth != this.width || newHeight != this.height)){
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

    canvasRightClick(event){
        event.preventDefault();
        const x = Math.floor(event.offsetX * this.width / this.canvas.scrollWidth);
        const y = Math.floor(event.offsetY * this.height / this.canvas.scrollHeight);
        let col = this.automata.getCell(x, y);
        let col_index = (this.colors.indexOf(col) + 1) % this.colors.length;
        col = this.colors[col_index];
        this.automata.setCell(col, x, y);
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

    isColor(char) {
        return this.pallet.hasOwnProperty(char);
    }

    readMapFromString(input) {
    }

    onLoadFile(input_text, info_elem) {
        let readLine = line => line.split("").filter(ch => ch.match(/\S/));
        let lines = input_text.split('\n').map(readLine).filter(arr => arr.length > 0);

        for (let x = 0; x < lines.length; x++) {
            for (let y = 0; y < lines[x].length; y++) {
                if (!this.isColor(lines[x][y])) {
                    if (info_elem) info_elem.innerHTML = "Unexpected symbol '" + lines[x][y] + "' in line " + (x + 1) + ", pos " + (y + 1) + ".";
                    if (info_elem) info_elem.innerHTML += "This is NOT counting empty lines and empty characters.";
                    if (info_elem) info_elem.classList.add("warning");
                    console.log("Unexpected symbol '" + lines[x][y] + "' in line " + (x + 1) + ", pos " + (y + 1) + ".");
                    return;
                }
            }
        }

        if (lines.length != this.height)
        {
            if (info_elem) info_elem.innerHTML = "Wrong number of lines (expected " + this.height + ", but got " + lines.length + " non-empty lines)";
            if (info_elem) info_elem.classList.add("warning");
            console.log("Wrong number of lines (expected " + this.height + ", but got " + lines.length + " non-empty lines)");
            return;
        }

        for (let i = 0; i < lines.length; i++) {
            if (lines[i].length != this.width) {
                if (info_elem) info_elem.innerHTML = "Wrong number of letters in line " + (i + 1) + " (expected " + this.width + ", but got " + lines[i].length + ").";
                if (info_elem) info_elem.innerHTML += "This is NOT counting empty lines and empty characters.";
                if (info_elem) info_elem.classList.add("warning");
                console.log("Wrong number of letters in line " + (i + 1) + " (expected " + this.width + ", but got " + lines[i].length + ").");
                return;
            }
        }

        this.stop();
        this.automata.setTableTransposed(lines);
        this.drawTable();

        if (info_elem) info_elem.classList.remove("warning");
        if (info_elem) info_elem.innerHTML = "Load successful";
    }

    downloadMap() {
        let mapStr = this.automata.getString();

        let element = document.createElement('a');
        element.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(mapStr));
        element.setAttribute('download', "map.txt");

        element.style.display = 'none';

        document.body.appendChild(element);
        element.click();
        document.body.removeChild(element);
    }

    submit(info_id, editor) {
        let info_elem = $('#' + info_id);
        info_elem.text("Zpracovávám...");
        info_elem.removeClass("warning");

        $.ajax({
            type: 'POST',
            url: '/task/' + this.taskId + '/submit',
            data: JSON.stringify({
                rules: editor.getValue(),
                grid: this.tableToString(),
            }),
            contentType: "application/json",
            dataType: "json",
            headers: {
                "X-CSRFToken": CSRF_TOKEN,
            },
            success: ((data)=>{
                if (data.ok) {
                    info_elem.removeClass("warning");
                } else {
                    info_elem.addClass("warning");
                }
                console.log(data)
                $('.remaining_submissions').text(data.submissions_remaining)
                info_elem.text(data.report);
            }),
            error: ((xhr)=>{
                info_elem.text(xhr.responseText + "<br>Pokud si myslíte, že by tu tato chyba neměla být, kontaktujte organizátory.");
                info_elem.addClass("warning");
            })
        });

        
    }
}
