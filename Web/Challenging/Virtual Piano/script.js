let audio = new Audio("white_keys/A.mp3");

document.addEventListener("keypress", function (event) {
    audio.pause();
    if (event.code === "KeyA") {
        audio = new Audio("white_keys/A.mp3");
        audio.play();
    } else if (event.code === "KeyS") {
        audio = new Audio("white_keys/S.mp3");
        audio.play();
    } else if (event.code === "KeyD") {
        audio = new Audio("white_keys/D.mp3");
        audio.play();
    } else if (event.code === "KeyF") {
        audio = new Audio("white_keys/F.mp3");
        audio.play();
    } else if (event.code === "KeyG") {
        audio = new Audio("white_keys/G.mp3");
        audio.play();
    } else if (event.code === "KeyH") {
        audio = new Audio("white_keys/H.mp3");
        audio.play();
    } else if (event.code === "KeyJ") {
        audio = new Audio("white_keys/J.mp3");
        audio.play();
    } else if (event.code === "KeyW") {
        audio = new Audio("black_keys/W.mp3");
        audio.play();
    } else if (event.code === "KeyE") {
        audio = new Audio("black_keys/E.mp3");
        audio.play();
    } else if (event.code === "KeyT") {
        audio = new Audio("black_keys/T.mp3");
        audio.play();
    } else if (event.code === "KeyY") {
        audio = new Audio("black_keys/Y.mp3");
        audio.play();
    } else if (event.code === "KeyU") {
        audio = new Audio("black_keys/U.mp3");
        audio.play();
    }
});