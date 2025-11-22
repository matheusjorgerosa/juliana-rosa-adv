import streamlit as st
import os
from transcribe import transcribe_audio
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure page
st.set_page_config(page_title="Transcritor de Áudio", page_icon="🎙️")

def main():
    st.title("🎙️ Transcritor de Áudio com Gemini")
    st.write("Faça upload de um arquivo de áudio para transcrever.")

    # File uploader
    uploaded_file = st.file_uploader("Escolha um arquivo de áudio", type=["mp3", "wav", "m4a", "ogg", "flac"])

    # Custom filename input
    output_filename = st.text_input("Nome do arquivo de saída (sem extensão)", placeholder="Ex: minha_transcricao")

    if uploaded_file is not None:
        st.audio(uploaded_file, format=f"audio/{uploaded_file.name.split('.')[-1]}")

        if st.button("Transcrever"):
            if not output_filename:
                st.warning("Por favor, digite um nome para o arquivo de saída.")
            else:
                with st.spinner("Transcrevendo... Isso pode levar alguns instantes."):
                    try:
                        # Save uploaded file temporarily
                        temp_filename = f"temp_{uploaded_file.name}"
                        with open(temp_filename, "wb") as f:
                            f.write(uploaded_file.getbuffer())

                        # Transcribe
                        # Using default model or allowing user selection could be an enhancement
                        transcription = transcribe_audio(temp_filename)

                        # Display result
                        st.success("Transcrição concluída!")
                        st.text_area("Texto Transcrito:", value=transcription, height=300)

                        # Download button
                        st.download_button(
                            label="📥 Baixar Transcrição",
                            data=transcription,
                            file_name=f"{output_filename}.txt",
                            mime="text/plain"
                        )

                        # Clean up temp file
                        os.remove(temp_filename)

                    except Exception as e:
                        st.error(f"Ocorreu um erro durante a transcrição: {e}")

if __name__ == "__main__":
    main()
