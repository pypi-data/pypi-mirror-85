# Gormanian

## Gormanian Calendar Calculator/Converter

### What is it?

Put simply, it is a library to calculate an alternative date structure based on the comedic sketch of [Dave Gorman](http://davegorman.com/).  In an episode of '*Modern Life is Goodish*', Dave Gorman proposed a new calendar format to replace the existing Gregorian calendar.  In particular, he takes umbridge at the fact that the length of a month varies, when all other units of time are fixed and identical.

You can watch the video in question [here](https://www.youtube.com/watch?v=vunESk53r5U&feature=youtu.be) on Dave Gorman's official YouTube channel.

### But why?

Why not?  I happen to agree with the calendar, and decided to write this for a laugh.

### How to Use

#### To convert the current date


    import gormanian
    
    response = gormanian.now()
    
    print(response.as_string)



#### To convert a specific date
Use the standard datetime format for any given date.

    from datetime import datetime
    import gormanian
    
    response = gormanian.convert(datetime(2000, 12, 1))
    
    print(response.as_string)

#### ISO-8601 format:
You can also retrieve the date in ISO-8601 basic format.

    from datetime import datetime
    import gormanian
    
    response = gormanian.convert(datetime(2000, 12, 31))
    
    print(response.isoformat)

