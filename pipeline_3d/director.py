import os
import re
import json
import urllib.request
from pathlib import Path


# ─────────────────────────────────────────────────────────────────────────────
# CURATED 3D CHOREOGRAPHIES FOR CORE TOPICS (Guaranteed Flawless)
# ─────────────────────────────────────────────────────────────────────────────

def get_chewing_gum_shots() -> str:
    return '''import * as THREE from 'three';
import { ctx, W, H, clamp, lerp, seg, eo, eio, eob } from './core/lib.js';
import { L, Wd, T } from './core/timing.js';
import { camera } from './core/engine.js';
import { Human } from './core/human.js';
import * as SETS from './core/sets.js';
import { label, pill, warning, blackout } from './core/look2d.js';

const V3 = (x, y, z) => new THREE.Vector3(x, y, z);
const lerpV = (a, b, k) => a.clone().lerp(b, k);
function screen(p, cam) { const v = p.clone().project(cam); return [(v.x + 1) / 2 * W, (1 - v.y) / 2 * H]; }

export function buildShots(E) {
  const S = [], CUES = [], add = (o) => (S.push(o), o), cue = (t, type, o = {}) => CUES.push({ t: +t.toFixed(3), type, ...o });
  const cut = (i) => (i === 0 ? 0 : L(i) - 0.08);
  const cam = camera(30);
  const KLOOK = { aperture: 0, bloom: 0.2 }, XLOOK = { aperture: 0, bloom: 0.45, vignette: 0.45 }, VLOOK = { aperture: 0, bloom: 0.5 };

  const K = SETS.kitchen(E), hero = new Human({}); hero.group.position.set(0.1, 0, -0.6); K.scene.add(hero.group);
  const X = SETS.xrayStage(E), xh = new Human({}), xmat = SETS.xrayMaterial(); xh.setBodyMaterial(xmat); const I = SETS.insides(); xh.spine.add(I.group); X.scene.add(xh.group);
  const VS = SETS.vessel(E);
  const CYAN = new THREE.Color('#4FD1E8'), RED = new THREE.Color('#FF3B3B'), GREEN = new THREE.Color('#7CF29A');
  const FACE = V3(0.1, 1.68, -0.6);

  const reset = () => { hero.pose({}); xh.pose({}); I.stomach.scale.setScalar(1); xmat.uniforms.uCol.value.copy(CYAN); };
  const kitchenRender = (focus, extra = {}) => E.render(K.scene, cam, { ...KLOOK, ...extra });

  // 1 · HOOK: hero swallowing gum, looking concerned
  { const st = cut(0);
    add({ id: 'S01', at: st, note: 'hero swallowing gum, camera pushing in', draw(lt, d, t, blit) {
      reset(); const k = eo(seg(lt, 0.1, 1.2));
      hero.pose({ head: [-6 * k, 4, 0], spine: [-2 * k, 0, 0], lid: lerp(0, -0.2, k), look: [0, -3 * k] });
      cam.position.copy(lerpV(V3(0.35, 1.72, 0.5), V3(0.2, 1.7, 0.15), eio(lt / d))); cam.lookAt(FACE); kitchenRender(1.0); blit();
      pill('SWALLOWED GUM', 540, 330, eob(seg(lt, 0.15, 0.45)), '#FFD43B');
    } });
    cue(st + 0.15, 'gulp', { dur: 0.8 }); }

  // 2 · FALSE MYTH: timer 7 years with big X
  { const st = cut(1);
    add({ id: 'S02', at: st, note: 'hero shakes head: 7 years myth debunked', draw(lt, d, t, blit) {
      reset(); const shake = Math.sin(lt * 8) * 8;
      hero.pose({ head: [0, shake, 0], lid: -0.1, look: [0, 0] });
      cam.position.set(0.1, 1.65, 0.7); cam.lookAt(FACE); kitchenRender(1.3); blit();
      pill('7 YEARS? FALSE ✗', 540, 330, eob(seg(lt, 0.1, 0.35)), '#FF4D4D');
    } });
    cue(st, 'whoosh'); cue(st + 0.1, 'pop', { gain: 0.6 }); }

  // 3 · Slides down esophagus into stomach (X-ray)
  { const st = cut(2);
    add({ id: 'S03', at: st, note: 'x-ray: gum sliding down into stomach', draw(lt, d, t, blit) {
      reset(); const prog = eio(clamp(lt / d));
      cam.position.copy(lerpV(V3(0.4, 1.6, 1.4), V3(0.2, 1.25, 0.9), prog)); cam.lookAt(0, 1.2, 0);
      E.render(X.scene, cam, XLOOK); blit();
      const [lx, ly] = screen(V3(0.03, 1.15, 0.05), cam);
      label('ESOPHAGUS → STOMACH', 720, 520, lx, ly, eob(seg(lt, 0.2, 0.5)));
    } });
    cue(st, 'whoosh'); cue(st + 0.2, 'slide', { dur: 1.2 }); }

  // 4 · Stomach acid dissolving sugars but NOT gum base
  { const st = cut(3);
    add({ id: 'S04', at: st, note: 'stomach closeup: acid dissolves sugars', draw(lt, d, t, blit) {
      reset(); const pulse = Math.sin(lt * 4) * 0.05;
      I.stomach.scale.set(1 + pulse, 1 - pulse, 1 + pulse);
      const STOM = V3(0.03, 1.14, 0.02);
      cam.position.copy(lerpV(V3(0.25, 1.25, 0.6), V3(0.1, 1.2, 0.4), eio(lt / d))); cam.lookAt(STOM);
      E.render(X.scene, cam, XLOOK); blit();
      pill('ACID: DISSOLVES FLAVORS', 540, 330, eob(seg(lt, 0.15, 0.4)), '#7CF29A');
    } });
    cue(st, 'whoosh'); cue(st + 0.15, 'bubbles', { dur: 1.5 }); }

  // 5 · Cannot dissolve rubbery base
  { const st = cut(4);
    add({ id: 'S05', at: st, note: 'stomach: rubbery gum base remains solid', draw(lt, d, t, blit) {
      reset(); const STOM = V3(0.03, 1.14, 0.02);
      cam.position.set(0.08, 1.2, 0.45); cam.lookAt(STOM);
      E.render(X.scene, cam, XLOOK); blit();
      pill('GUM BASE: INDIGESTIBLE', 540, 330, eob(seg(lt, 0.1, 0.35)), '#FFA500');
    } });
    cue(st, 'whoosh'); cue(st + 0.2, 'thud', { gain: 0.5 }); }

  // 6 · Instead of staying stuck
  { const st = cut(5);
    add({ id: 'S06', at: st, note: 'x-ray: peristalsis moving the gum', draw(lt, d, t, blit) {
      reset(); const wave = Math.sin(lt * 6) * 0.04;
      xh.pose({ spine: [0, 0, wave * 20] });
      cam.position.copy(lerpV(V3(0.3, 1.3, 1.1), V3(0.15, 1.1, 0.8), eio(lt / d))); cam.lookAt(0, 1.05, 0);
      E.render(X.scene, cam, XLOOK); blit();
      pill('PERISTALSIS (MUSCLE WAVES)', 540, 1180, eob(seg(lt, 0.15, 0.4)), '#4FD1E8');
    } });
    cue(st, 'whoosh'); cue(st + 0.2, 'pop', { gain: 0.4 }); }

  // 7 · Muscles keep contracting and pushing
  { const st = cut(6);
    add({ id: 'S07', at: st, note: 'digestive muscle contractions', draw(lt, d, t, blit) {
      reset(); const wave = Math.sin(lt * 5) * 0.06;
      cam.position.set(0.1, 1.1 + wave * 0.2, 0.85); cam.lookAt(0, 1.0, 0);
      E.render(X.scene, cam, XLOOK); blit();
      pill('CONTRACTING MUSCLES', 540, 330, eob(seg(lt, 0.1, 0.35)), '#7CF29A');
    } });
    cue(st, 'whoosh'); cue(st + 0.2, 'thud', { gain: 0.4 }); }

  // 8 · Leaves body within days (kitchen, hero smiling)
  { const st = cut(7);
    add({ id: 'S08', at: st, note: 'kitchen: hero smiles, normal transit', draw(lt, d, t, blit) {
      reset(); hero.pose({ head: [-2, 4, 0], lid: -0.15, look: [0, 0] });
      cam.position.copy(lerpV(V3(0.3, 1.68, 0.8), V3(0.1, 1.65, 0.5), eio(lt / d))); cam.lookAt(FACE);
      kitchenRender(1.0); blit();
      pill('PASSES IN 2-3 DAYS ✓', 540, 330, eob(seg(lt, 0.2, 0.45)), '#7CF29A');
    } });
    cue(st, 'whoosh'); cue(st + 0.2, 'pop', { gain: 0.6 }); }

  // 9 · Warning: don't swallow huge wad
  { const st = cut(8);
    add({ id: 'S09', at: st, note: 'warning sign: huge wad causes blockage', draw(lt, d, t, blit) {
      reset(); hero.pose({ head: [4, 0, 0], lid: 0.1 });
      cam.position.set(0.1, 1.62, 0.7); cam.lookAt(FACE);
      kitchenRender(1.2); blit();
      warning(540, 1150, eob(seg(lt, 0.2, 0.5)));
    } });
    cue(st, 'whoosh'); cue(st + 0.2, 'alarm', { gain: 0.7 }); }

  return { shots: S, cues: CUES };
}
'''


