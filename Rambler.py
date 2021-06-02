from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

driver = webdriver.Chrome()
wait = WebDriverWait(driver, 10)

driver.get("https://r0.ru/")
driver.maximize_window()

# Ожидание загрузки "тяжелого" элемента страницы - первого рекламного блока
wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div[3]/div[2]/span/a[2]")))

current_window = driver.current_window_handle
old_windows = driver.window_handles

# Скроллинг новостной ленты
def scrolling():
    #  Элемент, до которого скроллим
    rambler_info = driver.find_element_by_xpath("/html/body/footer/span[1]/a")

    # Первый новостной блок
    ad_block1 = driver.find_element_by_xpath("/html/body/div[3]/div[2]/span/a[2]")
    assert ad_block1.is_displayed() is True

    # Скроллинг
    actions = ActionChains(driver)
    actions.move_to_element(rambler_info).perform()

    # Ожидание появления второго новостного блока
    wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div[3]/div[2]/span/a[11]")))

    # Второй новостной блок
    ad_block2 = driver.find_element_by_xpath("/html/body/div[3]/div[2]/span/a[11]")
    assert ad_block2.is_displayed() is True

    actions = ActionChains(driver)
    actions.move_to_element(rambler_info).perform()

    # Ожидание появления третьего новостного блока
    wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div[3]/div[2]/span/a[20]")))

    # Третий новостной блок
    ad_block3 = driver.find_element_by_xpath("/html/body/div[3]/div[2]/span/a[20]")
    assert ad_block3.is_displayed() is True

    actions = ActionChains(driver)
    actions.move_to_element(rambler_info).perform()

    # Нажимаем кнопку "Показать еще"
    more_button = driver.find_element_by_xpath("/html/body/div[3]/div[2]/div/button")
    assert more_button.is_displayed() is True
    assert more_button.text == "ПОКАЗАТЬ ЕЩЁ"
    # print(more_button.text)
    more_button.click()

    # Ожидание появления четвертого новостного блока
    wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div[3]/div[2]/span/a[29]")))

    # Четвертый новостной блок
    ad_block4 = driver.find_element_by_xpath("/html/body/div[3]/div[2]/span/a[29]")
    assert ad_block4.is_displayed() is True

    # Скроллинг наверх
    scroll_up = driver.find_element_by_xpath("/html/body/div[4]/div")
    assert scroll_up.is_displayed() is True
    scroll_up.click()

scrolling()

# Логотип и строка поиска
def check_search_fields_and_logo():
    # Наличие и кликабельность логотипа
    logo = driver.find_element_by_link_text("Рамблер")
    assert logo.is_displayed() is True
    assert logo.text == "Рамблер"
    # print(logo.text)
    logo_link = driver.find_element_by_xpath("/html/body/div[2]/div[3]/span/a")
    logo_link.click()
    current_url = driver.current_url
    assert current_url == "https://www.rambler.ru/?utm_source=search_r0&utm_content=head&utm_medium=input_line&utm_campaign=self_promo"
    driver.back()

    # Проверка элементов строки поиска и ввод поискового запроса
    search_button = driver.find_element_by_xpath("/html/body/div[2]/div[3]/div[1]/div/form/button")
    # print(search_button.text)
    assert search_button.is_displayed() is True
    assert search_button.text == "НАЙТИ"

    search_form = driver.find_element_by_xpath("/html/body/div[2]/div[3]/div[1]/div/form/input[1]")
    assert search_form.is_displayed() is True
    search_form.send_keys("Wake up Neo")
    search_form_value = search_form.get_attribute("value")
    assert search_form_value == "Wake up Neo"
    # print(search_form_value)
    search_form.submit()
    current_url = driver.current_url
    assert current_url == "https://nova.rambler.ru/search?query=Wake+up+Neo&utm_source=search_r0&utm_campaign=self_promo&utm_medium=form&utm_content=search"
    driver.back()

check_search_fields_and_logo()

