# Three Buttons and One Light

`Netsol` • `Qualcomm` • `MakeMyTrip`

## Problem

There are **three buttons outside a room**. Only **one button controls a light inside the room**.

You can press the buttons as you like, but you are allowed to **enter the room only once**.

Your task is to figure out **which button turns on the light**.

## Solution

1. Turn **Button 1 ON** and leave it on for a few minutes.
2. Turn **Button 1 OFF**, then turn **Button 2 ON**.
3. Enter the room and check the light.

## Result

* If the **light is ON**, then **Button 2** controls the light.
* If the **light is OFF but the bulb is warm**, then **Button 1** controls the light.
* If the **light is OFF and the bulb is cool**, then **Button 3** controls the light.
