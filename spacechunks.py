# -*- coding: utf-8 -*-

import feedparser
import sys
import json
import os
import re



MEDIA_BUCKET = os.environ["MEDIA_BUCKET"]
REGION = os.environ["REGION"]
MEDIA_URL =  "https://{}.amazonaws.com/{}/{}"
print("URL=",MEDIA_URL)

d1 = feedparser.parse(".rss file")
SESSION_BODY_3 = "body_3"
SESSION_LIST_2 = "list_2"
SESSION_BODY_HELP = "help"
SESSION_BODY_TITLENAM = "title name"
SESSION_BODY_Notitle = "No title"
def lambda_handler(event, context):
    print("event=",event)
    print("context=",context)
    print("request type=",event["request"]["type"])
    if event["request"]["type"] == "LaunchRequest":
        print("on_launch")
        return list_template_two()
    elif event["request"]["type"] == "Display.ElementSelected":
        print("token selected=",event["context"]["Display"]["token"],event["request"]["token"])
        return item_selected(event["context"]["Display"]["token"], event["request"]["token"])

    elif event["request"]["type"] == "IntentRequest":
        #return list_template(event["request"]["intent"]["slots"]["number"]["value"])
        print("intent name=",event["request"]["intent"]["name"])
        if event["request"]["intent"]["name"] == "titlenumber":
            found="no match"
            titlenum=event["request"]["intent"]["slots"]["titlenum"]["value"]
            print("title num=",titlenum)
            found="match"
            return body_template_by_title(titlenum)
            if found=="nomatch":
                print("no title")
                return notitle()
        if event["request"]["intent"]["name"] == "titlename":
            found="no match"
            titlenam1=event["request"]["intent"]["slots"]["titlenam"]["value"]
            print("title nam=",titlenam1)
            i=0
            lengthrss=0
            lengthrsslen=len(d1.entries)
            titlenam=re.sub('[^A-Za-z0-9]+', '', titlenam1)
            for lengthrss in range(0, lengthrsslen):
                print("k=",d1.entries[lengthrss].title,lengthrss,titlenam)
                titlnam=re.sub('[^A-Za-z0-9]+', '', d1.entries[lengthrss].title)
                if titlenam.upper()==titlnam.upper():
                    print("title=",titlenam.upper(),titlnam.upper())
                    found="match"
                    break
            if found=="no match":
                for lengthrss in range(0, lengthrsslen):
                    cutnewtitle=""
                    titlnewnewname=d1.entries[lengthrss].title.split(" ")
                    cuttitle=titlenam1.split(" ")
                    print("cuttitle",len(cuttitle))
                    if len(cuttitle)==4 and len(titlnewnewname)>=4:
                        cutnewtitle=cuttitle[0]+cuttitle[1]+cuttitle[2]+cuttitle[3]
                        titlnewnename=titlnewnewname[0]+titlnewnewname[1]+titlnewnewname[2]+titlnewnewname[3]
                    if len(cuttitle)==3 and len(titlnewnewname)>=3:
                        cutnewtitle=cuttitle[0]+cuttitle[1]+cuttitle[2]
                        titlnewnename=titlnewnewname[0]+titlnewnewname[1]+titlnewnewname[2]
                    elif len(cuttitle)==2 and len(titlnewnewname)>=2:
                        cutnewtitle=cuttitle[0]+cuttitle[1]
                        titlnewnename=titlnewnewname[0]+titlnewnewname[1]
                    elif len(cuttitle)==1 and len(titlnewnewname)>=1:
                        cutnewtitle=cuttitle[0]
                        titlnewnename=titlnewnewname[0]
                    print("titlenewnename",titlnewnename,cutnewtitle,len(cuttitle))
                    titlnewnename=re.sub('[^A-Za-z0-9]+', '', titlnewnename)
                    cutnewtitle=re.sub('[^A-Za-z0-9]+', '', cutnewtitle)
                    if titlnewnename.upper()==cutnewtitle.upper():
                        print("title new inside cut=",titlnewnename.upper(),cutnewtitle.upper())
                        found="match"
                        break

            if found=="match":
                return body_template_by_titlename(d1.entries[lengthrss],titlenam)
            elif found=="no match":
                print("no title")
                return notitle()


        elif event["request"]["intent"]["name"] == "AMAZON.StopIntent":
                return goodby()
         #if event["request"]["intent"]["name"] == "listtemplate":
           #return list_template_three()
        #if event["request"]["intent"]["name"] == "AMAZON.YesIntent":
        #    ses = event["session"]["attributes"]["template"].split("_")
        #    print("session=",ses[0])
        #    if ses[0] == "list":
        #        return body_template(ses[1])
        #    elif ses[0] == "category":
        #        return video_template(ses[1])
        #    elif ses[0] == "act":
        #        return action_sample()
        #   else:
        #        return help()
        # print("video=",event["request"]["intent"]["name"])

        if event["request"]["intent"]["name"] == "Amazon.HelpIntent":
            print("request type unmatch")
            return help()
        if event["request"]["intent"]["name"] == "goback":
           return list_template_two()

    else:
        return help()

