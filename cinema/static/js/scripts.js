// Добавление звёзд рейтинга.
// Ищем форму с именем rating, когда у формы происходит событие change мы получаем все значения полей, при успешном
// ответе будет установлен рейтинг, а при отрицательном выведено сообщение об ошибке.
const rating = document.querySelector(selectors: 'form[name=rating]');

rating.addEventListener(type: 'change', listener: function (e: Event)) {
    // Получаем данные из формы.
    let data = new FormData(this);
    fetch(input: `${this.action}`, init: {
        method: 'POST',
        body: data
    }) Promise<Response>
        .then(response => alert('Рейтинг установлен')) Promise<void>
        .catch(error => alert('Ошибка'))
}