# Наличие и кликабельность ссылок под поисковой строкой
def check_search_fields_links():
    # "Поиск"
    poisk_link = driver.find_element_by_xpath("/html/body/div[2]/div[3]/div[2]/nav/a[1]")
    assert poisk_link.is_displayed() is True
    assert poisk_link.text == "Поиск"
    # print(poisk_link.text)
    poisk_link.click()
    current_url = driver.current_url
    assert current_url == "https://r0.ru/"

    # "Картинки"
    img_link = driver.find_element_by_xpath("/html/body/div[2]/div[3]/div[2]/nav/a[2]")
    assert img_link.is_displayed() is True
    assert img_link.text == "Картинки"
    # print(img_link.text)
    img_link.click()

    wait.until(EC.new_window_is_opened(old_windows))
    new_window = [i for i in driver.window_handles if i not in old_windows]
    driver.switch_to.window(new_window[0])

    current_url = driver.current_url
    assert current_url == "https://images.rambler.ru/?utm_source=search_r0&utm_content=search_img&utm_medium=menu&utm_campaign=self_promo&utm_term=main"
    driver.close()
    driver.switch_to.window(current_window)

    # "Организации"
    org_link = driver.find_element_by_xpath("/html/body/div[2]/div[3]/div[2]/nav/a[3]")
    assert org_link.is_displayed() is True
    assert org_link.text == "Организации"
    # print(org_link.text)
    org_link.click()

    wait.until(EC.new_window_is_opened(old_windows))
    new_window = [i for i in driver.window_handles if i not in old_windows]
    driver.switch_to.window(new_window[0])

    current_url = driver.current_url
    assert current_url == "https://org.rambler.ru/?utm_source=search_r0&utm_content=search_org&utm_medium=menu&utm_campaign=self_promo&utm_term=main"
    driver.close()
    driver.switch_to.window(current_window)

    # "Работа"
    rab_link = driver.find_element_by_xpath("/html/body/div[2]/div[3]/div[2]/nav/a[4]")
    assert rab_link.is_displayed() is True
    assert rab_link.text == "Работа"
    # print(rab_link.text)
    rab_link.click()

    wait.until(EC.new_window_is_opened(old_windows))
    new_window = [i for i in driver.window_handles if i not in old_windows]
    driver.switch_to.window(new_window[0])

    current_url = driver.current_url
    assert current_url == "https://rabota.rambler.ru/?utm_source=search_r0&utm_content=search_rabota&utm_medium=menu&utm_campaign=self_promo&utm_term=main"
    driver.close()
    driver.switch_to.window(current_window)

    # "Новости"
    novosti_link = driver.find_element_by_xpath("/html/body/div[2]/div[3]/div[2]/nav/a[5]")
    assert novosti_link.is_displayed() is True
    assert novosti_link.text == "Новости"
    # print(novosti_link.text)
    novosti_link.click()

    wait.until(EC.new_window_is_opened(old_windows))
    new_window = [i for i in driver.window_handles if i not in old_windows]
    driver.switch_to.window(new_window[0])

    current_url = driver.current_url
    assert current_url == "https://news.rambler.ru/?utm_source=search_r0&utm_content=news_media&utm_medium=menu&utm_campaign=self_promo&utm_term=main"
    driver.close()
    driver.switch_to.window(current_window)

check_search_fields_links()

