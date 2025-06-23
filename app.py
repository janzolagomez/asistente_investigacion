import streamlit as st
import pandas as pd
# Las siguientes líneas se comentan/eliminan si ya no se usa docx
# from io import BytesIO
# from docx import Document

# Configuración de la página
st.set_page_config(page_title="Asistente para Matriz de Investigación", layout="wide")

# Inicialización del estado de sesión
# ESTE BLOQUE DE INICIALIZACIÓN DEBE ESTAR AL PRINCIPIO DEL SCRIPT
# PARA GARANTIZAR QUE st.session_state.matrix_data EXISTE SIEMPRE.
if 'step' not in st.session_state:
    st.session_state.step = 0
if 'matrix_data' not in st.session_state:
    st.session_state.matrix_data = {
        'tipo_investigacion': '',
        'tema': '',
        'pregunta': '',
        'objetivo_general': '',
        'objetivos_especificos': ['', '', ''],
        'justificacion': '',
        'marco_teorico': [],
        'metodologia': {
            'poblacion': '',
            'muestra': '',
            'tecnicas': ''
        },
        'variables': {'independiente': '', 'dependiente': ''},
        'hipotesis': {'nula': '', 'alternativa': ''}
    }

# La función generate_word_document y las importaciones de docx/BytesIO se asumen eliminadas
# si no quieres la funcionalidad de descarga de Word.

# Chatbot: Lista de pasos y preguntas (ESTAS LISTAS PUEDEN ESTAR FUERA DE MAIN)
steps = [
    {
        'question': "¡Hola! Vamos a crear tu matriz de investigación. ¿Qué tipo de investigación realizarás?",
        'input_type': 'radio',
        'options': ['Cualitativa', 'Cuantitativa'],
        'key': 'tipo_investigacion'
    },
    {
        'question': "Perfecto. Ahora, ¿cuál es el tema de tu investigación? Describe brevemente el fenómeno y el contexto.",
        'input_type': 'text_area',
        'key': 'tema'
    },
    {
        'question': "¿Cuál es tu pregunta de investigación? Asegúrate de que sea clara y esté alineada con tu tema.",
        'input_type': 'text_area',
        'key': 'pregunta'
    },
    {
        'question': "Ahora escribe tu objetivo general. ¿Qué quieres lograr con tu investigación?",
        'input_type': 'text_area',
        'key': 'objetivo_general'
    },
    {
        'question': "Escribe hasta 3 objetivos específicos. Estos deben detallar cómo alcanzarás tu objetivo general. Ingresa uno por línea.",
        'input_type': 'text_area',
        'key': 'objetivos_especificos',
        'special': 'list'
    },
]

# Pasos adicionales para cuantitativa
quantitative_steps = [
    {
        'question': "Define tu variable independiente (la causa).",
        'input_type': 'text_input',
        'key': 'variables.independiente'
    },
    {
        'question': "Define tu variable dependiente (el efecto).",
        'input_type': 'text_input',
        'key': 'variables.dependiente'
    },
    {
        'question': "Escribe tu hipótesis nula (H₀).",
        'input_type': 'text_area',
        'key': 'hipotesis.nula'
    },
    {
        'question': "Escribe tu hipótesis alternativa (H₁).",
        'input_type': 'text_area',
        'key': 'hipotesis.alternativa'
    },
]

# Pasos finales (comunes)
final_steps = [
    {
        'question': "¿Por qué es importante tu investigación? Escribe la justificación.",
        'input_type': 'text_area',
        'key': 'justificacion'
    },
    {
        'question': "Para el marco teórico, ingresa un concepto o variable clave y sus autores (formato: Concepto - Autores). Ingresa uno por línea.",
        'input_type': 'text_area',
        'key': 'marco_teorico',
        'special': 'marco_teorico'
    },
    {
        'question': "Describe la población de tu estudio (¿quiénes son los participantes?).",
        'input_type': 'text_area',
        'key': 'metodologia.poblacion'
    },
    {
        'question': "Describe la muestra (¿cómo seleccionarás a los participantes?).",
        'input_type': 'text_area',
        'key': 'metodologia.muestra'
    },
    {
        'question': "¿Qué técnicas usarás para recolectar datos? (Ej. entrevistas, encuestas, observación).",
        'input_type': 'text_area',
        'key': 'metodologia.tecnicas'
    },
]

