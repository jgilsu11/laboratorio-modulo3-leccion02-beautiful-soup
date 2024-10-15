
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
import requests
from datetime import datetime

#Si uso una api key aquí necesito ponerla aquí también



def crear_df_pag(url):
    """
    Crea y devuelve un DataFrame con la información extraída de una página web específica de atrezzo.

    La función utiliza una URL proporcionada para hacer una solicitud HTTP y obtener el contenido HTML.
    Luego, extrae y organiza varios datos de la página, como el nombre del atrezzo, su categoría, 
    sección, descripción, dimensiones y la URL de su imagen.

    Args:
        url (str): La URL de la página web que se va a analizar y extraer.

    Returns:
        pd.DataFrame: Un DataFrame que contiene la información extraída de la página web, con las siguientes columnas:
            - nombre_atrezzo: El nombre del atrezzo.
            - imagen_atrezzo: La URL de la imagen del atrezzo.
            - categoria_atrezzo: La categoría a la que pertenece el atrezzo.
            - seccion_atrezzo: La sección de la página en la que está ubicado el atrezzo.
            - descripcion_atrezzo: La descripción del atrezzo.
            - largo: La longitud del atrezzo.
            - ancho: El ancho del atrezzo.
            - alto: La altura del atrezzo.

    Exceptions:
        Si ocurre algún error durante la solicitud HTTP o la extracción de datos, la función maneja la excepción y no devuelve nada.
    """

    try:    
        df_pag_pag= pd.DataFrame()
        resp= requests.get(url)
        sopa_atrezzo1= BeautifulSoup(resp.content, "html.parser")

        lista_nombre_at= sopa_atrezzo1.find_all("a", {"class": "title"})

        nombre_at=[nombre.getText() for nombre in lista_nombre_at]

        df_nombre_at= pd.DataFrame(nombre_at)

        df_nombre_at.drop(columns= 0, inplace=True)

        df_nombre_atrezzo= df_nombre_at.copy()

        df_nombre_atrezzo["nombre_atrezzo"]= nombre_at


        lista_categoria= sopa_atrezzo1.find_all("a", {"class": "tag"})
        categoria_at=[categoria.getText() for categoria in lista_categoria]
        df_cat_at= pd.DataFrame(categoria_at)
        df_cat_at.drop(columns= 0, inplace= True)
        df_cat_atrezzo= df_cat_at.copy()
        df_cat_atrezzo["categoria_atrezzo"]= categoria_at
        df_cat_atrezzo = df_cat_atrezzo.applymap(lambda x: x.replace("\n",""))


        lista_seccion= sopa_atrezzo1.find_all("div", {"class": "cat-sec-box"})  #Hemos cogido la box para que los indices coincidan (aunque haya algunos que vayan a tenerlo vacío por no tener seccion)
        seccion_at=[seccion.getText() for seccion in lista_seccion]
        df_sec_at= pd.DataFrame(seccion_at)
        df_sec_at.drop(columns= 0, inplace= True)
        df_sec_atrezzo= df_sec_at.copy()
        df_sec_atrezzo["seccion_atrezzo"]= seccion_at
        df_sec_atrezzo = df_sec_atrezzo.applymap(lambda x: x.replace("\n",""))


        lista_descripcion= sopa_atrezzo1.find_all("div", {"class": "product-slide-entry shift-image"}) 
        descripcion_at=[descripcion.contents[7].getText() for descripcion in lista_descripcion]
        df_des_at= pd.DataFrame(descripcion_at)
        df_des_at.drop(columns= 0, inplace= True)
        df_des_atrezzo= df_des_at.copy()
        df_des_atrezzo["descripcion_atrezzo"]= descripcion_at
        df_des_atrezzo = df_des_atrezzo.applymap(lambda x: x.replace("\n",""))

        lista_dimension= sopa_atrezzo1.find_all("div", {"class": "price"}) 
        dimension_at=[dimension.getText() for dimension in lista_dimension]
        df_dim_at= pd.DataFrame(dimension_at)
        df_dim_atrezzo= df_dim_at.copy()
        df_dim_atrezzo["descripcion_atrezzo"]= dimension_at
        df_dim_atrezzo = df_dim_atrezzo["descripcion_atrezzo"].str.split("x",expand=True)
        df_dim_atrezzo.columns = ["largo","ancho","alto"] 
        df_dim_atrezzo = df_dim_atrezzo.applymap(lambda x: x.replace("\n","").replace("(cm)","")).astype(int)


        lista_box= sopa_atrezzo1.find_all("div", class_ = "product-image" )
        imagenes_atrezo = [f"https://atrezzovazquez.es/{imagen.contents[0].get('src')}" for imagen in lista_box]
        df_de_imagen = pd.DataFrame(imagenes_atrezo,columns=["imagen_atrezzo"])


        df_pag_pag =pd.concat([df_pag_pag,df_nombre_atrezzo,df_de_imagen,df_cat_atrezzo,df_sec_atrezzo,df_des_atrezzo,df_dim_atrezzo], axis= 1) 

        return df_pag_pag
    
    except:
        pass





def creardf_final():
    """
    Crea y devuelve un DataFrame consolidado a partir de datos extraídos de múltiples páginas web.

    La función itera a través de 100 páginas de una tienda online, construyendo una URL específica para cada página.
    Para cada URL, extrae los datos utilizando la función 'crear_df_pag' y los concatena en un DataFrame final.

    Returns:
        pd.DataFrame: Un DataFrame que contiene la información consolidada de las 100 páginas web.
    """

    df_pag_final= pd.DataFrame()
    for pag in range(1,101):
        url= f"https://atrezzovazquez.es/shop.php?search_type=-1&search_terms=&limit=48&page={pag}"
        df_pag_final=pd.concat([df_pag_final,crear_df_pag(url)])
        
    return df_pag_final