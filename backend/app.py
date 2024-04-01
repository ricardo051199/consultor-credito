from flask import Flask, request, jsonify
from pgmpy.models import BayesianModel
from pgmpy.factors.discrete import TabularCPD
from pgmpy.inference import VariableElimination
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

modelo = BayesianModel([('Pb', 'Hp'), ('Em', 'Hp'), ('Hp','C'), ('Em','C'), ('Bi', 'Mb'), ('Bi', 'Bif'), ('Mb', 'Bif'), ('Pb', 'Dc'), ('C', 'Dc'), ('Bif', 'Dc')])

cpd_em = TabularCPD(variable='Em', variable_card=2, values=[[0.65], [0.35]])
cpd_bi = TabularCPD(variable='Bi', variable_card=2, values=[[0.56], [0.44]])
cpd_pb = TabularCPD(variable='Pb', variable_card=2, values=[[0.78], [0.22]])
cpd_hp = TabularCPD(variable='Hp', variable_card=2, values=[[0.78, 0.64, 0.66, 0.2], [0.22, 0.36, 0.34, 0.8]],
                    evidence=['Em', 'Pb'], evidence_card=[2, 2])
cpd_bif = TabularCPD(variable='Bif', variable_card=2, values=[[0.88, 0.51, 0.62, 0.35], [0.12, 0.49, 0.38, 0.65]],
                     evidence=['Mb', 'Bi'], evidence_card=[2, 2])
cpd_c = TabularCPD(variable='C', variable_card=2, values=[[0.88, 0.58, 0.69, 0.12], [0.12, 0.42, 0.31, 0.88]],
                   evidence=['Em', 'Hp'], evidence_card=[2, 2])
cpd_mb = TabularCPD(variable='Mb', variable_card=2, values=[[0.86, 0.34], [0.14, 0.66]], evidence=['Bi'], evidence_card=[2])
cpd_dc = TabularCPD(variable='Dc', variable_card=2, values=[[0.98, 0.78, 0.73, 0.23, 0.82, 0.2, 0.23, 0],
                                                             [0.02, 0.22, 0.27, 0.77, 0.18, 0.8, 0.77, 1]],
                    evidence=['Pb', 'C', 'Bif'], evidence_card=[2, 2, 2])

modelo.add_cpds(cpd_pb, cpd_em, cpd_bi, cpd_hp, cpd_bif, cpd_c, cpd_mb, cpd_dc)
inter = VariableElimination(modelo)

def determinar_estados(edad, estado_hp, ingresos, deuda, cantidad_activos):
    estado_edad = 0
    estado_pb = 0
    estado_ingresos = 0
    estado_activos = 0

    if edad > 30:
        estado_edad = 1

    if deuda / ingresos < 1:
        estado_pb = 1

    if ingresos > 5000:
        estado_ingresos = 1

    if cantidad_activos > 40:
        estado_activos = 1

    return estado_edad, estado_hp, estado_pb, estado_ingresos, estado_activos

@app.route('/')
def hola_mundo():
    return jsonify(mensaje="¡Hola desde el backend en Python!")

@app.route('/consultar-credito', methods=['POST'])
def consultar_credito():
    data = request.json
    edad = int(data['edad'])
    estado_hp = int(data['estadoHp'])
    ingresos = float(data['ingresos'])
    deuda = float(data['deuda'])
    cantidad_activos = int(data['cantidadActivos'])

    estado_edad, estado_hp, estado_pb, estado_ingresos, estado_activos = determinar_estados(edad, estado_hp, ingresos,
                                                                                            deuda, cantidad_activos)

    evidencias_c = {'Em': estado_edad, 'Hp': estado_hp}
    evidencias_bif = {'Bi': estado_ingresos, 'Mb': estado_activos}

    resultado_c = inter.query(variables=['C'], evidence=evidencias_c)
    phi_c_estado_1 = resultado_c.values[1]

    estado_c = 0
    if phi_c_estado_1 > 0.5:
        estado_c = 1

    resultado_bif = inter.query(variables=['Bif'], evidence=evidencias_bif)
    phi_bif_estado_1 = resultado_bif.values[1]

    estado_bif = 0
    if phi_bif_estado_1 > 0.5:
        estado_bif = 1

    evidencias_dc = {'Pb': estado_pb, 'C': estado_c, 'Bif': estado_bif}
    resultado_dc = inter.query(['Dc'], evidence=evidencias_dc)
    phi_dc_estado_1 = resultado_dc.values[1]

    if phi_dc_estado_1 > 0.5:
        resultado = "Tiene derecho a crédito con un " + str(phi_dc_estado_1*100) + "%"
    else:
        resultado = "NO tiene derecho a crédito"

    return jsonify({"resultado": resultado})

if __name__ == '__main__':
    app.run(debug=True)
