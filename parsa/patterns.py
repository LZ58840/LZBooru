IMGUR_PATTERN = r"(^(http|https):\/\/)?(i\.)?imgur.com\/((?P<gallery>gallery\/)(?P<galleryid>\w+)|(?P<album>a\/)(?P<albumid>\w+)#?)?(?P<imgid>\w*)"
REDDIT_PATTERN = r"(^(http|https):\/\/)?(((i|preview)\.redd\.it\/)(?P<imgid>\w+\.\w+)|(www\.reddit\.com\/gallery\/)(?P<galleryid>\w+))"
GENERIC_PATTERN = r"(https?:\/\/.*\.(?:png|jpg|jpeg))"