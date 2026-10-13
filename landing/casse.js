/**
 * Casse: a printer's type case with six compartments of uneven size, a finger
 * pull and a label holder on its front. Each compartment holds one UI part,
 * known by its shape: a button's pill, a switch's track and knob, an avatar's
 * disc, a card with its rules, an input with its caret, a checked box. The part
 * under the pointer rises out of its case on dashed drops, as `pyblade-ui add`
 * takes it out; the others settle, staggered outwards. The slider is the
 * stagger, in ms.
 */
const {
  Cam, circ, extremes, facing, fit, hull, open, poly, prism, proj, ringAt, rings, rrect, run, seg,
  tdone, tset, tval, tween, unproj, disposer, mk, pointer, put, reflect, register, solid,
} = HL;

const X0 = 0, X1 = 150, Y0 = 0, Y1 = 92, FB = 5, FH = 10, CH = 9, ZF = 1, LIFT = 30, WALL = 1.3;

/** A ring moved to (x, y): circ() is drawn round the origin. */
const at = (ring, x, y) => ring.map((q) => ({ ...q, u: q.u + x, v: q.v + y }));
const disc = (x, y, R, b) => [at(circ(R, 24), x, y), at(circ(R - b, 24), x, y)];

/** The parts, each in its cell [x0, y0, x1, y1], at col/row, with its solids [rings, z0, z1] and the marks on its top. */
const PARTS = [
  { name: "button", cell: [0, 0, 58, 44], cr: [0, 0], rest: 13,
    make: (x, y) => ({ solids: [[rings(x - 17, y - 7, x + 17, y + 7, 7, 1.2), 0, 5]],
      marks: [[(P, z) => seg(P(x - 7, y, z), P(x + 7, y, z)), "nf lo"]] }) },
  { name: "switch", cell: [58, 0, 104, 44], cr: [1, 0], rest: 3,
    make: (x, y) => ({ solids: [[rings(x - 15, y - 7, x + 15, y + 7, 7, 1.2), 0, 3], [disc(x + 8, y, 5.6, 1.2), 3, 7]], marks: [] }) },
  { name: "avatar", cell: [104, 0, 150, 44], cr: [2, 0], rest: 6,
    make: (x, y) => ({ solids: [[disc(x, y, 13, 1.6), 0, 4]],
      marks: [[(P, z) => poly(ringAt(P, at(circ(4.6, 16), x - 3, y - 3), z)), "nf"],
        [(P, z) => open(ringAt(P, at(circ(8.5, 24), x + 4, y + 4).filter((q) => q.u + q.v < 0), z)), "nf"]] }) },
  { name: "card", cell: [0, 44, 64, 92], cr: [0, 1], rest: 1,
    make: (x, y) => ({ solids: [[rings(x - 25, y - 17, x + 25, y + 17, 4, 1.2), 0, 2.5]],
      marks: [[(P, z) => seg(P(x - 19, y - 10, z), P(x + 4, y - 10, z)), "nf"],
        [(P, z) => seg(P(x - 19, y - 4, z), P(x + 15, y - 4, z)) + seg(P(x - 19, y + 1, z), P(x + 9, y + 1, z)), "nf lo"],
        [(P, z) => poly(ringAt(P, rrect(x + 7, y + 7, x + 20, y + 12.5, 2.7, 4), z)), "nf"]] }) },
  { name: "input", cell: [64, 44, 124, 92], cr: [1, 1], rest: 4,
    make: (x, y) => ({ solids: [[rings(x - 26, y - 7, x + 26, y + 7, 3, 1.2), 0, 3]],
      marks: [[(P, z) => seg(P(x - 20, y - 4, z), P(x - 20, y + 4, z)), "nf"],
        [(P, z) => seg(P(x - 16, y, z), P(x + 6, y, z)), "nf lo"]] }) },
  { name: "checkbox", cell: [124, 44, 150, 92], cr: [2, 1], rest: 8,
    make: (x, y) => ({ solids: [[rings(x - 7, y - 7, x + 7, y + 7, 2.5, 1.1), 0, 5]],
      marks: [[(P, z) => open([P(x - 4, y + 0.5, z), P(x - 1, y + 3.5, z), P(x + 4, y - 3, z)]), "nf"]] }) },
];

/** A run of points ordered left to right on screen. */
const LR = (pts) => (pts[0][0] <= pts[pts.length - 1][0] ? pts : pts.slice().reverse());

/** An open box seen from above: `far` goes before what it holds, `near` after; each entry is [d, class]. */
function box(P, front, outer, inner, h, cls) {
  const iF = LR(ringAt(P, run(inner, front), h)), oT = LR(ringAt(P, run(outer, front), h)), oB = LR(ringAt(P, run(outer, front), 0));
  return {
    far: [[poly(ringAt(P, inner, h)), "nf " + cls], [open(ringAt(P, run(inner, (q) => !front(q)), ZF)), "nf lo"]],
    near: [[poly([...iF, oT[oT.length - 1], ...oB.slice().reverse(), oT[0]]), "fo"], [open(iF), "nf " + cls]],
    edge: open([oT[0], ...oB, oT[oT.length - 1]]),
  };
}

