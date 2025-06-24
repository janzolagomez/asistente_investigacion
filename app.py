import streamlit as st
import pandas as pd
# Las siguientes líneas se eliminan si ya no se usa docx
# from io import BytesIO
# from docx import Document

# Configuración de la página
st.set_page_config(page_title="Asistente para Matriz de Investigación", layout="wide")

# ==============================================================================
# EXPLICACIONES DETALLADAS POR PASO Y TIPO DE INVESTIGACIÓN
# ==============================================================================
explanations = {
    'tipo_investigacion': "La investigación cualitativa busca comprender fenómenos desde la perspectiva de los participantes, mientras que la cuantitativa busca medir y probar hipótesis a través de datos numéricos y análisis estadístico. Elige el enfoque que mejor se adapte a tu pregunta y objetivos.",
    'tema': {
        'Cualitativa': "El tema en investigación cualitativa es una idea general que expresa el fenómeno, sujetos, actores y contexto que quieres estudiar, enfocado en la comprensión profunda. Debe ser amplio pero delimitado.",
        'Cuantitativa': "El tema en investigación cuantitativa debe ser específico, delimitado, e incluir al menos las variables principales y el contexto de estudio. Se enfoca en la medición y la relación entre variables."
    },
    'pregunta': {
        'Cualitativa': "La pregunta cualitativa es una pregunta amplia y abierta que expresa el fenómeno principal que se desea comprender desde la perspectiva de los participantes, sin buscar medir o cuantificar.",
        'Cuantitativa': "La pregunta cuantitativa es una formulación clara, específica y objetiva que plantea una relación, efecto, diferencia o nivel entre una o más variables medibles. Guía la recolección y el análisis estadístico de datos."
    },
    'objetivo_general': {
        'Cualitativa': "En la investigación cualitativa, el objetivo general busca orientar la exploración, comprensión, descripción o interpretación del fenómeno o experiencia en un grupo social o comunidad específica, de manera coherente con un enfoque interpretativo.",
        'Cuantitativa': "En la investigación cuantitativa, el objetivo general debe expresar claramente qué se quiere analizar, correlacionar, describir o explicar en términos de la relación, efecto o influencia entre las variables de estudio, en una población y contexto definidos."
    },
    'objetivos_especificos': {
        'Cualitativa': "Son metas concretas y delimitadas que el estudio busca alcanzar para lograr el objetivo general. En cualitativa, suelen enfocarse en acciones como identificar, analizar, describir, interpretar o caracterizar dimensiones, categorías o subprocesos del fenómeno en los participantes y contexto.",
        'Cuantitativa': "Son metas concretas y medibles que derivan del objetivo general, detallando los pasos para alcanzarlo. En cuantitativa, se enfocan en describir variables, comparar grupos, correlacionar variables o explicar relaciones específicas entre ellas, orientando la operacionalización y recolección de datos."
    },
    'variables.independiente': "Es la característica o propiedad observable y medible que se presume es la *causa* o el factor que influye en otra variable. El investigador la manipula o mide para observar su efecto.",
    'variables.dependiente': "Es la característica o propiedad observable y medible que se presume es el *efecto* o el resultado que cambia debido a la influencia de la variable independiente. Es lo que se observa o mide como respuesta.",
    'hipotesis.nula': "La hipótesis nula (H₀) es una afirmación que postula la ausencia de relación, diferencia o efecto entre variables. Se asume verdadera hasta que los datos demuestren lo contrario.",
    'hipotesis.alternativa': "La hipótesis alternativa (H₁) es la afirmación que el investigador busca establecer. Contradice la hipótesis nula, sugiriendo la existencia de una relación, efecto o diferencia significativa entre las variables.",
    'justificacion': "La justificación explica la *importancia* y el *porqué* de tu investigación. Debe argumentar su relevancia teórica (qué aporta al conocimiento), práctica (cómo resuelve un problema) y social (a quién beneficia o impacta positivamente).",
    'marco_teorico': {
        'Cualitativa': "El marco teórico en investigación cualitativa es una síntesis y selección de conceptos clave, modelos y teorías relevantes que fundamentan tu perspectiva del fenómeno. Sirve para construir tus categorías iniciales o 'lentes interpretativos' antes o durante la recolectión de datos.",
        'Cuantitativa': "El marco teórico en investigación cuantitativa es la conceptualización formal de tus variables, basada en la literatura científica existente. Define qué significa cada variable desde un punto de vista académico o técnico, usando autores y modelos reconocidos, y guía la operacionalización y medición."
    },
    'metodologia.poblacion': "La población es el *conjunto total* de todas las personas, objetos o elementos que poseen una o más características comunes y que son el universo de tu estudio. Es el grupo al cual deseas generalizar tus hallazgos.",
    'metodologia.muestra': "La muestra es un *subconjunto representativo* de la población, seleccionado para realizar el estudio. Se describe el tipo de muestreo (probabilístico/no probabilístico), el tamaño de la muestra y los criterios de selección utilizados para garantizar que sea adecuada y permita inferencias si es cuantitativa.",
    'metodologia.tecnicas': {
        'Cualitativa': "Las técnicas de recolección de datos cualitativas son los procedimientos y herramientas que te permiten obtener información detallada y profunda para comprender el fenómeno. Ejemplos incluyen entrevistas a profundidad, grupos focales, observación participante, o análisis documental.",
        'Cuantitativa': "Las técnicas de recolección de datos cuantitativas son los procedimientos y herramientas que te permiten obtener datos numéricos y estructurados para medir variables y probar hipótesis. Ejemplos incluyen encuestas con cuestionarios estandarizados, escalas de medición (Likert), o la recopilación de datos de registros existentes."
    }
}


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
        'objetivos_especificos': ['', '', ''], # Por defecto 3 objetivos
        'justificacion': '',
        'marco_teorico': [], # Almacena diccionarios {'concepto': '', 'autores': ''}
        'metodologia': {
            'poblacion': '',
            'muestra': '',
            'tecnicas': ''
        },
        # Estas claves se rellenarán solo si el tipo de investigación es Cuantitativa
        'variables': {'independiente': '', 'dependiente': ''},
        'hipotesis': {'nula': '', 'alternativa': ''}
    }

