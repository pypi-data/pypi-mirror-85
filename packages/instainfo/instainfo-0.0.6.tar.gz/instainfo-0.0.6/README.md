# InstaInfo!

## Project Description

It provides an efficient and usefull way of fetching information of a particular isntagram username withouth the hassle of providing credentials.

## Functions

- Get Profile Picture URL
- Check If the Profile is private
- Check If the Profile is a Business Account
- Check if the Profile is newly Created
- Get the number of followers of a profile
- Get the number of people that follow a particular profile

## Example

##### Import the module

##### import instainfo

##### Create an instance of the class

##### user = instainfo.UserProfile('alanwalkermusic')

##### Prints the users profile picture URL

##### print(user.GetProfilePicURL())

##### Prints the number of follower the Profile has

##### print(user.FollowersCount())

##### Prints the number of people that follow the profile

##### print(user.FollowedByCount())

##### prints True if the profile is private

##### print(user.IsPrivate())

##### prints True if the profile is business account

##### print(user.IsBusinessAccount())
