# -*- coding: utf-8 -*-
import sendgrid
import base64 

from os import environ
from os.path import join
from os.path import dirname


from sendgrid.helpers.mail import *
from sendgrid.helpers.mail import Mail as sendMail

import library.config as config




def send_mail(to,subject,body):
    from_email = Email(config.FROM_EMAIL,name='Gestor de Tareas')
    to_email = Email(to)
    sg = sendgrid.SendGridAPIClient(apikey=config.API_KEY)
    content = Content("text/html", body)
    mail = sendMail(from_email, subject, to_email, content)
    response = sg.client.mail.send.post(request_body=mail.get())
    return True


def get_plantilla(email,nombre,contrasena='',creacion=True,token='VACIO'):
    plantilla = """<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
            <html xmlns="http://www.w3.org/1999/xhtml">
            <head>
            <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
            <title>Demystifying Email Design</title>
            <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
            <style>
                .d-flex{
                    display: flex;
                    justify-content: center;
                    align-items: center;
                }

                .mail{
                    background-color: #1476b8;
                    color: #fff;
                    padding: 15px 15px 10px 15px;
                    margin: 15px 0 20px;
                    border-radius: 10px;
                    text-align: left;
                    justify-content: center;
                    align-items: center;

                }
                .main{
                    padding:40px;
                }
                body {
                    font-family: Open sans, sans-serif;
                    line-height: 130%;
                    font-size: 13px;
                    width: 100%;
                }
                .link{
                    padding;50px;
                }
                p{
                    margin-bottom: 5px;
                }
                h4{
                    margin-bottom: 10px; 
                }
                #url{
                    padding:45%;
                }
            </style>
            </head>
            <body style="margin: 0; padding: 0;">
                <table border="0" cellpadding="0" cellspacing="0" width="100%">	
                    <tr>
                        <td style="padding: 10px 0 30px 0;">
                            <table align="center" border="0" cellpadding="0" cellspacing="0" width="600" style="border: 1px solid #cccccc; border-collapse: collapse;">
                                <tr>
                                    <td align="center" bgcolor="#1476b8" style="padding: 40px 0 30px 0; color: #153643; font-size: 28px; font-weight: bold; font-family: Arial, sans-serif;">
                                        <img src="https://pngimage.net/wp-content/uploads/2018/05/bienvenida-png.png" alt="Creating Email Magic" width="300" height="230" style="display: block;" />
                                    </td>
                                </tr>
                                <tr>
                                    <td bgcolor="#ffffff" style="padding: 40px 30px 40px 30px;">
                                        <table border="0" cellpadding="0" cellspacing="0" width="100%">
                                            <tr>
                                                <td style="color: #153643; font-family: Arial, sans-serif; font-size: 24px;">
                                                    <b>Estimado: @Nombre_Usuario</b>
                                                </td>
                                            </tr>
                                            <tr>"""
    plantilla = plantilla.replace('@Nombre_Usuario',nombre)
    if creacion:
        plantilla += """<td style="padding: 20px 0 30px 0; color: #153643; font-family: Arial, sans-serif; font-size: 16px; line-height: 20px;">
                            <h3><span align='center'>Le damos la más cordial bienvenida a <b> Gestor de Tareas.</b></span></h3>
                            <br><br>
                            Sus credenciales son las siguiente:
                            <br>
                            <div class="d-flex">
                                <div class="mail">
                                    <p><strong>Usuario:</strong> @USUARIO </p>
                                    <p><strong>Password:</strong> @CONTRASENA </p>       
                                </div>
                            </div>
                            <div>
                                <a href="http://localhost:4200/new-password/@TOKEN" target="_blank" id='url'>LINK</a>
                            </div>
                            <br>
                            <p>El link tiene una duracion de 30 minutos desde el momento en que se recibe el correo</p>
                        </td>"""
        plantilla = plantilla.replace('@USUARIO',email)
        plantilla = plantilla.replace('@CONTRASENA',contrasena)
    else:
        plantilla += """<td style="padding: 20px 0 30px 0; color: #153643; font-family: Arial, sans-serif; font-size: 16px; line-height: 20px;">
                            <h3><span align='center'>Le damos la más cordial bienvenida a <b> Gestor de Tareas.</b></span></h3>
                            <br><br>
                            Este es el correo de recuperación de contraseña
                            <div>
                                <a href="http://localhost:4200/new-password/@TOKEN" target="_blank" id='url'>LINK</a>
                            </div>
                            <br>
                            <p>El link tiene una duracion de 30 minutos desde el momento en que se recibe el correo</p>
                        </td>"""



    plantilla = plantilla.replace('@TOKEN',str(token))

    plantilla+="""</tr>
                                    </table>
                                </td>
                            </tr>
                            <tr>
                                <td bgcolor="#ee4c50" style="padding: 30px 30px 30px 30px;">
                                    <table border="0" cellpadding="0" cellspacing="0" width="100%">
                                        <tr>
                                            <td style="color: #ffffff; font-family: Arial, sans-serif; font-size: 14px;" width="75%">
                                                &reg; Los Kbros spa. 2019<br/>
                                                &nbsp;<font color="#ffffff">info@loskbros.cl</font>
                                            </td>
                                            <td align="right" width="25%">
                                                <table border="0" cellpadding="0" cellspacing="0">
                                                    <tr>
                                                        <td style="font-family: Arial, sans-serif; font-size: 12px; font-weight: bold;">
                                                            <a href="http://www.twitter.com/" style="color: #ffffff;">
                                                                <img src="https://image.flaticon.com/icons/png/512/23/23931.png" alt="Twitter" width="38" height="38" style="display: block;" border="0" />
                                                            </a>
                                                        </td>
                                                        <td style="font-size: 0; line-height: 0;" width="20">&nbsp;</td>
                                                        <td style="font-family: Arial, sans-serif; font-size: 12px; font-weight: bold;">
                                                            <a href="http://www.facebook.com/" style="color: #ffffff;">
                                                                <img src="https://image.flaticon.com/icons/png/512/33/33702.png" alt="Facebook" width="38" height="38" style="display: block;" border="0" />
                                                            </a>
                                                        </td>
                                                    </tr>
                                                </table>
                                            </td>
                                        </tr>
                                    </table>
                                </td>
                            </tr>
                        </table>
                    </td>
                </tr>
            </table>
        </body>
        </html>

        """
    return plantilla