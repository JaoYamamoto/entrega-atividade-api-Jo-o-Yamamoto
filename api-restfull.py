from flask import Flask, request, jsonify

app = Flask(__name__)

usuarios = []
current_id = 1


# post / users (create)
@app.route('/usuarios', methods=['POST'])
def criar_usuario():
    global current_id
    dados = request.get_json()

    if not dados or "nome" not in dados or "email" not in dados:
        return jsonify({"erro": "Dados inválidos."}), 400

    novo_usuario = {
        "id": current_id,
        "nome": dados["nome"],
        "email": dados["email"]
    }
    usuarios.append(novo_usuario)
    current_id += 1

    return jsonify(novo_usuario), 201


# get / read all
@app.route('/usuarios', methods=['GET'])
def listar_usuarios():
    return jsonify(usuarios), 200


# get / read single
@app.route('/usuarios/<int:usuario_id>', methods=['GET'])
def obter_usuario(usuario_id):
    usuario = next((u for u in usuarios if u["id"] == usuario_id), None)
    if usuario:
        return jsonify(usuario), 200
    return jsonify({"erro": "Usuário não foi encontrado."}), 404


# put / update
@app.route('/usuarios/<int:usuario_id>', methods=['PUT'])
def atualizar_usuario(usuario_id):
    dados = request.get_json()
    usuario = next((u for u in usuarios if u["id"] == usuario_id), None)

    if not usuario:
        return jsonify({"erro": "Usuário não foi encontrado."}), 404

    if not dados:
        return jsonify({"erro": "Preencha os campos."}), 400

    usuario["nome"] = dados.get("nome", usuario["nome"])
    usuario["email"] = dados.get("email", usuario["email"])

    return jsonify(usuario), 200


# delete
@app.route('/usuarios/<int:usuario_id>', methods=['DELETE'])
def deletar_usuario(usuario_id):
    global usuarios
    usuario = next((u for u in usuarios if u["id"] == usuario_id), None)

    if not usuario:
        return jsonify({"erro": "Usuário não foi encontrado"}), 404

    usuarios = [u for u in usuarios if u["id"] != usuario_id]
    return jsonify({"mensagem": "Usuário foi deletado."}), 200


if __name__ == '__main__':
    app.run(debug=True)
