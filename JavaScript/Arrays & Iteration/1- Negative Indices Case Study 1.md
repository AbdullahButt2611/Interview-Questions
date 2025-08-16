## Array negative indices, iteration, and bind behavior in JavaScript

What should be the output of the following program?

```
const customerRide = [{
    riderId: "XC1452",
    walletBalance: 58960,
    totalDistanceInKm: 5.658,
    dateOfTravel: new Date("02-02-2023"),
}, ];
customerRide[-1] = {
    riderId: "XC1451",
    walletBalance: 8569,
    totalDistanceInKm: 14785,
    dateOfTravel: new Date("03-02-2023"),
};
customerRide[1] = {
    riderId: "XC145158",
    walletBalance: 78512,
    totalDistanceInKm: 6931,
    dateOfTravel: new Date("04-02-2023"),
};

function printCustomerRides() {
    let distance = 0;
    for (let index = 0; index < customerRide.length; index++) {
        distance += customerRide[index].totalDistanceInKm;
    }
    console.log(The distance travelled by all customers is $ {
        distance
    });
    distance = 0;
    for (let value of customerRide) {
        distance += value.totalDistanceInKm;
    }
    console.log(The distance travelled by all customers is $ {
        distance
    });
}
const bindedCustomerRides = printCustomerRides.bind(customerRide);
bindedCustomerRides();
```

`Turing - JavaScript`

---

Let’s go through this step-by-step because there’s a subtle trap here with **negative indexes** and **array iteration**.

### Step 1: Initial array

```js
const customerRide = [
  {
    riderId: "XC1452",
    walletBalance: 58960,
    totalDistanceInKm: 5.658,
    dateOfTravel: new Date("02-02-2023"),
  },
];
```

At this point:

* `length` = **1**
* Index `0` holds the first ride object.


### Step 2: Assigning `customerRide[-1]`

```js
customerRide[-1] = {
  riderId: "XC1451",
  walletBalance: 8569,
  totalDistanceInKm: 14785,
  dateOfTravel: new Date("03-02-2023"),
};
```

* In JavaScript, **negative indexes are not real array indexes**.
* `[-1]` becomes just a **string property** `"−1"` on the array object.
* This does **not** affect `length` or show up in `for...of` or `for` index loops.


### Step 3: Assigning `customerRide[1]`

```js
customerRide[1] = {
  riderId: "XC145158",
  walletBalance: 78512,
  totalDistanceInKm: 6931,
  dateOfTravel: new Date("04-02-2023"),
};
```

* This **does** create a second array element.
* Now:

  * Index `0` → first object
  * Index `1` → new object
  * `"−1"` → extra property not part of normal indexing
* `length` = **2**


### Step 4: First loop (`for` with index)

```js
distance = 0;
for (let index = 0; index < customerRide.length; index++) {
  distance += customerRide[index].totalDistanceInKm;
}
```

* Iterates over index `0` and `1`
* `0` → `5.658`
* `1` → `6931`
* Sum = **6936.658**


### Step 5: Second loop (`for...of`)

```js
distance = 0;
for (let value of customerRide) {
  distance += value.totalDistanceInKm;
}
```

* `for...of` also ignores `"−1"` property
* It will iterate over index `0` and `1` only
* Sum = **6936.658**


### Step 6: Output

```plaintext
The distance travelled by all customers is 6936.658
The distance travelled by all customers is 6936.658
```