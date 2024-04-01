document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('consultaForm');
    const resultadoDiv = document.getElementById('resultado');

    form.addEventListener('submit', function(event) {
        event.preventDefault();

        const edad = document.getElementById('edad').value;
        const estadoHp = document.getElementById('estadoHp').value;
        const ingresos = document.getElementById('ingresos').value;
        const deuda = document.getElementById('deuda').value;
        const cantidadActivos = document.getElementById('cantidadActivos').value;

        const data = {
            edad: edad,
            estadoHp: estadoHp,
            ingresos: ingresos,
            deuda: deuda,
            cantidadActivos: cantidadActivos
        };

        fetch('http://localhost:5000/consultar-credito', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        })
        .then(response => response.json())
        .then(data => {
            resultadoDiv.textContent = data.resultado;
        })
        .catch(error => {
            console.error('Error:', error);
        });
    });
});


function mostrarPopup() {
    document.getElementById("overlay").style.display = "block";
    document.getElementById("popup").style.display = "block";
  }

function mostrarPopup() {
    const edad = document.getElementById('edad').value;
    const estadoHp = document.getElementById('estadoHp').value;
    const ingresos = document.getElementById('ingresos').value;
    const deuda = document.getElementById('deuda').value;
    const cantidadActivos = document.getElementById('cantidadActivos').value;
    
    if (edad !== '' && estadoHp !== '' && ingresos !== '' && deuda !== '' && cantidadActivos !== '') {
      document.getElementById("overlay").style.display = "block";
      document.getElementById("popup").style.display = "block";
    }
}
  
function cerrarPopup() {
    document.getElementById("overlay").style.display = "none";
    document.getElementById("popup").style.display = "none";
}