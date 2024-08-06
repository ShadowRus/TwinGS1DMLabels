// Получаем элементы страницы
let input = document.getElementById("input"); // поле для ввода фамилии
let searchButton = document.getElementById("searchButton"); // кнопка Поиск товара
let scanText = document.getElementById("scanText"); // текстовое поле Сканируйте код регистрации участника
//let registerButton = document.getElementById("registerButton"); // кнопка Зарегистрировать нового участника
let list = document.getElementById("list"); // список с radio-button для выбора участника
let printButton = document.getElementById("printButton"); // кнопка Печать Бейджа
let backButton = document.getElementById("backButton"); // кнопка Назад
//let form = document.getElementById("form"); // форма для регистрации нового участника
//let submitButton = document.getElementById("submitButton"); // кнопка Зарегистрировать
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

// Функция для создания элемента списка с radio-button
function createListItem(participant) {
  let item = document.createElement("li");
  let radio = document.createElement("input");
  radio.type = "radio";
  radio.name = "participant";
  radio.value = participant.id;
  let label = document.createElement("label");
  //label.textContent = `${participant.goods_name}`;
  let output = `<strong>${participant.goods_name}</strong>`;
  if (participant.attr_1 !== null) {
        output += `<br>Атрибут 1: ${participant.attr_1}`;
    }
    if (participant.attr_2 !== null) {
        output += `<br>Атрибут 2: ${participant.attr_2}`;
    }
    if (participant.attr_3 !== null) {
        output += `<br>Атрибут 3: ${participant.attr_3}`;
    }
    if (participant.attr_4 !== null) {
        output += `<br>Атрибут 4: ${participant.attr_4}`;
    }
    if (participant.attr_5 !== null) {
        output += `<br>Атрибут 5: ${participant.attr_5}`;
    }
  // Добавляем разделительную полосу после всех атрибутов
  output += `<hr>`;
  label.innerHTML = output;
  item.appendChild(radio);
  item.appendChild(label);
  return item;
}

// Функция для обработки ответа от сервера при поиске
function handleSearchResponse(response) {
  if (response.status === 200) {
    // Если ответ успешный, парсим json
    response.json().then((data) => {
      // Скрываем текущие элементы
      hide(input, searchButton, scanText,barCode);
      // Очищаем список
      clearList();
      // Добавляем элементы списка для каждого участника
      for (let participant of data) {
        let item = createListItem(participant);
        list.appendChild(item);
      }
      // Показываем список, кнопку Печать и кнопку Назад
      show(list, printButton, backButton);
    });
  } else if (response.status === 500) {
    // Если ответ с ошибкой, выводим аллерт
    alert("Повторите поиск");
  }
}


// Добавляем обработчик события клика на кнопку Поиск
searchButton.addEventListener("click", () => {
  // Получаем введенную фамилию
  let name = input.value;
  // Отправляем запрос к серверу с фамилией
  fetch(`/search?name=${name}`).then(handleSearchResponse);
});

// Функция для обработки ответа от сервера при печати бейджа
function handlePrintResponse(response) {
  if (response.status === 200) {
    // Если ответ успешный, выводим аллерт
    alert("Этикетка напечатана");
    // Возвращаемся на начальное состояние страницы
    hide(list, printButton, backButton);
    show(input, searchButton, scanText,barCode);
  } else if (response.status === 500) {
    // Если ответ с ошибкой, можно повторно нажать кнопку Печать Бейджа
  }
}

// Функция для получения значений ШК
function onBarcode(code, type, base64) {
            barCode.innerHTML = code.toString()
            fetch(`/barcode?code=${code.toString()}`).then(handleSearchResponse);
        }

// Добавляем обработчик события клика на кнопку Печать
printButton.addEventListener("click", () => {
    // Получаем выбранный radio-button
    let selected = document.querySelector("input[name=participant]:checked");
    if (selected) {
        // Получаем идентификатор выбранного участника
        let id = selected.value;

        // Отправляем POST-запрос к серверу с идентификатором
        fetch('/print', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ goods_id: id })
        })
        .then(response => response.json()) // Предполагается, что сервер возвращает JSON
        .then(handlePrintResponse)
        .catch(error => {
            console.error('Ошибка:', error);
        });
    }
});

// Добавляем обработчик события клика на кнопку Назад
backButton.addEventListener("click", () => {
  // Возвращаемся на начальное состояние страницы
  hide(list, printButton, backButton);
  show(input, searchButton, scanText,barCode);
});









