
const express = require('express');
const bodyParser = require('body-parser');
const sqlite3 = require('sqlite3').verbose();
const path = require('path');

const app = express();
app.use(bodyParser.json());
app.use(express.static(__dirname)); // 

const db = new sqlite3.Database('./demo.db');

db.serialize(() => {
  db.run(`CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, password TEXT)`);
  db.run(`DELETE FROM users`); // reset for demo
  db.run(`INSERT INTO users (username, password) VALUES ('alice', 'password123')`);
});

app.post('/login', (req, res) => {
  const { username, password } = req.body || {};

  const sql = `SELECT id, username FROM users WHERE username = '${username}' AND password = '${password}' LIMIT 1;`;

  db.get(sql, (err, row) => {
    if (err) {
      console.error('SQL error:', err);
      return res.status(500).json({ ok: false, error: 'server error' });
    }
    if (row) {
      res.json({ ok: true, user: row });
    } else {
      res.json({ ok: false, message: 'invalid credentials' });
    }
  });
});

app.listen(3000, () => {
  console.log('VULNERABLE server running at http://localhost:3000 ');
});

