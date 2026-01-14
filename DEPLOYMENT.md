# Vercel Deployment - Serverless Contact Form s MongoDB Atlas

## Što je kreirano:

### 1. **api/contact.py** - Python serverless funkcija
- Prima POST zahtjeve s podacima iz kontakt forme
- Sprema kontakte u MongoDB Atlas (trajna cloud baza)
- Podržava CORS za frontend komunikaciju
- Error handling za konekcijske probleme

### 2. **vercel.json** - Konfiguracija za Vercel
- Postavlja Python 3.9 runtime za API funkcije

### 3. **requirements.txt** - Python paketi
- `pymongo[srv]>=4.6.0` - MongoDB driver za Python

### 4. Ažuriran **index.html**
- Kontakt forma s JavaScript fetch API-jem
- Prikazuje success/error poruke

### 5. Ažuriran **style.css**
- Stilovi za `.form-message`, `.form-message.success` i `.form-message.error`

### 6. **.env.example** - Primjer environment varijabli
- Template za MongoDB connection string

## MongoDB Atlas Setup (BESPLATNO):

### 1. Kreirajte MongoDB Atlas Account:
   - Idite na https://www.mongodb.com/cloud/atlas
   - Kliknite "Try Free"
   - Registrirajte se (možete koristiti Google account)

### 2. Kreirajte Cluster (M0 - besplatno):
   - Odaberite **M0 Sandbox** (besplatan forever)
   - Odaberite regiju (npr. eu-central-1 Frankfurt)
   - Cluster Name: npr. `personal-site-cluster`
   - Kliknite "Create Cluster"

### 3. Kreirajte Database Usera:
   - Idite na **Database Access** (lijeva stranica)
   - Kliknite "Add New Database User"
   - Authentication Method: **Password**
   - Username: npr. `admin`
   - Password: generirajte jak password ili napišite svoj
   - Database User Privileges: **Read and write to any database**
   - Kliknite "Add User"

### 4. Dozvolite Network Access:
   - Idite na **Network Access** (lijeva stranica)
   - Kliknite "Add IP Address"
   - Kliknite "Allow Access From Anywhere" (0.0.0.0/0) - potrebno za Vercel
   - Kliknite "Confirm"

### 5. Preuzmite Connection String:
   - Idite na **Database** → **Connect**
   - Odaberite "Connect your application"
   - Driver: **Python**, Version: **3.12 or later**
   - Kopirajte connection string:
     ```
     mongodb+srv://<username>:<password>@cluster.mongodb.net/?retryWrites=true&w=majority
     ```
   - Zamijenite `<username>` i `<password>` s vašim podacima

## Kako deployati na Vercel:

### 1. Instalirajte Vercel CLI (ako već nije instalirano):
   ```bash
   npm install -g vercel
   ```

### 2. Login u Vercel:
   ```bash
   vercel login
   ```

### 3. Dodajte MongoDB URI kao Environment Variable u Vercel:
   
   **Opcija A - Kroz CLI:**
   ```bash
   vercel env add MONGODB_URI
   ```
   Zatim unesite connection string kada vas pita.

   **Opcija B - Kroz Vercel Dashboard:**
   - Idite na https://vercel.com/dashboard
   - Odaberite projekt
   - Settings → Environment Variables
   - Dodajte:
     - Name: `MONGODB_URI`
     - Value: `mongodb+srv://username:password@cluster.mongodb.net/?retryWrites=true&w=majority`
     - Environment: **Production**, **Preview**, i **Development**

### 4. Deploy projekta:
   ```bash
   # Prvi deploy (postavlja projekt)
   vercel

   # Produkcijski deploy
   vercel --prod
   ```

## Testiranje lokalno:

### 1. Kreirajte `.env` datoteku (lokalno):
   ```bash
   cp .env.example .env
   ```

### 2. Uredite `.env` i dodajte pravi MongoDB connection string:
   ```
   MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/?retryWrites=true&w=majority
   ```

### 3. Pokrenite Vercel dev server:
   ```bash
   vercel dev
   ```

### 4. Otvorite browser:
   ```
   http://localhost:3000
   ```

## Struktura MongoDB Baze:

- **Database**: `personal_site`
- **Collection**: `contacts`
- **Document struktura**:
  ```json
  {
    "_id": "ObjectId(...)",
    "name": "Ime Prezime",
    "email": "email@example.com",
    "message": "Tekst poruke...",
    "timestamp": "2026-01-14T12:00:00.000000",
    "ip": "123.456.789.0"
  }
  ```

## Pregled kontakata u MongoDB Atlas:

1. Idite na **Database** → **Browse Collections**
2. Odaberite `personal_site` → `contacts`
3. Vidjet ćete sve primljene poruke

## Napomene:

✅ **Besplatni MongoDB Atlas plan** - 512 MB storage, dovoljno za tisuće kontakata
✅ **Trajna pohrana** - podaci ostaju spremljeni zauvijek
✅ **Automatsko skaliranje** - možete nadograditi na veći plan po potrebi
✅ **Backup** - MongoDB Atlas automatski pravi backupe

## Troubleshooting:

**Problem**: "MONGODB_URI environment variable nije postavljena"
- **Rješenje**: Dodajte `MONGODB_URI` u Vercel environment variables

**Problem**: Timeout ili connection error
- **Rješenje**: Provjerite je li 0.0.0.0/0 dozvoljen u Network Access na MongoDB Atlas

**Problem**: Authentication failed
- **Rješenje**: Provjerite username i password u connection stringu
