![By.Ouzrour](/logo.png)
# PowerMTA4 Watcher
![banner](/banner.png)

## Why PowerMTA4 Watcher ?
it Help You TO **CONSERVE** your sever from being **blacklisted** **_fastely_** , BY Alerting you when the 1 of the 2 **rates** ( or **both** )  is _less_ than the **minimum wanted**. 

By This Action , you gain not only the **_server Reputation_** , but also **_Money_** ( You don't need to buy a lot of servers ) and _**Time**_ ( you don't need to watch the process all the day ).

## How it work ?
![ScreenShot](/screenshot.png)
1. You **Choose** a **row**
2. You **Give** The **Name** to the server ( because ,in general cases; it isn't easy to remember the **details about the IP** ( the provider , the role of this server , some characteristics of this server ...)  . Specially if you have a **lot of servers** , so **giving name** can **help too much** !! )
3. you fill the IP/DNS box with the ip/dns of your server
4. you fill the Port box with the port of your server ( The Port is inevitable )
5. you fill the S/H(%) box with the minimum percentage to be reached. This percentage will be compared to the ratio: **OUT/IN x 100** whose values are taken from the line of **the last hour** _- as you can see in the image below -_ (this value can be for example **_90%_**: which means that the percentage of the message **actually sent** compared to **those you try to send** is **_90%_**). So all you have to do , is just to write the percentage you don't want to go below.

![Traffic_per_hour](/traffic_per_hour.png)
6. you fill the total(%) box with the minimum percentage to be reached. This percentage will be compared to the ratio: **OUT/IN x 100** whose values are taken from the line of **total** _- as you can see in the image below -_ (this value can be for example **_90%_**: which means that the percentage of the message **actually sent** compared to **those you try to send** is **_90%_**). So all you have to do , is just to write the percentage you don't want to go below.

![Traffic_total](/traffic_total.png)
7. you fill the Link box with **the link** that you want to be **redirected** to it **if 1 of the 2 tests _fails_** (the one of **S/H(%) _and/or_ total(%)**)
8. you fill the Refresh box with the **number of seconds** that you want to **wait** between **every check** . Note that , the _recommended value_ is **5** . **<!>** _ALERT_ : **_Below this value , you risk to have a high consumption of Memory / Cpu Ress . So be aware !_** ( if you let it empty , it gonna take **1s** between every check , because **the default value is : _1_** )
9. click "**START**" : To **Start The process** of watching
10. If you want to **stop the process** at any time , click "**STOP**" .
11. Click "**RESET**" to stop the process and to delete all the content of all the textboxes in the row .
## Steps to use it ?
1. install all dependencies : _( do it just 1 time , if already done it , go to Step 2 )_
```cmd
pip install -r requirements.txt
```
2. Do All Steps in **How it work ?** ( above )
3. ENJOY !

## For Windows User ( How to Deploy )

1. install pyinstaller
```cmd
pip install pyinstaller
```
2. Open The file "main.spec" and change the path "E:\\mailing\\3. PMTA Watcher\\" to the absolute path where the application is !
3. run cmd in the same folder as the project ( where application.py exist ) and run :
```cmd
pyinstaller main.spec
```
4. Go to the folder /dist and run .exe
5. Enjoy !