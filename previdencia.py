# aquirende-previdencia
#codigo gerado por Fabio Soares, para calculo de aposentadoria complementar

import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import plotly.express as px
from fpdf import FPDF

#para enviar por email o resultado:
#import os
import smtplib
from email.message import EmailMessage

#configuracao da pagina:
st.set_page_config(layout= 'wide', page_title = 'aposentei!')

#ajustando o cabecalho
st.write('<style>div.block-container{padding-top:1.5rem;}</style>', unsafe_allow_html=True)

st.title('Aposentei! E agora?')
st.subheader('Para que possamos viver a nossa melhor idade com tranquilidade, devemos pensar agora em planejar nosso futuro financeiro')

#Grafico do retorno acumulado:------------------------------------------------------------------------------
@st.cache_data
def gera_grafico(df_simulacao, nome):
    fig = plt.figure()
    fig=px.bar(df_simulacao, x =df_simulacao.mes, y = ['meu dinheiro', 'montante'], color_discrete_sequence=["#FFA15A", "#636EFA"]) #EF553B
    fig.update_yaxes(title = 'Total Acumulado em R$')  
    fig.update_xaxes(title = 'Tempo em meses')
    fig.update_layout(title_text = f'Seu dinheiro acumulando {nome.upper()}, ao longo do tempo:', legend_title_text = '')
    fig.update_layout(showlegend = True)
    st.plotly_chart(fig , use_container_width = True)
    st.write(' Veja a importância de pensar no longo prazo: O gráfico acima mostra :orange[em Laranja], o valor que você foi depositando no período e :blue[em Azul], o efeito do juros ao longo do tempo, aumentando de forma exponencial 🚀 o seu montante total 💵💵')
    
    fig.write_image('grafico.png', engine = 'kaleido') #gravar o grafico para levar para o pdf

    return(fig)
# fim do grafico de investimentos

