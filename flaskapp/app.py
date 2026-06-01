from flask import Flask, request, jsonify, render_template
import psycopg2
import psycopg2.extras

app = Flask(__name__)

# Configuração do banco de dados
DB_CONFIG = {
    "host": "localhost",
    "port": 5421,
    "database": "meubanco",
    "user": "postgres",
    "password": ""  # coloque sua senha aqui se tiver
}

def get_conn():
    return psycopg2.connect(**DB_CONFIG)


# ─── Página inicial ────────────────────────────────────────────────────────────
@app.route("/")
def index():
    return render_template("index.html")


# ─── INSERIR cliente ───────────────────────────────────────────────────────────
@app.route("/clientes", methods=["POST"])
def inserir_cliente():
    dados = request.get_json()
    nome   = dados.get("nome")
    email  = dados.get("email")
    cidade = dados.get("cidade", "")

    if not nome or not email:
        return jsonify({"erro": "nome e email são obrigatórios"}), 400

    try:
        conn = get_conn()
        cur  = conn.cursor()
        cur.execute(
            "INSERT INTO clientes (nome, email, cidade) VALUES (%s, %s, %s) RETURNING id",
            (nome, email, cidade)
        )
        novo_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({"mensagem": "Cliente inserido!", "id": novo_id}), 201
    except Exception as e:
        return jsonify({"erro": str(e)}), 500


# ─── CONSULTAR clientes ────────────────────────────────────────────────────────
@app.route("/clientes", methods=["GET"])
def listar_clientes():
    try:
        conn = get_conn()
        cur  = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cur.execute("SELECT id, nome, email, cidade, criado_em FROM clientes ORDER BY id")
        clientes = cur.fetchall()
        cur.close()
        conn.close()
        return jsonify([dict(c) for c in clientes])
    except Exception as e:
        return jsonify({"erro": str(e)}), 500


if __name__ == "__main__":
    app.run(port=4521, debug=True)