function mount({ stage, svg, read }, value) {
  const bag = disposer();
  let stag = value;

  // Fitted to the tray with the farthest part lifted, so nothing leaves the frame in any pose.
  const top = ZF + LIFT + 8;
  const C = Cam(45, 0.5, 1.72);
  fit(C, [[X0 - FB, Y0 - FB, 0], [X1 + FB, Y1 + FB, -8], [X1 + FB, Y0 - FB, 0], [X0 - FB, Y1 + FB, 0], [12, 10, top], [130, 10, top], [10, 60, top]], 200, 166);
  const P = proj(C), front = facing(C);

  const outer = rrect(X0 - FB, Y0 - FB, X1 + FB, Y1 + FB, 7, 6), inner = rrect(X0, Y0, X1, Y1, 2.5, 6);
  const frame = box(P, front, outer, inner, FH, "");
  const g = mk("g", {}, svg);
  reflect(svg, g, P, front, outer, 0, 14);
  mk("path", { d: poly(hull(ringAt(P, outer, 0).concat(ringAt(P, outer, FH)))), class: "sil" }, g);
  for (const [d, cls] of frame.far) mk("path", { d, class: cls }, g);

  // Cells from the far corner to the near one, so appending is painting back to front.
  const parts = PARTS.map((p) => ({ ...p })).sort((a, b) => a.cell[0] + a.cell[1] - (b.cell[0] + b.cell[1]));
  for (const p of parts) {
    const [x0, y0, x1, y1] = p.cell, cx = (x0 + x1) / 2, cy = (y0 + y1) / 2;
    const [co, ci] = rings(x0 + 0.4, y0 + 0.4, x1 - 0.4, y1 - 0.4, 4, WALL);
    const cup = box(P, front, co, ci, CH, "lo");
    for (const [d, cls] of cup.far) mk("path", { d, class: cls }, g);
    const grp = mk("g", {}, g), shape = p.make(cx, cy);
    p.guide = mk("path", { class: "nf dash" }, grp);
    p.solids = shape.solids.map(([[ring, inn], z0, z1]) => ({ ring, inn, z0, z1, el: solid(grp) }));
    p.marks = shape.marks.map(([fn, cls]) => ({ fn, el: mk("path", { class: cls }, grp) }));
    for (const [d, cls] of cup.near) mk("path", { d, class: cls }, g);
    p.tw = tween(p.rest);
    p.drawn = NaN;
  }
  const frameNear = mk("g", {}, g);
  for (const [d, cls] of frame.near) mk("path", { d, class: cls }, frameNear);
  // the front: a finger pull in the middle, a label holder with its card to the left
  const onFront = (ring) => poly(ring.map((q) => P(q.u, Y1 + FB, q.v)));
  const hx = (X0 + X1) / 2;
  mk("path", { d: frame.edge, class: "nf sil" }, frameNear);
  mk("path", { d: onFront(rrect(hx - 13, 3, hx + 13, 7.5, 2.2, 5)), class: "nf" }, frameNear);
  mk("path", { d: onFront(rrect(hx - 11, 4.2, hx + 11, 6.3, 1, 4)), class: "nf lo" }, frameNear);
  mk("path", { d: onFront(rrect(14, 2.6, 40, 7.8, 1, 4)), class: "nf" }, frameNear);
  mk("path", { d: onFront(rrect(16, 3.6, 38, 6.8, 0.6, 4)), class: "nf lo" }, frameNear);

  function draw(p, lift) {
    const zb = ZF + lift;
    p.solids.forEach((s) => put(s.el, prism(P, front, s.ring, s.inn, zb + s.z0, zb + s.z1)));
    const ztop = zb + p.solids[0].z1;
    p.marks.forEach((m) => m.el.setAttribute("d", m.fn(P, ztop)));
    const [l, r] = extremes(P, p.solids[0].ring);
    p.guide.setAttribute("d", lift > 10 ? seg(P(l.u, l.v, ZF), P(l.u, l.v, zb)) + seg(P(r.u, r.v, ZF), P(r.u, r.v, zb)) : "");
  }

  const B = register(stage, (_dt, now) => {
    let moving = false;
    for (const p of parts) {
      const v = tval(p.tw, now);
      if (v !== p.drawn) { draw(p, v); p.drawn = v; }
      if (!tdone(p.tw, now)) moving = true;
    }
    return moving;
  });
  bag.add(B.unregister);

  // Hit test on the plane of the parts' resting tops inside the cells: it never moves.
  function hit([sx, sy]) {
    const [x, y] = unproj(C, sx, sy, ZF + 4);
    return parts.findIndex((p) => x >= p.cell[0] && x < p.cell[2] && y >= p.cell[1] && y < p.cell[3]);
  }

  let act = -2;
  const lead = parts.find((p) => p.name === "button");
  function setActive(i) {
    const a = i < 0 ? -1 : i;
    if (a === act) return;
    const now = performance.now(), from = parts[a >= 0 ? a : act >= 0 ? act : parts.indexOf(lead)];
    act = a;
    for (const p of parts) {
      const delay = Math.hypot(p.cr[0] - from.cr[0], p.cr[1] - from.cr[1]) * stag;
      tset(p.tw, a < 0 ? p.rest : p === parts[a] ? LIFT : 0, now, delay);
      p.solids[0].el.sil.classList.toggle("hi", a < 0 ? p === lead : p === parts[a]);
    }
    read.textContent = a < 0 ? "rest" : "ui/" + parts[a].name;
    B.wake();
  }
  setActive(-1);

  bag.add(pointer(stage, { move: (pt) => setActive(hit(pt)), leave: () => setActive(-1) }));
  bag.add(() => svg.replaceChildren());

  return {
    set: (v) => { stag = v; },
    destroy: bag.dispose,
  };
}

hairline({
  name: "casse",
  means: "A type case of UI parts: the one under the pointer rises out of its compartment, as pyblade-ui add takes it.",
  rules: [1, 2, 5, 9, 10],
  range: [0, 45, 100],
  tour: [[236, 161], [121, 159], [249, 223], null],
  mount,
});
