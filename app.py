import streamlit as st
import pandas as pd
# from io import BytesIO  # Ya no es necesario si no generamos docx
# from docx import Document # Ya no es necesario si no generamos docx

# Configuración de la página
st.set_page_config(page_title="Asistente para Matriz de Investigación", layout="wide")

# Inicialización del estado de sesión
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

# La función generate_word_document se ha eliminado
# Ya no es necesario importar docx ni BytesIO

# Chatbot: Lista de pasos y preguntas
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

# Ajustar pasos según tipo de investigación
# Esta lógica debe estar DENTRO de main o re-evaluarse después del primer input de tipo_investigacion
# Para que all_steps se actualice correctamente cuando el usuario elija "Cuantitativa" o "Cualitativa"
# La forma en que está ahora, solo se evalúa una vez al inicio.

# Solución propuesta para la actualización dinámica de `all_steps`:
# Mover la determinación de `all_steps` dentro de la función `main`
# y recalcularla cada vez que 'tipo_investigacion' cambie.

# Función principal
def main():
    st.title("Asistente Chatbot para Matriz de Investigación")
    st.write("Soy tu asistente para crear una matriz de consistencia. Responde cada pregunta y al final podrás ver tu matriz.")

    # Determinar all_steps dinámicamente dentro de main
    tipo_investigacion = st.session_state.matrix_data.get('tipo_investigacion', '')
    if tipo_investigacion == 'Cuantitativa':
        current_all_steps = steps + quantitative_steps + final_steps
    else:
        current_all_steps = steps + final_steps


    # Mostrar progreso
    st.sidebar.header("Progreso")
    for i, step in enumerate(current_all_steps): # Usar current_all_steps
        icon = "⬜" if i > st.session_state.step else "✅" if i < st.session_state.step else "🟨"
        st.sidebar.markdown(f"{icon} Paso {i+1}")

    # Mostrar paso actual
    if st.session_state.step < len(current_all_steps): # Usar current_all_steps
        current_step = current_all_steps[st.session_state.step] # Usar current_all_steps
        st.markdown(f"**Chatbot:** {current_step['question']}")

        # Manejar diferentes tipos de entrada
        if current_step['input_type'] == 'radio':
            response = st.radio("Selecciona una opción:", current_step['options'], key=f"input_{st.session_state.step}")
            # Solo actualizamos el estado si la respuesta ha cambiado, para evitar re-runs innecesarios
            if st.session_state.matrix_data[current_step['key']] != response:
                st.session_state.matrix_data[current_step['key']] = response
                # Si el tipo de investigación cambia, ajustamos el paso para evitar saltos.
                # Esto es crucial para la lógica de los pasos dinámicos.
                if current_step['key'] == 'tipo_investigacion':
                    # Si el tipo de investigación cambia, podría ser necesario resetear o ajustar el paso
                    # para que el usuario no se quede en un paso que ya no existe en la nueva secuencia.
                    # Para simplificar, si cambian de Cualitativa a Cuantitativa o viceversa,
                    # se les pedirá que avancen o retrocedan para ver los nuevos pasos.
                    st.warning("Tipo de investigación cambiado. Por favor, revisa tus pasos.")
                    # No reseteamos st.session_state.step a 0 automáticamente,
                    # para que el usuario pueda navegar desde donde estaba.
                    # El `st.rerun()` manejará la re-renderización con los nuevos pasos.

        elif current_step['input_type'] == 'text_input':
            response = st.text_input("Tu respuesta:", value=st.session_state.matrix_data.get(current_step['key'], '') if '.' not in current_step['key'] else st.session_state.matrix_data.get(current_step['key'].split('.')[0], {}).get(current_step['key'].split('.')[1], ''), key=f"input_{st.session_state.step}")
            keys = current_step['key'].split('.')
            if len(keys) == 2:
                st.session_state.matrix_data[keys[0]][keys[1]] = response
            else:
                st.session_state.matrix_data[current_step['key']] = response
        elif current_step['input_type'] == 'text_area':
            current_value = ""
            if current_step.get('special') == 'list':
                current_value = "\n".join(st.session_state.matrix_data[current_step['key']])
            elif current_step.get('special') == 'marco_teorico':
                current_value = "\n".join([f"{entry['concepto']} - {entry['autores']}" for entry in st.session_state.matrix_data[current_step['key']]])
            else:
                keys = current_step['key'].split('.')
                if len(keys) == 2:
                    current_value = st.session_state.matrix_data[keys[0]][keys[1]]
                else:
                    current_value = st.session_state.matrix_data[current_step['key']]

            response = st.text_area("Tu respuesta:", value=current_value, key=f"input_{st.session_state.step}", height=100)

            if current_step.get('special') == 'list':
                # Convertir entrada en lista
                lines = [line.strip() for line in response.split('\n') if line.strip()]
                st.session_state.matrix_data[current_step['key']] = lines[:3]  # Limitar a 3
            elif current_step.get('special') == 'marco_teorico':
                # Convertir entrada en lista de diccionarios
                lines = [line.strip() for line in response.split('\n') if line.strip()]
                marco_teorico = []
                for line in lines:
                    parts = line.split(' - ')
                    if len(parts) >= 2:  # Manejar casos con múltiples guiones
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
            # Aquí, la condición para avanzar debería ser si el *valor actual en session_state* no está vacío.
            # Los componentes de Streamlit actualizan session_state al instante para inputs como radio.
            # Para text_input y text_area, el valor se actualiza cuando el usuario escribe.
            # El botón "Avanzar" solo debe forzar el rerun si el campo tiene datos.
            value_to_check = None
            if current_step['input_type'] == 'radio':
                value_to_check = st.session_state.matrix_data[current_step['key']]
            elif current_step['input_type'] in ['text_input', 'text_area']:
                keys = current_step['key'].split('.')
                if len(keys) == 2:
                    value_to_check = st.session_state.matrix_data[keys[0]][keys[1]]
                else:
                    value_to_check = st.session_state.matrix_data[current_step['key']]

            if st.button("Avanzar ➡️"):
                # Para campos de texto/área, `response` ya contiene el valor actual del widget.
                # Para radio, `response` también lo contiene.
                # Asegúrate de que `response` realmente representa lo que el usuario ha introducido
                # antes de permitir avanzar.
                if response or (current_step['input_type'] == 'radio' and value_to_check): # Asegurar que radio siempre permite avanzar si algo está seleccionado
                    st.session_state.step += 1
                    st.rerun()
                else:
                    st.warning("Por favor, completa el campo antes de avanzar.")

    # Paso final: Revisión (sin descarga de Word)
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

        # Se eliminó el botón de descarga del documento Word.
        # Se eliminó el bloque try-except para generate_word_document.

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