def help():
    title = "Echo Show Help"
    speech = "Welcome to Space Chunks. To show the details for an image say 'title number' and the number, or say 'title name' and the name ?. If the title is too long you can just say the first 2 or 3 words in the title. "
    directives = [
        {
            "type": "Hint",
            "hint": {
                "type": "PlainText",
                "text": "To show contents for the image say the title number or name ?"
            }
        }
    ]

    return build_speechlet_response(title, speech, directives, SESSION_BODY_HELP)
def notitle():
    body_template = {
        "type": "Display.RenderTemplate",
        "template": {
            "type": "BodyTemplate6",
            "token": "bt6",
            "backButton": "VISIBLE",
            "backgroundImage": {
                "contentDescription": "Space",
                "sources": [
                    {
                        "url": media_url("background-sp.png")
                    }
                ]
            },
        }
    }
    title = "There is no title by the title name or number. Choose a different title or number. Echo Show Help. "
    speech = "There is no title by the title name or number. Choose a different title or number"
    directives = [
        {
            "type": "Hint",
            "hint": {
                "type": "PlainText",
                "text": "Sorry, there is no title by the name or number. Say 'Go back' or title number or name ? "
            },
            "textContent": {
                "tertiaryText": {
                    "text": title,
                    "type": "RichText"
                },
            }
        },
        body_template
    ]

    return build_speechlet_response(title, speech, directives, SESSION_BODY_Notitle)

def goodby():

    body_template = {
        "type": "Display.RenderTemplate",
        "template": {
            "type": "BodyTemplate6",
            "token": "bt6",
            "backButton": "VISIBLE",
            "backgroundImage": {
                "contentDescription": "Space",
                "sources": [
                    {
                        "url": media_url("background-sp.png")
                    }
                ]
            },
        }
    }

    directives = [
        body_template
    ]
    response = {
        "version": "1.0",
        "response": {
            "outputSpeech": {
                "type": "PlainText",
                "text": "good bye."
            },
            "directives": directives,
            "shouldEndSession": True
        }
    }
    print("URL=",MEDIA_URL)
    print(response)
    return response
# list template zero

# list template one

