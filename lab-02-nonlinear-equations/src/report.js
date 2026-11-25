const data = JSON.parse(document.getElementById('report-data').textContent);
const el = id => document.getElementById(id);
const colors = ['#34699a', '#bc4b32', '#47834d', '#8662a1', '#b57a24', '#34699a', '#bc4b32'];
const color = method => colors[method.number - 1];
const fixed = value => value.toFixed(10);
const sci = value => value.toExponential(4);
const config = {
    responsive: true,
    displaylogo: false,
    displayModeBar: true,
    scrollZoom: true,
    doubleClick: 'reset',
    toImageButtonOptions: {format: 'png', filename: 'LR2_graph', scale: 2},
    modeBarButtonsToRemove: ['select2d', 'lasso2d', 'toggleSpikelines']
};
const layout = (x, y, extra = {}) => ({
    font: {family: 'Arial, sans-serif', size: 13, color: '#20242a'},
    paper_bgcolor: '#fff', plot_bgcolor: '#fff',
    margin: {l: 76, r: 25, t: 48, b: 65},
    xaxis: {title: {text: x}, gridcolor: '#e5e7eb', zerolinecolor: '#a4a9b0', automargin: true},
    yaxis: {title: {text: y}, gridcolor: '#e5e7eb', zerolinecolor: '#a4a9b0', automargin: true},
    dragmode: 'pan', hovermode: 'closest',
    legend: {orientation: 'h', x: 0, y: 1.02, yanchor: 'bottom'},
    ...extra
});

function table(id, headers, rows) {
    const element = document.createElement('table');
    const head = element.createTHead().insertRow();
    for (const value of headers) {
        const th = document.createElement('th');
        th.textContent = value;
        head.appendChild(th);
    }
    const body = element.createTBody();
    for (const row of rows) {
        const tr = body.insertRow();
        for (const value of row) tr.insertCell().textContent = value;
    }
    el(id).replaceChildren(element);
}

function summaries() {
    table('scalar-summary', ['Метод', 'k', 'x', '|f(x)|', 'Оценка погрешности', 'Формула'],
        data.scalar.map(m => [m.number + '. ' + m.name, m.iterations, fixed(m.x), sci(m.residual), sci(m.error), m.bound]));
    table('system-summary', ['Метод', 'k', 'x', 'y', '|F₁|', '|F₂|', 'Невязка', 'Ψ'],
        data.system.map(m => [m.number + '. ' + m.name, m.iterations, fixed(m.x), fixed(m.y), sci(Math.abs(m.first)), sci(Math.abs(m.second)), sci(m.residual), sci(m.psi)]));
    el('scalar-spread').textContent = 'Разброс корней: ' + sci(data.scalar_spread) + '. k — число переходов от начальной записи (k = 0).';
    el('system-spread').textContent = 'Максимальное различие координат: ' + sci(data.system_spread) + '.';
}

function bars(kind) {
    const methods = data[kind];
    return Plotly.newPlot(el(kind + '-bars'), [{
        type: 'bar', orientation: 'h', x: methods.map(m => m.iterations), y: methods.map(m => m.name),
        marker: {color: methods.map(color)}, text: methods.map(m => String(m.iterations)),
        textposition: 'outside', cliponaxis: false,
        hovertemplate: '%{y}: %{x} уточнений<extra></extra>'
    }], layout('k', '', {
        margin: {l: 150, r: 40, t: 45, b: 50},
        xaxis: {title: {text: 'k'}, rangemode: 'tozero', gridcolor: '#e5e7eb', dtick: 5},
        yaxis: {autorange: 'reversed', automargin: true}, showlegend: false
    }), config);
}

