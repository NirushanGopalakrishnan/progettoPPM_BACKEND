# 🛍 E-commerce Backend - Progetto PPM

Backend REST API per un sito e-commerce generico, sviluppato con *Django REST Framework*.  
Progetto universitario per il corso di *Progettazione e Programmazione del Software (PPM)*.  
Collegato a un frontend HTML/JavaScript minimale per la simulazione delle operazioni utente.

---

## 🚀 Funzionalità principali

- ✅ Registrazione, login e logout con autenticazione tramite token (JWT)
- 🛒 Visualizzazione prodotti (con sconti e disponibilità)
- 🧺 Carrello: aggiunta, rimozione e modifica quantità dei prodotti
- 📦 Checkout con aggiornamento dello stock (simulato)
- 🧑‍💼 Gestione utenti tramite gruppi e permessi
- 🔐 Ruoli con accessi differenziati
- ⚙ Admin panel disponibile all’indirizzo /admin
- 🌐 Database PostgreSQL (tramite Supabase)
- ☁ Deploy serverless su [Vercel](https://vercel.com/)

---

## 🧩 Tecnologie utilizzate

- Python 3.13
- Django 5.x
- Django REST Framework
- PostgreSQL (tramite Supabase)
- Vercel (deploy backend)
- GitHub Actions (CI/CD)
- HTML + JavaScript (frontend minimale)

---

## 👥 Tipi di utenti e permessi

| Ruolo               | Permessi principali                                                                 | Gruppo associato           |
|---------------------|--------------------------------------------------------------------------------------|----------------------------|
| 🧑‍💻 *Cliente*        | Registrazione, login, visualizza prodotti, aggiunge al carrello, checkout         | user                     |
| 🛠 *Moderatore*     | Tutti i permessi del cliente + visualizza e gestisce ordini e utenti (ban/unban)  | user, moderator        |
| 📦 *Product Manager*| Tutti i permessi del cliente + CRUD sui prodotti                                   | user, product_manager  |
| 👑 *Superuser*      | Accesso completo a tutto tramite Django Admin                                      | nessun gruppo necessario |

---

## 🔐 Credenziali di test

| Ruolo             | Username        | Password          |
|------------------|------------------|--------------------|
| Cliente           | client         | client           |
| Moderatore        | modera_Thor    | modera_Thor      |
| Product Manager   | product_manager| product_manager  |
| Superuser (admin) | admin          | admin            |

---

## 🌐 Endpoint principali

| Metodo | Endpoint                        | Descrizione                              |
|--------|----------------------------------|------------------------------------------|
| POST   | /api/users/register/          | Registrazione nuovo utente               |
| POST   | /api/users/login/             | Login e ottenimento token                |
| GET    | /api/products/                | Visualizza lista prodotti                |
| POST   | /api/orders/cart/items/       | Aggiunge un prodotto al carrello         |
| GET    | /api/orders/cart/             | Visualizza carrello attivo               |
| POST   | /api/orders/checkout/         | Checkout ordine e riduzione dello stock  |

⚠ Gli endpoint /orders/ e /products/ richiedono autenticazione tramite token.

---

## 🔒 Funzionalità riservate allo staff

| Azione                                 | Gruppo necessario        |
|----------------------------------------|--------------------------|
| Aggiunta/rimozione/modifica Utente     | moderator, superuser |
| Aggiunta/rimozione/modifica Prodotto   | product_manager        |
| Aggiunta/rimozione/modifica Ordine     | moderator, superuser |
| Ban/unban utenti                       | moderator, superuser |
| Gestione permessi e gruppi             | superuser              |

---

## 🛠 Deployment & Database

### Database

Il database è gestito su [Supabase](https://supabase.com/) e utilizza *PostgreSQL*.  
Tutte le configurazioni sensibili (es. DATABASE_URL, SECRET_KEY, credenziali) sono incluse nel file .env.

### Deploy

L'app Django è deployata su [Vercel](https://vercel.com/) con aggiornamento automatico su ogni push.  
🔗 URL pubblico: https://progetto-ppm-backend2.vercel.app/  
🔐 Admin: https://progetto-ppm-backend2.vercel.app/admin/

> ℹ Il deploy su Vercel e Supabase potrebbe risultare lento in alcuni momenti. Si consiglia di evitare richieste multiple simultanee.

---

## 📁 Struttura del progetto
