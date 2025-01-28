document.addEventListener("DOMContentLoaded", () => {
	const appDiv = document.getElementById("app")
	let inventory = [
		{ id: 1, name: "Стол", quantity: 10, status: "новый" },
		{ id: 2, name: "Стул", quantity: 50, status: "используемый" },
		{ id: 3, name: "Компьютер", quantity: 3, status: "сломанный" },
	]
	let requests = []
	let currentUser = "user" // Замените на реального пользователя

	function renderUserDashboard() {
		appDiv.innerHTML = `
            <h1>Панель пользователя</h1>
            <button id="logoutButton">Выйти</button>
            <h2>Доступный инвентарь</h2>
            <div id="inventoryList">${renderInventoryItems()}</div>
            <h2>Создать заявку на инвентарь</h2>
            <form id="createRequestForm">
                <label for="requestItem">Инвентарь:</label>
                <select id="requestItem" required>
                    ${inventory
											.map(
												(item) =>
													`<option value="${item.id}">${item.name}</option>`
											)
											.join("")}
                </select>
                <label for="requestQuantity">Количество:</label>
                <input type="number" id="requestQuantity" required min="1">
                <button type="submit">Отправить заявку</button>
            </form>
            <h2>Статус заявок</h2>
            <div id="requestStatus">${renderRequestStatus()}</div>
        `

		const logoutButton = document.getElementById("logoutButton")
		logoutButton.addEventListener("click", () => {
			window.location.href = "index.html"
		})

		const createRequestForm = document.getElementById("createRequestForm")
		createRequestForm.addEventListener("submit", (event) => {
			event.preventDefault()
			const itemId = parseInt(document.getElementById("requestItem").value)
			const quantity = parseInt(
				document.getElementById("requestQuantity").value
			)

			if (quantity <= 0) {
				alert("Количество должно быть больше нуля.")
				return
			}

			const selectedItem = inventory.find((item) => item.id === itemId)
			if (!selectedItem || quantity > selectedItem.quantity) {
				alert("Недостаточно инвентаря в наличии.")
				return
			}

			requests.push({
				id: requests.length + 1,
				itemId: itemId,
				quantity: quantity,
				status: "ожидает",
				user: currentUser,
			})
			renderUserDashboard()
		})
	}

	function renderInventoryItems() {
		return inventory
			.map(
				(item) => `
            <div class="inventory-item-card">
                <h3>${item.name}</h3>
                <p>Количество: ${item.quantity}</p>
                <p>Состояние: ${item.status}</p>
            </div>`
			)
			.join("")
	}

	function renderRequestStatus() {
		const userRequests = requests.filter(
			(request) => request.user === currentUser
		)
		if (userRequests.length === 0) {
			return "<p>Нет заявок.</p>"
		}

		return `<table>
            <thead>
                <tr>
                    <th>ID</th>
                    <th>Инвентарь</th>
                    <th>Количество</th>
                    <th>Статус</th>
                </tr>
            </thead>
            <tbody>
                ${userRequests
									.map((request) => {
										const itemName =
											inventory.find((item) => item.id === request.itemId)
												?.name || "Неизвестно"
										return `
                        <tr>
                            <td>${request.id}</td>
                            <td>${itemName}</td>
                            <td>${request.quantity}</td>
                            <td>${request.status}</td>
                        </tr>
                    `
									})
									.join("")}
            </tbody>
        </table>`
	}

	renderUserDashboard()
})
