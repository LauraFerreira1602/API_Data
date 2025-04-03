from flask import Flask, jsonify

from datetime import datetime

from flask_pydantic_spec import FlaskPydanticSpec

app = Flask(__name__)
spec = FlaskPydanticSpec('flask',
                         title='First API - SENAI',
                         version='1.0.0')
spec.register(app)


@app.route('/')
def index():
    return jsonify({})


@app.route('/verificar-data/<data>')
def data(data):
    """
        API para ver data

        ## Endpoint:
        'GET /data/<data_entrada>/data_atual>'

        ## Parâmetros:
        - 'data_entrada' - (str): data de entrada
        - 'data_atual' - (str): data atual
            - ** Qualquer outro formato resultara em erro. **

        ## Resposta (JSON):
        ''' json
            {"data_entrada": "12/10/2024",
                "data_atual": "15/10/2025"}
        '''

        ## Erros possiveis:
        - Se o formato da data não for correto, resultara em {'erro': 'Formato de data incorreto'}

    """

    try:
        data_entrada = datetime.strptime(data, "%d-%m-%Y")
        data_atual = datetime.now()

        if data_atual < data_entrada:
            status = "futuro"

        elif data_atual > data_entrada:
            status = "passado"

        else:
            status = "presente"

        diferenca_dias = abs((data_atual - data_entrada).days)
        diferenca_anos = abs(data_atual.year - data_entrada.year)
        diferenca_mes = (diferenca_anos * 12) + (data_atual.month - data_entrada.month)

        return jsonify({
            "Data atual": data_atual,
            "Data entrada": data_entrada,
            "Status": status,
            "Diferenca dias": str(diferenca_dias),
            "Diferenca meses": str(diferenca_mes),
            "Diferenca ano": str(diferenca_anos)
        })


    except ValueError:
        return jsonify({'erro': 'Formato de data incorreto'})


if __name__ == '__main__':
    app.run(debug=True)
