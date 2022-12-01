import smtplib
import email.message
import mysql.connector
from mysql.connector import Error
from PySimpleGUI import PySimpleGUI as sg

# função que envia o email


def enviar_email(email_alvo, tipo_sangue):
    tipo_sangue = str(tipo_sangue).strip('[]')

    envio_email = """
    <h1><b>Banco de Sangue Universitário.</b></h1>
    <p>Olá caro usuário,</p>
    <p>Como informado por você ao se cadastrar em nosso sistema, o seu tipo sanguíneo é: 
     {0}
    <p></p>
    <p>Que atualmente se encontra em falta na região.</b></p>
    <p>Faça o bem! Doe sangue!</p>
    """

    conteudo_email = envio_email.format(tipo_sangue)

    msg = email.message.Message()
    msg['Subject'] = 'Contamos com a sua Doação!'
    msg['From'] = 'bancodesangue.universitario@gmail.com'
    msg['To'] = email_alvo
    password = 'ivwjpfwdxnxoezdx'
    msg.add_header('Content-Type', 'text/html')
    msg.set_payload(conteudo_email)

    s = smtplib.SMTP('smtp.gmail.com: 587')
    s.starttls()
    s.login(msg['From'], password)
    s.sendmail(msg['From'], [msg['To']], msg.as_string().encode('utf-8'))
    print('O email foi enviado com sucesso.')


def ativar_envio(tipo_sangue):
    try:
        con = mysql.connector.connect(
            host='localhost', database='bd_sangue', user='root', password='PinkDarkchylde.1412')

        if con.is_connected():
            db_info = con.get_server_info()
            print("Conectado ao banco de dados ", db_info)

            cursor = con.cursor()

            if tipo_sangue == "A+":
                cursor.execute(
                    'select email from cadastro where tipoSangue = "A+" ')
            elif tipo_sangue == "A-":
                cursor.execute(
                    'select email from cadastro where tipoSangue = "A-" ')
            elif tipo_sangue == "B+":
                cursor.execute(
                    'select email from cadastro where tipoSangue = "B+" ')
            elif tipo_sangue == "B-":
                cursor.execute(
                    'select email from cadastro where tipoSangue = "B-" ')
            elif tipo_sangue == "AB+":
                cursor.execute(
                    'select email from cadastro where tipoSangue = "AB+" ')
            elif tipo_sangue == "AB-":
                cursor.execute(
                    'select email from cadastro where tipoSangue = "AB-" ')
            elif tipo_sangue == "O+":
                cursor.execute(
                    'select email from cadastro where tipoSangue = "O+" ')
            elif tipo_sangue == "O-":
                cursor.execute(
                    'select email from cadastro where tipoSangue = "O-" ')
            listaemail = cursor.fetchall()
            destinatario = list()

            for linha in listaemail:
                destinatario.append(linha[0])
                print(linha[0])
        print(destinatario)  # array dos emails obtida

    except Error as e:
        print("Ocorreu um erro ao acessar o MYSQL", e)
    finally:
        if con.is_connected():
            cursor.close()
            con.close()
            print("Conexão ao Banco encerrada.")
    for linha in listaemail:
        enviar_email(destinatario.pop(0), tipo_sangue)


##
sangue = []
sangue.append("A+")
sangue.append("A-")
sangue.append("B+")
sangue.append("B-")
sangue.append("AB+")
sangue.append("AB-")
sangue.append("O+")
sangue.append("O-")


# interface
sg.theme('DarkRed2')


def janela_inicial():
    layout = [
        [sg.Text('Mensageiro BDSU', font="unispace,26")],
        [sg.Text("")],
        [sg.Text("    "), sg.Combo(
            (sangue), key='select', default_value=None, size=10)],
        [sg.Text('    '), sg.Button("Enviar Email")]
    ]
    return sg.Window("BDSUM", layout=layout, finalize=True)


def janela_enviando():
    layout = [
        [sg.Text("Emails Enviados.")]
    ]
    return sg.Window("BDSUM", layout=layout, finalize=True)


janela1, janela2 = janela_inicial(), None

while True:
    window, event, values = sg.read_all_windows()

    if window == janela1 and event == "Enviar Email":
        if values['select'] == "":
            print('Escolha uma opção válida')
        else:
            sangue = values['select']
            ativar_envio(sangue)
            janela2 = janela_enviando()
            print("Enviando emails para usuarios cadastrados do tipo sanguíneo " +
                  str(values['select']))

 # fechar janelas
    if window == janela1 and event == sg.WINDOW_CLOSED:
        break
    if window == janela2 and event == sg.WINDOW_CLOSED:
        janela1.hide()
        janela2.hide()
        janela1.un_hide()
