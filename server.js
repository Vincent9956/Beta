const express = require('express');
          const app = express();
          const PORT = 3000;

          const API_KEY = 'sk_live_1234567890abcdef';
                    
          app.use(express.json());
          app.use(express.urlencoded({ extended: true }));

          // Home page
          app.get('/', (req, res) => {
            res.send(`
              <!DOCTYPE html>
              <html>
              <head><title>Sample App</title></head>
              <body>
                <h1>Sample Application for DAST Testing</h1>
                <ul>
                  <li><a href="/about">About</a></li>
                  <li><a href="/contact">Contact</a></li>
                  <li><a href="/api/users">API Users</a></li>
                </ul>
                <form action="/search" method="GET">
                  <input type="text" name="q" placeholder="Search...">
                  <button type="submit">Search</button>
                </form>
              </body>
              </html>
            `);
          });

          // About page
          app.get('/about', (req, res) => {
            res.send('<h1>About Us</h1><p>This is a sample application.</p>');
          });

          // Contact page
          app.get('/contact', (req, res) => {
            res.send(`
              <h1>Contact</h1>
              <form action="/contact" method="POST">
                <input type="text" name="name" placeholder="Name"><br>
                <input type="email" name="email" placeholder="Email"><br>
                <textarea name="message" placeholder="Message"></textarea><br>
                <button type="submit">Submit</button>
              </form>
            `);
          });

          // Handle contact form
          app.post('/contact', (req, res) => {
            res.send('<h1>Thank you!</h1><p>Your message has been received.</p>');
          });

          // Search endpoint
          app.get('/search', (req, res) => {
            const query = req.query.q || '';
            res.send(`<h1>Search Results for: ${query}</h1>`);
          });

          // API endpoint
          app.get('/api/users', (req, res) => {
            res.json([
              { id: 1, name: 'John Doe', email: 'john@example.com' },
              { id: 2, name: 'Jane Smith', email: 'jane@example.com' }
            ]);
          });

          // API endpoint with parameter
          app.get('/api/users/:id', (req, res) => {
            const userId = req.params.id;
            res.json({ id: userId, name: 'Sample User', email: 'user@example.com' });
          });

          app.listen(PORT, () => {
            console.log(`Server running at http://localhost:${PORT}`);
          });
          
