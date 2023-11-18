from flask import Flask, render_template, request
import pymysql

app = Flask(__name__, static_url_path='/static')

db = pymysql.connect(host="127.0.0.1",
                     user="root",
                    password="aluno",
                    database="mydb")

def calcular_cpf(cpf):
  cpf = ''.join(filter(str.isdigit, cpf))

  # Verifica se o CPF possui 11 dígitos
  if len(cpf) != 11:
      return False

  # Calcula o primeiro dígito verificador
  v1 = sum((10 - i) * int(cpf[i]) for i in range(9)) % 11
  v1 = 0 if v1 < 2 else 11 - v1

  # Verifica o primeiro dígito verificador
  if v1 != int(cpf[9]):
      return False

  # Calcula o segundo dígito verificador
  v2 = sum((11 - i) * int(cpf[i]) for i in range(10)) % 11
  v2 = 0 if v2 < 2 else 11 - v2

  # Verifica o segundo dígito verificador
  if v2 != int(cpf[10]):
      return False

  return True

# Uso
#cpf = input("Digite o CPF: ")
#if calcular_cpf(cpf):
#  print("CPF válido.")
#else:
#  print("CPF inválido, tente novamente!")

@app.route('/')
def index():
   return render_template('index.html')
   

@app.route('/validar_cpf', methods=['POST'])
def validar_cpf():
   cpf = request.form['cpf']
   if calcular_cpf(cpf):
      print("hello")
      nome = request.form['nome']
      cursor = db.cursor()
      sql = "INSERT INTO parceiros (cpf, nome) VALUES ('"
      sql+= cpf + "','" + nome + "');"
      print(sql)
      cursor.execute(sql)
      db.commit()

      return '<p>CPF válido e preocessado.</p>'+\
             '<p>Para inserir um novo parceiro, clique <a href="http://127.0.0.1:5000/">aqui!</a></p>'
   else:
      return '<p style="color:red">CPF<b>inválido</b>.</p>' +\
             'button onclick"history.back()">Voltar</button>'

if __name__=='__main__':
  app.run(debug=True)






