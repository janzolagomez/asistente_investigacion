import streamlit as st
import pandas as pd
import google.generativeai as genai
import time
from docx import Document # Importar la librería python-docx
from io import BytesIO # Para manejar archivos en memoria

# --- Configuración de la API de Gemini ---
# Asegúrate de que tu API key esté en .streamlit/secrets.toml
# Por ejemplo: GEMINI_API_KEY="tu_clave_aqui"
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
except KeyError:
    st.error("¡ERROR: Clave API de Gemini no encontrada! Por favor, crea un archivo .streamlit/secrets.toml con 'GEMINI_API_KEY=\"tu_clave\"'.")
    st.stop() # Detiene la ejecución si no hay API key

# Inicializar el modelo de Gemini
model = genai.GenerativeModel('gemini-pro')

# Configuración de la página
st.set_page_config(page_title="Asistente para Matriz de Investigación", layout="wide")

# ==============================================================================
# EXPLICACIONES DETALLADAS POR PASO Y TIPO DE INVESTIGACIÓN
# ==============================================================================
explanations = {
    'tipo_investigacion': "La investigación cualitativa busca comprender fenómenos desde la perspectiva de los participantes, mientras que la cuantitativa busca medir y probar hipótesis a través de datos numéricos y análisis estadístico. La investigación mixta combina ambos enfoques para una comprensión más completa. Elige el enfoque que mejor se adapte a tu pregunta y objetivos.",
    'tema': {
        'Cualitativa': "El tema en investigación cualitativa es una idea general que expresa el fenómeno, sujetos, actores y contexto que quieres estudiar, enfocado en la comprensión profunda. Debe ser amplio pero delimitado.",
        'Cuantitativa': "El tema en investigación cuantitativa debe ser específico, delimitado, e incluir al menos las variables principales y el contexto de estudio. Se enfoca en la medición y la relación entre variables.",
        'Mixta': "El tema en investigación mixta debe ser lo suficientemente amplio para integrar componentes cualitativos y cuantitativos, expresando el fenómeno y el contexto desde ambas perspectivas para una comprensión holística."
    },
    'pregunta': {
        'Cualitativa': "La pregunta cualitativa es una pregunta amplia y abierta que expresa el fenómeno principal que se desea comprender desde la perspectiva de los participantes, sin buscar medir o cuantificar.",
        'Cuantitativa': "La pregunta cuantitativa es una formulación clara, específica y objetiva que plantea una relación, efecto, diferencia o nivel entre una o más variables medibles. Guía la recolección y el análisis estadístico de datos.",
        'Mixta': "La pregunta de investigación mixta integra componentes cualitativos y cuantitativos, buscando comprender un fenómeno de manera más profunda, combinando la exploración de significados con la medición de relaciones o impactos."
    },
    'objetivo_general': {
        'Cualitativa': "En la investigación cualitativa, el objetivo general busca orientar la exploración, comprensión, descripción o interpretación del fenómeno o experiencia en un grupo social o comunidad específica, de manera coherente con un enfoque interpretativo. **Debe iniciar con un verbo en infinitivo (ejemplos: comprender, explorar, describir, interpretar, analizar, investigar).**",
        'Cuantitativa': "En la investigación cuantitativa, el objetivo general debe expresar claramente qué se quiere analizar, correlacionar, describir o explicar en términos de la relación, efecto o influencia entre las variables de estudio, en una población y contexto definidos. **Debe iniciar con un verbo en infinitivo (ejemplos: analizar, determinar, evaluar, establecer, comparar, medir).**",
        'Mixta': "En la investigación mixta, el objetivo general busca integrar la comprensión cualitativa y la medición cuantitativa para abordar el fenómeno de estudio de manera comprehensiva. **Debe iniciar con un verbo en infinitivo que refleje la integración (ejemplos: explorar y determinar, comprender y evaluar, analizar la relación e interpretar las percepciones).**"
    },
    'objetivos_especificos': {
        'Cualitativa': "Son metas concretas y delimitadas que el estudio busca alcanzar para lograr el objetivo general. En cualitativa, suelen enfocarse en acciones como identificar, analizar, describir o interpretar dimensiones del fenómeno.",
        'Cuantitativa': "Son metas concretas y medibles que derivan del objetivo general, detallando los pasos para alcanzarlo. En cuantitativa, se enfocan en describir variables, comparar grupos, correlacionar variables o explicar relaciones específicas.",
        'Mixta': "Son metas concretas que desglosan el objetivo general, incluyendo tanto pasos cualitativos (explorar, comprender, interpretar) como cuantitativos (medir, cuantificar, comparar, correlacionar) para abordar el fenómeno desde ambas perspectivas. Deben reflejar la secuencialidad o concurrencia de las fases."
    },
    'variables.independiente': "Es la característica o propiedad observable y medible que se presume es la *causa* o el factor que influye en otra variable. El investigador la manipula o mide para observar su efecto.",
    'variables.dependiente': "Es la característica o propiedad observable y medible que se presume es el *efecto* o el resultado que cambia debido a la influencia de la variable independiente. Es lo que se observa o mide como respuesta.",
    'hipotesis.nula': "La hipótesis nula (H₀) es una afirmación que postula la ausencia de relación, diferencia o efecto entre variables. Se asume verdadera hasta que los datos demuestren lo contrario.",
    'hipotesis.alternativa': "La hipótesis alternativa (H₁) es la afirmación que el investigador busca establecer. Contradice la hipótesis nula, sugiriendo la existencia de una relación, efecto o diferencia significativa entre las variables.",
    'justificacion': "La justificación explica la *importancia* y el *porqué* de tu investigación. Debe argumentar su relevancia teórica (qué aporta al conocimiento), práctica (cómo resuelve un problema) y social (a quién beneficia o impacta positivamente).",
    'marco_teorico': {
        'Cualitativa': "El marco teórico en investigación cualitativa es una síntesis y selección de **conceptos clave y temas relevantes** que fundamentan tu perspectiva del fenómeno. Sirve para construir tus categorías iniciales o 'lentes interpretativos' antes o durante la recolección de datos.",
        'Cuantitativa': "El marco teórico en investigación cuantitativa es la conceptualización formal de tus variables, basada en la literatura científica existente. Define qué significa cada variable desde un punto de vista académico o técnico, usando autores y modelos reconocidos, y guía la operacionalización y medición. **En esta etapa, concéntrate en los conceptos clave o temas de tu estudio.**",
        'Mixta': "El marco teórico en investigación mixta debe integrar conceptos y teorías relevantes de ambos enfoques (cualitativo y cuantitativo) para fundamentar la comprensión integral del fenómeno. Puede incluir conceptualizaciones de variables y categorías de análisis."
    },
    'metodologia.poblacion': "La población es el *conjunto total* de todas las personas, objetos o elementos que poseen una o más características comunes y que son el universo de tu estudio. Es el grupo al cual deseas generalizar tus hallazgos.",
    'metodologia.muestra': "La muestra es un *subconjunto representativo* de la población, seleccionado para realizar el estudio. Se describe el tipo de muestreo (probabilístico/no probabilístico), el tamaño de la muestra y los criterios de selección utilizados para garantizar que sea adecuada y permita inferencias si es cuantitativa.",
    'metodologia.tecnicas': {
        'Cualitativa': "Las técnicas de recolección de datos cualitativas son los procedimientos y herramientas que te permiten obtener información detallada y profunda para comprender el fenómeno. Ejemplos incluyen entrevistas, grupos focales, observación participante, o análisis documental.",
        'Cuantitativa': "Las técnicas de recolección de datos cuantitativas son los procedimientos y herramientas que te permiten obtener datos numéricos y estructurados para medir variables y probar hipótesis. Ejemplos incluyen encuestas con cuestionarios estandarizados, escalas de medición (Likert), o la recopilación de datos de registros existentes.",
        'Mixta': "Las técnicas de recolección de datos mixtas combinan procedimientos cualitativos (ej., entrevistas, grupos focales) y cuantitativos (ej., encuestas, escalas estandarizadas) para recopilar información rica y variada, buscando la complementariedad y triangulación de los datos."
    },
    'metodologia.filosofia': {
        'Cualitativa': "La filosofía de la investigación es la postura epistemológica sobre cómo se concibe el conocimiento y la realidad. Para la investigación cualitativa, los enfoques comunes son el Interpretativismo (que busca comprender el significado subjetivo de las experiencias) y el Pragmatismo (que se centra en la utilidad práctica del conocimiento).",
        'Cuantitativa': "La filosofía de la investigación es la postura epistemológica sobre cómo se concibe el conocimiento y la realidad. Para la investigación cuantitativa, los enfoques comunes son el Positivismo (que busca leyes generales y objetivas a través de la observación empírica y la verificación de hipótesis, buscando leyes generales).",
        'Mixta': "La filosofía de la investigación para un enfoque mixto es comúnmente el Pragmatismo, que valora la utilidad del conocimiento y la resolución de problemas, permitiendo la combinación de distintas perspectivas para lograr un objetivo de investigación más amplio y profundo."
    },
    'metodologia.enfoque': {
        'Cualitativa': "El enfoque de la investigación es el tipo de razonamiento que guía el proceso investigativo. En la investigación cualitativa, el enfoque es principalmente Inductivo, lo que significa que se parte de la observación de datos específicos para construir teorías o patrones generales.",
        'Cuantitativa': "El enfoque de la investigación es el tipo de razonamiento que guía el proceso investigativo. En la investigación cuantitativa, el enfoque es principalmente Deductivo, lo que significa que se parte de teorías o hipótesis generales para probarlas a través de la recolección y análisis de datos específicos.",
        'Mixta': "El enfoque de la investigación mixta combina razonamiento deductivo e inductivo, utilizando ambos enfoques en diferentes fases (secuencial) o de manera simultánea (concurrente), buscando la complementariedad en la construcción del conocimiento."
    },
    'metodologia.tipologia_estudio': {
        'Cualitativa': "La tipología o alcance de estudio clasifica la investigación cualitativa según su propósito y profundidad. Algunos tipos comunes incluyen: Fenomenológico (explora experiencias vividas), Hermenéutico (interpreta textos o símbolos), Crítico (analiza el poder y la injusticia), y Narrativo (examina historias de vida).",
        'Cuantitativa': "La tipología o alcance de estudio clasifica la investigación cuantitativa según su propósito. Los tipos comunes son: Descriptivo (describe características de una población), Correlacional (examina la relación entre variables), y Explicativo (busca causas y efectos de fenómenos).",
        'Mixta': "La tipología o alcance de estudio mixto depende del diseño específico, buscando integrar la exploración y la explicación. Incluye diseños como Exploratorio Secuencial (cual-cuant), Explicatorio Secuencial (cuant-cual), y Convergente Paralelo (cual+cuant)."
    },
    'metodologia.horizonte_tiempo': { # Añadido como diccionario para uniformidad, aunque el valor sea el mismo
        'Cualitativa': "El horizonte de tiempo se refiere al plazo temporal del estudio en función de su duración y momentos de observación. Puede ser Transversal (los datos se recogen en un único momento) o Longitudinal (los datos se recogen en múltiples momentos a lo largo del tiempo).",
        'Cuantitativa': "El horizonte de tiempo se refiere al plazo temporal del estudio en función de su duración y momentos de observación. Puede ser Transversal (los datos se recogen en un único momento) o Longitudinal (los datos se recogen en múltiples momentos a lo largo del tiempo).",
        'Mixta': "El horizonte de tiempo se refiere al plazo temporal del estudio en función de su duración y momentos de observación. Puede ser Transversal (los datos se recogen en un único momento) o Longitudinal (los datos se recogen en múltiples momentos a lo largo del tiempo)."
    },
    'metodologia.estrategias': {
        'Cualitativa': "Las estrategias de investigación cualitativa son los diseños estructurales generales para abordar el estudio. Ejemplos incluyen: Estudio de caso, Investigación Acción Participativa (IAP), Etnográfico y Teoría Fundamentada. Cada una ofrece una forma particular de acercarse al fenómeno para una comprensión profunda.",
        'Cuantitativa': "Las estrategias de investigación cuantitativa son los diseños estructurales generales que se emplean para la recolección y análisis de datos numéricos. Ejemplos comunes son el Diseño de Encuesta, Experimental, Cuasi-experimental y No experimental. Cada estrategia define cómo se manipularán o se observarán las variables y cómo se recolectarán los datos.",
        'Mixta': "Las estrategias de investigación mixta son diseños que integran explícitamente los componentes cualitativos y cuantitativos. Incluyen diseños como Convergente Paralelo, Exploratorio Secuencial (QUAL-quan) y Explicatorio Secuencial (QUAN-qual), los cuales definen la secuencia y la forma de integración de los datos."
    }
}