# list template two
def list_template_two():
    title = "Space Chunks "
    speech = "Welcome to Space Chunks. You can say 'show me contents for the title number' and say the title number,  or say 'show me contents for the title name' and say the title name to see the details for a particular image. Say help for more information. "
    #speech.reprompt("Choose a title or say yes")
    print("image=",d1.entries[0].published)
    template = {
        "type": "Display.RenderTemplate",
        "template": {
            "type": "ListTemplate2",
            "token": "list_template_two",
            "title": "Space Chunks",
            "backButton": "VISIBLE",
            "backgroundImage": {
                "contentDescription": "Mt Fuji",
                "sources": [
                    {
                        "url": media_url("background-sp.png")
                    }
                ]
            },


            "listItems": [
                {
                        "token": "item_1",
                        "image": {
                            "sources": [
                                {
                                #"url": media_url(d.entries[0].thumbnail)
                                "url":d1.entries[0].links[1].href,
                                "size":"SMALL",
                                "widthPixels": 280,
                                "heightPixels":280
                                }
                            ],
                        },

                            "textContent": {
                                "primaryText": {
                                "type": "RichText",
                                "text": "<font size='1'>" + d1.entries[0].title + "</font>"
                                },
                                "secondaryText": {
                                "type": "RichText",
                                "text": d1.entries[0].published
                                },
                                #"tertiaryText": {
                                #"type": "RichText",
                                #"text": "<br/><font size='2'><i>" + d1.entries[0].description + "</i></font>"
                                #}
                            }

                },
                {
                        "token": "item_2",
                        "image": {
                            "sources": [
                                {
                                #"url": media_url(d.entries[0].thumbnail)
                                "url":d1.entries[1].links[1].href,
                                "size":"SMALL",
                                "widthPixels": 280,
                                "heightPixels":280
                                }
                            ],
                        },

                            "textContent": {
                                "primaryText": {
                                "type": "RichText",
                                "text": "<font size='1'>" + d1.entries[1].title + "</font>"
                                },
                                "secondaryText": {
                                "type": "RichText",
                                "text": d1.entries[1].published
                                },
                                #"tertiaryText": {
                                #"type": "RichText",
                                #"text": "<br/><font size='2'><i>" + d1.entries[0].description + "</i></font>"
                                #}
                            }

                },
                {
                        "token": "item_3",
                        "image": {
                            "sources": [
                                {
                                #"url": media_url(d.entries[0].thumbnail)
                                "url":d1.entries[2].links[1].href,
                                "size":"SMALL",
                                "widthPixels": 280,
                                "heightPixels":280
                                }
                            ],
                        },

                            "textContent": {
                                "primaryText": {
                                "type": "RichText",
                                "text": "<font size='1'>" + d1.entries[2].title + "</font>"
                                },
                                "secondaryText": {
                                "type": "RichText",
                                "text": d1.entries[2].published
                                },
                                #"tertiaryText": {
                                #"type": "RichText",
                                #"text": "<br/><font size='2'><i>" + d1.entries[0].description + "</i></font>"
                                #}
                            }

                },
                {
                        "token": "item_4",
                        "image": {
                            "sources": [
                                {
                                #"url": media_url(d.entries[0].thumbnail)
                                "url":d1.entries[3].links[1].href,
                                "size":"SMALL",
                                "widthPixels": 280,
                                "heightPixels":280
                                }
                            ],
                        },

                            "textContent": {
                                "primaryText": {
                                "type": "RichText",
                                "text": "<font size='1'>" + d1.entries[3].title + "</font>"
                                },
                                "secondaryText": {
                                "type": "RichText",
                                "text": d1.entries[3].published
                                },
                                #"tertiaryText": {
                                #"type": "RichText",
                                #"text": "<br/><font size='2'><i>" + d1.entries[0].description + "</i></font>"
                                #}
                            }

                },
                {
                        "token": "item_5",
                        "image": {
                            "sources": [
                                {
                                #"url": media_url(d.entries[0].thumbnail)
                                "url":d1.entries[4].links[1].href,
                                "size":"SMALL",
                                "widthPixels": 280,
                                "heightPixels":280
                                }
                            ],
                        },

                            "textContent": {
                                "primaryText": {
                                "type": "RichText",
                                "text": "<font size='1'>" + d1.entries[4].title + "</font>"
                                },
                                "secondaryText": {
                                "type": "RichText",
                                "text": d1.entries[4].published
                                },
                                #"tertiaryText": {
                                #"type": "RichText",
                                #"text": "<br/><font size='2'><i>" + d1.entries[0].description + "</i></font>"
                                #}
                            }

                },
                {
                        "token": "item_6",
                        "image": {
                            "sources": [
                                {
                                #"url": media_url(d.entries[0].thumbnail)
                                "url":d1.entries[5].links[1].href,
                                "size":"SMALL",
                                "widthPixels": 280,
                                "heightPixels":280
                                }
                            ],
                        },

                            "textContent": {
                                "primaryText": {
                                "type": "RichText",
                                "text": "<font size='1'>" + d1.entries[5].title + "</font>"
                                },
                                "secondaryText": {
                                "type": "RichText",
                                "text": d1.entries[5].published
                                },
                                #"tertiaryText": {
                                #"type": "RichText",
                                #"text": "<br/><font size='2'><i>" + d1.entries[0].description + "</i></font>"
                                #}
                            }

                },
                {
                        "token": "item_7",
                        "image": {
                            "sources": [
                                {
                                #"url": media_url(d.entries[0].thumbnail)
                                "url":d1.entries[6].links[1].href,
                                "size":"SMALL",
                                "widthPixels": 280,
                                "heightPixels":280
                                }
                            ],
                        },

                            "textContent": {
                                "primaryText": {
                                "type": "RichText",
                                "text": "<font size='1'>" + d1.entries[6].title + "</font>"
                                },
                                "secondaryText": {
                                "type": "RichText",
                                "text": d1.entries[6].published
                                },
                                #"tertiaryText": {
                                #"type": "RichText",
                                #"text": "<br/><font size='2'><i>" + d1.entries[0].description + "</i></font>"
                                #}
                            }

                },
                {
                        "token": "item_8",
                        "image": {
                            "sources": [
                                {
                                #"url": media_url(d.entries[0].thumbnail)
                                "url":d1.entries[7].links[1].href,
                                "size":"SMALL",
                                "widthPixels": 280,
                                "heightPixels":280
                                }
                            ],
                        },

                            "textContent": {
                                "primaryText": {
                                "type": "RichText",
                                "text": "<font size='1'>" + d1.entries[7].title + "</font>"
                                },
                                "secondaryText": {
                                "type": "RichText",
                                "text": d1.entries[7].published
                                },
                                #"tertiaryText": {
                                #"type": "RichText",
                                #"text": "<br/><font size='2'><i>" + d1.entries[0].description + "</i></font>"
                                #}
                            }

                },
                {
                        "token": "item_9",
                        "image": {
                            "sources": [
                                {
                                #"url": media_url(d.entries[0].thumbnail)
                                "url":d1.entries[8].links[1].href,
                                "size":"SMALL",
                                "widthPixels": 280,
                                "heightPixels":280
                                }
                            ],
                        },

                            "textContent": {
                                "primaryText": {
                                "type": "RichText",
                                "text": "<font size='1'>" + d1.entries[8].title + "</font>"
                                },
                                "secondaryText": {
                                "type": "RichText",
                                "text": d1.entries[8].published
                                },
                                #"tertiaryText": {
                                #"type": "RichText",
                                #"text": "<br/><font size='2'><i>" + d1.entries[0].description + "</i></font>"
                                #}
                            }

                },
                {
                        "token": "item_10",
                        "image": {
                            "sources": [
                                {
                                #"url": media_url(d.entries[0].thumbnail)
                                "url":d1.entries[9].links[1].href,
                                "size":"SMALL",
                                "widthPixels": 280,
                                "heightPixels":280
                                }
                            ],
                        },

                            "textContent": {
                                "primaryText": {
                                "type": "RichText",
                                "text": "<font size='1'>" + d1.entries[9].title + "</font>"
                                },
                                "secondaryText": {
                                "type": "RichText",
                                "text": d1.entries[9].published
                                },
                                #"tertiaryText": {
                                #"type": "RichText",
                                #"text": "<br/><font size='2'><i>" + d1.entries[0].description + "</i></font>"
                                #}
                            }

                },
                {
                        "token": "item_11",
                        "image": {
                            "sources": [
                                {
                                #"url": media_url(d.entries[0].thumbnail)
                                "url":d1.entries[10].links[1].href,
                                "size":"SMALL",
                                "widthPixels": 280,
                                "heightPixels":280
                                }
                            ],
                        },

                            "textContent": {
                                "primaryText": {
                                "type": "RichText",
                                "text": "<font size='1'>" + d1.entries[10].title + "</font>"
                                },
                                "secondaryText": {
                                "type": "RichText",
                                "text": d1.entries[10].published
                                },
                                #"tertiaryText": {
                                #"type": "RichText",
                                #"text": "<br/><font size='2'><i>" + d1.entries[0].description + "</i></font>"
                                #}
                            }

                }



            ]



            #}
        }
    }

    directives = [
        template
    ]

    return build_speechlet_response(title, speech, directives, SESSION_LIST_2)