function convergence(kind) {
    const index = Number(el(kind + '-mode').value);
    const scalar = kind === 'scalar';
    const traces = data[kind].map(m => ({
        type: 'scatter', mode: 'lines+markers', name: m.name,
        x: m.history.map(row => row[0]), y: m.history.map(row => row[index] > 0 ? row[index] : null),
        line: {color: color(m), width: 2}, marker: {size: 6},
        hovertemplate: 'k = %{x}<br>Значение = %{y:.6e}<extra>%{fullData.name}</extra>'
    }));
    const ylabel = scalar ? (index === 2 ? '|f(x)|' : 'Оценка погрешности') : (index === 3 ? 'max(|F₁|, |F₂|)' : 'Ψ');
    const shapes = [];
    const annotations = [];
    if ((scalar && index === 3) || (!scalar && index === 3)) {
        shapes.push({type: 'line', xref: 'paper', x0: 0, x1: 1, y0: data.limit, y1: data.limit, line: {color: '#747a82', width: 1, dash: 'dash'}});
        annotations.push({xref: 'paper', x: 1, y: Math.log10(data.limit), text: 'ε/2', showarrow: false, xanchor: 'right', yanchor: 'bottom', font: {size: 11}});
    }
    return Plotly.react(el(kind + '-conv'), traces, layout('k', ylabel, {
        margin: {l: 92, r: 20, t: 76, b: 55},
        xaxis: {title: {text: 'k'}, gridcolor: '#e5e7eb', rangemode: 'tozero', dtick: 5},
        yaxis: {title: {text: ylabel}, type: 'log', exponentformat: 'power', gridcolor: '#e5e7eb', automargin: true},
        shapes, annotations, uirevision: kind + '-convergence-' + index
    }), config);
}

function selected(kind) {
    return data[kind].find(m => m.number === Number(el(kind + '-select').value));
}
function pathTrace(method, x, y, extra = {}) {
    return {
        type: 'scatter', mode: 'lines+markers', name: method.name,
        x, y, line: {color: color(method), width: 2}, marker: {color: color(method), size: 6},
        customdata: method.history.map(r => r[0]),
        hovertemplate: 'k = %{customdata}<br>x = %{x:.12f}<br>y = %{y:.12f}<extra>%{fullData.name}</extra>', ...extra
    };
}
function marker(method, x, y) {
    return {type: 'scatter', mode: 'markers', name: 'Текущая точка', showlegend: false,
        x: [x], y: [y], marker: {size: 12, color: color(method), line: {width: 2, color: '#fff'}},
        hovertemplate: 'x = %{x:.12f}<br>y = %{y:.12f}<extra>Текущая точка</extra>'};
}

function scalarGraph() {
    const m = selected('scalar');
    const k = Number(el('scalar-step').value);
    const r = m.history[k];
    const root = data.scalar[1].x;
    const graph = el('scalar-graph');
    if (graph.data) {
        Plotly.restyle(graph, {x: [m.history.map(row => row[1])], y: [m.values], customdata: [m.history.map(row => row[0])], name: [m.name], 'marker.color': [color(m)]}, [1]);
        return Plotly.restyle(graph, {x: [[r[1]]], y: [[m.values[k]]], 'marker.color': [color(m)]}, [3]);
    }
    const traces = [
        {type: 'scatter', mode: 'lines', x: data.curve.x, y: data.curve.y, name: 'f(x)', line: {color: '#30363d', width: 2}, hovertemplate: 'x = %{x:.6f}<br>f(x) = %{y:.6f}<extra></extra>'},
        pathTrace(m, m.history.map(row => row[1]), m.values, {mode: 'markers', hovertemplate: 'k = %{customdata}<br>x = %{x:.12f}<br>f(x) = %{y:.6e}<extra>%{fullData.name}</extra>'}),
        {type: 'scatter', mode: 'markers', name: 'Корень (Ньютон)', x: [root], y: [0], marker: {symbol: 'x', color: '#20242a', size: 10}, hovertemplate: 'x ≈ %{x:.14f}<extra>Корень</extra>'},
        marker(m, r[1], m.values[k])
    ];
    return Plotly.react(el('scalar-graph'), traces, layout('x', 'f(x)', {uirevision: 'scalar-path', xaxis: {title: {text: 'x'}, range: [2, 4], gridcolor: '#e5e7eb'}, yaxis: {title: {text: 'f(x)'}, range: [-1, 1], zeroline: true, gridcolor: '#e5e7eb'}}), config);
}

