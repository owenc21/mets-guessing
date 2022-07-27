let guesses = 0;

function getResult(guess) {
    fetch('/genresult?player=' + guess).then((response) => {
        return response.json();
    }).then((myJson) => {
        console.log(myJson.player);
    });
}


let inp = document.getElementById("guessTextBox");
inp.addEventListener('keypress', function(e){
    if (e.key == 'Enter') {
        let playerGuess = inp.value;
        getResult(playerGuess);
        guesses++;
        inp.value = "";
    }
});