# ==============================================================================
# DEFINICIÓN DE PASOS Y SUS PREGUNTAS/EJEMPLOS
# ==============================================================================
# Pasos iniciales (comunes a ambos tipos de investigación para comenzar)
base_steps = [
    {
        'name': "Tipo de Investigación",
        'question': "¡Hola! Vamos a crear tu matriz de investigación. ¿Qué tipo de investigación realizarás?",
        'examples': {}, # No aplica ejemplo en radio button
        'input_type': 'radio',
        'options': ['Cualitativa', 'Cuantitativa'],
        'key': 'tipo_investigacion',
        'validation': lambda x: x != ''
    },
    {
        'name': "Tema de Investigación",
        'question': "¿Cuál es el tema de tu investigación? Describe brevemente el fenómeno y el contexto.",
        'examples': {
            'Cuantitativa': [
                "Impacto del uso de redes sociales en el rendimiento académico de estudiantes universitarios de primer año en la Facultad de Comunicación de la Universidad X durante el ciclo 2024-II.",
                "Relación entre el estrés académico y la calidad del sueño en estudiantes de medicina de una universidad española.",
                "Efecto de un programa de intervención nutricional en los niveles de glucosa en pacientes diabéticos tipo 2 en un centro de salud urbano."
            ],
            'Cualitativa': [
                "Percepciones docentes sobre la educación para el desarrollo sostenible implementadas en el cantón Portovelo, Ecuador.",
                "Experiencias de resiliencia en mujeres migrantes venezolanas en España durante el proceso de integración laboral.",
                "Significados atribuidos por jóvenes a la participación ciudadana en contextos urbanos desfavorecidos de Madrid."
            ]
        },
        'input_type': 'text_area',
        'key': 'tema',
        'validation': lambda x: len(x) > 20
    },
    {
        'name': "Pregunta de Investigación",
        'question': "¿Cuál es tu pregunta de investigación? Asegúrate de que sea clara, específica y esté alineada con tu tema.",
        'examples': {
            'Cuantitativa': [
                "¿De qué manera el uso de redes sociales influye en el rendimiento académico de los estudiantes universitarios de primer año de la Facultad de Comunicación de la Universidad X durante el ciclo 2024-II?",
                "¿Existe una correlación significativa entre el nivel de estrés académico y la calidad del sueño reportada por estudiantes de medicina?",
                "¿Cuál es el efecto de un programa de dieta baja en carbohidratos en la reducción de los niveles de glucosa en sangre en pacientes diabéticos tipo 2?"
            ],
            'Cualitativa': [
                "¿Qué percepciones tienen los docentes de educación básica respecto a las inserciones curriculares de la educación para el desarrollo sostenible en el cantón Portovelo?",
                "¿Cómo construyen la resiliencia las mujeres migrantes venezolanas al enfrentar los desafíos de la integración laboral en España?",
                "¿Cuáles son los significados que los jóvenes de barrios desfavorecidos de Madrid atribuyen a la participación ciudadana?"
            ]
        },
        'input_type': 'text_area',
        'key': 'pregunta',
        'validation': lambda x: len(x) > 20 and '?' in x
    },
    {
        'name': "Objetivo General",
        'question': "Ahora escribe tu objetivo general. ¿Qué meta principal quieres lograr con tu investigación? Inicia con un verbo en infinitivo (analizar, determinar, describir, etc.).",
        'examples': {
            'Cuantitativa': [
                "Determinar la influencia del uso de redes sociales en el rendimiento académico de los estudiantes universitarios de primer año de la Facultad de Comunicación de la Universidad X durante el ciclo 2024-II.",
                "Analizar la relación entre el estrés académico y la calidad del sueño en estudiantes de medicina de una universidad española.",
                "Evaluar el efecto de un programa de intervención nutricional en los niveles de glucosa en pacientes diabéticos tipo 2 en un centro de salud urbano."
            ],
            'Cualitativa': [
                "Comprender las percepciones de los docentes de educación básica sobre las inserciones curriculares para el desarrollo sostenible en Portovelo.",
                "Explorar las experiencias de resiliencia en mujeres migrantes venezolanas durante su integración laboral en España.",
                "Interpretar los significados atribuidos por jóvenes a la participación ciudadana en contextos urbanos desfavorecidos de Madrid."
            ]
        },
        'input_type': 'text_area',
        'key': 'objetivo_general',
        'validation': lambda x: len(x) > 20 and any(x.lower().startswith(v) for v in ['analizar', 'determinar', 'describir', 'comprender', 'explorar', 'interpretar'])
    },
    {
        'name': "Objetivos Específicos",
        'question': "Escribe hasta 3 objetivos específicos. Estos deben detallar los pasos para alcanzar tu objetivo general. Inicia cada uno con un verbo en infinitivo. Ingresa uno por línea.",
        'examples': {
            'Cuantitativa': [
                "Identificar el tiempo promedio que los estudiantes de primer año dedican al uso de redes sociales diariamente.",
                "Establecer la relación entre el tiempo de uso de redes sociales y las calificaciones obtenidas por los estudiantes.",
                "Describir las percepciones de los estudiantes sobre el impacto de las redes sociales en su concentración y estudio."
            ],
            'Cualitativa': [
                "Caracterizar las inserciones curriculares en desarrollo sostenible implementadas por los docentes.",
                "Analizar las estrategias pedagógicas empleadas por los docentes para integrar el desarrollo sostenible.",
                "Explorar los desafíos que enfrentan los docentes al implementar la educación para el desarrollo sostenible."
            ]
        },
        'input_type': 'text_area',
        'key': 'objetivos_especificos',
        'special': 'list_split', # Indica que el texto se debe dividir en una lista por líneas
        'validation': lambda x: len(x) > 0 and all(len(line.strip()) > 10 for line in x.split('\n') if line.strip())
    },
]