function systemGraph() {
    const m = selected('system');
    const k = Number(el('system-step').value);
    const r = m.history[k];
    const graph = el('system-graph');
    if (graph.data) return Plotly.restyle(graph, {x: [[r[1]]], y: [[r[2]]], 'marker.color': [color(m)]}, [4]);
    const traces = data.curves.map((c, i) => ({type: 'scatter', mode: 'lines', name: i === 0 ? 'F₁ = 0' : 'F₂ = 0', x: c.x, y: c.y, line: {color: i === 0 ? '#626971' : '#969ca2', width: 2, dash: i === 0 ? 'solid' : 'dash'}, hoverinfo: 'skip'}));
    for (const method of data.system) {
        traces.push(pathTrace(method, method.history.map(row => row[1]), method.history.map(row => row[2])));
    }
    traces.push(marker(m, r[1], r[2]));
    return Plotly.react(el('system-graph'), traces, layout('x', 'y', {uirevision: 'system-path', xaxis: {title: {text: 'x'}, range: [-2.15, 0.45], gridcolor: '#e5e7eb'}, yaxis: {title: {text: 'y'}, range: [-1.15, 1.15], gridcolor: '#e5e7eb', scaleanchor: 'x', scaleratio: 1}}), config);
}

const camera = {azimuth: -0.9, elevation: 0.55, zoom: 1, dx: 0, dy: 0};
const initialCamera = {...camera};
const canvas = el('surface');
const mesh = data.surface;
const zMax = Math.max(...mesh.z.flat());
const xMin = mesh.x[0], xMax = mesh.x[mesh.x.length - 1];
const yMin = mesh.y[0], yMax = mesh.y[mesh.y.length - 1];