# Наличие и кликабельность виджетов и прочих элементов страницы
# (тесты виджетов погоды и пробок могут завалиться из-за того,
# что эти виджеты иногда не появляются на странице!)
def widgets():
    # Кнопка "Сделать стартовой"
    start_button = driver.find_element_by_xpath("/html/body/div[2]/div[1]/div[2]/a")
    assert start_button.is_displayed() is True
    assert start_button.text == "Сделать стартовой"
    # print(start_button.text)
    start_button.click()

    wait.until(EC.new_window_is_opened(old_windows))
    new_window = [i for i in driver.window_handles if i not in old_windows]
    driver.switch_to.window(new_window[0])

    current_url = driver.current_url
    assert current_url == "https://chrome.google.com/webstore/detail/%D1%80%D0%B0%D0%BC%D0%B1%D0%BB%D0%B5%D1%80%D0%BC%D0%B5%D0%B4%D0%B8%D0%B0/eflnfgjcfmhdpcaadiimlmclcmjpeaki"
    driver.close()
    driver.switch_to.window(current_window)

    # Виджет курса доллара
    dollar_widget = driver.find_element_by_xpath("/html/body/div[2]/div[2]/div[2]/a[1]/span")
    assert dollar_widget.is_displayed() is True
    dollar_widget.click()

    wait.until(EC.new_window_is_opened(old_windows))
    new_window = [i for i in driver.window_handles if i not in old_windows]
    driver.switch_to.window(new_window[0])

    current_url = driver.current_url
    assert current_url == "https://finance.rambler.ru/currencies/USD/?utm_source=search_r0&utm_content=finance_media&utm_medium=widget&utm_campaign=self_promo&utm_term=usd"
    driver.close()
    driver.switch_to.window(current_window)

    # Виджет курса евро
    euro_widget = driver.find_element_by_xpath("/html/body/div[2]/div[2]/div[2]/a[2]/span")
    assert euro_widget.is_displayed() is True
    euro_widget.click()

    wait.until(EC.new_window_is_opened(old_windows))
    new_window = [i for i in driver.window_handles if i not in old_windows]
    driver.switch_to.window(new_window[0])

    current_url = driver.current_url
    assert current_url == "https://finance.rambler.ru/currencies/EUR/?utm_source=search_r0&utm_content=finance_media&utm_medium=widget&utm_campaign=self_promo&utm_term=eur"
    driver.close()
    driver.switch_to.window(current_window)

    # Кнопка "Войти в почту"
    mail_button = driver.find_element_by_xpath("/html/body/div[2]/div[2]/div[3]/a/span")
    assert mail_button.is_displayed() is True
    assert mail_button.text == "Войти в почту"
    # print(mail_button.text)
    mail_button.click()

    wait.until(EC.new_window_is_opened(old_windows))
    new_window = [i for i in driver.window_handles if i not in old_windows]
    driver.switch_to.window(new_window[0])

    current_url = driver.current_url
    assert current_url == "https://mail.rambler.ru/?utm_source=search_r0&utm_content=mail&utm_medium=widget&utm_campaign=self_promo&utm_term=main"
    driver.close()
    driver.switch_to.window(current_window)

    # Часы и дата
    clock = driver.find_element_by_xpath("/html/body/div[2]/div[1]/div[3]/span[1]")
    assert clock.is_displayed() is True
    date = driver.find_element_by_xpath("/html/body/div[2]/div[1]/div[3]/span[2]")
    assert date.is_displayed() is True

    # Геопозиция
    geo = driver.find_element_by_xpath("/html/body/div[2]/div[1]/div[4]/span/span")
    assert geo.is_displayed() is True
    geo.click()
    wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/div[1]/div[5]/div[2]")))
    geo_change_window = driver.find_element_by_xpath("/html/body/div[2]/div[1]/div[5]/div[2]")
    assert geo_change_window.is_displayed() is True
    geo_change_window_close = driver.find_element_by_xpath("/html/body/div[2]/div[1]/div[5]/div[2]/span")
    geo_change_window_close.click()

    # Виджет погоды (Появляется не всегда!!!)
    weather_widget = driver.find_element_by_xpath("/html/body/div[2]/div[2]/a/span/span[1]")
    assert weather_widget.is_displayed() is True
    weather_widget.click()

    wait.until(EC.new_window_is_opened(old_windows))
    new_window = [i for i in driver.window_handles if i not in old_windows]
    driver.switch_to.window(new_window[0])

    current_url = driver.current_url
    assert current_url == "https://weather.rambler.ru/?utm_source=search_r0&utm_content=weather&utm_medium=widget&utm_campaign=self_promo&utm_term=main"
    driver.close()
    driver.switch_to.window(current_window)

    # Виджет пробок (Появляется не всегда!!!)
    probki_widget = driver.find_element_by_xpath("/html/body/div[2]/div[2]/div[1]/a/span[1]")
    assert probki_widget.is_displayed() is True
    assert probki_widget.text == "Пробки"
    # print(probki_widget.text)
    probki_widget.click()

    wait.until(EC.new_window_is_opened(old_windows))
    new_window = [i for i in driver.window_handles if i not in old_windows]
    driver.switch_to.window(new_window[0])

    current_url = driver.current_url
    current_url = current_url[:23]
    # print(current_url)
    assert current_url == "https://yandex.ru/maps/"
    driver.close()
    driver.switch_to.window(current_window)

