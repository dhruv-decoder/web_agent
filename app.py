import streamlit as st
from agent import WebQueryAgent
import time

# Page config
st.set_page_config(
    page_title="Web Query Agent",
    page_icon="🌐",
    layout="wide"
)

# Initialize agent
@st.cache_resource
def load_agent():
    return WebQueryAgent()

# Title
st.title("🌐 Web Query Agent")
st.markdown("---")

# Sidebar with info
with st.sidebar:
    st.header("ℹ️ About")
    st.markdown("""
    This agent:
    1. ✅ Validates your query
    2. 🔍 Checks for similar past queries
    3. 🌐 Scrapes web if needed
    4. 📝 Summarizes results
    5. 💾 Saves for future use
    """)
    
    st.markdown("---")
    st.markdown("**Examples:**")
    st.code("Best places to visit in Delhi")
    st.code("How to make pasta")
    st.code("Latest AI developments")

# Main interface
query = st.text_input(
    "Enter your query:",
    placeholder="e.g., Best restaurants in Paris",
    help="Ask anything that can be searched on the web"
)

col1, col2 = st.columns([1, 5])
with col1:
    search_button = st.button("🔍 Search", type="primary", use_container_width=True)

if search_button and query:
    agent = load_agent()
    
    # Progress indicators
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    with st.spinner("Processing your query..."):
        # Step-by-step progress
        status_text.text("⏳ Validating query...")
        progress_bar.progress(20)
        time.sleep(0.5)
        
        status_text.text("⏳ Checking cache...")
        progress_bar.progress(40)
        
        # Process query
        result = agent.process_query(query)
        
        progress_bar.progress(100)
        status_text.empty()
        progress_bar.empty()
    
    # Display results
    st.markdown("---")
    
    if result['status'] == 'invalid':
        st.error("❌ Invalid Query")
        st.warning(result['message'])
    
    elif result['status'] == 'cached':
        st.success(f"✅ Found in Cache (Similarity: {result['similarity']:.1%})")
        st.info(f"**Original Query:** {result['original_query']}")
        
        st.subheader("📝 Summary")
        st.write(result['summary'])
        
        with st.expander("ℹ️ Cache Info"):
            st.write(f"**Timestamp:** {result['timestamp']}")
            st.write(f"**Similarity Score:** {result['similarity']:.2%}")
    
    elif result['status'] == 'success':
        st.success("✅ Successfully Processed Query")
        
        st.subheader("📝 Summary")
        st.write(result['summary'])
        
        st.subheader(f"🔗 Sources ({result['num_sources']})")
        for i, url in enumerate(result['sources'], 1):
            st.markdown(f"{i}. [{url}]({url})")
    
    else:
        st.error("❌ Error Processing Query")
        st.write(result.get('message', 'Unknown error occurred'))

elif search_button:
    st.warning("⚠️ Please enter a query")

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: gray;'>Built with LangChain, Playwright, and ChromaDB</div>",
    unsafe_allow_html=True
)