function surface() {
    if (el('system').hidden) return;
    const width = canvas.clientWidth, height = canvas.clientHeight;
    if (!width || !height) return;
    const dpr = window.devicePixelRatio || 1;
    canvas.width = Math.round(width * dpr);
    canvas.height = Math.round(height * dpr);
    const ctx = canvas.getContext('2d');
    ctx.scale(dpr, dpr);
    ctx.fillStyle = '#fff';
    ctx.fillRect(0, 0, width, height);
    const scale = Math.min(width / 3.5, height / 2.75) * camera.zoom;
    const ca = Math.cos(camera.azimuth), sa = Math.sin(camera.azimuth);
    const ce = Math.cos(camera.elevation), se = Math.sin(camera.elevation);

    // Ортографическая проекция после поворота вокруг вертикальной оси.
    function project(x, y, z) {
        const u = 2 * (x - xMin) / (xMax - xMin) - 1;
        const v = 1.65 * (y - yMin) / (yMax - yMin) - 0.825;
        const w = 1.35 * z / zMax - 0.55;
        const horizontal = ca * u - sa * v;
        const depth = sa * u + ca * v;
        return [width / 2 + camera.dx + scale * horizontal,
                height / 2 + camera.dy - scale * (ce * w - se * depth),
                ce * depth + se * w];
    }
    function drawLine(points, stroke, weight = 1) {
        ctx.beginPath();
        points.forEach((p, i) => i ? ctx.lineTo(p[0], p[1]) : ctx.moveTo(p[0], p[1]));
        ctx.strokeStyle = stroke;
        ctx.lineWidth = weight;
        ctx.stroke();
    }
    function label(p, text, dx = 0, dy = 0) {
        ctx.fillStyle = '#40474f';
        ctx.font = '12px Arial';
        ctx.fillText(text, p[0] + dx, p[1] + dy);
    }
    // Сетка в плоскости Ψ = 0.
    for (let x = -2; x <= 0.5; x += 0.5) {
        drawLine([project(x, yMin, 0), project(x, yMax, 0)], '#dce0e5');
        label(project(x, yMin, 0), x.toFixed(1), -10, 17);
    }
    for (let y = -1; y <= 1; y += 0.5) {
        drawLine([project(xMin, y, 0), project(xMax, y, 0)], '#dce0e5');
        label(project(xMax, y, 0), y.toFixed(1), 8, 3);
    }
    drawLine([project(xMin, yMin, 0), project(xMax, yMin, 0), project(xMax, yMax, 0)], '#737a83', 1.4);
    drawLine([project(xMin, yMin, 0), project(xMin, yMin, zMax)], '#737a83', 1.4);
    label(project(xMax, yMin, 0), 'x', 15, 21);
    label(project(xMax, yMax, 0), 'y', 12, -7);
    label(project(xMin, yMin, zMax), 'Ψ', -14, -8);
    for (let z = 0; z <= zMax; z += 1) label(project(xMin, yMin, z), String(z), -18, 4);

    // Ячейки поверхности рисуются от дальних к ближним.
    const cells = [];
    for (let j = 0; j < mesh.y.length - 1; j += 2) {
        for (let i = 0; i < mesh.x.length - 1; i += 2) {
            const indices = [[j, i], [j, i + 2], [j + 2, i + 2], [j + 2, i]];
            const points = indices.map(([r, c]) => project(mesh.x[c], mesh.y[r], mesh.z[r][c]));
            const depth = points.reduce((sum, p) => sum + p[2], 0) / 4;
            const z = indices.reduce((sum, [r, c]) => sum + mesh.z[r][c], 0) / 4;
            cells.push({points, depth, z});
        }
    }
    cells.sort((a, b) => a.depth - b.depth);
    for (const cell of cells) {
        const t = Math.sqrt(cell.z / zMax);
        ctx.fillStyle = `rgba(${Math.round(225 - 165*t)}, ${Math.round(239 - 105*t)}, ${Math.round(246 - 78*t)}, 0.86)`;
        ctx.strokeStyle = 'rgba(74,100,122,0.25)';
        ctx.lineWidth = 0.6;
        ctx.beginPath();
        cell.points.forEach((p, i) => i ? ctx.lineTo(p[0], p[1]) : ctx.moveTo(p[0], p[1]));
        ctx.closePath();
        ctx.fill();
        ctx.stroke();
    }
    // Траектории показываем поверх сетки, чтобы все итерации были видны.
    for (const method of data.system) {
        const points = method.history.map(row => project(row[1], row[2], row[4]));
        drawLine(points, color(method), 2.6);
        for (const point of points) {
            ctx.beginPath();
            ctx.arc(point[0], point[1], 2.6, 0, 2*Math.PI);
            ctx.fillStyle = color(method);
            ctx.fill();
        }
    }
    const method = selected('system');
    const row = method.history[Number(el('system-step').value)];
    const point = project(row[1], row[2], row[4]);
    ctx.beginPath();
    ctx.arc(point[0], point[1], 6, 0, 2*Math.PI);
    ctx.fillStyle = color(method);
    ctx.fill();
    ctx.strokeStyle = '#fff';
    ctx.lineWidth = 2;
    ctx.stroke();
    data.system.forEach((m, i) => {
        ctx.fillStyle = color(m);
        ctx.fillRect(15 + 145*i, 15, 16, 3);
        ctx.font = '13px Arial';
        ctx.fillStyle = '#30363d';
        ctx.fillText(m.name, 36 + 145*i, 20);
    });
}

let drag = null;
canvas.addEventListener('pointerdown', event => {
    canvas.setPointerCapture(event.pointerId);
    drag = {x: event.clientX, y: event.clientY};
});
canvas.addEventListener('pointermove', event => {
    if (!drag) return;
    const dx = event.clientX - drag.x, dy = event.clientY - drag.y;
    if (event.shiftKey || el('surface-mode').value === 'pan') {
        camera.dx += dx;
        camera.dy += dy;
    } else {
        camera.azimuth += dx * 0.008;
        camera.elevation = Math.max(-1.45, Math.min(1.45, camera.elevation + dy * 0.008));
    }
    drag = {x: event.clientX, y: event.clientY};
    surface();
});
for (const event of ['pointerup', 'pointercancel', 'lostpointercapture']) canvas.addEventListener(event, () => { drag = null; });
canvas.addEventListener('wheel', event => {
    event.preventDefault();
    camera.zoom = Math.max(0.4, Math.min(12, camera.zoom * Math.exp(-event.deltaY * 0.0015)));
    surface();
}, {passive: false});
el('surface-save').onclick = () => {
    const link = document.createElement('a');
    link.download = 'LR2_surface.png';
    link.href = canvas.toDataURL('image/png');
    link.click();
};
window.addEventListener('resize', surface);

