from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, CallbackContext, MessageHandler, filters

# Список брендов
BRANDS = ['Is clinical', 'Skin Ceuticals', 'Allies of skin', 'SkinFix', 'Paula’s Choice', 'Instytutum', 'Ultraceuticals', 'Genosys', 'Sesderma', 'Sol de Janeiro', 'Dr.ceuracle', 'Comfort Zone', 'HydroPeptide', 'Другое...']

# Словарь с каталогами товаров для каждого бренда
PRODUCT_CATALOG = {
    'Is clinical': [
        'Active Serum', 'Pro Heal', 'Cleansing Complex', 'Brightening Serum', 'Water Honey Cleanser'
    ],
    'Skin Ceuticals': [
        'Phloretin CF', 'Advanced Brightening UV Defense Sunscreen', 'Daily Moisture', 'A.G.E. Interrupter', 'Emollience', 'Soothing Cleanser', 'Blemish + AGE Defense', 'Phyto Corrective', 'C E Republic', 'Serum 10', 'Retexturing Activator', 'Hydrating B5', 'Retinol 0.3'
    ],
    'Allies of skin': [
        'Molecular Multi-Nutrient Day Cream', 'Peptides & Antioxidants Firming Daily Treatment', 'Mandelic Pigmentation Corrector Night Serum', 'Vitamin C Brighten + Firm Serum', 'Retinal & Peptides Repair Night Cream', 'Vitamin C+ Perfecting Serum', 'Triple Hyaluronic Antioxidant Hydration Serum'
    ],
    'SkinFix': [
        'Foaming Oil Cleanser', 'Antioxidant Redness Treatment', 'Glycolic Renewing Scrub', 'Dermatitis Relief Balm', 'Acne Treatment Cream', 'Triple-Peptide Cream', 'Glycol Lactic Brightening Boost', 'Skin Barrier Restoring Gel Cream'
    ],
    'Paula’s Choice': [
        'Salicylic Acid', 'Vitamin C', 'Niacinamide Treatment', 'Earth Source', 'Salicylic Acid + Antioxidants', 'Pore-Reducing Toner', 'Optimal Results Hydrating Cleanser', 'Daily Smoothing Treatment', 'Retinol Treatment', 'Super-Light Daily Wrinkle Defense'
    ],
    'Instytutum': [
        'Eye Multi Tasker', 'Hydra Fusion', 'Super Biotic', 'A-Retinol', 'Retinol Toner', 'Super Serum', 'Firm Agic', 'Xceptional Flawless Cream', 'Sun Scription', 'Anti-Wrinkle Brightening', 'Melting Cleanser', 'Hydra Mist', 'Triple Action Peel', 'Powerful Retinoil', 'Truly-Transforming Brightening Eye Cream'
    ],
    'Ultraceuticals': [
        'Ultra UV Protective SPF 30', 'Ultra UV Protective SPF 50', 'Ultra Moisturiser Cream', 'Ultra DNA Complex Recovery Night Cream', 'Ultra Hydrating Lotion', 'Ultra Brightening Moisturiser Cream', 'Face & Body Recovery Cream', 'Ultra Protective Antioxidant Complex', 'Ultra Clear Foaming Cleanser', 'Ultra Moisturiser Eye Cream', 'Ultra Rich Moisturiser Cream'
    ],
    'Genosys': [
        'Intensive Problem Control Cream', 'Multi Sun Cream', 'Soothing Repair Postcream', 'Intensive Blemish Balm Cream', 'Snow O2', 'Skin Barrier Protecting Cream', 'Intensive Multi Functional Cream', 'Snow Booster', 'Intensive Hydro Soothing Cream', 'Multi Vita Radiance Cream', 'Skin Whitening Serum', 'Revitalizing Hydro Mist', 'Anti-Wrinkle Serum', 'All For Sensitive Serum', 'Professional Biphasic Makeup Remover', 'Problem Control Serum'
    ],
    'Sesderma': [
        'Acglicolic Classic', 'Resveraderm', 'Soberskin Smoothening Bath Gel', 'Soberskin Clarifying Bath Gel', 'Atopises Original Body Milk', 'C-Vit Radiance', 'Acnises Spot Colour Cream', 'Atopises Ultra Clarifying Essence', 'Reti Age Liposomal Serum', 'Hidraloe', 'Azelac', 'Sesgen 32', 'Atopises Body Lotion', 'Soberskin Brightening', 'Retises 0.15/0.25', 'Factor G'
    ],
    'Sol de Janeiro': [
        '40', '59', '62', '68', '71', 'Bum Bum Cream', 'Rio Radiance', 'Bom Dia Bright', 'Brazilian Play', 'After Hours', 'Hand Cream'
    ],
    'Dr.ceuracle': [
        'Vegan Kombucha Tea Essence', 'Cica Regen Vegan Sun', 'Royal Vita Propolis 33 Ampoule', 'Pro Balance Night Enzyme Wash', 'Jeju Matcha Clay Pack', 'Cica Regen 95 Soothing Gel', 'Pro Balance Biotics Toner', 'Tea Tree Purfine Green Up Sun', 'Hyal Reyouth Hydrogel Eye Mask', 'Purfine Cleansing Foam'
    ],
    'Comfort Zone': [
        'Revitalizing Tonic', 'Absolute Pearl Serum', 'Renight Oil', 'Sacred Nature Youth Serum', 'Renight Cream', 'Hydramemory Water Source Serum', 'Hydramemory Eye Gel', 'Tranquillity Oil', 'Essential Face Wash', 'Active Purness Mask', 'Hydramemory Essence', 'Sublime Skin Serum', 'Hydramemory Light Sorbet Cream', 'Hydramemory Rich Sorbet Cream', 'Sun Soul Age Gel', 'Sacred Nature Nutrient Cream', 'Hydramemory Mask', 'Hydramemory Serum', 'Skin Regimen Cleansing Cream', 'Skin Regimen HA Booster', 'Skin Regimen Body Cream', 'Skin Regimen Microalgae Essence', 'Hydramemory Cream', 'Hydramemory Face Mist'
    ],
    'HydroPeptide': [
        'Exfoliating Cleanser', 'Polypeptide Collagel', 'Power Luxe', 'Nimni Cream', 'Eye Authority', 'Solar Defense'
    ]
}

