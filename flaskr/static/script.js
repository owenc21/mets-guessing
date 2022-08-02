let guesses = 0;
let resultTable = document.querySelector('#guessTable');


function createRow(jsonData) {
    console.log(jsonData.guess);
    let guessPlayer = jsonData.guess.player;
    let guessBirth = jsonData.guess.birth;
    let guessPos = jsonData.guess.pos;
    let guessAge = jsonData.guess.age;
    let guessBat = jsonData.guess.bat;
    let guessThrow = jsonData.guess.throw;
    let guessHeight = jsonData.guess.height;
    let guessWeight = jsonData.guess.weight;

    let guessRow = resultTable.insertRow();

    let playerCell = guessRow.insertCell();
    playerCell.classList.add(jsonData.adjust.adj_player);
    let playerText = document.createTextNode(guessPlayer);
    playerCell.appendChild(playerText);

    let birthCell = guessRow.insertCell();
    birthCell.classList.add(jsonData.adjust.adj_birth);
    let birthText = document.createTextNode(guessBirth);
    birthCell.appendChild(birthText);

    let posCell = guessRow.insertCell();
    posCell.classList.add(jsonData.adjust.adj_pos);
    let posText = document.createTextNode(guessPos);
    posCell.appendChild(posText);

    let ageCell = guessRow.insertCell();
    ageCell.classList.add(jsonData.adjust.adj_age);
    let ageText = document.createTextNode(guessAge);
    ageCell.appendChild(ageText);

    let batCell = guessRow.insertCell();
    batCell.classList.add(jsonData.adjust.adj_bat);
    let batText = document.createTextNode(guessBat);
    batCell.appendChild(batText);

    let throwCell = guessRow.insertCell();
    throwCell.classList.add(jsonData.adjust.adj_throw);
    let throwText = document.createTextNode(guessThrow);
    throwCell.appendChild(throwText);

    let heightCell = guessRow.insertCell();
    heightCell.classList.add(jsonData.adjust.adj_height);
    let heightText = document.createTextNode(guessHeight);
    heightCell.appendChild(heightText);

    let weightCell = guessRow.insertCell();
    weightCell.classList.add(jsonData.adjust.adj_weight);
    let weightText = document.createTextNode(guessWeight);
    weightCell.appendChild(weightText);

    if (jsonData.adjust.correct === true) {
        alert("You won in " + (guesses + 1) + " guess!");
        guesses = 8;
    }
}


function getResult(guess) {
    fetch('/genresult?player=' + guess).then((response) => {
        return response.json();
    }).then((jsonData) => {
        if (guesses < 8) {
            try {
                if (jsonData.error === "not a met player") {
                    alert("Please Enter a Mets' Player");
                }
                else {
                    createRow(jsonData);
                    guesses++;
                }
            }
            catch (err) {
                console.log(err);
            }
        }
        else {
            alert("You're out of guesses!")
        }
        
    });
}


let inp = document.getElementById("guessTextBox");
inp.addEventListener('keypress', function(e){
    if (e.key == 'Enter') {
        let playerGuess = inp.value;
        getResult(playerGuess);
        inp.value = "";
    }
});
