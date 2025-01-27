document.addEventListener('DOMContentLoaded', () => {
    const appDiv = document.getElementById('app');
    let currentUser = null;
    let currentInterface = 'login';

    const users = {
        'user': 'user',
        'admin': 'admin'
    };

    let inventory = [
        { id: 1, name: 'Стол', quantity: 10, status: 'новый' },
        { id: 2, name: 'Стул', quantity: 50, status: 'используемый' },
        { id: 3, name: 'Компьютер', quantity: 3, status: 'сломанный' }
    ];
    
     let requests = [];

    let purchasePlans = [];

    function renderInterface() {
      switch(currentInterface){
        case 'login':
          renderLoginScreen();
          break;
         case 'user':
           renderUserDashboard();
           break;
        case 'admin':
           renderAdminDashboard();
           break;
      }
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
        `;

        const loginForm = document.getElementById('loginForm');
        loginForm.addEventListener('submit', (event) => {
            event.preventDefault();
            const username = document.getElementById('loginUsername').value;
            const password = document.getElementById('loginPassword').value;
            const loginError = document.getElementById('loginError');

            if (users[username] && users[username] === password) {
                currentUser = username;
                 loginError.style.display = 'none';
                 if (currentUser === 'admin') {
                    currentInterface = 'admin';
                 } else {
                   currentInterface = 'user';
                 }
                 renderInterface();
            } else {
                  loginError.textContent = "Неверный логин или пароль";
                 loginError.style.display = 'block';
            }
        });
         const registrationForm = document.getElementById('registrationForm');
        registrationForm.addEventListener('submit', (event) => {
            event.preventDefault();
            const registrationUsername = document.getElementById('registrationUsername').value;
            const registrationPassword = document.getElementById('registrationPassword').value;
           const registrationError = document.getElementById('registrationError');
          if (users[registrationUsername]) {
             registrationError.textContent = 'Пользователь с таким именем уже существует';
              registrationError.style.display = 'block';
             return;
         }
         users[registrationUsername] = registrationPassword;
           registrationError.textContent = 'Регистрация успешна. Теперь вы можете войти';
            registrationError.style.display = 'block';
             setTimeout(()=>{
               registrationError.style.display = 'none';
            }, 3000)
        })
    }
    function renderUserDashboard() {
        appDiv.innerHTML = `
            <h1>Панель пользователя</h1>
            <button id="logoutButton">Выйти</button>
            <h2>Доступный инвентарь</h2>
            <div id="inventoryList">
               ${renderInventoryItems()}
            </div>
            <h2>Создать заявку на инвентарь</h2>
            <form id="createRequestForm">
                <label for="requestItem">Инвентарь:</label>
                <select id="requestItem" required>
                     ${inventory.map(item => `<option value="${item.id}">${item.name}</option>`).join('')}
                   </select>
                <label for="requestQuantity">Количество:</label>
                <input type="number" id="requestQuantity" required min="1">
                <button type="submit">Отправить заявку</button>
            </form>
              <h2>Заявки на ремонт/замену инвентаря</h2>
             <form id="createRepairForm">
                <label for="repairItem">Инвентарь:</label>
                 <select id="repairItem" required>
                      ${inventory.map(item => `<option value="${item.id}">${item.name}</option>`).join('')}
                 </select>
               <label for="repairDescription">Описание:</label>
                <textarea id="repairDescription" required></textarea>
               <button type="submit">Отправить заявку</button>
           </form>
           <h2>Статус заявок</h2>
            <div id="requestStatus">
               ${renderRequestStatus()}
            </div>
        `;
      const logoutButton = document.getElementById('logoutButton');
         logoutButton.addEventListener('click', () => {
            currentUser = null;
           currentInterface = 'login';
           renderInterface();
        });
          const createRequestForm = document.getElementById('createRequestForm');
          createRequestForm.addEventListener('submit', (event) => {
                event.preventDefault();
                 const itemId = parseInt(document.getElementById('requestItem').value);
                const quantity = parseInt(document.getElementById('requestQuantity').value);

                if (quantity <= 0) {
                      alert('Количество должно быть больше нуля.');
                      return;
                }
                   const selectedItem = inventory.find(item => item.id === itemId);
                if (!selectedItem || quantity > selectedItem.quantity) {
                  alert('Недостаточно инвентаря в наличии.');
                  return;
                }
                  
                 requests.push({
                   id: requests.length + 1,
                   itemId: itemId,
                  quantity: quantity,
                  status: 'ожидает',
                   user: currentUser,
                });
                renderUserDashboard();
             });
           const createRepairForm = document.getElementById('createRepairForm');
         createRepairForm.addEventListener('submit', (event) => {
            event.preventDefault();
             const repairItemId = parseInt(document.getElementById('repairItem').value);
             const repairDescription = document.getElementById('repairDescription').value;

            requests.push({
             id: requests.length + 1,
               itemId: repairItemId,
               description: repairDescription,
              type: 'ремонт',
             status: 'ожидает',
               user: currentUser,
          });
            renderUserDashboard();
          });
    }
       function renderInventoryItems() {
      return inventory.map(item => `
       <div class="inventory-item-card">
       <h3>${item.name}</h3>
      <p>Количество: ${item.quantity}</p>
      <p>Состояние: ${item.status}</p>
      </div>`).join('');
      }
     function renderRequestStatus() {
    const userRequests = requests.filter(request => request.user === currentUser);
        if (userRequests.length === 0) {
            return '<p>Нет заявок.</p>';
        }
    
        return `<table>
            <thead>
                <tr>
                  <th>ID</th>
                    <th>Инвентарь</th>
                   <th>Тип</th>
                    <th>Количество/Описание</th>
                   <th>Статус</th>
                </tr>
            </thead>
            <tbody>
               ${userRequests.map(request => {
                    const itemName = inventory.find(item => item.id === request.itemId)?.name || 'Неизвестно';
                     const quantityOrDescription = request.quantity ? request.quantity : request.description;
                     const requestType = request.type ? request.type : 'заявка';
                    return `
                       <tr>
                         <td>${request.id}</td>
                          <td>${itemName}</td>
                          <td>${requestType}</td>
                           <td>${quantityOrDescription}</td>
                          <td>${request.status}</td>
                      </tr>
                    `
                 }).join('')}
            </tbody>
        </table>`;
      }

    function renderAdminDashboard() {
        appDiv.innerHTML = `
            <h1>Панель администратора</h1>
              <button id="logoutButton">Выйти</button>
            <h2>Управление инвентарём</h2>
            <div id="inventoryManagement">
              ${renderAdminInventory()}
            </div>
            <h2>Добавить инвентарь</h2>
            <form id="addInventoryForm">
                <label for="addItemName">Название:</label>
                <input type="text" id="addItemName" required>
                <label for="addItemQuantity">Количество:</label>
                <input type="number" id="addItemQuantity" required min="1">
                <button type="submit">Добавить</button>
            </form>
              <h2>Планы закупок</h2>
             <div id="purchasePlan">
              ${renderPurchasePlan()}
             </div>
            <h2>Добавить план закупок</h2>
              <form id="addPurchaseForm">
                <label for="purchaseItem">Инвентарь:</label>
                 <select id="purchaseItem" required>
                      ${inventory.map(item => `<option value="${item.id}">${item.name}</option>`).join('')}
                  </select>
                 <label for="purchasePrice">Цена:</label>
                 <input type="number" id="purchasePrice" required min="0.01" step="0.01">
                <label for="purchaseSupplier">Поставщик:</label>
                <input type="text" id="purchaseSupplier" required>
                <button type="submit">Добавить в план закупок</button>
              </form>
              <h2>Заявки пользователей</h2>
              <div id="adminRequestStatus">
                ${renderAdminRequestStatus()}
              </div>
                <h2>Отчёты по инвентарю</h2>
             <div id="inventoryReports">
                ${renderInventoryReport()}
            </div>
        `;
          const logoutButton = document.getElementById('logoutButton');
           logoutButton.addEventListener('click', () => {
           currentUser = null;
             currentInterface = 'login';
             renderInterface();
         });
         const addInventoryForm = document.getElementById('addInventoryForm');
         addInventoryForm.addEventListener('submit', (event) => {
            event.preventDefault();
              const itemName = document.getElementById('addItemName').value;
            const itemQuantity = parseInt(document.getElementById('addItemQuantity').value);
            if (itemQuantity <= 0) {
            alert('Количество должно быть больше нуля.');
               return;
          }
           const newItem = {
             id: inventory.length + 1,
             name: itemName,
              quantity: itemQuantity,
              status: 'новый',
            };
            inventory.push(newItem);
            renderAdminDashboard();
      });
      const addPurchaseForm = document.getElementById('addPurchaseForm');
         addPurchaseForm.addEventListener('submit', (event) => {
           event.preventDefault();
             const itemId = parseInt(document.getElementById('purchaseItem').value);
             const purchasePrice = parseFloat(document.getElementById('purchasePrice').value);
             const supplier = document.getElementById('purchaseSupplier').value;
              if (purchasePrice <= 0) {
                  alert('Цена должна быть больше нуля.');
                 return;
            }
           const newItemPurchase = {
             id: purchasePlans.length + 1,
               itemId: itemId,
               price: purchasePrice,
             supplier: supplier,
            };
              purchasePlans.push(newItemPurchase);
             renderAdminDashboard();
         });
    }
       function renderAdminRequestStatus() {
        if (requests.length === 0) {
            return '<p>Нет заявок.</p>';
         }
        return `<table>
            <thead>
                <tr>
                  <th>ID</th>
                    <th>Пользователь</th>
                    <th>Инвентарь</th>
                   <th>Тип</th>
                    <th>Количество/Описание</th>
                   <th>Статус</th>
                   <th>Действия</th>
                </tr>
            </thead>
            <tbody>
               ${requests.map(request => {
                    const itemName = inventory.find(item => item.id === request.itemId)?.name || 'Неизвестно';
                     const quantityOrDescription = request.quantity ? request.quantity : request.description;
                     const requestType = request.type ? request.type : 'заявка';
                    return `
                       <tr>
                         <td>${request.id}</td>
                         <td>${request.user}</td>
                          <td>${itemName}</td>
                          <td>${requestType}</td>
                           <td>${quantityOrDescription}</td>
                          <td>
                            <select class="request-status-select" data-request-id="${request.id}">
                                <option value="ожидает" ${request.status === 'ожидает' ? 'selected' : ''}>ожидает</option>
                                <option value="выполнено" ${request.status === 'выполнено' ? 'selected' : ''}>выполнено</option>
                                <option value="отклонено" ${request.status === 'отклонено' ? 'selected' : ''}>отклонено</option>
                             </select>
                           </td>
                           <td>
                            <button class="delete-request-button" data-request-id="${request.id}">Удалить</button>
                         </td>
                      </tr>
                    `
                 }).join('')}
            </tbody>
        </table>`;
      }
     function renderAdminInventory() {
        if (inventory.length === 0) {
             return '<p>Инвентарь пуст</p>'
        }
         return `
            <table>
                <thead>
                  <tr>
                      <th>ID</th>
                        <th>Название</th>
                        <th>Количество</th>
                        <th>Состояние</th>
                      <th>Действия</th>
                    </tr>
                </thead>
               <tbody>
                   ${inventory.map(item => `
                        <tr>
                         <td>${item.id}</td>
                           <td>${item.name}</td>
                         <td>${item.quantity}</td>
                          <td>
                               <select class="status-select" data-item-id="${item.id}">
                                 <option value="новый" ${item.status === 'новый' ? 'selected' : ''}>новый</option>
                                 <option value="используемый" ${item.status === 'используемый' ? 'selected' : ''}>используемый</option>
                                   <option value="сломанный" ${item.status === 'сломанный' ? 'selected' : ''}>сломанный</option>
                               </select>
                            </td>
                             <td>
                              <button class="edit-item-button" data-item-id="${item.id}">Изменить</button>
                               </td>
                           </tr>
                       `).join('')}
                  </tbody>
             </table>
           `;
    }
  function renderPurchasePlan() {
          if(purchasePlans.length === 0) {
              return '<p>Нет планов закупок</p>'
         }
       return `
            <table>
              <thead>
                 <tr>
                   <th>ID</th>
                    <th>Инвентарь</th>
                      <th>Цена</th>
                    <th>Поставщик</th>
                </tr>
              </thead>
            <tbody>
                ${purchasePlans.map(plan => {
                 const itemName = inventory.find(item => item.id === plan.itemId)?.name || 'Неизвестно';
                    return `
                       <tr>
                        <td>${plan.id}</td>
                          <td>${itemName}</td>
                          <td>${plan.price}</td>
                         <td>${plan.supplier}</td>
                       </tr>
                    `
              }).join('')}
           </tbody>
         </table>
      `;
     }
    function renderInventoryReport() {
         const totalItems = inventory.length;
          const newItems = inventory.filter(item => item.status === 'новый').length;
           const usedItems = inventory.filter(item => item.status === 'используемый').length;
        const brokenItems = inventory.filter(item => item.status === 'сломанный').length;

      return `
       <p>Всего инвентаря: ${totalItems}</p>
       <p>Новый инвентарь: ${newItems}</p>
        <p>Используемый инвентарь: ${usedItems}</p>
       <p>Сломанный инвентарь: ${brokenItems}</p>
      `;
     }
       appDiv.addEventListener('change', (event) => {
        if (event.target.classList.contains('status-select')) {
            const itemId = parseInt(event.target.getAttribute('data-item-id'));
             const newStatus = event.target.value;
              const item = inventory.find(item => item.id === itemId);
            if (item) {
               item.status = newStatus;
               renderAdminDashboard();
          }
        }
        if(event.target.classList.contains('request-status-select')) {
             const requestId = parseInt(event.target.getAttribute('data-request-id'));
              const newStatus = event.target.value;
              const request = requests.find(request => request.id === requestId);
              if (request) {
                 request.status = newStatus;
               renderAdminDashboard();
             }
        }
    });
      appDiv.addEventListener('click', (event) => {
        if(event.target.classList.contains('edit-item-button')) {
           const itemId = parseInt(event.target.getAttribute('data-item-id'));
             editItem(itemId)
        }
        if(event.target.classList.contains('delete-request-button')) {
             const requestId = parseInt(event.target.getAttribute('data-request-id'));
           deleteRequest(requestId);
        }
      })
    function deleteRequest(requestId) {
         requests = requests.filter(request => request.id !== requestId);
          renderAdminDashboard();
    }
    function editItem(itemId) {
        const item = inventory.find(item => item.id === itemId);
            if (!item) return;
        appDiv.innerHTML = `
         <h1>Редактировать инвентарь</h1>
           <form id="editItemForm">
                <label for="editItemName">Название:</label>
                <input type="text" id="editItemName" value="${item.name}" required>
               <label for="editItemQuantity">Количество:</label>
               <input type="number" id="editItemQuantity" value="${item.quantity}" required>
                 <button type="submit">Сохранить</button>
               <button type="button" id="cancelEditButton">Отмена</button>
            </form>
         `;
        const editForm = document.getElementById('editItemForm');
         editForm.addEventListener('submit', (event) => {
           event.preventDefault();
             const newName = document.getElementById('editItemName').value;
              const newQuantity = parseInt(document.getElementById('editItemQuantity').value);
           if (newQuantity <= 0) {
                 alert('Количество должно быть больше нуля.');
                  return;
             }
           item.name = newName;
           item.quantity = newQuantity;
              renderAdminDashboard();
         });
          const cancelButton = document.getElementById('cancelEditButton');
            cancelButton.addEventListener('click', renderAdminDashboard);
      }
       

    renderInterface();
});