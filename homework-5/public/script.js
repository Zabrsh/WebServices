document.getElementById('userForm').addEventListener('submit', function(event) {
    event.preventDefault();
    const email = document.getElementById('email').value;
    const age = document.getElementById('age').value;

    fetch('/add_user', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ email, age })
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            document.getElementById('message').innerHTML = `<span id="error">${data.error}</span>`;
        } else {
            document.getElementById('message').innerHTML = data.message;
            loadUsers();
        }
    });
});

document.getElementById('loginForm').addEventListener('submit', function(event) {
    event.preventDefault();
    const email = document.getElementById('loginEmail').value;

    fetch('/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ email })
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            document.getElementById('message').innerHTML = `<span id="error">${data.error}</span>`;
        } else {
            document.getElementById('message').innerHTML = `Logged in as ${data.email}`;
            document.getElementById('editForm').style.display = 'block';
            document.getElementById('editForm').dataset.email = data.email;
        }
    });
});

document.getElementById('editForm').addEventListener('submit', function(event) {
    event.preventDefault();
    const email = event.target.dataset.email;
    const age = document.getElementById('editAge').value;

    fetch(`/update_user/${email}`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ age })
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('message').innerHTML = data.message;
        loadUsers();
    });
});

function loadUsers() {
    fetch('/get_users')
    .then(response => response.json())
    .then(users => {
        const userList = document.getElementById('userList');
        userList.innerHTML = '';
        for (const email in users) {
            const user = users[email];
            userList.innerHTML += `<div>
                <strong>${user.email}</strong> (Age: ${user.age})
                <button onclick="deleteUser('${user.email}')">Delete</button>
            </div>`;
        }
    });
}

function deleteUser(email) {
    fetch(`/delete_user/${email}`, {
        method: 'DELETE'
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('message').innerHTML = data.message;
        loadUsers();
    });
}

loadUsers();