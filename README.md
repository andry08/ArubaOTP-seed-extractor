>This project is useful only to Italian people, but feel free to take a look if you want.  
>Why am I writing this in english? I don't know.
# ArubaOTP seed extractor
[Aruba](https://aruba.it/) is an Italian service provider (not to be confused with Aruba Networks) which provides numerous services.
One of these services is [SPID](https://it.wikipedia.org/wiki/SPID), the Italian version of [eIDAS](https://en.wikipedia.org/wiki/EIDAS),
and its level 2 requires 2FA to be enabled.  
Aruba implements this with it's own app, called [ArubaOTP](https://play.google.com/store/apps/details?id=it.aruba.pec.mobile.otp) which under the hood is just
an implementation of TOTP, but the secret key never gets exposed to the user (the app pairs with an unique identifier, which is just a long number).

## So, why this?
This little script allows for the extraction of this TOTP key, so it can be used in another authenticator app.  
>**NOTE** however that some apps don't support the HMAC-SHA256 algorithm for TOTP generation, take a look at [this article](https://labanskoller.se/blog/2019/07/11/many-common-mobile-authenticator-apps-accept-qr-codes-for-modes-they-dont-support/) for example (it's a bit old, however).

- Google Authenticator sadly doesn't even implement support for a custom number of digits (8 are needed for this purpose)
- Authy doesn't support the sha256 algorithm, but it doesn't explicitly mention it. Reading the qr code with this will lead to a successful import, but a wrong code to be generated.

There is a script in this repo, in which you can paste the seed, to check the validity of the otp code from your app, or simply to validate the code the first time.
If you need an hint, I found and use [Aegis Authenticator](https://play.google.com/store/apps/details?id=com.beemdevelopment.aegis), pretty cool and open source too.

# Usage
1. After cloning the repo run the command `pip install -r requirements.txt`
2. Open the Aruba website and start the pairing, ignoring the ArubaOTP step
3. When the QR code appears copy the code on the right (without spaces)
4. Run the command `python ./scripts/main.py extract <validation_code>`, add `-q` flag if you need the QR representation
5. Run the command `python ./scripts/main.py generate` to get the current OTP code

# WARNING
Always make a backup of your seed, without it you could lose access to your aruba account!  
I don't take responsibility from any damage caused by this script.  
This project was made only for educational purposes