def get_knuckle_shots() -> str:
    return '''import * as THREE from 'three';
import { ctx, W, H, clamp, lerp, seg, eo, eio, eob } from './core/lib.js';
import { L, Wd, T } from './core/timing.js';
import { camera } from './core/engine.js';
import { Human } from './core/human.js';
import * as SETS from './core/sets.js';
import { label, pill, warning } from './core/look2d.js';

const V3 = (x, y, z) => new THREE.Vector3(x, y, z);
const lerpV = (a, b, k) => a.clone().lerp(b, k);
function screen(p, cam) { const v = p.clone().project(cam); return [(v.x + 1) / 2 * W, (1 - v.y) / 2 * H]; }

export function buildShots(E) {
  const S = [], CUES = [], add = (o) => (S.push(o), o), cue = (t, type, o = {}) => CUES.push({ t: +t.toFixed(3), type, ...o });
  const cut = (i) => (i === 0 ? 0 : L(i) - 0.08);
  const cam = camera(30);
  const KLOOK = { aperture: 0, bloom: 0.2 }, XLOOK = { aperture: 0, bloom: 0.45, vignette: 0.45 }, VLOOK = { aperture: 0, bloom: 0.5 };

  const K = SETS.kitchen(E), hero = new Human({}); hero.group.position.set(0.1, 0, -0.6); K.scene.add(hero.group);
  const X = SETS.xrayStage(E), xh = new Human({}), xmat = SETS.xrayMaterial(); xh.setBodyMaterial(xmat); const I = SETS.insides(); xh.spine.add(I.group); X.scene.add(xh.group);
  const VS = SETS.vessel(E);
  const CYAN = new THREE.Color('#4FD1E8'), RED = new THREE.Color('#FF3B3B');
  const FACE = V3(0.1, 1.68, -0.6);

  const reset = () => { hero.pose({}); xh.pose({}); xmat.uniforms.uCol.value.copy(CYAN); };
  const kitchenRender = (focus, extra = {}) => E.render(K.scene, cam, { ...KLOOK, ...extra });

  // 1 · HOOK: examining fingers in kitchen
  { const st = cut(0);
    add({ id: 'S01', at: st, note: 'hero looking at fingers about to crack', draw(lt, d, t, blit) {
      reset(); const k = eo(seg(lt, 0.1, 1.2));
      hero.pose({ head: [10 * k, -12 * k, 0], shR: [15 * k, -20 * k, 35 * k], elR: [-50 * k, 0, 0] });
      cam.position.copy(lerpV(V3(0.35, 1.65, 0.6), V3(0.2, 1.55, 0.25), eio(lt / d))); cam.lookAt(0.15, 1.45, -0.3);
      kitchenRender(0.9); blit();
      pill('CRACKING KNUCKLES', 540, 330, eob(seg(lt, 0.15, 0.45)), '#FFD43B');
    } });
    cue(st, 'whoosh'); }

  // 2 · Bones not rubbing together (X-ray joint)
  { const st = cut(1);
    add({ id: 'S02', at: st, note: 'x-ray: bones have space between them', draw(lt, d, t, blit) {
      reset();
      cam.position.copy(lerpV(V3(0.3, 1.4, 1.0), V3(0.15, 1.35, 0.7), eio(lt / d))); cam.lookAt(0, 1.35, 0);
      E.render(X.scene, cam, XLOOK); blit();
      pill('BONES DO NOT RUB ✗', 540, 330, eob(seg(lt, 0.15, 0.4)), '#7CF29A');
    } });
    cue(st, 'whoosh'); cue(st + 0.2, 'pop', { gain: 0.5 }); }

  // 3 · Synovial fluid lubricating joint
  { const st = cut(2);
    add({ id: 'S03', at: st, note: 'joint capsule with synovial fluid', draw(lt, d, t, blit) {
      reset(); const pulse = Math.sin(lt * 3) * 0.02;
      cam.position.set(0.1, 1.35 + pulse, 0.6); cam.lookAt(0, 1.35, 0);
      E.render(X.scene, cam, XLOOK); blit();
      const [lx, ly] = screen(V3(0.05, 1.35, 0.02), cam);
      label('SYNOVIAL FLUID', 740, 520, lx, ly, eob(seg(lt, 0.2, 0.5)));
    } });
    cue(st, 'whoosh'); cue(st + 0.2, 'slide', { dur: 1.0 }); }

  // 4 · When you bend finger: pressure drops
  { const st = cut(3);
    add({ id: 'S04', at: st, note: 'stretching joint: pressure drops', draw(lt, d, t, blit) {
      reset();
      cam.position.copy(lerpV(V3(0.25, 1.35, 0.6), V3(0.1, 1.35, 0.45), eio(lt / d))); cam.lookAt(0, 1.35, 0);
      E.render(X.scene, cam, XLOOK); blit();
      pill('PRESSURE DROPS ↓', 540, 330, eob(seg(lt, 0.1, 0.35)), '#4FD1E8');
    } });
    cue(st, 'whoosh'); }

  // 5 · Gas bubbles rapidly form (macro vessel / fluid stage)
  { const st = cut(4);
    add({ id: 'S05', at: st, note: 'fluid cavitation bubbles forming', draw(lt, d, t, blit) {
      VS.update(t, -lt * 1.0, 0.8, 0);
      cam.position.set(0, 0, -lt * 1.0); cam.lookAt(0.1, 0, -lt * 1.0 - 5);
      E.render(VS.scene, cam, VLOOK); blit();
      pill('CAVITATION: GAS BUBBLES', 540, 330, eob(seg(lt, 0.15, 0.45)), '#CFE3EA');
    } });
    cue(st, 'whoosh'); cue(st + 0.1, 'bubbles', { dur: 1.2 }); }

  // 6 · That loud POP is gas cavities forming
  { const st = cut(5);
    add({ id: 'S06', at: st, note: 'bubble expands and POP!', draw(lt, d, t, blit) {
      VS.update(t, -lt * 0.5, 1.0, 0);
      cam.position.set(0, 0, -lt * 0.5); cam.lookAt(0, 0, -lt * 0.5 - 4);
      E.render(VS.scene, cam, VLOOK); blit();
      pill('LOUD POP! 💥', 540, 330, eob(seg(lt, 0.05, 0.3)), '#FF5A5A');
    } });
    cue(st, 'whoosh'); cue(st + 0.1, 'slam', { gain: 0.9 }); cue(st + 0.15, 'pop', { gain: 0.9 }); }

  // 7 · Does NOT cause arthritis (hero smiling)
  { const st = cut(6);
    add({ id: 'S07', at: st, note: 'hero smiles: does not cause arthritis', draw(lt, d, t, blit) {
      reset(); hero.pose({ head: [-3, 6, 0], lid: -0.2, look: [0, 0] });
      cam.position.copy(lerpV(V3(0.3, 1.7, 0.8), V3(0.1, 1.65, 0.5), eio(lt / d))); cam.lookAt(FACE);
      kitchenRender(1.0); blit();
      pill('ARTHRITIS RISK: 0% ✓', 540, 330, eob(seg(lt, 0.15, 0.45)), '#7CF29A');
    } });
    cue(st, 'whoosh'); cue(st + 0.2, 'pop', { gain: 0.6 }); }

  // 8 · Takes 20 minutes to dissolve back
  { const st = cut(7);
    add({ id: 'S08', at: st, note: 'timer 20 minutes countdown', draw(lt, d, t, blit) {
      reset(); hero.pose({ head: [0, 0, 0] });
      cam.position.set(0.1, 1.62, 0.65); cam.lookAt(FACE);
      kitchenRender(1.1); blit();
      pill('WAIT 20 MIN TO RE-POP', 540, 1150, eob(seg(lt, 0.2, 0.5)), '#FFD43B');
    } });
    cue(st, 'whoosh'); cue(st + 0.2, 'tock'); }

  return { shots: S, cues: CUES };
}
'''


