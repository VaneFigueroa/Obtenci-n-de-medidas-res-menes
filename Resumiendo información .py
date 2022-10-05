#!/usr/bin/env python
# coding: utf-8

# ## Obtención de medidas resúmenes

# Con SQL podemos ejecutar cálculos que resuman los datos para responder preguntas comerciales. Emplearemos las funciones agregadas más comunes que se utilizan para resumir la información almacenada en tablas: AVG(), COUNT(), MAX(), MIN() y SUM(). También, resumiremos subconjuntos de datos en una misma consulta, usando la cláusula "GROUP BY" y  consultaremos subconjuntos de grupos agregados con la cláusula HAVING. Revisamos problemas de desajustes de agregación.
# 
# 
# Además, emplearemos la función lógica ISNULL(), la función TIMESTAMPDIF() para obtener una nueva medida de duración de tiempo y la función MONTH() para obtener el mes de una entreda de fecha.

# COUNT es la única función agregada que puede funcionar en cualquier tipo de variable. Las otras cuatro funciones agregadas solo son apropiadas para datos numéricos. 
# Todas las funciones agregadas requieren que ingrese un nombre de columna o un "*" entre paréntesis después de la palabra de función.

# In[1]:


get_ipython().run_line_magic('load_ext', 'sql')


# In[2]:


get_ipython().run_line_magic('sql', 'mysql://studentuser:studentpw@localhost/dognitiondb')


# La interfaz de Jupyter nos dice convenientemente cuántas filas hay en la salida de una consulta. Comparamos los resultados de la función COUNT con los resultados de salida de función SELECT.

# In[3]:


get_ipython().run_cell_magic('sql', '', 'SELECT breed\nFROM dogs;')


# Jupyter dice que 35050 filas están "afectadas", lo que significa que este es el número de filas en el resultado de la consulta. Ahora, con COUNT obtendremos cuántas filas hay en total en la columna de raza, y vemos que llegamos al mismo resultado que el Jupyter sin mostrar las filas reales de datos que se agregan.

# In[4]:


get_ipython().run_cell_magic('sql', '', 'SELECT COUNT(breed) \nFROM dogs;')


# Se puede usar DISTINCT con COUNT para contar todos los valores únicos en una columna, pero debe colocarse entre paréntesis, inmediatamente antes de la columna que se está contando. Por ejemplo, para contar el número de nombres de razas distintos contenidos en las entradas de la columna de raza:

# In[3]:


get_ipython().run_cell_magic('sql', '', 'SELECT COUNT(DISTINCT breed)\n  FROM dogs;')


# Cuando se incluye una columna entre paréntesis, los valores nulos se ignoran automáticamente, en esta salida obtenemos los valores únicos, no nulos de columna de raza.  

# Se puede usar "\*" entre paréntesis en una función COUNT para contar cuántas filas hay en la tabla completa (o subtabla). Sin embargo, existen dos diferencias con COUNT(column_name). La primera diferencia es que no se puede usar DISTINCT con COUNT(\*), en este caso, se contará todas las filas de la tabla. La segunda diferencia, es que con COUNT(\*) se considera los valores nulos de las filas de la tabla.

# Obtenemos de la consulta de COUNT(\*) de la tabla dogs, 35050 filas. Posteriormente, exlcuimos los valores nulos de la columna user_guid. Este último resultado, lo podemos obtener con COUNT(\*) y WHERE, o bien con COUNT(user_guid) para considerar los valores no nulos de esta columna. 

# In[6]:


get_ipython().run_cell_magic('sql', '', 'SELECT COUNT(*)\nFROM dogs;')


# In[7]:


get_ipython().run_cell_magic('sql', '', 'SELECT COUNT(*)\nFROM dogs\nWHERE user_guid IS NOT NULL;')


# In[8]:


get_ipython().run_cell_magic('sql', '', 'SELECT COUNT(user_guid)\nFROM dogs;')


# Combinamos COUNT con una cláusula WHERE para averiguar cuántos perros individuales completaron las pruebas después del 1 de marzo de 2014. 

# In[9]:


get_ipython().run_cell_magic('sql', '', 'SELECT COUNT(DISTINCT dog_guid)\nFROM complete_tests\nWHERE created_at>"2014_03_01"; ')


# Queremos saber cuántos nombres de exámenes posibles hay en la tabla exam_answers:

# In[10]:


get_ipython().run_cell_magic('sql', '', 'SELECT COUNT(DISTINCT test_name)\nFROM exam_answers; ')


# ISNULL es una función lógica que devuelve un 1 para cada fila que tiene un valor NULL en la columna especificada y un 0 para todo lo demás. Si sumamos la cantidad de 1 generados por ISNULL()con la función SUM(), obtenemos la cantidad total de valores NULL de la columna.