# Pasos adicionales para investigación Cuantitativa (se insertan si se selecciona 'Cuantitativa')
quantitative_specific_steps = [
    {
        'name': "Variable Independiente",
        'question': "Define tu variable independiente (la causa o el factor que se manipula o se presume que influye en otra variable).",
        'examples': {
            'Cuantitativa': [
                "Uso de redes sociales (medido en horas de conexión diaria).",
                "Horas de estudio semanales (medidas en autorreporte).",
                "Participación en programa de tutorías (variable categórica: sí/no)."
            ],
            'Cualitativa': [] # Vacío, ya que este paso es específico de cuantitativa
        },
        'input_type': 'text_input',
        'key': 'variables.independiente',
        'validation': lambda x: len(x) > 5
    },
    {
        'name': "Variable Dependiente",
        'question': "Define tu variable dependiente (el efecto o el resultado que se mide y se presume que es influenciado por la variable independiente).",
        'examples': {
            'Cuantitativa': [
                "Rendimiento académico (medido por el promedio de calificaciones finales).",
                "Nivel de ansiedad ante exámenes (medido con escala validada).",
                "Tasa de abandono universitario (variable dicotómica: abandono/continúa)."
            ],
            'Cualitativa': [] # Vacío, ya que este paso es específico de cuantitativa
        },
        'input_type': 'text_input',
        'key': 'variables.dependiente',
        'validation': lambda x: len(x) > 5
    },
    {
        'name': "Hipótesis Nula (H₀)",
        'question': "Escribe tu hipótesis nula (H₀). Esta es una afirmación de no efecto o no relación. Se asume verdadera hasta que la evidencia demuestre lo contrario.",
        'examples': {
            'Cuantitativa': [
                "No existe influencia significativa del uso de redes sociales en el rendimiento académico de los estudiantes universitarios de primer año de la Facultad de Comunicación de la Universidad X durante el ciclo 2024-II.",
                "No hay diferencias significativas en el nivel de ansiedad ante exámenes entre estudiantes que reciben tutorías y los que no.",
                "La edad del estudiante no se correlaciona significativamente con su tasa de abandono universitario."
            ],
            'Cualitativa': [] # Vacío, ya que este paso es específico de cuantitativa
        },
        'input_type': 'text_area',
        'key': 'hipotesis.nula',
        'validation': lambda x: len(x) > 20
    },
    {
        'name': "Hipótesis Alternativa (H₁)",
        'question': "Escribe tu hipótesis alternativa (H₁). Esta es la afirmación que el investigador busca establecer, la que contradice la hipótesis nula.",
        'examples': {
            'Cuantitativa': [
                "Existe una influencia significativa del uso de redes sociales en el rendimiento académico de los estudiantes universitarios de primer año de la Facultad de Comunicación de la Universidad X durante el ciclo 2024-II.",
                "Existen diferencias significativas en el nivel de ansiedad ante exámenes entre estudiantes que reciben tutorías y los que no.",
                "La edad del estudiante se correlaciona significativamente de forma inversa con su tasa de abandono universitario."
            ],
            'Cualitativa': [] # Vacío, ya que este paso es específico de cuantitativa
        },
        'input_type': 'text_area',
        'key': 'hipotesis.alternativa',
        'validation': lambda x: len(x) > 20
    },
]

