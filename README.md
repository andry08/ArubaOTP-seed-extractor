>This project is useful only to Italian people, but feel free to take a look if you want.  
# ArubaOTP seed extractor
[Aruba](https://aruba.it/) è uno dei fornitori di [SPID](https://it.wikipedia.org/wiki/SPID) in Italia, il cui livello 2, necessario per accedere a molti dei servizi
che offrono questo metodo di login, richiede l'attivazione dell'autenticazione 2FA.
Aruba la implementa con la sua app ([ArubaOTP](https://play.google.com/store/apps/details?id=it.aruba.pec.mobile.otp)) che al suo interno utilizza
un 'implementazione standard di TOTP, ma il seed (la chiave segreta per effettuare la generazione) non viene mai esposta direttamente all'utente,
visto che l'associazione in app avviene attraverso un qr code, che contiene solamente un numero, che viene scambiato con il server al fine di ottenere
il seed vero e proprio.

## Perchè
Questo piccolo script permette l'estrazione del seed TOTP, in modo da poterlo utilizzare in un'altra app (magari quella che usi normalmente per il 2FA),
ed evitare di installare un'altra app inutile nel telefono.

Oltre che per la 2FA relativa allo SPID, l'estrazione del seed TOTP funziona anche per la 2FA relativa alla firma digitale remota di Aruba.

>**NOTA BENE** Alcune app non supportano l'algoritmo `HMAC-SHA256` per il TOTP.
>- Google Authenticator supporta solamente codici a 6 cifre (inoltre su android non supporta l'algorimo specificato, mentre su apple si)
>- Authy non supporta l'algoritmo, ma non fornisce alcun avvertimento a riguardo. Leggendo il qr non darà errore, ma fornirà codici sbagliati.

Se volete un suggerimento, io ho trovato ed utilizzo tuttora [Aegis Authenticator](https://play.google.com/store/apps/details?id=com.beemdevelopment.aegis)

# Utilizzo

## Prerequisito
Installa [uv](https://docs.astral.sh/uv/): è l'unica cosa che ti serve, perché gestisce in automatico sia Python che le dipendenze.
Poi clona la repo (con il comando `git clone`, oppure scaricala come zip dal pulsante in alto a destra).

## Procedura
1. Apri il sito di Aruba, inizia il processo per associare l'app, e ignora il passo in cui ti chiede di installare l'app sul telefono
2. Adesso che ti trovi nella pagina con il QR code, copia il numero presente sotto il QR, facendo attenzione a rimuovere eventuali spazi prima e dopo
   >**Non scansionare il QR con l'app aruba, altrimenti lo script non potrà fare il suo lavoro**
3. Da un terminale nella cartella del progetto esegui:
   ```sh
   ./launch.sh extract <validation_code> -q
   ```
   Al primo avvio uv crea un ambiente isolato e installa le dipendenze in automatico; il seed verrà stampato a schermo in caso di successo.
4. Scansiona il codice con l'app di tua scelta e inserisci il codice sul sito aruba per confermare l'associazione

> In alternativa puoi usare `./launch.sh generate` per ottenere il codice per l'associazione, ed il comando `./launch.sh printqr` in un secondo momento per generare il qr per salvare il codice sul telefono

## Compatibilità (pip)
Se preferisci non usare uv, puoi ancora installare le dipendenze con pip (serve Python 3.6 o superiore installato manualmente):
```sh
pip install -r requirements.txt
python ./scripts/main.py extract <validation_code> -q
```
I comandi `generate` e `printqr` funzionano allo stesso modo, sostituendo `./launch.sh` con `python ./scripts/main.py`.

# ATTENZIONE
Ricorda di fare un backup del seed, altrimenti rischi di rimanere chiuso fuori dal tuo account! (Ovvio ci sono le procedure di recupero ma comunque...)

**Non mi assumo alcuna responsabilità per danni derivanti dall'uso di questo script.**
