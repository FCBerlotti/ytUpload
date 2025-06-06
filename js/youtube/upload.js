(() => {
    setTimeout(() => {
        var createButton = document.querySelector("#create-icon > ytcp-button-shape > button > yt-touch-feedback-shape > div > div.yt-spec-touch-feedback-shape__fill")

        if (createButton) {
            createButton.click(); // Clica no botão se o elemento for encontrado
        } else {
            console.log("Botão não encontrado.");
        }
    }, 0);

    setTimeout(() => {
        var upVideo =  document.querySelector("#text-item-0")
        if (upVideo) {
            upVideo.click(); // Clica no botão se o elemento for encontrado
        } else {
            console.log("Botão não encontrado.");
        }
    }, 2000);
})();
