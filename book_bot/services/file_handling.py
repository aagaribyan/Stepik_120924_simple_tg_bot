BOOK_PATH = 'book/book.txt'
PAGE_SIZE = 1050

book: dict[int, int] = {}


# функция, возвращающая строку с текстом страницы и её размер
def _get_part_text(text: str, start: int, size: int) -> tuple[int, int]:
    if len(text) <= size + start:
        size = len(text) - start
    
    part = text[start: start + size]

    if part[-1] in '.?!' and len(text) > start + size and text[start + size] == '.':
        if part[-2] == '.':
            part = part[:-3]
        else:
            part = part[:-2]

    for i, letter in enumerate(part[::-1]):
        if letter in '.,!?:;':
            break
    else:
        i = 0

    if i != 0:
        part = part[:-i]

    return part, len(part)


# функция, формирующая словарь книги
def prepare_book(path: str) -> None:
    with open(path, 'r', encoding='UTF-8') as file:
        f_book = file.read()
        page = 1
        curs = 0

        while curs < len(f_book):
            page_text, page_end = _get_part_text(f_book, curs, PAGE_SIZE)
            curs += page_end

            book[page] = page_text.lstrip()
            page += 1


# вызов функции prepare_book для подготовки книги из текстового файла
prepare_book(BOOK_PATH)