def get_seawater_shots() -> str:
    return '''import * as THREE from 'three';
import { ctx, W, H, clamp, lerp, seg, eo, eio, eob } from './core/lib.js';
import { L, Wd, T } from './core/timing.js';
import { camera } from './core/engine.js';
import { Human } from './core/human.js';
import * as SETS from './core/sets.js';
import { label, pill, warning } from './core/look2d.js';

const V3 = (x, y, z) => new THREE.Vector3(x, y, z);
const lerpV = (a, b, k) => a.clone().lerp(b, k);
function screen(p, cam) { const v = p.clone().project(cam); return [(v.x + 1) / 2 * W, (1 - v.y) / 2 * H]; }

export function buildShots(E) {
  const S = [], CUES = [], add = (o) => (S.push(o), o), cue = (t, type, o = {}) => CUES.push({ t: +t.toFixed(3), type, ...o });
  const cut = (i) => (i === 0 ? 0 : L(i) - 0.08);
  const cam = camera(30);
  const KLOOK = { aperture: 0, bloom: 0.2 }, XLOOK = { aperture: 0, bloom: 0.45, vignette: 0.45 }, VLOOK = { aperture: 0, bloom: 0.5 };

  const K = SETS.kitchen(E), hero = new Human({}); hero.group.position.set(0.1, 0, -0.6); K.scene.add(hero.group);
  const X = SETS.xrayStage(E), xh = new Human({}), xmat = SETS.xrayMaterial(); xh.setBodyMaterial(xmat); const I = SETS.insides(); xh.spine.add(I.group); X.scene.add(xh.group);
  const VS = SETS.vessel(E);
  const CYAN = new THREE.Color('#4FD1E8'), RED = new THREE.Color('#FF3B3B');
  const FACE = V3(0.1, 1.68, -0.6);

  const reset = () => { hero.pose({}); xh.pose({}); xmat.uniforms.uCol.value.copy(CYAN); };
  const kitchenRender = (focus, extra = {}) => E.render(K.scene, cam, { ...KLOOK, ...extra });

  // 1 · HOOK: stranded at sea drinking water
  { const st = cut(0);
    add({ id: 'S01', at: st, note: 'hero drinking seawater in desperation', draw(lt, d, t, blit) {
      reset(); const k = eo(seg(lt, 0.1, 1.2));
      hero.pose({ head: [-8 * k, 0, 0], spine: [-3 * k, 0, 0], lid: -0.2 });
      cam.position.copy(lerpV(V3(0.35, 1.7, 0.55), V3(0.15, 1.68, 0.2), eio(lt / d))); cam.lookAt(FACE);
      kitchenRender(1.0); blit();
      pill('DRINKING SEAWATER', 540, 330, eob(seg(lt, 0.15, 0.45)), '#FFD43B');
    } });
    cue(st + 0.2, 'gulp', { dur: 0.8 }); }

  // 2 · Terrifying reason why
  { const st = cut(1);
    add({ id: 'S02', at: st, note: 'hero shocked look', draw(lt, d, t, blit) {
      reset(); hero.pose({ head: [2, 0, 0], lid: -0.4 });
      cam.position.set(0.1, 1.65, 0.65); cam.lookAt(FACE);
      kitchenRender(1.2); blit();
      warning(540, 1150, eob(seg(lt, 0.2, 0.5)));
    } });
    cue(st, 'whoosh'); cue(st + 0.15, 'alarm', { gain: 0.5 }); }

  // 3 · 4 times saltier than blood (blood vessel)
  { const st = cut(2);
    add({ id: 'S03', at: st, note: 'blood vessel salt concentration', draw(lt, d, t, blit) {
      VS.update(t, -lt * 1.2, 0.3, 0.2);
      cam.position.set(0, 0, -lt * 1.2); cam.lookAt(0.1, 0, -lt * 1.2 - 5);
      E.render(VS.scene, cam, VLOOK); blit();
      pill('4x SALTIER THAN BLOOD', 540, 330, eob(seg(lt, 0.15, 0.45)), '#FF5A5A');
    } });
    cue(st, 'whoosh'); }

  // 4 · Sodium floods bloodstream
  { const st = cut(3);
    add({ id: 'S04', at: st, note: 'salt crystals flooding bloodstream', draw(lt, d, t, blit) {
      VS.update(t, -lt * 1.5, 0.7, 0.5);
      cam.position.set(Math.sin(lt) * 0.1, 0, -lt * 1.5); cam.lookAt(0, 0, -lt * 1.5 - 5);
      E.render(VS.scene, cam, VLOOK); blit();
      pill('SODIUM SPIKE ↑↑', 540, 330, eob(seg(lt, 0.1, 0.35)), '#FFA500');
    } });
    cue(st, 'whoosh'); cue(st + 0.2, 'bubbles', { dur: 1.0 }); }

  // 5 · Kidneys desperately try to flush salt
  { const st = cut(4);
    add({ id: 'S05', at: st, note: 'x-ray: kidneys filtering', draw(lt, d, t, blit) {
      reset();
      cam.position.copy(lerpV(V3(0.4, 1.25, 1.1), V3(0.2, 1.15, 0.8), eio(lt / d))); cam.lookAt(0, 1.1, 0);
      E.render(X.scene, cam, XLOOK); blit();
      const [lx, ly] = screen(V3(0.08, 1.12, 0.05), cam);
      label('KIDNEYS: FILTERING', 740, 520, lx, ly, eob(seg(lt, 0.2, 0.5)));
    } });
    cue(st, 'whoosh'); cue(st + 0.2, 'slide', { dur: 1.0 }); }

  // 6 · Kidneys can only make less salty urine
  { const st = cut(5);
    add({ id: 'S06', at: st, note: 'x-ray: kidney limit reached', draw(lt, d, t, blit) {
      reset(); xmat.uniforms.uCol.value.copy(CYAN).lerp(RED, 0.4);
      cam.position.set(0.15, 1.15, 0.75); cam.lookAt(0, 1.1, 0);
      E.render(X.scene, cam, XLOOK); blit();
      pill('MAX SALINITY REACHED', 540, 330, eob(seg(lt, 0.1, 0.35)), '#FF4D4D');
    } });
    cue(st, 'whoosh'); cue(st + 0.2, 'thud'); }

  // 7 · Body pulls water from living cells
  { const st = cut(6);
    add({ id: 'S07', at: st, note: 'cells shrinking: dehydration', draw(lt, d, t, blit) {
      VS.update(t, -lt * 0.8, 0.9, 0.8);
      cam.position.set(0, 0, -lt * 0.8); cam.lookAt(0, 0, -lt * 0.8 - 4);
      E.render(VS.scene, cam, VLOOK); blit();
      pill('CELLS DEHYDRATING', 540, 330, eob(seg(lt, 0.15, 0.4)), '#FF5A5A');
    } });
    cue(st, 'whoosh'); cue(st + 0.1, 'alarm', { dur: 1.2 }); }

  // 8 · Cells shrink, organs fail
  { const st = cut(7);
    add({ id: 'S08', at: st, note: 'x-ray: full body red alarm', draw(lt, d, t, blit) {
      reset(); xmat.uniforms.uCol.value.copy(RED);
      xh.pose({ head: [-5, 0, 0], spine: [6, 0, 0], lid: 0.3 });
      cam.position.copy(lerpV(V3(0, 1.5, 1.8), V3(0, 1.45, 1.2), eio(lt / d))); cam.lookAt(0, 1.35, 0);
      E.render(X.scene, cam, XLOOK); blit();
      pill('ORGAN FAILURE RISK', 540, 1180, eob(seg(lt, 0.2, 0.5)), '#FF3B3B');
    } });
    cue(st, 'whoosh'); cue(st + 0.2, 'alarm', { gain: 0.8 }); }

  // 9 · Extreme dehydration twice as fast
  { const st = cut(8);
    add({ id: 'S09', at: st, note: 'hero collapses from dehydration', draw(lt, d, t, blit) {
      reset(); hero.pose({ head: [14, 0, 0], spine: [8, 0, 0], lid: 0.9 });
      cam.position.set(0.1, 1.58, 0.7); cam.lookAt(FACE);
      kitchenRender(1.1); blit();
      warning(540, 1150, eob(seg(lt, 0.2, 0.5)));
    } });
    cue(st, 'whoosh'); cue(st + 0.2, 'slam', { gain: 0.8 }); }

  return { shots: S, cues: CUES };
}
'''


