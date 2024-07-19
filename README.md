Hosted on Netlify, using Hugo.

# Change format of pics and delete exif data

```bash
magick mogrify -format jpg '*.heic' '*.HEIC'
rm -rf *heic
exiftool -all= -ext jpg -ext jpeg -ext png .
rm -rf *.jp[e]*g_original
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

# Strava

