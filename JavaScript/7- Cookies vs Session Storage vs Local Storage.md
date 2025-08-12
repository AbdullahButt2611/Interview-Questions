# Cookies vs Session Storage vs Local Storage
Explain the differences and typical use cases.

`Turing`

## The Big Picture

All three are **ways for a website to store data in your browser** so it can be used later.
Think of your browser as your house, and these three are different **storage rooms** with different rules:

* **Cookies** → Like a tiny mailbox outside your house — the server can read it, write in it, and it’s sent back-and-forth with every request.
* **sessionStorage** → Like a desk drawer you use **only while you’re working** — as soon as you leave (close the browser tab), it’s cleared.
* **localStorage** → Like a closet that **keeps things until you clean them** — data stays even if you close the browser or restart your PC.



## Cookies

**What are they?**

* Small pieces of text data stored in your browser (maximum \~4 KB).
* They’re automatically sent to the server with **every HTTP request** for the same website.
* Can be read by both JavaScript and the server (if not marked as `HttpOnly`).

**Lifetime**

* Can be short-term (session cookies) or long-term (persistent cookies with expiry date).

**Typical Uses**

* **Authentication**: Keeping you logged in (session IDs, tokens).
* **User preferences**: Theme, language.
* **Tracking**: Analytics, ad personalization.

**Pros**

* Server can access them directly.
* Work with older browsers.

**Cons**

* Very small size limit (\~4 KB).
* Sent with every request → adds to network traffic.
* Less secure if not set properly (need HTTPS, Secure, HttpOnly flags).



## sessionStorage

**What is it?**

* A browser storage for **temporary data** tied to the current **tab**.
* Maximum size: \~5–10 MB depending on browser.
* Data is **deleted when the tab is closed**.

**Lifetime**

* Ends when you close the tab/window.

**Typical Uses**

* Temporary state: Form data while filling it out.
* Shopping cart items (if you want them to disappear when user closes the tab).
* Preventing data from being shared across tabs.

**Pros**

* Bigger than cookies (in storage capacity).
* Not sent to the server automatically → faster.
* Isolated to the tab.

**Cons**

* Data gone after tab close.
* Can’t be shared between tabs.



## localStorage

**What is it?**

* Browser storage for **long-term data**.
* Maximum size: \~5–10 MB depending on browser.
* Data **stays until it’s deleted manually** (by code or user clearing browser data).

**Lifetime**

* Persistent — survives browser restarts, PC shutdowns, etc.

**Typical Uses**

* Saving user preferences (theme, layout settings).
* Caching API responses to avoid repeated requests.
* Storing "remember me" type data for faster reload.

**Pros**

* Persistent storage.
* Bigger capacity than cookies.
* Not sent to server → no extra network cost.

**Cons**

* Only accessible via JavaScript (not server).
* Not secure for sensitive data (any script on page can read it if page is compromised).



## Summary Table

| Feature            | Cookies                       | sessionStorage         | localStorage           |
| ------------------ | ----------------------------- | ---------------------- | ---------------------- |
| **Capacity**       | \~4 KB                        | \~5–10 MB              | \~5–10 MB              |
| **Expires**        | Set manually or session end   | Tab close              | Until manually cleared |
| **Accessible by**  | Server & JS (unless HttpOnly) | JS only                | JS only                |
| **Sent to server** | Yes, every request            | No                     | No                     |
| **Scope**          | Domain & path                 | Tab                    | Domain                 |
| **Security**       | Can be secured with flags     | Depends on JS security | Depends on JS security |



**Rule of Thumb**

* **Use cookies** when the server needs the data (e.g., login sessions, CSRF tokens).
* **Use sessionStorage** for temporary tab-specific data.
* **Use localStorage** for persistent, client-only data.