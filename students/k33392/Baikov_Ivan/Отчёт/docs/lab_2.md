# Лабораторная работа №2

Цель работы: понять отличия перечисленных понятий.

## Задача №1

Задача: Напишите три различных программы на Python, использующие каждый из подходов: threading, multiprocessing и async. Каждая программа должна решать считать сумму всех чисел от 1 до 1000000. Разделите вычисления на несколько параллельных задач для ускорения выполнения.

Подробности задания:

Напишите программу на Python для каждого подхода: threading, multiprocessing и async.
Каждая программа должна содержать функцию calculate_sum(), которая будет выполнять вычисления.
Для threading используйте модуль threading, для multiprocessing - модуль multiprocessing, а для async - ключевые слова async/await и модуль asyncio.
Каждая программа должна разбить задачу на несколько подзадач и выполнять их параллельно.
Замерьте время выполнения каждой программы и сравните результаты.

## Ход выполнения работы

### async.py:
    import asyncio
    import time
    
    
    async def calculate_sum(start, end):
        return sum(range(start, end))
    
    async def main():
        tasks = 69
        total = 10000000
        step = total // tasks
        tasks_arr = []
    
        start = 1
        end = step + total % tasks + 1
    
        for i in range(tasks):
            task = asyncio.create_task(calculate_sum(start, end))
            start = end
            end = end + step
            tasks_arr.append(task)
    
        results = await asyncio.gather(*tasks_arr)
        total = sum(results)
        print(f"Total: {total}")
    
    
    if __name__ == "__main__":
        print("Async")
        start_time = time.time()
        asyncio.run(main())
        end_time = time.time()
        print(f"Time: {end_time - start_time} seconds")

### multik.py:
    import multiprocessing
    import time
    
    
    def calculate_sum(start, end):
        return sum(range(start, end))
    
    def worker(start, end, queue):
        queue.put(calculate_sum(start, end))
    
    if __name__ == '__main__':
        print("Multiprocessing")
        start_time = time.time()
    
        tasks = 69
        total = 10000000
        step = total // tasks
        tasks_arr = []
        queue = multiprocessing.Queue()
    
        start = 1
        end = step + total % tasks + 1
    
        for i in range(tasks):
            task = multiprocessing.Process(target=worker, args=(start, end, queue))
            start = end
            end = end + step
            tasks_arr.append(task)
            task.start()
    
        for task in tasks_arr:
            task.join()
    
        results = [queue.get() for i in tasks_arr]
        total_sum = sum(results)
        print(f"Total: {total_sum}")
    
        end_time = time.time()
        print(f"Time: {end_time - start_time} seconds")



### threads.py:
    import threading
    import time
    
    lock = threading.Lock()
    
    def calculate_sum(start, end):
        return sum(range(start, end))
    
    def worker(start, end, result):
        answer = calculate_sum(start, end)
        lock.acquire()
        result.append(answer)
        lock.release()
    
    
    print("Threading")
    start_time = time.time()
    
    tasks = 69
    total = 10000000
    step = total // tasks
    threads = []
    results = []
    
    start = 1
    end = step + total % tasks + 1
    
    for i in range(tasks):
        thread = threading.Thread(target=worker, args=(start, end, results))
        start = end
        end = end + step
        threads.append(thread)
        thread.start()
    
    for thread in threads:
        thread.join()
    
    total_answer = sum(results)
    print(f"Total: {total_answer}")
    
    end_time = time.time()
    print(f"Time: {end_time - start_time} seconds")

## Результат

![Результат](images/lab_2/hZjRC26pZ6c.jpg)

![Результат](images/lab_2/mhhGFj5s8RE.jpg)

![Результат](images/lab_2/Zg7XxQDgGmw.jpg)


## Задача №2

Напишите программу на Python для параллельного парсинга нескольких веб-страниц с сохранением данных в базу данных с использованием подходов threading, multiprocessing и async. Каждая программа должна парсить информацию с нескольких веб-сайтов, сохранять их в базу данных.

Подробности задания:

Напишите три различных программы на Python, использующие каждый из подходов: threading, multiprocessing и async.
Каждая программа должна содержать функцию parse_and_save(url), которая будет загружать HTML-страницу по указанному URL, парсить ее, сохранять заголовок страницы в базу данных и выводить результат на экран.
Используйте PostgreSQL или другую базу данных на ваш выбор для сохранения данных.
Для threading используйте модуль threading, для multiprocessing - модуль multiprocessing, а для async - ключевые слова async/await и модуль aiohttp для асинхронных запросов.
Создайте список нескольких URL-адресов веб-страниц для парсинга и разделите его на равные части для параллельного парсинга.
Запустите параллельный парсинг для каждой программы и сохраните данные в базу данных.
Замерьте время выполнения каждой программы и сравните результаты.

