# How Does React Router Handle Dynamic Routing?

`LinkedIn`

## What This Question Is Asking

The question wants you to walk through the **process React Router follows to turn a changing URL into the right rendered components**, with a focus on routes that contain dynamic segments (the parts written as `:param`).

In plain terms, you need to explain:

- How React Router **notices** that the URL changed.
- How it **matches** that URL against the routes you defined.
- How it **extracts** the dynamic values from the URL (for example, the `42` in `/users/42`).
- How it **renders** the matched components, including nested ones.

<mark>The word "dynamic" is the key. Make sure you clearly explain how `:param` segments are captured and made available through `useParams()`, since that is the heart of the answer.</mark>

<br><br>

## How to Answer This Well

- Open with a **one-line idea** of dynamic routing (one route pattern serving many URLs, like `/users/:userId` handling any user).
- Walk through the flow **in order**, from URL change to final render, instead of one long paragraph.
- Name the **actual pieces** as you go (the history listener, your `<Routes>` tree, match ranking, `useParams()`, and `<Outlet>`).
- Drop in a **tiny code example** for the dynamic segment and `useParams()`, since it makes the answer concrete.
- Finish with a **short recap** of the full pipeline so the interviewer hears a clean summary.
<br><br>

## Answer

### 1. It Keeps an Ear on the Address Bar
- When you click a link, hit Back or Forward, or call `navigate()`, React Router's history helper notices the new URL right away.
- Internally it stores that new URL in its own state, so the rest of React can react to the change.

<br><br>

### 2. It Reads Your Route "Map"
You write a tree of `<Routes>` in your app (for example):

```jsx
<Route path="users/:userId" element={<Profile />} />
<Route path="about" element={<About />} />
```

React Router flattens that tree into a simple list, like reading all the street signs in one go.

<br><br>

### 3. It Picks the Best Match
- Imagine you have two possible street signs: `/users/new` (static) and `/users/:userId` (dynamic).
- React Router has a small rulebook that says "static is more precise than dynamic," so if you go to `/users/new`, it picks the static one first.
- Otherwise, it tries each pattern in order until one fits your exact URL.

<br><br>

### 4. It Grabs the "Wildcard" Pieces
- For a dynamic route like `/users/:userId`, whatever you type in place of `:userId` (for example `/users/42`) gets plucked out and stored as `{ userId: "42" }`.
- That object of parameters is made available through the `useParams()` hook, so inside your `<Profile>` component you just write:

```js
let { userId } = useParams();
```

and you immediately know you are displaying user "42."

<br><br>

### 5. It Builds Your Page Tree
- Once it knows which route matched, React Router lines up all the matched pieces in order (parents first, children next) and renders them.
- Think of it like stacking nested boxes: each route's component sits inside its parent through an `<Outlet>` placeholder.

<br><br>

### Putting It All Together
- Listen to address-bar changes.
- Flatten your route definitions into a simple list.
- Rank and match the URL against that list, choosing the most specific route first.
- Extract any dynamic bits (the parts after `:`) into a params object.
- Render the matched components, dropping them into each other through `<Outlet>`.

<br><br>

## Other Ways This Question Can Be Asked

- What is the difference between static routing and dynamic routing in React Router?
- How do you read URL parameters from a route, and which hook do you use?
- How does `useParams()` work, and when would you reach for it?
- How does React Router decide which route to render when two patterns could match?
- How do nested routes and `<Outlet>` work together?
- How would you build a route that handles any user ID without defining one route per user?