# In[11]:


get_ipython().run_cell_magic('sql', '', 'SELECT SUM(ISNULL(user_guid))\nFROM dogs;')


# La salida debe devolver un valor de 2. Cuando agregamos este número a las 35048 entradas que se obtuvimos de extraer los user_guid no nulos de la tabla dogs, llegamos al total de 35 050, que es la cantidad de filas reportadas por SELECT COUNT(*) de dogs.

# Podríamos recuperar la calificación promedio, mínima y máxima que los clientes dieron en la prueba de "Eye Contact Game":

# In[12]:


get_ipython().run_cell_magic('sql', '', 'SELECT test_name, \nAVG(rating) AS AVG_Rating, \nMIN(rating) AS MIN_Rating, \nMAX(rating) AS MAX_Rating\nFROM reviews\nWHERE test_name="Eye Contact Game";')


# Si quisiera la calificación promedio para cada una de las 40 pruebas en la tabla de reviews. Una forma de hacerlo, es escribir 40 consultas separadas como la anterior para cada prueba y luego copiar o transcribir los resultados en una tabla separada en otro programa como Excel para reunir todos los resultados en un sólo lugar. Esto sería una tarea muy tediosa y lenta. Afortunadamente, existe una forma más sencilla de producir los resultados que se desea en una sola consulta. El método para hacer esto es incluir una cláusula "GROUP BY". 
# 
# La cláusula GROUP BY viene después de la cláusula WHERE, pero antes de ORDER BY o LIMIT. Esta consulta generará la calificación promedio para cada prueba. Más técnicamente, esta consulta le indicará a MySQL que promedie todas las filas que tienen el mismo valor en la columna test_name. Como regla general sólida, si se agrupa por una columna, también se debe incluir esa columna en la instrucción SELECT para indicar a MySQL a qué grupo corresponde cada fila de la salida. Para ver esto, corremos ambas consultas:
# 

# In[13]:


get_ipython().run_cell_magic('sql', '', 'SELECT test_name, AVG(rating) AS AVG_Rating\nFROM reviews\nGROUP BY test_name;')


# In[3]:


get_ipython().run_cell_magic('sql', '', 'SELECT AVG(rating) AS AVG_RATING\nFROM reviews\nGROUP BY test_name\nLIMIT 5;')


# Necesitamos consultar cuánto tiempo tomó completar cada prueba proporcionada en la tabla exam_answers, en minutos. Usamos la función TIMESTAMPDIFF() para obtener una nueva medida de duración de tiempo. En el siguiente enlace, encontramos detalles de la función y otras funciones útiles: http://www.w3resource.com/mysql/date-and-time-functions/date-and-time-functions.php

# In[18]:


get_ipython().run_cell_magic('sql', '', 'SELECT TIMESTAMPDIFF(minute,start_time,end_time) AS Duration\nFROM exam_answers\nLIMIT 10;')


# Si explora su salida, encontrará que algunas de sus duraciones calculadas parecen ser "0". En algunos casos, verá muchas entradas del mismo Dog_ID con la misma hora de inicio y hora de finalización. Eso debería ser imposible. Este tipo de entradas probablemente representan pruebas realizadas por el equipo, en lugar de datos reales de clientes. Sin embargo, en otros casos, se ingresa un "0" en la columna Duración, aunque la hora de inicio y la hora de finalización sean diferentes. Esto se debe a que le indicamos a la función que emita la diferencia de tiempo en minutos; a menos que cambie su configuración, generará "0" para cualquier diferencia de tiempo menor que el número entero 1. Si cambia su función para generar la diferencia de tiempo en segundos, la duración en la mayoría de estas columnas tendrá un número distinto de cero.

# In[19]:


get_ipython().run_cell_magic('sql', '', 'SELECT TIMESTAMPDIFF(second,start_time,end_time) AS Duration\nFROM exam_answers\nLIMIT 10;')


# Si queremos la cantidad de tiempo promedio (en minutos) que les tomó a los clientes completar todas las pruebas en la tabla exam_answers:

# In[20]:


get_ipython().run_cell_magic('sql', '', 'SELECT AVG(TIMESTAMPDIFF(minute,start_time,end_time)) AS AvgDuration\nFROM exam_answers;')


# El tiempo promedio que les llevó a los clientes completar la prueba "Eye Contact Game":

# In[21]:


get_ipython().run_cell_magic('sql', '', 'SELECT AVG(TIMESTAMPDIFF(minute,start_time,end_time)) AS AvgDuration\nFROM exam_answers\nWHERE test_name="Eye Contact Game";')


# Averiguamos cuál es el valor mínimo y máximo en la nueva columna de duración, se incluye los datos de toda la tabla:

# In[24]:


