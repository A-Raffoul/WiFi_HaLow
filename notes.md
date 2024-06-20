# WiFi HaLow 

Few notes that could usefull for future research

Main issue:  we were unable to get the latest version of the NRC_pkg, the oneline command script for the alfa website is not working properly, 
https://docs.alfa.com.tw/Product/AHPI7292S/20_Getting_Started_New/

After many days if trial and debugging the issue seems to be from the public key of the alfa website. 

Err:5 https://downloads.alfa.com.tw/raspbian bullseye InRelease
The following signatures were invalid: EXPKEYSIG EF8954B081D0A5A6 ALFA Network Inc. (noreply) noreply@alfa.com.tw

I tried contacting the ALFA network support without any success.

French paper authors were able to get the latest software
https://www.sciencedirect.com/science/article/pii/S2542660523002809/pdfft?crasolve=1&r=896c80ac7d693b5d&ts=1718894307357&rtype=https&vrr=UKN&redir=UKN&redir_fr=UKN&redir_arc=UKN&vhash=UKN&host=d3d3LnNjaWVuY2VkaXJlY3QuY29t&tsoh=d3d3LnNjaWVuY2VkaXJlY3QuY29t&rh=d3d3LnNjaWVuY2VkaXJlY3QuY29t&re=X2JsYW5rXw%3D%3D&ns_h=d3d3LnNjaWVuY2VkaXJlY3QuY29t&ns_e=X2JsYW5rXw%3D%3D&rh_fd=rrr)n%5Ed%60i%5E%60_dm%60%5Eo)%5Ejh&tsoh_fd=rrr)n%5Ed%60i%5E%60_dm%60%5Eo)%5Ejh&iv=5f35b6fc5f166cce6e98eb0fb0074327&token=62323631353235313864653437386333636232346235306634653633623361633038346565393635356136626536303832343638363933313439333266333836333532646631633965303361383764353133643761396136356565346263643262666137336339623a656132366161323032366465383462643838623162376335&text=2fb2c50b4734aebbac754db4c451894270e16ccefe73467dacc47eefc29e3e96ec28401b7c53627feaf720c9a2e4afebce2ac52c7c0cd71d769758b30deb186669fa9b71ad061833fb6e51f30f44a4f683d4b9184ee0585e140cacadcb1a1d02514bc2e02387ad9f10a515e3c58d8f33164c07cda8651ca078bed8df13457c6bc33460025f5c2cba07ead8da3a7ffc5d6d453d54f3dc7a2424310c323a3993cd588c849104247dd9f35169fe5cb7aa3c2847a8827bf7dcc3e2b6bb1553b5fe540165e8a6ca0dec75b74f6bfd697653b27245d0e2e3f839e2aa10d2117984741b401f6359f1f48f0554036abc2da35f270a65dfe238d516a615159768e310358baf1b9431d76fff8d107e45f4671d88ed8cfc0346b34a3d59eb3c574c13012bde90cca5fdcc9d93e17b838ac0f055b357&original=3f6d64353d6639336266633539613038663736633639333134623538616131353032343737267069643d312d73322e302d53323534323636303532333030323830392d6d61696e2e706466

We used the prebuilt image from the alfa website using the 2022 version of the NRC_pkg


when setting up make sure that the toggle of the ALFA HAT is at Host mode, other modes will not work as each mode has it's own package or sdk