widgets()

# Наличие и кликабельность ссылок в футере
def footer():
    # Ссылка "Рамблер"
    rambler_info = driver.find_element_by_xpath("/html/body/footer/span[1]/a")
    assert rambler_info.is_displayed() is True
    assert rambler_info.text == "Рамблер"
    rambler_info.click()

    wait.until(EC.new_window_is_opened(old_windows))
    new_window = [i for i in driver.window_handles if i not in old_windows]
    driver.switch_to.window(new_window[0])

    current_url = driver.current_url
    assert current_url == "https://ramblergroup.com/?utm_source=search_r0&utm_content=rambler_all&utm_medium=footer&utm_campaign=self_promo&utm_term=main"
    driver.close()
    driver.switch_to.window(current_window)

    # Ссылка "Мобильная версия/Полная версия"
    mob_ver = driver.find_element_by_xpath("/html/body/footer/span[2]/a")
    assert mob_ver.is_displayed() is True
    assert mob_ver.text == "Мобильная версия"
    mob_ver.click()

    wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/footer/span[2]/a")))

    current_url = driver.current_url
    assert current_url == "https://r0.ru/"

    web_ver = driver.find_element_by_xpath("/html/body/div[1]/footer/span[2]/a")
    assert web_ver.is_displayed() is True
    assert web_ver.text == "Полная версия"
    web_ver.click()

    wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/footer/span[2]/a")))

    mob_ver = driver.find_element_by_xpath("/html/body/footer/span[2]/a")
    assert mob_ver.is_displayed() is True
    assert mob_ver.text == "Мобильная версия"

    # Ссылка "Помощь"
    help = driver.find_element_by_xpath("/html/body/footer/a[1]")
    assert help.is_displayed() is True
    assert help.text == "Помощь"
    help.click()

    wait.until(EC.new_window_is_opened(old_windows))
    new_window = [i for i in driver.window_handles if i not in old_windows]
    driver.switch_to.window(new_window[0])

    current_url = driver.current_url
    assert current_url == "https://help.rambler.ru/rsearch/?utm_source=search_r0&utm_content=help&utm_medium=footer&utm_campaign=self_promo&utm_term=main"
    driver.close()
    driver.switch_to.window(current_window)

    # Ссылка "Обратная связь"
    feedback = driver.find_element_by_xpath("/html/body/footer/a[2]")
    assert feedback.is_displayed() is True
    assert feedback.text == "Обратная связь"
    feedback.click()

    wait.until(EC.new_window_is_opened(old_windows))
    new_window = [i for i in driver.window_handles if i not in old_windows]
    driver.switch_to.window(new_window[0])

    current_url = driver.current_url
    assert current_url == "https://help.rambler.ru/feedback/rsearch/?utm_source=search_r0&utm_content=help&utm_medium=footer&utm_campaign=self_promo&utm_term=main"
    driver.close()
    driver.switch_to.window(current_window)

    # Ссылка "Пользовательское соглашение"
    legal = driver.find_element_by_xpath("/html/body/footer/a[3]")
    assert legal.is_displayed() is True
    assert legal.text == "Пользовательское соглашение"
    legal.click()

    wait.until(EC.new_window_is_opened(old_windows))
    new_window = [i for i in driver.window_handles if i not in old_windows]
    driver.switch_to.window(new_window[0])

    current_url = driver.current_url
    assert current_url == "https://help.rambler.ru/legal/rsearch/?utm_source=search_r0&utm_content=help&utm_medium=footer&utm_campaign=self_promo&utm_term=main"
    driver.close()
    driver.switch_to.window(current_window)

    # Ссылка "Удаление информации"
    delete = driver.find_element_by_xpath("/html/body/footer/a[4]")
    assert delete.is_displayed() is True
    assert delete.text == "Удаление информации"
    delete.click()

    wait.until(EC.new_window_is_opened(old_windows))
    new_window = [i for i in driver.window_handles if i not in old_windows]
    driver.switch_to.window(new_window[0])

    current_url = driver.current_url
    assert current_url == "https://help.rambler.ru/rsearch/rsearch-udalenie-informacii-iz-poiska/1367/?utm_source=search_r0&utm_content=help&utm_medium=footer&utm_campaign=self_promo&utm_term=main"
    driver.close()
    driver.switch_to.window(current_window)

    # Иконка возраст "18+"
    age = driver.find_element_by_xpath("/html/body/footer/div")
    assert age.is_displayed() is True

