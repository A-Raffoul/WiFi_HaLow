# WiFi HaLow 

Few notes that could usefull for future research

Main issue:  we were unable to get the latest version of the NRC_pkg, the oneline command script for the alfa website is not working properly, 
https://docs.alfa.com.tw/Product/AHPI7292S/20_Getting_Started_New/

After many days if trial and debugging the issue seems to be from the public key of the alfa website. 

Err:5 https://downloads.alfa.com.tw/raspbian bullseye InRelease
The following signatures were invalid: EXPKEYSIG EF8954B081D0A5A6 ALFA Network Inc. (noreply) noreply@alfa.com.tw

I tried contacting the ALFA network support without any success.

French paper authors were able to get the latest software
(https://www.sciencedirect.com/science/article/pii/S2542660523002809)

We used the prebuilt image from the alfa website using the 2022 version of the NRC_pkg


when setting up make sure that the toggle of the ALFA HAT is at Host mode, other modes will not work as each mode has it's own package or sdk




