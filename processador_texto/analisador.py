import spacy, docx, pickle, string, collections, re

def preprocess(infile: str):
    '''Util para agilizar o processo.
    Preprocessa o arquivo de texto em docx criando um .pkl com cada paragráfo.
    
    infile: caminho para o arquivo de entrada.'''
    doc = docx.Document(infile)
    alltext = []
    for para in doc.paragraphs:
        texto = para.text
        if len(texto) > 0:
            alltext.append(texto)
        else:
            alltext.append('\n')    
    pickle.dump(alltext,open('alltext.pkl','wb'))
    return print('Arquivo criado!')

def frequencia_termos(infile: str,outfile: str, tipo: str, minusculo: bool = False, infinitivo: bool = False):
    '''Conta a frequencia com que um determinado tipo de palavra aparece no texto.
    
    infile: caminho para o arquivo de entrada;
    outfile: caminho para o arquivo de saida;
    tipo: tipo de palavra a ser contabilizada, pode ser VERB (verbo), ADJ (adjetivo), PROPN (nome próprio); 
    minusculo: se vai transformar todas as palavras em minusculo (True ou False). Default = False;
    infinitivo: se deve converter as palavras para o infinitivo antes de contar (True ou False). Default = False'''
    
    if '.pkl' in infile:
        alltext = pickle.load(open(infile,'rb'))
    else:
        doc = docx.Document(infile)
        alltext = []
        for para in doc.paragraphs:
            texto = para.text
            if len(texto) > 0:
                alltext.append(texto)
            else:
                alltext.append('\n')

    pln = spacy.load('pt_core_news_lg')
    alltext = '\n'.join(alltext)
    
    alltext = alltext.lower().translate(str.maketrans('','',string.punctuation)) if minusculo else alltext.translate(str.maketrans('','',string.punctuation))
    
    tokens = pln(alltext)

    saida = []
    for token in tokens:
        if not minusculo:
            if token.tag_ == tipo and token.text[0].isupper():
                saida.append(token.text) if not infinitivo else saida.append(token.lemma_)
        else:
            if token.tag_ == tipo:
                saida.append(token.text) if not infinitivo else saida.append(token.lemma_)
        
    contagem = collections.Counter(saida)
    
    with open(outfile,'w',encoding='utf8') as f:
        for i in contagem:
            f.write(f'{i},{contagem[i]}\n')
         
    return print(contagem)

def corrige_parentese_fala(infile: str, outfile: str):
    alltext = pickle.load(open(infile,'rb'))

    with open(outfile,'w',encoding='utf8') as f:
        for para in alltext:
            para = re.sub('\s+',' ',para)
            if '-' in para[0:2]:
                if '(' in para:
                    para = re.sub(r'[()]','--',para)
                if para[0] == '-':
                    if not para[1] == ' ':
                        para = f'- {para[1:]}'

            f.write(f'{para}\n')