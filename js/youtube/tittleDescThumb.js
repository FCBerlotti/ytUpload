(() => {
    // Localiza o campo contenteditable que representa o título
    var campoTitulo = document.querySelector('#textbox[contenteditable="true"][aria-label*="Adicione um título"]');

    if (campoTitulo) {
        campoTitulo.innerText = tituloDesejado;

        // Dispara evento de input para notificar o sistema do YouTube
        campoTitulo.dispatchEvent(new InputEvent('input', { bubbles: true }));

        console.log("✅ Título atualizado com sucesso!");
    } else {
        console.log("❌ Campo de título não encontrado.");
    }

    // Seleciona o campo de descrição pelo ID
    var campoDescricao = document.querySelector('div#textbox[contenteditable="true"][aria-label*="Fale sobre seu vídeo"]');

    if (campoDescricao) {
        campoDescricao.innerText = descricaoDesejada;

        // Dispara evento de input para o YouTube reconhecer a mudança
        campoDescricao.dispatchEvent(new InputEvent('input', { bubbles: true }));

        console.log("✅ Descrição atualizada com sucesso!");
    } else {
        console.log("❌ Campo de descrição não encontrado.");
    }

    var thumbnail = document.querySelector("#select-button")
    if (thumbnail) {
        thumbnail.click(); 
    } else {
        console.log("Botão não encontrado.");
    }
})();