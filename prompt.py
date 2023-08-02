template = """Eres un chatbot asistente amistoso y educado. Estas conversando con "Jesus Milano"
    Utilizando la informacion proporcionada. Responde siempre de manera clara, directa, y muy concisa. 
    Cuando te pregunten sobre algo, retorna el enlace correspondiente que más ayudará a responder la pregunta, 
    solo si el enlace existe en el contexto, no crees enlaces. 
    Por ejemplo si te preguntan "¿Como subo una transacción?" 
    responde "Aquí puedes ver un tutorial sobre como subir una transacción" y comparte el enlace correspondiente
    {context}
    Pregunta: {question}
    Respuesta:"""

sources = [
  "https://blog.valiapro.com/faq/nuevo-newsfeed", # ¿Cómo utilizar el News Feed?
  "https://blog.valiapro.com/faq/reglas-newsfeed", # Reglas para el uso del News Feed
  "https://blog.valiapro.com/valia-flex", # ¿Qué es el programa Valia Flex?
  "https://blog.valiapro.com/que-son-las-colecciones", # ¿Qué son las Colecciones Valia y cómo crearlas?
  "https://blog.valiapro.com/c%C3%B3mo-subir-un-inmueble-a-valia", # Cómo subir un inmueble a Valia
  "https://blog.valiapro.com/faq/tutorial-como-usar-el-buscador-de-inmuebles-de-valia", # Cómo usar el Buscador de Inmuebles de Valia
  "https://blog.valiapro.com/como-encontrar-inmuebles-de-otros-agentes-en-valia", # Cómo encontrar inmuebles de otros Agentes en Valia
  "https://blog.valiapro.com/como-encontrar-pedidos-de-otros-agentes-en-valia", # Cómo encontrar pedidos de otros Agentes en Valia
  "https://blog.valiapro.com/como-subir-una-transaccion-a-valia", # Cómo subir una transacción a Valia
  "https://blog.valiapro.com/c%C3%B3mo-puedo-ver-mi-historial-de-reportes-en-valia", # ¿Cómo puedo ver mi historial de reportes en Valia?
  "https://blog.valiapro.com/como-hacer-un-analisis-comparativo-de-mercado-amc-con-valia", # Cómo hacer un Análisis Comparativo de Mercado (ACM) con Valia
  "https://blog.valiapro.com/como-hacer-analisis-de-oferta-de-mercado-inmobiliario-aom-valia", # Cómo hacer un Análisis de la Oferta de Mercado (AOM) con Valia
  "https://blog.valiapro.com/como-hacer-un-reporte-de-valuacion-inmobiliaria-con-valia", # Cómo hacer un reporte de valuación inmobiliaria con Valia
  "https://blog.valiapro.com/como-actualizar-mi-metodo-de-pago-en-valia", # Cómo actualizar mi método de pago en Valia
  "https://blog.valiapro.com/c%C3%B3mo-puedo-ver-y-descargar-los-recibos-de-subscripci%C3%B3n-en-valia", # ¿Cómo puedo ver y descargar los Recibos de subscripción en Valia?
  "https://blog.valiapro.com/qu%C3%A9-es-valia-y-c%C3%B3mo-funciona-gu%C3%ADa-completa-para-agentes-inmobiliarios", # ¿Qué es Valia y cómo funciona? Guía completa para Agentes Inmobiliarios
  "https://blog.valiapro.com/c%C3%B3mo-crear-tu-perfil-valia-en-3-minutos", # Cómo crear tu Perfil Valia en 3 minutos
  "https://blog.valiapro.com/c%C3%B3mo-puedo-recuperar-mi-contrase%C3%B1a-en-valia", # ¿Cómo puedo recuperar mi contraseña en Valia?
  "https://blog.valiapro.com/como-activar-7-dias-de-prueba-gratis-valiapro", # Cómo activar 7 días de prueba gratis ValiaPro
]