import time
import os
import random
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from supabase import create_client, Client

# ==============================================================================
# CONFIGURACIÓN (VARIABLES DE ENTORNO OCULTAS)
# ==============================================================================
SUPABASE_URL = os.environ.get('SUPABASE_URL')
SUPABASE_KEY = os.environ.get('SUPABASE_KEY')

# Cambiamos los nombres aquí para que coincidan con el resto de tu código
SMTP_USER = os.environ.get('EMAIL_ORIGEN')
SMTP_PASS = os.environ.get('EMAIL_PASS')

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

LIMITE_DIARIO = 45 
# Tiempos de espera en segundos (300 a 900 = entre 5 y 15 minutos de pausa por correo)
ESPERA_MINIMA = 180
ESPERA_MAXIMA = 300

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def generate_copy(local_name, rating, reviews_count):
    rating_text = f"{rating}" if rating else "buenas"
    reviews_text = f"{reviews_count}" if reviews_count else "algunas"
    url_imagen = "https://placa-nfc-1.vercel.app/placa.png"
    
    # ====================================================================
    # PLANTILLA 1: El enfoque "Clásico" (El que ya teníamos)
    # ====================================================================
    asunto_1 = f"Placa de reseñas en Google Maps de {local_name}"
    cuerpo_1 = f"""
    <html>
      <body style="font-family: Arial, sans-serif; color: #333; line-height: 1.5;">
        <p>Hola equipo de {local_name},</p>
        <p>He estado viendo vuestro perfil de Google Maps. Tenéis {reviews_text} reseñas y una nota de {rating_text} estrellas.</p>
        <p>Sé que muchos clientes satisfechos no os dejan reseña simplemente por la pereza de tener que buscar el local en el móvil en ese momento.</p>
        <p>Hemos creado unas placas físicas con tecnología NFC. Se colocan en el mostrador y, cuando el cliente acerca su móvil, se le abre automáticamente vuestro perfil de Google para que deje las 5 estrellas en 2 segundos.</p>
        <p>Te la dejo configurada y funcionando en el mostrador por veinticinco euros. Nada de cuotas mensuales ni mantenimientos.</p>
        <p>Si os interesa, me decís, la dejo configurada exactamente con vuestro enlace, vosotros no tenéis que configurar nada y me paso por el local para entregárosla funcionando.</p>
        <p>¿Os preparo una unidad?</p>
        <p>Muchas Gracias.</p>
        <p><strong>Guillermo</strong></p>
        <p style="text-align: center;"><img src="{url_imagen}" alt="Placa NFC" style="max-width: 250px; border-radius: 8px;"></p>
      </body>
    </html>
    """

    # ====================================================================
    # PLANTILLA 2: El enfoque "Directo y de Mejora"
    # ====================================================================
    asunto_2 = f"Mejorar las {reviews_text} reseñas de {local_name}"
    cuerpo_2 = f"""
    <html>
      <body style="font-family: Helvetica, sans-serif; color: #2c3e50; line-height: 1.6;">
        <p>Hola {local_name},</p>
        <p>Estaba revisando vuestra ficha en Google Maps y veo que contáis con un {rating_text} de valoración media.</p>
        <p>El problema habitual en los negocios locales es que el cliente contento se olvida de puntuar porque le da pereza buscar el nombre en su teléfono.</p>
        <p>Para solucionar esto, estamos instalando unos soportes físicos NFC. Van directamente en la caja o el mostrador: el cliente solo tiene que acercar su móvil y la pantalla de las 5 estrellas se le abre sola al instante.</p>
        <p>El importe es de veinticinco euros por dejarla operativa en vuestro local. Cero mantenimientos y ningún coste oculto posterior.</p>
        <p>Yo me encargo de programarla con vuestro link de Google y os la llevo lista para usar, no hace falta que toquéis nada técnico.</p>
        <p>¿Queréis que os acerque una esta semana?</p>
        <p>Un saludo,</p>
        <p><strong>Guillermo</strong></p>
        <p style="text-align: center;"><img src="{url_imagen}" alt="Soporte Reseñas" style="max-width: 250px; border-radius: 8px;"></p>
      </body>
    </html>
    """

    # ====================================================================
    # PLANTILLA 3: El enfoque "Consultivo"
    # ====================================================================
    asunto_3 = f"Sugerencia para el perfil de Google de {local_name}"
    cuerpo_3 = f"""
    <html>
      <body style="font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; color: #1a1a1a; line-height: 1.5;">
        <p>Buenas equipo de {local_name},</p>
        <p>Me he cruzado con vuestro negocio en Maps. Tenéis muy buena base con las {reviews_text} reseñas que ya habéis conseguido.</p>
        <p>La mayoría de clientes que se van contentos no dejan valoración por la fricción de tener que teclear el nombre del local en Google.</p>
        <p>Nosotros montamos unos pequeños expositores NFC. El funcionamiento es simple: el cliente pasa su teléfono por encima y aterriza directamente en vuestro formulario de reseñas.</p>
        <p>Entregaros la unidad ya programada y funcionando cuesta veinticinco euros, en un abono único y sin ninguna cuota de suscripción.</p>
        <p>Si os encaja la idea, la vinculo a vuestra cuenta y os la acerco al local para que podáis usarla desde el primer minuto.</p>
        <p>¿Os dejo preparada una?</p>
        <p>Gracias,</p>
        <p><strong>Guillermo</strong></p>
        <p style="text-align: center;"><img src="{url_imagen}" alt="Dispositivo NFC" style="max-width: 250px; border-radius: 8px;"></p>
      </body>
    </html>
    """

    # Empaquetamos las opciones
    opciones = [
        (asunto_1, cuerpo_1),
        (asunto_2, cuerpo_2),
        (asunto_3, cuerpo_3)
    ]
    
    # El motor selecciona una al azar de forma matemática
    import random
    asunto_elegido, cuerpo_elegido = random.choice(opciones)
    
    return asunto_elegido, cuerpo_elegido   


