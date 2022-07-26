
function getResult(guess) {
    fetch('/genresult?player=' + guess).then((response) => {
        return response.json()
    }).then((myJson) => {
        return myJson.player;
    });
}


let inp = document.getElementById("guessTextBox");
inp.addEventListener('keypress', function(e){
    if (e.key == 'Enter') {
        let playerGuess = inp.value;
        let result =  await getResult(playerGuess);
        console.log(result);
    }
});
