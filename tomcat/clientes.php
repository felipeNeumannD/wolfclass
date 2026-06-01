<?php
$conn = pg_connect("host=localhost port=5421 dbname=meubanco user=postgres password=123");

if (!$conn) {
    die("<p>Erro ao conectar no banco.</p>");
}

$result = pg_query($conn, "SELECT id, nome, email, cidade FROM clientes ORDER BY id");
?>
<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <title>Clientes</title>
  <style>
    body { font-family: sans-serif; padding: 2rem; background: #f5f5f5; }
    h1 { color: #333; }
    table { border-collapse: collapse; width: 100%; background: white; }
    th, td { padding: 10px 14px; border: 1px solid #ddd; text-align: left; }
    th { background: #333; color: white; }
    tr:nth-child(even) { background: #f9f9f9; }
  </style>
</head>
<body>
  <h1>Clientes — meubanco</h1>
  <table>
    <thead>
      <tr><th>ID</th><th>Nome</th><th>Email</th><th>Cidade</th></tr>
    </thead>
    <tbody>
      <?php while ($row = pg_fetch_assoc($result)): ?>
      <tr>
        <td><?= $row['id'] ?></td>
        <td><?= $row['nome'] ?></td>
        <td><?= $row['email'] ?></td>
        <td><?= $row['cidade'] ?></td>
      </tr>
      <?php endwhile; ?>
    </tbody>
  </table>
</body>
</html>
<?php pg_close($conn); ?>