# ==============================================================================
# PROMPTS PARA LA VALIDACIÓN CON GEMINI
# ==============================================================================
gemini_prompts = {
    'tipo_investigacion': lambda respuesta: f"""
Actúa como un experto en metodología de investigación. Evalúa la elección del tipo de investigación '{respuesta}'.

Estructura tu respuesta en:
1. Reconocimiento del aporte del estudiante.
2. Evaluación crítica fundamentada: ¿el tipo de investigación es coherente con el enfoque general del estudio?
3. Orientación para la mejora (si aplica).
4. Ejemplo orientativo (si aplica).

Extensión máxima: 300 tokens. Mantén un tono académico, respetuoso y crítico.
""",
    'tema': {
        'Cualitativa': lambda tema: f"""
Actúa como experto en investigación cualitativa. Evalúa el siguiente tema de investigación:

"{tema}"

Estructura tu respuesta en:
1. Valoración inicial del esfuerzo.
2. Evaluación crítica: ¿delimita fenómeno y contexto? ¿es apropiado para estudio cualitativo?
3. Sugerencias claras de mejora.
4. Ejemplo orientador (no resolver).

Extensión máxima: 300 tokens. Sé claro y empático.
""",
        'Cuantitativa': lambda tema: f"""
Actúa como experto en investigación cuantitativa. Evalúa el siguiente tema:

"{tema}"

Estructura tu evaluación en:
1. Reconocimiento del aporte.
2. Evaluación crítica: ¿incluye variables? ¿es específico? ¿coherente con lo cuantitativo?
3. Orientación para mejorar.
4. Ejemplo ilustrativo (si aplica).

Responde en tono académico y constructivo. Extensión máxima: 300 tokens.
""",
        'Mixta': lambda tema: f"""
Actúa como experto en investigación mixta. Evalúa el siguiente tema de investigación:

"{tema}"

Estructura tu respuesta en:
1. Valoración inicial del esfuerzo.
2. Evaluación crítica: ¿delimita el fenómeno desde perspectivas cualitativas y cuantitativas? ¿Es lo suficientemente amplio para un diseño mixto?
3. Sugerencias claras de mejora.
4. Ejemplo orientador (no resolver).

Extensión máxima: 300 tokens. Sé claro y empático.
"""
    },
    'pregunta': {
        'Cualitativa': lambda pregunta: f"""
Eres experto en investigación cualitativa. Evalúa la siguiente pregunta:

"{pregunta}"

Tu retroalimentación debe:
1. Reconocer el esfuerzo.
2. Evaluar si es abierta, interpretativa y fenomenológica.
3. Orientar si requiere mejoras.
4. Incluir ejemplo similar como guía.

Sé crítico y empático. Extensión máxima: 300 tokens.
""",
        'Cuantitativa': lambda pregunta: f"""
Actúa como experto en investigación cuantitativa. Evalúa:

"{pregunta}"

Tu evaluación debe:
1. Valorar el intento del estudiante.
2. Evaluar claridad, relación de variables, objetividad.
3. Orientar sin reemplazar.
4. Dar ejemplo comparativo.

Responde de forma crítica y constructiva. Extensión máxima: 300 tokens.
""",
        'Mixta': lambda pregunta: f"""
Eres experto en investigación mixta. Evalúa la siguiente pregunta:

"{pregunta}"

Tu retroalimentación debe:
1. Reconocer el esfuerzo.
2. Evaluar si integra componentes cualitativos y cuantitativos. ¿Es clara, específica y abarcadora para un diseño mixto?
3. Orientar si requiere mejoras.
4. Incluir ejemplo similar como guía.

Sé crítico y empático. Extensión máxima: 300 tokens.
"""
    },
    'objetivo_general': {
        'Cualitativa': lambda obj: f"""
Eres especialista en investigación cualitativa. Evalúa el objetivo general:

"{obj}"

Organiza tu respuesta en:
1. Reconocimiento.
2. Evaluación: ¿verbo en infinitivo adecuado? ¿coherente con lo cualitativo?
3. Recomendaciones claras.
4. Ejemplo tipo.

Extensión máxima: 300 tokens.
""",
        'Cuantitativa': lambda obj: f"""
Actúa como experto en metodología cuantitativa. Evalúa:

"{obj}"

Responde en:
1. Valoración inicial.
2. Evaluación técnica: ¿verbo de acción medible? ¿variables claras?
3. Orientación pedagógica.
4. Modelo orientador.

Extensión máxima: 300 tokens.
""",
        'Mixta': lambda obj: f"""
Eres especialista en investigación mixta. Evalúa el objetivo general:

"{obj}"

Organiza tu respuesta en:
1. Reconocimiento.
2. Evaluación: ¿El verbo en infinitivo refleja la integración cualitativa y cuantitativa? ¿Es coherente con un diseño mixto?
3. Recomendaciones claras.
4. Ejemplo tipo.

Extensión máxima: 300 tokens.
"""
    },
    'objetivos_especificos': {
        'Cualitativa': lambda objs: f"""
Evalúa los siguientes objetivos específicos cualitativos:

"{objs}"

Tu respuesta debe incluir:
1. Aprecio por el esfuerzo.
2. Evaluación crítica: ¿derivan del objetivo general? ¿son coherentes con lo cualitativo?
3. Orientación concreta.
4. Ejemplo orientativo parcial.

Extensión máxima: 300 tokens.
""",
        'Cuantitativa': lambda objs: f"""
Evalúa los siguientes objetivos específicos cuantitativos:

"{objs}"

Organiza la retroalimentación en:
1. Reconocimiento inicial.
2. Evaluación crítica: ¿son medibles? ¿alineados con variables y objetivo general?
3. Recomendaciones formativas.
4. Ejemplo ilustrativo.

Extensión máxima: 300 tokens.
""",
        'Mixta': lambda objs: f"""
Evalúa los siguientes objetivos específicos mixtos:

"{objs}"

Tu respuesta debe incluir:
1. Aprecio por el esfuerzo.
2. Evaluación crítica: ¿derivan del objetivo general? ¿Integran pasos cualitativos y cuantitativos? ¿Reflejan la secuencialidad/concurrencia del diseño?
3. Orientación concreta.
4. Ejemplo orientativo parcial.

Extensión máxima: 300 tokens.
"""
    },
    'variables.independiente': lambda var: f"""
Evalúa la siguiente variable independiente:

"{var}"

Estructura tu respuesta en:
1. Apreciación inicial.
2. Evaluación crítica: ¿es la causa? ¿está bien definida y operacionalizada?
3. Orientación pedagógica.
4. Ejemplo similar.

Extensión máxima: 300 tokens.
""",
    'variables.dependiente': lambda var: f"""
Evalúa la siguiente variable dependiente:

"{var}"

Organiza tu retroalimentación en:
1. Valoración del aporte.
2. Evaluación crítica: ¿representa el efecto? ¿es medible y coherente?
3. Recomendación para refinar.
4. Ejemplo modelo.

Extensión máxima: 300 tokens.
""",
    'hipotesis.nula': lambda hip: f"""
Evalúa la siguiente hipótesis nula:

"{hip}"

Sigue esta estructura:
1. Reconocimiento del esfuerzo.
2. Evaluación: ¿representa ausencia de relación/efecto? ¿es verificable?
3. Sugerencias.
4. Ejemplo orientador.

Extensión máxima: 300 tokens.
""",
    'hipotesis.alternativa': lambda hip: f"""
Evalúa la siguiente hipótesis alternativa:

"{hip}"

Desarrolla tu retroalimentación en:
1. Apreciación del intento.
2. Evaluación crítica: ¿contradice a la nula? ¿establece relación o efecto verificable?
3. Sugerencia de mejora.
4. Ejemplo ilustrativo.

Extensión máxima: 300 tokens.
""",
    'justificacion': lambda just: f"""
Evalúa la siguiente justificación:

"{just}"

Tu evaluación debe:
1. Reconocer aspectos positivos.
2. Evaluar: ¿aborda conveniencia, relevancia social, valor teórico, utilidad?
3. Orientación formativa.
4. Preguntas guía para revisión.

Extensión máxima: 300 tokens.
""",
    'marco_teorico': lambda temas: f"""
Evalúa la lista de conceptos para el marco teórico:

"{temas}"

1. Breve introducción en español.
2. Evaluación de pertinencia.
3. Genera lista de 5-10 palabras clave en inglés para búsqueda científica (Scopus, WoS).

Extensión máxima: 300 tokens.
""",
    'metodologia.poblacion': lambda pob: f"""
Evalúa la descripción de población:

"{pob}"

1. Valoración del esfuerzo.
2. Evaluación crítica: ¿está bien delimitada? ¿se identifican características comunes?
3. Sugerencias.
4. Ejemplo orientativo.

Extensión máxima: 300 tokens.
""",
    'metodologia.muestra': lambda mue: f"""
Evalúa la muestra propuesta:

"{mue}"

1. Reconocimiento.
2. Evaluación: ¿tipo de muestreo y tamaño adecuados?
3. Orientación para ajustes.
4. Ejemplo similar.

Extensión máxima: 300 tokens.
""",
    'metodologia.tecnicas': {
        'Cualitativa': lambda tec: f"""
Evalúa técnicas e instrumentos:

"{tec}"

1. Aprecio inicial.
2. Evaluación crítica: ¿permiten recolectar los datos necesarios según el enfoque?
3. Recomendaciones.
4. Ejemplo.

Extensión máxima: 300 tokens.
""",
        'Cuantitativa': lambda tec: f"""
Evalúa técnicas e instrumentos:

"{tec}"

1. Aprecio inicial.
2. Evaluación crítica: ¿permiten recolectar los datos necesarios según el enfoque?
3. Recomendaciones.
4. Ejemplo.

Extensión máxima: 300 tokens.
""",
        'Mixta': lambda tec: f"""
Evalúa las técnicas e instrumentos propuestos para un estudio mixto:

"{tec}"

1. Aprecio inicial.
2. Evaluación crítica: ¿Las técnicas e instrumentos cualitativos y cuantitativos son apropiados para el diseño mixto? ¿Se complementan para la triangulación de datos?
3. Recomendaciones.
4. Ejemplo.

Extensión máxima: 300 tokens.
"""
    },
    'metodologia.filosofia': {
        'Cualitativa': lambda filo: f"""
Evalúa la filosofía de investigación cualitativa:

"{filo}"

1. Reconocimiento del intento.
2. Evaluación: ¿se alinea con paradigmas interpretativos/pragmáticos?
3. Sugerencias.
4. Ejemplo orientativo.

Extensión máxima: 300 tokens.
""",
        'Cuantitativa': lambda filo: f"""
Evalúa la filosofía de investigación cuantitativa:

"{filo}"

1. Apreciación inicial.
2. Evaluación: ¿se alinea con paradigma positivista/pragmático?
3. Orientación.
4. Ejemplo.

Extensión máxima: 300 tokens.
""",
        'Mixta': lambda filo: f"""
Evalúa la filosofía de investigación para un estudio mixto:

"{filo}"

1. Reconocimiento del intento.
2. Evaluación: ¿Es la filosofía adecuada para integrar ambos enfoques?
3. Sugerencias.
4. Ejemplo orientativo.

Extensión máxima: 300 tokens.
"""
    },
    'metodologia.enfoque': {
        'Cualitativa': lambda enfoque: f"""
Evalúa el enfoque cualitativo:

"{enfoque}"

1. Reconocimiento.
2. Evaluación crítica: ¿se alinea con razonamiento inductivo?
3. Recomendaciones.
4. Ejemplo.

Extensión máxima: 300 tokens.
""",
        'Cuantitativa': lambda enfoque: f"""
Evalúa el enfoque cuantitativo:

"{enfoque}"

1. Apreciación.
2. Evaluación crítica: ¿se alinea con razonamiento deductivo?
3. Recomendaciones.
4. Ejemplo.

Extensión máxima: 300 tokens.
""",
        'Mixta': lambda enfoque: f"""
Evalúa el enfoque para un estudio mixto:

"{enfoque}"

1. Reconocimiento.
2. Evaluación crítica: ¿Refleja la combinación de razonamiento inductivo y deductivo apropiada para un diseño mixto?
3. Recomendaciones.
4. Ejemplo.

Extensión máxima: 300 tokens.
"""
    },
    'metodologia.tipologia_estudio': {
        'Cualitativa': lambda tipologia: f"""
Evalúa la tipología del estudio cualitativo:

"{tipologia}"

1. Aprecio inicial.
2. Evaluación crítica: ¿es una clasificación reconocida? ¿coherente con el propósito?
3. Recomendación.
4. Ejemplo.

Extensión máxima: 300 tokens.
""",
        'Cuantitativa': lambda tipologia: f"""
Evalúa la tipología del estudio cuantitativo:

"{tipologia}"

1. Reconocimiento.
2. Evaluación: ¿es adecuada para lo que se quiere medir o comparar?
3. Sugerencia.
4. Modelo.

Extensión máxima: 300 tokens.
""",
        'Mixta': lambda tipologia: f"""
Evalúa la tipología del estudio mixto:

"{tipologia}"

1. Reconocimiento.
2. Evaluación: ¿Es una clasificación reconocida para diseños mixtos? ¿Es coherente con el propósito de integrar ambos enfoques?
3. Sugerencia.
4. Modelo.

Extensión máxima: 300 tokens.
"""
    },
    'metodologia.horizonte_tiempo': lambda horiz: f"""
Evalúa el horizonte de tiempo:

"{horiz}"

1. Reconocimiento del esfuerzo.
2. Evaluación crítica: ¿Es la elección (transversal/longitudinal) adecuada para la pregunta y objetivos de investigación?
3. Sugerencias para mayor claridad o justificación.
4. Ejemplo orientativo.

Extensión máxima: 300 tokens.
""",
    'metodologia.estrategias': {
        'Cualitativa': lambda est: f"""
Evalúa las estrategias de investigación cualitativas:

"{est}"

1. Reconocimiento.
2. Evaluación crítica: ¿Son las estrategias apropiadas para el enfoque cualitativo y el tipo de estudio?
3. Recomendaciones para mayor detalle o ajuste.
4. Ejemplo.

Extensión máxima: 300 tokens.
""",
        'Cuantitativa': lambda est: f"""
Evalúa las estrategias de investigación cuantitativas:

"{est}"

1. Reconocimiento.
2. Evaluación crítica: ¿Son las estrategias apropiadas para el enfoque cuantitativo y el tipo de estudio?
3. Recomendaciones para mayor detalle o ajuste.
4. Ejemplo.

Extensión máxima: 300 tokens.
""",
        'Mixta': lambda est: f"""
Evalúa las estrategias de investigación mixta:

"{est}"

1. Reconocimiento.
2. Evaluación crítica: ¿Son las estrategias apropiadas para el diseño mixto y cómo integran los componentes cualitativos y cuantitativos?
3. Recomendaciones para mayor detalle o ajuste.
4. Ejemplo.

Extensión máxima: 300 tokens.
"""
    },
    # --- NUEVO PROMPT PARA LA EVALUACIÓN COMPLETA DE LA MATRIZ ---
    'evaluacion_completa_matriz': lambda datos_matriz: f"""
Actúa como un comité de expertos en metodología de investigación altamente experimentado. Tu tarea es realizar una evaluación crítica y holística de la siguiente matriz de investigación, centrándote en la **coherencia interna, la robustez metodológica y la alineación general** entre todos sus componentes.

Aquí están los detalles de la matriz de investigación proporcionados por el estudiante:

Tipo de Investigación: {datos_matriz.get('tipo_investigacion', 'No especificado')}

---
**Sección de Problema:**
Tema: {datos_matriz.get('tema', 'No especificado')}
Pregunta de Investigación: {datos_matriz.get('pregunta', 'No especificado')}
Objetivo General: {datos_matriz.get('objetivo_general', 'No especificado')}
Objetivos Específicos: {datos_matriz.get('objetivos_especificos', 'No especificado')}
Variables (Cuantitativa/Mixta):
    - Independiente: {datos_matriz.get('variables.independiente', 'N/A')}
    - Dependiente: {datos_matriz.get('variables.dependiente', 'N/A')}
Hipótesis (Cuantitativa/Mixta):
    - Nula: {datos_matriz.get('hipotesis.nula', 'N/A')}
    - Alternativa: {datos_matriz.get('hipotesis.alternativa', 'N/A')}
Justificación: {datos_matriz.get('justificacion', 'No especificada')}

---
**Sección de Marco Teórico:**
Conceptos Clave / Temas para el Marco Teórico: {datos_matriz.get('marco_teorico', 'No especificados')}

---
**Sección de Metodología:**
Población: {datos_matriz.get('metodologia.poblacion', 'No especificada')}
Muestra: {datos_matriz.get('metodologia.muestra', 'No especificada')}
Técnicas de Recolección de Datos: {datos_matriz.get('metodologia.tecnicas', 'No especificadas')}
Filosofía de Investigación: {datos_matriz.get('metodologia.filosofia', 'No especificada')}
Enfoque de Investigación: {datos_matriz.get('metodologia.enfoque', 'No especificado')}
Tipología del Estudio: {datos_matriz.get('metodologia.tipologia_estudio', 'No especificada')}
Horizonte de Tiempo: {datos_matriz.get('metodologia.horizonte_tiempo', 'No especificado')}
Estrategias de Investigación: {datos_matriz.get('metodologia.estrategias', 'No especificadas')}

---

Basado en la información anterior, tu evaluación debe abordar los siguientes puntos de forma concisa y profesional:

1.  **Coherencia Interna General:** ¿Cómo se relacionan el tipo de investigación con el tema, pregunta, objetivos y metodología? Identifica cualquier inconsistencia mayor.
2.  **Claridad y Precisión:** ¿Los elementos están formulados de manera clara y específica para el enfoque seleccionado?
3.  **Viabilidad:** ¿Parece la propuesta metodológica viable y adecuada para abordar la pregunta de investigación?
4.  **Sugerencias de Fortalecimiento:** Proporciona recomendaciones concretas para mejorar la matriz en su conjunto, enfocándote en la integración y la solidez.

Mantén un tono académico, objetivo y constructivo. La extensión máxima para esta evaluación es de 800 tokens para permitir una visión global sin ser excesivamente detallada en cada punto individual.
"""
}

