(() => {
    setTimeout(() => {
        var thumbnail = document.querySelector("#select-button")
        if (thumbnail) {
            thumbnail.click(); 
        } else {
            console.log("Botão não encontrado.");
        }
    }, 0);
})();


