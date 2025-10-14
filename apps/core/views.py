from django.shortcuts import render
from django.http import HttpResponse


def homepage(request):
    """Temporary homepage view"""
    return HttpResponse("""
        <!DOCTYPE html>
        <html>
        <head>
            <title>AMMA CMS</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    min-height: 100vh;
                    margin: 0;
                    background: linear-gradient(135deg, #1a1a1a 0%, #2c2c2c 100%);
                    color: #d4af37;
                }
                .container {
                    text-align: center;
                    padding: 2rem;
                }
                h1 {
                    font-size: 3rem;
                    margin-bottom: 1rem;
                }
                p {
                    font-size: 1.2rem;
                    color: #f8f8f8;
                    margin-bottom: 2rem;
                }
                a {
                    display: inline-block;
                    padding: 12px 30px;
                    background-color: #d4af37;
                    color: #1a1a1a;
                    text-decoration: none;
                    border-radius: 5px;
                    font-weight: bold;
                    transition: all 0.3s ease;
                }
                a:hover {
                    background-color: #b8941f;
                    transform: translateY(-2px);
                }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>🏛️ AMMA CMS</h1>
                <p>Asokore Mampong Municipal Assembly</p>
                <p>Content Management System</p>
                <a href="/admin/">Go to Admin Panel</a>
            </div>
        </body>
        </html>
    """)
