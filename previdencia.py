# aquirende-previdencia

#codigo gerado por fabio soares, para calculo de aposentadoria complementar

import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import plotly.express as px

#configuracao da pagina:
st.set_page_config(layout= 'wide', page_title = 'aposentei!')

#ajustando o cabecalho
st.write('<style>div.block-container{padding-top:1.5rem;}</style>', unsafe_allow_html=True)

st.title('Aposentei! E agora?')
st.subheader('Para que possamos viver a nossa melhor idade com tranquilidade, devemos pensar agora em planejar nosso futuro financeiro')

#Grafico do retorno acumulado:------------------------------------------------------------------------------

def gera_grafico(df_simulacao, nome):
    fig = plt.figure()
    fig=px.bar(df_simulacao, x =df_simulacao.mes, y = ['meu dinheiro', 'montante'], color_discrete_sequence=["#FFA15A", "#636EFA"]) #EF553B
    fig.update_yaxes(title = 'Total Acumulado em R$')  
    fig.update_xaxes(title = 'Tempo em meses')
    fig.update_layout(title_text = f'Seu dinheiro acumulando {nome.upper()}, ao longo do tempo:', legend_title_text = '')
    fig.update_layout(showlegend = True)

    st.plotly_chart(fig , use_container_width = True)
    st.write(' Veja a importância de pensar no longo prazo: O gráfico acima mostra :orange[em Laranja], o valor que você foi depositando no período e :blue[em Azul], o efeito do juros ao longo do tempo, aumentando de forma exponencial 🚀 o seu montante total 💵💵')
    #st.write(fig)
    return(fig)
# fim do grafico de investimentos


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

    #st.markdown('Para isso, vamos utilizar nosso simulador de aposentadoria, onde identificamos hoje, o que precisamos fazer para chegar no nosso futuro de forma garantida 🏖️')
    #st.markdown('Vamos lá construir o seu futuro financeiro?')
   # st.markdown('Use o simulador a seguir para calcular quanto de dinheiro você consegue reservar e a renda que virá no futuro, fruto desta reserva  e veja como se preparar para viver a melhor fase da sua vida!')
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

        dinheiro_inicial = st.number_input('Digite a quantidade de dinheiro inicial do Investimento:',value = None, min_value=10, placeholder= 'R$:')
        
        
        if dinheiro_inicial != None:
            with col2:
                st.write('')
                st.write('* Você vai Investir R$: :green[{:,.2f}]'.format(dinheiro_inicial).replace(',', '-').replace('.', ',').replace('-', '.'))

            tempo_desejado = st.slider('Digite quantos MESES você deixará o dinheiro investido:', 0, 780, 36, step = 6)
            if tempo_desejado != None:
                st.write(f'**Você escolheu investir por** :red[{(tempo_desejado/12)} anos] ⌛')
        
                with col2:
                    st.write(f'* Este valor vai ficar investido por {tempo_desejado} meses  ou :red[{(tempo_desejado/12)} anos]')

                taxa = st.slider('Escolha a Taxa Mensal de Retorno do seu Investimento que você está buscando:', value = None , min_value = 0.00, max_value = 3.00,  step = 0.10, format= '%f')  
                if taxa:
        
                    with col2:
                        st.write(F' * E vamos buscar um retorno de {taxa} % AM de Taxa de Juros ')
   
                    
                    taxa = taxa/100 # transformei na taxa decimal para o calculo

                    aporte = st.slider('Quanto de dinheiro você consegue depositar mensalmente: R$ ', min_value = 0, max_value = 10000, step = 50)
                    if aporte:

                        with col2:
                            st.write(' * Você vai depositar + R$: {:,.2f} todos os meses!'.format(aporte))

                    salario_desejado = st.number_input('Digite o Salário mensal que você quer receber ao se aposentar:', value = None , format = '%.f')  

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

                        #with col2:
                        #    limpar = st.button('Nova Simulação')
                        #    if limpar:
                                
                        #        nome = nome.new_value("")
                        #        st.rerun()

                    except:
                        st.error('Você ainda não informou todos os dados solicitados')



