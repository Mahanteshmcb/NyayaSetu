import { useEffect, useState } from 'react';
import { onAuthStateChanged, signInWithPopup, signInWithEmailAndPassword, createUserWithEmailAndPassword, updateProfile } from 'firebase/auth';
import { Scale, LogIn, Mail } from 'lucide-react';
import { auth, googleProvider, firebaseConfigured } from './firebaseClient';
import './style.css';

export default function AuthGate({ children }) {
  const [user, setUser] = useState(null);
  const [ready, setReady] = useState(!firebaseConfigured);
  const [mode, setMode] = useState('signin');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [name, setName] = useState('');
  const [error, setError] = useState('');
  const [working, setWorking] = useState(false);
  const [localMode, setLocalMode] = useState(false);

  useEffect(() => {
    if (!firebaseConfigured || !auth) return;
    return onAuthStateChanged(auth, next => { setUser(next); setReady(true); });
  }, []);

  async function googleSignIn() {
    setError(''); setWorking(true);
    try { await signInWithPopup(auth, googleProvider); }
    catch (e) { setError(authError(e)); }
    finally { setWorking(false); }
  }
  async function emailSubmit(e) {
    e.preventDefault(); setError(''); setWorking(true);
    try {
      if (mode === 'signup') {
        const credential = await createUserWithEmailAndPassword(auth, email.trim(), password);
        if (name.trim()) await updateProfile(credential.user, { displayName: name.trim() });
      } else await signInWithEmailAndPassword(auth, email.trim(), password);
    } catch (e) { setError(authError(e)); }
    finally { setWorking(false); }
  }
  if (!firebaseConfigured) return <div className="auth-screen"><div className="auth-card"><div className="auth-logo"><Scale size={24}/></div><p className="auth-eyebrow">LEGAL INFORMATION WORKSPACE</p><h1>Set up secure sign-in</h1><p className="auth-description">Connect a Firebase project to enable Google login and account creation for NyayaSetu.</p><div className="setup-steps"><strong>Firebase setup</strong><ol><li>Open <a href="https://console.firebase.google.com/" target="_blank" rel="noreferrer">Firebase Console</a> and create a project.</li><li>In <b>Authentication → Sign-in method</b>, enable Google (and Email/Password if wanted).</li><li>In <b>Project settings → General → Your apps</b>, register a Web app and copy its config values.</li><li>In Authentication → Settings → Authorized domains, add <code>localhost</code> and your production domain.</li><li>Copy <code>frontend/.env.example</code> to <code>frontend/.env</code> and fill in the Firebase values.</li></ol></div><div className="auth-actions"><button className="auth-primary" onClick={()=>window.open('https://console.firebase.google.com/','_blank','noopener,noreferrer')}>Open Firebase Console</button><button className="auth-secondary" onClick={()=>setLocalMode(true)}>Continue in local demo mode</button></div><p className="auth-footnote">Local demo mode does not authenticate users or sync accounts. Configure Firebase before deployment.</p></div>{localMode&&<div className="demo-banner">Local demo mode — sign-in is not enabled. <button onClick={()=>setLocalMode(false)}>Close</button><button onClick={()=>window.location.reload()}>Refresh after setup</button></div>}{localMode&&children}</div>;
  if (!ready) return <div className="auth-screen"><div className="auth-card">Checking your sign-in…</div></div>;
  if (user) return <div className="authenticated-shell">{children}</div>;
  return <div className="auth-screen"><div className="auth-card"><div className="auth-logo"><Scale size={24}/></div><p className="auth-eyebrow">LEGAL INFORMATION WORKSPACE</p><h1>{mode === 'signup' ? 'Create your account' : 'Welcome back'}</h1><p className="auth-description">Sign in to continue to NyayaSetu.</p><button className="google-button" disabled={working} onClick={googleSignIn}><GoogleMark/> Continue with Google</button><div className="auth-divider"><span>or continue with email</span></div><form className="auth-form" onSubmit={emailSubmit}>{mode==='signup'&&<label>Full name<input value={name} onChange={e=>setName(e.target.value)} autoComplete="name" required/></label>}<label>Email address<input type="email" value={email} onChange={e=>setEmail(e.target.value)} autoComplete="email" required/></label><label>Password<input type="password" value={password} onChange={e=>setPassword(e.target.value)} minLength={6} autoComplete={mode==='signup'?'new-password':'current-password'} required/></label><button className="auth-primary" type="submit" disabled={working}>{working?'Please wait…':mode==='signup'?'Create account':'Sign in'}</button></form>{error&&<p className="auth-error" role="alert">{error}</p>}<p className="auth-switch">{mode==='signup'?'Already have an account?':'New to NyayaSetu?'} <button onClick={()=>{setMode(mode==='signup'?'signin':'signup');setError('')}}>{mode==='signup'?'Sign in':'Create account'}</button></p><p className="auth-footnote">Your Google sign-in is handled by Firebase Authentication. Never share passwords or API keys.</p></div></div>;
}
function authError(e) {
  const map = { 'auth/popup-closed-by-user':'The sign-in window was closed before completing login.', 'auth/unauthorized-domain':'This domain is not authorized in Firebase Authentication settings.', 'auth/invalid-credential':'Email or password is incorrect.', 'auth/email-already-in-use':'An account already exists for this email. Try signing in.', 'auth/weak-password':'Use a password with at least 6 characters.', 'auth/popup-blocked':'Your browser blocked the popup. Allow popups and try again.' };
  return map[e?.code] || e?.message || 'Authentication failed. Check Firebase settings and try again.';
}
function GoogleMark(){return <svg width="18" height="18" viewBox="0 0 48 48" aria-hidden="true"><path fill="#EA4335" d="M24 9.5c3.54 0 6.71 1.22 9.21 3.6l6.85-6.85C35.9 2.38 30.47 0 24 0 14.62 0 6.51 5.38 2.56 13.22l7.98 6.19C12.43 13.72 17.74 9.5 24 9.5Z"/><path fill="#4285F4" d="M46.98 24.55c0-1.57-.15-3.09-.38-4.55H24v9.02h12.94c-.58 2.96-2.26 5.48-4.76 7.18l7.73 6C44.42 37.99 46.98 31.87 46.98 24.55Z"/><path fill="#FBBC05" d="M10.53 28.59A14.4 14.4 0 0 1 9.75 24c0-1.59.27-3.13.76-4.59l-7.98-6.2A23.9 23.9 0 0 0 0 24c0 3.87.93 7.52 2.56 10.78l7.97-6.19Z"/><path fill="#34A853" d="M24 48c6.48 0 11.93-2.13 15.91-5.8l-7.73-6c-2.14 1.44-4.89 2.3-8.18 2.3-6.26 0-11.57-4.22-13.47-9.91l-7.98 6.19C6.51 42.62 14.62 48 24 48Z"/></svg>}