footer()

driver.close()
driver.quit()

#==================================================================================================================================

# ДАННАЯ ПРОВЕРКА ШАПКИ СТРАНИЦЫ САЙТА ДО КОНЦА НЕ РЕАЛИЗОВАНА!!!

# Наличие и кликабельность ссылок и кнопок в шапке
def buttons():
    # Кнопка "Еще"
    if not len(driver.find_element_by_xpath("/html/body/div[2]/div[1]/div[1]/div/div/div/div/div[1]/div[2]").text):
        more_button = driver.find_element_by_xpath("/html/body/div[2]/div[1]/div[1]/div/div/div[1]/div[1]/div/div[2]/div[9]/button")
    else:
        more_button = driver.find_element_by_xpath("/html/body/div[2]/div[1]/div[1]/div/div/div[1]/div/div[1]/div[2]")
    assert more_button.is_displayed() is True
    print(more_button.text)
    more_button.click()
    wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/div[1]/div[1]/div/div/div[2]/div/div")))
    more_window = driver.find_element_by_xpath("/html/body/div[2]/div[1]/div[1]/div/div/div[2]/div/div")
    assert more_window.is_displayed() is True


    # Кнопка "Вход"
    if not len(driver.find_element_by_xpath("/html/body/div[2]/div[1]/div[1]/div/div/div/div/div[2]/div[2]/div").text):
        sign_in = driver.find_element_by_xpath("/html/body/div[2]/div[1]/div[1]/div/div/div/div[2]/div[3]/button/span")
    else:
        sign_in = driver.find_element_by_xpath("/html/body/div[2]/div[1]/div[1]/div/div/div/div/div[2]/div[2]/div")
    assert sign_in.text == "Вход"
    print(sign_in.text)
    sign_in.click()
    wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div/div[1]/div")))
    sign_in_window = driver.find_element_by_xpath("/html/body/div[1]/div/div[1]/div")
    assert sign_in_window.is_displayed() is True
    sign_in_window_close = driver.find_element_by_xpath("/html/body/div[1]/div/div[1]/header/div/button/svg/path")
    sign_in_window_close.click()

