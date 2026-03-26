# 📊 Bitácora de Desarrollo: Potros Sports (Versión conFerro)

## 📅 Estado Actual: 25 de marzo de 2026
**Objetivo:** Crear una versión de pruebas (Staging) mejorada antes de actualizar la plataforma principal en Render.

### ✅ Mejoras Implementadas (en conFerro/app.py):
1. **Sincronización Robusta:** Añadida función `safe_link` para manejar registros vacíos en Airtable (evita errores en radar de perfil).
2. **Gestión de Staff:** Habilitada la visualización y edición de PINs de entrenadores desde el panel de administración.
3. **Manejo de Errores:** Mejorada la respuesta de la API para mostrar errores específicos de conexión en lugar de mensajes genéricos.
4. **Seguridad:** Configuración de variables de entorno para producción.
5. **Login de Staff:** Añadido campo de "Nombre de Usuario" obligatorio junto al PIN para mejorar la seguridad del acceso técnico.

### 🚀 Infraestructura de Pruebas:
* **Repositorio GitHub:** `https://github.com/luisfelipegillopez-svg/potros-pruebas-` (Ya sincronizado con el código mejorado).
* **Despliegue Automático:** Creado archivo `render.yaml` (Blueprint) para facilitar la subida a Render con un solo clic.
* **Servidor Local:** Configurado en el puerto 5000 para pruebas en tiempo real.

### ⚠️ Restricciones de Desarrollo Obligatorias:
* **Integridad Técnica:** Ningún cambio nuevo puede comprometer o "dañar" las funciones que ya están operativas. 
* **Prioridad IA:** Las funciones de generación de planes de **IA de Cancha** y de **IA Física** deben mantenerse 100% funcionales en todo momento tras cualquier actualización.
* **Validación:** Antes de cada despliegue, se debe verificar que la comunicación con la API de Gemini siga produciendo tablas HTML válidas.

### 📝 Próximos Pasos:
* Verificar el despliegue en la nueva URL de Render (`potros-pruebas`).
* Validar que la edición de PINs funcione correctamente en el panel "Gestión Staff".
* Una vez validado todo, clonar estas mejoras en el repositorio principal `potros-sports`.

---
*Nota: Este archivo se actualiza automáticamente tras cada mejora importante.*
