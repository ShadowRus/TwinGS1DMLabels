// Получаем элементы страницы
let input = document.getElementById("input"); // поле для ввода фамилии
let scanText = document.getElementById("scanText"); // текстовое поле Сканируйте код регистрации участника
let barCode = document.getElementById("barcode"); // текстовое поле с ШК



// Функция для скрытия элементов
function hide(...elements) {
  for (let element of elements) {
    element.style.display = "none";
  }
}

// Функция для показа элементов
function show(...elements) {
  for (let element of elements) {
    element.style.display = "block";
  }
}

// Функция для очистки списка
function clearList() {
  while (list.firstChild) {
    list.removeChild(list.firstChild);
  }
}


// Функция для обработки ответа от сервера при печати бейджа
function handlePrintResponse(response) {
  if (response.status === 200) {
    // Если ответ успешный, выводим аллерт
    alert("Этикетка напечатана");
    // Возвращаемся на начальное состояние страницы
  } else if (response.status === 500) {
    // Если ответ с ошибкой, можно повторно нажать кнопку Печать Бейджа
  }
}

// Функция для получения значений ШК
function onBarcode(code, type, base64) {
            barCode.innerHTML = code.toString()
            fetch(`/barcode_print?code=${code.toString()}`).then(handleSearchResponse);
        }

// Добавляем обработчик события клика на кнопку Назад
backButton.addEventListener("click", () => {
  // Возвращаемся на начальное состояние страницы
  hide(list, printButton, backButton);
  show(input, searchButton, scanText,barCode);
});









