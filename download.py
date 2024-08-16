#!/usr/bin/env python3

import os
import sys
import json
import time
import logging
import zipfile
import argparse
import requests

color_reset = "\033[0m"
color_red = "\033[1;31m"
color_green = "\033[1;32m"
color_yellow = "\033[1;33m"
color_blue = "\033[1;34m"

try:
    from tqdm import tqdm

    tqdm_installed = True
except ImportError:
    tqdm_installed = False
    print(f"{color_red}tqdm not installed, will not show progress bar.{color_reset}")
    time.sleep(2)


def parse_config(config_path):
    fonts_map = {}
    try:
        with open(config_path) as file:
            data = json.load(file)
        for font_name, urls in data.items():
            fonts_map[font_name] = urls
    except json.JSONDecodeError:
        print(
            f"{color_red} Error: Failed to parse JSON file {config_path}.{color_reset}"
        )
        sys.exit(1)
    except Exception as e:
        print(f"{color_red}Error: {e}{color_reset}")
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
        print(
            f"{color_red} Error: {config_name} not found in current and parent dir.{color_reset}"
        )
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
    print(f"Extracting {color_blue} {os.path.basename(src)} {color_reset}")
    with zipfile.ZipFile(src, "r") as zip_ref:
        zip_ref.extractall(det)


def get_fonts_from_config(fonts_map):
    current_dir = os.path.abspath(os.path.dirname(__file__))
    for font_name, urls in fonts_map.items():
        curr_font_dir = os.path.join(current_dir, font_name)
        os.makedirs(curr_font_dir, exist_ok=True)
        for url in urls:
            url = f"{download_proxy}{url}"
            basename = os.path.basename(url)
            download_path = os.path.join(curr_font_dir, basename)
            print("\n")
            print(f"Download {color_blue} {basename} {color_reset}")
            print(f"From {color_green} {url} {color_reset}")
            print(f"Save to {color_yellow} {download_path} {color_reset}")
            file_type = os.path.splitext(url)[1]
            if file_type == ".zip":
                download_font(url, download_path)
                extract_font(download_path, curr_font_dir)
                print(f"Remove {color_green} {download_path} {color_reset}")
                os.remove(download_path)
            elif file_type == ".ttf":
                download_font(url, download_path)
            else:
                print(f"{color_red} Unsupported file type: {file_type}. {color_reset}")


download_proxy = ""


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--proxy", action="store_true", help="Use proxy to download.")
    if parser.parse_args().proxy:
        global download_proxy
        download_proxy = "https://mirror.ghproxy.com/"
    print(
        f"{color_red}If you encounter any network issues, try using the --proxy parameter.{color_reset}\n"
    )
    fonts_map = load_config("fonts.json")
    get_fonts_from_config(fonts_map)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nCancelled by user.")
        sys.exit(0)