#funcao para gerar o pdf para o usuario -------------------------------------------------------------
@st.cache_data
def gera_pdf(df_simulacao, nome,dinheiro_inicial,tempo_desejado,aporte,taxa, montante, salario_mensal):
    try:

        meus_depositos      = df_simulacao['meu dinheiro'].iloc[-1]
        juros               = df_simulacao['rendimento'].sum().round(2)

        # 1. Setup básico do PDF
        #Criamos o pdf
        pdf = FPDF('P', 'mm', (210, 297)) #pdf = FPDF()

        # Define as margens esquerda, superior, direita (em milímetros) e rodape
        pdf.set_margins(15, 10, 15)
        pdf.set_auto_page_break(True, margin= 5)  # 5 mm do rodapé

        #Adicionamos uma nova página. antes era so um arquivo virtual
        pdf.add_page()

        #Setup de fonte
        pdf.set_font('Arial', 'B', 16)

        # 2. Layout do pdf

        ## Título
        pdf.cell(40, 10, '                  Análise de Simulação de Aposentadoria ')

        ## Quebra de linha
        pdf.ln(14)

        #comentarios
        pdf.set_font('Arial', 'B', 11)
        pdf.write(5, 'Como é bom não ter que se preocupar com dinheiro não é mesmo?')
        pdf.ln(7.3)
        pdf.set_font('Arial', '', 11)
        pdf.write(5,'Imagina chegar na sua melhor idade e não ter problemas para manter o seu padrão de gastos de hoje, ou mesmo melhorar a renda\
        a receber além da aposentadoria oficial. Para isso é fundamental termos uma reserva para o nosso futuro!')
        pdf.ln(7.3)
        pdf.write(5, 'Por isso, pensando no seu futuro {} e com base nos valores informados por você durante a simulação, veremos a seguir, uma análise das suas finanças para a sua MELHOR IDADE,\
        através de uma Previdência Privada'.format(nome.upper()))
        pdf.ln(8)
        pdf.set_font('Times', 'B', 11)
        pdf.cell(20, 7, 'Resultado da Simulação:')
        pdf.ln(9)
        pdf.set_font('Arial', '', 11)
        pdf.write(5, 'Você escolheu investir R$: {:,.2f} por {} meses. acrescentando todos os meses R$ {:,.2f} e desejando\
        uma taxa mensal de juros de {:.2f} %am,'.format(dinheiro_inicial,tempo_desejado,aporte,(taxa*100)).replace(',', '-').replace('.', ',').replace('-', '.'))
        pdf.ln(6)
        pdf.write(5,'Ao final do periodo, você terá acumulado o montante de R${:,.2f}. o que\
        deve lhe proporcionar uma renda mensal de aproximadamente R$ {:,.2f}*'.format(montante,salario_mensal).replace(',', '-').replace('.', ',').replace('-', '.'))

        pdf.ln(8.5)
        pdf.image('grafico.png', w=160, h=100)
        pdf.ln(2)
        pdf.set_font('Arial', '', 10)
        pdf.write(5,'Veja a importância de pensar no longo prazo: O gráfico acima mostra em Laranja, o valor que você foi depositando no período e em Azul,\
        o efeito do juros ao longo do tempo, que aumenta o seu montante total.')

        pdf.ln(8)
        pdf.write(5,'Em resumo:')
        pdf.ln(6)
        pdf.set_font('Arial', 'B', 11)
        pdf.write(5,'Seus depósitos: R$ {:,.2f}     Juros: R$ {:,.2f}      Montante Acumulado: R$ {:,.2f}'.format(meus_depositos, juros, montante).replace(',', '-').replace('.', ',').replace('-', '.'))

        pdf.ln(9)
        pdf.set_font('Arial', '', 10)
        pdf.write(5,'{}, Faça uma revisão nos valores que você sugeriu para a sua aposentadoria e se estiver de acordo, vamos\
        começar agora mesmo a construir esta história juntos!'.format(nome.upper()))
        pdf.ln(12)

        # 3. logo
        pdf.image('paola_foto.PNG', w=20, h=20)
        pdf.ln(2)

        # 4. Assinatura
        pdf.set_font('Times', '', 12)
        pdf.cell(5, 2, 'Paola Bitencourt, Educação Financeira. ')
        pdf.ln(4)
        pdf.set_font('Times', '', 10)
        pdf.cell(5, 2, 'https://meuscontatos.streamlit.app')
        pdf.ln(12)

        # 5. Disclaimer
        pdf.set_font('Arial', '', 6.5)
        pdf.write(5,'*Obs: Renda mensal projetada c/ base na taxa de juros informada na simulação, o que pode variar o resultado a receber, em função do retorno real do seu investimento.')
        pdf.ln(4.5)

        pdf.set_font('Times', '', 8)
        pdf.cell(5, 2, 'Todos os direitos reservados ©')

        # 6. Output do PDF file
        pdf.output('aposentei.pdf', 'F')
    except:
        st.error('Problemas ao gerar a simulação em pdf!🚨 - Fale com seu Assessor!')
    return()
#fim da funcao para gerar o pdf ----------------------------------------------------------------------


#funcao para enviar email ao usuario:-----------------------------------------------------------------
@st.cache_data
def gera_email(nome,email):
    meuemail = "apaolabitt@gmail.com"
    #parte do codigo para acessar a senha salva em arquivo
    #with open('senha.txt') as f:
    #    senha = f.readlines()
