#!/usr/bin/env python
# -*- coding: utf-8 -*-
# peer_titles.py
"""Collection of peer titles."""
import json
import requests
import unicodedata
from bs4 import BeautifulSoup
from typing import List


def peertitles() -> dict:
    try:
        with open('./persontitles/peertitles.json', mode='r', encoding='utf-8') as fin:  # noqa
            PEERTITLES = json.load(fin)
    except FileNotFoundError:
        PEERTITLES = _titles()
        with open('./persontitles/peertitles.json', mode='w', encoding='utf-8') as fout:  # noqa
            json.dump(PEERTITLES, fout)

    return PEERTITLES


def get_table(soup):
    for h2 in soup.find_all('h2'):
        if 'Adelstitel in verschiedenen Sprachen' in h2.text:
            tbody = h2.find_next('tbody')

    return tbody


def get_titles(tbody, language):
    """Get country specific titles."""
    counter = 16
    index = 17
    titles = []
    residue = _residue(language)
    for td in tbody.find_all('td'):
        if index % counter == residue:
            title = td.text.split(',')
            # print(title)
            titles.append(title)
        index += 1

    return titles


def _residue(language):
    language_dict = {
        'German': 1,
        'Latin': 2,
        'French': 3,
        'Italian': 4,
        'Spanish': 5,
        'English': 6,
        'Danish': 7,
        'Greek': 8,
        'Dutch': 9,
        'Czech': 10,
        'Hungarian': 11,
        'Russian': 12,
        'Persian': 13,
        'Arab': 14,
        'Chinese': 15,
        'Amharic': 0,
    }

    return language_dict[language]


LANGUAGES = [
    'German',
    'Latin',
    'French',
    'Italian',
    'Spanish',
    'English',
    'Danish',
    'Greek',
    'Dutch',
    'Czech',
    'Hungarian',
    'Russian',
    'Persian',
    'Arab',
    'Chinese',
    'Amharic',
]


def _titles() -> dict:
    # data = requests.get('https://www.heraldik-wiki.de/wiki/Adelstitel#Adelstitel_in_verschiedenen_Sprachen')  # noqa
    peer_dict = dict()
    data = requests.get('https://de.wikipedia.org/wiki/Adelstitel')
    soup = BeautifulSoup(data.text, 'lxml')
    tbody = get_table(soup)
    for language in LANGUAGES:
        titles = get_titles(tbody, language)
        stripped_titles = strip_titles(titles)
        final_titles = finalize_titles(stripped_titles, language)
        unique_titles = _unique(final_titles)
        peer_dict[language] = unique_titles

    return peer_dict


def strip_titles(titles) -> list:
    peers = []
    for i, title in enumerate(titles):
        for item in title:
            if '[' in item:
                ttle = item.split('[')[0]
                peers.append(ttle)
            else:
                item = item.strip()
                if ';' in item:
                    item = item[:-1]
                peers.append(item.strip())

    return peers


def finalize_titles(peers, language) -> list:
    final_titles: List = []
    for peer in peers:
        if language == 'German':
            final_titles = finalize_german_titles(final_titles, peer)
        elif language == 'Latin':
            final_titles = finalize_latin_titles(final_titles, peer)
        elif language in ['French', 'Russian', 'Chinese', 'Persian', 'Arab']:
            final_titles = finalize_french_titles(final_titles, peer)
        elif language in ['Spanish', 'Italian', 'Danish', 'Greek', 'Hungarian']:  # noqa
            final_titles = finalize_spanish_titles(final_titles, peer)
        elif language in ['Dutch', 'Czech', 'Amharic']:
            final_titles = finalize_dutch_titles(final_titles, peer)
        elif language == 'English':
            final_titles = finalize_english_titles(final_titles, peer)

    return final_titles


def _unique(final_titles) -> list:
    uniques = []
    for item in set(final_titles):
        item = unicodedata.normalize('NFKD', item)
        uniques.append(item)

    return uniques


