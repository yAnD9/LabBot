let tg = window.Telegram.WebApp;
tg.expand();

function showNotification(message, isError = false) {
    const notification = document.createElement('div');
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        left: 50%;
        transform: translateX(-50%);
        background: ${isError ? '#ff4444' : '#8A2BE2'};
        color: white;
        padding: 10px 20px;
        border-radius: 10px;
        z-index: 1000;
        font-weight: bold;
    `;
    notification.textContent = message;
    document.body.appendChild(notification);

    setTimeout(() => {
        document.body.removeChild(notification);
    }, 3000);
}

let btnBalet = document.getElementById("btn_balet");
let btnBunker = document.getElementById("btn_bunker");
let btnBeerfactory = document.getElementById("btn_beerfactory");
let btnTheater = document.getElementById("btn_theater");
let btnJesus = document.getElementById("btn_Jesus");
let btnWing = document.getElementById("btn_wing");
let btnRocket = document.getElementById("btn_rocket");
let btnChurch = document.getElementById("btn_church");
let btnPlane = document.getElementById("btn_plane");
let btnMuseum = document.getElementById("btn_museum");

btnBalet.addEventListener("click", function() {
    sendAttractionToBot("Самарский академический театр оперы и балета имени Шостаковича");
});

btnBunker.addEventListener("click", function() {
    sendAttractionToBot("Бункер Сталина");
});

btnBeerfactory.addEventListener("click", function() {
    sendAttractionToBot("Жигулевский пивоваренный завод");
});

btnTheater.addEventListener("click", function() {
    sendAttractionToBot("Самарский академический театр драмы имени Горького");
});

btnJesus.addEventListener("click", function() {
    sendAttractionToBot("Храм Пресвятого Сердца Иисуса");
});

btnWing.addEventListener("click", function() {
    sendAttractionToBot("Монумент Славы в честь работников авиапромышленности");
});

btnRocket.addEventListener("click", function() {
    sendAttractionToBot("Монумент ракета-носитель "Союз"");
});

btnChurch.addEventListener("click", function() {
    sendAttractionToBot("Софийская церковь");
});

btnPlane.addEventListener("click", function() {
    sendAttractionToBot("Памятник штурмовику Ил-2");
});

btnMuseum.addEventListener("click", function() {
    sendAttractionToBot("Самарский областной историко-краеведческий музей");
});

document.addEventListener('DOMContentLoaded', function() {
    document.getElementById("usercard").innerHTML =
        `<div style="text-align: center; padding: 10px;">
            <p> Выберите достопримечательность выше</p>
        </div>`;
});



