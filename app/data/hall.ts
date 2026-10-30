// Схема зала: положение столов и места. В iiko этого нет: там только номера столов, а места указаны как 0.
// x, y — центр стола, w, h — размер; всё в процентах от плана. Вход внизу справа.

export interface HallTable { number: number; zone: string; seats: number; x: number; y: number; w: number; h: number; title?: string; tv?: boolean }

export const hallTables: HallTable[] = [
  { number: 1, zone: 'Общий зал', seats: 6, x: 11, y: 10, w: 15, h: 12 },
  { number: 2, zone: 'Общий зал', seats: 4, x: 11, y: 37, w: 15, h: 12 },
  { number: 3, zone: 'Общий зал', seats: 4, x: 37, y: 37, w: 15, h: 12 },
  { number: 4, zone: 'Общий зал', seats: 6, x: 37, y: 10, w: 15, h: 12 },
  { number: 5, zone: 'Зона бара', seats: 6, x: 70, y: 60, w: 15, h: 13, tv: true },
  { number: 6, zone: 'Шатры', seats: 6, x: 93, y: 58, w: 12, h: 13 },
  { number: 7, zone: 'Шатры', seats: 4, x: 93, y: 79, w: 12, h: 13 },
  { number: 8, zone: 'Игровая зона', seats: 4, x: 68, y: 11, w: 12, h: 12 },
  { number: 9, zone: 'Игровая зона', seats: 4, x: 87, y: 11, w: 12, h: 12 },
  { number: 10, zone: 'Игровая зона', seats: 4, x: 68, y: 35, w: 12, h: 12 },
  { number: 11, zone: 'Игровая зона', seats: 4, x: 87, y: 35, w: 12, h: 12 },
  // в iiko 12 столов, а на схеме 11 и бильярд: считаем, что стол 12 в iiko — это бильярд
  { number: 12, zone: 'Общий зал', seats: 8, x: 34, y: 77, w: 30, h: 23, title: 'Бильярд' }
]

// подписи зон и стены: left, top, width, height в процентах
export const hallZones = [
  { name: 'Общий зал', x: 2, y: 52 },
  { name: 'Игровая зона', x: 49, y: 22 },
  { name: 'Зона бара', x: 49, y: 48 },
  { name: 'Шатры', x: 87, y: 47 }
]

export const hallWalls = [
  { x: 47, y: 0, w: 0.3, h: 45.7 }, // общий зал и игровая зона
  { x: 47, y: 45.7, w: 4, h: 0.5 }, // игровая зона и зона бара, в проёме 51–59 проход
  { x: 59, y: 45.7, w: 41, h: 0.5 },
  { x: 86, y: 45.7, w: 0.3, h: 43.5 }, // шатры
  { x: 86, y: 68, w: 14, h: 0.5 },
  { x: 86, y: 89, w: 14, h: 0.5 }
]
