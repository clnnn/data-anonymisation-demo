text_examples = {
    "Medical Record": """
Patient John Doe, born in 10/10/1980 was admitted to the hospital on 2021-09-01. He presented with a fever of 102°F and a cough. We performed a chest X-ray and found signs of pneumonia. 
We diagnosed him with COVID-19 and started treatment with remdesivir. He was discharged on 2021-09-10 and advised to self-isolate for 14 days. 
His insurance ID is 123456789 and his SSN is 123456789.""",
    "Medical Record (Dutch)": """
Patiënt John Doe, geboren op 10/10/1980, werd op 2021-09-01 opgenomen in het ziekenhuis. 
Hij vertoonde een koorts van 39°C en een hoest. We hebben een borst X-ray uitgevoerd en tekenen van longontsteking gevonden. 
We hebben hem gediagnosticeerd met COVID-19 en zijn behandeling gestart met remdesivir. 
Hij werd ontslagen op 2021-09-10 en geadviseerd om zichzelf gedurende 14 dagen te isoleren. 
Zijn verzekeringsnummer is 123456789 en zijn SSN is 123456789.""",
    "Email": """
Hi John,

I hope you're doing well. I hope you liked the presentation and the demo I showed you about PII Analyzer and Anonymizer.
If you have any questions, please contact me at voicu.moldovan@tss-yonder.com
        
Best regards,
Voicu M.
voicu.moldovan@tss-yonder.com
Delivery Manager at Yonder
    """,
    "Transaction": """
Transaction ID: 10
Amount: $500.00
Card Number: 5425-2334-3010-9903
Expiry Date: 12/25
    """,
    "Personal Information": """
Hello, my name is David Johnson and I live in Maine. 
My credit card number is 4095-2609-9393-4932 and my crypto wallet id is 16Yeky6GMjeNkAiNcBY7ZhrLoMSgg1BoyZ.
On September 18 I visited microsoft.com and sent an email to test@presidio.site,  from the IP 192.168.0.1.
My passport: 191280342 and my phone number: (212) 555-1234.
This is a valid International Bank Account Number: IL150120690000003111111 . Can you please check the status on bank account 954567876544?
Kate's social security number is 078-05-1126.  Her driver license? it is 1234567A.
    """,
    "Personal Information (Dutch)": """
Hallo, mijn naam is David Johnson en ik woon in Maine. 
Mijn creditcardnummer is 4095-2609-9393-4932 en mijn cryptoportefeuille-ID is 16Yeky6GMjeNkAiNcBY7ZhrLoMSgg1BoyZ.
Op 18 september bezocht ik microsoft.com en stuurde een e-mail naar test@presidio.site, vanaf het IP-adres 192.168.0.1.
Mijn paspoortnummer is 191280342 en mijn telefoonnummer is (212) 555-1234. Dit is een geldig Internationaal Bankrekeningnummer: IL150120690000003111111. 
Kunt u alstublieft de status controleren van bankrekening 954567876544? Het socialezekerheidsnummer van Kate is 078-05-1126. Haar rijbewijs? Het is 1234567A.
    """,
}