#def list_template_three():

#    title = "Life Minute TV"
#    speech = "Welcome to Life minute TV. You can select a title or choose a category"
#    #speech.reprompt("Choose a title or say yes")
#    template = {
#        "type": "Display.RenderTemplate",
#        "template": {
#            "type": "ListTemplate3",
#            "token": "list_template_three",
#            "title": " ",
#            "backButton": "HIDE",

# "listItems": [
#                {
#                        "token": "item_list_three",
#                       "textContent": {
#                        "tertiaryText": {
#                            "type": "RichText",
#                            "text": "Categories Home Movies Music Fashion Celebrity Beauty Health Family Eat & Drink"
#                        }
#                    }
#                }
#            ],
            #}
#        }
#    }

#    directives = [
#        template
#    ]

#    return build_speechlet_response(title, speech, directives, SESSION_LIST_2)

##------------- List template three by title number------------------
def body_template_by_title(number):

    url = d1.entries[int(number)-1].links[1].href
    print("url=",number,url)
    title = d1.entries[int(number)-1].title
    speech = d1.entries[int(number)-1].title + ". " + d1.entries[int(number)-1].description
    primary_text = d1.entries[int(number)-1].title
    secondary_text = " "
    tertiary_text = d1.entries[int(number)-1].description
    speech = " ".join([speech])

    template = {
        "type": "Display.RenderTemplate",
        "template": {
            "type": "BodyTemplate1",
            "token": "bt1",
            "backButton": "VISIBLE",
            "backgroundImage": {
                "contentDescription": "space",
                "sources": [
                    {
                        "url": media_url("background-sp.png")
                    }
                ]
            },
            #"title": title,
            "image": {
                "contentDescription": d1.entries[int(number)-1].title,
                "sources": [
                    {
                        "url": d1.entries[int(number)-1].links[1].href,
                        "size":"SMALL",
                        "widthPixels": 280,
                        "heightPixels":280
                    }
                ]
            },
            "textContent": {
                "primaryText": {
                    "text": "<font size='1'>" + primary_text + "</font>",
                    "type": "RichText"
                },
                "secondaryText": {
                    "text": "<font size='7'>" + secondary_text + "</font>",
                    "type": "RichText"
                },
                "tertiaryText": {
                    "text": "<font size='1'>" + tertiary_text + "</font>",
                    "type": "RichText"
                }
            }
        }
    }

    # body template 3 do not show hint
    directives = [
        template
    ]
    return build_speechlet_response(title, speech, directives, SESSION_BODY_3)

