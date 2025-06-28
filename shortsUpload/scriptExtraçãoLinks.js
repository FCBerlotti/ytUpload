//EXECUTAR NO CONSOLE APOS TODOS OS VIDEOS SEREM CARREGADOS
(function() {
    // 1. Seleciona todos os elementos que contêm os links dos vídeos
    const videoElements = document.querySelectorAll('ytd-rich-item-renderer a#video-title-link');

    // 2. Extrai o atributo 'href' (o link) de cada elemento
    const videoLinks = [...videoElements].map(element => element.href);

    // 3. Exibe os links no console, um por linha
    console.log("--- Links Extraídos ---");
    console.log(videoLinks.join('\n'));
    console.log(`\nTotal de ${videoLinks.length} links encontrados.`);
})();



//EXTRACAO DOS SHORTS
(function() {
    // 1. Seleciona todas as âncoras (<a>) dentro dos elementos de shorts
    // Usamos uma seleção mais ampla para garantir que funcione
    const shortElements = document.querySelectorAll('a.reel-item-endpoint, ytm-shorts-lockup-view-model a');

    // 2. Extrai o 'href', transforma em link completo e remove duplicados
    const shortLinks = [...shortElements].map(element => new URL(element.getAttribute('href'), window.location.origin).href);
    const uniqueLinks = [...new Set(shortLinks)]; // Remove links duplicados

    // 3. Exibe os links no console, um por linha
    console.log("--- Links dos Shorts Extraídos ---");
    console.log(uniqueLinks.join('\n'));
    console.log(`\nTotal de ${uniqueLinks.length} links encontrados.`);
})();