# ==============================================================================
# FUNCIONES AUXILIARES
# ==============================================================================

def get_gemini_response(prompt_template, input_data, research_type=None):
    """
    Obtiene una respuesta de Gemini para un prompt dado.
    Maneja prompts que son strings directos o diccionarios con tipos de investigación.
    """
    if isinstance(prompt_template, dict):
        if research_type and research_type in prompt_template:
            prompt = prompt_template[research_type](input_data)
        else:
            st.warning(f"No se encontró un prompt específico para el tipo de investigación '{research_type}' para esta sección. Usando un prompt genérico si existe.")
            # Podrías definir un prompt_template['default'] si quieres un fallback
            return "No hay un prompt específico configurado para este tipo de investigación en esta sección."
    else: # Es un string directo o una función lambda directa
        prompt = prompt_template(input_data)

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        st.error(f"Error al obtener respuesta de Gemini: {e}")
        st.warning("Asegúrate de que tu clave API es válida y de que no se superan los límites de tokens.")
        return "No se pudo generar la evaluación en este momento. Por favor, inténtalo de nuevo."


def init_session_state():
    """Inicializa el session_state para todas las variables de la matriz si no existen."""
    default_values = {
        'tipo_investigacion': None,
        'tema': '',
        'pregunta': '',
        'objetivo_general': '',
        'objetivos_especificos': '',
        'variables.independiente': '',
        'variables.dependiente': '',
        'hipotesis.nula': '',
        'hipotesis.alternativa': '',
        'justificacion': '',
        'marco_teorico': '',
        'metodologia.poblacion': '',
        'metodologia.muestra': '',
        'metodologia.tecnicas': '',
        'metodologia.filosofia': '',
        'metodologia.enfoque': '',
        'metodologia.tipologia_estudio': '',
        'metodologia.horizonte_tiempo': '',
        'metodologia.estrategias': ''
    }
    for key, default_value in default_values.items():
        if key not in st.session_state:
            st.session_state[key] = default_value