#
 #       f.close()

    senha_do_email = st.secrets["db_password"]


    #corpo do email
    texto = """
    Olá {}! Como vai?
    Segue a simulação feita para o seu futuro financeiro!

    Revise os valores que você sugeriu para a sua Aposentadoria e se estiver de acordo, vamos começar já a construir esta história juntos!

    Nos falamos em breve!

    Um abraço!

    Paola Bittencourt

    contatos:
    https://meuscontatos.streamlit.app/
    """.format(nome.upper())

    #configuracao dos dados do email
    msg = EmailMessage()
    msg['Subject']  = (f'Seu futuro começa aqui {nome.upper()}')
    msg['From'] = 'apaolabitt@gmail.com'
    msg['To'] = email
    msg.set_content(texto)

    #arquivo a ser enviado
    
    #cabecalho do email
    with open('cabecalho.png', 'rb') as content_file:
        content = content_file.read()
        msg.add_attachment(content, maintype='application', subtype='png', filename='cabecalho.png')
    
    #arquivo a ser enviado
    with open('aposentei.pdf', 'rb') as content_file:
        content = content_file.read()
        msg.add_attachment(content, maintype='application', subtype='pdf', filename='aposentei.pdf')

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(meuemail, senha_do_email)
        smtp.send_message(msg)
        st.success('E-mail com a simulação Enviado com sucesso!')
    return()
# fim da funcao de geracao de email:

#envia email para o dono da pagina:-----------------------------------------------------------------
@st.cache_data
def novo_cliente(nome,email, telefone):
    meuemail = "apaolabitt@gmail.com"
    #parte do codigo para acessar a senha salva em arquivo
    #with open('senha.txt') as f:
     #   senha = f.readlines()
#
       # f.close()

    senha_do_email = st.secrets["db_password"]

    #corpo do email
    texto = """
    Olá Paola! Como vai?
    Você acaba de receber uma nova simulação feita pelo usuário {}

    Entre em contato pelo telefone {} ou email {}, e tenha uma ótima reunião!

    AquiRende ©
    """.format(nome.upper(), telefone, email)

    #configuracao dos dados do email
    msg = EmailMessage()
    msg['Subject']  = (f'Simulação de Aposentadoria para {nome.upper()}')
    msg['From']     = 'apaolabitt@gmail.com'
    msg['To']       = 'apaolabitt@gmail.com'
    msg.set_content(texto)

    #arquivo a ser enviado
    with open('aposentei.pdf', 'rb') as content_file:
        content = content_file.read()
        msg.add_attachment(content, maintype='application', subtype='pdf', filename='aposentei.pdf')

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(meuemail, senha_do_email)
        smtp.send_message(msg)
    return()
# fim da funcao de geracao de email:

col1, col2 = st.columns(2)

with col1:
    st.write('')
    st.markdown('O seu futuro, será fruto do que foi construído ao longo do tempo. ⌛')
    st.markdown('Seja para manter o padrão de gastos de hoje ou melhorar o valor a receber da aposentadoria oficial,  é fundamental termos uma reserva para o nosso futuro! ')
    st.write('')
    st.image('renda_complementar.jpg',width= 350)
    st.markdown("<p style='text-align: left;'>foto: inovo.org</p>", unsafe_allow_html=True)
    st.write('')
    st.markdown('Afinal, guardar dinheiro 💵 também é cuidar de quem você ama! E o quanto antes começarmos, menor será nosso esforço, pois os juros e o tempo irão trabalhar a nosso favor!')
    
    st.image('futuro.jpg',width= 350)
    st.markdown('foto: familius.com')

with col2:
    st.image('casal.jpeg',width= 450, use_column_width= True)
    st.markdown("<p style='text-align: center;'>foto: revistadorh.com.br</p>", unsafe_allow_html=True)
    st.write('')
    st.write('')
    st.markdown('Para isso, vamos utilizar nosso simulador de aposentadoria, onde identificamos hoje, o que precisamos fazer para chegar no nosso futuro de forma garantida 🏖️')
    st.markdown('Vamos lá construir o seu futuro financeiro?')
    st.markdown('Use o simulador a seguir para calcular quanto de dinheiro você consegue reservar e a renda que virá no futuro, fruto desta reserva  e veja como se preparar para viver a melhor fase da sua vida!')
    
st.divider()

col1, col2 = st.columns(2)
col_grafico, col_dados = st.columns([0.6,0.4])