##------------- List template three by title number------------------
def body_template_by_titlename(k,titlename):

    url = k.links[1].href
    print("url=",url)
    title = k.title
    speech = k.title + ". " + k.description
    primary_text = k.title
    secondary_text = " "
    tertiary_text = k.description
    speech = " ".join([speech])

    template = {
        "type": "Display.RenderTemplate",
        "template": {
            "type": "BodyTemplate1",
            "token": "bt1",
            "backButton": "VISIBLE",
            "backgroundImage": {
                "contentDescription": "space",
                "sources": [
                    {
                        "url": media_url("background-sp.png")
                    }
                ]
            },
            #"title": title,
            "image": {
                "contentDescription": k.title,
                "sources": [
                    {
                        "url": k.links[1].href,
                        "size":"SMALL",
                        "widthPixels": 280,
                        "heightPixels":280
                    }
                ]
            },
            "textContent": {
                "primaryText": {
                    "text": "<font size='1'>" + primary_text + "</font>",
                    "type": "RichText"
                },
                "secondaryText": {
                    "text": "<font size='7'>" + secondary_text + "</font>",
                    "type": "RichText"
                },
                "tertiaryText": {
                    "text": "<font size='1'>" + tertiary_text + "</font>",
                    "type": "RichText"
                }
            }
        }
    }

    # body template 3 do not show hint
    directives = [
        template
    ]
    return build_speechlet_response(title, speech, directives, SESSION_BODY_TITLENAM)



