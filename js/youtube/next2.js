(() => {

    setTimeout(() => {
        var next3 = document.querySelector("#next-button")
        if (next3) {
            next3.click(); 
        } else {
            console.log("Botão não encontrado.");
        }
    }, 0);

})();