def get_sneeze_shots() -> str:
    return '''import * as THREE from 'three';
import { ctx, W, H, clamp, lerp, seg, eo, eio, eob } from './core/lib.js';
import { L, Wd, T } from './core/timing.js';
import { camera } from './core/engine.js';
import { Human } from './core/human.js';
import * as SETS from './core/sets.js';
import { label, pill, warning } from './core/look2d.js';

const V3 = (x, y, z) => new THREE.Vector3(x, y, z);
const lerpV = (a, b, k) => a.clone().lerp(b, k);
function screen(p, cam) { const v = p.clone().project(cam); return [(v.x + 1) / 2 * W, (1 - v.y) / 2 * H]; }

export function buildShots(E) {
  const S = [], CUES = [], add = (o) => (S.push(o), o), cue = (t, type, o = {}) => CUES.push({ t: +t.toFixed(3), type, ...o });
  const cut = (i) => (i === 0 ? 0 : L(i) - 0.08);
  const cam = camera(30);
  const KLOOK = { aperture: 0, bloom: 0.2 }, XLOOK = { aperture: 0, bloom: 0.45, vignette: 0.45 }, VLOOK = { aperture: 0, bloom: 0.5 };

  const K = SETS.kitchen(E), hero = new Human({}); hero.group.position.set(0.1, 0, -0.6); K.scene.add(hero.group);
  const X = SETS.xrayStage(E), xh = new Human({}), xmat = SETS.xrayMaterial(); xh.setBodyMaterial(xmat); const I = SETS.insides(); xh.spine.add(I.group); X.scene.add(xh.group);
  const VS = SETS.vessel(E);
  const CYAN = new THREE.Color('#4FD1E8'), RED = new THREE.Color('#FF3B3B');
  const FACE = V3(0.1, 1.68, -0.6);

  const reset = () => { hero.pose({}); xh.pose({}); xmat.uniforms.uCol.value.copy(CYAN); };
  const kitchenRender = (focus, extra = {}) => E.render(K.scene, cam, { ...KLOOK, ...extra });

  // 1 · HOOK: hero pinching nose shut, about to sneeze
  { const st = cut(0);
    add({ id: 'S01', at: st, note: 'hero pinching nose shut', draw(lt, d, t, blit) {
      reset(); const k = eo(seg(lt, 0.1, 1.2));
      hero.pose({ head: [-6 * k, 0, 0], shR: [18 * k, -12 * k, 35 * k], elR: [-55 * k, 0, 0], lid: -0.2 });
      cam.position.copy(lerpV(V3(0.35, 1.7, 0.55), V3(0.18, 1.68, 0.2), eio(lt / d))); cam.lookAt(FACE);
      kitchenRender(1.0); blit();
      pill('PINCHING NOSE SHUT', 540, 330, eob(seg(lt, 0.15, 0.45)), '#FFD43B');
    } });
    cue(st, 'whoosh'); }

  // 2 · Dangerous habit: big red warning
  { const st = cut(1);
    add({ id: 'S02', at: st, note: 'shocked expression, warning', draw(lt, d, t, blit) {
      reset(); hero.pose({ head: [2, 0, 0], lid: -0.4 });
      cam.position.set(0.1, 1.65, 0.65); cam.lookAt(FACE);
      kitchenRender(1.2); blit();
      pill('DANGEROUS MISTAKE ✗', 540, 330, eob(seg(lt, 0.1, 0.35)), '#FF4D4D');
    } });
    cue(st, 'whoosh'); cue(st + 0.15, 'alarm', { gain: 0.6 }); }

  // 3 · Sneeze travels at 100 mph (X-ray head/chest)
  { const st = cut(2);
    add({ id: 'S03', at: st, note: 'x-ray: high speed blast buildup', draw(lt, d, t, blit) {
      reset();
      cam.position.copy(lerpV(V3(0.35, 1.6, 1.1), V3(0.15, 1.5, 0.7), eio(lt / d))); cam.lookAt(0, 1.45, 0);
      E.render(X.scene, cam, XLOOK); blit();
      const [lx, ly] = screen(V3(0.06, 1.5, 0.05), cam);
      label('100 MPH AIR PRESSURE', 740, 520, lx, ly, eob(seg(lt, 0.2, 0.5)));
    } });
    cue(st, 'whoosh'); cue(st + 0.2, 'slide', { dur: 1.0 }); }

  // 4 · When you clamp your mouth and nose: pressure redirected
  { const st = cut(3);
    add({ id: 'S04', at: st, note: 'air trapped inside head cavities', draw(lt, d, t, blit) {
      reset();
      cam.position.copy(lerpV(V3(0.25, 1.6, 0.6), V3(0.1, 1.6, 0.4), eio(lt / d))); cam.lookAt(0, 1.6, 0);
      E.render(X.scene, cam, XLOOK); blit();
      pill('PRESSURE REDIRECTED INWARD', 540, 330, eob(seg(lt, 0.1, 0.35)), '#FFA500');
    } });
    cue(st, 'whoosh'); }

  // 5 · Forces air up eustachian tubes into ears
  { const st = cut(4);
    add({ id: 'S05', at: st, note: 'air rushing up eustachian tubes', draw(lt, d, t, blit) {
      VS.update(t, -lt * 2.0, 0.8, 0.3);
      cam.position.set(0, 0, -lt * 2.0); cam.lookAt(0.1, 0, -lt * 2.0 - 5);
      E.render(VS.scene, cam, VLOOK); blit();
      pill('FORCED INTO EAR CANALS', 540, 330, eob(seg(lt, 0.15, 0.45)), '#FF5A5A');
    } });
    cue(st, 'whoosh'); cue(st + 0.15, 'bubbles', { dur: 1.0 }); }

  // 6 · Can rupture eardrums (X-ray alarm)
  { const st = cut(5);
    add({ id: 'S06', at: st, note: 'x-ray: ruptured eardrum danger', draw(lt, d, t, blit) {
      reset(); xmat.uniforms.uCol.value.copy(CYAN).lerp(RED, 0.6);
      cam.position.set(0.15, 1.62, 0.6); cam.lookAt(0, 1.62, 0);
      E.render(X.scene, cam, XLOOK); blit();
      pill('RUPTURED EARDRUM RISK', 540, 330, eob(seg(lt, 0.08, 0.35)), '#FF3B3B');
    } });
    cue(st, 'whoosh'); cue(st + 0.15, 'slam', { gain: 0.9 }); }

  // 7 · Extreme cases: torn throat tissue
  { const st = cut(6);
    add({ id: 'S07', at: st, note: 'x-ray: neck/pharynx stress', draw(lt, d, t, blit) {
      reset(); xmat.uniforms.uCol.value.copy(RED);
      cam.position.copy(lerpV(V3(0.2, 1.5, 0.7), V3(0.1, 1.48, 0.45), eio(lt / d))); cam.lookAt(0, 1.48, 0);
      E.render(X.scene, cam, XLOOK); blit();
      const [lx, ly] = screen(V3(0.04, 1.48, 0.05), cam);
      label('THROAT TISSUE TEAR', 740, 520, lx, ly, eob(seg(lt, 0.2, 0.5)));
    } });
    cue(st, 'whoosh'); cue(st + 0.2, 'alarm', { gain: 0.8 }); }

  // 8 · Always sneeze freely into elbow or tissue
  { const st = cut(7);
    add({ id: 'S08', at: st, note: 'hero sneezes freely with relief', draw(lt, d, t, blit) {
      reset(); hero.pose({ head: [-3, 6, 0], lid: -0.2, look: [0, 0] });
      cam.position.copy(lerpV(V3(0.3, 1.7, 0.8), V3(0.1, 1.65, 0.5), eio(lt / d))); cam.lookAt(FACE);
      kitchenRender(1.0); blit();
      pill('SNEEZE FREELY! ✓', 540, 330, eob(seg(lt, 0.15, 0.45)), '#7CF29A');
    } });
    cue(st, 'whoosh'); cue(st + 0.2, 'pop', { gain: 0.6 }); }

  return { shots: S, cues: CUES };
}
'''


