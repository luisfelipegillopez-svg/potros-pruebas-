# Potros Sports - Elite Management

Sistema integral de gestión deportiva diseñado para el club **Corp. Potros**. Esta aplicación permite a entrenadores y administradores gestionar nóminas de atletas, evaluaciones físicas, planes de entrenamiento táctico y asistencia, todo potenciado por Inteligencia Artificial (Google Gemini).

## 🚀 Tecnologías Principales
- **Frontend:** HTML5, Tailwind CSS (v3 CDN), JavaScript Vanila.
- **Gráficos:** Chart.js (Radares de potencial élite).
- **Backend:** Google Apps Script (Proxy para persistencia de datos).
- **IA:** Google Gemini API (Generación de rutinas y planes tácticos).

## 🛠️ Estructura del Proyecto
- `index.html`: Archivo único que contiene toda la lógica (SPA), estilos y estructura.
- **Sistema de Roles:**
  - `Public`: Vista de solo lectura.
  - `Coach`: Acceso a creación de sesiones, toma de asistencia y edición de atletas.
  - `Super Admin`: Acceso total, incluyendo gestión de cuentas de entrenadores y respaldos de base de datos.

## 🔑 Credenciales y Seguridad
- **Master PIN:** `Fg050522` (Acceso Super Admin).
- **Entrenadores:** Se identifican mediante PINs creados en el panel de registro.
- **Sesiones:** Se gestionan mediante `sessionStorage`.

## 📋 Comandos de Desarrollo
Este proyecto es una aplicación estática de un solo archivo.
- **Ejecución:** Abrir `index.html` en cualquier navegador moderno.
- **Sincronización:** Los datos se guardan automáticamente en la nube a través de la URL de script configurada en `window.app.scriptURL`.

## 📐 Convenciones de Desarrollo
- **Vistas:** El cambio de pantallas se gestiona mediante la clase `.view` y el método `window.app.showView()`.
- **Datos:** Todos los métodos de manipulación de datos deben llamar a `window.app.save()` para persistir los cambios en la nube.
- **IA:** Las llamadas a la IA deben pasar por `window.app.fetchGeminiData()` para asegurar el manejo de errores y estados de carga.
