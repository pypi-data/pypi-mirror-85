#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
from requests import Response
from .. import const
from ..model.colors import BColors


class API:
    @staticmethod
    def find_instance():
        with open(const.ALLO_INFO_PATH, 'rb') as payload:
            r = requests.post("{}/referees/{}".format(const.API_PATH, const.getnode()), verify=False, data=payload)
            if API.has_error(r):
                return False
            return r.json()

    @staticmethod
    def get_secret():
        r = requests.get("{}/referees/{}/secret".format(const.API_PATH, const.getnode()), verify=False)
        if API.has_error(r):
            return False
        return r.text

    @staticmethod
    def ask_install():
        with open(const.ALLO_INFO_PATH, 'rb') as payload:
            r = requests.post("{}/referees/{}/install".format(const.API_PATH, const.getnode()), verify=False, data=payload)
            if API.has_error(r):
                return False
            return r.text

    @staticmethod
    def get_versions(beta):
        url = "{}/referees/{}/versions/beta" if beta else "{}/referees/{}/versions"
        r = requests.get(url.format(const.API_PATH, const.getnode()), verify=False)
        if API.has_error(r):
            return False
        return r.json()

    @staticmethod
    def update_to_version(versionid, beta):
        with open(const.ALLO_INFO_PATH, 'rb') as payload:
            url = "{}/referees/{}/update/{}/beta" if beta else "{}/referees/{}/update/{}"
            r = requests.post(url.format(const.API_PATH, const.getnode(), versionid),
                              verify=False, data=payload)
            if API.has_error(r):
                return False
            return r.text

    @staticmethod
    def has_error(r: Response):
        if r.status_code is 502:
            BColors.error("Erreur lors de la communication avec Allo Server : Erreur {}".format(r.status_code))
            return True
        return False
