from django.shortcuts import render
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
#funciones necesarias de limpiza y stiming
def top3Doc(X,index):
    similares = cosine_similarity(X[index:index+1], X).flatten() 
    #vamos a llamar a la libreria  numpy
    #para ordenar los indices
    import numpy as np
    #con el metodo argsort() ordenos los indices sin tocar 
    #los volores
    #como ordena de menor a mayor asi q 
    #ponemos [::-1] para que me ordene de manera decreciente 
    orderindices = np.array(similares).argsort()[::-1]
    #eliminamos el index osea el archivo que se compara con todos ya q se esta hablando de texto q se esta
    #analizando
    modified_array = np.delete(orderindices, np.where(orderindices == index))
    #sacar los 2 textos similares
    return {'idice':list(modified_array[:3]),'proporcion':[similares[xf] for xf in modified_array[:3]]}

def procesarTfidf(index, corpus):    
    #palabras bacias en spaniol
    vectorizer = []
    #creacion con el texto en crudo 
    vectorizer.append(TfidfVectorizer())
    #creamos una lista con todos los  tipos de vectorizer 'texto pila' , 'con stop words' etc
    lista_tras = [vec.fit_transform(corpus) for vec in vectorizer]
    #%%
    #similaridad  traenmos el top 3 de textos similares 
    list_top3 =[top3Doc(X,index) for X in lista_tras]  
    
    lista1 = []
    lista2 = []
    for xdic in list_top3:
        lista1 += xdic['idice']
        lista2 += xdic['proporcion']
        
    return [lista1 , lista2]  


#######################################################
###################PRINCIPAL###########################





# Create your views here.
def index(request):
    archivo_excel = pd.ExcelFile('/home/ali/Documentos/prjectFInalrain/tpfinal/web/letras_de_canciones.xlsx')
    df=archivo_excel.parse()
    list_10=df['title'][0:10].tolist()
    c= [(i,x,df['musica'][i]) for i,x in enumerate(list_10)]

    return render(request, "web/index.html",{'top_10':c})

def add(request):
    
    val1 = int(request.POST['num'])
    archivo_excel = pd.ExcelFile('/home/ali/Documentos/prjectFInalrain/tpfinal/web/letras_de_canciones.xlsx')
    df=archivo_excel.parse()
    articulos = df['texto'].tolist()
    orden2=procesarTfidf(val1, articulos[:1000])
    titu =[(df['title'][x],df['musica'][x],df['texto'][x]) for x in orden2[0]]
    titulo=df['title'][val1] 
    letra=df['texto'][val1] 
    return render(request, "web/result.html", {'titu_similares': titu , 'result':titulo , 'leta':letra})