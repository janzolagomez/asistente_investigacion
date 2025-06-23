import streamlit as st
import pandas as pd
# Las siguientes líneas se eliminan si ya no se usa docx
# from io import BytesIO
# from docx import Document

# Configuración de la página
st.set_page_config(page_title="Asistente para Matriz de Investigación", layout="wide")

# ==============================================================================
# INICIALIZACIÓN DEL ESTADO DE SESIÓN
# ==============================================================================
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

# ==============================================================================
# DEFINICIÓN DE PASOS Y SUS PREGUNTAS/EJEMPLOS (Nuevos nombres y ejemplos)
# ==============================================================================
steps = [
    {
        'name': "Tipo de Investigación",
        'question': "¡Hola! Vamos a crear tu matriz de investigación. ¿Qué tipo de investigación realizarás?",
        'examples': "", # No aplica ejemplo en radio button
        'input_type': 'radio',
        'options': ['Cualitativa', 'Cuantitativa'],
        'key': 'tipo_investigacion'
    },
    {
        'name': "Tema de Investigación",
        'question': "¿Cuál es el tema de tu investigación? Describe brevemente el fenómeno y el contexto.",
        'examples': "**Ejemplo:** Impacto del uso de redes sociales en el rendimiento académico de estudiantes universitarios de primer año en la Facultad de Comunicación de la Universidad X durante el ciclo 2024-II.",
        'input_type': 'text_area',
        'key': 'tema'
    },
    {
        'name': "Pregunta de Investigación",
        'question': "¿Cuál es tu pregunta de investigación? Asegúrate de que sea clara, específica y esté alineada con tu tema.",
        'examples': "**Ejemplo:** ¿De qué manera el uso de redes sociales influye en el rendimiento académico de los estudiantes universitarios de primer año de la Facultad de Comunicación de la Universidad X durante el ciclo 2024-II?",
        'input_type': 'text_area',
        'key': 'pregunta'
    },
    {
        'name': "Objetivo General",
        'question': "Ahora escribe tu objetivo general. ¿Qué meta principal quieres lograr con tu investigación? Inicia con un verbo en infinitivo (analizar, determinar, describir, etc.).",
        'examples': "**Ejemplo:** Determinar la influencia del uso de redes sociales en el rendimiento académico de los estudiantes universitarios de primer año de la Facultad de Comunicación de la Universidad X durante el ciclo 2024-II.",
        'input_type': 'text_area',
        'key': 'objetivo_general'
    },
    {
        'name': "Objetivos Específicos",
        'question': "Escribe hasta 3 objetivos específicos. Estos deben detallar los pasos para alcanzar tu objetivo general. Inicia cada uno con un verbo en infinitivo. Ingresa uno por línea.",
        'examples': """**Ejemplo:**
- Identificar el tiempo promedio que los estudiantes de primer año dedican al uso de redes sociales diariamente.
- Establecer la relación entre el tiempo de uso de redes sociales y las calificaciones obtenidas por los estudiantes.
- Describir las percepciones de los estudiantes sobre el impacto de las redes sociales en su concentración y estudio.""",
        'input_type': 'text_area',
        'key': 'objetivos_especificos',
        'special': 'list'
    },
]

# Pasos adicionales para investigación Cuantitativa
quantitative_steps = [
    {
        'name': "Variable Independiente",
        'question': "Define tu variable independiente (la causa o el factor que se manipula o se presume que influye en otra variable).",
        'examples': "**Ejemplo:** Uso de redes sociales (medida en horas/día).",
        'input_type': 'text_input',
        'key': 'variables.independiente'
    },
    {
        'name': "Variable Dependiente",
        'question': "Define tu variable dependiente (el efecto o el resultado que se mide y se presume que es influenciado por la variable independiente).",
        'examples': "**Ejemplo:** Rendimiento académico (medido por el promedio de calificaciones).",
        'input_type': 'text_input',
        'key': 'variables.dependiente'
    },
    {
        'name': "Hipótesis Nula (H₀)",
        'question': "Escribe tu hipótesis nula (H₀). Esta es una afirmación de no efecto o no relación. Se asume verdadera hasta que la evidencia demuestre lo contrario.",
        'examples': "**Ejemplo:** No existe influencia significativa del uso de redes sociales en el rendimiento académico de los estudiantes universitarios de primer año de la Facultad de Comunicación de la Universidad X durante el ciclo 2024-II.",
        'input_type': 'text_area',
        'key': 'hipotesis.nula'
    },
    {
        'name': "Hipótesis Alternativa (H₁)",
        'question': "Escribe tu hipótesis alternativa (H₁). Esta es la afirmación que el investigador busca establecer, la que contradice la hipótesis nula.",
        'examples': "**Ejemplo:** Existe una influencia significativa del uso de redes sociales en el rendimiento académico de los estudiantes universitarios de primer año de la Facultad de Comunicación de la Universidad X durante el ciclo 2024-II.",
        'input_type': 'text_area',
        'key': 'hipotesis.alternativa'
    },
]

