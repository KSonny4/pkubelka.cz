Hosted on Netlify, using Hugo.

# Change format of pics and delete exif data

```bash
magick mogrify -format jpg *.heic
exiftool -all= *.jpg
```

# References

Example:

```
[Notes: How to talk to users]({{< ref "week1/how_to_talk_to_users.md" >}})
```

# images

```
![airbnb](/images/week2/airbnb.jpg)
```

# Twitter

https://publish.twitter.com/#

# Youtube

share as embedded

# Spotify

share as embedded