keyboard = ReplyKeyboardMarkup([
    [KeyboardButton("Заказать товар")],
    [KeyboardButton("Каталог товаров")]
], resize_keyboard=True)

async def start(update: Update, context: CallbackContext) -> None:
    photo_url = "photo_2024-07-02_00-06-36.jpg"
    await update.message.reply_photo(photo=photo_url, caption='''Привет, дорогой покупатель!👋
Я твой помощник SkinHub Bot. Рад видеть тебя здесь. 

Хочу немного рассказать про нас:
Мы магазин косметических товаров. С помощью нас можно приобрести любимые бренды по выгодным ценам! Мы анализируем их на рынке и готовим для вас самые лучшие предложения. Это дело стало для нас уже родным, поэтому присоединяйся к нам. С каждым новым днем SkinHub будет развиваться, становиться лучше. Мы уже готовы работать под заказ, а дальше — БОЛЬШЕ. 🔥

Попробуй сам, уважаемый покупатель, познакомься с нами немного ближе!✅
⬇️ЖМИ⬇️''', reply_markup=keyboard)

async def actions_panel(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text('Выберите действие:', reply_markup=keyboard)

async def handle_message(update: Update, context: CallbackContext) -> None:
    text = update.message.text
    
    if text == "Заказать товар":
        await update.message.reply_text("Для оформления заказа напишите @assistant_skinhub")
    elif text == "Каталог товаров":
        keyboard = [
            [InlineKeyboardButton(brand, callback_data=f'brand_{brand}') for brand in BRANDS[i:i+2]]
            for i in range(0, len(BRANDS), 2)
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text('Каталог Skin.Hub Cosmetics🔤:\nМы предоставляем обширный список брендов и товаров, которые вы, уважаемые клиенты, можете у нас заказать. ✅\nНаш магазин предлагает вам ознакомиться с каталогом! Мы составили его для вашего удобства, для возможности посмотреть наличие товара или возможность его \nоформить под заказ. 🔔\nПриятных покупок!🤞', reply_markup=reply_markup)

async def button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    await query.answer()
    
    if query.data.startswith('brand_'):
        brand = query.data.split('_')[1]
        if brand != 'Другое...':
            products = PRODUCT_CATALOG.get(brand, [])
            product_list = "\n -".join(products)
            await query.edit_message_text(text=f"Каталог товаров для {brand}:\n -{product_list}")
        else:
            await query.edit_message_text(text=f"Если вашего товара нет в списке, свяжитесь с асистентом🙌\n@assistant_skinhub")

def main() -> None:
    application = ApplicationBuilder().token("7025335462:AAHVxTrH4hx7vwo0bmE3YQxzc0zMk1QJwDs").build()

    application.add_handler(CommandHandler('start', start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.add_handler(CallbackQueryHandler(button))
    application.run_polling()

if __name__ == '__main__':
    main()
