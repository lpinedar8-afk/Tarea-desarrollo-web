# API Productos - Laboratorio de Despliegue en Render

API REST construida con Express.js y desplegada en la nube utilizando **Render**.

## Requisitos
- Node.js (v18 o superior)
- npm

## Instalación
```bash
npm install
```

## Variables de Entorno
Crea un archivo `.env` basado en `.env.example`:
```env
PORT=3000
NODE_ENV=development
FRONTEND_URL=http://localhost:5173
```

## Ejecución Local
```bash
# Modo producción / estándar
npm start

# Modo desarrollo con auto-reload
npm run dev
```

## Endpoints Disponibles
- `GET /` - Bienvenida e información del entorno actual.
- `GET /health` - Estado de salud y timestamp del servicio.
- `GET /api/productos` - Listado de productos.
- `POST /api/productos` - Validación y simulación de registro de producto.
