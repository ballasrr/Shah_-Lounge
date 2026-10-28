// Меню «Шах Lounge». Цены в рублях.
// price: одно число или [малый, большой] / [объём 1, объём 2]; sizes — подписи столбцов цен.

export type Price = number | [number, number]

export interface MenuItem {
  name: string
  price: Price
  note?: string
}

export interface MenuGroup {
  title: string
  sizes?: string | [string, string]
  items: MenuItem[]
}

export interface MenuTab {
  id: string
  label: string
  groups: MenuGroup[]
}

export const menu: MenuTab[] = [
  {
    id: 'coffee',
    label: 'Кофе',
    groups: [
      {
        title: 'Чёрный кофе',
        items: [
          { name: 'Эспрессо', price: 200 },
          { name: 'Американо', price: 200 },
          { name: 'Гранатовый тоник', price: 330 }
        ]
      },
      {
        title: 'Кофе с молоком',
        items: [
          { name: 'Капучино', price: [250, 280], note: 'малый / большой' },
          { name: 'Латте', price: 280, note: '350 мл' },
          { name: 'Флэт уайт', price: 280, note: '250 мл' },
          { name: 'Мокачино', price: 300 }
        ]
      },
      {
        title: 'Холодный кофе',
        items: [
          { name: 'Айс латте', price: 300 },
          { name: 'Айс кофе', price: 350 },
          { name: 'Айс кофе с урбечем / арахисом', price: 380 },
          { name: 'Бамбл', price: 350 },
          { name: 'Бамбл щавель-апельсин', price: 380 },
          { name: 'Колд брю', price: 300, note: 'гранат / вишня / малина' }
        ]
      },
      {
        title: 'Десертный кофе',
        items: [
          { name: 'Раф классический', price: 350 },
          { name: 'Раф солёная карамель', price: 350 },
          { name: 'Раф урбеч', price: 380 },
          { name: 'Раф арахис', price: 380 }
        ]
      },
      {
        title: 'Не кофе',
        items: [
          { name: 'Айс какао', price: 280 },
          { name: 'Какао', price: 280 },
          { name: 'Горячий шоколад', price: 330 }
        ]
      }
    ]
  },
  {
    id: 'tea',
    label: 'Чай',
    groups: [
      {
        title: 'Чаи', sizes: '1,2 л',
        items: [
          { name: 'Чёрный чай (Ассам)', price: 260 },
          { name: 'Зелёный чай (Сенча)', price: 260 },
          { name: 'Сбор трав', price: 260 },
          { name: 'Фруктовый чай «Наглый фрукт»', price: 260 },
          { name: 'Таёжный сбор', price: 260 }
        ]
      },
      {
        title: 'Авторские чаи', sizes: ['500 мл', '900 мл'],
        items: [
          { name: 'Облепиховый', price: [350, 400] },
          { name: 'Марокканский', price: [350, 400] },
          { name: 'Манго-маракуйя', price: [350, 400] },
          { name: 'Ягодный', price: [350, 400] },
          { name: 'Малина-имбирь', price: [350, 400] },
          { name: 'Лимон-имбирь', price: [350, 400] }
        ]
      },
      {
        title: 'Глинтвейн',
        items: [
          { name: 'Глинтвейн', price: 350, note: '300 мл' }
        ]
      },
      {
        title: 'Допы к чаю',
        items: [
          { name: 'Чабрец', price: 40 },
          { name: 'Гвоздика', price: 40 },
          { name: 'Мята', price: 40 },
          { name: 'Имбирь', price: 40 },
          { name: 'Лимон', price: 40 }
        ]
      },
      {
        title: 'К чаю', sizes: '100 г',
        items: [
          { name: 'Варенье клубничное', price: 180 },
          { name: 'Варенье малиновое', price: 180 },
          { name: 'Варенье инжирное', price: 180 },
          { name: 'Варенье из белой черешни', price: 180 },
          { name: 'Мёд', price: 150 },
          { name: 'Мёд с орехами', price: 180 },
          { name: 'Сухофрукты', price: 220 },
          { name: 'Финики', price: 150 },
          { name: 'Плитка шоколада', price: 180 },
          { name: 'Шоколад Ritter Sport', price: 100 },
          { name: 'Мини Ritter Sport', price: 50 },
          { name: 'Печенье «Кофе Джой»', price: 150 }
        ]
      }
    ]
  },
  {
    id: 'drinks',
    label: 'Коктейли и фреши',
    groups: [
      {
        title: 'Лимонады', sizes: ['500 мл', '1,5 л'],
        items: [
          { name: 'Голубая лагуна', price: [320, 600] },
          { name: 'Манго-маракуйя', price: [320, 600] },
          { name: 'Щавелевый', price: [320, 600] },
          { name: 'Мохито', price: [320, 600] },
          { name: 'Мохито клубничный', price: [320, 600] },
          { name: 'Ягодный', price: [320, 600] }
        ]
      },
      {
        title: 'Молочные коктейли',
        items: [
          { name: 'Коктейль «Шах»', price: 350 },
          { name: 'Молочный', price: 300 },
          { name: 'Шоколадный', price: 300 },
          { name: 'Банановый', price: 300 },
          { name: 'Шоколадно-банановый', price: 330 },
          { name: 'Клубничный', price: 300 },
          { name: 'Чернично-банановый', price: 330 },
          { name: 'Орео', price: 330 },
          { name: 'Протеиновый', price: 350 }
        ]
      },
      {
        title: 'Смузи',
        items: [
          { name: 'Фруктовый микс', price: 400 },
          { name: 'Пеликан', price: 400 }
        ]
      },
      {
        title: 'Фреши',
        items: [
          { name: 'Апельсин', price: 330 },
          { name: 'Гранат', price: 450 },
          { name: 'Грейпфрут', price: 330 },
          { name: 'Яблоко', price: 330 }
        ]
      },
      {
        title: 'Шоты',
        items: [
          { name: 'Эспрессо шот', price: 500 },
          { name: 'Витаминный шот', price: 450 },
          { name: 'Шах-шот', price: 550 }
        ]
      }
    ]
  },
  {
    id: 'soft',
    label: 'Напитки',
    groups: [
      {
        title: 'Энергетики',
        items: [
          { name: 'Adrenaline Rush', price: [180, 230], note: '300 / 500 мл' },
          { name: 'Red Bull', price: [200, 250], note: '300 / 500 мл' },
          { name: 'Gorilla Energy', price: 150, note: '500 мл' },
          { name: 'LIT Energy', price: 150, note: '500 мл' }
        ]
      },
      {
        title: 'Газировка и вода',
        items: [
          { name: 'Barbican', price: 200 },
          { name: 'Kinza', price: 120 },
          { name: 'Кола (стекло)', price: 180 },
          { name: 'Кола / Фанта / Спрайт', price: 100 },
          { name: 'Менди', price: 120 },
          { name: 'Боржоми', price: 200 },
          { name: 'Рычал-Су', price: 150 },
          { name: 'Минеральная вода «Махачкала»', price: 100 },
          { name: 'Вода', price: 150 }
        ]
      },
      {
        title: 'Соки',
        items: [
          { name: 'Натуральный сок (стекло)', price: 100 },
          { name: 'Натуральный сок', price: 250, note: '1 л' }
        ]
      }
    ]
  }
]
