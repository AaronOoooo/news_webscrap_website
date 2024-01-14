# news_webscrap_website

To set up the LCD, refer to these pages: 
https://wiki.52pi.com/index.php?title=Z-0234

https://www.amazon.com/gp/product/B07S7PJYM6/ref=ppx_yo_dt_b_search_asin_title?ie=UTF8&psc=1


pi@Thunder:~ $ i2cdetect -y 1
     0  1  2  3  4  5  6  7  8  9  a  b  c  d  e  f
00:                         -- -- -- -- -- -- -- -- 
10: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
20: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
30: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 3f 
40: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
50: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
60: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
70: -- -- -- -- -- -- -- --   

The address of the LCD running on hostname Thunder at 192.168.50.95 is 3f, as shown in the table above when i2cdetect -y 1 is executed in termimal.