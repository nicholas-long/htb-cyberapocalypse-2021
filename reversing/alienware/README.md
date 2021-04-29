This challenge was kind of like reverse engineering some ransomware.

The exe decodes creates a DLL, which I have saved for convenience and analysis.

This DLL encrypts files in the Docs folder.

I have reverse engineered the function to generate the encryption key in order to create a decryption program (and get the flag out of the pdf)