# Pasos finales (comunes para ambos tipos de investigación)
final_steps = [
    {
        'name': "Justificación",
        'question': "¿Por qué es importante tu investigación? Explica su relevancia académica, social o práctica, y a quién beneficiará.",
        'examples': """**Ejemplo:** Esta investigación es relevante socialmente al abordar cómo una herramienta de uso masivo como las redes sociales impacta en un aspecto fundamental como el rendimiento académico, beneficiando a estudiantes, docentes e instituciones educativas al proporcionar información para estrategias de estudio y bienestar. Académicamente, contribuye al campo de la pedagogía y la comunicación digital.""",
        'input_type': 'text_area',
        'key': 'justificacion'
    },
    {
        'name': "Marco Teórico",
        'question': "Para el marco teórico, ingresa un concepto o variable clave y sus autores principales (formato: Concepto - Autores). Ingresa uno por línea.",
        'examples': """**Ejemplo:**
- Redes sociales - Boyd & Ellison (2007)
- Rendimiento académico - Román y Murillo (2011)
- Distracción digital - Greenfield (2009)""",
        'input_type': 'text_area',
        'key': 'marco_teorico',
        'special': 'marco_teorico'
    },
    {
        'name': "Población",
        'question': "Describe la población de tu estudio (¿quiénes son el grupo completo de personas o elementos con características comunes que son objeto de tu investigación?).",
        'examples': "**Ejemplo:** Todos los estudiantes de primer año de la Facultad de Comunicación de la Universidad X inscritos en el ciclo 2024-II, que suman aproximadamente 500 estudiantes.",
        'input_type': 'text_area',
        'key': 'metodologia.poblacion'
    },
    {
        'name': "Muestra",
        'question': "Describe la muestra de tu estudio (¿cómo seleccionarás a los participantes de la población y cuántos serán?).",
        'examples': "**Ejemplo:** 100 estudiantes seleccionados aleatoriamente de la población total, asegurando representatividad por sexo y programa de estudios. Se utilizará un muestreo aleatorio simple.",
        'input_type': 'text_area',
        'key': 'metodologia.muestra'
    },
    {
        'name': "Técnicas de Recolección de Datos",
        'question': "¿Qué técnicas e instrumentos usarás para recolectar datos? (Ej. encuestas con cuestionarios, entrevistas a profundidad, observación, análisis documental).",
        'examples': """**Ejemplo:**
- Encuesta mediante cuestionario (para recabar datos sobre el uso de redes sociales y rendimiento percibido).
- Análisis documental de registros académicos (para obtener calificaciones objetivas).""",
        'input_type': 'text_area',
        'key': 'metodologia.tecnicas'
    },
]

