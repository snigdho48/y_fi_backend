# Privacy Policy — Y FI

**Effective date:** May 3, 2026  

**App name:** Y FI  

**Developer / data controller:** Adcelerate (“we”, “us”).  

**Primary region:** This policy is written for users in **Bangladesh**.  

**Contact (privacy & data requests):** [contact@adcelerate.com](mailto:contact@adcelerate.com)  

---

This Privacy Policy describes how Y FI (“the App”) collects, uses, and shares information when you use our mobile application. By using the App, you agree to this policy. If you do not agree, please do not use the App.

We may update this policy from time to time. We will post the new effective date at the top. Continued use after changes means you accept the updated policy.

---

## Bangladesh — additional notices

### Applicable law

If you use the App **in or from Bangladesh**, our processing of your personal data is subject to **applicable laws and regulations in Bangladesh**, including personal data protection rules in force from time to time (such as instruments adopted under the Digital Security Act framework and **personal data protection ordinances** and related amendments as enacted or updated). This policy is intended to help us meet transparency obligations; it is **not legal advice**. Adcelerate may adjust practices as Bangladesh’s regulatory guidance evolves.

### Your rights (Bangladesh)

Subject to applicable law and verification, users in Bangladesh may have rights that include:

- **Access** to your personal data we hold  
- **Correction** of inaccurate or incomplete data  
- **Deletion** or erasure where applicable  
- **Restriction** of certain processing  
- **Objection** to processing where the law allows  
- Information about **automated decision-making**, where relevant  

To exercise these rights, email us at **contact@adcelerate.com**. We will respond within a reasonable time as required by applicable law. We may need to verify your identity before fulfilling certain requests.

### Children and minors (Bangladesh)

The App is **not directed at young children**. Where Bangladesh law requires **parental or guardian consent** for processing personal data relating to minors, we rely on appropriate consent mechanisms. If you are a parent or guardian and believe your child has provided personal data without consent, contact us at **contact@adcelerate.com**.

### Cross-border transfers

Some of our processors (for example **Google / Firebase**, **Google Ads**, and hosting outside Bangladesh) may process data **outside Bangladesh**. Where the law requires safeguards for transfers, we use appropriate measures offered by those providers and contractual arrangements where applicable. See **International transfers** below.

### Complaints

If you are in Bangladesh and have a concern about how we handle personal data, contact us first at **contact@adcelerate.com**. You may also have the right to lodge a complaint with **competent authorities or mechanisms designated under Bangladesh law** as those frameworks become operational.

---

## 1. Information we collect

### 1.1 You provide or we obtain through sign-in

- **Google sign-in (optional):** If you choose to sign in with Google, we receive information processed by Google and Firebase Authentication, including your Google account email, display name, and a Firebase user identifier used with our backend. That data is sent to our servers at **`https://app.freeyfi.com/api/`** when you complete login (for example to **`auth/login/`**) so we can create or recognize your account and issue an access token stored on your device.
- **Phone sign-in (if enabled in your build):** Firebase may process your phone number for verification. Profile fields available after sign-in may be stored locally as described below.

### 1.2 Device and connection information

The App collects and uses:

- **Device identifiers:** For example, on Android a device identifier exposed via the device info API, and on iOS the vendor identifier where available.
- **Device attributes:** Device manufacturer/model, operating system name and version.
- **Public IP address:** Obtained via a third-party IP lookup service (`dart_ipify` / Ipify) when the App requests device information — used in connection with Wi‑Fi session features.
- **Network state:** Information about connectivity so the App can tell when the device is online for features such as QR-based venue setup.

This information may be stored locally (see section 2) and sent to our servers when you use certain features, for example to **`data/collect/`** (including partner/venue identifiers tied to your session) for operational and session-related purposes.

### 1.3 Wi‑Fi and venue / hotspot usage

- **QR codes:** The App uses the camera to scan QR codes that identify a venue or hotspot. Parsed codes are sent to our backend (**`venue/data/`**) with your authorization token so the App can retrieve Wi‑Fi network details for that venue.
- **Wi‑Fi credentials:** SSID and password may be stored **locally on your device** to reconnect or manage timed sessions. Our systems receive venue/partner identifiers and session-related telemetry as described above; design your backend retention to match your legal obligations.

### 1.4 Permissions (why we ask)

Depending on platform and version, the App may request:

| Permission / capability | Purpose |
|----------------------|---------|
| Internet | Connect to our API, ads, Firebase, and IP lookup. |
| Location (fine/coarse/background where declared) | Required by the OS for Wi‑Fi scanning and connection on many Android versions; may be used for Wi‑Fi-related features. |
| Camera | Scan QR codes for venue Wi‑Fi setup. |
| Nearby Wi‑Fi devices | Wi‑Fi configuration on supported Android versions. |
| Notifications | Show local notifications (e.g. connection status). |
| Foreground service / background work | Timers, reconnection, or background tasks as implemented. |
| **Advertising ID (Android)** | Declared for use with Google advertising services where applicable. |

iOS and Android may show their own permission dialogs; you can control many of these in system settings.

### 1.5 Advertising and analytics (third parties)