get_ipython().run_cell_magic('sql', '', 'SELECT MIN(TIMESTAMPDIFF(minute,start_time,end_time)) AS MinDuration, \n       MAX(TIMESTAMPDIFF(minute,start_time,end_time)) AS MaxDuration\nFROM exam_answers;')


# El valor mínimo de Duración es negativo, esto dado que las horas finales ingresadas son anteriores a las horas iniciales. Estas entradas deben ser errores, queremos saber a cuántas entradas corresponde:

# In[26]:


get_ipython().run_cell_magic('sql', '', 'SELECT COUNT(TIMESTAMPDIFF(minute,start_time,end_time)) AS ErrorDuration\nFROM exam_answers\nWHERE TIMESTAMPDIFF(minute,start_time,end_time)<0; ')


# Para poder examinar estas 620 filas y averiguar si comparten alguna característica que pueda brindar pistas sobre la causa del error de entrada, realizamos la siguiente consulta: 

# In[27]:


get_ipython().run_cell_magic('sql', '', 'SELECT *\nFROM exam_answers\nWHERE TIMESTAMPDIFF(minute,start_time,end_time)<0; ')


# Averiguamos cuántas pruebas se completaron durante cada mes del año, para ello usamos la función MONTH(), que devolverá un número que representa el mes de una entrada de fecha. Para obtener el número total de pruebas completadas cada mes, puede colocar la función MONTH en la cláusula GROUP BY, en este caso a través de un alias:

# In[15]:


get_ipython().run_cell_magic('sql', '', 'SELECT test_name, MONTH(created_at) AS Month, COUNT(created_at) AS Num_Completed_Tests\nFROM complete_tests\nGROUP BY Month;')


# También se puede agrupar por varias columnas o campos derivados. Si quisiéramos determinar el número total de cada tipo de prueba completada cada mes, podríamos incluir tanto "test_name" como el campo "Mes" derivado en la cláusula GROUP BY, separados por una coma. MySQL le permite usar alias en una cláusula GROUP BY, pero algunos sistemas de bases de datos no lo permiten.

# In[16]:


get_ipython().run_cell_magic('sql', '', 'SELECT test_name, MONTH(created_at) AS Month, COUNT(created_at) AS Num_Completed_Tests\nFROM complete_tests\nGROUP BY test_name, Month;')


# Si está utilizando un sistema de base de datos que NO acepta alias en cláusulas GROUP BY, aún se puede agrupar por campos derivados, pero debe duplicar el cálculo para el campo derivado en la cláusula GROUP BY además de incluir el campo derivado en el Cláusula SELECT:
# 

# In[17]:


get_ipython().run_cell_magic('sql', '', 'SELECT test_name, MONTH(created_at) AS Month, COUNT(created_at) AS Num_Completed_Tests\nFROM complete_tests\nGROUP BY test_name, MONTH(created_at);')


# Para asegurarnos de que la salida se ordene de la manera que se desea, agreguemos una cláusula ORDER BY:

# In[4]:


get_ipython().run_cell_magic('sql', '', 'SELECT test_name, MONTH(created_at) AS Month, COUNT(created_at) AS Num_Completed_Tests\nFROM complete_tests\nGROUP BY test_name, Month\nORDER BY test_name ASC, Month ASC;')


# Se puede abreviar la consulta anterior asignando a cada campo en su instrucción SELECT un número de acuerdo con el orden en que aparece y empleando estos en las cláusulas siguientes: 

# In[ ]:


get_ipython().run_cell_magic('sql', '', 'SELECT test_name, MONTH(created_at) AS Month, COUNT(created_at) AS Num_Completed_Tests\nFROM complete_tests\nGROUP BY 1, 2\nORDER BY 1 ASC, 2 ASC;')


# Al igual que se puede consultar subconjuntos de filas con la cláusula WHERE, se puede consultar subconjuntos de grupos agregados con la cláusula HAVING. Sin embargo, mientras que la expresión que sigue a una cláusula WHERE tiene que ser aplicable a cada fila de datos en una columna, la expresión que sigue a una cláusula HAVING tiene que ser aplicable o computable utilizando un grupo de datos.
# 
# Si queremos examinar la cantidad de pruebas completadas solo durante los meses de noviembre y diciembre, usaremos la cláusula WHERE:

# In[ ]:


get_ipython().run_cell_magic('sql', '', 'SELECT test_name, MONTH(created_at) AS Month, COUNT(created_at) AS Num_Completed_Tests\nFROM complete_tests\nWHERE MONTH(created_at)=11 OR MONTH(created_at)=12\nGROUP BY 1, 2\nORDER BY 3 DESC\nLIMIT 5;')


# Usamos la cláusula HAVING para considerar solo los pares de meses de prueba que tuvieran al menos 20 registros porque la estipulación de al menos 20 registros se computa en el nivel de grupo agregado:

