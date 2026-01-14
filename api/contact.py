from http.server import BaseHTTPRequestHandler
import json
from datetime import datetime
import os
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, OperationFailure


class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        # Omogući CORS
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

        try:
            # Čitaj podatke iz POST requesta
            content_length = int(self.headers["Content-Length"])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode("utf-8"))

            # Pripremi podatke za spremanje
            contact_entry = {
                "name": data.get("name", ""),
                "email": data.get("email", ""),
                "message": data.get("message", ""),
                "timestamp": datetime.now().isoformat(),
                "ip": self.headers.get("X-Forwarded-For", "unknown"),
            }

            # Spoji se na MongoDB Atlas
            mongo_uri = os.environ.get("MONGODB_URI")

            if not mongo_uri:
                raise ValueError("MONGODB_URI environment variable nije postavljena")

            # Kreiraj MongoDB klijent
            client = MongoClient(mongo_uri, serverSelectionTimeoutMS=5000)

            # Testiraj konekciju
            client.admin.command("ping")

            # Odaberi bazu i kolekciju
            db = client.personal_site
            contacts_collection = db.contacts

            # Spremi kontakt u MongoDB
            result = contacts_collection.insert_one(contact_entry)

            # Zatvori konekciju
            client.close()

            # Odgovori klijentu
            response = {
                "success": True,
                "message": "Poruka uspješno primljena i spremljena!",
                "id": str(result.inserted_id),
            }

            self.wfile.write(json.dumps(response).encode("utf-8"))

        except ConnectionFailure:
            error_response = {
                "success": False,
                "message": "Greška pri povezivanju s bazom podataka.",
            }
            self.wfile.write(json.dumps(error_response).encode("utf-8"))
        except ValueError as e:
            error_response = {
                "success": False,
                "message": "Konfiguracija servera nije potpuna.",
            }
            self.wfile.write(json.dumps(error_response).encode("utf-8"))
        except Exception as e:
            error_response = {"success": False, "message": f"Greška: {str(e)}"}
            self.wfile.write(json.dumps(error_response).encode("utf-8"))

    def do_OPTIONS(self):
        # Podržava CORS preflight request
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()
