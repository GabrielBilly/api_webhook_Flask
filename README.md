# Integração API com Webhook


## Bibliotecas Utilizadas

import os
import requests
from flask import Flask, request, render_template, flash, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_migrate import Migrate
from flask_login import LoginManager, UserMixin, login_user, login_required, current_user, logout_user


## Objetivo do Projeto

O sistema utiliza o framework Flask em Python para criar uma aplicação web. Ele possui as seguintes funcionalidades:
Registro e autenticação de usuários: O sistema permite que os usuários se cadastrem e façam login usando um endereço de e-mail e senha. O registro de novos usuários é validado por um token de acesso.
Página protegida: Existe uma página protegida que só pode ser acessada por usuários autenticados. Essa página exibe as tratativas (ações) realizadas com base nos webhooks recebidos.
Recebimento de webhooks: O sistema possui um endpoint ("/webhook") que aceita requisições POST contendo webhooks em formato JSON. Os webhooks contêm informações como nome, e-mail, status, valor, forma de pagamento e parcelas. Os webhooks são processados e salvos no banco de dados.
Tratamento de webhooks: Com base no campo "status" do webhook recebido, são realizadas ações específicas. Por exemplo, se o status for "aprovado", a ação registrada é "Liberar acesso". As ações são armazenadas no banco de dados juntamente com as informações do webhook.
Exibição das tratativas: Na página protegida, as tratativas (ações) são exibidas para os usuários autenticados. Os webhooks recebidos e as ações realizadas são recuperados do banco de dados e exibidos em uma tabela.