def display_section(title, key, input_type, options=None, is_required_for_full_eval=False):
    st.markdown(f"### {title}")
    
    # Mostrar explicación detallada
    if key in explanations:
        current_explanation = explanations[key]
        if isinstance(current_explanation, dict) and st.session_state['tipo_investigacion']:
            st.info(current_explanation.get(st.session_state['tipo_investigacion'], "Explicación no disponible para este tipo de investigación."))
        elif isinstance(current_explanation, str):
            st.info(current_explanation)
    else:
        st.info("No hay una explicación detallada para esta sección.")

    user_input = None
    if input_type == 'text_area':
        user_input = st.text_area(
            f"Introduce tu propuesta para {title.lower()}:",
            value=st.session_state.get(key, ''),
            key=key,
            height=150
        )
    elif input_type == 'text_input':
        user_input = st.text_input(
            f"Introduce tu propuesta para {title.lower()}:",
            value=st.session_state.get(key, ''),
            key=key
        )
    elif input_type == 'selectbox':
        user_input = st.selectbox(
            f"Selecciona una opción para {title.lower()}:",
            options=options,
            index=options.index(st.session_state.get(key, options[0])) if st.session_state.get(key) in options else 0,
            key=key
        )
    elif input_type == 'radio':
        user_input = st.radio(
            f"Selecciona una opción:",
            options=options,
            index=options.index(st.session_state.get(key, options[0])) if st.session_state.get(key) in options else 0,
            key=key
        )

    # Actualizar session_state con el nuevo valor
    st.session_state[key] = user_input

    if st.button(f"Evaluar {title} con IA ✨", key=f"btn_{key}"):
        if user_input:
            with st.spinner(f"Evaluando {title.lower()}..."):
                response_text = ""
                if key in gemini_prompts:
                    prompt_template = gemini_prompts[key]
                    if isinstance(prompt_template, dict):
                        if st.session_state.get('tipo_investigacion'):
                            response_text = get_gemini_response(prompt_template, user_input, st.session_state['tipo_investigacion'])
                        else:
                            st.warning("Por favor, selecciona primero el Tipo de Investigación para una evaluación más precisa.")
                            response_text = "No se puede evaluar sin el tipo de investigación definido."
                    else:
                        response_text = get_gemini_response(prompt_template, user_input)
                else:
                    response_text = "No hay un prompt de validación configurado para esta sección."
                
                st.markdown(f"**Retroalimentación del Experto para {title}:**")
                st.write(response_text)
        else:
            st.warning(f"Por favor, introduce algo en '{title}' antes de evaluarlo.")

    st.markdown("---") # Separador para cada sección

