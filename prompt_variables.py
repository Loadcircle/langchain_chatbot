template = """Eres un ux writer, utilizando todo el contexto, redacta un post detallado similar a estos
    Sobre el input ingresado, debe tener un largo considerable, similar a los del contexto
    Si consideras necesario el uso de imagenes dejalo referenciado como [imagen]  
    {context}
    Input: {question}
    Post: <<>>
    
    """

sources = [
  {
      "source": "https://blog.valiapro.com/faq/nuevo-newsfeed",
      "description": "¿Cómo utilizar el News Feed?"
  },
  {
      "source": "https://blog.valiapro.com/faq/reglas-newsfeed",
      "description": "Reglas para el uso del News Feed"
  },
  {
      "source": "https://blog.valiapro.com/valia-flex",
      "description": "¿Qué es el programa Valia Flex?"
  },
  {
      "source": "https://blog.valiapro.com/que-son-las-colecciones",
      "description": "¿Qué son las Colecciones Valia y cómo crearlas?"
  },
  {
      "source": "https://blog.valiapro.com/c%C3%B3mo-subir-un-inmueble-a-valia",
      "description": "Cómo subir un inmueble a Valia"
  },
  {
      "source": "https://blog.valiapro.com/faq/tutorial-como-usar-el-buscador-de-inmuebles-de-valia",
      "description": "Cómo usar el Buscador de Inmuebles de Valia"
  },
  {
      "source": "https://blog.valiapro.com/como-encontrar-inmuebles-de-otros-agentes-en-valia",
      "description": "Cómo encontrar inmuebles de otros Agentes en Valia"
  },
  {
      "source": "https://blog.valiapro.com/como-encontrar-pedidos-de-otros-agentes-en-valia",
      "description": "Cómo encontrar pedidos de otros Agentes en Valia"
  },
  {
      "source": "https://blog.valiapro.com/como-subir-una-transaccion-a-valia",
      "description": "Cómo subir una transacción a Valia"
  },
  {
      "source": "https://blog.valiapro.com/c%C3%B3mo-puedo-ver-mi-historial-de-reportes-en-valia",
      "description": "¿Cómo puedo ver mi historial de reportes en Valia?"
  },
  {
      "source": "https://blog.valiapro.com/como-hacer-un-analisis-comparativo-de-mercado-amc-con-valia",
      "description": "Cómo hacer un Análisis Comparativo de Mercado (ACM) con Valia"
  },
  {
      "source": "https://blog.valiapro.com/como-hacer-analisis-de-oferta-de-mercado-inmobiliario-aom-valia",
      "description": "Cómo hacer un Análisis de la Oferta de Mercado (AOM) con Valia"
  },
  {
      "source": "https://blog.valiapro.com/como-hacer-un-reporte-de-valuacion-inmobiliaria-con-valia",
      "description": "Cómo hacer un reporte de valuación inmobiliaria con Valia"
  },
  {
      "source": "https://blog.valiapro.com/como-actualizar-mi-metodo-de-pago-en-valia",
      "description": "Cómo actualizar mi método de pago en Valia"
  },
  {
      "source": "https://blog.valiapro.com/c%C3%B3mo-puedo-ver-y-descargar-los-recibos-de-subscripci%C3%B3n-en-valia",
      "description": "¿Cómo puedo ver y descargar los Recibos de subscripción en Valia?"
  },
  {
      "source": "https://blog.valiapro.com/qu%C3%A9-es-valia-y-c%C3%B3mo-funciona-gu%C3%ADa-completa-para-agentes-inmobiliarios",
      "description": "¿Qué es Valia y cómo funciona? Guía completa para Agentes Inmobiliarios"
  },
  {
      "source": "https://blog.valiapro.com/c%C3%B3mo-crear-tu-perfil-valia-en-3-minutos",
      "description": "Cómo crear tu Perfil Valia en 3 minutos"
  },
  {
      "source": "https://blog.valiapro.com/c%C3%B3mo-puedo-recuperar-mi-contrase%C3%B1a-en-valia",
      "description": "¿Cómo puedo recuperar mi contraseña en Valia?"
  },
  {
      "source": "https://blog.valiapro.com/como-activar-7-dias-de-prueba-gratis-valiapro",
      "description": "Cómo activar 7 días de prueba gratis ValiaPro"
  }
]

link_sources = [item["source"] for item in sources]

link_validator_template =  """Given a raw text input \
    select the link best suited for the input. \
    You will be given the available links and a \
    description of what the link is best suited for. \

    << FORMATTING >>
    Return a plain text formatted to look like:
    "link": string \ only the link, remove any text that is not part of the link to use or "NONE"


    REMEMBER: "source" MUST be one of the candidate links, just the link, no the description or any other text \
    specified below OR it can be "NONE" if the input is not\
    well suited for any of the candidate links.

    << CANDIDATE LINKS >>
    {sources}

    << INPUT >>
    {{input}}

    << OUTPUT (remember just return a plain text link, remove anything that is not part of the link or return "NONE")>>"""


validator_template = """
    Eres un verificador de informacion, dado el siguiente contexto debes verificar que la respuesta dada por un asistente\
    es veraz y factual. Si la respuesta es correcta dado el contexto, verifica que la respuesta cumpla con los siguientes parametros:\
        1 - No debe tener mas de 300 caracteres
        2 - Debe estar escrita en un lenguaje humano natural
        3 - Debe ser un lenguaje amistoso y educado 
        4 - No debe mencionar iniciar sesion en valia.
    
    Si la informacion es factual y veraz dado el contexto, asegurate de que cumpla los 4 parametros. Haz las modificaciones\
    necesarias, siempre manteniendo un lenguaje amistoso y educado. Si no es necesario retorna la respuesta tal cual la recibiste

    Si la informacion no es factual y veraz, realiza las correcciones necesarias, si en el contexto no tienes la informacion necesaria\
    retorna un mensaje educado indicando que no lo sabes 
    
    << contexto >>
    {context}

    << respuesta >>
    {question}

    << OUTPUT (recuerda, verifica que la respuesta compla con los parametros, no hagas modificaciones innecesarias, \
    si comple con los parametros retorna la respuesta tal cual la has recibido) >>
"""