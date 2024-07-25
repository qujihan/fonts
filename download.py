#!/usr/bin/env python3

import os
import sys
import json
import zipfile
import argparse
import requests


try:
    from tqdm import tqdm

    tqdm_installed = True
except ImportError:
    tqdm_installed = False
    print("tqdm not installed, will not show progress bar.")


def parse_config(config_path):
    fonts_map = {}
    try:
        with open(config_path) as file:
            data = json.load(file)
        for font_name, urls in data.items():
            fonts_map[font_name] = urls
    except json.JSONDecodeError:
        print(f"Error: Failed to parse JSON file {config_path}. ")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
    return fonts_map


def load_config(config_name):
    current_dir = os.path.abspath(os.path.dirname(__file__))
    parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
    parent_config_path = os.path.join(parent_dir, config_name)
    current_config_path = os.path.join(current_dir, config_name)
    parent_config_exist = os.path.exists(parent_config_path)
    current_config_exist = os.path.exists(current_config_path)
    if parent_config_exist:
        return parse_config(parent_config_path)
    elif current_config_exist:
        return parse_config(current_config_path)
    else:
        print(f"Error: {config_name} not found in current and parent dir. ")
        sys.exit(1)


def download_font(url, path):
    response = requests.get(url, stream=True)
    total_size = int(response.headers.get("content-length", 0))
    block_size, downloaded_size = 1024, 0

    if tqdm_installed:
        progress_bar = tqdm(total=total_size, unit="iB", unit_scale=True)

    with open(path, "wb") as file:
        for data in response.iter_content(block_size):
            downloaded_size += len(data)
            file.write(data)
            if tqdm_installed:
                progress_bar.update(len(data))
            else:
                progress = downloaded_size / total_size * 100
                print(f"Download {os.path.basename(path)}: {progress:.2f}%")


def extract_font(src, det):
    with zipfile.ZipFile(src, "r") as zip_ref:
        zip_ref.extractall(det)


def get_fonts_from_config(fonts_map):
    current_dir = os.path.abspath(os.path.dirname(__file__))
    for font_name, urls in fonts_map.items():
        curr_font_dir = os.path.join(current_dir, font_name)
        os.makedirs(curr_font_dir, exist_ok=True)
        for url in urls:
            url = f"{download_proxy}{url}"
            download_path = os.path.join(curr_font_dir, os.path.basename(url))
            print(f"Download{font_name} from {url}")
            file_type = os.path.splitext(url)[1]
            if file_type == ".zip":
                download_font(url, download_path)
                extract_font(download_path, curr_font_dir)
                os.remove(download_path)
            elif file_type == ".ttf":
                download_font(url, download_path)
            else:
                print(f"Unsupported file type: {file_type}. ")

download_proxy = ""

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--proxy", action="store_true", help="Use proxy to download.")
    if parser.parse_args().proxy:
        global download_proxy
        download_proxy = "https://mirror.ghproxy.com/"

    fonts_map = load_config("fonts.json")
    get_fonts_from_config(fonts_map)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nCancelled by user.")
        sys.exit(0)
