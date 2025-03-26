# reportes/reportes_html.py (mejorado con Bootstrap)

import os
from datetime import datetime

class ReporteHTML:

    @staticmethod
    def generar_reporte_punto(punto, nombre_archivo="reporte_atencion"):
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        html = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Reporte de Atención</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body class="bg-light">
    <div class="container mt-5 mb-5">
        <h1 class="mb-4 text-center text-primary">Reporte de Atención</h1>
        <div class="mb-4">
            <h3 class="text-secondary">Punto: {punto.nombre}</h3>
            <p><strong>Fecha y hora:</strong> {now}</p>
        </div>

        <h4 class="mt-4">Estadísticas Generales</h4>
        <table class="table table-bordered table-hover table-sm">
            <tbody>
                <tr><th>Clientes Atendidos</th><td>{punto.clientes_atendidos}</td></tr>
                <tr><th>Tiempo Promedio de Espera</th><td>{round(punto.estadisticas()['espera']['promedio'], 2)} min</td></tr>
                <tr><th>Tiempo Máximo de Espera</th><td>{punto.estadisticas()['espera']['max']} min</td></tr>
                <tr><th>Tiempo Mínimo de Espera</th><td>{punto.estadisticas()['espera']['min']} min</td></tr>
                <tr><th>Tiempo Promedio de Atención</th><td>{round(punto.estadisticas()['atencion']['promedio'], 2)} min</td></tr>
                <tr><th>Tiempo Máximo de Atención</th><td>{punto.estadisticas()['atencion']['max']} min</td></tr>
                <tr><th>Tiempo Mínimo de Atención</th><td>{punto.estadisticas()['atencion']['min']} min</td></tr>
            </tbody>
        </table>

        <h4 class="mt-5">Escritorios Activos</h4>
        <table class="table table-striped table-bordered table-hover table-sm">
            <thead class="table-dark">
                <tr>
                    <th>Identificación</th>
                    <th>Encargado</th>
                    <th>Clientes Atendidos</th>
                    <th>Promedio</th>
                    <th>Máximo</th>
                    <th>Mínimo</th>
                </tr>
            </thead>
            <tbody>"""

        for esc in punto.escritorios.recorrer_adelante():
            if esc.clientes_atendidos == 0:
                continue
            html += f"""
                <tr>
                    <td>{esc.identificacion}</td>
                    <td>{esc.encargado}</td>
                    <td>{esc.clientes_atendidos}</td>
                    <td>{round(esc.promedio_atencion(), 2)} min</td>
                    <td>{esc.max_tiempo} min</td>
                    <td>{esc.min_tiempo} min</td>
                </tr>"""

        html += """
            </tbody>
        </table>
    </div>
</body>
</html>
"""

        os.makedirs("reportes", exist_ok=True)
        ruta = f"reportes/{nombre_archivo}.html"
        with open(ruta, "w", encoding="utf-8") as f:
            f.write(html)

        print(f"Reporte generado en: {ruta}")
