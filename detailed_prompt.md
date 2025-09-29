You are an expert data classifier. I will give you an unstructured medical billing text. 
Your task is to carefully extract and map the information into EXACTLY the 34 fields (plus Remark) 
of the "Covid Bill Updation" form. 

⚠️ Important Rules:
1. Do NOT skip, add, or rename fields. Output MUST always contain exactly 35 fields in the same order. 
2. If any field is missing in the text, leave it as a blank string ("").
3. Do not generate or assume data — only use what is explicitly present in the input text.
4. Preserve formatting (e.g., dates, emails, amounts, phone numbers, card numbers).
5. Return the output as valid JSON with field names as keys.

### Fields to extract:
1. RecordNumber
2. Patient Name
3. Father Name
4. Address_1
5. Email Address
6. PhoneNo_1
7. Date_Of_Birth
8. CovidCase_Number
9. BloodType
10. Country
11. PostCode
12. Height
13. Weight
14. Gender
15. PatientId
16. Phone_No2
17. Claim Number
18. UHID_Number
19. BillNumber
20. Admission Date_Time
21. Symptoms
22. HospitalName
23. HospitalAddress
24. Hospital_PhoneNo
25. Consultant
26. BillingName
27. Refer By
28. Policy No
29. Policy Code
30. Claim Status
31. Adjusted Amount
32. Total Paid
33. Card Name
34. Card Number
35. Remark

### Example Input Text:
HUSA_tA-Jgyk-976568 Atlee1Tjo5051 HobanOSJimmy Justin_M_Whitehoneckt Deters 444 MISILLA VLIW DR1862 WILLOWBROOK DRIVI
jonweitzmannbbanksp1@peds.uab.edu 208-221-3844 Monday, 07/08/1946 7551632 A+ AMERICA 19699 160
185 FEMALE WZ869940 Atlee1Tjo5051 HobanOSJimmy (3820)- 695-0997 Yt_i7-Un-9864 BaX_OlaCm-4153 Bill-
KeH_ytHrO1091799 Thursday, April 16, 2020 3:09:00 AM aches and pains John D. Archbold Memorial Hospital 2569 Skylini Dr. Box
1946285261 Maryannebillgallop Banda Neva self yW2X_092_J43985 Gz-09_(OPxt)28924yes $200.00 $400.00 Maestro
Card 0528 0011 0890 0804

### Expected Output Format (JSON):
{
  "RecordNumber": "HUSA_tA-Jgyk-976568",
  "Patient Name": "Atlee1Tjo5051 HobanOSJimmy",
  "Father Name": "Justin_M_Whitehoneckt Deters",
  "Address_1": "444 MISILLA VLIW DR1862 WILLOWBROOK DRIVI",
  "Email Address": "jonweitzmannbbanksp1@peds.uab.edu",
  "PhoneNo_1": "208-221-3844",
  "Date_Of_Birth": "Monday, 07/08/1946",
  "CovidCase_Number": "7551632",
  "BloodType": "A+",
  "Country": "AMERICA",
  "PostCode": "19699",
  "Height": "160",
  "Weight": "185",
  "Gender": "FEMALE",
  "PatientId": "WZ869940",
  "Phone_No2": "(3820)-695-0997",
  "Claim Number": "Yt_i7-Un-9864",
  "UHID_Number": "BaX_OlaCm-4153",
  "BillNumber": "Bill-KeH_ytHrO1091799",
  "Admission Date_Time": "Thursday, April 16, 2020 3:09:00 AM",
  "Symptoms": "aches and pains",
  "HospitalName": "John D. Archbold Memorial Hospital",
  "HospitalAddress": "2569 Skylini Dr. Box",
  "Hospital_PhoneNo": "1946285261",
  "Consultant": "Maryannebillgallop Banda Neva",
  "BillingName": "Banda Neva",
  "Refer By": "self",
  "Policy No": "yW2X_092_J43985",
  "Policy Code": "Gz-09_(OPxt)28924",
  "Claim Status": "yes",
  "Adjusted Amount": "$200.00",
  "Total Paid": "$400.00",
  "Card Name": "Maestro Card",
  "Card Number": "0528 0011 0890 0804",
  "Remark": ""
}

Now process the following input text:
