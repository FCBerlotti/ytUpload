(() => {
    setTimeout(() => {
    var openProgramar = document.querySelector("#second-container-expand-button")
        if (openProgramar) {
            openProgramar.click(); 
        } else {
            console.log("Botão não encontrado.");
        }
    }, 1000);

    setTimeout(() => {
        var openDateProgramar = document.querySelector("#datepicker-trigger > ytcp-dropdown-trigger > div")
        if (openDateProgramar) {
            openDateProgramar.click(); 
        } else {
            console.log("Botão não encontrado.");
        }
    }, 3000);
})();