# Pasos finales (comunes para ambos tipos de investigación)
final_common_steps = [
    {
        'name': "Justificación",
        'question': "¿Por qué es importante tu investigación? Explica su relevancia académica, social o práctica, y a quién beneficiará.",
        'examples': {
            'Cuantitativa': [
                "Esta investigación es relevante socialmente al abordar cómo el uso de redes sociales impacta el rendimiento académico, beneficiando a estudiantes y universidades con estrategias de estudio. Académicamente, contribuye al campo de la pedagogía digital y el bienestar estudiantil.",
                "El estudio sobre el estrés académico y calidad del sueño es vital para la salud mental estudiantil, aportando datos que pueden guiar intervenciones universitarias y enriquecer la literatura sobre factores no cognitivos del rendimiento.",
                "Evaluar la efectividad del programa nutricional ofrecerá evidencia empírica crucial para mejorar el manejo de la diabetes tipo 2, beneficiando directamente a pacientes y profesionales de la salud, y validando un modelo de intervención en el contexto local."
            ],
            'Cualitativa': [
                "Este estudio es relevante porque busca comprender las complejidades de la implementación de la educación para el desarrollo sostenible desde la voz de los docentes, lo que puede informar políticas educativas más contextualizadas y efectivas en Portovelo.",
                "Comprender la resiliencia en mujeres migrantes es fundamental para diseñar programas de apoyo psicosocial y laboral que respondan a sus necesidades reales, contribuyendo a una integración más humana y efectiva en la sociedad de acogida.",
                "La exploración de los significados de participación ciudadana en jóvenes de barrios desfavorecidos es crucial para fomentar su empoderamiento, desafiando narrativas preestablecidas y promoviendo una inclusión social más genuina."
            ]
        },
        'input_type': 'text_area',
        'key': 'justificacion',
        'validation': lambda x: len(x) > 50
    },
    {
        'name': "Marco Teórico",
        'question': "Para el marco teórico, ingresa un concepto o variable clave y sus autores principales (formato: Concepto - Autores). Ingresa uno por línea.",
        'examples': {
            'Cuantitativa': [
                "Redes sociales - Boyd & Ellison (2007), Kaplan & Haenlein (2010)",
                "Rendimiento académico - Román y Murillo (2011), Tinto (1993)",
                "Distracción digital - Greenfield (2009), Carr (2010)"
            ],
            'Cualitativa': [
                "Inserciones curriculares - UNESCO (2017), Jickling (2006), Sterling (2012)",
                "Educación para el Desarrollo Sostenible (EDS) - UNESCO (2015), McCloskey (2010)",
                "Percepción docente - Pajares (1992), Shulman (1986)"
            ]
        },
        'input_type': 'text_area',
        'key': 'marco_teorico',
        'special': 'marco_teorico_split', # Indica que el texto se debe parsear para concepto/autores
        'validation': lambda x: len(x) > 0 and all(' - ' in line for line in x.split('\n') if line.strip())
    },
    {
        'name': "Población",
        'question': "Describe la población de tu estudio (¿quiénes son el grupo completo de personas o elementos con características comunes que son objeto de tu investigación?).",
        'examples': {
            'Cualitativa': [
                "La totalidad de docentes de educación básica en el cantón Portovelo, registrados en el distrito educativo durante el período 2024-2025.",
                "Un grupo focal de madres de familia de estudiantes con necesidades especiales en la escuela urbana X, durante el año escolar 2023-2024.",
                "Los pacientes mayores de 65 años diagnosticados con depresión mayor que asisten a la consulta de salud mental en el centro de salud Y, en el último semestre."
            ],
            'Cuantitativa': [
                "Todos los estudiantes de primer año de la Facultad de Comunicación de la Universidad X inscritos en el ciclo 2024-II (aproximadamente 500 estudiantes).",
                "La población estudiantil matriculada en programas de grado de la Facultad de Medicina de la Universidad Z durante el curso académico 2024-2025.",
                "Los residentes de la ciudad A mayores de 18 años, según el último censo poblacional disponible."
            ]
        },
        'input_type': 'text_area',
        'key': 'metodologia.poblacion',
        'validation': lambda x: len(x) > 20
    },
    {
        'name': "Muestra",
        'question': "Describe la muestra de tu estudio (¿cómo seleccionarás a los participantes de la población y cuántos serán?).",
        'examples': {
            'Cualitativa': [
                "15 docentes de educación básica con al menos 5 años de experiencia y que hayan implementado proyectos de desarrollo sostenible, seleccionados por muestreo intencional o por conveniencia.",
                "6 madres de familia participantes en un grupo focal, seleccionadas mediante muestreo por bola de nieve a partir de contactos iniciales.",
                "8 pacientes mayores de 65 años que han completado al menos 3 meses de terapia, seleccionados por muestreo por criterio."
            ],
            'Cuantitativa': [
                "100 estudiantes seleccionados aleatoriamente de la población total (N=500), asegurando representatividad por sexo y programa de estudios mediante muestreo aleatorio simple.",
                "Una muestra estratificada de 250 estudiantes de medicina (125 por sexo) para asegurar la representatividad de la población, calculada con un nivel de confianza del 95% y un margen de error del 5%.",
                "384 ciudadanos seleccionados mediante muestreo aleatorio simple con listado telefónico, para una población infinita con un margen de error del 5% y un nivel de confianza del 95%."
            ]
        },
        'input_type': 'text_area',
        'key': 'metodologia.muestra',
        'validation': lambda x: len(x) > 20
    },
    {
        'name': "Técnicas de Recolección de Datos",
        'question': "¿Qué técnicas e instrumentos usarás para recolectar datos? (Ej. encuestas con cuestionarios, entrevistas a profundidad, observación, análisis documental).",
        'examples': {
            'Cuantitativa': [
                "Encuesta mediante cuestionario estandarizado (para recabar datos numéricos sobre uso de redes sociales y rendimiento percibido).",
                "Análisis documental de expedientes académicos (para obtener promedios de calificaciones objetivas y tasas de abandono)."
                "Escalas de medición psicométricas (para evaluar niveles de estrés o ansiedad, con validación y confiabilidad, como la Escala de Estrés Percibido)."
            ],
            'Cualitativa': [
                "Entrevistas semiestructuradas a docentes (para comprender sus percepciones y experiencias a profundidad).",
                "Observación participante en el aula (para documentar la dinámica de implementación de las inserciones curriculares)."
                "Análisis de contenido de documentos curriculares y planes de estudio (para identificar el enfoque del desarrollo sostenible)."
            ]
        },
        'input_type': 'text_area',
        'key': 'metodologia.tecnicas',
        'validation': lambda x: len(x) > 20
    },
]

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
        'objetivos_especificos': ['', '', ''], # Por defecto 3 objetivos
        'justificacion': '',
        'marco_teorico': [], # Almacena diccionarios {'concepto': '', 'autores': ''}
        'metodologia': {
            'poblacion': '',
            'muestra': '',
            'tecnicas': ''
        },
        # Estas claves se rellenarán solo si el tipo de investigación es Cuantitativa
        'variables': {'independiente': '', 'dependiente': ''},
        'hipotesis': {'nula': '', 'alternativa': ''}
    }