# Función principal
def main():
    st.title("Asistente Chatbot para Matriz de Investigación")
    st.write("Soy tu asistente para crear una matriz de consistencia. Responde cada pregunta y al final podrás ver tu matriz.")

    # Mover la determinación de all_steps AQUÍ, DESPUÉS DE LA INICIALIZACIÓN DE SESSION_STATE
    tipo_investigacion = st.session_state.matrix_data.get('tipo_investigacion', '')
    if tipo_investigacion == 'Cuantitativa':
        all_steps = steps + quantitative_steps + final_steps
    else:
        all_steps = steps + final_steps

    # Mostrar progreso
    st.sidebar.header("Progreso")
    for i, step in enumerate(all_steps):
        icon = "⬜" if i > st.session_state.step else "✅" if i < st.session_state.step else "🟨"
        st.sidebar.markdown(f"{icon} Paso {i+1}")

    # Mostrar paso actual
    if st.session_state.step < len(all_steps):
        current_step = all_steps[st.session_state.step]
        st.markdown(f"**Chatbot:** {current_step['question']}")

        # Manejar diferentes tipos de entrada
        if current_step['input_type'] == 'radio':
            # Obtener el valor actual de session_state para el radio
            current_radio_value = st.session_state.matrix_data.get(current_step['key'], current_step['options'][0] if current_step['options'] else '')
            response = st.radio("Selecciona una opción:", current_step['options'], index=current_step['options'].index(current_radio_value) if current_radio_value in current_step['options'] else 0, key=f"input_{st.session_state.step}")
            st.session_state.matrix_data[current_step['key']] = response
            # Si el tipo de investigación cambia, puede que quieras hacer algo especial,
            # pero el st.rerun() ya manejará que la lista de pasos se recalcule correctamente.

        elif current_step['input_type'] == 'text_input':
            # Recuperar el valor existente para precargar el input
            current_value_input = ''
            keys = current_step['key'].split('.')
            if len(keys) == 2:
                current_value_input = st.session_state.matrix_data[keys[0]].get(keys[1], '')
            else:
                current_value_input = st.session_state.matrix_data.get(current_step['key'], '')

            response = st.text_input("Tu respuesta:", value=current_value_input, key=f"input_{st.session_state.step}")
            
            if len(keys) == 2:
                st.session_state.matrix_data[keys[0]][keys[1]] = response
            else:
                st.session_state.matrix_data[current_step['key']] = response

        elif current_step['input_type'] == 'text_area':
            # Recuperar el valor existente para precargar el text_area
            current_value_area = ""
            if current_step.get('special') == 'list':
                current_value_area = "\n".join(st.session_state.matrix_data[current_step['key']])
            elif current_step.get('special') == 'marco_teorico':
                current_value_area = "\n".join([f"{entry['concepto']} - {entry['autores']}" for entry in st.session_state.matrix_data[current_step['key']]])
            else:
                keys = current_step['key'].split('.')
                if len(keys) == 2:
                    current_value_area = st.session_state.matrix_data[keys[0]].get(keys[1], '')
                else:
                    current_value_area = st.session_state.matrix_data.get(current_step['key'], '')

            response = st.text_area("Tu respuesta:", value=current_value_area, key=f"input_{st.session_state.step}", height=100)

            if current_step.get('special') == 'list':
                lines = [line.strip() for line in response.split('\n') if line.strip()]
                st.session_state.matrix_data[current_step['key']] = lines[:3]  # Limitar a 3
            elif current_step.get('special') == 'marco_teorico':
                lines = [line.strip() for line in response.split('\n') if line.strip()]
                marco_teorico = []
                for line in lines:
                    parts = line.split(' - ')
                    if len(parts) >= 2:
                        marco_teorico.append({'concepto': parts[0], 'autores': ' - '.join(parts[1:])})
                st.session_state.matrix_data[current_step['key']] = marco_teorico
            else:
                keys = current_step['key'].split('.')
                if len(keys) == 2:
                    st.session_state.matrix_data[keys[0]][keys[1]] = response
                else:
                    st.session_state.matrix_data[current_step['key']] = response

        # Botones de navegación
        col1, col2 = st.columns(2)
        with col1:
            if st.session_state.step > 0:
                if st.button("⬅️ Regresar"):
                    st.session_state.step -= 1
                    st.rerun()
        with col2:
            # Obtener el valor actual del estado de sesión para validar
            current_data_value = None
            keys = current_step['key'].split('.')
            if len(keys) == 2:
                current_data_value = st.session_state.matrix_data[keys[0]].get(keys[1])
            else:
                current_data_value = st.session_state.matrix_data.get(current_step['key'])

            # Para listas o marco teórico, verificar si hay elementos
            if current_step.get('special') in ['list', 'marco_teorico']:
                is_completed = bool(current_data_value) and len(current_data_value) > 0
            else:
                is_completed = bool(current_data_value and str(current_data_value).strip() != '') # Considerar vacío si solo hay espacios

            if st.button("Avanzar ➡️"):
                if is_completed:
                    st.session_state.step += 1
                    st.rerun()
                else:
                    st.warning("Por favor, completa el campo antes de avanzar.")

    # Paso final: Revisión
    else:
        st.markdown("**Chatbot:** ¡Hemos terminado! Aquí tienes un resumen de tu matriz.")
        data = st.session_state.matrix_data
        st.subheader("Resumen de tu Matriz")
        st.write(f"**Tipo de Investigación:** {data['tipo_investigacion'] or 'No definido'}")
        st.write(f"**Tema:** {data['tema'] or 'No definido'}")
        st.write(f"**Pregunta:** {data['pregunta'] or 'No definido'}")
        st.write(f"**Objetivo General:** {data['objetivo_general'] or 'No definido'}")
        st.write("**Objetivos Específicos:**")
        for oe in data['objetivos_especificos']:
            if oe:
                st.write(f"- {oe}")
        if data['tipo_investigacion'] == 'Cuantitativa':
            st.write(f"**Variable Independiente:** {data['variables']['independiente'] or 'No definido'}")
            st.write(f"**Variable Dependiente:** {data['variables']['dependiente'] or 'No definido'}")
            st.write(f"**Hipótesis Nula (H₀):** {data['hipotesis']['nula'] or 'No definido'}")
            st.write(f"**Hipótesis Alternativa (H₁):** {data['hipotesis']['alternativa'] or 'No definido'}")
        st.write(f"**Justificación:** {data['justificacion'] or 'No definido'}")
        st.write("**Marco Teórico:**")
        if data['marco_teorico']:
            for entry in data['marco_teorico']:
                st.write(f"- {entry['concepto']}: {entry['autores']}")
        else:
            st.write("No definido")
        st.write("**Metodología:**")
        st.write(f"- Población: {data['metodologia']['poblacion'] or 'No definido'}")
        st.write(f"- Muestra: {data['metodologia']['muestra'] or 'No definido'}")
        st.write(f"- Técnicas: {data['metodologia']['tecnicas'] or 'No definido'}")

        # Botón para reiniciar
        if st.button("🔄 Empezar de nuevo"):
            st.session_state.step = 0
            st.session_state.matrix_data = {
                'tipo_investigacion': '',
                'tema': '',
                'pregunta': '',
                'objetivo_general': '',
                'objetivos_especificos': ['', '', ''],
                'justificacion': '',
                'marco_teorico': [],
                'metodologia': {
                    'poblacion': '',
                    'muestra': '',
                    'tecnicas': ''
                },
                'variables': {'independiente': '', 'dependiente': ''},
                'hipotesis': {'nula': '', 'alternativa': ''}
            }
            st.rerun()

if __name__ == "__main__":
    main()
