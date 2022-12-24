# ECE445-Refill_Dispensary

**Welcome to our refill dispensary repo!**

**Introduction:**. 

Plastic waste is a massive issue world-wide, particularly as it pertains to the packaging of food and other household goods. The United States Environmental Protection Agency estimates that in 2018, 14 million tons of plastic was consumed for packaging in the USA with about seventy percent of that ending up in landfills[1]. Plastic waste is detrimental to the environment as it doesn’t decompose naturally on human time scales. End-user plastic waste is often unnecessary as consumers own containers capable of being reused. 

We built a vending machine that dispenses precise quantities of goods (between 10 g and 5 kg) into reusable containers. The goal of the machine is to get users to keep bringing the same container back. In addition to plastic waste, our machine tackles the issue of waste in general as users are no longer forced to get quantities larger than desired. 

<img width="271" alt="Screenshot 2022-12-24 at 10 35 45 AM" src="https://user-images.githubusercontent.com/77509822/209442734-a2842fff-d14c-4912-ace2-dbd37597fce8.png"> <img width="390" alt="Screenshot 2022-12-24 at 10 50 10 AM" src="https://user-images.githubusercontent.com/77509822/209443107-f388752b-1c9a-44e2-8186-c785f6a76512.png">

**High-level requirements:**
1. The user is able to choose an item and quantity to get dispensed via buttons and rotary potentiometers. Before placing the order, the user will have some indication of the amount ordered within a tolerance of 10 grams for weights between .1 kg and 2kg.
2. The machine dispenses two different types of low-viscosity liquids and is able to perform 2 orders in succession. 
3. The machine can deliver another order properly after 1 of the liquids is switched out or refilled. 

**Block Diagram:**. 

<img width="739" alt="Screenshot 2022-12-24 at 11 00 21 AM" src="https://user-images.githubusercontent.com/77509822/209443388-2926d432-04e5-417a-aa58-91b34c838393.png">
