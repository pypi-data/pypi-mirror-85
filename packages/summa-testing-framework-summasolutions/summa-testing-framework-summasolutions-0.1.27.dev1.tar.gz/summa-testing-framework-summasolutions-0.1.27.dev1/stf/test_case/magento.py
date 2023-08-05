from .base import BaseTestCase

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys


class MagentoTestCase(BaseTestCase):
    def visit_product_page(self, sku: str):
        driver = self.driver
        wait = WebDriverWait(driver, self.config['time_to_sleep'])

        search_input = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@id='search']")))
        search_input.send_keys(sku)
        search_input.submit()
        pdp = wait.until(EC.visibility_of_element_located((By.XPATH, "//div[@class='product-info-main']")))

        return pdp

    def checkout_loader(self):
        driver = self.driver
        # function wait for checkout loader
        wait = WebDriverWait(driver, self.config['time_to_sleep'])
        loading = wait.until(EC.invisibility_of_element_located((By.XPATH, "//div[@class='loading-mask']")))

        return loading

    def login_page(self):
        driver = self.driver
        # function to go to login page
        wait = WebDriverWait(driver, self.config['time_to_sleep'])
        loading = wait.until(EC.invisibility_of_element_located((By.XPATH, "//div[@class='loading-mask']")))
        loginBtn = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@id='header-my-account']")))
        loginBtn.click()

    def login(self, username: str, password: str):
        driver = self.driver
        # function to fill login form
        wait = WebDriverWait(driver, self.config['time_to_sleep'])
        login_form = wait.until(EC.visibility_of_element_located((By.XPATH, "//form[@id='login-form']")))
        email_field = driver.find_element_by_xpath("//input[@id='customer-email']")
        password_field = driver.find_element_by_xpath("//input[@id='pass']")
        email_field.send_keys(username)
        password_field.send_keys(password)
        password_field.submit()

    def register_user(self, email: str, password: str):
        driver = self.driver
        # function to fill register form
        wait = WebDriverWait(driver, self.config['time_to_sleep'])
        # First name
        firstname_field = wait.until(EC.visibility_of_element_located((By.XPATH, "//input[@id='firstname']")))
        firstname_field.send_keys('automated')
        # Last name
        lastname_field = wait.until(EC.visibility_of_element_located((By.XPATH, "//input[@id='lastname']")))
        lastname_field.send_keys('test')
        # Email address
        email_address_field = wait.until(EC.visibility_of_element_located((By.XPATH, "//input[@id='email_address']")))
        email_address_field.send_keys(email)
        # Password
        password_field = wait.until(EC.visibility_of_element_located((By.XPATH, "//input[@id='password']")))
        password_field.send_keys(password)
        # Password confirmation
        password_confirmation_field = wait.until(
            EC.visibility_of_element_located((By.XPATH, "//input[@id='password-confirmation']")))
        password_confirmation_field.send_keys(password)
        # Submit
        send_button = wait.until(
            EC.visibility_of_element_located((By.XPATH, "//div[contains(@class, 'actions-toolbar')]/.//button")))
        send_button.click()

    def create_account(self, email: str, password: str):
        driver = self.driver
        # function to create an account during checkout process
        wait = WebDriverWait(driver, self.config['time_to_sleep'])
        self.login_page()
        wait.until(EC.visibility_of_element_located((By.XPATH, "//form[@id='login-form']")))
        # Create account button
        new_customer_button = wait.until(
            EC.visibility_of_element_located((By.XPATH, "//a[contains(@href, 'account/create')]")))
        new_customer_button.click()
        # Fill form
        self.register_user(email, password)

    def new_address_book(self):
        driver = self.driver

        # function to fill new shipping address in address book in my account
        wait = WebDriverWait(driver, self.config['time_to_sleep'])
        address_book_button = wait.until(EC.visibility_of_element_located(
            (By.XPATH, "//div[contains(@class, 'box-shipping-address')]/.//a[contains(@href, 'customer/address')]")))
        address_book_button.click()
        # First Name
        firstname_field = wait.until(EC.visibility_of_element_located((By.XPATH, "//input[@id='firstname']")))
        firstname_field.send_keys('automated')
        # Last Name
        lastname_field = wait.until(EC.visibility_of_element_located((By.XPATH, "//input[@id='lastname']")))
        lastname_field.send_keys('test')
        # Street
        street_field = wait.until(EC.visibility_of_element_located((By.XPATH, "//input[@id='street_1']")))
        street_field.send_keys('Testing')
        # Street Number
        # streetNumber = driver.find_element_by_xpath("//input[@name='custom_attributes[number]']")
        # streetNumber.send_keys('123')
        # Document
        # documentNumber = driver.find_element_by_xpath("//input[@name='custom_attributes[numero_documento]']")
        # documentNumber.send_keys('12345678')
        # Region
        region_field = wait.until(
            EC.visibility_of_element_located((By.XPATH, "//select[@id='region_id']/option[@value='654']")))
        region_field.click()
        # City
        city_field = wait.until(EC.visibility_of_element_located((By.XPATH, "//input[@id='city']")))
        city_field.send_keys('CABA')
        # Postcode
        postal_code_field = wait.until(EC.visibility_of_element_located((By.XPATH, "//input[@id='zip']")))
        postal_code_field.send_keys('1414')
        # Telephone
        phone_field = wait.until(EC.visibility_of_element_located((By.XPATH, "//input[@id='telephone']")))
        phone_field.send_keys('1234567')
        # save address
        save_address_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[@data-action='save-address']")))
        save_address_button.click()

    def add_simple_product_to_cart(self):
        driver = self.driver
        wait = WebDriverWait(driver, self.config['time_to_sleep'])

        add_to_cart_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[@id='product-addtocart-button']")))
        add_to_cart_button.click()

    def add_configurable_product_to_cart(self, config_option):
        driver = self.driver
        wait = WebDriverWait(driver, self.config['time_to_sleep'])

        swatch = driver.find_element_by_xpath(
            "//div[@id='product-options-wrapper']/.//option[@value='" + str(config_option) + "']")
        swatch.click()

        add_to_cart_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[@id='product-addtocart-button']")))
        add_to_cart_button.click()

    def validate_checkout(self):
        driver = self.driver
        # function to validate checkout process
        wait = WebDriverWait(driver, self.config['time_to_sleep'])
        checkout = wait.until(EC.visibility_of_element_located((By.XPATH, "//div[@id='checkout']")))

    def go_to_checkout_from_popup(self):
        driver = self.driver

        wait = WebDriverWait(driver, self.config['time_to_sleep'])
        wait.until(
            EC.visibility_of_element_located((By.XPATH, "//aside[contains(@class, 'added-to-cart-popup')]")))
        start_checkout_button = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//aside[contains(@class, 'added-to-cart-popup')]/.//button[@class='action-primary']")))
        start_checkout_button.click()

    def go_to_checkout_from_minicart(self):
        driver = self.driver
        # function to go to checkout from minicart
        wait = WebDriverWait(driver, self.config['time_to_sleep'])
        minicart_button = wait.until(EC.visibility_of_element_located((By.XPATH, "//div[@data-block='minicart']")))
        minicart_button.click()

    def checkout_form_fill_email(self, user: str):
        # function to fill mail input in checkout process
        wait = WebDriverWait(driver, timeToSleep)
        email_field = wait.until(EC.visibility_of_element_located((By.XPATH, "//input[@id='customer-email']")))
        email_field.send_keys(user)
        self.checkout_loader()
        next_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@class='confirm-email']/button")))
        next_button.click()

    def validate_address_book(self):
        driver = self.driver
        # function to validate address book from registered user
        wait = WebDriverWait(driver, self.config['time_to_sleep'])
        address_book = wait.until(
            EC.visibility_of_element_located((By.XPATH, "//div[@class='shipping-address-items']")))
        return address_book

    def new_shipping_address(self):
        driver = self.driver
        # function to fill new shipping address
        wait = WebDriverWait(driver, self.config['time_to_sleep'])
        self.checkout_loader()
        # First Name
        firstname_field = wait.until(EC.visibility_of_element_located((By.XPATH, "//input[@name='firstname']")))
        firstname_field.send_keys('automated')
        # Last Name
        lastname_field = driver.find_element_by_xpath("//input[@name='lastname']")
        lastname_field.send_keys('test')
        # Street
        street_field = driver.find_element_by_xpath("//input[@name='street[0]']")
        street_field.send_keys('Testing')
        # Street Number
        # streetNumber = driver.find_element_by_xpath("//input[@name='custom_attributes[number]']")
        # streetNumber.send_keys('123')
        # Document
        # documentNumber = driver.find_element_by_xpath("//input[@name='custom_attributes[numero_documento]']")
        # documentNumber.send_keys('12345678')
        # Region
        region_field = wait.until(
            EC.visibility_of_element_located((By.XPATH, "//select[@name='region_id']/option[@value='654']")))
        region_field.click()
        # City
        city_field = wait.until(EC.visibility_of_element_located((By.XPATH, "//input[@name='city']")))
        city_field.send_keys('CABA')
        # Postcode
        postalcode_field = driver.find_element_by_xpath("//input[@name='postcode']")
        postalcode_field.send_keys('1414')
        # Telephone
        phone_field = driver.find_element_by_xpath("//input[@name='telephone']")
        phone_field.send_keys('123456789')

    def checkout_select_shipping_method_flatrate(self):
        driver = self.driver
        # function to choose flat rate method
        wait = WebDriverWait(driver, self.config['time_to_sleep'])
        self.checkout_loader()
        shipping_method_checkbox = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@id='flatrate']")))
        shipping_method_checkbox.click()

    def checkout_select_shipping_method_storepickup(self):
        driver = self.driver
        # function to choose store pickup method
        wait = WebDriverWait(driver, self.config['time_to_sleep'])
        self.checkout_loader()
        shipping_method_checkbox = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@id='storepickup']")))
        shipping_method_checkbox.click()
        # fill pickup data
        # First Name
        firstname_field = wait.until(EC.visibility_of_element_located((By.XPATH, "//input[@name='firstname']")))
        firstname_field.send_keys('automated')
        # Last Name
        lastname_field = wait.until(EC.visibility_of_element_located((By.XPATH, "//input[@name='lastname']")))
        lastname_field.send_keys('test')
        # Telephone
        telephone_field = wait.until(EC.visibility_of_element_located((By.XPATH, "//input[@name='telephone']")))
        telephone_field.send_keys('12354789')
        # choose a store
        stores_list_field = wait.until(EC.visibility_of_element_located((By.XPATH, "//select[@id='select-store']")))
        stores_list_item = wait.until(EC.element_to_be_clickable((By.XPATH, "//select[@id='select-store']/option[2]")))
        stores_list_item.click()

    def checkout_go_to_payment_step(self):
        driver = self.driver
        # function go to payment
        wait = WebDriverWait(driver, self.config['time_to_sleep'])
        self.checkout_loader()
        next_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//div[@id='shipping-method-buttons-container']/.//button")))
        next_button.click()

    def checkout_new_billing_address(self):
        driver = self.driver
        # function to fill new billing address
        wait = WebDriverWait(driver, self.config['time_to_sleep'])
        self.checkout_loader()
        wait.until(
            EC.visibility_of_element_located((By.XPATH, "//div[@class='checkout-billing-address']")))
        # First Name
        firstname_field = wait.until(EC.visibility_of_element_located(
            (By.XPATH, "//div[@class='billing-address-form']/.//input[@name='firstname']")))
        firstname_field.send_keys('automated')
        # Last Name
        lastname_field = driver.find_element_by_xpath("//div[@class='billing-address-form']/.//input[@name='lastname']")
        lastname_field.send_keys('test')
        # Street
        street_field = driver.find_element_by_xpath("//div[@class='billing-address-form']/.//input[@name='street[0]']")
        street_field.send_keys('Testing')
        # Street Number
        # streetNumber = driver.find_element_by_xpath("//input[@name='custom_attributes[number]']")
        # streetNumber.send_keys('123')
        # Document
        # documentNumber = driver.find_element_by_xpath("//input[@name='custom_attributes[numero_documento]']")
        # documentNumber.send_keys('12345678')
        # Region
        region_field = wait.until(EC.visibility_of_element_located(
            (By.XPATH, "//div[@class='billing-address-form']/.//select[@name='region_id']/option[@value='654']")))
        region_field.click()
        # City
        city_field = wait.until(
            EC.visibility_of_element_located((By.XPATH, "//div[@class='billing-address-form']/.//input[@name='city']")))
        city_field.send_keys('CABA')
        # Postcode
        postal_code_field = driver.find_element_by_xpath(
            "//div[@class='billing-address-form']/.//input[@name='postcode']")
        postal_code_field.send_keys('1414')
        # Telephone
        phone_field = driver.find_element_by_xpath("//div[@class='billing-address-form']/.//input[@name='telephone']")
        phone_field.send_keys('123456789')
        # update billing address
        update_address_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'action-update')]")))
        update_address_button.click()

    def checkout_place_order_payment_method_mercadopago(self):
        driver = self.driver
        # funcion to place order with MercadoPago
        wait = WebDriverWait(driver, self.config['time_to_sleep'])
        self.checkout_loader()
        save_payment_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[@id='mp-custom-save-payment-ag']")))
        self.checkout_loader()
        save_payment_button.click()

    def checkout_place_order_payment_method_decidir(self):
        driver = self.driver
        # function to place order with Decidir
        wait = WebDriverWait(driver, self.config['time_to_sleep'])
        self.checkout_loader()
        save_payment_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@id='sps-pagar-btn']")))
        self.checkout_loader()
        save_payment_button.click()

    def checkout_fill_payment_method_mercadopago(self, card):
        driver = self.driver
        # funcion to pay with MercadoPago in Agreggator mode
        wait = WebDriverWait(driver, self.config['time_to_sleep'])
        self.checkout_loader()
        # choose mercadopago aggregator
        payment_method_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//input[@id='mercadopago_custom_aggregator']")))
        payment_method_button.click()
        self.checkout_loader()
        # Credit Card Number
        number_field = wait.until(EC.visibility_of_element_located((By.XPATH, "//input[@id='cardNumberAg']")))
        number_field.send_keys(card['number'])
        number_field.send_keys(Keys.TAB)
        # Expiration Date
        month_field = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//select[@id='cardExpirationMonthAg']/option[@value='" + str(card['month']) + "']")))
        month_field.click()
        year_field = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//select[@id='cardExpirationYearAg']/option[@value='" + str(card['year']) + "']")))
        year_field.click()
        # Name On Card
        holder_field = wait.until(EC.visibility_of_element_located((By.XPATH, "//input[@id='cardholderNameAg']")))
        holder_field.send_keys(card['owner'])
        # Card Verification Number
        cvv_field = wait.until(EC.visibility_of_element_located((By.XPATH, "//input[@id='securityCodeAg']")))
        cvv_field.send_keys(card['cvv'])
        # Document Type
        document_type_field = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//select[@id='docTypeAg']/option[@value='DNI']")))
        document_type_field.click()
        # Document ID
        document_number_field = wait.until(EC.visibility_of_element_located((By.XPATH, "//input[@id='docNumberAg']")))
        document_number_field.send_keys(card['dni'])
        # Installments
        installments_field = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//select[@id='installmentsAg']/option[@value='" + str(card['plan']) + "']")))
        installments_field.click()

    def checkout_fill_cc_form_decidir(self, card):
        driver = self.driver
        wait = WebDriverWait(driver, self.config['time_to_sleep'])
        self.checkout_loader()
        # Name On Card
        holder_field = wait.until(EC.visibility_of_element_located((By.XPATH, "//input[@id='sps-tarjeta-nombre']")))
        holder_field.send_keys(card['owner'])
        # Credit Card Number
        number_field = wait.until(EC.visibility_of_element_located((By.XPATH, "//input[@id='sps-tarjeta-numero']")))
        number_field.send_keys(card['number'])
        # Expiration Date
        month_field = wait.until(
            EC.visibility_of_element_located((By.XPATH, "//input[@id='sps-tarjeta-vencimiento-month']")))
        month_field.send_keys(card['month'])
        year_field = wait.until(
            EC.visibility_of_element_located((By.XPATH, "//input[@id='sps-tarjeta-vencimiento-year']")))
        year_field.send_keys(card['year'])
        # Card Verification Number
        cvv_field = wait.until(
            EC.visibility_of_element_located((By.XPATH, "//input[@id='sps-tarjeta-codigo-seguridad']")))
        cvv_field.send_keys(card['cvv'])
        # Document Number
        dni_field = wait.until(
            EC.visibility_of_element_located((By.XPATH, "//input[@id='sps-tarjeta-numero-documento']")))
        dni_field.send_keys(card['dni'])

    def checkout_fill_payment_method_decidir(self, card, payment_plan):
        driver = self.driver
        # function to pay with Decidir
        wait = WebDriverWait(driver, self.config['time_to_sleep'])
        self.checkout_loader()
        # elijo el metodo de pago
        payment_method_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@id='decidir_spsdecidir']")))
        payment_method_button.click()
        self.checkout_loader()
        # elijo tarjeta
        card_field = wait.until(EC.visibility_of_element_located((By.XPATH, "//div[@id='tarjeta-container']")))
        card_field_option = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//li[@class='box-tarjeta' and @id='box-tarjeta_" + str(payment_plan['card']) + "']")))
        card_field_option.click()
        # elijo banco
        bank_field_option = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//li[@class='box-banco' and @id='box-banco_" + str(payment_plan['bank']) + "']")))
        bank_field_option.click()
        # elijo plan
        plan_field_option = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "(//div[@class='box-plan-cuota' and @id='box_plan_" + payment_plan['plan'] + "']/.//span)[1]")))
        plan_field_option.click()
        # aplico plan
        apply_plan_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@class='confirmar-plan']/button")))
        apply_plan_button.click()
        self.checkout_fill_cc_form_decidir(driver, card)

    def get_subtotals(self):
        driver = self.driver
        # function to get subtotals from order info
        wait = WebDriverWait(driver, self.config['time_to_sleep'])
        sub_total = wait.until(EC.visibility_of_element_located((By.XPATH,
                                                                 "//div[@class='opc-block-summary']/.//tr[contains(@class,'sub')]/.//span[@class='price']"))).get_attribute(
            'innerHTML')
        ship_total = wait.until(EC.visibility_of_element_located((By.XPATH,
                                                                  "//div[@class='opc-block-summary']/.//tr[contains(@class,'shipping')]/.//span[@class='price']"))).get_attribute(
            'innerHTML')
        grand_total = wait.until(EC.visibility_of_element_located((By.XPATH,
                                                                   "//div[@class='opc-block-summary']/.//tr[contains(@class,'totals')]/.//span[@class='price']"))).get_attribute(
            'innerHTML')
        return [sub_total, ship_total, grand_total]

    def get_shipping_address(self):
        driver = self.driver
        # function to get shipping address from order info
        wait = WebDriverWait(driver, self.config['time_to_sleep'])
        shipping_address = wait.until(
            EC.visibility_of_element_located((By.XPATH, "//div[@class='shipping-information-content']"))).get_attribute(
            'innerHTML')
        return shipping_address

    def get_checkout_success_message(self):
        driver = self.driver
        # function to validate magento success page
        wait = WebDriverWait(driver, self.config['time_to_sleep'])
        success_message = wait.until(EC.visibility_of_element_located((By.XPATH, "//div[@class='checkout-success']")))
        return success_message

    def get_checkout_success_message_mercadopago(self):
        driver = self.driver
        # function to validate mercadopago success page
        wait = WebDriverWait(driver, self.config['time_to_sleep'])
        success_message = wait.until(EC.visibility_of_element_located((By.XPATH, "//div[contains(@class, 'success')]")))
        return success_message

    def get_checkout_failure_message(self):
        driver = self.driver
        # function to validate magento failure page
        wait = WebDriverWait(driver, self.config['time_to_sleep'])
        failure_message = wait.until(
            EC.visibility_of_element_located((By.XPATH, "//div[@class='checkout-failure-wrapper']")))
        return failure_message

    def empty_cart(self, items):
        driver = self.driver
        # function to empty cart
        wait = WebDriverWait(driver, self.config['time_to_sleep'])
        for i in range(items, 0, -1):
            itemXpath = "//table[@id='shopping-cart-table']/tbody[" + str(i) + "]/tr/td[1]/div[1]"
            item = wait.until(EC.element_to_be_clickable((By.XPATH, itemXpath)))
            item.click()
