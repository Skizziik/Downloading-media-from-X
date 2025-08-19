#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
import requests
import re
from urllib.parse import urlparse
from pathlib import Path
from datetime import datetime
import json
import time
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

def extract_tweet_id(url):
    patterns = [
        r'twitter\.com/\w+/status/(\d+)',
        r'x\.com/\w+/status/(\d+)',
        r'/status/(\d+)'
    ]
    
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None

def get_media_urls(tweet_url):
    tweet_id = extract_tweet_id(tweet_url)
    if not tweet_id:
        print(f"[ERROR] Failed to extract tweet ID from: {tweet_url}")
        return []
    
    try:
        api_url = f"https://api.vxtwitter.com/Twitter/status/{tweet_id}"
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        response = requests.get(api_url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            media_urls = []
            
            # Check for media in extended format
            if 'media_extended' in data:
                for media in data['media_extended']:
                    if media['type'] == 'video':
                        if 'url' in media:
                            media_urls.append({'url': media['url'], 'type': 'video'})
                    elif media['type'] == 'image':
                        if 'url' in media:
                            media_urls.append({'url': media['url'], 'type': 'image'})
            
            # Fallback to mediaURLs if no extended media found
            if not media_urls and 'mediaURLs' in data:
                for url in data['mediaURLs']:
                    if '.mp4' in url:
                        media_urls.append({'url': url, 'type': 'video'})
                    else:
                        media_urls.append({'url': url, 'type': 'image'})
            
            return media_urls
        else:
            print(f"[ERROR] API Error: {response.status_code}")
            return []
            
    except Exception as e:
        print(f"[ERROR] Error fetching media: {str(e)}")
        return []

def download_media(url, save_path, media_type, index=1):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        response = requests.get(url, headers=headers, stream=True, timeout=30)
        response.raise_for_status()
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        if media_type == 'video':
            extension = '.mp4'
        else:
            extension = os.path.splitext(urlparse(url).path)[1] or '.jpg'
        
        filename = f"media_{timestamp}_{index}{extension}"
        filepath = os.path.join(save_path, filename)
        
        total_size = int(response.headers.get('content-length', 0))
        downloaded = 0
        
        with open(filepath, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    file.write(chunk)
                    downloaded += len(chunk)
                    if total_size > 0:
                        progress = (downloaded / total_size) * 100
                        print(f"\rDownloading: {progress:.1f}%", end='')
        
        print(f"\n[SUCCESS] Downloaded: {filename}")
        return True
        
    except Exception as e:
        print(f"\n[ERROR] Download error: {str(e)}")
        return False

def main():
    print("=" * 50)
    print("X/Twitter Media Downloader")
    print("=" * 50)
    
    links_file = "links.txt"
    if not os.path.exists(links_file):
        print(f"[ERROR] File {links_file} not found!")
        print("Create links.txt file and add media links (one link per line)")
        with open(links_file, 'w', encoding='utf-8') as f:
            f.write("")
        return
    
    with open(links_file, 'r', encoding='utf-8') as f:
        links = [line.strip() for line in f if line.strip()]
    
    if not links:
        print(f"[ERROR] File {links_file} is empty!")
        print("Add media links to the file (one link per line)")
        return
    
    download_dir = input("\nSpecify download folder (Enter for default): ").strip()
    if not download_dir:
        download_dir = "downloads"
    
    download_path = Path(download_dir)
    download_path.mkdir(parents=True, exist_ok=True)
    
    print(f"\nMedia will be saved to: {download_path.absolute()}")
    print(f"Links found: {len(links)}")
    print("-" * 50)
    
    total_downloaded = 0
    failed_links = []
    
    for i, link in enumerate(links, 1):
        print(f"\n[{i}/{len(links)}] Processing: {link}")
        
        media_urls = get_media_urls(link)
        
        if media_urls:
            print(f"Media found: {len(media_urls)}")
            for j, media in enumerate(media_urls, 1):
                if download_media(media['url'], str(download_path), media['type'], f"{i}_{j}"):
                    total_downloaded += 1
                time.sleep(1)
        else:
            print("[WARNING] No media found")
            failed_links.append(link)
        
        time.sleep(2)
    
    print("\n" + "=" * 50)
    print("SUMMARY:")
    print(f"Successfully downloaded: {total_downloaded} files")
    if failed_links:
        print(f"Failed to process: {len(failed_links)} links")
        for link in failed_links:
            print(f"   - {link}")
    print("=" * 50)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n[WARNING] Interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n[ERROR] Critical error: {str(e)}")
        sys.exit(1)