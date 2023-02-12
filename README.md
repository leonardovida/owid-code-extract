# Code extract for the OWID application

## Original repository

This repository contains just a part of the code used for the etl pipeline I developed for the nearit.io project.

The nearit.io project is a simple website offers freely pre-compiled lists of places for world cities (mainly restaurants for now) 
that are highly recommended by locals. These lists exist only on Google Maps, because of its popularity.

Initially the project aggregated data from locals leveraging our network of friends, unfortunately this approach was not scalable. 
We then turned to scrape data from Google Maps, Amigo, Mapstr and other sources. The objective is to provide a simple way to create lists of places for a certain city 
and share them with other people.

Here I selected the code I wrote for the Amigo extract pipeline.