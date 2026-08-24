# How does React Router handle dynamic routing?
`Linkedin`

## 1. It Keeps an Ear on the Address Bar
- When you click a link, hit Back/Forward, or call navigate(), React Router’s history helper notices the new URL right away.
- Internally it stores that new URL in its own state so the rest of React can react to the change.

## 2. It Reads Your Route “Map”
You write a tree of `<Routes>` in your app (for example):

```jsx
<Route path="users/:userId" element={<Profile />} />
<Route path="about" element={<About />} />
```

React Router flattens that tree into a simple list, like reading all the street signs in one go.

## 3. It Picks the Best Match
- Imagine you have two possible street signs: `“/users/new”`(static) and `“/users/:userId”` (dynamic).
- React Router has a little rulebook that says “static is more precise than dynamic,” so if you go to `/users/new`, it picks the first.
- Otherwise, it tries each pattern in order until one fits your exact URL.
  
## 4. It Grabs the “Wildcard” Pieces
- For a dynamic route like `/users/:userId`, whatever you type in place of `:userId` (for example `/users/42`) gets plucked out and stored as `{ userId: "42" }`.
- That object of parameters is made available via the `useParams()` hook, so inside your `<Profile>` component you just say:

```js
let { userId } = useParams();
```
and you immediately know you’re displaying user “42.”

## 5. It Builds Your Page Tree
- Once it knows which route matched, React Router lines up all the matched pieces in order (parents first, children next) and renders them.
- Think of it like stacking nested boxes: each route’s component sits inside its parent via an `<Outlet>` placeholder.


## Putting It All Together
- Listen to address-bar changes.
- Flatten your route definitions into a simple list.
- Rank & match the URL against that list, choosing the most specific route first.
- Extract any dynamic bits (the parts after `:`) into a params object.
- Render the matched components, dropping them into each other via `<Outlet>`.