def send_email(to_email, subject, body_html):
    msg = MIMEMultipart('alternative')
    msg['From'] = f"Guillermo <{SMTP_USER}>"
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body_html, 'html'))
    
    try:
        server = smtplib.SMTP(SMTP_HOST, SMTP_PORT)
        server.starttls()
        server.login(SMTP_USER, SMTP_PASS)
        server.send_message(msg)
        server.quit()
        return True
    except Exception as e:
        print(f"[-] Fallo SMTP con {to_email}: {str(e)}")
        return False

def main():
    print(f"[*] Solicitando a Supabase {LIMITE_DIARIO} leads pendientes...")
    
    # 1. Obtener leads donde enviado es false, limitando al máximo diario
    response = supabase.table('leads').select('*').eq('enviado', False).limit(LIMITE_DIARIO).execute()
    leads_pendientes = response.data
    
    if not leads_pendientes:
        print("[!] No hay leads nuevos en la base de datos para enviar. Ejecuta el Scraper primero.")
        return

    print(f"[+] Se van a procesar {len(leads_pendientes)} correos. Comenzando campaña de envío...")
    
    # 2. Bucle de envío con emulación humana
    for index, lead in enumerate(leads_pendientes):
        email = lead['email']
        nombre = lead['nombre']
        
        print(f"\n[{index + 1}/{len(leads_pendientes)}] Enviando a: {nombre} ({email})...")
        
        asunto, cuerpo = generate_copy(nombre, lead.get('rating'), lead.get('reviews'))
        enviado_ok = send_email(email, asunto, cuerpo)
        
        if enviado_ok:
            # 3. Marcar como enviado en Supabase de forma irreversible
            supabase.table('leads').update({'enviado': True}).eq('id', lead['id']).execute()
            print("[+] Marcado como ENVIADO en la base de datos.")
            
            # Si no es el último correo, calcula y ejecuta el tiempo de espera aleatorio
            if index < len(leads_pendientes) - 1:
                espera = random.randint(ESPERA_MINIMA, ESPERA_MAXIMA)
                minutos = round(espera / 60, 2)
                print(f"[*] Pausa de emulación humana: Esperando {minutos} minutos hasta el próximo correo...")
                time.sleep(espera)

if __name__ == '__main__':
    main()
