# Appointment Checker for Topdriver
This program will notify you (by email) when a new appointment opens up for top driver. This is useful right now because topdriver sessions are fully booked 2 months in advance. So this program is looking out for cancellations every hour.


# Prerequisites:
```
pip install selenium
```

# Directions

## Login (lines 129-130)
```
usr = "topdriver username"
passwd = "topdriver password"

```

## Email Setup & Etc (lines 14-15 and 29-31)

```
recipients=['recipient email here@gmail.com','recipient2@gmail.com']
alreadybooked=['DEC 29','DEC 13','other dates you already have booked']
```



This program will email you when an appointment is available, so for the first "recipients" variable, please type in all the email addresses you want to be sent to. 

The "alreadybooked" variable is used to ignore dates that you already have scheduled. Please use the same format that I have in the example. 



```
        smtp.login("senderemailaddress@gmail.com","passwordtoemail")
        for recipient in recipients:
            smtp.sendmail("senderemailaddress@gmail.com", recipient,message) 

```


In order to send the emails, you will need a sender email, so please customize the second snipped above too. 



![Screenshot](ss.png)
