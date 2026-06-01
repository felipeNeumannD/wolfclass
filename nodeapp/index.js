const express = require('express');
const { Pool } = require('pg');

const app = express();

const pool = new Pool({
  host: 'localhost',
  port: 5421,
  database: 'meubanco',
  user: 'postgres',
  password: '123'
});

app.get('/', async (req, res) => {
  try {
    const result = await pool.query('SELECT id, nome, email, cidade FROM clientes ORDER BY id');
    const rows = result.rows;

    const linhas = rows.map(r => `
      <tr>
        <td>${r.id}</td>
        <td>${r.nome}</td>
        <td>${r.email}</td>
        <td>${r.cidade || '—'}</td>
      </tr>`).join('');

    res.send(`
      <!DOCTYPE html>
      <html lang="pt-BR">
      <head>
        <meta charset="UTF-8">
        <title>Clientes — Node</title>
        <style>
          body { font-family: sans-serif; padding: 2rem; background: #0f0f0f; color: #f0f0f0; }
          h1 { color: #00e5a0; }
          table { border-collapse: collapse; width: 100%; }
          th, td { padding: 10px 14px; border: 1px solid #2a2a2a; text-align: left; }
          th { background: #1a1a1a; color: #00e5a0; }
          tr:nth-child(even) { background: #181818; }
        </style>
      </head>
      <body>
        <h1>Clientes — meubanco</h1>
        <p>Node.js rodando na porta 4522</p>
        <table>
          <thead><tr><th>ID</th><th>Nome</th><th>Email</th><th>Cidade</th></tr></thead>
          <tbody>${linhas}</tbody>
        </table>
      </body>
      </html>
    `);
  } catch (err) {
    res.status(500).send(`<p>Erro: ${err.message}</p>`);
  }
});

app.listen(4522, '0.0.0.0', () => {
  console.log('Servidor rodando em http://0.0.0.0:4522');
});
