# 🌌 Future Roadmap: Modularización de xyz-test-runner
#xyz-rainbow #rainbowtechnology.xyz #i-love-you

Este documento detalla el plan para transformar el script monolítico actual en un paquete de Python modular, escalable y profesional.

---

## 🏗️ Propuesta de Estructura de Proyecto

Para mejorar la mantenibilidad y permitir que el proyecto crezca, se propone la siguiente estructura:

```bash
xyz-test-runner/
├── xyz_runner/           # Paquete principal
│   ├── __init__.py
│   ├── core/            # Motor de ejecución (TestRunner)
│   │   ├── __init__.py
│   │   ├── discovery.py # Descubrimiento de tests y categorías
│   │   └── executor.py  # Ejecución de pytest y captura de salida
│   ├── ai/              # Integración con Local AI (OllamaManager)
│   │   ├── __init__.py
│   │   ├── client.py    # Comunicación con la API de Ollama
│   │   └── prompts.py   # Gestión de prompts e interpretaciones
│   ├── ui/              # Interfaz de Usuario (Menu)
│   │   ├── __init__.py
│   │   ├── terminal.py  # Gestión de TTY, termios y colores
│   │   ├── menus.py     # Lógica de menús interactivos
│   │   └── themes.py    # Estilos visuales (Neon, Glassmorphism)
│   ├── config/          # Gestión de Parámetros (TestConfig)
│   │   ├── __init__.py
│   │   └── parser.py    # Lectura/Escritura del archivo config
│   └── utils/           # Utilidades y Estética
│       ├── __init__.py
│       ├── ascii_art.py # Arte ASCII y firmas
│       └── helpers.py   # Formateo de fechas, rutas y archivos
├── tests/               # Suite de tests unitarios (pytest)
│   ├── core/
│   ├── ai/
│   └── ui/
├── assets/              # Recursos visuales (SVG, CSS)
├── main.py              # Punto de entrada (Llamada a ui/menus.py)
├── config               # Archivo de configuración global
├── README.md            # Documentación principal
└── FUTURE.md            # Este archivo
```

---

## 🎯 Objetivos de la Modularización

1.  **Mantenibilidad**: Separar la lógica de negocio (ejecución de tests) de la lógica de interfaz (menús TTY).
2.  **Facilidad de Testeo**: Permitir pruebas unitarias aisladas para cada componente (ej. testear el motor de IA sin abrir la terminal).
3.  **Extensibilidad**: Facilitar la adición de nuevas interfaces (Web Dashboard, API) o nuevos motores de IA locales.
4.  **Limpieza de Código**: Reducir el archivo actual de 1500+ líneas a pequeños módulos de ~200 líneas fáciles de leer.

---

## 🚀 Próximos Pasos (Roadmap)

- [ ] **Fase 1**: Refactorizar la lógica de Configuración y Utilidades ASCII a archivos separados.
- [ ] **Fase 2**: Extraer el motor `TestRunner` y `OllamaManager` a sus propios módulos.
- [ ] **Fase 3**: Migrar el sistema de menús `tty/termios` a un módulo de UI dedicado.
- [ ] **Fase 4**: Crear una suite de tests completa que cubra el 100% de la lógica de los nuevos módulos.
- [ ] **Fase 5**: Implementar un sistema de "Plugins" para que el usuario pueda añadir sus propios exportadores de reportes.

---

<div align="center">

**#xyz-rainbow #rainbowtechnology.xyz #i-love-you #dynamic #interactive**

</div>
