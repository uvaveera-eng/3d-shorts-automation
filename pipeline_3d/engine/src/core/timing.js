// Timing: everything on screen is placed on the narration's clock.
//   data/lines.json  { duration, lines: [{ i, text, start, end }] }   (voice.py, or estimate.py for captions-only)
//   data/words.json  [{ w, line, s, e }]                                (words.py, or estimate.py)
// L(i) = line i start · Le(i) = line i end · Wd(word, line) = start of the first word in that line matching
// the prefix (case/punctuation ignored; throws if it isn't there, so a rewritten script can't silently drift).
export const T = { dur: 0, lines: [], words: [] };
const norm = (w) => String(w).toLowerCase().replace(/[^a-z0-9']+/g, '');

export async function loadTiming() {
  const get = async (f) => { const r = await fetch(f, { cache: 'no-store' }); if (!r.ok) throw new Error(`missing ${f}: run voice.py + words.py (or estimate.py)`); return r.json(); };
  const lines = await get('data/lines.json'), words = await get('data/words.json');
  T.lines = lines.lines; T.words = words; T.dur = lines.duration;
  return T;
}
export const L = (i) => {
  const l = T.lines[i];
  if (!l) {
    if (T.lines.length > 0) {
      const last = T.lines[T.lines.length - 1];
      return Math.min(T.dur || 30, last.end + (i - T.lines.length + 1) * 2.0);
    }
    return i * 3.0;
  }
  return l.start;
};
export const Le = (i) => {
  const l = T.lines[i];
  if (!l) return (T.dur || 30);
  return l.end;
};
export function Wd(word, line, which = 's') {
  const n = norm(word);
  const hit = T.words.find((w) => (line == null || w.line === line) && norm(w.w).startsWith(n));
  if (!hit) {
    const lw = lineWords(line);
    if (lw && lw.length) return lw[Math.floor(lw.length / 2)][which] || lw[0][which];
    return T.lines && T.lines[line] ? T.lines[line].start : 0;
  }
  return hit[which];
}
export const lineWords = (i) => T.words.filter((w) => w.line === i);
