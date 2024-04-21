import os
from faker import Faker
from requests import get, post

fake = Faker()

def test_web_app():

    # GIVEN
    host_name="HOST_HOSTNAME="+fake.domain_name()
    host_ip="HOST_IP="+fake.ipv4()
    host_mac="HOST_MAC="+fake.mac_address()
    host_cpu="HOST_CPU="+fake.random_element(elements=('Intel', 'AMD'))+" "+fake.random_element(elements=('i3', 'i5', 'i7', 'Ryzen 3', 'Ryzen 5', 'Ryzen 7'))
    host_ram="HOST_RAM="+str(fake.random_int(min=1, max=64, step=1))+"GB"
    host_os="HOST_OS="+fake.random_element(elements=('Windows', 'Ubuntu', 'Debian', 'CentOS', 'Fedora', 'Red Hat'))
    host_kernel="HOST_KERNEL="+fake.random_element(elements=('4.4', '4.9', '4.14', '4.19', '5.4', '5.8', '5.10', '5.11', '5.12', '5.13', '5.14', '5.15'))
    host_docker="HOST_DOCKER="+str(fake.boolean(chance_of_getting_true=50))
    cache_host="CACHE_HOST="+fake.domain_name()
    cache_port="CACHE_PORT="+str(fake.random_int(min=1024, max=65535, step=1))
    database_host="DATABASE_HOST="+fake.domain_name()
    database_port="DATABASE_PORT="+str(fake.random_int(min=1024, max=65535, step=1))
    database_name="DATABASE_NAME="+fake.user_name()
    database_user="DATABASE_USER="+fake.user_name()
    database_table_prefix="DATABASE_TABLE_PREFIX="+fake.user_name()
    website_title="WEBSITE_TITLE="+fake.sentence(nb_words=6, variable_nb_words=True)
    website_description="WEBSITE_DESCRIPTION="+fake.sentence(nb_words=6, variable_nb_words=True)
    website_hostname="WEBSITE_HOSTNAME="+fake.domain_name()
    website_name="WEBSITE_NAME="+fake.company()
    website_admin_first_name="WEBSITE_ADMIN_FIRSTNAME="+fake.first_name()
    website_admin_last_name="WEBSITE_ADMIN_LASTNAME="+fake.last_name()
    website_admin_username="WEBSITE_ADMIN_USERNAME="+fake.user_name()
    website_admin_email="WEBSITE_ADMIN_EMAIL="+fake.email()
    mail_smtp_host="MAIL_SMTP_HOST=smtp."+fake.domain_name()
    mail_smtp_port="MAIL_SMTP_PORT="+str(fake.random_int(min=1024, max=65535, step=1))
    mail_smtp_user="MAIL_SMTP_USER="+fake.user_name()
    mail_smtp_protocol="MAIL_SMTP_PROTOCOL=tls"
    redis_host="WORDPRESS_REDIS_HOST="+fake.domain_name()
    redis_port="WORDPRESS_REDIS_PORT="+str(fake.random_int(min=1024, max=65535, step=1))
    redis_cache_enabled="WORDPRESS_CACHE_ENABLED="+str(fake.boolean(chance_of_getting_true=50))
    redis_cache_duration="WORDPRESS_CACHE_DURATION="+str(fake.random_int(min=1, max=60, step=1))
    redis_cache_type="WORDPRESS_CACHE_TYPE="+fake.random_element(elements=('redis', 'memcached'))
    pma_user="PMA_USER="+fake.user_name()
    woocommerce_enable="WOOCOMMERCE_ENABLED="+str(fake.boolean(chance_of_getting_true=50))
    woocommerce_tax_enabled="WOOCOMMERCE_TAX_ENABLED="+str(fake.boolean(chance_of_getting_true=50))
    woocommerce_tax_country="WOOCOMMERCE_TAX_COUNTRY="+fake.country()
    woocommerce_tax_state="WOOCOMMERCE_TAX_STATE="+fake.state()
    woocommerce_tax_rate="WOOCOMMERCE_TAX_RATE="+str(fake.random_int(min=1, max=30, step=1))
    woocommerce_tax_shipping_enabled="WOOCOMMERCE_TAX_SHIPPING_ENABLED="+str(fake.boolean(chance_of_getting_true=50))
    woocommerce_tax_shipping_class="WOOCOMMERCE_TAX_SHIPPING_TAX_CLASS="+fake.random_element(elements=('standard', 'reduced rate', 'zero rate'))
    woocommerce_tax_shipping_rate="WOOCOMMERCE_TAX_SHIPPING_TAX_RATE="+str(fake.random_int(min=1, max=30, step=1))
    woocommerce_tax_shipping_priority="WOOCOMMERCE_TAX_SHIPPING_TAX_PRIORITY="+str(fake.random_int(min=1, max=5, step=1))
    woocommerce_url="WOOCOMMERCE_URL="+fake.url()
    woocommerce_key="WOOCOMMERCE_KEY="+fake.password(length=32, special_chars=True, digits=True, upper_case=True, lower_case=True)
    woocommerce_secret="WOOCOMMERCE_SECRET="+fake.password(length=32, special_chars=True, digits=True, upper_case=True, lower_case=True)
    woocommerce_currency="WOOCOMMERCE_CURRENCY="+fake.currency_code()
    woocommerce_currency_position="WOOCOMMERCE_CURRENCY_POSITION=right"
    woocommerce_currency_thousands_separator="WOOCOMMERCE_CURRENCY_THOUSANDS_SEPARATOR=."
    woocommerce_currency_decimal_separator="WOOCOMMERCE_CURRENCY_DECIMAL_SEPARATOR=,"
    woocommerce_currency_decimals="WOOCOMMERCE_CURRENCY_DECIMALS=2"
    remote_server_username="REMOTE_SERVER_USERNAME="+fake.user_name()
    remote_server_ip="REMOTE_SERVER_IP="+fake.ipv4()
    remote_server_port="REMOTE_SERVER_PORT="+str(fake.random_int(min=1024, max=65535, step=1))
    remote_server_path="REMOTE_SERVER_PATH="+fake.file_path(depth=2, category=None, extension=None)
    proxy_title="PROXY_TITLE="+fake.sentence(nb_words=6, variable_nb_words=True)
    proxy_hostname="PROXY_HOSTNAME="+fake.domain_name()
    proxy_port="PROXY_PORT="+str(fake.random_int(min=1024, max=65535, step=1))
    proxy_username="PROXY_USERNAME="+fake.user_name()
    proxy_password="PROXY_PASSWORD="+fake.password(length=32, special_chars=True, digits=True, upper_case=True, lower_case=True)
    proxy_protocol="PROXY_PROTOCOL="+fake.random_element(elements=('http', 'https', 'socks4', 'socks5'))
    
    # WHEN
    response = post(
        'http://woopy-web:5000/docker-compose',
        headers={'Content-Type': 'text/plain',
                 'Accept': 'text/plain',
                 'User-Agent': 'WooPyAPI',
                 'Connection': 'keep-alive'},
        data="""
        {host_name}
        {host_ip}
        {host_mac}
        {host_cpu}
        {host_ram}
        {host_os}
        {host_kernel}
        {host_docker}
        {cache_host}
        {cache_port}
        {database_host}
        {database_port}
        {database_name}
        {database_user}
        {database_table_prefix}
        {website_title}
        {website_description}
        {website_hostname}
        {website_name}
        {website_admin_first_name}
        {website_admin_last_name}
        {website_admin_username}
        {website_admin_email}
        {mail_smtp_host}
        {mail_smtp_port}
        {mail_smtp_user}
        {mail_smtp_protocol}
        {redis_host}
        {redis_port}
        {redis_cache_enabled}
        {redis_cache_duration}
        {redis_cache_type}
        {pma_user}
        {woocommerce_enable}
        {woocommerce_tax_enabled}
        {woocommerce_tax_country}
        {woocommerce_tax_state}
        {woocommerce_tax_rate}
        {woocommerce_tax_shipping_enabled}
        {woocommerce_tax_shipping_class}
        {woocommerce_tax_shipping_rate}
        {woocommerce_tax_shipping_priority}
        {woocommerce_url}
        {woocommerce_key}
        {woocommerce_secret}
        {woocommerce_currency}
        {woocommerce_currency_position}
        {woocommerce_currency_thousands_separator}
        {woocommerce_currency_decimal_separator}
        {woocommerce_currency_decimals}
        {remote_server_username}
        {remote_server_ip}
        {remote_server_port}
        {remote_server_path}
        {proxy_title}
        {proxy_hostname}
        {proxy_port}
        {proxy_username}
        {proxy_password}
        {proxy_protocol}
        """.format(
            host_name=host_name,
            host_ip=host_ip,
            host_mac=host_mac,
            host_cpu=host_cpu,
            host_ram=host_ram,
            host_os=host_os,
            host_kernel=host_kernel,
            host_docker=host_docker,
            cache_host=cache_host,
            cache_port=cache_port,
            database_host=database_host,
            database_port=database_port,
            database_name=database_name,
            database_user=database_user,
            database_table_prefix=database_table_prefix,
            website_title=website_title,
            website_description=website_description,
            website_hostname=website_hostname,
            website_name=website_name,
            website_admin_first_name=website_admin_first_name,
            website_admin_last_name=website_admin_last_name,
            website_admin_username=website_admin_username,
            website_admin_email=website_admin_email,
            mail_smtp_host=mail_smtp_host,
            mail_smtp_port=mail_smtp_port,
            mail_smtp_user=mail_smtp_user,
            mail_smtp_protocol=mail_smtp_protocol,
            redis_host=redis_host,
            redis_port=redis_port,
            redis_cache_enabled=redis_cache_enabled,
            redis_cache_duration=redis_cache_duration,
            redis_cache_type=redis_cache_type,
            pma_user=pma_user,
            woocommerce_enable=woocommerce_enable,
            woocommerce_tax_enabled=woocommerce_tax_enabled,
            woocommerce_tax_country=woocommerce_tax_country,
            woocommerce_tax_state=woocommerce_tax_state,
            woocommerce_tax_rate=woocommerce_tax_rate,
            woocommerce_tax_shipping_enabled=woocommerce_tax_shipping_enabled,
            woocommerce_tax_shipping_class=woocommerce_tax_shipping_class,
            woocommerce_tax_shipping_rate=woocommerce_tax_shipping_rate,
            woocommerce_tax_shipping_priority=woocommerce_tax_shipping_priority,
            woocommerce_url=woocommerce_url,
            woocommerce_key=woocommerce_key,
            woocommerce_secret=woocommerce_secret,
            woocommerce_currency=woocommerce_currency,
            woocommerce_currency_position=woocommerce_currency_position,
            woocommerce_currency_thousands_separator=woocommerce_currency_thousands_separator,
            woocommerce_currency_decimal_separator=woocommerce_currency_decimal_separator,
            woocommerce_currency_decimals=woocommerce_currency_decimals,
            remote_server_username=remote_server_username,
            remote_server_ip=remote_server_ip,
            remote_server_port=remote_server_port,
            remote_server_path=remote_server_path,
            proxy_title=proxy_title,
            proxy_hostname=proxy_hostname,
            proxy_port=proxy_port,
            proxy_username=proxy_username,
            proxy_password=proxy_password,
            proxy_protocol=proxy_protocol
        )
    )

    # THEN
    assert response.status_code == 200
    assert response.text == "docker-compose.yml file created successfully."
    assert os.path.exists('docker-compose.yml')
    assert os.path.getsize('docker-compose.yml') > 0
    assert os.path.isfile('docker-compose.yml')
    



    