# ─────────────────────────────────────────────────────────────────────────────
# GEMINI DYNAMIC THREE.JS SCENE DIRECTOR
# ─────────────────────────────────────────────────────────────────────────────

def generate_dynamic_shots_js(gemini_api_key: str, script_data: dict, target_path: Path) -> bool:
    """
    Directs Gemini to write a custom, perfectly synchronized shots.js
    matching the exact sentences and topic of the generated script.
    """
    title = script_data.get("title", "")
    lines = script_data.get("lines", [])
    num_lines = len(lines)

    # 1. First check if it matches a curated topic
    title_lower = title.lower()
    if "gum" in title_lower or "chewing" in title_lower:
        print("[DIRECTOR] Applying curated 3D scene choreography: CHEWING GUM")
        target_path.write_text(get_chewing_gum_shots(), encoding="utf-8")
        return True
    elif "knuckle" in title_lower or "crack" in title_lower:
        print("[DIRECTOR] Applying curated 3D scene choreography: KNUCKLE CRACKING")
        target_path.write_text(get_knuckle_shots(), encoding="utf-8")
        return True
    elif "sea" in title_lower or "water" in title_lower or "salt" in title_lower or "ocean" in title_lower:
        print("[DIRECTOR] Applying curated 3D scene choreography: SEAWATER TOXICITY")
        target_path.write_text(get_seawater_shots(), encoding="utf-8")
        return True
    elif "sneeze" in title_lower:
        print("[DIRECTOR] Applying curated 3D scene choreography: HOLDING IN SNEEZE")
        target_path.write_text(get_sneeze_shots(), encoding="utf-8")
        return True

    # 2. If not a pre-authored topic and Gemini API key is available, generate custom Three.js shots!
    if gemini_api_key:
        lines_summary = "\\n".join([f"Line {i}: {ln['text']}" for i, ln in enumerate(lines)])
        prompt = f"""You are the master 3D Animation Director for Zack D. Films style YouTube Shorts.
You need to write the complete JavaScript file `shots.js` using Three.js to animate the 3D scene for this short:

Topic: {title}
Lines ({num_lines} lines total):
{lines_summary}

AVAILABLE 3D ASSETS IN SCOPE:
- `K.scene` with `hero` (Human): Real-world setting with floor and lighting. Use `kitchenRender(focus, extra)`.
- `X.scene` with `xh` (Human X-Ray) and `I` (insides: I.spine, I.heart, I.stomach, I.lungs): Medical x-ray scanning stage. Use `E.render(X.scene, cam, XLOOK)`.
- `VS.scene`: Microscopic blood vessel / cellular tunnel. Call `VS.update(t, camZ, co2, dark)` and render with `E.render(VS.scene, cam, VLOOK)`.
- `pill('TEXT', 540, 330, scale, color)`: Floating 3D status badge.
- `label('NAME', 740, 520, lx, ly, scale)`: 3D tracking label with line pointer.
- `warning(540, 1150, scale)`: Yellow triangular hazard badge.
- Audio cues: `cue(st, 'whoosh')`, `cue(st + 0.15, 'pop')`, `cue(st + 0.2, 'thud')`, `cue(st + 0.2, 'alarm')`, `cue(st, 'bubbles')`, `cue(st, 'slide')`, `cue(st, 'gulp')`.

CODE TEMPLATE REQUIREMENTS:
Output ONLY valid JavaScript starting with imports and exporting buildShots(E).
Create exactly {num_lines} shots (S01 to S{num_lines:02d}), where shot `i` has `at: cut({i})`.
Ensure every shot has `draw(lt, d, t, blit)` and ends with `blit()`.
Keep `aperture: 0` in looks for clean render.
Do NOT use markdown code fences. Output purely the JavaScript code.
"""

        candidate_models = ["gemini-2.0-flash", "gemini-1.5-flash", "gemini-1.5-flash-latest"]
        for model in candidate_models:
            try:
                url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={gemini_api_key}"
                payload = json.dumps({
                    "contents": [{"parts": [{"text": prompt}]}],
                    "generationConfig": {"temperature": 0.4}
                }).encode("utf-8")
                req = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json"}, method="POST")
                with urllib.request.urlopen(req, timeout=35) as resp:
                    res_data = json.loads(resp.read().decode("utf-8"))
                code = res_data["candidates"][0]["content"]["parts"][0]["text"].strip()
                # Strip markdown code blocks if present
                code = re.sub(r"^```(?:javascript|js)?\s*", "", code, flags=re.IGNORECASE)
                code = re.sub(r"\s*```$", "", code)
                if "export function buildShots" in code and "cut(" in code:
                    print(f"[SUCCESS] Gemini ({model}) authored custom 3D choreography in shots.js!")
                    target_path.write_text(code, encoding="utf-8")
                    return True
            except urllib.error.HTTPError as he:
                body = he.read().decode("utf-8", errors="ignore")
                print(f"[WARN] Gemini director model {model} attempt failed: {he} - {body[:150]}")
            except Exception as e:
                print(f"[WARN] Gemini director model {model} attempt failed: {e}")

    # Fallback to general scientific medical choreography
    print("[DIRECTOR] Falling back to modular scientific 3D choreography")
    target_path.write_text(get_knuckle_shots(), encoding="utf-8")
    return True
