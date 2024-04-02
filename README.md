# OllamaSMS
Ollama Project to allow AI interactions in native messaging apps

How to use:
1. Install the requirements. Im not fancy so no requirements.txt Im sorry.
2. Replace {email} and {password} with the login info for your gmail account (See notes!)
3. Set your email list. Edit the portion of the code with {phone1} and {phone2} to include your own list. (See notes at the bottom)
4. Change the client address if you so choose
5. Ensure you have pulled the model you have set in the Ollama Part. (Default is llama2)
6. run ``` python ollamasms.py ```
7. Send a text/ email to the email address you have set
8. A response should generate and reply back.

# NOTES
> You MUST use an app password for the email password. This means enabling 2fa and generating a separate pw.
> 
> This project was designed to allow use from phone messaging apps as well as email
> 
> In order to "whitelist" phones you must use the MMS address (you may need to look this up). Verizon example: 1234567891@vzwpix.com (MMS) 1234567891@vtext.com (SMS)
> 
> In order to "whitelist" emails that have names attached they must be formatted like so: "Bob Duncan {emailaddress}"
> 
> This goes through ALL unread emails and reads them but only processes the ones that are in the list. Keep that in mind.
> 
> I super extra highly recommend creating a new gmail account for this
> 
> For any issues please DM me on discord @ fatphrog and I will try to help you. Otherwise open an issue on Github
