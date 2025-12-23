import streamlit as st
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import TranscriptsDisabled, NoTranscriptFound
import re
import datetime

st.set_page_config(
    page_title="YouTube Transkript",
    page_icon="📝",
    layout="centered"
)

st.title("📝 YouTube Transkript")
st.write("Klistra in en YouTube-länk för att hämta transkriptet.")

url = st.text_input("YouTube-URL", placeholder="https://www.youtube.com/watch?v=...")

if url:
    # Extrahera video-ID
    match = re.search(r"([a-zA-Z0-9_-]{11})", url)
    
    if not match:
        st.error("Kunde inte hitta ett giltigt video-ID i URL:en.")
    else:
        vid = match.group(1)
        
        with st.spinner("Hämtar transkript..."):
            try:
                ytt_api = YouTubeTranscriptApi()

                # Försök hämta svensk transkript först, annars engelska, annars första tillgängliga
                try:
                    t = ytt_api.fetch(vid, languages=["sv", "en"])
                except NoTranscriptFound:
                    t = ytt_api.fetch(vid)

                # Skapa transkripttext
                txt = " ".join([x.text for x in t.snippets])
                
                # Skapa filnamn med datum
                now = datetime.datetime.now().strftime("%Y%m%d_%H%M")
                filename = f"transcript_{vid}_{now}.txt"
                
                st.success(f"Transkript hämtat! ({len(txt)} tecken)")
                
                # Nedladdningsknapp
                st.download_button(
                    label="⬇️ Ladda ner som textfil",
                    data=txt,
                    file_name=filename,
                    mime="text/plain"
                )
                
                # Visa transkriptet
                with st.expander("Visa transkript", expanded=True):
                    st.text_area("", txt, height=400, label_visibility="collapsed")
                    
            except TranscriptsDisabled:
                st.error("Transkript är inaktiverat för denna video.")
            except NoTranscriptFound:
                st.error("Inget transkript hittades för denna video.")
            except Exception as e:
                st.error(f"Ett fel uppstod: {str(e)}")

st.divider()
st.caption("Transkript hämtas via YouTubes automatiska eller manuella undertexter.")
