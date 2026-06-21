import pyodbc
import json
import streamlit as st

#Run: streamlit run "src/queryEngine.py"

#Global Variables
SERVER = "localhost"
DATABASE = "StreamUCV"
USERNAME = "sa"
PASSWORD = "Cyber2026*"
DRIVER = "ODBC Driver 17 for SQL Server"
QUERIES_PATH = "queries/mainQueries.json"
st.set_page_config(
    page_title="Proyecto ABD - StreamUCV",
    layout="wide")

#Main Controller
class MainController():
    #Query Loader
    @staticmethod
    @st.cache_data
    def queryLoader(path: str) -> dict:
        try:
            with open(path, 'r', encoding='utf-8') as file:
                return json.load(file)
        except FileNotFoundError as e:
            print(f"Error: {e}")
            return {}
        except json.JSONDecodeError as e:
            print(f"Error: {e}")
            return {}
    #Query Master
    @staticmethod
    def makeQuery(conexion: pyodbc.Connection, query: str):
        if conexion is None: return None, None
        cursor = conexion.cursor()
        try:
            cursor.execute(query)
            colsNames = [col[0] for col in cursor.description]
            rows = cursor.fetchall()
            return colsNames, rows
        except pyodbc.Error as e:
            print(f"Error: {e}")
            return None, None
        finally:
            cursor.close()
    #Main Connector
    @staticmethod
    @st.cache_resource
    def connectToDB() -> pyodbc.Connection | None:
        connectionData = (
            f"DRIVER={{{DRIVER}}};"
            f"SERVER={SERVER};"
            f"DATABASE={DATABASE};"
            f"UID={USERNAME};"
            f"PWD={PASSWORD};"
        )
        try: 
            return pyodbc.connect(connectionData)
        except pyodbc.Error as e:
            print(f"Error: {e}")
            return None
        
#Interfaz en Streamlit
app = MainController()
queries = app.queryLoader(QUERIES_PATH)
#Main Panel
with st.sidebar:
    st.title("StreamUCV")
    st.markdown("---")
    options = list(queries.keys()) if queries else ["Sin datos"]
    actualSelection = st.selectbox("Seleccionar Requerimiento:", options)
    st.markdown("---")
    exec = st.button("Consultar", type="primary", use_container_width=True)
#Central Panel
if queries and actualSelection in queries:
    st.header(f"Query {actualSelection}")
    req_data = queries[actualSelection]
    st.info(req_data.get("desc", "Sin descripción disponible."))
    if actualSelection == "10":
        st.write("### Parámetros de Simulación de Costos")
        col1, col2 = st.columns(2)
        with col1:
            tableInput = st.text_input("Tabla a consultar").strip()
        with col2:
            colInput = st.text_input("Columna a filtrar").strip()
    if exec:
        querySQL = req_data.get("query", "")
        with st.spinner("Consultando al Diccionario de Datos..."):
            conexion = app.connectToDB()
            if conexion:
                colNames, rows = app.makeQuery(conexion, querySQL)
                if colNames and rows:
                    cleanData = [dict(zip(colNames, row)) for row in rows]
                    st.success("Consulta ejecutada con éxito")
                    if actualSelection == "10" and tableInput and colInput:
                        filteredRow = None
                        for row in cleanData:
                            dbTabla = row.get("Tabla", "")
                            dbColumna = row.get("Columna", "")
                            if dbTabla == tableInput and dbColumna == colInput:
                                filteredRow = row
                                break
                        if filteredRow:
                            hashIndex = filteredRow.get("Tiene_Indice")
                            pages = filteredRow.get("Paginas_Tabla", 0)
                            time = filteredRow.get("Tiempo", 0)
                            numAccess = 3 if hashIndex == 'SI' else pages
                            operation = "Index Seek" if hashIndex == 'SI' else "Full Table Scan"
                            st.markdown("---")
                            st.subheader(f"Análisis de Rendimiento: {tableInput}.{colInput}")
                            st.write(f"**Estrategia de Ejecución:** {operation}")
                            m1, m2, m3 = st.columns(3)
                            m1.metric("Tiene Índice", hashIndex)
                            m2.metric("Accesos a Disco Físico", f"{numAccess} Páginas")
                            m3.metric("Tiempo de Ejecución Estimado", f"{float(time):.4f} ms")
                            st.markdown("---")
                            st.write("Datos en crudo del Diccionario de Datos:")
                        else:
                            st.warning(f"El filtro no encontró coincidencia.")
                    st.dataframe(cleanData, use_container_width=True)
                else:
                    st.warning("La consulta no devolvió resultados.")