function updateHistory(kind, reset) {
    const scalar = kind === 'scalar';
    const m = selected(kind);
    const slider = el(kind + '-step');
    slider.max = m.iterations;
    if (reset) slider.value = m.iterations;
    const k = Number(slider.value);
    const r = m.history[k];
    el(kind + '-k').textContent = k + ' / ' + m.iterations;
    if (scalar) {
        el('scalar-current').textContent = 'x = ' + fixed(r[1]) + '   |   f(x) = ' + sci(m.values[k]) + '   |   Оценка погрешности = ' + sci(r[3]);
        table('scalar-history', ['k', 'x', '|f(x)|', 'Оценка погрешности'], m.history.map(row => [row[0], fixed(row[1]), sci(row[2]), sci(row[3])]));
        scalarGraph();
    } else {
        el('system-current').textContent = 'x = ' + fixed(r[1]) + '   |   y = ' + fixed(r[2]) + '   |   Невязка = ' + sci(r[3]) + '   |   Ψ = ' + sci(r[4]) + '   |   α = ' + r[5];
        table('system-history', ['k', 'x', 'y', 'Невязка', 'Ψ', 'Шаг'], m.history.map(row => [row[0], fixed(row[1]), fixed(row[2]), sci(row[3]), sci(row[4]), row[5]]));
        systemGraph();
        surface();
    }
    el(kind + '-history').querySelectorAll('tbody tr')[k].classList.add('selected');
}

const initialized = new Set();
function show(kind) {
    for (const item of ['scalar', 'system']) {
        el(item).hidden = item !== kind;
        el('tab-' + item).setAttribute('aria-selected', String(item === kind));
    }
    if (!initialized.has(kind)) {
        initialized.add(kind);
        const select = el(kind + '-select');
        for (const m of data[kind]) select.add(new Option(m.number + '. ' + m.name, m.number));
        select.value = kind === 'scalar' ? '5' : '7';
        select.addEventListener('change', () => updateHistory(kind, true));
        el(kind + '-step').addEventListener('input', () => updateHistory(kind, false));
        el(kind + '-mode').addEventListener('change', () => convergence(kind));
        bars(kind);
        convergence(kind);
        updateHistory(kind, true);
    } else {
        for (const graph of el(kind).querySelectorAll('.js-plotly-plot')) Plotly.Plots.resize(graph);
        if (kind === 'system') surface();
    }
}

el('scalar-fit').onclick = () => Plotly.relayout(el('scalar-graph'), {'xaxis.range': [2, 4], 'yaxis.range': [-1, 1]});
el('scalar-root').onclick = () => {
    const x = data.scalar[1].x;
    Plotly.relayout(el('scalar-graph'), {'xaxis.range': [x - 0.01, x + 0.01], 'yaxis.range': [-0.012, 0.012]});
};
el('system-fit').onclick = () => Plotly.relayout(el('system-graph'), {'xaxis.range': [-2.15, 0.45], 'yaxis.range': [-1.15, 1.15]});
el('system-root').onclick = () => {
    const {x, y} = data.system[0];
    Plotly.relayout(el('system-graph'), {'xaxis.range': [x - 0.05, x + 0.05], 'yaxis.range': [y - 0.05, y + 0.05]});
};
el('surface-reset').onclick = () => { Object.assign(camera, initialCamera); surface(); };
for (const kind of ['scalar', 'system']) el('tab-' + kind).onclick = () => show(kind);
summaries();
show('scalar');
