# tobbetu-classFetcher
A simple library to fetch class Zoom links from the TOBB ETU class portal.

# How to use?
To install simply use:
`pip install tobbetu-classFetcher`

At the beginning of your code add:
`from tobbetu-classFetcher import classFetcher`

Call the function using:
`classFetcher(className, classID)`
  - className is as the name implies, e.g. "ELE 263"
  - classID includes your section to fit with the website formatting, e.g. "cELE2632" (ELE263, Section2)
  
# Dependencies
This library uses *Selenium* and *time*.