- **Google Mobile Ads (AdMob):** The App initializes the Google Mobile Ads SDK and may display ads. Google may use the **advertising ID** (on supported Android versions) and other data as described in Google’s policies. See: [Google’s Privacy & Terms](https://policies.google.com/privacy) and (for ads) [How Google uses information from sites or apps that use our services](https://policies.google.com/technologies/partner-sites).
- **Ad delivery metadata:** The App may request ad configuration from our backend (**`ad/load/`**), including device-related identifiers already collected by the App (such as device id) and optional partner/venue identifiers — so ads can be contextual to the session.

### 1.6 Firebase / Google services

We use **Firebase** (including Authentication and core initialization). Google processes data according to its terms. See: [Google Privacy Policy](https://policies.google.com/privacy) and Firebase documentation.

### 1.7 In-app updates (Android)

On Android, the App may check for updates via Google Play’s in-app update APIs and, when required by our implementation, open the Play Store listing or prompt for an update. Google processes information related to installs and updates under Google’s policies.

### 1.8 Web content in the App

Advertisement or partner content may be shown inside an **in-app WebView**. That content may set cookies or collect information according to the third party’s own policies. We do not control those third-party sites.

---

## 2. Local storage on your device

The App uses on-device storage (e.g. via `GetStorage`) for items such as:

- Authentication **tokens**, **email**, **display name**, **group name**, and related session fields  
- **Wi‑Fi SSID and password** for reconnect flows  
- **Venue/partner identifiers**, connection timestamps, and flags used for session timing  
- **Device id / device profile fields** used for ads and API calls  

Data remains on your device unless transmitted to our servers or third-party services as described above. **Signing out** in the App removes several stored fields locally and signs out of Firebase; you should still treat lost devices as a security risk.

---

## 3. How we use information

We use the information above to:

- Provide login, Wi‑Fi venue connection, timed sessions, and notifications  
- Operate and secure our services and backend API  
- Show advertisements and request ad configuration  
- Improve reliability and troubleshoot issues  

---

## 4. Sharing of information

We may share information with:

- **Service providers** that process data on our behalf (e.g. cloud hosting, Firebase/Google, advertising networks), subject to their terms  
- **Legal or safety reasons** when required by law or to protect rights and safety  

We do not sell your personal information as a standalone commercial product; where regional laws define “sale” broadly (e.g. certain U.S. state laws), review our disclosures in Google Play’s **Data safety** section and applicable regional notices.

---

## 5. Security

We use reasonable measures to protect information in transit and on our systems. No method of transmission or storage is 100% secure.

---

## 6. Children’s privacy (general)

In addition to the **Bangladesh** subsection above: if you believe we have collected data from a child inappropriately, email **contact@adcelerate.com** and we will take appropriate steps.

---

## 7. Your rights and choices

**Bangladesh users:** see **Your rights (Bangladesh)** in the Bangladesh section at the top.

You may also:

- Revoke permissions in device settings  
- Use Google’s [My Ad Center](https://myadcenter.google.com/) and device settings to limit ad personalization where available  
- Uninstall the App  

---

## 8. International transfers

Information may be transferred to and processed in countries **outside Bangladesh** (including where Google and other processors operate). Those countries may have different data protection laws. We rely on provider safeguards (such as contractual terms offered by Google) where applicable. **Bangladesh users:** see **Cross-border transfers** above.

---

## 9. Third-party policies (reference)

- Google / Firebase: https://policies.google.com/privacy  
- Google Play: https://policies.google.com/technologies/partner-sites  

---

## 10. Google Play Console (how to use this policy)

Google requires a **public, working HTTPS link** to your privacy policy (a file on your computer is not enough). Do the following before you submit or update the app:

1. **Publish this document on the web** at a stable address, for example:  
   `https://adcelerate.com/privacy` or `https://www.adcelerate.com/y-fi-privacy`  
   - The page must load without a login.  
   - Use **HTTPS** (not HTTP-only).  
   - You may paste the same Markdown as HTML on your site, or export to HTML/PDF on a public page.

2. **In Play Console**, paste the **same** URL in **both** places (when shown):  
   - **App content** → **Privacy policy**  
   - **Grow** → **Store presence** → **Main store listing** → **Privacy policy URL**  

   Repo guide: `docs/STORE_LISTING_PRIVACY_POLICY_URL.md`.

3. **Data safety form:** In **App content** → **Data safety**, declare the data your app collects and how it is used, so it **matches** this policy and your real backend (types such as **Personal info** (email, name), **Device or other IDs**, **Location** (approximate, if you declare it), **App activity** as applicable, **Advertising ID** for AdMob, etc.). Mismatches between the form, this policy, and the app can cause review issues or policy strikes.

4. **Account & support:** The contact email in this policy is **contact@adcelerate.com**. Keep that inbox monitored for user and Google policy correspondence.

5. **Updates:** When you change data practices, update this policy, the live URL, and the **Data safety** form together.

---

*This document was drafted from a technical review of the Y FI client application and scoped for Bangladesh. Adcelerate should have qualified counsel in Bangladesh review it for compliance with current statutes, ordinances, and regulatory guidance, and you should update section 1 if your server-side processing, retention, or third parties change.*
