window.popupPhotos360HTML =
    '<b class="titleb">Photos 360°</b><hr class="titlehr">' +
    '<input type="text" id="filterPhotos360" style="width:100%;box-sizing:border-box;" placeholder="Filtrer..." onkeyup="var f=sansAccents(this.value.toLowerCase());var a=document.getElementById(\'photos360List\').getElementsByTagName(\'a\');for(var i=0;i<a.length;i++)a[i].parentNode.style.display=sansAccents(a[i].textContent.toLowerCase()).indexOf(f)>=0?\'\':\'none\';">' +
    '<div id="photos360List">' +
    '<ul>' +
    '<li><a href="?file=../photos360/camping_cilaos_20230210_061857.jpg">camping_cilaos_20230210_061857.jpg</a></li>' +
    '<li><a href="?file=../photos360/camping_cilaos_20230210_091203.jpg">camping_cilaos_20230210_091203.jpg</a></li>' +
    '<li><a href="?file=../photos360/cryptomeria_la_nouvelle_20231207_153847.jpg">cryptomeria_la_nouvelle_20231207_153847.jpg</a></li>' +
    '<li><a href="?file=../photos360/cryptomeria_la_nouvelle_20231208_092010.jpg">cryptomeria_la_nouvelle_20231208_092010.jpg</a></li>' +
    '<li><a href="?file=../photos360/grand_brule_20210430_120657.jpg">grand_brule_20210430_120657.jpg</a></li>' +
    '<li><a href="?file=../photos360/grand_brule_20221104_172848.jpg">grand_brule_20221104_172848.jpg</a></li>' +
    '<li><a href="?file=../photos360/observatoire_des_makes_20230904_103401.jpg">observatoire_des_makes_20230904_103401.jpg</a></li>' +
    '<li><a href="?file=../photos360/ravine_blanche_20261004_131931.jpg">ravine_blanche_20261004_131931.jpg</a></li>' +
    '<li><a href="?file=../photos360/st_philippe_port_20221028_181030.jpg">st_philippe_port_20221028_181030.jpg</a></li>' +
    '<li><a href="?file=../photos360/stjoseph_ancienne_usine_20260926_135034.jpg">stjoseph_ancienne_usine_20260926_135034.jpg</a></li>' +
    '<li><a href="?file=../photos360/stjoseph_jardin20decembre_20240706_122013.jpg">stjoseph_jardin20decembre_20240706_122013.jpg</a></li>' +
    '<li><a href="?file=../photos360/stjoseph_manapany_20230709_161124.jpg">stjoseph_manapany_20230709_161124.jpg</a></li>' +
    '<li><a href="?file=../photos360/stphilippe_20250906_125201.jpg">stphilippe_20250906_125201.jpg</a></li>' +
    '<li><a href="?file=../photos360/strose_anse_des_cascades_20230323_161054.jpg">strose_anse_des_cascades_20230323_161054.jpg</a></li>' +
    '<li><a href="?file=../photos360/strose_anse_des_cascades_20230323_161705.jpg">strose_anse_des_cascades_20230323_161705.jpg</a></li>' +
    '<li><a href="?file=../photos360/strose_anse_des_cascades_20230323_162145.jpg">strose_anse_des_cascades_20230323_162145.jpg</a></li>' +
    '<li><a href="?file=../photos360/strose_anse_des_cascades_20230323_163422.jpg">strose_anse_des_cascades_20230323_163422.jpg</a></li>' +
    '<li><a href="?file=../photos360/strose_port_20230930_113820.jpg">strose_port_20230930_113820.jpg</a></li>' +
    '<li><a href="?file=../photos360/vincendo_container_20240817_135505.jpg">vincendo_container_20240817_135505.jpg</a></li>' +
    '</ul>' +
    '</div>';

function sansAccents(str){return str
        .replace(/[àáâãäå]/g, "a")
        .replace(/[ç]/g, "c")
        .replace(/[èéêë]/g, "e")
        .replace(/[ìíîï]/g, "i")
        .replace(/[ñ]/g, "n")
        .replace(/[òóôõö]/g, "o")
        .replace(/[ùúûü]/g, "u")
        .replace(/[ýÿ]/g, "y");
}