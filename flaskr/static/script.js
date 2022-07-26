function getResult(guess) {
    fetch('/genresult?player=' + guess).then((response) => {
        console.log(response);
        return response.json();
    });
}


let inp = document.getElementById("guessTextBox");
inp.addEventListener('keypress', function(e){
    if (e.key == 'Enter') {
        let playerGuess = inp.value;
        let response = getResult(playerGuess);
        console.log(response);
        inp.value = "";
    }
});
