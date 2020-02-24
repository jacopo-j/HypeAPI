#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from lxml import html


def parse_form(data, **fields):
    page = html.fromstring(data)
    form = page.xpath("//form")[0]
    url = form.xpath("./@action")[0]
    post_data = {**fields}
    for field in form.xpath("./input"):
        post_data[field.xpath("./@name")[0]] = field.xpath("./@value")[0]
    return {"url": url, "post_data": post_data}
