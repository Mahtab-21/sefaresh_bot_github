def extract_data(text, products):
    """
    ورودی:
        text: متن کاربر
        products: دیکشنری محصولات

    خروجی:
        code, color
    """

    parts = text.strip().split()

    code = None
    color = None

    # اگر کاربر چیزی ننوشته
    if not parts:
        return None, None

    # اولین بخش رو به عنوان کد بگیر
    if parts[0] in products:
        code = parts[0]
    else:
        return None, None

    # اگر رنگ هم نوشته باشه
    if len(parts) > 1:
        possible_color = parts[1]
        if possible_color in products[code]["colors"]:
            color = possible_color

    return code, color
