<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Calculator</title>

<style>
    body {
        margin: 0;
        font-family: Arial, sans-serif;
        display: flex;
        height: 100vh;
        transition: 0.3s;
    }

    /* Sidebar */
    .sidebar {
        width: 220px;
        padding: 20px;
        background-color: #1e1e1e;
        color: white;
        transition: 0.3s;
    }

    .sidebar.light {
        background-color: #f1f1f1;
        color: black;
    }

    .sidebar h2 {
        margin-bottom: 20px;
    }

    .sidebar button {
        width: 100%;
        padding: 12px;
        border: none;
        margin: 6px 0;
        font-size: 16px;
        cursor: pointer;
        border-radius: 6px;
    }

    /* Calculator area */
    .calculator {
        flex: 1;
        display: flex;
        justify-content: center;
        align-items: center;
        background-color: #121212;
        transition: 0.3s;
    }

    .calculator.light {
        background-color: white;
    }

    .calc-box {
        background-color: #222;
        padding: 20px;
        border-radius: 12px;
        width: 320px;
        transition: 0.3s;
    }

    .calc-box.light {
        background-color: #e8e8e8;
    }

    input {
        width: 100%;
        font-size: 22px;
        padding: 15px;
        text-align: right;
        border: none;
        border-radius: 8px;
        margin-bottom: 20px;
    }

    /* Buttons */
    .btn-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 12px;
    }

    button.calc-btn {
        padding: 18px;
        font-size: 18px;
        border: none;
        border-radius: 10px;
        cursor: pointer;
        background-color: #3a3a3a;
        color: white;
        transition: 0.3s;
    }

    .light button.calc-btn {
        background-color: #d2d2d2;
        color: black;
    }

    .operator {
        background-color: #ff9500 !important;
        color: white !important;
    }

</style>
</head>
<body>

<!-- Sidebar -->
<div class="sidebar" id="sidebar">
    <h2>Modes</h2>
    <button onclick="setOperation('+')">Addition (+)</button>
    <button onclick="setOperation('-')">Subtraction (-)</button>
    <button onclick="setOperation('*')">Multiplication (×)</button>
    <button onclick="setOperation('/')">Division (÷)</button>
    <button onclick="setOperation('^')">Power (^)</button>
    <hr>
    <button onclick="toggleTheme()">Toggle Light/Dark</button>
</div>

<!-- Calculator -->
<div class="calculator" id="calc-area">
    <div class="calc-box" id="calc-box">
        <input type="text" id="display" disabled>

        <div class="btn-grid">
            <button class="calc-btn" onclick="append('7')">7</button>
            <button class="calc-btn" onclick="append('8')">8</button>
            <button class="calc-btn" onclick="append('9')">9</button>
            <button class="calc-btn operator" onclick="append('/')">÷</button>

            <button class="calc-btn" onclick="append('4')">4</button>
            <button class="calc-btn" onclick="append('5')">5</button>
            <button class="calc-btn" onclick="append('6')">6</button>
            <button class="calc-btn operator" onclick="append('*')">×</button>

            <button class="calc-btn" onclick="append('1')">1</button>
            <button class="calc-btn" onclick="append('2')">2</button>
            <button class="calc-btn" onclick="append('3')">3</button>
            <button class="calc-btn operator" onclick="append('-')">−</button>

            <button class="calc-btn" onclick="append('0')">0</button>
            <button class="calc-btn" onclick="append('.')">.</button>
            <button class="calc-btn" onclick="calculate()">=</button>
            <button class="calc-btn operator" onclick="append('+')">+</button>
        </div>

    </div>
</div>

<script>

let display = document.getElementById("display");
let currentOperation = "";

function append(val) {
    display.value += val;
}

function setOperation(op) {
    display.value = "";
    currentOperation = op;
}

function calculate() {
    try {
        if (currentOperation === "^") {
            let parts = display.value.split("^");
            display.value = Math.pow(parseFloat(parts[0]), parseFloat(parts[1]));
        } else {
            display.value = eval(display.value);
        }
    } catch {
        display.value = "Error";
    }
}

function toggleTheme() {
    let body = document.body;
    let sidebar = document.getElementById("sidebar");
    let calcArea = document.getElementById("calc-area");
    let calcBox = document.getElementById("calc-box");

    body.classList.toggle("light");
    sidebar.classList.toggle("light");
    calcArea.classList.toggle("light");
    calcBox.classList.toggle("light");
}

</script>

</body>
</html>
