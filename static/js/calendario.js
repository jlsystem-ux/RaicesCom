class Calendario {    constructor() {
        console.log('Initializing calendar...');
        this.fecha = new Date();
        this.mesActual = this.fecha.getMonth();
        this.anioActual = this.fecha.getFullYear();
        this.eventos = {};
        
        // Initialize calendar toggle first
        const calendarioToggle = document.getElementById('eventosToggle');
        const calendarioContainer = document.getElementById('calendarioContainer');

        if (calendarioToggle && calendarioContainer) {
            calendarioToggle.addEventListener('click', () => {
                calendarioContainer.classList.toggle('collapsed');
                const span = calendarioToggle.querySelector('span');
                if (span) {
                    span.textContent = calendarioContainer.classList.contains('collapsed') ? 
                        'Ver Calendario' : 'Ocultar Calendario';
                }
            });
        }
    }    inicializar() {
        console.log('Setting up calendar elements...');
        this.prevBtn = document.getElementById('prevMonth');
        this.nextBtn = document.getElementById('nextMonth');
        this.monthYearElement = document.getElementById('monthYear');
        this.diasContainer = document.getElementById('dias');
        this.eventosLista = document.getElementById('eventos-lista');
        
        if (!this.prevBtn || !this.nextBtn || !this.monthYearElement || !this.diasContainer || !this.eventosLista) {
            console.error('Some calendar elements were not found:', {
                prevBtn: !!this.prevBtn,
                nextBtn: !!this.nextBtn,
                monthYear: !!this.monthYearElement,
                dias: !!this.diasContainer,
                eventos: !!this.eventosLista
            });
            return;
        }

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
    }    async cargarEventos() {
        try {
            console.log('Fetching events...');
            const response = await fetch('/api/events/', {
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                    'Accept': 'application/json',
                }
            });
            console.log('Response status:', response.status);
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const eventosData = await response.json();
            console.log('Events data:', eventosData);
            
            if (Array.isArray(eventosData)) {
                this.eventos = {};
                eventosData.forEach(event => {
                    const fecha = event.start.split(' ')[0];
                    if (!this.eventos[fecha]) {
                        this.eventos[fecha] = [];
                    }
                    this.eventos[fecha].push({
                        titulo: event.title,
                        descripcion: event.description,
                        hora: event.start.split(' ')[1],
                        location: event.location,
                        online: event.online,
                        meeting_link: event.meeting_link
                    });
                });
                console.log('Processed events:', this.eventos);
                this.renderizarCalendario();
            } else {
                console.error('Events data is not an array:', eventosData);
            }
            
            this.eventos = {};
            eventosData.forEach(event => {
                const fecha = event.start.split(' ')[0];
                if (!this.eventos[fecha]) {
                    this.eventos[fecha] = [];
                }
                this.eventos[fecha].push({
                    titulo: event.title,
                    descripcion: event.description,
                    hora: event.start.split(' ')[1],
                    location: event.location,
                    online: event.online,
                    meeting_link: event.meeting_link
                });
            });
            
            this.renderizarCalendario();
        } catch (error) {
            console.error('Error al cargar eventos:', error);
        }
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

        const list = document.createElement('div');
        list.className = 'cal-event-list';

        eventos.forEach(evento => {
            const item = document.createElement('div');
            item.className = 'cal-event-item';
            item.innerHTML = `
                <div class="cal-event-title">&#128197; ${evento.titulo}</div>
                <div class="cal-event-detail"><span>&#128197;</span> <strong>Hora:</strong> ${evento.hora}</div>
                <div class="cal-event-detail"><span>&#128205;</span> <strong>Lugar:</strong> ${evento.location || 'N/A'}</div>
                <div class="cal-event-detail"><span>&#9998;&#65039;</span> ${evento.descripcion}</div>
                ${evento.online ? `<div class='cal-event-detail'><span>&#128187;</span> <strong>Online</strong></div>` : ''}
                ${evento.meeting_link ? `<div class='cal-event-detail'><span>&#128279;</span> <a href='${evento.meeting_link}' target='_blank'>Enlace de reunión</a></div>` : ''}
            `;
            list.appendChild(item);
        });
        this.eventosLista.appendChild(list);
    }
}

// Inicializar el calendario cuando el DOM esté cargado
document.addEventListener('DOMContentLoaded', () => {
    new Calendario();
}); 