# ==============================================================================
# FUNCIÓN PRINCIPAL DE LA APLICACIÓN STREAMLIT
# ==============================================================================
def main():
    # Título principal y descripción en el área de contenido principal
    st.title("Asistente para Matriz de Investigación")
    st.write("Completa cada sección para construir tu matriz de consistencia.")
    st.markdown("---") # Separador visual

    # ==========================================================================
    # DETERMINACIÓN DINÁMICA DE LOS PASOS COMPLETOS
    # ==========================================================================
    tipo_investigacion = st.session_state.matrix_data.get('tipo_investigacion', '')
    
    # Construir la lista de pasos completa de forma dinámica
    all_steps = list(base_steps) # Copia los pasos base
    if tipo_investigacion == 'Cuantitativa':
        all_steps.extend(quantitative_specific_steps) # Añade los pasos cuantitativos si aplica
    # Los pasos finales comunes siempre se añaden al final, independientemente del tipo
    all_steps.extend(final_common_steps)

    # ==========================================================================
    # BARRA LATERAL DE PROGRESO
    # ==========================================================================
    st.sidebar.header("Progreso de la Matriz")
    # Mostrar el tipo de investigación seleccionado en la barra lateral
    # Si el tipo de investigación ya ha sido seleccionado, se muestra aquí.
    if tipo_investigacion:
        st.sidebar.markdown(f"**Tipo Seleccionado:** {tipo_investigacion}")
        st.sidebar.markdown("---") # Separador visual

    for i, step_info in enumerate(all_steps):
        icon = "⬜" # No iniciado
        if i < st.session_state.step:
            icon = "✅" # Completado
        elif i == st.session_state.step:
            icon = "🟨" # En proceso
        st.sidebar.markdown(f"{icon} {step_info['name']}")

    # ==========================================================================
    # LÓGICA DE VISUALIZACIÓN DEL PASO ACTUAL
    # ==========================================================================
    if st.session_state.step < len(all_steps):
        current_step = all_steps[st.session_state.step]
        
        # Formato de título 1 para la Sección
        st.header(f"Sección: {current_step['name']}") 

        # === Expander de Explicación (primero) ===
        exp_key = current_step['key']
        explanation_content = explanations.get(exp_key)

        if explanation_content:
            with st.expander("Ver explicación 📖"): # Texto ajustado aquí
                if isinstance(explanation_content, dict): # Es una explicación que depende del tipo de investigación
                    current_research_type = st.session_state.matrix_data.get('tipo_investigacion')
                    if current_research_type:
                        st.markdown(explanation_content.get(current_research_type, "Explicación no disponible para este tipo de investigación."))
                    else:
                        st.markdown("Selecciona un tipo de investigación primero para ver la explicación relevante.")
                else: # Es una explicación general
                    st.markdown(explanation_content)
        # === Fin Expander Explicación ===

        # Formato de título 2 para la Pregunta/Tarea
        st.subheader(current_step['question']) # Ahora es subheader

        # === Expander para Ejemplos (segundo, condicional por tipo de investigación) ===
        if current_step['examples']: # Solo muestra el expander si hay ejemplos definidos para el paso
            with st.expander("Ver ejemplos 💡"): # Texto ajustado e icono agregado aquí
                current_research_type = st.session_state.matrix_data.get('tipo_investigacion')
                
                # Obtener los ejemplos específicos para el tipo de investigación actual
                example_list = []
                if isinstance(current_step['examples'], dict):
                    if current_research_type:
                        example_list = current_step['examples'].get(current_research_type, [])
                    else: # Si no hay tipo de investigación seleccionado (primer paso)
                        st.info("Selecciona un tipo de investigación para ver los ejemplos relevantes.")
                # Si 'examples' no es un diccionario, se asume que es una lista directa de ejemplos (para casos futuros si se añadiera)
                elif isinstance(current_step['examples'], list):
                    example_list = current_step['examples']

                if example_list:
                    for i, example_text in enumerate(example_list):
                        st.markdown(f"- **Ejemplo {i+1}:** {example_text}")
                elif current_research_type and isinstance(current_step['examples'], dict):
                    st.info("No hay ejemplos específicos para este tipo de investigación en este paso.")
        # === Fin Expander Ejemplos ===


        # Obtener el valor actual del estado de sesión para el campo
        current_data_value = None
        keys = current_step['key'].split('.')
        if len(keys) == 2: # Para claves anidadas como 'variables.independiente'
            current_data_value = st.session_state.matrix_data[keys[0]].get(keys[1], '')
        else:
            current_data_value = st.session_state.matrix_data.get(current_step['key'], '')

        # Manejar la visualización del input
        if current_step['input_type'] == 'radio':
            # Para radio buttons, el valor por defecto se selecciona del estado
            response = st.radio("Selecciona una opción:", current_step['options'], 
                                index=current_step['options'].index(current_data_value) if current_data_value in current_step['options'] else 0, 
                                key=f"input_{st.session_state.step}")
            st.session_state.matrix_data[current_step['key']] = response

        elif current_step['input_type'] == 'text_input':
            response = st.text_input("Tu respuesta:", value=current_data_value, key=f"input_{st.session_state.step}")
            if len(keys) == 2:
                st.session_state.matrix_data[keys[0]][keys[1]] = response
            else:
                st.session_state.matrix_data[current_step['key']] = response

        elif current_step['input_type'] == 'text_area':
            # Manejo especial para listas y marco teórico
            if current_step.get('special') == 'list_split':
                current_value_area = "\n".join(st.session_state.matrix_data[current_step['key']])
            elif current_step.get('special') == 'marco_teorico_split':
                current_value_area = "\n".join([f"{entry['concepto']} - {entry['autores']}" for entry in st.session_state.matrix_data[current_step['key']]])
            else:
                current_value_area = current_data_value
            
            response = st.text_area("Tu respuesta:", value=current_value_area, key=f"input_{st.session_state.step}", height=150)

            # Guardar el valor procesado en el estado de sesión
            if current_step.get('special') == 'list_split':
                lines = [line.strip() for line in response.split('\n') if line.strip()]
                # Asegurar que no se exceda el límite de 3 objetivos si es el caso
                if current_step['key'] == 'objetivos_especificos':
                    st.session_state.matrix_data[current_step['key']] = lines[:3] 
                else:
                    st.session_state.matrix_data[current_step['key']] = lines
            elif current_step.get('special') == 'marco_teorico_split':
                lines = [line.strip() for line in response.split('\n') if line.strip()]
                marco_teorico_list = []
                for line in lines:
                    parts = line.split(' - ', 1) # Divide solo en el primer ' - '
                    if len(parts) >= 2:
                        marco_teorico_list.append({'concepto': parts[0], 'autores': parts[1]})
                st.session_state.matrix_data[current_step['key']] = marco_teorico_list
            else:
                if len(keys) == 2:
                    st.session_state.matrix_data[keys[0]][keys[1]] = response
                else:
                    st.session_state.matrix_data[current_step['key']] = response
        
        # Validación antes de avanzar
        is_current_step_valid = current_step['validation'](response)
        
        # Mostrar advertencia si no es válido
        if not is_current_step_valid:
            if current_step['input_type'] == 'radio' and response == '': # Específico para el radio inicial
                 st.warning("Por favor, selecciona una opción para continuar.")
            elif current_step['key'] == 'tema' and len(response) <= 20:
                st.warning("El tema de investigación debe tener al menos 20 caracteres.")
            elif current_step['key'] == 'pregunta' and (len(response) <= 20 or '?' not in response):
                 st.warning("La pregunta debe tener al menos 20 caracteres y contener un signo de interrogación.")
            elif current_step['key'] == 'objetivo_general' and (len(response) <= 20 or not any(response.lower().startswith(v) for v in ['analizar', 'determinar', 'describir', 'comprender', 'explorar', 'interpretar'])):
                st.warning("El objetivo general debe tener al menos 20 caracteres y empezar con un verbo en infinitivo (analizar, determinar, describir, comprender, explorar, interpretar).")
            elif current_step['key'] == 'objetivos_especificos' and (len(response) == 0 or not all(len(line.strip()) > 10 for line in response.split('\n') if line.strip())):
                st.warning("Debes ingresar al menos un objetivo específico y cada uno debe tener al menos 10 caracteres.")
            elif current_step['key'] in ['variables.independiente', 'variables.dependiente'] and len(response) <= 5:
                st.warning("El nombre de la variable debe tener al menos 5 caracteres.")
            elif current_step['key'] in ['hipotesis.nula', 'hipotesis.alternativa'] and len(response) <= 20:
                st.warning("La hipótesis debe tener al menos 20 caracteres.")
            elif current_step['key'] == 'justificacion' and len(response) <= 50:
                st.warning("La justificación debe tener al menos 50 caracteres.")
            elif current_step['key'] == 'marco_teorico' and (len(response) == 0 or not all(' - ' in line for line in response.split('\n') if line.strip())):
                st.warning("Debes ingresar al menos una entrada para el marco teórico en formato 'Concepto - Autores'.")
            elif current_step['key'] in ['metodologia.poblacion', 'metodologia.muestra', 'metodologia.tecnicas'] and len(response) <= 20:
                st.warning("La descripción para esta sección de metodología debe tener al menos 20 caracteres.")
            else:
                 st.warning("Por favor, completa el campo antes de avanzar.")


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
            # El botón "Avanzar" solo estará habilitado si la validación es exitosa
            if st.button("Avanzar ➡️", disabled=not is_current_step_valid):
                st.session_state.step += 1
                st.rerun()

    # ==========================================================================
    # PASO FINAL: REVISIÓN DE LA MATRIZ Y DESCARGA
    # ==========================================================================
    else:
        st.subheader("🎉 ¡Matriz de Investigación Completa!")
        st.write("Aquí tienes un resumen de tu matriz de consistencia. Puedes revisarla y empezar una nueva si lo deseas.")
        data = st.session_state.matrix_data
        
        st.markdown("---")
        st.markdown("### Resumen de tu Matriz de Consistencia:")
        st.markdown(f"**Tipo de Investigación:** {data['tipo_investigacion'] or 'No definido'}")
        st.markdown(f"**Tema de Investigación:** {data['tema'] or 'No definido'}")
        st.markdown(f"**Pregunta de Investigación:** {data['pregunta'] or 'No definido'}")
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
                st.markdown(f"- **{entry.get('concepto', 'N/A')}**: {entry.get('autores', 'N/A')}")
        else: st.markdown("No definido")
        
        st.markdown("**Metodología:**")
        st.markdown(f"- **Población:** {data['metodologia']['poblacion'] or 'No definido'}")
        st.markdown(f"- **Muestra:** {data['metodologia']['muestra'] or 'No definido'}")
        st.markdown(f"- **Técnicas de Recolección de Datos:** {data['metodologia']['tecnicas'] or 'No definido'}")
        st.markdown("---")

        # Mini rúbrica de autoevaluación
        st.subheader("Mini Rúbrica de Autoevaluación:")
        st.write("¡Es hora de reflexionar sobre la coherencia de tu diseño!")
        st.checkbox("¿Mi pregunta de investigación está claramente alineada con mis objetivos?")
        st.checkbox("¿Mis objetivos específicos detallan los pasos para alcanzar mi objetivo general?")
        
        if data['tipo_investigacion'] == 'Cualitativa':
            st.checkbox("¿Las categorías analíticas son pertinentes para mi pregunta cualitativa?")
            st.checkbox("¿Las técnicas de recolección de datos son adecuadas para mi enfoque cualitativo?")
        elif data['tipo_investigacion'] == 'Cuantitativa':
            st.checkbox("¿Mis variables (independiente y dependiente) están bien definidas y son medibles?")
            st.checkbox("¿Mis hipótesis son coherentes con mis variables y tipo de estudio?")
            st.checkbox("¿La metodología que propongo es adecuada para responder mi pregunta y probar mis hipótesis?")

        st.markdown("---")
        st.info("¡Recuerda que este es un punto de partida! La investigación es un proceso iterativo. Lee, ajusta y perfecciona tu matriz con la literatura científica.")

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
