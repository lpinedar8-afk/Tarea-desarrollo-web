require("dotenv").config();
const express = require("express");
const cors = require("cors");
const app = express();
app.disable("x-powered-by");
app.use(express.json({
  limit: "10kb"
}));
const PORT = Number(process.env.PORT || 3000);
const NODE_ENV = process.env.NODE_ENV || "development";

//configuración de CORS
if (process.env.FRONTEND_URL) {
  app.use(cors({
    origin: process.env.FRONTEND_URL,
    methods: ["GET", "POST"],
    allowedHeaders: ["Content-Type"]
  }));
}

//endpoint de bienvenida
app.get("/", (req, res) => {
  res.json({
    mensaje: "Bienvenido a la API, version 2.1 (Produccion)",
    entorno: NODE_ENV
  });
});

//endpoint de salud
app.get("/health", (req, res) => {
  res.status(200).json({
    status: "ok",
    servicio: "API Desarrollo Web",
    timestamp: new Date().toISOString()
  });
});

const productos = [
  { id: 1, nombre: "Teclado", precio: 250 },
  { id: 2, nombre: "Mouse", precio: 125 }
];

//endpoint obtener productos
app.get("/api/productos", (req, res) => {
  res.status(200).json(productos);
});

//endpoint obtener producto por ID
app.get("/api/productos/:id", (req, res) => {
  const id = parseInt(req.params.id, 10);
  const producto = productos.find(p => p.id === id);
  if (!producto) {
    return res.status(404).json({
      error: "Producto no encontrado"
    });
  }
  res.status(200).json(producto);
});

//validación de solicitudes
app.post("/api/productos", (req, res) => {
  const { nombre, precio } = req.body || {};
  if (
    typeof nombre != "string" || !nombre.trim() ||
    typeof precio != "number" || !Number.isFinite(precio) ||
    precio <= 0
  ) {
    return res.status(400).json({
      error: "Datos de producto inválidos"
    });
  }
  res.status(201).json({
    mensaje: "Solicitud de creación validada",
    producto: { nombre: nombre.trim(), precio },
    persistido: false
  });
});

//Ruta no encontrada
app.use((req, res) => {
  res.status(404).json({
    error: "Ruta no encontrada"
  });
});

//middleware central
app.use((err, req, res, next) => {
  console.error("Error", err.message);
  res.status(err.status || 500).json({
    error: "Error procesando la solicitud"
  });
});

//escuchar en todas las interfaces de red
app.listen(PORT, "0.0.0.0", () => {
  console.log(
    `API ejecutandose en el puerto ${PORT}`
  );
});
