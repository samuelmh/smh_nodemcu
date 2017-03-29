-- Class to print messages on a GM009605 128x64 screen
-- Table-based pattern


GM009605 = {}

function GM009605.new(pinSDA, pinSCL)
  local self = setmetatable({}, GM009605)
  i2c.setup(0, pinSDA, pinSCL, i2c.SLOW)
  self.disp = u8g.ssd1306_128x64_i2c(0x3c)
  return self
end

function GM009605:fit_msg(msg, char_pad, max_len)
  local len_msg = msg:len()
  if len_msg > max_len then -- Cut message
    return(msg:sub(0,max_len))
  else -- Pad message
    return(msg..string.rep(char_pad, max_len - len_msg))
  end
end

function GM009605:print_screen_txt(msg)
  -- Print a 126 character message.
  -- msg is truncated to 126 or padded with spaces
  local new_msg = self:fit_msg(msg,' ',126)
  self.disp:firstPage()
  self.disp:setFont(u8g.font_6x10)
  repeat
    for i=0, 5, 1 do
     self.disp:drawStr( 2, 8+(11*i), new_msg:sub(21*i+1,(21*(i+1))))
    end
  until self.disp:nextPage() == false
end

function GM009605:off()
  self.disp:sleepOn()
end

function GM009605:on()
  self.disp:sleepOff()
end


GM009605.__index = GM009605
setmetatable(GM009605, {
  __call = function (cls, pinSDA, pinSCL)
    return cls.new(pinSDA, pinSCL)
  end,
})
