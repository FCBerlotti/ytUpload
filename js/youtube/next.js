(() => {

    setTimeout(() => {
        var next1 = document.querySelector("#next-button")
        if (next1) {
            next1.click(); 
        } else {
            console.log("Botão não encontrado.");
        }
    }, 0);

    setTimeout(() => {
        var next2 = document.querySelector("#next-button")
        if (next2) {
            next2.click(); 
        } else {
            console.log("Botão não encontrado.");
        }
    }, 1500);

})();