class Calendario {
    constructor() {
        this.fecha = new Date();
        this.mesActual = this.fecha.getMonth();
        this.anioActual = this.fecha.getFullYear();
        this.eventos = {};
        
        this.inicializar();
        this.cargarEventos();
        
        // Ir al mes del próximo evento si existe
        this.irAProximoEvento();
    }

    inicializar() {
        this.prevBtn = document.getElementById('prevMonth');
        this.nextBtn = document.getElementById('nextMonth');
        this.monthYearElement = document.getElementById('monthYear');
        this.diasContainer = document.getElementById('dias');
        this.eventosLista = document.getElementById('eventos-lista');

        // Agregar botones para navegar años
        this.prevYearBtn = document.createElement('button');
        this.nextYearBtn = document.createElement('button');
        this.prevYearBtn.innerHTML = '&lt;&lt;';
        this.nextYearBtn.innerHTML = '&gt;&gt;';
        this.prevYearBtn.className = 'calendar-nav-btn';
        this.nextYearBtn.className = 'calendar-nav-btn';
        
        // Insertar botones junto a los existentes
        this.prevBtn.parentNode.insertBefore(this.prevYearBtn, this.prevBtn);
        this.nextBtn.parentNode.appendChild(this.nextYearBtn);

        this.prevYearBtn.addEventListener('click', () => this.cambiarAnio(-1));
        this.nextYearBtn.addEventListener('click', () => this.cambiarAnio(1));
        this.prevBtn.addEventListener('click', () => this.cambiarMes(-1));
        this.nextBtn.addEventListener('click', () => this.cambiarMes(1));

        this.renderizarCalendario();
    }

    cargarEventos() {
        // Eventos del calendario
        this.eventos = {
            '2025-04-04': [{
                titulo: 'Charla Motivacional',
                hora: '15:00',
                descripcion: 'Sesión de apoyo y motivación para solicitantes de asilo. Únete a nosotros para compartir experiencias y encontrar inspiración en el camino.'
            }]
        };
    }

    irAProximoEvento() {
        // Encontrar el próximo evento
        const fechaHoy = new Date();
        let proximoEvento = null;
        
        for (let fecha in this.eventos) {
            const fechaEvento = new Date(fecha);
            if (fechaEvento >= fechaHoy) {
                if (!proximoEvento || fechaEvento < new Date(proximoEvento)) {
                    proximoEvento = fecha;
                }
            }
        }
        
        if (proximoEvento) {
            const [anio, mes] = proximoEvento.split('-').map(num => parseInt(num));
            this.mesActual = mes - 1; // Ajustar porque los meses en JS son 0-based
            this.anioActual = anio;
            this.renderizarCalendario();
        }
    }

    cambiarAnio(delta) {
        this.anioActual += delta;
        this.renderizarCalendario();
    }

    cambiarMes(delta) {
        this.mesActual += delta;
        if (this.mesActual > 11) {
            this.mesActual = 0;
            this.anioActual++;
        } else if (this.mesActual < 0) {
            this.mesActual = 11;
            this.anioActual--;
        }
        this.renderizarCalendario();
    }

    renderizarCalendario() {
        const primerDia = new Date(this.anioActual, this.mesActual, 1);
        const ultimoDia = new Date(this.anioActual, this.mesActual + 1, 0);
        const meses = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 
                      'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'];

        this.monthYearElement.textContent = `${meses[this.mesActual]} ${this.anioActual}`;
        this.diasContainer.innerHTML = '';

        // Agregar días vacíos al inicio
        for (let i = 0; i < primerDia.getDay(); i++) {
            const diaVacio = document.createElement('div');
            diaVacio.className = 'dia vacio';
            this.diasContainer.appendChild(diaVacio);
        }

        // Agregar los días del mes
        for (let dia = 1; dia <= ultimoDia.getDate(); dia++) {
            const diaElement = document.createElement('div');
            diaElement.className = 'dia';
            diaElement.textContent = dia;

            const fechaStr = `${this.anioActual}-${String(this.mesActual + 1).padStart(2, '0')}-${String(dia).padStart(2, '0')}`;
            
            if (this.eventos[fechaStr]) {
                diaElement.classList.add('tiene-evento');
                diaElement.addEventListener('click', () => this.mostrarEventos(fechaStr));
            }

            this.diasContainer.appendChild(diaElement);
        }

        // Mostrar eventos del día actual si existen
        const hoy = new Date();
        if (this.mesActual === hoy.getMonth() && this.anioActual === hoy.getFullYear()) {
            const fechaHoyStr = `${this.anioActual}-${String(this.mesActual + 1).padStart(2, '0')}-${String(hoy.getDate()).padStart(2, '0')}`;
            if (this.eventos[fechaHoyStr]) {
                this.mostrarEventos(fechaHoyStr);
            }
        }
    }

    mostrarEventos(fecha) {
        const eventos = this.eventos[fecha] || [];
        this.eventosLista.innerHTML = '<h3>Eventos del Día</h3>';

        if (eventos.length === 0) {
            this.eventosLista.innerHTML += '<p>No hay eventos programados para este día.</p>';
            return;
        }

        eventos.forEach(evento => {
            const eventoElement = document.createElement('div');
            eventoElement.className = 'evento-item';
            eventoElement.innerHTML = `
                <h4>${evento.titulo}</h4>
                <p><strong>Hora:</strong> ${evento.hora}</p>
                <p>${evento.descripcion}</p>
            `;
            this.eventosLista.appendChild(eventoElement);
        });
    }
}

// Inicializar el calendario cuando el DOM esté cargado
document.addEventListener('DOMContentLoaded', () => {
    new Calendario();
}); 