st.caption('Simulador desenvolvido por Fábio Soares, Cientista de dados e Especialista em Investimentos - CEA Anbima')
st.caption('Contato: ✉︎ ofabiosoares@outlook.com')
with col1:

    nome = st.text_input('Qual o seu Nome?', value = '')
    if nome:
        with col2:
            st.write('')
            st.write('**Resultado** da Simulação:')
            st.write(f'Olá {nome.upper()}, seja muito bem vindo(a) ao SEU FUTURO! Aqui, nós estamos cuidando da sua Aposentadoria!')

        dinheiro_inicial = st.number_input('Digite a quantidade de dinheiro inicial do Investimento:',value = None, min_value=10, placeholder= 'Digite em R$ e tecle ENTER', help = 'Digite o valor e tecle ENTER para continuar')
        
        if dinheiro_inicial != None:
            with col2:
                st.write('')
                st.write('* Você vai Investir R$: :green[{:,.2f}]'.format(dinheiro_inicial).replace(',', '-').replace('.', ',').replace('-', '.'))

            tempo_desejado = st.slider('Digite quantos MESES você deixará o dinheiro investido:', 0, 780, 36, step = 6, help = 'deslize a barra para alterar o prazo ')

            if tempo_desejado != None:
                st.write(f'**Você escolheu investir por** :red[{(tempo_desejado/12)} anos] ⌛')
                with col2:
                    st.write(f'* Este valor vai ficar investido por {tempo_desejado} meses  ou :red[{(tempo_desejado/12)} anos]')

                taxa = st.slider('Escolha a Taxa Mensal de Retorno do seu Investimento que você está buscando:', value = None , min_value = 0.00, max_value = 3.00,  step = 0.10, format= '%f', help = 'deslize a barra para alterar a taxa de JUROS ') 

                if taxa:
                    with col2:
                        st.write(F' * E vamos buscar um retorno de {taxa} % AM de Taxa de Juros ')
   
                    taxa = taxa/100 # transformei na taxa decimal para o calculo

                    aporte = st.slider('Quanto de dinheiro você consegue depositar mensalmente: R$ ', min_value = 0, max_value = 10000, step = 50, help = 'deslize a barra para informar o valor em R$ dos depositos mensais')

                    if aporte:
                        with col2:
                            st.write(' * Você vai depositar + R$: {:,.2f} todos os meses!'.format(aporte))
                    
                    st.markdown('Ótimo! **Para terminar**, só falta informar seus meios de contato 📩 📞e a renda 💰 que deseja ter mensalmente ao se aposentar, e vamos enviar para você, um relatório super completo e personalizado do seu futuro financeiro!💵')
                    
                    email    = st.text_input('Digite seu melhor e-mail?', value = '') 
                    if email != '':
                        
                        telefone = st.number_input('Digite seu telefone com DDD: 📞', value = 0, format = '%i', key = 'tel',  help= 'Digite somente números e tecle ENTER', placeholder= 'somente números e tecle ENTER')
                        if telefone != None and telefone != 0:
            
                            salario_desejado = st.number_input('Digite o Salário mensal que você quer receber ao se aposentar:', value = None , format = '%.f', help = 'Digite o valor e tecle ENTER', placeholder= 'digite o valor e tecle ENTER')  

                    tempo_decorrido = 0
                    dados = []

                    while tempo_decorrido < tempo_desejado:
  
                        if tempo_decorrido == 0:
  
                            montante = (dinheiro_inicial) *(1+taxa)** 1 #tempo inicial
                            montante = round(montante,2)
                            tempo_decorrido = tempo_decorrido +1
    
                            #incluir isso
                            rendimento = (montante) - (dinheiro_inicial) 
                            rendimento = round(rendimento,2)
                            meu_dinheiro = (dinheiro_inicial)                            
    
                            dicionario = {'montante':montante, 'mes':1, 'rendimento': rendimento,'aporte':0, 'meu dinheiro': meu_dinheiro}
                            dados.append(dicionario)
                    
                        else:
                            meu_dinheiro = (meu_dinheiro + aporte) 
                            rendimento = ((montante + aporte) *(1+taxa)** 1 ) - (montante + aporte)
                            montante = (montante + aporte) *(1+taxa)** 1 #tempo inicial
                            montante = round(montante,2)
                            tempo_decorrido = tempo_decorrido +1
                            rendimento = round(rendimento,2)
                            
                            dicionario = {'montante':montante, 'mes':tempo_decorrido, 'rendimento': rendimento, 'aporte':aporte, 'meu dinheiro': meu_dinheiro}
                            dados.append(dicionario)

                    df_simulacao = pd.concat([pd.DataFrame([d]) for d in dados])

                    st.divider()
                    with col2:
                        st.write('')
                        st.write(':green[Parabéns] {}! \n\nAo final do período ⌛ você terá Acumulado R$: {:,.2f} 💰💸'.format(nome.upper(), montante).replace(',', '-').replace('.', ',').replace('-', '.'))
                    

                    salario_mensal = (montante*taxa)
                    salario_mensal = round(salario_mensal,2)

                    try:

                        if salario_mensal >= salario_desejado:
                            with col2:
                                st.success(':green[Parabéns!] Você pode se aposentar! Seu **Salário mensal** com este montante será de aproximadamente R$: {:,.2f}'.format(salario_mensal).replace(',', '-').replace('.', ',').replace('-', '.'), icon="✅")
                                st.balloons()
                                st.subheader('Confira **abaixo**, um resumo sobre sua simulação:')

                            with col_grafico: #grafico:
                                fig = gera_grafico(df_simulacao, nome)

                            with col_dados:
                                st.metric('Montante Acumulado:', value = "R$ {:,.2f} 💵 ".format(df_simulacao['montante'].iloc[-1].round(2)).replace(',', '-').replace('.', ',').replace('-', '.'))
                                st.metric('Juros   :'          , value = "R$ {:,.2f} 🚀".format(df_simulacao['rendimento'].sum().round(2)).replace(',', '-').replace('.', ',').replace('-', '.'))
                                st.metric('Meus depósitos   :' , value = "R$ {:,.2f} 💰 ".format(df_simulacao['meu dinheiro'].iloc[-1]).replace(',', '-').replace('.', ',').replace('-', '.'))
                            
                            #gera o pdf com os dados da simulacao
                            gera_pdf(df_simulacao, nome,dinheiro_inicial,tempo_desejado,aporte,taxa, montante, salario_mensal)
                            gera_email(nome,email)
                            novo_cliente(nome,email, telefone)
   
                        elif salario_mensal < salario_desejado:
                            with col2:
                                st.warning(":red[Infelizmente] você não atingiu o Salário desejado, Com este montante. seu **Salário Mensal** será de aproximadamente R$ {:,.2f}".format(salario_mensal).replace(',', '-').replace('.', ',').replace('-', '.'))
                                st.subheader('Confira **abaixo**, um resumo sobre sua simulação:')

                            with col_grafico: #grafico:
                                fig = gera_grafico(df_simulacao, nome)
                            
                            with col_dados:
                                st.metric('Montante Acumulado:', value = "R$ {:,.2f} 💵 ".format(df_simulacao['montante'].iloc[-1].round(2)).replace(',', '-').replace('.', ',').replace('-', '.'))
                                st.metric('Juros   :'          , value = "R$ {:,.2f} 🚀".format(df_simulacao['rendimento'].sum().round(2)).replace(',', '-').replace('.', ',').replace('-', '.'))
                                st.metric('Meus depósitos   :' , value = "R$ {:,.2f} 💰 ".format(df_simulacao['meu dinheiro'].iloc[-1]).replace(',', '-').replace('.', ',').replace('-', '.'))

                            #gera o pdf com os dados da simulacao
                            gera_pdf(df_simulacao, nome,dinheiro_inicial,tempo_desejado,aporte,taxa, montante, salario_mensal)
                            gera_email(nome,email)
                            novo_cliente(nome,email, telefone)


                    except:
                        st.error('Você ainda não informou todos os dados solicitados')

