// decryptstuff.cpp : This file contains the 'main' function. Program execution begins and ends there.
//

#include "pch.h"
#include <iostream>



int main()
{
	char passed_in_data[] = "\x2F\x6B\x18\xE4\x9A\x33\xD9\xC7\xA0\x31\x46\x1F\x16\x66\x19\xF7\x00\x00\x04\xFF\x00\x00\x00\x00";

	wchar_t dest[100];
	ZeroMemory(dest, 100);
	mbstowcs(dest, passed_in_data, 16);

	wchar_t szProvider[] = L"Microsoft Enhanced RSA and AES Cryptographic Provider";

	HCRYPTPROV phProv; // [rsp+48h] [rbp-B8h]
	DWORD NumberOfBytesWritten; // [rsp+50h] [rbp-B0h]
	DWORD NumberOfBytesRead; // [rsp+50h] [rbp-B0h]

	HCRYPTHASH phHash; // [rsp+58h] [rbp-A8h]
	HCRYPTKEY phKey; // [rsp+60h] [rbp-A0h]

	if (!CryptAcquireContextW(&phProv, 0i64, szProvider, 0x18u, 0xF0000000))
		exit(1);
	if (!CryptCreateHash(phProv, 0x800Cu, 0i64, 0, &phHash)) // sha256
		exit(2);

	int v5 = lstrlenW(dest);

	if (!CryptHashData(phHash, (const BYTE *)dest, v5, 0))
	{
		std::cout << std::hex << GetLastError() << std::endl;
		exit(3);
	}

	if (!CryptDeriveKey(phProv, 0x660Eu, phHash, 0, &phKey))
		exit(4);

	LPCWSTR lpFileName = L"C:\\Users\\nicho\\Desktop\\ctf\\Confidential2.alien";
	LPCWSTR lpOutFileName = L"C:\\Users\\nicho\\Desktop\\ctf\\Confidential2.pdf";

	HANDLE v6 = CreateFileW(lpFileName, 0x80000000, 1u, 0i64, 3u, 0x8000000u, 0i64);

	HANDLE v7 = CreateFileW(lpOutFileName, 0x40000000u, 0, 0i64, 2u, 0x80u, 0i64);

	DWORD i = GetFileSize(v6, 0i64);

	char buffer[0x100];
	BOOL final = FALSE;

	while (!final)
	{
		ZeroMemory(buffer, 0x100);

		ReadFile(v6, &buffer, 0x30u, &NumberOfBytesRead, 0i64);
		//if (!CryptDecrypt(phKey, 0i64, v10, 0, (BYTE *)&buffer, &NumberOfBytesRead, 0x30u))
		final = NumberOfBytesRead < 0x30 ? TRUE : FALSE;
		if (NumberOfBytesRead > 0)
		{
			if (!CryptDecrypt(phKey, 0/*phHash*/, final, 0, (BYTE *)&buffer, &NumberOfBytesRead))
			{
				std::cout << std::hex << GetLastError() << std::endl;
				//8009000c = NTE_BAD_HASH_STATE
				//80090004 = NTE_BAD_LEN
				exit(5);
			}

			if (!WriteFile(v7, &buffer, NumberOfBytesRead, &NumberOfBytesWritten, 0i64))
				exit(6);
		}
	}

	CryptReleaseContext(phProv, 0);
	CryptDestroyKey(phKey);
	CryptDestroyHash(phHash);
	CloseHandle(v6);
	CloseHandle(v7);

}

// Run program: Ctrl + F5 or Debug > Start Without Debugging menu
// Debug program: F5 or Debug > Start Debugging menu

// Tips for Getting Started: 
//   1. Use the Solution Explorer window to add/manage files
//   2. Use the Team Explorer window to connect to source control
//   3. Use the Output window to see build output and other messages
//   4. Use the Error List window to view errors
//   5. Go to Project > Add New Item to create new code files, or Project > Add Existing Item to add existing code files to the project
//   6. In the future, to open this project again, go to File > Open > Project and select the .sln file
