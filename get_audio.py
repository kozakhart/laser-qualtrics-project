
import os
import shutil
import asyncio
import aiohttp
import csv
import glob
import time

async def download_audio(session, url, max_retries=3):
    file_id = url.split("file/")[1]
    output_file = f"{file_id}.mp3"
    retries = 0

    while retries < max_retries:
        try:
            async with session.get(url, timeout=None) as response:
                if response.status == 200:
                    with open(output_file, "wb") as f:
                        while True:
                            chunk = await response.content.read(1024)
                            if not chunk:
                                break
                            f.write(chunk)
                    print("File downloaded successfully as", output_file)
                    return
                elif response.status == 202:
                    print("File not ready yet. Retrying...")
                    retries += 1
                    print(f"Retrying ({retries}/{max_retries})...")
                    await asyncio.sleep(1)
                else:
                    print("Failed to download the file. Status code:", response.status)
                    return
        except aiohttp.ClientError as e:
            print(f"Error occurred: {e}")
            retries += 1
            print(f"Retrying ({retries}/{max_retries})...")
            await asyncio.sleep(1) 

async def concurrent_download(urls, concurrency_limit):
    async with aiohttp.ClientSession() as session:
        semaphore = asyncio.Semaphore(concurrency_limit)
        async with semaphore:
            tasks = [download_audio(session, url) for url in urls]
            await asyncio.gather(*tasks)

async def get_sample_urls_from_csv(csv_file, concurrency_limit):
    start_time = time.time()
    urls = []
    with open(csv_file, 'r', encoding='utf-8') as file:
        csv_reader = csv.DictReader(file)
        urls = [row.get("SupSpR1_URL", "") for row in csv_reader if row.get("SupSpR1_URL", "").startswith("https")]

    await concurrent_download(urls, concurrency_limit)

    source_directory = os.getcwd()
    destination_directory = "demonstration"
    mp3_files = glob.glob(os.path.join(source_directory, "*.mp3"))

    for mp3_file in mp3_files:
        destination_path = os.path.join(destination_directory, os.path.basename(mp3_file))
        
        shutil.move(mp3_file, destination_path)
        print(f"Moved '{mp3_file}' to '{destination_path}'")

    end_time = time.time()  # Record the end time
    runtime = end_time - start_time  # Calculate the total runtime
    print(f"Script completed in {runtime:.2f} seconds.")
    print(f"Downloaded {len(mp3_files)} files.")

concurrency_limit = 10
asyncio.run(get_sample_urls_from_csv('LaSER_2_Winter2024.csv', concurrency_limit))

