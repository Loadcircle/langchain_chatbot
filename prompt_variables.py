template = """Eres un chatbot asistente amistoso y educado. Estas conversando con "Jesus Milano"
    Utilizando la informacion proporcionada. Responde siempre de manera clara, directa, y muy concisa. 
    No des informacion que no tengas disponible, si te preguntan algo que no sabes, responde de forma educada
    que no lo sabes
    {context}
    Pregunta: {question}
    Respuesta:"""

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

link_validator_template = """Dada la siguiente pregunta, determina cual de los siguientes enlaces \
  segun su descripcion, es mas acertado para encontrar la respuesta a la pregunta

  << FORMATTING >>
  retorna el enlace en una sola linea de texto, sin ningun tipo de informacion adicional\
  por ejemplo: si determinas que la pregunta es sobre como encontrar inmuebles retorna \
  "https://blog.valiapro.com/como-encontrar-inmuebles-de-otros-agentes-en-valia"
  si consideras que no hay un enlace que responda de forma apropiada la pregunta simplemente retorna "NONE"\
  

  recuerda: no intentes crear enlaces, si no estas seguro solo retorna "NONE"\
  los enlaces deben ser solo uno de los indicados abajo\

  << CANDIDATE sources >>
  {sources}

  << QUESTION >>
  {{question}} """