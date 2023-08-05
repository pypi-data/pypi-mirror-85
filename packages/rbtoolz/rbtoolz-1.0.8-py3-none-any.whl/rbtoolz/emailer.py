#!/usr/bin/env python
# -*- coding: utf-8 -*-


""" Code for programatic emailing of images, requires SSL e.g workplace or gmail.
"""


__author__ = 'Ross Bonallo'
__license__ = 'MIT Licence'
__version__ = '1.0.3'

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage


def send_email(_from, _to, subject, heading=None, message=None, image_file_paths=None):

    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = _from
    msg['To'] = _to

    as_row = True

    if image_file_paths:
        img_srcs = ' '.join(['<img scr="cid:image{}" width=1200>'.format(i)
            for i in range(len(image_file_paths))])

    else:
        img_srcs = ''

    heading = '<h3>{}</h3>'.format(heading) if heading else ''
    message = message if message else ''

    html = """<p>{}{}<br/>{}</p>""".format(heading, message, img_srcs)

    msgHtml = MIMEText(html, 'html')

    if image_file_paths:

        for (filename, i) in zip(image_file_paths, list(range(len(image_file_paths)))):
            img = open(filename, 'rb').read()
            msgImg = MIMEImage(img, 'png')
            msgImg.add_header('Content-ID', '<image{}>'.format(i))
            msgImg.add_header('Content-Disposition', 'inline', filename=filename)

            msg.attach(msgHtml)
            msg.attach(msgImg)

    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    username, pwd = '','' # Not setup 
    server.ehlo()
    server.login(username, pwd)
    server.send_message(msg)
    server.quit()