def links():
    # Ссылка "Почта"
    current_window = driver.current_window_handle
    old_windows = driver.window_handles

    mail_link = driver.find_element_by_link_text("Почта")
    print(mail_link.text)
    assert mail_link.text == "Почта"
    mail_link.click()

    wait.until(EC.new_window_is_opened(old_windows))
    new_window = [i for i in driver.window_handles if i not in old_windows]
    driver.switch_to.window(new_window[0])

    current_url = driver.current_url
    assert current_url == "https://mail.rambler.ru/?utm_source=search_r0&utm_campaign=self_promo&utm_medium=topline&utm_content=mail"

    driver.close()
    driver.switch_to.window(current_window)

    # Ссылка "Новости"
    current_window = driver.current_window_handle
    old_windows = driver.window_handles

    news_link = driver.find_element_by_link_text("Новости")
    print(news_link.text)
    assert news_link.text == "Новости"
    news_link.click()

    wait.until(EC.new_window_is_opened(old_windows))
    new_window = [i for i in driver.window_handles if i not in old_windows]
    driver.switch_to.window(new_window[0])

    current_url = driver.current_url
    assert current_url == "https://news.rambler.ru/?utm_source=search_r0&utm_campaign=self_promo&utm_medium=topline&utm_content=news_media"

    driver.close()
    driver.switch_to.window(current_window)

    # Ссылка "Кино"
    current_window = driver.current_window_handle
    old_windows = driver.window_handles
    kino_link = driver.find_element_by_link_text("Кино")
    print(kino_link.text)
    assert kino_link.text == "Кино"
    kino_link.click()

    wait.until(EC.new_window_is_opened(old_windows))
    new_window = [i for i in driver.window_handles if i not in old_windows]
    driver.switch_to.window(new_window[0])

    current_url = driver.current_url
    assert current_url == "https://kino.rambler.ru/?utm_source=search_r0&utm_campaign=self_promo&utm_medium=topline&utm_content=kino_media"

    driver.close()
    driver.switch_to.window(current_window)

    # Ссылка "Спорт"
    current_window = driver.current_window_handle
    old_windows = driver.window_handles
    sport_link = driver.find_element_by_link_text("Спорт")
    print(sport_link.text)
    assert sport_link.text == "Спорт"
    sport_link.click()

    wait.until(EC.new_window_is_opened(old_windows))
    new_window = [i for i in driver.window_handles if i not in old_windows]
    driver.switch_to.window(new_window[0])

    current_url = driver.current_url
    assert current_url == "https://sport.rambler.ru/?utm_source=search_r0&utm_campaign=self_promo&utm_medium=topline&utm_content=sport_media"

    driver.close()
    driver.switch_to.window(current_window)

    # Ссылка "Авто"
    current_window = driver.current_window_handle
    old_windows = driver.window_handles
    auto_link = driver.find_element_by_link_text("Авто")
    print(auto_link.text)
    assert auto_link.text == "Авто"
    auto_link.click()

    wait.until(EC.new_window_is_opened(old_windows))
    new_window = [i for i in driver.window_handles if i not in old_windows]
    driver.switch_to.window(new_window[0])

    current_url = driver.current_url
    assert current_url == "https://auto.rambler.ru/?utm_source=search_r0&utm_campaign=self_promo&utm_medium=topline&utm_content=auto_media"

    driver.close()
    driver.switch_to.window(current_window)

    # Ссылка "Гороскопы"
    current_window = driver.current_window_handle
    old_windows = driver.window_handles
    goro_link = driver.find_element_by_link_text("Гороскопы")
    print(goro_link.text)
    assert goro_link.text == "Гороскопы"
    goro_link.click()

    wait.until(EC.new_window_is_opened(old_windows))
    new_window = [i for i in driver.window_handles if i not in old_windows]
    driver.switch_to.window(new_window[0])

    current_url = driver.current_url
    assert current_url == "https://horoscopes.rambler.ru/?utm_source=search_r0&utm_campaign=self_promo&utm_medium=topline&utm_content=horoscopes"

    driver.close()
    driver.switch_to.window(current_window)

    # Ссылка "Финансы"
    current_window = driver.current_window_handle
    old_windows = driver.window_handles
    finance_link = driver.find_element_by_link_text("Финансы")
    print(finance_link.text)
    assert finance_link.text == "Финансы"
    finance_link.click()

    wait.until(EC.new_window_is_opened(old_windows))
    new_window = [i for i in driver.window_handles if i not in old_windows]
    driver.switch_to.window(new_window[0])

    current_url = driver.current_url
    assert current_url == "https://finance.rambler.ru/?utm_source=search_r0&utm_campaign=self_promo&utm_medium=topline&utm_content=finance_media"

    driver.close()
    driver.switch_to.window(current_window)

    # Ссылка "Работа"
    current_window = driver.current_window_handle
    old_windows = driver.window_handles
    rabota_link = driver.find_element_by_link_text("Работа")
    print(rabota_link.text)
    assert rabota_link.text == "Работа"
    rabota_link.click()

    wait.until(EC.new_window_is_opened(old_windows))
    new_window = [i for i in driver.window_handles if i not in old_windows]
    driver.switch_to.window(new_window[0])

    current_url = driver.current_url
    assert current_url == "https://rabota.rambler.ru/?utm_source=search_r0&utm_content=search_rabota&utm_medium=menu&utm_campaign=self_promo&utm_term=main"

    driver.close()
    driver.switch_to.window(current_window)

# buttons()
# links()

# driver.close()
# driver.quit()