const express = require('express');
const bodyParser = require('body-parser');
const bcrypt = require('bcrypt');
const session = require('express-session');
const cors = require('cors');
const fs = require('fs');
const path = require('path');

const app = express();
const DATA_FILE = 'users.json';

app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));
app.use(cors());
app.use(express.static(path.join(__dirname, 'public')));
app.use(session({
    secret: 'your_secret_key',
    resave: false,
    saveUninitialized: true,
    cookie: { secure: false } // Set to true if using HTTPS
}));

function readUsers() {
    if (fs.existsSync(DATA_FILE)) {
        const data = fs.readFileSync(DATA_FILE);
        return JSON.parse(data);
    }
    return {};
}

function writeUsers(users) {
    fs.writeFileSync(DATA_FILE, JSON.stringify(users, null, 2));
}

app.post('/register', (req, res) => {
    const { email, age, password } = req.body;
    if (!email || !age || !password) {
        return res.status(400).json({ message: 'Email, age, and password are required' });
    }

    const users = readUsers();
    if (users[email]) {
        return res.status(400).json({ message: 'User already exists' });
    }

    const hashedPassword = bcrypt.hashSync(password, 10);
    users[email] = { email, age, password: hashedPassword };
    writeUsers(users);
    res.status(201).json({ message: 'User added successfully' });
});

app.post('/login', (req, res) => {
    const { email, password } = req.body;
    const users = readUsers();
    const user = users[email];
    if (!user || !bcrypt.compareSync(password, user.password)) {
        return res.status(401).json({ message: 'Invalid credentials' });
    }

    req.session.user = email;
    res.json({ message: 'Login successful' });
});

app.get('/profile', (req, res) => {
    if (!req.session.user) {
        return res.status(401).json({ message: 'Not authenticated' });
    }

    const users = readUsers();
    const user = users[req.session.user];
    res.json(user);
});

app.post('/profile', (req, res) => {
    if (!req.session.user) {
        return res.status(401).json({ message: 'Not authenticated' });
    }

    const { age } = req.body;
    const users = readUsers();
    const user = users[req.session.user];
    user.age = age;
    writeUsers(users);
    res.json({ message: 'Profile updated successfully' });
});

app.post('/delete_account', (req, res) => {
    if (!req.session.user) {
        return res.status(401).json({ message: 'Not authenticated' });
    }

    const users = readUsers();
    delete users[req.session.user];
    writeUsers(users);
    req.session.destroy();
    res.json({ message: 'Account deleted successfully' });
});

app.post('/api/add_user', (req, res) => {
    const { email, age, password } = req.body;
    const users = readUsers();
    if (users[email]) {
        return res.status(400).json({ message: 'User already exists' });
    }

    const hashedPassword = bcrypt.hashSync(password, 10);
    users[email] = { email, age, password: hashedPassword };
    writeUsers(users);
    res.status(201).json({ message: 'User added successfully' });
});

app.post('/api/login', (req, res) => {
    const { email, password } = req.body;
    const users = readUsers();
    const user = users[email];
    if (!user || !bcrypt.compareSync(password, user.password)) {
        return res.status(401).json({ message: 'Invalid credentials' });
    }

    res.json({ message: 'Login successful' });
});

app.route('/api/user/:email')
    .get((req, res) => {
        const { email } = req.params;
        const users = readUsers();
        const user = users[email];
        if (!user) {
            return res.status(404).json({ message: 'User not found' });
        }
        res.json(user);
    })
    .put((req, res) => {
        const { email } = req.params;
        const { age } = req.body;
        const users = readUsers();
        const user = users[email];
        if (!user) {
            return res.status(404).json({ message: 'User not found' });
        }

        user.age = age;
        writeUsers(users);
        res.json({ message: 'User updated successfully' });
    })
    .delete((req, res) => {
        const { email } = req.params;
        const users = readUsers();
        if (!users[email]) {
            return res.status(404).json({ message: 'User not found' });
        }

        delete users[email];
        writeUsers(users);
        res.json({ message: 'User deleted successfully' });
    });

const PORT = process.env.PORT || 5000;
app.listen(PORT, () => {
    console.log(`Server is running on port ${PORT}`);
});