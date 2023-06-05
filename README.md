# Integração API com Webhook


### Libraries Used:

    import os
    import requests
    from flask import Flask, request, render_template, flash, redirect, url_for, jsonify
    from flask_sqlalchemy import SQLAlchemy
    from werkzeug.security import generate_password_hash, check_password_hash
    from flask_migrate import Migrate
    from flask_login import LoginManager, UserMixin, login_user, login_required, current_user, logout_user


### Project's goal:

    The system uses the Flask framework in Python to create a web application. It has the following functionalities:
    User registration and authentication: The system allows users to register and login using an email address and password. Registration of new users is validated by an access token.
    Protected page: There is a protected page that can only be accessed by authenticated users. This page displays the dealings (actions) carried out based on the webhooks received.
    Receiving webhooks: The system has an endpoint ("/webhook") that accepts POST requests containing webhooks in JSON format. Webhooks contain information such as name, email, status, amount, payment method and installments. Webhooks are processed and saved in the database.
    Handling webhooks: Based on the "status" field of the received webhook, specific actions are performed. For example, if the status is "approved", the action recorded is "Grant access". Actions are stored in the database along with the webhook information.
    Display of dealings: On the protected page, dealings (actions) are displayed to authenticated users. Incoming webhooks and actions taken are retrieved from the database and displayed in a table.
    
    
### Deploy:
    https://api-webhook-tratativas.herokuapp.com/
    
    
## Att, Gabriel Souza
