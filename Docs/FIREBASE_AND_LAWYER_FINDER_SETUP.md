# NyayaSetu: Google sign-in and nearby lawyer search

## What is implemented

- Firebase Authentication UI with Google popup sign-in, email/password sign-in and account creation.
- A setup screen when Firebase Web configuration is not present.
- Account strip and sign-out button after sign-in.
- Nearby lawyer finder that requests browser geolocation only after the user presses **Use my current location**. It builds a Google Maps search link for advocates, property lawyers, labour lawyers, workplace-harassment lawyers or legal-aid offices. The app does not send coordinates to the FastAPI backend.
- Maps listings may show phone, address, website and directions when the listing owner/Google has those details. The frontend does not scrape or independently verify listings.

## A. Create a Firebase project

1. Open https://console.firebase.google.com/ and choose **Create a project**.
2. Open **Build → Authentication → Get started**.
3. Under **Sign-in method**, enable **Google** and choose a support email. Optionally enable **Email/Password** for the additional form.
4. Open **Project settings → General → Your apps** and register a **Web app** (the `</>` icon).
5. Copy the web app's `apiKey`, `authDomain`, `projectId` and `appId`. These are Firebase client configuration values, not service-account credentials.
6. Under **Authentication → Settings → Authorized domains**, confirm `localhost` is present for development. Add your production hostname before deployment.

## B. Configure the frontend

From PowerShell in the project root:

```powershell
Copy-Item frontend\.env.example frontend\.env
notepad frontend\.env
```

Fill in:

```dotenv
VITE_API_URL=http://127.0.0.1:8008
VITE_FIREBASE_API_KEY=your_web_api_key
VITE_FIREBASE_AUTH_DOMAIN=your-project-id.firebaseapp.com
VITE_FIREBASE_PROJECT_ID=your-project-id
VITE_FIREBASE_APP_ID=your_web_app_id
```

Save the file. Do not put a Firebase Admin SDK service-account JSON or private key in `frontend/.env`.

Install and run:

```powershell
cd frontend
bun install
bun run dev
```

Restart Vite after changing `.env`. Open the local Vite URL printed by the command (normally http://127.0.0.1:5173).

## C. Test sign-in

- Click **Continue with Google** and choose a Google account.
- Test sign out, then sign in again.
- If the popup is blocked, allow popups for localhost.
- If Firebase says `auth/unauthorized-domain`, add the exact hostname under Authentication → Settings → Authorized domains.
- Email/password signup requires at least 6 characters and Email/Password provider enabled.

## D. Test nearby lawyers

1. Open **Find legal help**.
2. Press **Use my current location** and allow location access in the browser, or enter a city/locality manually.
3. Choose the practice category and open the Google Maps search.
4. Open individual listings to view available phone, website, address and directions. Verify advocate enrolment and fees before hiring.

Browser geolocation requires localhost or HTTPS. On deployed sites, serve the site over HTTPS.

## Important security and product limits

- Firebase currently gates the frontend UI. The existing FastAPI routes have not been changed to verify Firebase ID tokens, so this change alone does **not** secure the backend API against direct requests. Before deploying with private user data, implement backend token verification with Firebase Admin SDK and require valid tokens on protected endpoints. Do not assume a signed-in UI is backend authorization.
- Chat history remains in this browser's local storage, not a cloud-synced account history.
- The lawyer search uses Google Maps search links without a Places API key. Google Maps displays details available in its listings; NyayaSetu does not fetch individual listings or guarantee phone numbers, qualifications, current opening hours, distance radius or quality. For in-app contact cards, configure Google Maps Platform Places API and billing, then build a server-side Places integration that follows Google's terms.
- Never expose server-side API keys or Firebase service-account credentials in Vite `VITE_*` variables.