def generate_word_doc(data):
    doc = Document()
    doc.add_heading('Matriz de Investigación', level=1)

    # Añadir Tipo de Investigación (si existe)
    if 'tipo_investigacion' in data and data['tipo_investigacion']:
        doc.add_heading('Tipo de Investigación', level=2)
        doc.add_paragraph(data['tipo_investigacion'])

    sections = {
        "Problema de Investigación": [
            ("Tema", 'tema'),
            ("Pregunta de Investigación", 'pregunta'),
            ("Objetivo General", 'objetivo_general'),
            ("Objetivos Específicos", 'objetivos_especificos')
        ],
        "Variables e Hipótesis (si aplica)": [
            ("Variable Independiente", 'variables.independiente'),
            ("Variable Dependiente", 'variables.dependiente'),
            ("Hipótesis Nula", 'hipotesis.nula'),
            ("Hipótesis Alternativa", 'hipotesis.alternativa')
        ],
        "Justificación": [("Justificación", 'justificacion')],
        "Marco Teórico": [("Conceptos Clave / Temas", 'marco_teorico')],
        "Metodología": [
            ("Población", 'metodologia.poblacion'),
            ("Muestra", 'metodologia.muestra'),
            ("Técnicas de Recolección de Datos", 'metodologia.tecnicas'),
            ("Filosofía de Investigación", 'metodologia.filosofia'),
            ("Enfoque de Investigación", 'metodologia.enfoque'),
            ("Tipología del Estudio", 'metodologia.tipologia_estudio'),
            ("Horizonte de Tiempo", 'metodologia.horizonte_tiempo'),
            ("Estrategias de Investigación", 'metodologia.estrategias')
        ]
    }

    for section_title, items in sections.items():
        has_content = False
        for _, key in items:
            if data.get(key) and data[key].strip():
                has_content = True
                break
        
        if has_content:
            doc.add_heading(section_title, level=2)
            for item_name, key in items:
                value = data.get(key, '')
                if value and value.strip(): # Solo añadir si hay contenido
                    doc.add_paragraph(f"**{item_name}:** {value}")
            doc.add_paragraph("") # Espacio entre secciones

    bio = BytesIO()
    doc.save(bio)
    bio.seek(0)
    return bio

