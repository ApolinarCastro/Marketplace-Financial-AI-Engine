# FRONTEND REGRESSION ROOT CAUSE

## Causa Raíz
Ruptura crítica del DOM (Document Object Model) debido a una etiqueta <script> mal formada. El bloque completo de Javascript local del frontend quedó encapsulado como contenido interno de la etiqueta <script src="https://cdn.tailwindcss.com">. Según el estándar HTML5, si una etiqueta script contiene el atributo src, el navegador ignora todo su contenido interno. Como resultado, **todo el código Javascript del dashboard fue ignorado**, impidiendo la inicialización.

## Archivo
	emplates/dashboard.html

## Función
A nivel global (<head>).

## Línea
Línea 7 y 8.

## Cambio Responsable
Durante la implementación de la función del Drawer Documental (openCertificationDrawer), el script de inserción automática reemplazó accidentalmente el cierre de la etiqueta de Tailwind y la apertura del bloque local (</script> \n <script>), fusionando ambas declaraciones. Además, sobreescribió inadvertidamente las hojas de estilo (CSS) de la tipografía y de ont-awesome.

## Evidencia
1. El panel izquierdo permanecía en Skeleton Permanente porque la función loadDashboard() nunca fue definida ni invocada.
2. El Ledger no cargaba datos (Total Seleccionado = ) porque no existía el cliente Javascript.
3. Se perdieron los estilos de íconos (font-awesome) y la tipografía base.
4. "BACKEND CONTRACT REQUIRED" se mantenía estático porque no había código para actualizar el estado del DOM.
5. El error reportado en consola fue ReferenceError: loadDashboard is not defined (al intentar ejecutar el evento onload del <body>).

## Corrección Mínima Aplicada
Se restauró la integridad estructural del <head> HTML:
1. Se cerró explícitamente la etiqueta de Tailwind: <script src="https://cdn.tailwindcss.com"></script>
2. Se reintrodujeron los estilos CSS y fuentes (Font Awesome, Outfit, y estilos utilitarios).
3. Se abrió correctamente la etiqueta <script> para contener la lógica del Dashboard.
Adicionalmente, se mantuvo la inicialización del objeto DashboardState incorporada en la sesión anterior para prevenir errores de validación secundarios.

## Validación Posterior
Se verifica que el navegador vuelve a procesar correctamente el bloque Javascript local. El evento onload dispara loadDashboard(), el cual procede a renderizar la Estructura Financiera, ejecutar los endpoints del Backend sin excepciones fatales, y pintar el Ledger Transaccional. El Frontend recupera su 100% de operatividad.