def finalize_german_titles(final_titles, peer):
    # German
    if peer == 'BaronFreifrau':
        final_titles.append('Baron')
        final_titles.append('Freifrau')
    elif peer == '(Groß-)Herzogin':
        final_titles.append('Großherzogin')
    elif peer in ['Herr', 'Frau', 'Fräulein']:
        pass
    elif 'Freiin' in peer:
        final_titles.append('Baronin')
        final_titles.append('Freiin')
    else:
        final_titles.append(peer)

    return final_titles


def finalize_latin_titles(final_titles, peer):
    if 'Eques/' in peer:
        final_titles.append('Eques')
        final_titles.append('Miles')
    elif '(Vir)' in peer:
        final_titles.append('Nobilis')
        final_titles.append('Vir nobilis')
    elif '(Zwei' in peer:
        final_titles.append('Imperatrix')
    elif peer == '':
        pass
    else:
        final_titles.append(peer)

    return final_titles


def finalize_french_titles(final_titles, peer):
    # print(peer)
    if 'im Sinne' in peer or 'Fürst' in peer:
        pass
    elif 'Le/' in peer:
        peer_ttle = peer.split(' ')[-1]
        if peer_ttle == 'Rougrave':
            final_titles.append('Le ' + peer_ttle)
            final_titles.append('La ' + peer_ttle)
            peer_ttle = 'Raugraveoder'
            final_titles.append('Le ' + peer_ttle)
            final_titles.append('La ' + peer_ttle)
    elif peer == '':
        pass
    elif '(' in peer:
        peer_tmp = peer.split('(')[0].strip()
        if peer_tmp == '':
            pass
        else:
            final_titles.append(peer_tmp)
        peer = peer.split('(')[-1].strip()
        peer_tmp = peer.split(')')[0].strip()
        final_titles.append(peer_tmp)
    elif ')' in peer:
        final_titles.append(peer.split(')')[0].strip())
    elif 'pl.' in peer:
        final_titles.append(peer.split('pl.')[-1].strip())
    elif peer.split(' ')[-1] == 'Schah':
        final_titles.append(peer.split(' ')[0].strip())
        final_titles.append(peer.split(' ')[-1].strip())
    else:
        final_titles.append(peer)

    return final_titles


def finalize_spanish_titles(final_titles, peer):
    if peer == '':
        pass
    elif '/' in peer:
        peers = peer.split('/')
        final_titles.append(peers[0].strip())
        final_titles.append(peers[-1].strip())
    else:
        final_titles.append(peer)

    return final_titles


def finalize_dutch_titles(final_titles, peer):
    # print(peer)
    if peer == '':
        pass
    elif 'Wildgraaf' in peer:
        final_titles.append('Wildgraaf')
        final_titles.append('Wildgraavin')
    elif ';' in peer:
        final_titles.append(peer.split(';')[0].strip())
        final_titles.append(peer.split(';')[-1].strip())
    elif '(' in peer:
        final_titles.append(peer.split('(')[0].strip())
    elif 'Grazmach' in peer:
        final_titles.append('Grazmach')
    else:
        final_titles.append(peer)

    return final_titles


def finalize_english_titles(final_titles, peer):
    if 'Baron /' in peer:
        final_titles.append('Sovereign Baron')
        final_titles.append('Sovereign Baroness')
    elif '/' in peer:
        peers = peer.split('/')
        final_titles.append(peers[0].strip())
        final_titles.append(peers[-1].strip())
#     elif 'Marchioness/' in peer:
#         final_titles.append('Marchioness')
#         final_titles.append('Margravine')
#     elif 'Knight/' in peer:
#         final_titles.append('Knight')
#         final_titles.append('Dame')
    elif peer == '':
        pass
    else:
        final_titles.append(peer)

    return final_titles


if __name__ == '__main__':
    peers = _titles()
    for k, v in peers.items():
        print(k, v)
        print()