## Ход выполнения работы

### asyio.py:
    import asyncio
    import aiohttp
    import time
    import requests
    from bs4 import BeautifulSoup
    import asyncpg
    
    from part_2.conn import sion, init_db
    from models import *
    from urls import URLS
    
    QUERY = """INSERT INTO product (title, name, cost) VALUES ($1, $2, $3)"""
    
    
    async def parse_and_save(url, db_pool):
        try:
            async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
                async with session.get(url) as response:
                    r = await response.text()
                    soup = BeautifulSoup(r, 'html.parser')
                    print("Type of furniture: ", soup.find('title').text)
                    title = soup.find('title').text
                    products = soup.find_all('div', class_="product-card__info")
                    for product in products:
                        try:
                            name = product.find('div', class_='product-card__title').get_text().strip()
                            price = product.find('div', class_='product-card__buy-wrapper').find('div', class_='product-card__price-wrapper').get_text().strip()
                            price_info = price.split('\n')
                            price_info = price_info[0].strip()
                            await db_pool.fetch(QUERY,title, name, price_info)
                        except Exception as e:
                            print(e)
        except Exception as ex:
            print(ex)
    
    async def main():
        tasks = []
        db_pool = await asyncpg.create_pool('postgresql://postgres:Scalapendra1219212712192127@localhost:5433/product_db')
    
        for url in URLS:
            task = asyncio.create_task(parse_and_save(url, db_pool))
            tasks.append(task)
        await asyncio.gather(*tasks)
    
    
    if __name__ == '__main__':
        init_db()
        start_time = time.time()
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        asyncio.run(main())
        end_time = time.time()
        print(f"Async time ': {end_time - start_time} seconds")
### mp.py
    import multiprocessing
    import time
    import requests
    from bs4 import BeautifulSoup
    
    from part_2.conn import sion, init_db
    from models import *
    from urls import URLS
    
    
    def parse_and_save(queue,url):
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')
        print("Type of furniture: ", soup.find('title').text)
        title = soup.find('title').text
        products = soup.find_all('div', class_="product-card__info")
        for product in products:
            try:
                name = product.find('div', class_='product-card__title').get_text().strip()
                price = product.find('div', class_='product-card__buy-wrapper').find('div', class_='product-card__price-wrapper').get_text().strip()
                price_info = price.split('\n')
                price_info = price_info[0].strip()
                queue.put((title, name, price_info))
            except Exception as e:
                pass
        queue.put(None)
    
    if __name__ == '__main__':
        init_db()
        start_time = time.time()
        queue = multiprocessing.Queue()
        processes = []
        for url in URLS:
            process = multiprocessing.Process(target=parse_and_save,args=(queue, url))
            processes.append(process)
            process.start()
        len_proc = len(URLS)
        while len_proc>0:
            data = queue.get()
            if data is None:
                len_proc = len_proc - 1
            else:
                title, name, cost  = data[0], data[1], data[2]
                pesnya = Product(name=name, cost = cost, title=title)
                sion.add(pesnya)
                sion.commit()
        end_time = time.time()
        print(f"Multiprocessing time ': {end_time - start_time} seconds")
### threads.py
    import threading
    import time
    import requests
    from bs4 import BeautifulSoup
    
    from part_2.conn import sion, init_db
    from models import *
    from urls import URLS
    
    lock = threading.Lock()
    
    def parse_and_save(url):
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')
        print("Type of furniture: ",soup.find('title').text)
        title = soup.find('title').text
        products = soup.find_all('div', class_="product-card__info")
        for product in products:
            try:
                name = product.find('div', class_ = 'product-card__title').get_text().strip()
                price = product.find('div', class_='product-card__buy-wrapper').find('div',class_='product-card__price-wrapper').get_text().strip()
                price_info = price.split('\n')
                price_info = price_info[0].strip()
                lock.acquire()
                prod = Product(name = name, title = title, cost = price_info)
                sion.add(prod)
                sion.commit()
                lock.release()
            except Exception as e:
                pass
    
    if __name__ == '__main__':
    
        init_db()
        start_time = time.time()
        threads = []
        for url in URLS:
            thread = threading.Thread(target=parse_and_save, args=(url,))
            threads.append(thread)
            thread.start()
        for thread in threads:
            thread.join()
        end_time = time.time()
        print(f"Threading time ': {end_time - start_time} seconds")
## Результат

![Результат](images/lab_2/1.jpg)
![Результат](images/lab_2/2.jpg)
![Результат](images/lab_2/3.jpg)


