class MatrixText {
    constructor(canvasId){
        this.canvasId = canvasId
        
        this.pallet = {
            black: '#000',
            black_filter: '#0001',
            green: '#75ffb1',
            red: '#f00',
        }

        this.numbers = {
            1: [
                [0,0,1,1,0],
                [0,1,1,1,0],
                [1,1,1,1,0],
                [1,0,1,1,0],
                [0,0,1,1,0],
                [0,0,1,1,0],
                [0,0,1,1,0],
                [0,0,1,1,0],
                [0,1,1,1,1],
            ],
            2: [
                [0,1,1,1,0],
                [1,1,1,1,1],
                [1,1,0,1,1],
                [0,0,0,1,1],
                [0,0,0,1,1],
                [0,0,1,1,1],
                [1,1,1,1,0],
                [1,1,0,0,0],
                [1,1,1,1,1],
            ],
        }

        // Get the canvas node and the drawing context
        this.canvas = document.getElementById('matrix-chars');
        this.ctx = this.canvas.getContext('2d');
        
        // set the width and height of the canvas
        this.width = this.canvas.width = document.body.offsetWidth;
        this.height = this.canvas.height = document.body.offsetHeight;
        
        // draw a black rectangle of width and height same as that of the canvas
        this.ctx.fillStyle = this.pallet.black;
        this.ctx.fillRect(0, 0, this.width, this.height);
        
        // init character pointers
        this.cols = 100;
        this.colWidth  = this.width / this.cols;
        this.pointers = Array(this.cols);
        this.ptrNum = 5
        for (let i=0; i<this.cols; i++) {
            this.pointers[i] = Array();
            for (let j=0; j<this.ptrNum; j++){
                this.pointers[i].push(j*20);
            }
        }

        // init color mapping for characters
        this.colorMap = Array(this.cols);
        for (let i=0; i<this.cols; i++) {
            this.colorMap[i] = Array(100);
            for (let j=0; j<this.cols; j++) {
                this.colorMap[i][j] = this.pallet.green;
            }
        }

        this.addButton(6, 6, 1);
        this.addButton(16, 6, 2);

        this.run()
    }
    
    run() {
        if (this.matrixRunning) return;
        this.matrixRunning = true;
        this.interval = setInterval(this.matrixLoop.bind(this), 100);
    }

    stop() {
        if (!this.matrixRunning) return;
        this.matrixRunning = false;
        window.clearInterval(this.interval);
    }

    addButton(x, y, number) {
        const numberWidth = 5;
        const numberheight = 9;
        for (let i=0; i<numberWidth; i++) {
            for (let j=0; j<numberheight; j++) {
                this.colorMap[x+i][y+j] = this.numbers[number][j][i] ? this.pallet.red : this.pallet.green;
            }    
        }
    }

    matrixLoop() {
        // Draw a semitransparent black rectangle on top of previous drawing
        this.ctx.fillStyle = this.pallet.black_filter;
        this.ctx.fillRect(0, 0, this.width, this.height);
      
        // Set font to 15pt monospace in the drawing context
        const fontSize = this.colWidth * 0.6 * (1 + 0. * Math.random());
        this.ctx.font = fontSize + 'pt monospace';
      
        // for each column put a random character at the end
        this.pointers.forEach((yPts, x) => {
            yPts.forEach((y, index) =>{
                // generate a random character
                const text = String.fromCharCode(Math.random() * (255-20) + 20);
            
                // x coordinate of the column, y coordinate is already given
                const xPos = x * this.colWidth;
                const yPos = (y+1) * this.colWidth;
                // render the character at (x, y)
                this.ctx.fillStyle = this.colorMap[x][y];
                // if (this.colorMap[x][y] == this.pallet.red){
                //     this.ctx.fillRect(xPos-0.2*this.colWidth, yPos-0.8*this.colWidth, this.colWidth, this.colWidth);
                //     this.ctx.fillStyle = this.pallet.black;
                // }
                this.ctx.fillText(text, xPos, yPos);
            
                // randomly reset the end of the column if it's at least 100px high
                if (y > 5 + Math.min(Math.random() * 5000, 80)) this.pointers[x][index] = 0;
                // otherwise just move the y coordinate for the column 20px down,
                else this.pointers[x][index] = y + 1;
            })
        });
    }
}    