##--------------Video Template Cat ----------------
def video_template_cat(entry):


    print("inside category=", brightcoveurl, entry.guid)

    url = entry.guid.split("/")
    print("url=", url[3])


    video_template = {

        "type": "VideoApp.Launch",
        "videoItem":
            {
                    #"source": media_url("alexa_test.mp4"),
                    #"source": entry.media_content[0]["url"],
                    "source": brightcoveurl + url[3],
                    "metadata": {
                        "title": entry.title,
                        "subtitle": entry.category
                    }
            }
    }


    primary_text = "starting video"
    secondary_text = entry.title

    body_template = {
        "type": "Display.RenderTemplate",
        "template": {
            "type": "BodyTemplate6",
            "token": "bt6",
            "backButton": "VISIBLE",
            "backgroundImage": {
                "contentDescription": "Mt Fuji",
                "sources": [
                    {
                        "url": media_url("background-sp.png")
                    }
                ]
            },
            "textContent": {
                "primaryText": {
                    "text": primary_text,
                    "type": "PlainText"
                },
            "secondaryText": {
                    "text": secondary_text,
                    "type": "PlainText"
                }
            }
        }
    }

    directives = [
        video_template,
        body_template
        ]

    response = {
        "version": "1.0",
        "response": {
            "outputspeech": "Playing Video",
            "card": {
                'type': 'Simple',
                'title': "video player",
                'content': "this template play video."
            },
            "directives": directives
        }
    }
    print(response)
    return response
        #build_speechlet_response(title, speech, directives, SESSION_VIDEO)
## --------- video ---------

def video_template(url):


    print("inside category=", url)



    video_template = {

        "type": "VideoApp.Launch",
        "videoItem":
            {
                    #"source": media_url("alexa_test.mp4"),
                    "source": url,
                    "metadata": {
                        "title": d1.entries[0].title,
                        "subtitle": d1.entries[0].category
                    }
            }
    }


    primary_text = "starting video"
    secondary_text = d1.entries[1].title

    body_template = {
        "type": "Display.RenderTemplate",
        "template": {
            "type": "BodyTemplate6",
            "token": "bt6",
            "backButton": "VISIBLE",
            "backgroundImage": {
                "contentDescription": "Mt Fuji",
                "sources": [
                    {
                        "url": media_url("background-space.jpg")
                    }
                ]
            },
            "textContent": {
                "primaryText": {
                    "text": primary_text,
                    "type": "PlainText"
                },
            "secondaryText": {
                    "text": secondary_text,
                    "type": "PlainText"
                }
            }
        }
    }

    directives = [
        video_template,
        body_template
        ]

    response = {
        "version": "1.0",
        "response": {
            "outputspeech": "Playing Video",
            "card": {
                'type': 'Simple',
                'title': "video player",
                'content': "this template play video."
            },
            "directives": directives
        }
    }
    print(response)
    return response
        #build_speechlet_response(title, speech, directives, SESSION_VIDEO)

##------------------ Video 1 --------------------##

## --------- video ---------

def video_template1(number):


    print("inside category=", number)

    url = d1.entries[int(number)].guid.split("/")

    video_template = {

        "type": "VideoApp.Launch",
        "videoItem":
            {
                    #"source": media_url("alexa_test.mp4"),
                    #"source": d1.entries[int(number)].media_content[0]["url"],
                    "source" : brightcoveurl + url[3],
                    "metadata": {
                        "title": d1.entries[int(number)].title,
                        "subtitle": d1.entries[int(number)].category
                    }
            }
    }


    primary_text = "starting video"
    secondary_text = d1.entries[int(number)].title

    body_template = {
        "type": "Display.RenderTemplate",
        "template": {
            "type": "BodyTemplate6",
            "token": "bt6",
            "backButton": "VISIBLE",
            "backgroundImage": {
                "contentDescription": "Mt Fuji",
                "sources": [
                    {
                        "url": media_url("background-1.jpg")
                    }
                ]
            },
            "textContent": {
                "primaryText": {
                    "text": primary_text,
                    "type": "PlainText"
                },
            "secondaryText": {
                    "text": secondary_text,
                    "type": "PlainText"
                }
            }
        }
    }

    directives = [
        video_template,
        body_template
        ]

    response = {
        "version": "1.0",
        "response": {
            "outputspeech": "Playing Video",
            "card": {
                'type': 'Simple',
                'title': "video player",
                'content': "this template play video."
            },
            "directives": directives
        }
    }
    print(response)
    return response
    #build_speechlet_response(title, speech, directives, SESSION_VIDEO)

