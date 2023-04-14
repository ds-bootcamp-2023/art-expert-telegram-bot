def start(name: str) -> str:
    return (
        f"Hello {name}.\n\n"
        "We are Chat Art Project © – world's most authoritative arts appraisal company established  in 1809.\n\n"
        "You can send us an image of piece of art and get it's value estimated by our most experienced specialists.\n\n"
        "We may also offer you some exclusive lots if your taste for the art proves to be worthy."
    )


def image_description(price: float, caption: str) -> str:
    return f'<b>"{caption.capitalize()}"</b>\n' f"Price: <b>${price:.2f}</b>\n"


def similar_image_description(price: float) -> str:
    return (
        f"❗<b>ONLY TODAY</b> you can get <b>THIS BAD BOY</b> just for <b>${price:.2f}</b>❗\n\n"
        '💎💎💎<a href="https://tinyurl.com/4ub9r2wj">BUY NOW</a>💎💎💎'
    )


def meme_prelude() -> str:
    return (
        "Наши сммщики говорт, что пользователей привлекает\n\n<b>💅💅💅контент💅💅💅</b>\n\n"
        "так что мы решили добавить\n\n<b>💅💅💅контент💅💅💅</b>\n\n"
        "Доставка <b>💅💅💅контента💅💅💅</b> через 3..2..1.."
    )
