let tg = window.Telegram.WebApp;
tg.expand();
tg.ready();

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
        text-align: center;
    `;
    notification.textContent = message;
    document.body.appendChild(notification);

    setTimeout(() => {
        if (document.body.contains(notification)) {
            document.body.removeChild(notification);
        }
    }, 3000);
}

function sendAttractionToBot(attractionName) {
    console.log('Отправка данных:', attractionName);

    if (window.Telegram && window.Telegram.WebApp) {
        try {
            // Основной способ отправки данных
            tg.sendData(attractionName);
            showNotification(`✓ Отправлено: ${attractionName}`);

            // Дополнительно можно закрыть WebApp после отправки
            setTimeout(() => {
                tg.close();
            }, 1000);

        } catch (error) {
            console.error('Ошибка отправки:', error);
            showNotification('❌ Ошибка отправки', true);
        }
    } else {
        console.log('Тестовый режим:', attractionName);
        showNotification(`Тест: ${attractionName}`);
    }
}

// Инициализация после загрузки DOM
document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM загружен, инициализация кнопок...');

    // Инициализируем usercard
    const usercard = document.getElementById("usercard");
    if (usercard) {
        usercard.innerHTML =
            `<div style="text-align: center; padding: 10px;">
                <p>🎯 Выберите достопримечательность выше</p>
                <p style="font-size: 12px; color: #666;">После высказавания откроется чат с ботом</p>
            </div>`;
    }

    // Маппинг кнопок
    const buttons = {
        "btn_balet": "Самарский академический театр оперы и балета имени Шостаковича",
        "btn_bunker": "Бункер Сталина",
        "btn_beerfactory": "Жигулевский пивоваренный завод",
        "btn_theater": "Самарский академический театр драмы имени Горького",
        "btn_Jesus": "Храм Пресвятого Сердца Иисуса",
        "btn_wing": "Монумент Славы в честь работников авиапромышленности",
        "btn_rocket": 'Монумент ракета-носитель "Союз"',
        "btn_church": "Софийская церковь",
        "btn_plane": "Памятник штурмовику Ил-2",
        "btn_museum": "Самарский областной историко-краеведческий музей"
    };

    // Добавляем обработчики для всех кнопок
    Object.keys(buttons).forEach(buttonId => {
        const button = document.getElementById(buttonId);
        if (button) {
            button.addEventListener("click", function() {
                console.log(`Нажата кнопка: ${buttonId}`);
                sendAttractionToBot(buttons[buttonId]);
            });

            // Добавляем визуальный feedback
            button.style.transition = 'all 0.2s ease';
            button.addEventListener('mousedown', () => {
                button.style.transform = 'scale(0.95)';
            });
            button.addEventListener('mouseup', () => {
                button.style.transform = 'scale(1)';
            });
            button.addEventListener('mouseleave', () => {
                button.style.transform = 'scale(1)';
            });

        } else {
            console.warn(`Кнопка не найдена: ${buttonId}`);
        }
    });

    // Проверяем доступность Telegram WebApp
    if (window.Telegram && window.Telegram.WebApp) {
        console.log('Telegram WebApp доступен');
        console.log('Версия WebApp:', tg.version);
        console.log('Платформа:', tg.platform);
    } else {
        console.warn('Telegram WebApp не доступен - тестовый режим');
        showNotification('⚠️ Тестовый режим (не в Telegram)', true);
    }
});

// Обработчик ошибок
window.addEventListener('error', function(e) {
    console.error('Global error:', e.error);
    showNotification('⚠️ Произошла ошибка', true);
});