# ==============================================================================
# FUNCIÓN PRINCIPAL DE LA APLICACIÓN STREAMLIT
# ==============================================================================
def main():
    st.title("Asistente Interactivo para tu Matriz de Investigación 🚀")
    st.markdown("Este asistente te guiará paso a paso en la construcción de tu matriz de investigación, ofreciéndote explicaciones detalladas y retroalimentación experta con IA.")

    # Inicializar session_state
    init_session_state()

    st.header("1. Tipo de Investigación")
    st.info(explanations['tipo_investigacion'])
    st.session_state['tipo_investigacion'] = st.radio(
        "Selecciona el tipo principal de tu investigación:",
        options=["Cualitativa", "Cuantitativa", "Mixta"],
        index=["Cualitativa", "Cuantitativa", "Mixta"].index(st.session_state.get('tipo_investigacion', "Cualitativa"))
    )
    if st.button("Evaluar Tipo de Investigación ✨", key="btn_tipo_investigacion"):
        if st.session_state['tipo_investigacion']:
            with st.spinner("Evaluando el tipo de investigación..."):
                response_text = get_gemini_response(gemini_prompts['tipo_investigacion'], st.session_state['tipo_investigacion'])
                st.markdown("**Retroalimentación del Experto para Tipo de Investigación:**")
                st.write(response_text)
    st.markdown("---")

    # Mostrar secciones restantes solo si se ha seleccionado un tipo de investigación
    if st.session_state.get('tipo_investigacion'):
        current_type = st.session_state['tipo_investigacion']

        st.header("2. Problema de Investigación")
        display_section("Tema de Investigación", 'tema', 'text_area')
        display_section("Pregunta de Investigación", 'pregunta', 'text_area')
        display_section("Objetivo General", 'objetivo_general', 'text_area')
        display_section("Objetivos Específicos", 'objetivos_especificos', 'text_area')

        if current_type in ["Cuantitativa", "Mixta"]:
            st.header("3. Variables e Hipótesis")
            st.info("Esta sección aplica para investigaciones cuantitativas o mixtas.")
            display_section("Variable Independiente", 'variables.independiente', 'text_area')
            display_section("Variable Dependiente", 'variables.dependiente', 'text_area')
            display_section("Hipótesis Nula (H₀)", 'hipotesis.nula', 'text_area')
            display_section("Hipótesis Alternativa (H₁)", 'hipotesis.alternativa', 'text_area')

        st.header("4. Justificación de la Investigación")
        display_section("Justificación", 'justificacion', 'text_area')

        st.header("5. Marco Teórico")
        display_section("Conceptos Clave para el Marco Teórico", 'marco_teorico', 'text_area')

        st.header("6. Metodología de la Investigación")
        display_section("Población", 'metodologia.poblacion', 'text_area')
        display_section("Muestra", 'metodologia.muestra', 'text_area')
        display_section("Técnicas e Instrumentos de Recolección", 'metodologia.tecnicas', 'text_area')

        # Opciones para selectbox o radio buttons basados en el tipo de investigación
        filosofia_options = list(explanations['metodologia.filosofia'].keys())
        enfoque_options = list(explanations['metodologia.enfoque'].keys())
        tipologia_options = list(explanations['metodologia.tipologia_estudio'].keys())
        estrategias_options = list(explanations['metodologia.estrategias'].keys())

        # Asegurarse de que las opciones del radio button sean las relevantes para el tipo de inv.
        # Ajustamos el display_section para que pase las opciones correctas.
        # Filosofía
        current_filo_options = list(explanations['metodologia.filosofia'].keys()) # [Cualitativa, Cuantitativa, Mixta]
        display_section("Filosofía de Investigación", 'metodologia.filosofia', 'radio', options=current_filo_options)

        # Enfoque
        current_enfoque_options = list(explanations['metodologia.enfoque'].keys())
        display_section("Enfoque de Investigación", 'metodologia.enfoque', 'radio', options=current_enfoque_options)

        # Tipología
        current_tipologia_options = list(explanations['metodologia.tipologia_estudio'].keys())
        display_section("Tipología del Estudio", 'metodologia.tipologia_estudio', 'radio', options=current_tipologia_options)

        display_section("Horizonte de Tiempo", 'metodologia.horizonte_tiempo', 'radio', options=["Transversal", "Longitudinal"])

        # Estrategias
        current_estrategias_options = list(explanations['metodologia.estrategias'].keys())
        display_section("Estrategias de Investigación", 'metodologia.estrategias', 'radio', options=current_estrategias_options)


        st.header("7. Evaluación Crítica Completa de la Matriz por la IA 🧐")
        st.write("A continuación, se evaluará la coherencia de toda tu matriz.")

        if st.button("Obtener Evaluación Crítica de la Matriz ✨", key="btn_eval_completa"):
            # Recopilar todos los datos de st.session_state para la evaluación completa
            datos_completos_matriz = {key: st.session_state.get(key, '') for key in init_session_state.__defaults__[0].keys()}

            with st.spinner("Analizando la matriz completa con el experto AI..."):
                prompt_completo = gemini_prompts['evaluacion_completa_matriz'](datos_completos_matriz)
                try:
                    response = model.generate_content(prompt_completo)
                    analisis_experto = response.text
                    st.markdown("**Análisis del Experto:**")
                    st.write(analisis_experto)
                except Exception as e:
                    st.error(f"Hubo un error al obtener la evaluación de Gemini: {e}")
                    st.warning("Por favor, asegúrate de que tu clave API de Gemini esté configurada correctamente y que el modelo sea accesible.")

        st.markdown("---")
        st.header("8. Exportar Matriz a Word")
        st.write("Una vez que estés satisfecho con tu matriz, puedes exportarla a un documento de Word.")

        if st.button("Generar Documento Word 📄"):
            all_data = {key: st.session_state.get(key, '') for key in init_session_state.__defaults__[0].keys()} # Recopilar todos los datos
            word_doc_bytes = generate_word_doc(all_data)
            st.download_button(
                label="Descargar Matriz.docx",
                data=word_doc_bytes,
                file_name="matriz_investigacion.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            )

    else:
        st.warning("Por favor, selecciona primero el 'Tipo de Investigación' para continuar con el resto de la matriz.")


if __name__ == "__main__":
    main()
