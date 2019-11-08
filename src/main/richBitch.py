import requests
from bs4 import BeautifulSoup
import os
base ="https://www.xiaohongshu.com/discovery/item/"
url ="5dc3859c00000000010097c5"
header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36",
    "Connection": "keep-alive",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.8",
    "cookie": "xhsTrackerId=99966177-73ac-4d2d-cde1-3c4311835464; xhsTracker=url=/discovery/item/59832f83d1d3b92ac89ace3c&xhsshare=CopyLink; extra_exp_ids=; rookie=yes; timestamp1=3914713226; timestamp2=3768899945; hasaki=%5B%22Mozilla%2F5.0%20(Windows%20NT%2010.0%3B%20WOW64)%20AppleWebKit%2F537.36%20(KHTML%2C%20like%20Gecko)%20Chrome%2F70.0.3538.25%20Safari%2F537.36%20Core%2F1.70.3732.400%20QQBrowser%2F10.5.3819.400%22%2C%22zh-CN%22%2C24%2C-480%2Ctrue%2Ctrue%2Ctrue%2C%22undefined%22%2C%22function%22%2Cnull%2C%22Win32%22%2C6%2C8%2Cnull%2C%22Chromium%20PDF%20Plugin%3A%3APortable%20Document%20Format%3A%3Aapplication%2Fx-google-chrome-pdf~pdf%3BChromium%20PDF%20Viewer%3A%3A%3A%3Aapplication%2Fpdf~pdf%3BGoogle%E6%96%87%E6%A1%A3%E3%80%81%E8%A1%A8%E6%A0%BC%E5%8F%8A%E5%B9%BB%E7%81%AF%E7%89%87%E7%9A%84Office%E7%BC%96%E8%BE%91%E6%89%A9%E5%B1%95%E7%A8%8B%E5%BA%8F%3A%3A%3A%3Aapplication%2Fmsexcel~%2Capplication%2Fmspowerpoint~%2Capplication%2Fmsword~doc%2Capplication%2Fmsword-template~%2Capplication%2Fvnd.ces-quickpoint~%2Capplication%2Fvnd.ces-quicksheet~%2Capplication%2Fvnd.ces-quickword~%2Capplication%2Fvnd.ms-excel~xls%2Capplication%2Fvnd.ms-excel.sheet.macroEnabled.12~xlsm%2Capplication%2Fvnd.ms-excel.sheet.macroenabled.12~xlsm%2Capplication%2Fvnd.ms-powerpoint~ppt%2Capplication%2Fvnd.ms-powerpoint.presentation.macroEnabled.12~pptm%2Capplication%2Fvnd.ms-powerpoint.presentation.macroenabled.12~pptm%2Capplication%2Fvnd.ms-word~%2Capplication%2Fvnd.ms-word.document.12~docx%2Capplication%2Fvnd.ms-word.document.macroEnabled.12~docm%2Capplication%2Fvnd.ms-word.document.macroenabled.12~docm%2Capplication%2Fvnd.msword~%2Capplication%2Fvnd.openxmlformats-officedocument.presentationml.presentation~pptx%2Capplication%2Fvnd.openxmlformats-officedocument.presentationml.template~potx%2Capplication%2Fvnd.openxmlformats-officedocument.spreadsheetml.sheet~xlsx%2Capplication%2Fvnd.openxmlformats-officedocument.spreadsheetml.template~xltx%2Capplication%2Fvnd.openxmlformats-officedocument.wordprocessingml.document~docx%2Capplication%2Fvnd.openxmlformats-officedocument.wordprocessingml.template~dotx%2Capplication%2Fvnd.presentation-openxml~%2Capplication%2Fvnd.presentation-openxmlm~%2Capplication%2Fvnd.spreadsheet-openxml~%2Capplication%2Fvnd.wordprocessing-openxml~%2Ctext%2Fcsv~%3BNative%20Client%3A%3A%3A%3Aapplication%2Fx-nacl~%2Capplication%2Fx-pnacl~%3BShockwave%20Flash%3A%3AShockwave%20Flash%2027.0%20r0%3A%3Aapplication%2Fx-shockwave-flash~swf%2Capplication%2Ffuturesplash~spl%22%5D; xhs_spses.5dde=*; xhs_spid.5dde=ee270aad39a36e7f.1569549405.2.1573181643.1569549405.85585e18-73b4-4def-8fd3-8c42b17ee231; noteIndex=2"
}

if __name__ == '__main__':
    text = requests.get(
        base + url,
        headers=header).text

    soup = BeautifulSoup(text, 'html.parser')
    images = soup.find_all("i",class_="img")
    path = "./"+url
    os.makedirs(path)
    count = 0
    for img in images:
        with open(path+"/"+str(count)+".jpg",'wb') as f:
            f.write(requests.get(img["style"].replace("background-image:url(","").replace(");","").replace("100","500")).content)
            count = count+1
