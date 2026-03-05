
// _________________________________________________________________
(function () {

  var canvas, ctx, circ, nodes, mouse,
      SENSITIVITY, SIBLINGS_LIMIT, DENSITY, NODES_QTY, ANCHOR_LENGTH, MOUSE_RADIUS;

  SENSITIVITY   = 100;
  SIBLINGS_LIMIT = 10;
  DENSITY       = 60;
  NODES_QTY     = 0;
  ANCHOR_LENGTH = 20;
  MOUSE_RADIUS  = 200;

  circ  = 2 * Math.PI;
  nodes = [];

  // ── Cibler le bon canvas selon la page ──
  canvas = document.getElementById('heroCanvas') || document.querySelector('canvas');
  if (!canvas) return;

  ctx = canvas.getContext('2d');
  if (!ctx) return;

  resizeCanvas();

  mouse = {
    x: canvas.width  / 2,
    y: canvas.height / 2
  };

  // ── Couleur d'accent selon le thème ──
  function getAccentRGB() {
    var theme = document.documentElement.getAttribute('data-theme');
    return theme === 'dark' ? '14, 165, 233' : '14, 165, 233'; // #0ea5e9 dans les deux cas
  }

  // ── Node ──
  function Node(x, y) {
    this.anchorX = x;
    this.anchorY = y;
    this.x = Math.random() * (x - (x - ANCHOR_LENGTH)) + (x - ANCHOR_LENGTH);
    this.y = Math.random() * (y - (y - ANCHOR_LENGTH)) + (y - ANCHOR_LENGTH);
    this.vx = Math.random() * 2 - 1;
    this.vy = Math.random() * 2 - 1;
    this.energy = Math.random() * 100;
    this.radius = Math.random();
    this.siblings = [];
    this.brightness = 0;
  }

  Node.prototype.drawNode = function () {
    var color = 'rgba(' + getAccentRGB() + ', ' + this.brightness + ')';
    ctx.beginPath();
    ctx.arc(this.x, this.y, 2 * this.radius + 2 * this.siblings.length / SIBLINGS_LIMIT, 0, circ);
    ctx.fillStyle = color;
    ctx.fill();
  };

  Node.prototype.drawConnections = function () {
    for (var i = 0; i < this.siblings.length; i++) {
      var color = 'rgba(' + getAccentRGB() + ', ' + this.brightness * 0.6 + ')';
      ctx.beginPath();
      ctx.moveTo(this.x, this.y);
      ctx.lineTo(this.siblings[i].x, this.siblings[i].y);
      ctx.lineWidth = 1 - calcDistance(this, this.siblings[i]) / SENSITIVITY;
      ctx.strokeStyle = color;
      ctx.stroke();
    }
  };

  Node.prototype.moveNode = function () {
    this.energy -= 2;
    if (this.energy < 1) {
      this.energy = Math.random() * 100;
      if      (this.x - this.anchorX < -ANCHOR_LENGTH) { this.vx =  Math.random() * 2; }
      else if (this.x - this.anchorX >  ANCHOR_LENGTH) { this.vx = -Math.random() * 2; }
      else                                              { this.vx =  Math.random() * 4 - 2; }
      if      (this.y - this.anchorY < -ANCHOR_LENGTH) { this.vy =  Math.random() * 2; }
      else if (this.y - this.anchorY >  ANCHOR_LENGTH) { this.vy = -Math.random() * 2; }
      else                                              { this.vy =  Math.random() * 4 - 2; }
    }
    this.x += this.vx * this.energy / 100;
    this.y += this.vy * this.energy / 100;
  };

  // ── Init ──
  function initNodes() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    nodes     = [];
    NODES_QTY = 0;
    for (var i = DENSITY; i < canvas.width; i += DENSITY) {
      for (var j = DENSITY; j < canvas.height; j += DENSITY) {
        nodes.push(new Node(i, j));
        NODES_QTY++;
      }
    }
  }

  function calcDistance(a, b) {
    return Math.sqrt(Math.pow(a.x - b.x, 2) + Math.pow(a.y - b.y, 2));
  }

  function findSiblings() {
    var node1, node2, distance;
    for (var i = 0; i < NODES_QTY; i++) {
      node1 = nodes[i];
      node1.siblings = [];
      for (var j = 0; j < NODES_QTY; j++) {
        node2 = nodes[j];
        if (node1 === node2) continue;
        distance = calcDistance(node1, node2);
        if (distance < SENSITIVITY) {
          if (node1.siblings.length < SIBLINGS_LIMIT) {
            node1.siblings.push(node2);
          } else {
            var maxDist = 0, s = 0, d;
            for (var k = 0; k < SIBLINGS_LIMIT; k++) {
              d = calcDistance(node1, node1.siblings[k]);
              if (d > maxDist) { maxDist = d; s = k; }
            }
            if (distance < maxDist) {
              node1.siblings.splice(s, 1);
              node1.siblings.push(node2);
            }
          }
        }
      }
    }
  }

  function redrawScene() {
    resizeCanvas();
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    findSiblings();

    var i, node, distance;

    for (i = 0; i < NODES_QTY; i++) {
      node = nodes[i];
      distance = calcDistance({ x: mouse.x, y: mouse.y }, node);
      node.brightness = distance < MOUSE_RADIUS ? 1 - distance / MOUSE_RADIUS : 0;
    }

    for (i = 0; i < NODES_QTY; i++) {
      node = nodes[i];
      if (node.brightness) {
        node.drawNode();
        node.drawConnections();
      }
      node.moveNode();
    }

    requestAnimationFrame(redrawScene);
  }

  // ── Resize : recalcule le canvas ET réinitialise les noeuds ──
  function resizeCanvas() {
    var parent = canvas.parentElement;
    // Sur la page d'accueil le canvas est dans .hero (plein écran)
    // Sur les autres pages il prend la taille de la fenêtre
    canvas.width  = parent ? parent.offsetWidth  : window.innerWidth;
    canvas.height = parent ? parent.offsetHeight : window.innerHeight;
  }

  var resizeTimer;
  window.addEventListener('resize', function () {
    clearTimeout(resizeTimer);
    resizeTimer = setTimeout(function () {
      initNodes();
    }, 200);
  }, false);

  // Écouter sur window pour capturer la souris même hors du canvas
  window.addEventListener('mousemove', function (e) {
    var rect = canvas.getBoundingClientRect();
    mouse.x  = e.clientX - rect.left;
    mouse.y  = e.clientY - rect.top;
  }, false);

  // Quand la souris quitte le canvas, elle revient au centre
  canvas.addEventListener('mouseleave', function () {
    mouse.x = canvas.width  / 2;
    mouse.y = canvas.height / 2;
  }, false);

  initNodes();
  redrawScene();

})();
