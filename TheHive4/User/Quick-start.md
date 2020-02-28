# Quick start with TheHive 4



* [TL;DR](#tl-dr)
* [Intialize TheHive 4](#intialize-thehive-4)
  + [Create an organisation](#create-an-organisation)
  + [Create a user](#create-a-user)





## TL;DR

0. Default administrator account: `admin@thehive.local`/`secret`
1. Login with default account
2. Create an organisaton
3. Create a user account



## Before starting

Starting from TheHive 4.0-RC1, an email address is requested, and is mandatory to register a new user, and to log in the application. 



## Intialize TheHive 4

This version of TheHive comes with a big improvement: multi-tenancy and fine tuning permissions. 

A default system group name "*admin*" belong to the application and is dedicated to user accounts in charge of administrating the solution. This group contains one default account named "*admin@thehive.local*" with the password `secret`.

This default group cannot create and own *Cases* of any other related objects like *Tasks* or *Observables*.

### Create an organisation

To start using TheHive, an *organisation* and at least a standard user belonging to this group have to be created. 



![admin-add-organisation](files/admin-add-organisation.png)

###  Create a user

![admin-add-user](files/admin-add-user.png)