# ABD_Proyecto1
---
# Requisitos de Ejecución  

Para el funcionamiento de la solución se debe garantizar lo siguiente requisitos: 
* Tener instalado el intérprete de Python 3 (Realizado en 3.14.3). 
Contar con las librerías: 
* Streamlit (pip install streamlit streamlit). 
* Pyodbc (pip install streamlit pyodbc). 
* El servidor de Base de Datos debe estar activo y funcional. 
* Configurar correctamente las variables globales de conexión. 
* Se deben suministrar los datos relativos a un usuario con acceso total a la base 
de datos.  

---

# Arquitectura 

El elemento principal de la solución es la clase “queryEngine” la cual actúa de interfaz 
entre el servidor de base de datos y la lógica propia de la solución. Esta conexión está 
regida por un conjunto de variables globales presentes en la cabecera del código 
fuente de la solución.  
Una vez establecida la conexión, el usuario decide que consulta desea realizar, vía 
interfaz, y se crea un cursor que permite recorrer los registros obtenidos.  
En el caso específico de la consulta relativa a los tiempos de acceso a disco, la interfaz 
ofrece un selector de tabla y campo para la respuesta específica.

---

# Autores 
Creado por Oriana Arellano, Bárbara Ravelo y Bryan Silva para la Catedra de Administracion de Base de Datos
En la universidad Central de Venezuela.