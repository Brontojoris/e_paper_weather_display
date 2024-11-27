<h1>E-paper Weather Display</h1>
<p>Original source from <a href="https://github.com/AbnormalDistributions/e_paper_weather_display/">github.com/AbnormalDistributions/e_paper_weather_display</a></p>
<p>
  Raspberry Pi weather display using Waveshare e-paper 7.5 inch display, Open Weather Map API, and Python.</p>

<img src="/photos/photo2.jpg" width=40% height=40%>
<img src="/photos/photo1.jpg" width=40% height=40%> <br>

<p>If you like what you see, consider <a href="https://ko-fi.com/abnormaldistributions">buying James a coffee</a>.

<h1>Versions</h1>
  <h2>Version 1.0</h2>
    <ul>
	  <li>Initial Commit.</li>
	</ul>
  <h2>Version 1.1</h2>
    <ul>
      <li>Switched to more legible icons.</li>
    </ul>
  <h2>Version 1.2</h2>
    <ul>
      <li>Added support for connection errors.</li>
      <li>Added support for HTTP errors.</li>
      <li>Added "dispay_error" fuction to display respective errors if present.</li>
    </ul>
  <h2>Version 1.3</h2>
    <ul>
      <li>Added option to store retreived weather data in CSV file.</li>
    </ul>
  <h2>Version 1.4</h2>
    <ul>
      <li>Updated to use all 480 vertical pixels instead of just 450.</li>
    </ul>
  <h2>Version 1.5</h2>
    <ul>
      <li>Fixed error where "TAKEOUT TRASH TODAY!" was writing in incorrect font size.</li>
    </ul>
  <h2>Version 1.6</h2>
    <ul>
      <li>Increased size of fonts for "Humidity" and "Wind" for better legibility.</li>
    </ul>
  <h2>Version 1.7</h2>
    <ul>
      <li>Added clear screen function to reduce possibility of burn-in.</li>
      <li>Changed refresh time from 300 to 600 seconds.</li>
    </ul>
  <h2>Version 1.8</h2>
  <p>Forked from <a href="https://github.com/AbnormalDistributions/e_paper_weather_display">AbnormalDistributions/e_paper_weather_display</a></p>
    <ul>
      <li>Added .env file and loader</li>
      <li>Changed display to <a  href="https://www.waveshare.com/wiki/7.3inch_e-Paper_HAT_(G)_Manual">7.3inch 4 colour e-Paper HAT</a></li>
    </ul>


<h1>Setup</h1>
  <ol type="1">
    <li>The first thing you need is a free API key from https://home.openweathermap.org/users/sign_up.</li>
    <li>Open 'weather.py' and replace **Key Here** with your API key.</li>
    <li>**Location** can be left as it is unless you want to add it to your display.</li>
    <li>Get your **longitude** and **lattitude** using I used https://www.latlong.net and put that in as well.</li>
    <li>Set CSV_OPTION to False if you would not like weather data appended to 'records.csv' after every refresh.</li>
    <li>There is also a reminder for taking out the trash near the end of the script that you will want to change if your trash pickup doesn't come on Monday and Thursday like mine. :)</li>
  </ol>
<br>
That's about it. Run the python file and you should see output on the display.

# Note
If you are not using a 7.5 inch Version 2 display, you will want to replace 'epd7in5_V2.py' in the 'lib' folder with whichever one you have from https://github.com/waveshare/e-Paper/tree/master/RaspberryPi_JetsonNano/python/lib/waveshare_epd<br>
Fairly extensive adjustments will have to be made for other sized screens.

# Parts
<ul>
  <li><strike>https://www.waveshare.com/wiki/7.5inch_e-Paper_HAT</strike></li>
  <li><a href="https://www.waveshare.com/product/raspberry-pi/displays/e-paper/7.3inch-e-paper-hat-g.htm">7.3inch e-Paper HAT (G), 800 × 480, Red/Yellow/Black/White</a></li>
  <li><strike>Raspberry Pi 3, but this will run on any of them except the Pi Zero that doesn't have soldered headers.</strike></li>
  <li>Raspberry Pi Zero 2 WH</li>
  <li>SD card for the Pi at least 8 GB.</li>
  <li>Power supply for the Pi.</li>
  <li><a href="https://www.officeworks.com.au/shop/officeworks/p/promenade-5x7-frame-oak-ur20623">5 x 7 inch photo frame from Officeworks</a></li>
</ul>

<h1>Credit</h1>
  Original source by [James Steele Howard] (https://github.com/AbnormalDistributions/e_paper_weather_display)
  Icon designs are originally by [Erik Flowers] (https://erikflowers.github.io/weather-icons/). Some icons have been modified.

<h1>Licensing</h1>
  <ul>
    <li>Weather Icons licensed under [SIL OFL 1.1](http://scripts.sil.org/OFL)</li>
    <li>Code licensed under [MIT License](http://opensource.org/licenses/mit-license.html)</li>
    <li>Documentation licensed under [CC BY 3.0](http://creativecommons.org/licenses/by/3.0)</li>
  <ul>
