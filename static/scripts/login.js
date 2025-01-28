document.addEventListener("DOMContentLoaded", () => {
	const appDiv = document.getElementById("app")
	const users = {
		user: "user",
		admin: "admin",
	}

	function renderLoginScreen() {
		appDiv.innerHTML = `
            <h1>Вход в систему</h1>
            <form id="loginForm">
                <label for="loginUsername">Имя пользователя:</label>
                <input type="text" id="loginUsername" required>
                <label for="loginPassword">Пароль:</label>
                <input type="password" id="loginPassword" required>
                <button type="submit">Войти</button>
                <p class="error" id="loginError" style="display: none;">Неверный логин или пароль</p>
            </form>
            <h2>Регистрация</h2>
            <form id="registrationForm">
                <label for="registrationUsername">Имя пользователя:</label>
                <input type="text" id="registrationUsername" required>
                <label for="registrationPassword">Пароль:</label>
                <input type="password" id="registrationPassword" required>
                <button type="submit">Зарегистрироваться</button>
                <p class="error" id="registrationError" style="display: none;"></p>
            </form>
        `

		const loginForm = document.getElementById("loginForm")
		loginForm.addEventListener("submit", (event) => {
			event.preventDefault()
			const username = document.getElementById("loginUsername").value
			const password = document.getElementById("loginPassword").value
			const loginError = document.getElementById("loginError")

			if (users[username] && users[username] === password) {
				window.location.href = username === "admin" ? "admin.html" : "user.html"
			} else {
				loginError.textContent = "Неверный логин или пароль"
				loginError.style.display = "block"
			}
		})

		const registrationForm = document.getElementById("registrationForm")
		registrationForm.addEventListener("submit", (event) => {
			event.preventDefault()
			const registrationUsername = document.getElementById(
				"registrationUsername"
			).value
			const registrationPassword = document.getElementById(
				"registrationPassword"
			).value
			const registrationError = document.getElementById("registrationError")

			if (users[registrationUsername]) {
				registrationError.textContent =
					"Пользователь с таким именем уже существует"
				registrationError.style.display = "block"
				return
			}
			users[registrationUsername] = registrationPassword
			registrationError.textContent =
				"Регистрация успешна. Теперь вы можете войти"
			registrationError.style.display = "block"
			setTimeout(() => {
				registrationError.style.display = "none"
			}, 3000)
		})
	}

	renderLoginScreen()
})