# ==============================================================================
# FUNCIÓN PRINCIPAL DE LA APLICACIÓN STREAMLIT
# ==============================================================================
def main():
    st.title("Asistente para Matriz de Investigación")
    st.write("Completa cada sección para construir tu matriz de consistencia.")

    # ==========================================================================
    # DETERMINACIÓN DINÁMICA DE LOS PASOS COMPLETOS
    # ==========================================================================
    tipo_investigacion = st.session_state.matrix_data.get('tipo_investigacion', '')
    if tipo_investigacion == 'Cuantitativa':
        all_steps = steps + quantitative_steps + final_steps
    else:
        all_steps = steps + final_steps

    # ==========================================================================
    # BARRA LATERAL DE PROGRESO (Ahora con los nombres de los pasos)
    # ==========================================================================
    st.sidebar.header("Progreso de la Matriz")
    for i, step_info in enumerate(all_steps):
        icon = "⬜" if i > st.session_state.step else "✅" if i < st.session_state.step else "🟨"
        st.sidebar.markdown(f"{icon} {step_info['name']}")

    # ==========================================================================
    # LÓGICA DE VISUALIZACIÓN DEL PASO ACTUAL
    # ==========================================================================
    if st.session_state.step < len(all_steps):
        current_step = all_steps[st.session_state.step]
        st.subheader(f"Sección: {current_step['name']}") # Mostrar el nombre del paso

        st.markdown(current_step['question']) # Pregunta
        if current_step['examples']:
            with st.expander("Ver ejemplo"): # Expander para los ejemplos
                st.markdown(current_step['examples'])

        # Manejar diferentes tipos de entrada
        response = None # Inicializar response para asegurar que siempre tenga un valor

        if current_step['input_type'] == 'radio':
            current_radio_value = st.session_state.matrix_data.get(current_step['key'], current_step['options'][0] if current_step['options'] else '')
            response = st.radio("Selecciona una opción:", current_step['options'], index=current_step['options'].index(current_radio_value) if current_radio_value in current_step['options'] else 0, key=f"input_{st.session_state.step}")
            st.session_state.matrix_data[current_step['key']] = response

        elif current_step['input_type'] == 'text_input':
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
            
            response = st.text_area("Tu respuesta:", value=current_value_area, key=f"input_{st.session_state.step}", height=150) # Aumentado la altura

            if current_step.get('special') == 'list':
                lines = [line.strip() for line in response.split('\n') if line.strip()]
                st.session_state.matrix_data[current_step['key']] = lines[:3]
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

        # ==========================================================================
        # BOTONES DE NAVEGACIÓN
        # ==========================================================================
        col1, col2 = st.columns(2)
        with col1:
            if st.session_state.step > 0:
                if st.button("⬅️ Regresar"):
                    st.session_state.step -= 1
                    st.rerun()
        with col2:
            current_data_value = None
            keys = current_step['key'].split('.')
            if len(keys) == 2:
                current_data_value = st.session_state.matrix_data[keys[0]].get(keys[1])
            else:
                current_data_value = st.session_state.matrix_data.get(current_step['key'])

            is_completed = False
            if current_step.get('special') in ['list', 'marco_teorico']:
                is_completed = bool(current_data_value) and len(current_data_value) > 0
            else:
                is_completed = bool(current_data_value is not None and str(current_data_value).strip() != '')

            if st.button("Avanzar ➡️"):
                if is_completed or current_step['input_type'] == 'radio': # Radio buttons siempre permiten avanzar si hay una opción por defecto/seleccionada
                    st.session_state.step += 1
                    st.rerun()
                else:
                    st.warning("Por favor, completa el campo antes de avanzar.")

    # ==========================================================================
    # PASO FINAL: REVISIÓN DE LA MATRIZ
    # ==========================================================================
    else:
        st.subheader("¡Matriz Completa!")
        st.write("Aquí tienes un resumen de tu matriz de investigación. Puedes revisarla y empezar una nueva si lo deseas.")
        data = st.session_state.matrix_data
        
        st.markdown("---")
        st.markdown(f"**Tipo de Investigación:** {data['tipo_investigacion'] or 'No definido'}")
        st.markdown(f"**Tema:** {data['tema'] or 'No definido'}")
        st.markdown(f"**Pregunta:** {data['pregunta'] or 'No definido'}")
        st.markdown(f"**Objetivo General:** {data['objetivo_general'] or 'No definido'}")
        st.markdown("**Objetivos Específicos:**")
        if data['objetivos_especificos']:
            for oe in data['objetivos_especificos']:
                if oe: st.markdown(f"- {oe}")
        else: st.markdown("No definido")
        
        if data['tipo_investigacion'] == 'Cuantitativa':
            st.markdown(f"**Variable Independiente:** {data['variables']['independiente'] or 'No definido'}")
            st.markdown(f"**Variable Dependiente:** {data['variables']['dependiente'] or 'No definido'}")
            st.markdown(f"**Hipótesis Nula (H₀):** {data['hipotesis']['nula'] or 'No definido'}")
            st.markdown(f"**Hipótesis Alternativa (H₁):** {data['hipotesis']['alternativa'] or 'No definido'}")
        
        st.markdown(f"**Justificación:** {data['justificacion'] or 'No definido'}")
        st.markdown("**Marco Teórico:**")
        if data['marco_teorico']:
            for entry in data['marco_teorico']:
                st.markdown(f"- **{entry['concepto']}**: {entry['autores']}")
        else: st.markdown("No definido")
        
        st.markdown("**Metodología:**")
        st.markdown(f"- **Población:** {data['metodologia']['poblacion'] or 'No definido'}")
        st.markdown(f"- **Muestra:** {data['metodologia']['muestra'] or 'No definido'}")
        st.markdown(f"- **Técnicas de Recolección de Datos:** {data['metodologia']['tecnicas'] or 'No definido'}")
        st.markdown("---")


        # Botón para reiniciar
        if st.button("🔄 Empezar una nueva matriz"):
            st.session_state.step = 0
            st.session_state.matrix_data = { # Reiniciar completamente los datos
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

# ==============================================================================
# PUNTO DE ENTRADA DE LA APLICACIÓN
# ==============================================================================
if __name__ == "__main__":
    main()