## -------------------Playing video by title ---------------------------
## --------- video ---------

def video_template_title(tittitle,entry):


    print("inside title name=", tittitle)

    url = entry.guid.split("/")

    print("url=",tittitle)

    video_template = {

        "type": "VideoApp.Launch",
        "videoItem":
            {
                    #"source": media_url("alexa_test.mp4"),
                    #"source": entry.media_content[0]["url"],
                    "source" : brightcoveurl + url[3],
                    "metadata": {
                        "title":entry.title,
                        "subtitle": entry.category
                    }
            }
    }



    body_template = {
        "type": "Display.RenderTemplate",
        "template": {
            "type": "BodyTemplate6",
            "token": "bt6",
            "backButton": "VISIBLE",
            "backgroundImage": {
                "contentDescription": "Mt Fuji",
                "sources": [
                    {
                        "url": media_url("background-sp.png")
                    }
                ]
            },
            "textContent": {
                "primaryText": {
                    "text": entry.title,
                    "type": "PlainText"
                },
                "secondaryText": {
                    "text": entry.category,
                    "type": "PlainText"
                }
            }
        }
    }

    directives = [
        video_template,
        body_template
        ]

    response = {
        "version": "1.0",
        "response": {
            "outputspeech": "Playing Video " + entry.title,
            "card": {
                'type': 'Simple',
                'title': "video player",
                'content': "this template play video."
            },
        "directives": directives
        }
    }
    print(response)
    return response
        #build_speechlet_response(title, speech, directives, SESSION_VIDEO)

##----------------------------Echo Show touch screen ------------------
def item_selected(context_token, token):
    action_map = {
        "action1": "Action sample",
        "list_template_two": "list of items",
        "list_template_by_cat": "list tepmlate by category"
    }
    title = "Playing title."
    primary_text = "action invoked from {}. the token is {}.".format(
        action_map[context_token],
        token
    )
    #if event["context"]["Display"]["token"] == "list of items" and event["request"]["token"] == "item_1":

    #video_template = {

    #    "type": "VideoApp.Launch",
    #    "videoItem":
    #       {
    #                "source": media_url("alexa_test.mp4"),
    #                #"source": entry.media_content[0]["url"],
    #                "metadata": {
    #                   "title":"test",
    #                     "subtitle": "sub test"
    #                }
    #        }
    #}

    template = {
        "type": "Display.RenderTemplate",
        "template": {
            "type": "BodyTemplate1",
            "token": "action2",
            "backButton": "HIDDEN",
            "title": title,
            "textContent": {
                "primaryText": {
                    "text": primary_text,
                    "type": "PlainText"
                }
            }
        }
    }
    directives = [
        video_template,
        template
    ]

    return build_speechlet_response(title, primary_text, directives, SESSION_ACTION)






## --------- helper methods ---------

def media_url(key):
    return MEDIA_URL.format(MEDIA_BUCKET,REGION,key)

def build_speechlet_response(title, speech, directives, phase):

    response = {
        "version": "1.0",
        "response": {
            "outputSpeech": {
                "type": "PlainText",
                "text": "{}.".format(speech)
            },
            "card": {
                'type': 'Simple',
                'title': title,
                'content': speech
            },
            "directives": directives,
            "shouldEndSession": False
        },
        "sessionAttributes": {
            "template": phase
        }
    }
    print(response)
    return response
