document.addEventListener("DOMContentLoaded", () => {
	const appDiv = document.getElementById("app")
	let inventory = [
		{ id: 1, name: "Стол", quantity: 10, status: "новый" },
		{ id: 2, name: "Стул", quantity: 50, status: "используемый" },
		{ id: 3, name: "Компьютер", quantity: 3, status: "сломанный" },
	]
	let requests = []
	let purchasePlans = []

	function renderAdminDashboard() {
		appDiv.innerHTML = `
            <h1>Панель администратора</h1>
            <button id="logoutButton">Выйти</button>
            <h2>Управление инвентарём</h2>
            <div id="inventoryManagement">${renderAdminInventory()}</div>
            <h2>Добавить инвентарь</h2>
            <form id="addInventoryForm">
                <label for="addItemName">Название:</label>
                <input type="text" id="addItemName" required>
                <label for="addItemQuantity">Количество:</label>
                <input type="number" id="addItemQuantity" required min="1">
                <button type="submit">Добавить</button>
            </form>
            <h2>Заявки пользователей</h2>
            <div id="adminRequestStatus">${renderAdminRequestStatus()}</div>
        `

		const logoutButton = document.getElementById("logoutButton")
		logoutButton.addEventListener("click", () => {
			window.location.href = "index.html"
		})

		const addInventoryForm = document.getElementById("addInventoryForm")
		addInventoryForm.addEventListener("submit", (event) => {
			event.preventDefault()
			const itemName = document.getElementById("addItemName").value
			const itemQuantity = parseInt(
				document.getElementById("addItemQuantity").value
			)
			if (itemQuantity <= 0) {
				alert("Количество должно быть больше нуля.")
				return
			}
			const newItem = {
				id: inventory.length + 1,
				name: itemName,
				quantity: itemQuantity,
				status: "новый",
			}
			inventory.push(newItem)
			renderAdminDashboard()
		})
	}

	function renderAdminInventory() {
		if (inventory.length === 0) {
			return "<p>Инвентарь пуст</p>"
		}
		return `
            <table>
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Название</th>
                        <th>Количество</th>
                        <th>Состояние</th>
                    </tr>
                </thead>
                <tbody>
                    ${inventory
											.map(
												(item) => `
                        <tr>
                            <td>${item.id}</td>
                            <td>${item.name}</td>
                            <td>${item.quantity}</td>
                            <td>${item.status}</td>
                        </tr>
                    `
											)
											.join("")}
                </tbody>
            </table>
        `
	}

	function renderAdminRequestStatus() {
		if (requests.length === 0) {
			return "<p>Нет заявок.</p>"
		}
		return `
            <table>
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Пользователь</th>
                        <th>Инвентарь</th>
                        <th>Статус</th>
                    </tr>
                </thead>
                <tbody>
                    ${requests
											.map((request) => {
												const itemName =
													inventory.find((item) => item.id === request.itemId)
														?.name || "Неизвестно"
												return `
                            <tr>
                                <td>${request.id}</td>
                                <td>${request.user}</td>
                                <td>${itemName}</td>
                                <td>${request.status}</td>
                            </tr>
                        `
											})
											.join("")}
                </tbody>
            </table>
        `
	}

	renderAdminDashboard()
})
