--[[
AUTHOR: Samuel M.H. <samuel.mh@gmail.com>
DESCRIPTION: Lua script for NodeMCU.
  It connects the ESP8266 chip to an access point, takes the UTC time
  from a NTP server, set its internal clock and servers timestamps through a
  HTTP server.
]]

-- Edit this parameters
AP = "<AP_NAME>" --Name of the access point to connect
PASSWORD =  "<AP_PASSWORD>" --Password for the access point


-- WiFi events
function print_ip()
  print("Connected to the net.")
  print("Synchronizing internal time.")
  sntp.sync("hora.roa.es") --NTP server (Spanish time)
  addr, nm, gw = wifi.sta.getip()
  print("Visit http://"..addr..":80 to see the current UTC time.")
end

wifi.setmode(wifi.STATION)
wifi.sta.eventMonReg(wifi.STA_GOTIP, print_ip)
wifi.sta.eventMonReg(wifi.STA_IDLE, function() print("STATION_IDLE") end)
wifi.sta.eventMonReg(wifi.STA_CONNECTING, function() print("STATION_CONNECTING") end)
wifi.sta.eventMonReg(wifi.STA_WRONGPWD, function() print("STATION_WRONG_PASSWORD") end)
wifi.sta.eventMonReg(wifi.STA_APNOTFOUND, function() print("STATION_NO_AP_FOUND") end)
wifi.sta.eventMonReg(wifi.STA_FAIL, function() print("STATION_CONNECT_FAIL") end)


-- HTTP server
srv = net.createServer(net.TCP)
srv:listen(80, function(conn)
  conn:on("receive", function(sck, payload)
      print(payload)
      tm = rtctime.epoch2cal(rtctime.get())
      sck:send("HTTP/1.0 200 OK\r\nContent-Type: text/html\r\n\r\n<h1>UTC TIME: "..string.format("%04d/%02d/%02d %02d:%02d:%02d", tm["year"], tm["mon"], tm["day"], tm["hour"], tm["min"], tm["sec"]).."</h1>")
  end)
  conn:on("sent", function(sck) sck:close() end)
end)


-- Run
wifi.sta.eventMonStart()
wifi.sta.config(AP, PASSWORD)
