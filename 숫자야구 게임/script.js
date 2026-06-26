let answer = [];
let attempts = 9;

let number1 = document.getElementById("number1");
let number2 = document.getElementById("number2");
let number3 = document.getElementById("number3");

let attemptsText = document.getElementById("attempts");
let results = document.getElementById("results");
let resultImg = document.getElementById("game-result-img");
let submitButton = document.querySelector(".submit-button");

function make_answer() {
    answer = [];
    while(answer.length < 3) {
        let randomNumber = Math.floor(Math.random() * 10);

        if(!answer.includes(randomNumber)) {
            answer.push(randomNumber);
        }
    }

    console.log(answer);
}

function clear_input() {
    number1.value = "";
    number2.value = "";
    number3.value = "";
    number1.focus();
}

function check_numbers() {
    if(number1.value === "" || number2.value === "" || number3.value === "") {
        clear_input();
        return;
    }

    let userNumber = [
        Number(number1.value),
        Number(number2.value),
        Number(number3.value)
    ];

    attempts = attempts - 1;
    attemptsText.textContent = attempts;

    let strike = 0;
    let ball = 0;

    for(let i = 0; i < 3; i++) {
        if(userNumber[i] === answer[i]) {
            strike = strike + 1;
        } else if(answer.includes(userNumber[i])) {
            ball = ball + 1;
        }
    }

    if(strike === 0 && ball === 0) {
        results.innerHTML = results.innerHTML +
        '<div class="check-result">' +
            '<div class="left">' + userNumber[0] + ' ' + userNumber[1] + ' ' + userNumber[2] + '</div>' +
            '<div>:</div>' +
            '<div class="right">' +
                '<span class="num-result out">O</span>' +
            '</div>' +
        '</div>';
    } else {
        results.innerHTML = results.innerHTML +
        '<div class="check-result">' +
            '<div class="left">' + userNumber[0] + ' ' + userNumber[1] + ' ' + userNumber[2] + '</div>' +
            '<div>:</div>' +
            '<div class="right">' +
                strike +
                '<span class="num-result strike">S</span>' +
                ball +
                '<span class="num-result ball">B</span>' +
            '</div>' +
        '</div>';
    }

    clear_input();

    if(strike === 3) {
        resultImg.src = "success.png";
        resultImg.style.display = "block";
        submitButton.disabled = true;
    } else if(attempts === 0) {
        resultImg.src = "fail.png";
        resultImg.style.display = "block";
        submitButton.disabled = true;
    }
}
make_answer();
attemptsText.textContent = attempts;
results.innerHTML = "";
resultImg.style.display = "none";