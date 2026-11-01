import { useMemo, useState } from 'react';
import { MapPin, Navigation, ExternalLink, Phone, ShieldCheck, AlertTriangle, LocateFixed } from 'lucide-react';

const TYPES = [
  {id:'all', label:'All advocates', query:'lawyers advocates'},
  {id:'property', label:'Rent & property', query:'property lawyer tenancy rental deposit advocate'},
  {id:'labour', label:'Wages & employment', query:'labour lawyer employment lawyer advocate'},
  {id:'harassment', label:'Workplace harassment', query:'workplace harassment lawyer POSH advocate'},
  {id:'legal-aid', label:'Free legal aid', query:'District Legal Services Authority legal aid office'},
];

export default function LawyerFinder({ state='Karnataka' }) {
  const [coords,setCoords] = useState(null);
  const [place,setPlace] = useState('');
  const [kind,setKind] = useState('all');
  const [radius,setRadius] = useState('10');
  const [status,setStatus] = useState('');
  const [loading,setLoading] = useState(false);
  const selected = TYPES.find(t=>t.id===kind) || TYPES[0];
  const locationLabel = useMemo(()=>coords ? `${coords.latitude.toFixed(5)}, ${coords.longitude.toFixed(5)}` : place.trim(),[coords,place]);
  const mapsUrl = useMemo(()=>{
    const distanceText = radius === 'any' ? '' : ` within ${radius} km of`;
    const search = `${selected.query}${distanceText} near ${locationLabel || state}`;
    const params = new URLSearchParams({api:'1',query:search});
    if(coords) params.set('query', `${selected.query}${distanceText} near ${coords.latitude},${coords.longitude}`);
    return `https://www.google.com/maps/search/?${params.toString()}`;
  },[selected,locationLabel,coords,state,radius]);
  function useLocation(){
    setStatus('');
    if(!navigator.geolocation){setStatus('This browser does not support location. Enter a city or area instead.');return;}
    setLoading(true);setStatus('Requesting your location permission…');
    navigator.geolocation.getCurrentPosition(pos=>{
      setCoords({latitude:pos.coords.latitude,longitude:pos.coords.longitude});
      setPlace('');setLoading(false);setStatus('Location ready. Open Google Maps to view nearby listings and their published contact details.');
    },err=>{
      setLoading(false);setStatus(err.code===1?'Location permission was denied. You can enter your area manually.':'Could not get your location. Check browser permissions and try again, or enter your area manually.');
    },{enableHighAccuracy:true,timeout:12000,maximumAge:60000});
  }
  function updatePlace(value){setPlace(value);setCoords(null);}
  return <section className="page-content"><div className="page-heading"><MapPin/><div><h1>Find legal help nearby</h1><p>Use your current location or enter an area, then open relevant advocate listings in Google Maps.</p></div></div>
    <div className="location-panel"><div className="location-panel-heading"><span className="location-icon"><LocateFixed size={20}/></span><div><strong>Search around your location</strong><p>Your location is used in this browser to build a Maps search. NyayaSetu does not send it to its backend.</p></div></div>
      <button className="primary-button location-button" onClick={useLocation} disabled={loading}><Navigation size={15}/>{loading?'Getting location…':'Use my current location'}</button>
      <div className="location-or"><span>or enter a place manually</span></div>
      <label className="location-label">City, locality or PIN code<input value={place} onChange={e=>updatePlace(e.target.value)} placeholder={`e.g. Bengaluru, ${state}`}/></label>
      <div className="two-fields location-filters"><label>Type of legal help<select value={kind} onChange={e=>setKind(e.target.value)}>{TYPES.map(t=><option value={t.id} key={t.id}>{t.label}</option>)}</select></label><label>Distance preference<select value={radius} onChange={e=>setRadius(e.target.value)}><option value="5">About 5 km</option><option value="10">About 10 km</option><option value="25">About 25 km</option><option value="any">Any distance</option></select></label></div>
      {status&&<p className="location-status" role="status">{status}</p>}
      <a className="primary-button maps-button" href={mapsUrl} target="_blank" rel="noreferrer"><MapPin size={15}/> Search {selected.label.toLowerCase()} on Google Maps <ExternalLink size={14}/></a>
    </div>
    <div className="maps-info-grid"><article className="lawyer-card"><div className="verified-label"><Phone size={14}/> Contact details</div><h3>Phone numbers & websites</h3><p>Open a listing in Google Maps to see the business's published phone number, website, address and opening hours, when provided by the listing.</p></article><article className="lawyer-card"><div className="verified-label"><MapPin size={14}/> Directions</div><h3>Location and route</h3><p>Google Maps shows the listed address and can provide directions from your current location. Confirm details before travelling.</p></article></div>
    <div className="legal-aid-callout"><ShieldCheck/><div><strong>Need free or subsidized legal aid?</strong><p>Try the official National Legal Services Authority or your State/District Legal Services Authority. Eligibility conditions may apply.</p><a href="https://nalsa.gov.in/" target="_blank" rel="noreferrer">National Legal Services Authority <ExternalLink size={14}/></a></div></div>
    <div className="warning-card"><AlertTriangle/><p>Google Maps results are third-party listings, not a guarantee of advocate credentials or quality. NyayaSetu does not directly retrieve or verify each listing's phone number. Check enrolment with the relevant State Bar Council, confirm fees in writing and avoid paying before verifying identity. A search radius is a preference; Google Maps may interpret the distance preference differently and controls actual result ordering and distance filters.</p></div>
  </section>;
}
