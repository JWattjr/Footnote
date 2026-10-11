import type {Metadata} from 'next';
import '@fontsource/dm-sans/400.css';
import '@fontsource/dm-sans/500.css';
import '@fontsource/dm-sans/600.css';
import '@fontsource/libre-baskerville/400.css';
import './globals.css';
export const metadata:Metadata={title:'Footnote — Follow the evidence',description:'Community notes for Bluesky, judged by GenLayer. Check the sources. Read the history. Keep tone separate from evidence.'};
export default function Layout({children}:{children:React.ReactNode}){return <html lang="en"><body>{children}</body></html>;}
