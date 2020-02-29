# HypeAPI

Modulo Python non ufficiale per interagire con l'API delle carte HYPE e TIM Pay.

Lo scopo di questo modulo è quello di accedere programmaticamente ai movimenti delle proprie carte e ad altre informazioni utili per integrare i dati con altri servizi. Ad esempio è possibile scrivere un semplice script che possa inserire i movimenti effettuati con le carte su [Firefly III](https://github.com/firefly-iii/firefly-iii) per automatizzare e agevolare la gestione delle finanze personali.

## Note

- HYPE consente di utilizzare un solo dispositivo per volta. Effettuando il login con questo modulo si verrà disconnessi dall'applicazione e viceversa. Questo non vale per TIM Pay.
- TIM Pay non richiede la verifica di un codice OTP via SMS.
- Con TIM Pay non è possibile rinnovare il token di accesso senza effettuare nuovamente il login con le proprie credenziali (vedi esempio). Questo significa che la password deve essere salvata da qualche parte per poter utilizzare il modulo in modalità non interattiva.

## Descrizione dei metodi disponibili

<table>
    <thead>
        <tr>
            <th>HYPE</th>
            <th>TIM Pay</th>
            <th>Descrizione</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><code>login(username, password, data_nascita=None)</code></td>
            <td><code>login(cellulare, username, password)</code></td>
            <td>Permette di effettuare il login con il proprio account</td>
        </tr>
        <tr>
            <td><code>otp2fa(codice_otp)</code></td>
            <td><i>Non supportato</i></td>
            <td>Permette di autenticarsi utilizzando il codice OTP ricevuto via SMS</td>
        </tr>
        <tr>
            <td><code>renew()</code></td>
            <td><i>Non supportato</i></td>
            <td>Permette di rinnovare il token di accesso</td>
        </tr>
        <tr>
            <td><code>get_movements(limit=5)</code></td>
            <td><code>get_movements(limit=10, offset=0)</code></td>
            <td>Permette di ottenere i movimenti della propria carta</td>
        </tr>
        <tr>
            <td colspan="2"><code>get_profile_info()</code></td>
            <td>Permette di ottenere informazioni sul proprio account</td>
        </tr>
        <tr>
            <td colspan="2"><code>get_balance()</code></td>
            <td>Permette di visualizzare il saldo della propria carta</td>
        </tr>
        <tr>
            <td colspan="2"><code>get_card_info()</code></td>
            <td>Permette di ottenere informazioni sulla propria carta</td>
        </tr>
    </tbody>
</table>

## Esempi di utilizzo

### HYPE

```python
import banking
from hype import Hype
from getpass import getpass  # For interactive password input

h = Hype()
h.login("user@example.com", getpass(), "1970-01-01")

# Wait for OTP code to arrive via SMS

h.otp2fa(123456)

# You are now logged in

try:
    h.get_card_info()
except banking.Banking.AuthenticationFailure:
    # Token has expired
    h.renew()
    h.get_card_info()
```

### TIM Pay

```python
import banking
from timpay import TimPay
from getpass import getpass  # For interactive password input

t = TimPay()
t.login("3331234567", "user@example.com", getpass())

# You are now logged in

try:
    t.get_card_info()
except banking.Banking.AuthenticationFailure:
    # Token has expired
    t.login("3331234567", "user@example.com", getpass())
    t.get_card_info()
```

## Disclaimer

I contenuti di questo repository sono a scopo informativo e frutto di ricerca personale. L'autore non è affiliato, associato, autorizzato, appoggiato da o in alcun modo legato con Banca Sella S.p.A., con TIM S.p.A. o con le società controllate da esse. Tutti i marchi registrati appartengono ai rispettivi proprietari.