# In[4]:


get_ipython().run_cell_magic('sql', '', 'SELECT test_name, MONTH(created_at) AS Month, COUNT(created_at) AS Num_Completed_Tests\nFROM complete_tests\nWHERE MONTH(created_at)=11 OR MONTH(created_at)=12\nGROUP BY 1, 2\nHAVING COUNT(created_at)>=20\nORDER BY 3 DESC;')


# Queremos el número total de User_Guids únicos en cada combinación de estado y código postal en los Estados Unidos que tengan al menos 5 usuarios, ordenados primero por nombre de estado en orden alfabético ascendente y segundo por el número total de User_Guids únicos en orden descendente. 

# In[ ]:


get_ipython().run_cell_magic('sql', '', 'SELECT state, zip, COUNT(DISTINCT user_guid) AS Num_Users\nFROM users\nWHERE country="US"\nGROUP BY state, zip\nHAVING Num_Users>=5 \nORDER BY state ASC, Num_Users DESC; ')


# Las consultas agrupadas pueden causar problemas de discrepancias de agregación en las medidas. A veces, no son fáciles de 
# detectar estos inconvenientes porque la consulta se ejecuta sin mensajes de errores. 
# 
# Por ejemplo, queremos recuperar el número de dog_guids únicos asociados con el tipo de raza y su peso. Cuando intentemos escribir una consulta que refleje esa solicitud, debemos tener en cuenta que la cantidad de dog_guids únicos es un solo número para cada id, mientras que la medida peso, no es una sola medida. Necesitamos que dog_guids y peso sean singulares o plurales, entonces, el peso debe agregarse o dog_guids y el peso considerarlos sin agregar. Es útil recordar que la salida de SQL siempre es una tabla. No es posible construir una tabla válida que tuviera columnas para recuentos agregados y medidas de peso individuales al mismo tiempo. Una opción es desagregar el conteo para que tenga una columna con dog_guids y otra columna con medidas de peso para cada dog_guid. La otra opción es agregar las medidas de peso para que tenga una columna con el recuento total de dog_guids y otra columna con la medida de peso promedio (o algún otro tipo de agregación resumida) para el grupo que representa el recuento. 
# 
# Vemos que si ignoramos esto, la consulta no tendrá sentido: 

# In[5]:


get_ipython().run_cell_magic('sql', '', 'SELECT breed_type, weight, COUNT(DISTINCT dog_guid) AS NumDogs\nFROM dogs\nGROUP BY breed_type;')


# Obtenemos valor cero para el campo de peso. MySQL completa la columna no agregada con el primer valor que encuentra en esa columna dentro del primer "grupo" de filas que está examinando. Otras bases de datos no le permitirán ejecutar las consultas descritas anteriormente. 
# 
# Para evitar un desajuste de agregación, debemos solicitar para cada tipo de raza de perro, la cantidad de Dog_Guids únicos que hay en la base de datos y el peso promedio de la raza_tipo.

# In[9]:


get_ipython().run_cell_magic('sql', '', 'SELECT COUNT(DISTINCT dog_guid), breed_type, AVG(weight) AS avg_weight \nFROM dogs\nGROUP BY breed_type;')


# Como regla general, todos los campos no agregados que aparecen en la lista SELECT deben aparecer en la lista GROUP BY. 

# El orden de las consultas SQL está destinado a reflejar la forma en que escribimos oraciones, pero en realidad se ejecutan en un orden diferente al que las escribimos. La imagen a continuación muestra el orden en que escribimos las consultas que se envían a la base de datos en la parte superior del embudo, y el orden en que la base de datos generalmente ejecuta las consultas en la cinta transportadora.
# 
# <img src="https://duke.box.com/shared/static/irmwu5o8qcx4ctapjt5h0bs4nsrii1cl.jpg" width=600 alt="ORDER" />
# 
# 
# Este diagrama le muestra que los datos se agrupan antes de que se apliquen las expresiones SELECT. Eso significa que cuando se incluye una expresión GROUP BY en una consulta SQL, no hay forma de usar una declaración SELECT para resumir datos que cruzan varios grupos. Por cierto, este diagrama también muestra por qué algunas plataformas y algunas consultas en algunas plataformas fallan cuando intenta usar alias o campos derivados en las cláusulas WHERE, GROUP BY o HAVING. Si la instrucción SELECT aún no se ha ejecutado, el alias o los campos derivados no estarán disponibles (como recordatorio, algunos sistemas de bases de datos, como MySQL, han encontrado formas de superar este problema). Por otro lado, SELECT se ejecuta antes que las cláusulas ORDER BY. Eso significa que la mayoría de los sistemas de bases de datos deberían poder usar alias y campos derivados en las cláusulas ORDER BY.
